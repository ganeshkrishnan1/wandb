"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import grpc
import wandb_internal_pb2
import wandb_server_pb2
import wandb_telemetry_pb2

class InternalServiceStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    RunUpdate: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.RunRecord,
        wandb_internal_pb2.RunUpdateResult,
    ]
    Attach: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.AttachRequest,
        wandb_internal_pb2.AttachResponse,
    ]
    TBSend: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.TBRecord,
        wandb_internal_pb2.TBResult,
    ]
    RunStart: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.RunStartRequest,
        wandb_internal_pb2.RunStartResponse,
    ]
    GetSummary: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.GetSummaryRequest,
        wandb_internal_pb2.GetSummaryResponse,
    ]
    SampledHistory: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.SampledHistoryRequest,
        wandb_internal_pb2.SampledHistoryResponse,
    ]
    PollExit: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.PollExitRequest,
        wandb_internal_pb2.PollExitResponse,
    ]
    ServerInfo: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.ServerInfoRequest,
        wandb_internal_pb2.ServerInfoResponse,
    ]
    Shutdown: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.ShutdownRequest,
        wandb_internal_pb2.ShutdownResponse,
    ]
    RunStatus: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.RunStatusRequest,
        wandb_internal_pb2.RunStatusResponse,
    ]
    RunExit: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.RunExitRecord,
        wandb_internal_pb2.RunExitResult,
    ]
    RunPreempting: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.RunPreemptingRecord,
        wandb_internal_pb2.RunPreemptingResult,
    ]
    Metric: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.MetricRecord,
        wandb_internal_pb2.MetricResult,
    ]
    PartialLog: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.PartialHistoryRequest,
        wandb_internal_pb2.PartialHistoryResponse,
    ]
    Log: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.HistoryRecord,
        wandb_internal_pb2.HistoryResult,
    ]
    Summary: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.SummaryRecord,
        wandb_internal_pb2.SummaryResult,
    ]
    Config: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.ConfigRecord,
        wandb_internal_pb2.ConfigResult,
    ]
    Files: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.FilesRecord,
        wandb_internal_pb2.FilesResult,
    ]
    Output: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.OutputRecord,
        wandb_internal_pb2.OutputResult,
    ]
    OutputRaw: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.OutputRawRecord,
        wandb_internal_pb2.OutputRawResult,
    ]
    Telemetry: grpc.UnaryUnaryMultiCallable[
        wandb_telemetry_pb2.TelemetryRecord,
        wandb_telemetry_pb2.TelemetryResult,
    ]
    Alert: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.AlertRecord,
        wandb_internal_pb2.AlertResult,
    ]
    Artifact: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.ArtifactRecord,
        wandb_internal_pb2.ArtifactResult,
    ]
    LinkArtifact: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.LinkArtifactRecord,
        wandb_internal_pb2.LinkArtifactResult,
    ]
    UseArtifact: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.UseArtifactRecord,
        wandb_internal_pb2.UseArtifactResult,
    ]
    JobInfo: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.JobInfoRequest,
        wandb_internal_pb2.JobInfoResponse,
    ]
    ArtifactSend: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.ArtifactSendRequest,
        wandb_internal_pb2.ArtifactSendResponse,
    ]
    """rpc messages for async operations: Send, Poll, Cancel, Release"""
    ArtifactPoll: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.ArtifactPollRequest,
        wandb_internal_pb2.ArtifactPollResponse,
    ]
    Cancel: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.CancelRequest,
        wandb_internal_pb2.CancelResponse,
    ]
    Keepalive: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.KeepaliveRequest,
        wandb_internal_pb2.KeepaliveResponse,
    ]
    CheckVersion: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.CheckVersionRequest,
        wandb_internal_pb2.CheckVersionResponse,
    ]
    Pause: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.PauseRequest,
        wandb_internal_pb2.PauseResponse,
    ]
    Resume: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.ResumeRequest,
        wandb_internal_pb2.ResumeResponse,
    ]
    Status: grpc.UnaryUnaryMultiCallable[
        wandb_internal_pb2.StatusRequest,
        wandb_internal_pb2.StatusResponse,
    ]
    ServerShutdown: grpc.UnaryUnaryMultiCallable[
        wandb_server_pb2.ServerShutdownRequest,
        wandb_server_pb2.ServerShutdownResponse,
    ]
    ServerStatus: grpc.UnaryUnaryMultiCallable[
        wandb_server_pb2.ServerStatusRequest,
        wandb_server_pb2.ServerStatusResponse,
    ]
    ServerInformInit: grpc.UnaryUnaryMultiCallable[
        wandb_server_pb2.ServerInformInitRequest,
        wandb_server_pb2.ServerInformInitResponse,
    ]
    ServerInformStart: grpc.UnaryUnaryMultiCallable[
        wandb_server_pb2.ServerInformStartRequest,
        wandb_server_pb2.ServerInformStartResponse,
    ]
    ServerInformFinish: grpc.UnaryUnaryMultiCallable[
        wandb_server_pb2.ServerInformFinishRequest,
        wandb_server_pb2.ServerInformFinishResponse,
    ]
    ServerInformAttach: grpc.UnaryUnaryMultiCallable[
        wandb_server_pb2.ServerInformAttachRequest,
        wandb_server_pb2.ServerInformAttachResponse,
    ]
    ServerInformDetach: grpc.UnaryUnaryMultiCallable[
        wandb_server_pb2.ServerInformDetachRequest,
        wandb_server_pb2.ServerInformDetachResponse,
    ]
    ServerInformTeardown: grpc.UnaryUnaryMultiCallable[
        wandb_server_pb2.ServerInformTeardownRequest,
        wandb_server_pb2.ServerInformTeardownResponse,
    ]

class InternalServiceServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def RunUpdate(
        self,
        request: wandb_internal_pb2.RunRecord,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.RunUpdateResult: ...
    @abc.abstractmethod
    def Attach(
        self,
        request: wandb_internal_pb2.AttachRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.AttachResponse: ...
    @abc.abstractmethod
    def TBSend(
        self,
        request: wandb_internal_pb2.TBRecord,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.TBResult: ...
    @abc.abstractmethod
    def RunStart(
        self,
        request: wandb_internal_pb2.RunStartRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.RunStartResponse: ...
    @abc.abstractmethod
    def GetSummary(
        self,
        request: wandb_internal_pb2.GetSummaryRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.GetSummaryResponse: ...
    @abc.abstractmethod
    def SampledHistory(
        self,
        request: wandb_internal_pb2.SampledHistoryRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.SampledHistoryResponse: ...
    @abc.abstractmethod
    def PollExit(
        self,
        request: wandb_internal_pb2.PollExitRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.PollExitResponse: ...
    @abc.abstractmethod
    def ServerInfo(
        self,
        request: wandb_internal_pb2.ServerInfoRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.ServerInfoResponse: ...
    @abc.abstractmethod
    def Shutdown(
        self,
        request: wandb_internal_pb2.ShutdownRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.ShutdownResponse: ...
    @abc.abstractmethod
    def RunStatus(
        self,
        request: wandb_internal_pb2.RunStatusRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.RunStatusResponse: ...
    @abc.abstractmethod
    def RunExit(
        self,
        request: wandb_internal_pb2.RunExitRecord,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.RunExitResult: ...
    @abc.abstractmethod
    def RunPreempting(
        self,
        request: wandb_internal_pb2.RunPreemptingRecord,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.RunPreemptingResult: ...
    @abc.abstractmethod
    def Metric(
        self,
        request: wandb_internal_pb2.MetricRecord,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.MetricResult: ...
    @abc.abstractmethod
    def PartialLog(
        self,
        request: wandb_internal_pb2.PartialHistoryRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.PartialHistoryResponse: ...
    @abc.abstractmethod
    def Log(
        self,
        request: wandb_internal_pb2.HistoryRecord,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.HistoryResult: ...
    @abc.abstractmethod
    def Summary(
        self,
        request: wandb_internal_pb2.SummaryRecord,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.SummaryResult: ...
    @abc.abstractmethod
    def Config(
        self,
        request: wandb_internal_pb2.ConfigRecord,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.ConfigResult: ...
    @abc.abstractmethod
    def Files(
        self,
        request: wandb_internal_pb2.FilesRecord,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.FilesResult: ...
    @abc.abstractmethod
    def Output(
        self,
        request: wandb_internal_pb2.OutputRecord,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.OutputResult: ...
    @abc.abstractmethod
    def OutputRaw(
        self,
        request: wandb_internal_pb2.OutputRawRecord,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.OutputRawResult: ...
    @abc.abstractmethod
    def Telemetry(
        self,
        request: wandb_telemetry_pb2.TelemetryRecord,
        context: grpc.ServicerContext,
    ) -> wandb_telemetry_pb2.TelemetryResult: ...
    @abc.abstractmethod
    def Alert(
        self,
        request: wandb_internal_pb2.AlertRecord,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.AlertResult: ...
    @abc.abstractmethod
    def Artifact(
        self,
        request: wandb_internal_pb2.ArtifactRecord,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.ArtifactResult: ...
    @abc.abstractmethod
    def LinkArtifact(
        self,
        request: wandb_internal_pb2.LinkArtifactRecord,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.LinkArtifactResult: ...
    @abc.abstractmethod
    def UseArtifact(
        self,
        request: wandb_internal_pb2.UseArtifactRecord,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.UseArtifactResult: ...
    @abc.abstractmethod
    def JobInfo(
        self,
        request: wandb_internal_pb2.JobInfoRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.JobInfoResponse: ...
    @abc.abstractmethod
    def ArtifactSend(
        self,
        request: wandb_internal_pb2.ArtifactSendRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.ArtifactSendResponse:
        """rpc messages for async operations: Send, Poll, Cancel, Release"""
    @abc.abstractmethod
    def ArtifactPoll(
        self,
        request: wandb_internal_pb2.ArtifactPollRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.ArtifactPollResponse: ...
    @abc.abstractmethod
    def Cancel(
        self,
        request: wandb_internal_pb2.CancelRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.CancelResponse: ...
    @abc.abstractmethod
    def Keepalive(
        self,
        request: wandb_internal_pb2.KeepaliveRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.KeepaliveResponse: ...
    @abc.abstractmethod
    def CheckVersion(
        self,
        request: wandb_internal_pb2.CheckVersionRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.CheckVersionResponse: ...
    @abc.abstractmethod
    def Pause(
        self,
        request: wandb_internal_pb2.PauseRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.PauseResponse: ...
    @abc.abstractmethod
    def Resume(
        self,
        request: wandb_internal_pb2.ResumeRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.ResumeResponse: ...
    @abc.abstractmethod
    def Status(
        self,
        request: wandb_internal_pb2.StatusRequest,
        context: grpc.ServicerContext,
    ) -> wandb_internal_pb2.StatusResponse: ...
    @abc.abstractmethod
    def ServerShutdown(
        self,
        request: wandb_server_pb2.ServerShutdownRequest,
        context: grpc.ServicerContext,
    ) -> wandb_server_pb2.ServerShutdownResponse: ...
    @abc.abstractmethod
    def ServerStatus(
        self,
        request: wandb_server_pb2.ServerStatusRequest,
        context: grpc.ServicerContext,
    ) -> wandb_server_pb2.ServerStatusResponse: ...
    @abc.abstractmethod
    def ServerInformInit(
        self,
        request: wandb_server_pb2.ServerInformInitRequest,
        context: grpc.ServicerContext,
    ) -> wandb_server_pb2.ServerInformInitResponse: ...
    @abc.abstractmethod
    def ServerInformStart(
        self,
        request: wandb_server_pb2.ServerInformStartRequest,
        context: grpc.ServicerContext,
    ) -> wandb_server_pb2.ServerInformStartResponse: ...
    @abc.abstractmethod
    def ServerInformFinish(
        self,
        request: wandb_server_pb2.ServerInformFinishRequest,
        context: grpc.ServicerContext,
    ) -> wandb_server_pb2.ServerInformFinishResponse: ...
    @abc.abstractmethod
    def ServerInformAttach(
        self,
        request: wandb_server_pb2.ServerInformAttachRequest,
        context: grpc.ServicerContext,
    ) -> wandb_server_pb2.ServerInformAttachResponse: ...
    @abc.abstractmethod
    def ServerInformDetach(
        self,
        request: wandb_server_pb2.ServerInformDetachRequest,
        context: grpc.ServicerContext,
    ) -> wandb_server_pb2.ServerInformDetachResponse: ...
    @abc.abstractmethod
    def ServerInformTeardown(
        self,
        request: wandb_server_pb2.ServerInformTeardownRequest,
        context: grpc.ServicerContext,
    ) -> wandb_server_pb2.ServerInformTeardownResponse: ...

def add_InternalServiceServicer_to_server(servicer: InternalServiceServicer, server: grpc.Server) -> None: ...
