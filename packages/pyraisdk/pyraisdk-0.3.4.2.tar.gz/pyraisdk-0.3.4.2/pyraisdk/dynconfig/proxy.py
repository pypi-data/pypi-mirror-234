
from __future__ import annotations
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
import asyncio
from threading import RLock
import time
from typing import Dict, List, Optional, Tuple, Union
import uuid
from azure.core import MatchConditions
from azure.core.credentials import TokenCredential
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos import aio
from azure.cosmos.container import ContainerProxy
from azure.cosmos.exceptions import (
    CosmosAccessConditionFailedError,
    CosmosResourceNotFoundError,
    CosmosResourceExistsError,
)
from .common import (
    CONTAINER_COMMIT, CONTAINER_META, DATABASE_DYNCONF, PARTITION_KEY_DATA,
    CommitRecord, DataRecord, MetaRecord,
)
from .utils import run_async_batch, Call


# To exclude fields when update to remote cosmos.
FIELDS_EXCLUDE = {'etag', 'ts'}


class RecordExistsException(Exception):
    pass


##
## abstract
##

class DataAccessProxy(ABC):
    @abstractmethod
    def try_get_meta(self, app: str) -> Optional[MetaRecord]:
        ''' Get meta record by app.
            Args:
                app: dynamic config application name
            Returns:
                Got meta record, or None if not found.
        '''
        pass
    
    @abstractmethod
    def create_meta(self, meta: MetaRecord) -> MetaRecord:
        ''' Create meta record.
            Args:
                meta: meta record to create
            Returns:
                Created meta record.
            Raises:
                If meta record already exists, raise RecordExistsException.
        '''
        pass
    
    @abstractmethod
    def update_meta_if_not_modified(self, meta: MetaRecord, etag: str) -> Optional[MetaRecord]:
        ''' Update meta record if given etag matched with remote _etag.
            Args:
                meta: meta record to update
                etag: etag to match
            Returns:
                Updated meta record, or None if etag conflicts.
            Raises:
                If meta record not exists, raise an exception.
        '''
        pass

    @abstractmethod
    def create_commit(self, commit: CommitRecord) -> CommitRecord:
        ''' Create commit record.
            Args:
                commit: commit record to create.
            Returns:
                Created commit record.
            Raises:
                If commit record already exists, raise RecordExistsException.
        '''
        pass
    
    @abstractmethod
    def update_commit(self, commit: CommitRecord) -> CommitRecord:
        ''' Update commit record.
            Args:
                commit: commit record to update.
            Returns:
                Updated commit record.
            Raises:
                If commit record not exists, raise an exception.
        '''
        pass
    
    @abstractmethod
    def batch_delete_commits(self, commits: List[CommitRecord]):
        ''' Delete multiple commit records. Ignore non-existed.
            No requirements for atomic/trasaction.
            Args:
                commits: commit records to delete.
        '''
        pass
    
    @abstractmethod
    def query_commits_by_seq_range(self, app: str, seq_begin: int, seq_end: int) -> List[CommitRecord]:
        ''' Query commit records by sequence range.
            Args:
                app: dynamic config application name.
                seq_begin: begin of sequence range, inclusive.
                seq_end: end of sequence range, inclusive.
            Returns:
                List of queried commit records.
        '''
        pass
    
    @abstractmethod
    def query_data_items_by_commit_ids(self, app: str, commit_ids: List[str]) -> List[DataRecord]:
        ''' Get all the data item records belonging to given commits.
            Args:
                app: dynamic config application name.
                commit_ids: commit ids to query.
            Returns:
                Queried data item records.
        '''
        pass

    @abstractmethod
    def batch_upsert_data_items(self, app: str, data_items: List[DataRecord]):
        ''' Create or update for multiple data item records.
            No requirements for atomic/trasaction.
            Args:
                app: dynamic config application name.
                data_items: data item records to be upserted.
        '''
        pass
    
    @abstractmethod
    def batch_delete_data_items(self, app: str, data_items: List[DataRecord]):
        ''' Delete multiple data item records. Ignore non-existed.
            No requirements for atomic/trasaction.
            Args:
                app: dynamic config application name.
                data_items: data item records to be deleted.
        '''
        pass
    
    def close(self):
        ''' Close proxy to release related resources.
        '''
        pass


##
## stubbed
##

class StubbedDataAccessProxy(DataAccessProxy):
    def __init__(self):
        self._metas: Dict[str, MetaRecord] = {}
        self._commits: Dict[str, CommitRecord] = {}
        self._data_items: Dict[Tuple[str, str], DataRecord] = {}  # {(app, id): record}
        self._lock = RLock()


    def try_get_meta(self, app: str) -> Optional[MetaRecord]:
        meta = self._metas.get(app)
        if meta is None:
            return meta
        else:
            return meta.copy(deep=True)


    def create_meta(self, meta: MetaRecord) -> MetaRecord:
        new = meta.copy(deep=True)
        new.etag = str(uuid.uuid4())
        new.ts = int(time.time())
        with self._lock:
            if new.id in self._metas:
                raise RecordExistsException(f'meta "{new.id}" already exists')
            self._metas[new.id] = new
        return new.copy(deep=True)
            
    
    def update_meta_if_not_modified(self, meta: MetaRecord, etag: str) -> Optional[MetaRecord]:
        new = meta.copy(deep=True)
        new.etag = str(uuid.uuid4())
        new.ts = int(time.time())
        with self._lock:
            old = self._metas.get(meta.id)
            if old is None:
                raise Exception('meta not exists')
            if old.etag != etag:
                return None
            self._metas[new.id] = new
        return new.copy(deep=True)
            

    def create_commit(self, commit: CommitRecord) -> CommitRecord:
        new = commit.copy(deep=True)
        new.etag = str(uuid.uuid4())
        new.ts = int(time.time())
        with self._lock:
            if new.id in self._commits:
                raise RecordExistsException(f'commit "{new.id}" already exists')
            self._commits[new.id] = new
        return new.copy(deep=True)
    
    
    def update_commit(self, commit: CommitRecord) -> CommitRecord:
        new = commit.copy(deep=True)
        new.etag = str(uuid.uuid4())
        new.ts = int(time.time())
        with self._lock:
            if new.id not in self._commits:
                raise Exception('commit not exists')
            self._commits[new.id] = new
        return new.copy(deep=True)

    
    def batch_delete_commits(self, commits: List[CommitRecord]):
        with self._lock:
            for commit in commits:
                if commit.id in self._commits:
                    self._commits.pop(commit.id)


    def query_commits_by_seq_range(self, app: str, seq_begin: int, seq_end: int) -> List[CommitRecord]:
        commits: List[CommitRecord] = []
        with self._lock:
            for commit in self._commits.values():
                if commit.app == app and seq_begin <= commit.seq <= seq_end:
                    commits.append(commit)
        return [c.copy(deep=True) for c in commits]
    
    
    def query_data_items_by_commit_ids(self, app: str, commit_ids: List[str]) -> List[DataRecord]:
        commit_idset = set(commit_ids)
        ditems: List[DataRecord] = []
        with self._lock:
            for (_app, _id), ditem in self._data_items.items():
                if _app == app and ditem.commitId in commit_idset:
                    ditems.append(ditem)
        return [ditem.copy(deep=True) for ditem in ditems]
    
    
    def batch_upsert_data_items(self, app: str, data_items: List[DataRecord]):
        with self._lock:
            for ditem in data_items:
                new = ditem.copy(deep=True)
                new.etag = str(uuid.uuid4())
                new.ts = int(time.time())
                self._data_items[(app, new.id)] = new


    def batch_delete_data_items(self, app: str, data_items: List[DataRecord]):
        with self._lock:
            for ditem in data_items:
                key = (app, ditem.id)
                if key in self._data_items:
                    self._data_items.pop(key)



##
## Cosmos Proxy
##

class CosmosDataAccessProxy(DataAccessProxy):
    ''' Designed for DynamicConfigConsumer.
        Cosmos synchronous client is not good at batch operations, some 
        batch functions are not implemented. Batch functions are only 
        required in DynamicConfigWriter.
    '''
    def __init__(self, client: CosmosClient, dbname: str = DATABASE_DYNCONF):
        ''' Args:
                client: cosmos client.
                dbname: database name. Default: "dynconfig".
        '''
        self._dbname = dbname
        self._client = client
        
        self._proxy_db = self._client.get_database_client(self._dbname)
        self._proxy_meta = self._proxy_db.get_container_client(CONTAINER_META)
        self._proxy_commit = self._proxy_db.get_container_client(CONTAINER_COMMIT)
        self._proxy_data_dict: Dict[str, ContainerProxy] = {}


    def _get_proxy_data(self, app: str) -> ContainerProxy:
        proxy_data = self._proxy_data_dict.get(app)
        if proxy_data is not None:
            return proxy_data
        
        # get container proxy
        assert app not in [CONTAINER_META, CONTAINER_COMMIT]
        proxy_data = self._proxy_db.get_container_client(app)

        self._proxy_data_dict[app] = proxy_data
        return proxy_data


    def try_get_meta(self, app: str) -> Optional[MetaRecord]:
        try:
            resp = self._proxy_meta.read_item(app, partition_key=app)
            return MetaRecord.parse_obj(resp)
        except CosmosResourceNotFoundError:
            return None
        
    
    def create_meta(self, meta: MetaRecord) -> MetaRecord:
        try:
            resp = self._proxy_meta.create_item(meta.dict(exclude=FIELDS_EXCLUDE))
            return MetaRecord.parse_obj(resp)
        except CosmosResourceExistsError as ex:
            raise RecordExistsException(f'meta "{meta.id}" already exists') from ex
    

    def update_meta_if_not_modified(self, meta: MetaRecord, etag: str) -> Optional[MetaRecord]:
        try:
            resp = self._proxy_meta.replace_item(
                meta.id,
                meta.dict(exclude=FIELDS_EXCLUDE),
                etag=etag,
                match_condition=MatchConditions.IfNotModified,
            )
            return MetaRecord.parse_obj(resp)
        except CosmosAccessConditionFailedError:
            return None


    def create_commit(self, commit: CommitRecord) -> CommitRecord:
        try:
            resp = self._proxy_commit.create_item(commit.dict(exclude=FIELDS_EXCLUDE))
            return CommitRecord.parse_obj(resp)
        except CosmosResourceExistsError as ex:
            raise RecordExistsException(f'commit "{commit.id}" already exists') from ex
    

    def update_commit(self, commit: CommitRecord) -> CommitRecord:
        resp = self._proxy_commit.replace_item(commit.id, commit.dict(exclude=FIELDS_EXCLUDE))
        return CommitRecord.parse_obj(resp)
    

    def batch_delete_commits(self, commits: List[CommitRecord]):
        raise NotImplementedError
    

    def query_commits_by_seq_range(self, app: str, seq_begin: int, seq_end: int) -> List[CommitRecord]:
        cursor = self._proxy_commit.query_items(
            'SELECT * FROM c WHERE c.seq between @seqBegin and @seqEnd',
            parameters=[
                dict(name="@seqBegin", value=seq_begin),
                dict(name="@seqEnd", value=seq_end),
            ],
            partition_key=app,
        )
        return [CommitRecord.parse_obj(item) for item in cursor]
    

    def query_data_items_by_commit_ids(self, app: str, commit_ids: List[str]) -> List[DataRecord]:
        proxy_data = self._get_proxy_data(app)
        cursor = proxy_data.query_items(
            'SELECT * FROM c WHERE ARRAY_CONTAINS(@L, c.commitId)',
            parameters=[
                dict(name='@L', value=commit_ids)
            ],
            enable_cross_partition_query=True,
        )
        return [DataRecord.parse_obj(item) for item in cursor]


    def batch_upsert_data_items(self, app: str, data_items: List[DataRecord]):
        raise NotImplementedError
    

    def batch_delete_data_items(self, app: str, data_items: List[DataRecord]):
        raise NotImplementedError
    
    
    
##
## Async Cosmos Proxy
##

class AsyncCosmosDataAccessProxy(DataAccessProxy):
    def __init__(
        self,
        client: aio.CosmosClient,
        loop: AbstractEventLoop,
        lock: RLock,
        dbname: str = DATABASE_DYNCONF,
    ):
        ''' Args:
                client: async cosmos client.
                loop: event loop bind to client.
                lock: lock for event loop.
                dbname: database name. Default: "dynconfig".
        '''
        self._dbname = dbname
        self._client = client
        self._loop = loop
        self._lock = lock
        
        self._proxy_db = self._client.get_database_client(self._dbname)
        self._proxy_meta = self._proxy_db.get_container_client(CONTAINER_META)
        self._proxy_commit = self._proxy_db.get_container_client(CONTAINER_COMMIT)
        self._proxy_data_dict: Dict[str, aio.ContainerProxy] = {}
    
    
    @staticmethod
    def from_cosmos_url(
        url: str,
        credential: Union[str, Dict[str, str], TokenCredential],
        dbname: str = DATABASE_DYNCONF,
    ) -> AsyncCosmosDataAccessProxy:
        ''' Args:
                url: cosmos url.
                credential: token with access. Need to use the async series of token objects, 
                            like `azure.identity.aio.ManagedIdentityCredential`.
                dbname: database name. Default: "dynconfig".
        '''
        client = aio.CosmosClient(url, credential)
        loop = asyncio.get_event_loop()
        lock = RLock()
        return AsyncCosmosDataAccessProxy(client, loop=loop, lock=lock, dbname=dbname)
        
    
    def close(self):
        ''' aio.CosmosClient requires to be closed after finished.
        '''
        with self._lock:
            self._loop.run_until_complete(self._client.close())

    
    def _get_data_proxy(self, app: str) -> aio.ContainerProxy:
        proxy_data = self._proxy_data_dict.get(app)
        if proxy_data is not None:
            return proxy_data
        
        # get container proxy
        assert app not in [CONTAINER_META, CONTAINER_COMMIT]
        proxy_data = self._proxy_db.get_container_client(app)

        self._proxy_data_dict[app] = proxy_data
        return proxy_data
        

    def try_get_meta(self, app: str) -> Optional[MetaRecord]:
        with self._lock:
            try:
                resp = self._loop.run_until_complete(
                    self._proxy_meta.read_item(app, partition_key=app)
                )
                return MetaRecord.parse_obj(resp)
            except CosmosResourceNotFoundError:
                return None

    
    def create_meta(self, meta: MetaRecord) -> MetaRecord:
        with self._lock:
            try:
                resp = self._loop.run_until_complete(
                    self._proxy_meta.create_item(meta.dict(exclude=FIELDS_EXCLUDE))
                )
                return MetaRecord.parse_obj(resp)
            except CosmosResourceExistsError as ex:
                raise RecordExistsException(f'meta "{meta.id}" already exists') from ex
            
    
    def update_meta_if_not_modified(self, meta: MetaRecord, etag: str) -> Optional[MetaRecord]:
        with self._lock:
            try:
                resp = self._loop.run_until_complete(
                    self._proxy_meta.replace_item(
                        meta.id,
                        meta.dict(exclude=FIELDS_EXCLUDE),
                        etag=etag,
                        match_condition=MatchConditions.IfNotModified,
                    )
                )
                return MetaRecord.parse_obj(resp)
            except CosmosAccessConditionFailedError:
                return None
        

    def create_commit(self, commit: CommitRecord) -> CommitRecord:
        with self._lock:
            try:
                resp = self._loop.run_until_complete(
                    self._proxy_commit.create_item(commit.dict(exclude=FIELDS_EXCLUDE))
                )
                return CommitRecord.parse_obj(resp)
            except CosmosResourceExistsError as ex:
                raise RecordExistsException(f'commit "{commit.id}" already exists') from ex
        
    
    def update_commit(self, commit: CommitRecord) -> CommitRecord:
        with self._lock:
            resp = self._loop.run_until_complete(
                self._proxy_commit.replace_item(commit.id, commit.dict(exclude=FIELDS_EXCLUDE))
            )
            return CommitRecord.parse_obj(resp)
        
    
    def batch_delete_commits(self, commits: List[CommitRecord]):
        with self._lock:
            self._loop.run_until_complete(
                self._batch_delete_commits(commits)
            )

    
    async def _batch_delete_commits(self, commits: List[CommitRecord]):
        async def delete_commit(c: CommitRecord):
            try:
                await self._proxy_commit.delete_item(c.id, partition_key=c.app)
            except CosmosResourceNotFoundError:
                pass
        await run_async_batch(
            delete_commit, 
            [Call(c) for c in commits],
        )


    def query_commits_by_seq_range(self, app: str, seq_begin: int, seq_end: int) -> List[CommitRecord]:
        with self._lock:
            return self._loop.run_until_complete(
                self._query_commits_by_seq_range(app, seq_begin, seq_end)
            )
            

    async def _query_commits_by_seq_range(self, app: str, seq_begin: int, seq_end: int) -> List[CommitRecord]:
        cursor = self._proxy_commit.query_items(
            'SELECT * FROM c WHERE c.seq between @seqBegin and @seqEnd',
            parameters=[
                dict(name="@seqBegin", value=seq_begin),
                dict(name="@seqEnd", value=seq_end),
            ],
            partition_key=app,
        )
        commits: List[CommitRecord] = []
        async for item in cursor:
            commits.append(CommitRecord.parse_obj(item))
        return commits
        
    
    def query_data_items_by_commit_ids(self, app: str, commit_ids: List[str]) -> List[DataRecord]:
        with self._lock:
            return self._loop.run_until_complete(
                self._query_data_items_by_commits(app, commit_ids)
            )


    async def _query_data_items_by_commits(self, app: str, commit_ids: List[str]) -> List[DataRecord]:
        proxy_data = self._get_data_proxy(app)
        cursor = proxy_data.query_items(
            'SELECT * FROM c WHERE ARRAY_CONTAINS(@L, c.commitId)',
            parameters=[
                dict(name='@L', value=commit_ids)
            ],
            partition_key=None,
        )
        drs: List[DataRecord] = []
        async for item in cursor:
            d = DataRecord.parse_obj(item)
            drs.append(d)
        return drs


    def batch_upsert_data_items(self, app: str, data_items: List[DataRecord]):
        with self._lock:
            self._loop.run_until_complete(
                self._batch_upsert_data_items(app, data_items)
            )
    
    
    async def _batch_upsert_data_items(self, app: str, data_items: List[DataRecord]):
        proxy_data = self._get_data_proxy(app)
        await run_async_batch(
            proxy_data.upsert_item,
            [Call(d.dict(exclude=FIELDS_EXCLUDE)) for d in data_items],
        )


    def batch_delete_data_items(self, app: str, data_items: List[DataRecord]):
        with self._lock:
            self._loop.run_until_complete(
                self._batch_delete_data_items(app, data_items)
            )
    
    
    async def _batch_delete_data_items(self, app: str, data_items: List[DataRecord]):
        proxy_data = self._get_data_proxy(app)
        async def delete_data_item(d: DataRecord):
            try:
                await proxy_data.delete_item(d.id, partition_key=d.key)
            except CosmosResourceNotFoundError:
                pass
        await run_async_batch(
            delete_data_item, 
            [Call(d) for d in data_items],
        )

