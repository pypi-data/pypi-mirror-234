
from pydantic import BaseModel, Field
from typing import Any


DATABASE_DYNCONF = "dynconfig"
CONTAINER_META = 'dynconf_meta'
CONTAINER_COMMIT= 'dynconf_commit'

PARTITION_KEY_META = 'id'
PARTITION_KEY_COMMIT = 'app'
PARTITION_KEY_DATA = 'key'

MAX_WRITE_CONFLICT_RETRY_COUNT = 20
MAX_COMMIT_DURATION_IN_SECONDS = 3600 * 6
MAX_COMMIT_CHAIN_LENGTH = 20


# logical primary key: id
class MetaRecord(BaseModel):
    # [partition key]
    # format: f'{app}'
    id: str
    # sequence number of top commit in chain
    # initial value: 0
    topSeq: int
    # sequence number of root commit in chain
    # initial value: 1
    rootSeq: int
    # commit id of top commit in chain
    topCommitId: str
    # cosmos provided
    # intentionally not using default values (for _etag & _ts). Want to perform strict 
    # checks on the record from cosmos to ensure that all the fields are correctly provided.
    # same for `CommitRecord` and `DataRecord`.
    etag: str = Field(alias='_etag')
    ts: int = Field(alias='_ts')


# logical primary key: id
class CommitRecord(BaseModel):
    # commit id
    # random generated id, like `uuid4()`
    id: str
    # [partition key]
    # application name
    app: str
    # sequence number of commit in chain
    seq: int
    # commit id of parent commit in chain
    parentId: str
    # external incremental sequence number
    # negative number (like -1) will reset incrementality
    extSeq: int
    # cosmos provided
    etag: str = Field(alias='_etag')
    ts: int = Field(alias='_ts')
    

# logical primary key: commitId + key
class DataRecord(BaseModel):
    # format: f'{key}:{commitId}'
    id: str
    # the commit this data record belongs to
    commitId: str
    # [partition key]
    # key of config item
    key: str
    # value of config item
    value: Any
    # indicates this is a delete operation on the key
    # value will be ignored when deleted is True
    deleted: bool
    # cosmos provided
    etag: str = Field(alias='_etag')
    ts: int = Field(alias='_ts')



#
# A brief structure diagram of the algorithm
#
# +-----------------------+
# |       topSeq: 3       |
# |      rootSeq: 1       |
# | topCommitId: 2de34efe |
# +-----------------------+
#   :
#   : meta
#   v
# +-----------------------+         +--------------------+     +--------------------+
# |        seq: 3         |         | commitId: 2de34efe |     | commitId: 2de34efe |
# |     id: 2de34efe      |         |       key: a       |     |       key: c       |
# |  parentId: 511e31c4   |  data   |     value: 11      |     |    value: null     |
# |                       | ......> |   deleted: false   | ... |   deleted: true    |
# +-----------------------+         +--------------------+     +--------------------+
#   |
#   | commit chain
#   v
# +-----------------------+         +--------------------+     +--------------------+
# |        seq: 2         |         | commitId: 511e31c4 |     | commitId: 511e31c4 |
# |     id: 511e31c4      |         |       key: c       |     |       key: b       |
# |  parentId: f257feb8   |         |     value: 30      |     |     value: 20      |
# |                       | ......> |   deleted: false   | ... |   deleted: false   |
# +-----------------------+         +--------------------+     +--------------------+
#   |
#   |
#   v
# +-----------------------+         +--------------------+
# |        seq: 1         |         | commitId: f257feb8 |
# |     id: f257feb8      |         |       key: a       |
# |     parentId: ''      |         |     value: 10      |
# |                       | ......> |   deleted: false   |
# +-----------------------+         +--------------------+
#
#
# Code for diagram (tool: graph-easy)
# ```
# graph {flow: down}
# [m] {label: "topSeq: 3 \n rootSeq: 1 \n topCommitId: 2de34efe"}
# [c3] {label: "seq: 3 \n id: 2de34efe \n parentId: 511e31c4"}
# [c2] {label: "seq: 2 \n id: 511e31c4 \n parentId: f257feb8"}
# [c1] {label: "seq: 1 \n id: f257feb8 \n parentId: ''"}
# [c3.1] {label: "commitId: 2de34efe \n key: a \n value: 11 \n deleted: false"}
# [c3.2] {label: "commitId: 2de34efe \n key: c \n value: null \n deleted: true"}
# [c2.1] {label: "commitId: 511e31c4 \n key: c \n value: 30 \n deleted: false"}
# [c2.2] {label: "commitId: 511e31c4 \n key: b \n value: 20 \n deleted: false"}
# [c1.1] {label: "commitId: f257feb8 \n key: a \n value: 10 \n deleted: false"}
# [m]  .. meta ..> { flow: down } [c3]  -- commit chain --> { flow: down } [c2] -> { flow: down } [c1]
# [c3] .. data ..> { flow: left } [c3.1]  .. { flow: left } [c3.2]
# [c2] ..> { flow: left } [c2.1]  .. { flow: left } [c2.2]
# [c1] ..> { flow: left } [c1.1]
# ```
#
