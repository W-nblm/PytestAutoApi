# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: upgradeFirmware.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15upgradeFirmware.proto\"L\n\x0eUpgradeRequest\x12\x10\n\x08objDevId\x18\x01 \x01(\t\x12\r\n\x05otaId\x18\x02 \x01(\t\x12\x19\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x0b.FirmwareVo\"O\n\x0fUpgradeResponse\x12\x0e\n\x06result\x18\x01 \x01(\x08\x12\x10\n\x08objDevId\x18\x02 \x01(\t\x12\x0b\n\x03msg\x18\x03 \x01(\t\x12\r\n\x05otaId\x18\x04 \x01(\t\"8\n\nFirmwareVo\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\x05\x12\x0f\n\x07version\x18\x03 \x01(\t\"a\n\x0eUpgradeStateVo\x12\r\n\x05otaId\x18\x01 \x01(\t\x12\x10\n\x08objDevId\x18\x02 \x01(\t\x12\x11\n\tstateType\x18\x03 \x01(\x05\x12\x0e\n\x06status\x18\x04 \x01(\x05\x12\x0b\n\x03msg\x18\x05 \x01(\tB5\n com.szlongzy.common.protobuf.dtoB\x11UpgradeFirmwareVob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'upgradeFirmware_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n com.szlongzy.common.protobuf.dtoB\021UpgradeFirmwareVo'
  _UPGRADEREQUEST._serialized_start=25
  _UPGRADEREQUEST._serialized_end=101
  _UPGRADERESPONSE._serialized_start=103
  _UPGRADERESPONSE._serialized_end=182
  _FIRMWAREVO._serialized_start=184
  _FIRMWAREVO._serialized_end=240
  _UPGRADESTATEVO._serialized_start=242
  _UPGRADESTATEVO._serialized_end=339
# @@protoc_insertion_point(module_scope)
