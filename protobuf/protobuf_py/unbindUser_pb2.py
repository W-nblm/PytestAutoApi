# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: unbindUser.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10unbindUser.proto\"?\n\runbindRequest\x12\x10\n\x08objDevId\x18\x01 \x01(\t\x12\x0f\n\x07\x61uthKey\x18\x02 \x01(\t\x12\x0b\n\x03uid\x18\x05 \x01(\t\"L\n\x0eunbindResponse\x12\x0e\n\x06result\x18\x01 \x01(\x08\x12\x10\n\x08objDevId\x18\x02 \x01(\t\x12\x0b\n\x03msg\x18\x03 \x01(\t\x12\x0b\n\x03uid\x18\x04 \x01(\tB0\n com.szlongzy.common.protobuf.dtoB\x0cUnbindUserVob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'unbindUser_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n com.szlongzy.common.protobuf.dtoB\014UnbindUserVo'
  _UNBINDREQUEST._serialized_start=20
  _UNBINDREQUEST._serialized_end=83
  _UNBINDRESPONSE._serialized_start=85
  _UNBINDRESPONSE._serialized_end=161
# @@protoc_insertion_point(module_scope)
