// Package filestream communicates with the W&B backend filestream service.
package filestream

import (
	"fmt"
	"maps"
	"sync"
	"time"

	"github.com/wandb/wandb/core/internal/api"
	"github.com/wandb/wandb/core/internal/waiting"
	"github.com/wandb/wandb/core/pkg/observability"
	"github.com/wandb/wandb/core/pkg/service"
)

const (
	BufferSize               = 32
	EventsFileName           = "wandb-events.jsonl"
	HistoryFileName          = "wandb-history.jsonl"
	SummaryFileName          = "wandb-summary.json"
	OutputFileName           = "output.log"
	defaultMaxItemsPerPush   = 5_000
	defaultDelayProcess      = 20 * time.Millisecond
	defaultHeartbeatInterval = 30 * time.Second

	// Maximum line length for filestream jsonl files, imposed by the back-end.
	//
	// See https://github.com/wandb/core/pull/7339 for history.
	maxFileLineBytes = (10 << 20) - (100 << 10)
)

type ChunkTypeEnum int8
type FileStreamOffsetMap map[ChunkTypeEnum]int

const (
	NoneChunk ChunkTypeEnum = iota
	HistoryChunk
	OutputChunk
	EventsChunk
	SummaryChunk
)

var chunkFilename = map[ChunkTypeEnum]string{
	HistoryChunk: HistoryFileName,
	OutputChunk:  OutputFileName,
	EventsChunk:  EventsFileName,
	SummaryChunk: SummaryFileName,
}

type FileStream interface {
	// Start asynchronously begins to upload to the backend.
	//
	// All operations are associated with the specified run (defined by
	// `entity`, `project` and `runID`). In case we are resuming a run,
	// the `offsetMap` specifies the initial file offsets for each file
	// type (history, output logs, events, summary).
	Start(
		entity string,
		project string,
		runID string,
		offsetMap FileStreamOffsetMap,
	)

	// Close waits for all work to be completed.
	Close()

	// StreamUpdate uploads information through the filestream API.
	StreamUpdate(update Update)
}

// fileStream is a stream of data to the server
type fileStream struct {
	// The relative path on the server to which to make requests.
	//
	// This must not include the schema and hostname prefix.
	path string

	processChan  chan Update
	feedbackWait *sync.WaitGroup

	// keep track of where we are streaming each file chunk
	offsetMap FileStreamOffsetMap

	// settings is the settings for the filestream
	settings *service.Settings

	// A logger for internal debug logging.
	logger *observability.CoreLogger

	// A way to print console messages to the user.
	printer *observability.Printer

	// The client for making API requests.
	apiClient api.Client

	maxItemsPerPush int
	delayProcess    waiting.Delay

	// A schedule on which to send heartbeats to the backend
	// to prove the run is still alive.
	heartbeatStopwatch waiting.Stopwatch

	clientId string

	// A channel that is closed if there is a fatal error.
	deadChan     chan struct{}
	deadChanOnce *sync.Once
}

type FileStreamParams struct {
	Settings           *service.Settings
	Logger             *observability.CoreLogger
	Printer            *observability.Printer
	ApiClient          api.Client
	MaxItemsPerPush    int
	ClientId           string
	DelayProcess       waiting.Delay
	HeartbeatStopwatch waiting.Stopwatch
}

func NewFileStream(params FileStreamParams) FileStream {
	// Panic early to avoid surprises. These fields are required.
	if params.Logger == nil {
		panic("filestream: nil logger")
	}
	if params.Printer == nil {
		panic("filestream: nil printer")
	}

	fs := &fileStream{
		settings:        params.Settings,
		logger:          params.Logger,
		printer:         params.Printer,
		apiClient:       params.ApiClient,
		processChan:     make(chan Update, BufferSize),
		feedbackWait:    &sync.WaitGroup{},
		offsetMap:       make(FileStreamOffsetMap),
		maxItemsPerPush: defaultMaxItemsPerPush,
		deadChanOnce:    &sync.Once{},
		deadChan:        make(chan struct{}),
	}

	fs.delayProcess = params.DelayProcess
	if fs.delayProcess == nil {
		fs.delayProcess = waiting.NewDelay(defaultDelayProcess)
	}

	fs.heartbeatStopwatch = params.HeartbeatStopwatch
	if fs.heartbeatStopwatch == nil {
		fs.heartbeatStopwatch = waiting.NewStopwatch(defaultHeartbeatInterval)
	}

	if params.MaxItemsPerPush > 0 {
		fs.maxItemsPerPush = params.MaxItemsPerPush
	}

	// TODO: this should become the default
	if fs.settings.GetXShared().GetValue() && params.ClientId != "" {
		fs.clientId = params.ClientId
	}

	return fs
}

func (fs *fileStream) Start(
	entity string,
	project string,
	runID string,
	offsetMap FileStreamOffsetMap,
) {
	fs.logger.Debug("filestream: start", "path", fs.path)

	fs.path = fmt.Sprintf(
		"files/%s/%s/%s/file_stream",
		entity,
		project,
		runID,
	)

	if offsetMap != nil {
		fs.offsetMap = maps.Clone(offsetMap)
	}

	transmitChan := fs.startProcessingUpdates(fs.processChan)
	feedbackChan := fs.startTransmitting(transmitChan)
	fs.startProcessingFeedback(feedbackChan, fs.feedbackWait)
}

func (fs *fileStream) StreamUpdate(update Update) {
	fs.logger.Debug("filestream: stream update", "update", update)
	fs.processChan <- update
}

func (fs *fileStream) Close() {
	close(fs.processChan)
	fs.feedbackWait.Wait()
	fs.logger.Debug("filestream: closed")
}

// logFatalAndStopWorking logs a fatal error and kills the filestream.
//
// After this, most filestream operations are no-ops. This is meant for
// when we can't guarantee correctness, in which case we stop uploading
// data but continue to save it to disk to avoid data loss.
func (fs *fileStream) logFatalAndStopWorking(err error) {
	fs.logger.CaptureFatal("filestream: fatal error", err)
	fs.deadChanOnce.Do(func() {
		close(fs.deadChan)
		fs.printer.Write(
			"Fatal error while uploading data. Some run data will" +
				" not be synced, but it will still be written to disk. Use" +
				" `wandb sync` at the end of the run to try uploading.",
		)
	})
}

// isDead reports whether the filestream has been killed.
func (fs *fileStream) isDead() bool {
	select {
	case <-fs.deadChan:
		return true
	default:
		return false
	}
}
