# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: querys.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cquerys.proto\x12\x07openiap\"-\n\x16ListCollectionsRequest\x12\x13\n\x0bincludehist\x18\x01 \x01(\x08\"*\n\x17ListCollectionsResponse\x12\x0f\n\x07results\x18\x01 \x01(\t\"/\n\x15\x44ropCollectionRequest\x12\x16\n\x0e\x63ollectionname\x18\x01 \x01(\t\"\x18\n\x16\x44ropCollectionResponse\"\x86\x01\n\x0cQueryRequest\x12\r\n\x05query\x18\x01 \x01(\t\x12\x16\n\x0e\x63ollectionname\x18\x02 \x01(\t\x12\x12\n\nprojection\x18\x03 \x01(\t\x12\x0b\n\x03top\x18\x04 \x01(\x05\x12\x0c\n\x04skip\x18\x05 \x01(\x05\x12\x0f\n\x07orderby\x18\x06 \x01(\t\x12\x0f\n\x07queryas\x18\x07 \x01(\t\" \n\rQueryResponse\x12\x0f\n\x07results\x18\x01 \x01(\t\"a\n\x19GetDocumentVersionRequest\x12\x16\n\x0e\x63ollectionname\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\x05\x12\x0f\n\x07\x64\x65\x63rypt\x18\x04 \x01(\x08\",\n\x1aGetDocumentVersionResponse\x12\x0e\n\x06result\x18\x01 \x01(\t\"]\n\x10\x41ggregateRequest\x12\x16\n\x0e\x63ollectionname\x18\x01 \x01(\t\x12\x12\n\naggregates\x18\x02 \x01(\t\x12\x0f\n\x07queryas\x18\x03 \x01(\t\x12\x0c\n\x04hint\x18\x04 \x01(\t\"$\n\x11\x41ggregateResponse\x12\x0f\n\x07results\x18\x01 \x01(\t\"F\n\x0c\x43ountRequest\x12\x16\n\x0e\x63ollectionname\x18\x01 \x01(\t\x12\r\n\x05query\x18\x02 \x01(\t\x12\x0f\n\x07queryas\x18\x03 \x01(\t\"\x1f\n\rCountResponse\x12\x0e\n\x06result\x18\x01 \x01(\x05\"N\n\x10InsertOneRequest\x12\x16\n\x0e\x63ollectionname\x18\x01 \x01(\t\x12\x0c\n\x04item\x18\x02 \x01(\t\x12\t\n\x01w\x18\x03 \x01(\x05\x12\t\n\x01j\x18\x04 \x01(\x08\"#\n\x11InsertOneResponse\x12\x0e\n\x06result\x18\x01 \x01(\t\"e\n\x11InsertManyRequest\x12\x16\n\x0e\x63ollectionname\x18\x01 \x01(\t\x12\r\n\x05items\x18\x02 \x01(\t\x12\t\n\x01w\x18\x03 \x01(\x05\x12\t\n\x01j\x18\x04 \x01(\x08\x12\x13\n\x0bskipresults\x18\x05 \x01(\x08\"%\n\x12InsertManyResponse\x12\x0f\n\x07results\x18\x01 \x01(\t\"N\n\x10UpdateOneRequest\x12\x16\n\x0e\x63ollectionname\x18\x01 \x01(\t\x12\x0c\n\x04item\x18\x02 \x01(\t\x12\t\n\x01w\x18\x03 \x01(\x05\x12\t\n\x01j\x18\x04 \x01(\x08\"#\n\x11UpdateOneResponse\x12\x0e\n\x06result\x18\x01 \x01(\t\"f\n\x15UpdateDocumentRequest\x12\x16\n\x0e\x63ollectionname\x18\x01 \x01(\t\x12\r\n\x05query\x18\x02 \x01(\t\x12\x10\n\x08\x64ocument\x18\x03 \x01(\t\x12\t\n\x01w\x18\x04 \x01(\x05\x12\t\n\x01j\x18\x05 \x01(\x08\"|\n\x0cUpdateResult\x12\x14\n\x0c\x61\x63knowledged\x18\x01 \x01(\x08\x12\x14\n\x0cmatchedCount\x18\x02 \x01(\x05\x12\x15\n\rmodifiedCount\x18\x03 \x01(\x05\x12\x15\n\rupsertedCount\x18\x04 \x01(\x05\x12\x12\n\nupsertedId\x18\x05 \x01(\t\"A\n\x16UpdateDocumentResponse\x12\'\n\x08opresult\x18\x01 \x01(\x0b\x32\x15.openiap.UpdateResult\"i\n\x18InsertOrUpdateOneRequest\x12\x16\n\x0e\x63ollectionname\x18\x01 \x01(\t\x12\x11\n\tuniqeness\x18\x02 \x01(\t\x12\x0c\n\x04item\x18\x03 \x01(\t\x12\t\n\x01w\x18\x04 \x01(\x05\x12\t\n\x01j\x18\x05 \x01(\x08\"+\n\x19InsertOrUpdateOneResponse\x12\x0e\n\x06result\x18\x01 \x01(\t\"\x80\x01\n\x19InsertOrUpdateManyRequest\x12\x16\n\x0e\x63ollectionname\x18\x01 \x01(\t\x12\x11\n\tuniqeness\x18\x02 \x01(\t\x12\r\n\x05items\x18\x03 \x01(\t\x12\t\n\x01w\x18\x04 \x01(\x05\x12\t\n\x01j\x18\x05 \x01(\x08\x12\x13\n\x0bskipresults\x18\x06 \x01(\x08\"-\n\x1aInsertOrUpdateManyResponse\x12\x0f\n\x07results\x18\x01 \x01(\t\"I\n\x10\x44\x65leteOneRequest\x12\x16\n\x0e\x63ollectionname\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x11\n\trecursive\x18\x03 \x01(\x08\")\n\x11\x44\x65leteOneResponse\x12\x14\n\x0c\x61\x66\x66\x65\x63tedrows\x18\x01 \x01(\x05\"Z\n\x11\x44\x65leteManyRequest\x12\x16\n\x0e\x63ollectionname\x18\x01 \x01(\t\x12\r\n\x05query\x18\x02 \x01(\t\x12\x11\n\trecursive\x18\x03 \x01(\x08\x12\x0b\n\x03ids\x18\x04 \x03(\t\"*\n\x12\x44\x65leteManyResponse\x12\x14\n\x0c\x61\x66\x66\x65\x63tedrows\x18\x01 \x01(\x05\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'querys_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LISTCOLLECTIONSREQUEST._serialized_start=25
  _LISTCOLLECTIONSREQUEST._serialized_end=70
  _LISTCOLLECTIONSRESPONSE._serialized_start=72
  _LISTCOLLECTIONSRESPONSE._serialized_end=114
  _DROPCOLLECTIONREQUEST._serialized_start=116
  _DROPCOLLECTIONREQUEST._serialized_end=163
  _DROPCOLLECTIONRESPONSE._serialized_start=165
  _DROPCOLLECTIONRESPONSE._serialized_end=189
  _QUERYREQUEST._serialized_start=192
  _QUERYREQUEST._serialized_end=326
  _QUERYRESPONSE._serialized_start=328
  _QUERYRESPONSE._serialized_end=360
  _GETDOCUMENTVERSIONREQUEST._serialized_start=362
  _GETDOCUMENTVERSIONREQUEST._serialized_end=459
  _GETDOCUMENTVERSIONRESPONSE._serialized_start=461
  _GETDOCUMENTVERSIONRESPONSE._serialized_end=505
  _AGGREGATEREQUEST._serialized_start=507
  _AGGREGATEREQUEST._serialized_end=600
  _AGGREGATERESPONSE._serialized_start=602
  _AGGREGATERESPONSE._serialized_end=638
  _COUNTREQUEST._serialized_start=640
  _COUNTREQUEST._serialized_end=710
  _COUNTRESPONSE._serialized_start=712
  _COUNTRESPONSE._serialized_end=743
  _INSERTONEREQUEST._serialized_start=745
  _INSERTONEREQUEST._serialized_end=823
  _INSERTONERESPONSE._serialized_start=825
  _INSERTONERESPONSE._serialized_end=860
  _INSERTMANYREQUEST._serialized_start=862
  _INSERTMANYREQUEST._serialized_end=963
  _INSERTMANYRESPONSE._serialized_start=965
  _INSERTMANYRESPONSE._serialized_end=1002
  _UPDATEONEREQUEST._serialized_start=1004
  _UPDATEONEREQUEST._serialized_end=1082
  _UPDATEONERESPONSE._serialized_start=1084
  _UPDATEONERESPONSE._serialized_end=1119
  _UPDATEDOCUMENTREQUEST._serialized_start=1121
  _UPDATEDOCUMENTREQUEST._serialized_end=1223
  _UPDATERESULT._serialized_start=1225
  _UPDATERESULT._serialized_end=1349
  _UPDATEDOCUMENTRESPONSE._serialized_start=1351
  _UPDATEDOCUMENTRESPONSE._serialized_end=1416
  _INSERTORUPDATEONEREQUEST._serialized_start=1418
  _INSERTORUPDATEONEREQUEST._serialized_end=1523
  _INSERTORUPDATEONERESPONSE._serialized_start=1525
  _INSERTORUPDATEONERESPONSE._serialized_end=1568
  _INSERTORUPDATEMANYREQUEST._serialized_start=1571
  _INSERTORUPDATEMANYREQUEST._serialized_end=1699
  _INSERTORUPDATEMANYRESPONSE._serialized_start=1701
  _INSERTORUPDATEMANYRESPONSE._serialized_end=1746
  _DELETEONEREQUEST._serialized_start=1748
  _DELETEONEREQUEST._serialized_end=1821
  _DELETEONERESPONSE._serialized_start=1823
  _DELETEONERESPONSE._serialized_end=1864
  _DELETEMANYREQUEST._serialized_start=1866
  _DELETEMANYREQUEST._serialized_end=1956
  _DELETEMANYRESPONSE._serialized_start=1958
  _DELETEMANYRESPONSE._serialized_end=2000
# @@protoc_insertion_point(module_scope)
