# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: wandb/proto/wandb_server.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from wandb.proto import wandb_base_pb2 as wandb_dot_proto_dot_wandb__base__pb2
from wandb.proto import wandb_internal_pb2 as wandb_dot_proto_dot_wandb__internal__pb2
from wandb.proto import wandb_telemetry_pb2 as wandb_dot_proto_dot_wandb__telemetry__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ewandb/proto/wandb_server.proto\x12\x0ewandb_internal\x1a\x1cwandb/proto/wandb_base.proto\x1a wandb/proto/wandb_internal.proto\x1a!wandb/proto/wandb_telemetry.proto\"D\n\x15ServerShutdownRequest\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"\x18\n\x16ServerShutdownResponse\"B\n\x13ServerStatusRequest\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"\x16\n\x14ServerStatusResponse\")\n\x10StringTupleValue\x12\x15\n\rstring_values\x18\x01 \x03(\t\"\xe1\x01\n\rSettingsValue\x12\x13\n\tint_value\x18\x01 \x01(\x03H\x00\x12\x16\n\x0cstring_value\x18\x02 \x01(\tH\x00\x12\x15\n\x0b\x66loat_value\x18\x03 \x01(\x01H\x00\x12\x14\n\nbool_value\x18\x04 \x01(\x08H\x00\x12\x14\n\nnull_value\x18\x05 \x01(\x08H\x00\x12\x37\n\x0btuple_value\x18\x06 \x01(\x0b\x32 .wandb_internal.StringTupleValueH\x00\x12\x19\n\x0ftimestamp_value\x18\x07 \x01(\tH\x00\x42\x0c\n\nvalue_type\"\xea\x01\n\x17ServerInformInitRequest\x12O\n\r_settings_map\x18\x32 \x03(\x0b\x32\x38.wandb_internal.ServerInformInitRequest.SettingsMapEntry\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\x1aQ\n\x10SettingsMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12,\n\x05value\x18\x02 \x01(\x0b\x32\x1d.wandb_internal.SettingsValue:\x02\x38\x01\"\x1a\n\x18ServerInformInitResponse\"\xec\x01\n\x18ServerInformStartRequest\x12P\n\r_settings_map\x18\x32 \x03(\x0b\x32\x39.wandb_internal.ServerInformStartRequest.SettingsMapEntry\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\x1aQ\n\x10SettingsMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12,\n\x05value\x18\x02 \x01(\x0b\x32\x1d.wandb_internal.SettingsValue:\x02\x38\x01\"\x1b\n\x19ServerInformStartResponse\"H\n\x19ServerInformFinishRequest\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"\x1c\n\x1aServerInformFinishResponse\"H\n\x19ServerInformAttachRequest\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"\xf0\x01\n\x1aServerInformAttachResponse\x12R\n\r_settings_map\x18\x32 \x03(\x0b\x32;.wandb_internal.ServerInformAttachResponse.SettingsMapEntry\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\x1aQ\n\x10SettingsMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12,\n\x05value\x18\x02 \x01(\x0b\x32\x1d.wandb_internal.SettingsValue:\x02\x38\x01\"H\n\x19ServerInformDetachRequest\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"\x1c\n\x1aServerInformDetachResponse\"]\n\x1bServerInformTeardownRequest\x12\x11\n\texit_code\x18\x01 \x01(\x05\x12+\n\x05_info\x18\xc8\x01 \x01(\x0b\x32\x1b.wandb_internal._RecordInfo\"\x1e\n\x1cServerInformTeardownResponse\"\xa4\x04\n\rServerRequest\x12\x30\n\x0erecord_publish\x18\x01 \x01(\x0b\x32\x16.wandb_internal.RecordH\x00\x12\x34\n\x12record_communicate\x18\x02 \x01(\x0b\x32\x16.wandb_internal.RecordH\x00\x12>\n\x0binform_init\x18\x03 \x01(\x0b\x32\'.wandb_internal.ServerInformInitRequestH\x00\x12\x42\n\rinform_finish\x18\x04 \x01(\x0b\x32).wandb_internal.ServerInformFinishRequestH\x00\x12\x42\n\rinform_attach\x18\x05 \x01(\x0b\x32).wandb_internal.ServerInformAttachRequestH\x00\x12\x42\n\rinform_detach\x18\x06 \x01(\x0b\x32).wandb_internal.ServerInformDetachRequestH\x00\x12\x46\n\x0finform_teardown\x18\x07 \x01(\x0b\x32+.wandb_internal.ServerInformTeardownRequestH\x00\x12@\n\x0cinform_start\x18\x08 \x01(\x0b\x32(.wandb_internal.ServerInformStartRequestH\x00\x42\x15\n\x13server_request_type\"\xb0\x04\n\x0eServerResponse\x12\x34\n\x12result_communicate\x18\x02 \x01(\x0b\x32\x16.wandb_internal.ResultH\x00\x12H\n\x14inform_init_response\x18\x03 \x01(\x0b\x32(.wandb_internal.ServerInformInitResponseH\x00\x12L\n\x16inform_finish_response\x18\x04 \x01(\x0b\x32*.wandb_internal.ServerInformFinishResponseH\x00\x12L\n\x16inform_attach_response\x18\x05 \x01(\x0b\x32*.wandb_internal.ServerInformAttachResponseH\x00\x12L\n\x16inform_detach_response\x18\x06 \x01(\x0b\x32*.wandb_internal.ServerInformDetachResponseH\x00\x12P\n\x18inform_teardown_response\x18\x07 \x01(\x0b\x32,.wandb_internal.ServerInformTeardownResponseH\x00\x12J\n\x15inform_start_response\x18\x08 \x01(\x0b\x32).wandb_internal.ServerInformStartResponseH\x00\x42\x16\n\x14server_response_type2\x9b\x1a\n\x0fInternalService\x12I\n\tRunUpdate\x12\x19.wandb_internal.RunRecord\x1a\x1f.wandb_internal.RunUpdateResult\"\x00\x12I\n\x06\x41ttach\x12\x1d.wandb_internal.AttachRequest\x1a\x1e.wandb_internal.AttachResponse\"\x00\x12>\n\x06TBSend\x12\x18.wandb_internal.TBRecord\x1a\x18.wandb_internal.TBResult\"\x00\x12O\n\x08RunStart\x12\x1f.wandb_internal.RunStartRequest\x1a .wandb_internal.RunStartResponse\"\x00\x12U\n\nGetSummary\x12!.wandb_internal.GetSummaryRequest\x1a\".wandb_internal.GetSummaryResponse\"\x00\x12\x61\n\x0eSampledHistory\x12%.wandb_internal.SampledHistoryRequest\x1a&.wandb_internal.SampledHistoryResponse\"\x00\x12O\n\x08PollExit\x12\x1f.wandb_internal.PollExitRequest\x1a .wandb_internal.PollExitResponse\"\x00\x12U\n\nServerInfo\x12!.wandb_internal.ServerInfoRequest\x1a\".wandb_internal.ServerInfoResponse\"\x00\x12I\n\x06GetRun\x12\x1d.wandb_internal.GetRunRequest\x1a\x1e.wandb_internal.GetRunResponse\"\x00\x12O\n\x08Shutdown\x12\x1f.wandb_internal.ShutdownRequest\x1a .wandb_internal.ShutdownResponse\"\x00\x12I\n\x07RunExit\x12\x1d.wandb_internal.RunExitRecord\x1a\x1d.wandb_internal.RunExitResult\"\x00\x12[\n\rRunPreempting\x12#.wandb_internal.RunPreemptingRecord\x1a#.wandb_internal.RunPreemptingResult\"\x00\x12\x46\n\x06Metric\x12\x1c.wandb_internal.MetricRecord\x1a\x1c.wandb_internal.MetricResult\"\x00\x12]\n\nPartialLog\x12%.wandb_internal.PartialHistoryRequest\x1a&.wandb_internal.PartialHistoryResponse\"\x00\x12\x45\n\x03Log\x12\x1d.wandb_internal.HistoryRecord\x1a\x1d.wandb_internal.HistoryResult\"\x00\x12I\n\x07Summary\x12\x1d.wandb_internal.SummaryRecord\x1a\x1d.wandb_internal.SummaryResult\"\x00\x12\x46\n\x06\x43onfig\x12\x1c.wandb_internal.ConfigRecord\x1a\x1c.wandb_internal.ConfigResult\"\x00\x12\x43\n\x05\x46iles\x12\x1b.wandb_internal.FilesRecord\x1a\x1b.wandb_internal.FilesResult\"\x00\x12\x46\n\x06Output\x12\x1c.wandb_internal.OutputRecord\x1a\x1c.wandb_internal.OutputResult\"\x00\x12O\n\tOutputRaw\x12\x1f.wandb_internal.OutputRawRecord\x1a\x1f.wandb_internal.OutputRawResult\"\x00\x12O\n\tTelemetry\x12\x1f.wandb_internal.TelemetryRecord\x1a\x1f.wandb_internal.TelemetryResult\"\x00\x12\x43\n\x05\x41lert\x12\x1b.wandb_internal.AlertRecord\x1a\x1b.wandb_internal.AlertResult\"\x00\x12L\n\x08\x41rtifact\x12\x1e.wandb_internal.ArtifactRecord\x1a\x1e.wandb_internal.ArtifactResult\"\x00\x12X\n\x0cLinkArtifact\x12\".wandb_internal.LinkArtifactRecord\x1a\".wandb_internal.LinkArtifactResult\"\x00\x12[\n\x0c\x41rtifactSend\x12#.wandb_internal.ArtifactSendRequest\x1a$.wandb_internal.ArtifactSendResponse\"\x00\x12[\n\x0c\x41rtifactPoll\x12#.wandb_internal.ArtifactPollRequest\x1a$.wandb_internal.ArtifactPollResponse\"\x00\x12R\n\tKeepalive\x12 .wandb_internal.KeepaliveRequest\x1a!.wandb_internal.KeepaliveResponse\"\x00\x12[\n\x0c\x43heckVersion\x12#.wandb_internal.CheckVersionRequest\x1a$.wandb_internal.CheckVersionResponse\"\x00\x12\x46\n\x05Pause\x12\x1c.wandb_internal.PauseRequest\x1a\x1d.wandb_internal.PauseResponse\"\x00\x12I\n\x06Resume\x12\x1d.wandb_internal.ResumeRequest\x1a\x1e.wandb_internal.ResumeResponse\"\x00\x12I\n\x06Status\x12\x1d.wandb_internal.StatusRequest\x1a\x1e.wandb_internal.StatusResponse\"\x00\x12\x61\n\x0eServerShutdown\x12%.wandb_internal.ServerShutdownRequest\x1a&.wandb_internal.ServerShutdownResponse\"\x00\x12[\n\x0cServerStatus\x12#.wandb_internal.ServerStatusRequest\x1a$.wandb_internal.ServerStatusResponse\"\x00\x12g\n\x10ServerInformInit\x12\'.wandb_internal.ServerInformInitRequest\x1a(.wandb_internal.ServerInformInitResponse\"\x00\x12j\n\x11ServerInformStart\x12(.wandb_internal.ServerInformStartRequest\x1a).wandb_internal.ServerInformStartResponse\"\x00\x12m\n\x12ServerInformFinish\x12).wandb_internal.ServerInformFinishRequest\x1a*.wandb_internal.ServerInformFinishResponse\"\x00\x12m\n\x12ServerInformAttach\x12).wandb_internal.ServerInformAttachRequest\x1a*.wandb_internal.ServerInformAttachResponse\"\x00\x12m\n\x12ServerInformDetach\x12).wandb_internal.ServerInformDetachRequest\x1a*.wandb_internal.ServerInformDetachResponse\"\x00\x12s\n\x14ServerInformTeardown\x12+.wandb_internal.ServerInformTeardownRequest\x1a,.wandb_internal.ServerInformTeardownResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'wandb.proto.wandb_server_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SERVERINFORMINITREQUEST_SETTINGSMAPENTRY._options = None
  _SERVERINFORMINITREQUEST_SETTINGSMAPENTRY._serialized_options = b'8\001'
  _SERVERINFORMSTARTREQUEST_SETTINGSMAPENTRY._options = None
  _SERVERINFORMSTARTREQUEST_SETTINGSMAPENTRY._serialized_options = b'8\001'
  _SERVERINFORMATTACHRESPONSE_SETTINGSMAPENTRY._options = None
  _SERVERINFORMATTACHRESPONSE_SETTINGSMAPENTRY._serialized_options = b'8\001'
  _SERVERSHUTDOWNREQUEST._serialized_start=149
  _SERVERSHUTDOWNREQUEST._serialized_end=217
  _SERVERSHUTDOWNRESPONSE._serialized_start=219
  _SERVERSHUTDOWNRESPONSE._serialized_end=243
  _SERVERSTATUSREQUEST._serialized_start=245
  _SERVERSTATUSREQUEST._serialized_end=311
  _SERVERSTATUSRESPONSE._serialized_start=313
  _SERVERSTATUSRESPONSE._serialized_end=335
  _STRINGTUPLEVALUE._serialized_start=337
  _STRINGTUPLEVALUE._serialized_end=378
  _SETTINGSVALUE._serialized_start=381
  _SETTINGSVALUE._serialized_end=606
  _SERVERINFORMINITREQUEST._serialized_start=609
  _SERVERINFORMINITREQUEST._serialized_end=843
  _SERVERINFORMINITREQUEST_SETTINGSMAPENTRY._serialized_start=762
  _SERVERINFORMINITREQUEST_SETTINGSMAPENTRY._serialized_end=843
  _SERVERINFORMINITRESPONSE._serialized_start=845
  _SERVERINFORMINITRESPONSE._serialized_end=871
  _SERVERINFORMSTARTREQUEST._serialized_start=874
  _SERVERINFORMSTARTREQUEST._serialized_end=1110
  _SERVERINFORMSTARTREQUEST_SETTINGSMAPENTRY._serialized_start=762
  _SERVERINFORMSTARTREQUEST_SETTINGSMAPENTRY._serialized_end=843
  _SERVERINFORMSTARTRESPONSE._serialized_start=1112
  _SERVERINFORMSTARTRESPONSE._serialized_end=1139
  _SERVERINFORMFINISHREQUEST._serialized_start=1141
  _SERVERINFORMFINISHREQUEST._serialized_end=1213
  _SERVERINFORMFINISHRESPONSE._serialized_start=1215
  _SERVERINFORMFINISHRESPONSE._serialized_end=1243
  _SERVERINFORMATTACHREQUEST._serialized_start=1245
  _SERVERINFORMATTACHREQUEST._serialized_end=1317
  _SERVERINFORMATTACHRESPONSE._serialized_start=1320
  _SERVERINFORMATTACHRESPONSE._serialized_end=1560
  _SERVERINFORMATTACHRESPONSE_SETTINGSMAPENTRY._serialized_start=762
  _SERVERINFORMATTACHRESPONSE_SETTINGSMAPENTRY._serialized_end=843
  _SERVERINFORMDETACHREQUEST._serialized_start=1562
  _SERVERINFORMDETACHREQUEST._serialized_end=1634
  _SERVERINFORMDETACHRESPONSE._serialized_start=1636
  _SERVERINFORMDETACHRESPONSE._serialized_end=1664
  _SERVERINFORMTEARDOWNREQUEST._serialized_start=1666
  _SERVERINFORMTEARDOWNREQUEST._serialized_end=1759
  _SERVERINFORMTEARDOWNRESPONSE._serialized_start=1761
  _SERVERINFORMTEARDOWNRESPONSE._serialized_end=1791
  _SERVERREQUEST._serialized_start=1794
  _SERVERREQUEST._serialized_end=2342
  _SERVERRESPONSE._serialized_start=2345
  _SERVERRESPONSE._serialized_end=2905
  _INTERNALSERVICE._serialized_start=2908
  _INTERNALSERVICE._serialized_end=6263
# @@protoc_insertion_point(module_scope)
