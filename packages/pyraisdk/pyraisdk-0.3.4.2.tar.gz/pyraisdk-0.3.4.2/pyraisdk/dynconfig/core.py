
from __future__ import annotations
import json
from threading import RLock
import time
from typing import Any, Dict, List, Optional, Set
import uuid
from azure.cosmos import CosmosClient
from .proxy import (
    AsyncCosmosDataAccessProxy, 
    CosmosDataAccessProxy, 
    DataAccessProxy, 
    RecordExistsException,
)
from .common import (
    MAX_COMMIT_CHAIN_LENGTH,
    MAX_COMMIT_DURATION_IN_SECONDS,
    MAX_WRITE_CONFLICT_RETRY_COUNT,
    CommitRecord,
    DataRecord, 
    MetaRecord,
)


class ExternalSequenceError(Exception):
    pass


# ChangeSet is for data implicitly. Not for meta or commit.
class ChangeSet:
    def __init__(self):
        self._updates: Dict[str, Any] = {}
        self._deletions: Set[str] = set()

    @property
    def updates(self) -> Dict[str, Any]:
        return self._updates
    
    @property
    def deletions(self) -> Set[str]:
        return self._deletions
    
    @property
    def count(self) -> int:
        return len(self._updates) + len(self._deletions)

    def set(self, key: str, val: Any):
        self._updates[key] = val
        if key in self._deletions:
            self._deletions.remove(key)
            
    def delete(self, key: str):
        self._deletions.add(key)
        if key in self._updates:
            self._updates.pop(key)

    def is_empty(self) -> bool:
        return not self._updates and not self._deletions
    
    def __contains__(self, k: str):
        return k in self._updates or k in self._deletions
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ChangeSet):
            return self._updates == other._updates and self._deletions == other._deletions
        return False

    def apply_on(self, dataset: Dict[str, Any]):
        ''' Apply changeset on the input dataset.
        '''
        dataset.update(self._updates)
        for k in self._deletions:
            if k in dataset:
                dataset.pop(k)

    def update(self, sub: ChangeSet):
        for k, v in sub._updates.items():
            self.set(k, v)
        for k in sub._deletions:
            self.delete(k)

    @classmethod
    def make_from_datasets(cls, src: Dict[str, Any], dst: Dict[str, Any]) -> ChangeSet:
        ''' Compare 2 datasets, and get the changeset from `src` to `dst`.
        '''
        changeset = ChangeSet()
        for key in src.keys() | dst.keys():
            if key in src and key in dst:
                src_val_str = json.dumps(src[key], sort_keys=True)
                dst_val_str = json.dumps(dst[key], sort_keys=True)
                if src_val_str != dst_val_str:
                    changeset.set(key, dst[key])
            elif key in src:
                changeset.delete(key)
            elif key in dst:
                changeset.set(key, dst[key])
        return changeset
    

class CommitChainManager:
    def __init__(self, proxy: DataAccessProxy, app: str):
        self._proxy = proxy
        self._app = app
        self._meta: Optional[MetaRecord] = None
        self._commits: Dict[int, CommitRecord] = {}  # key: seq
    
    
    @property
    def meta(self) -> MetaRecord:
        if self._meta is None: 
            raise Exception('require refresh_chain first')
        return self._meta
    

    @property
    def top_commit(self) -> CommitRecord:
        return self._commits[self.meta.topSeq]


    def get_sub_chain(self, seq_begin: Optional[int] = None, seq_end: Optional[int] = None) -> List[CommitRecord]:
        if seq_begin is None:
            seq_begin = self.meta.rootSeq
        if seq_end is None:
            seq_end = self.meta.topSeq
        return [self._commits[seq] for seq in range(seq_begin, seq_end + 1)]
    
    
    def refresh_chain(self, enable_init: bool = True):
        ''' Update (or initialize) the commit chain to latest.
            Args:
                enable_init: Indicates whether to initialize meta record when it doesn't exist.
                             Will raise Exception when it's False and meta not found.
        '''
        # try to get latest meta
        # when meta not exist, try to create initial meta, if enable_init.
        meta = self._proxy.try_get_meta(self._app)
        if meta is None:
            if self._meta is not None:
                # Won't happen unless cosmosdb records are manually deleted.
                raise Exception(f'unexpected error to get meta record "{self._app}"')
            elif not enable_init:
                raise Exception(f'meta record {self._app} does not exist')
            else:
                # create meta
                try:
                    meta = self._proxy.create_meta(
                        MetaRecord(
                            id=self._app, 
                            topSeq=0,
                            rootSeq=1,
                            topCommitId='',
                            _etag='',
                            _ts=0,
                        )
                    )
                except RecordExistsException:
                    # already exists, try get again
                    meta = self._proxy.try_get_meta(self._app)
                    if meta is None:
                        raise Exception(f'unexpected error for existed meta record {self._app}')
        
        # topSeq check for robustness, expect always meet.
        # But if somehow happend (can't imagine how), should raise out immediately.
        if self._meta is not None:
            assert self._meta.topSeq <= meta.topSeq

        # seq range of sub chain to fetch
        seq_begin = meta.rootSeq if self._meta is None else self._meta.topSeq + 1
        seq_end = meta.topSeq
        if seq_begin > seq_end:
            self._meta = meta
            return
        
        # query commit records and build chain
        commits = self._proxy.query_commits_by_seq_range(self._app, seq_begin, seq_end)
        chain = self.build_sub_commit_chain(commits, seq_begin, seq_end, meta.topCommitId)
        if self._meta is not None:
            # validate the join point of the chain
            if chain[0].parentId != self._meta.topCommitId or chain[0].seq != self._meta.topSeq + 1:
                raise Exception(f'invalid commit {self._meta.topCommitId} at seq {self._meta.topSeq}')

        # update
        self._commits.update({c.seq: c for c in chain})
        self._meta = meta


    def create_commit(self, ext_seq: int) -> CommitRecord:
        commit_req = CommitRecord(
            id=str(uuid.uuid4()),
            app=self._app,
            seq=self.meta.topSeq + 1,
            parentId=self.meta.topCommitId,
            extSeq=ext_seq,
            _etag='',
            _ts=0,
        )
        return self._proxy.create_commit(commit_req)


    def submit_change(self, commit: CommitRecord, squash: bool = False) -> bool:
        ''' Try to submit commit.
            Returns:
                True: success
                False: indicates etag conflict
        '''
        # validate commit not submitted, for robustness
        # assume it was success, but we got an error caused by any reason
        sub_chain = self.get_sub_chain(seq_begin=commit.seq)
        if commit.id in (c.id for c in sub_chain):
            raise Exception(f'commit {commit.id} already submitted')

        # update commit
        if commit.seq != self.meta.topSeq + 1:
            commit.seq = self.meta.topSeq + 1
            commit.parentId = self.meta.topCommitId
            self._proxy.update_commit(commit)
        
        # update meta from commit
        meta_req = self.meta.copy()
        meta_req.topSeq = commit.seq
        meta_req.topCommitId = commit.id
        if squash:
            meta_req.rootSeq = meta_req.topSeq
        
        meta_resp = self._proxy.update_meta_if_not_modified(meta_req, meta_req.etag)
        return meta_resp is not None


    # This method does not mutate the state of chain manager.
    def fetch_changeset_of_chain(self, from_seq: int) -> ChangeSet:
        ''' Get the changeset from `from_seq` to `topSeq`.
            `from_seq` == 0 indicates it's in full mode.
        '''
        seq_begin = self.meta.rootSeq if from_seq == 0 else from_seq
        seq_end = self.meta.topSeq
        if seq_begin > seq_end:
            return ChangeSet()

        # get commit chain
        sub_chain: List[CommitRecord] = self.get_sub_chain(seq_begin, seq_end)
        id_commits: Dict[str, CommitRecord] = {c.id: c for c in sub_chain}
        
        # data query
        data_items = self._proxy.query_data_items_by_commit_ids(self._app, [c.id for c in sub_chain])

        # build changeset
        key_item: Dict[str, DataRecord] = {}
        key_seq: Dict[str, int] = {}
        for ditem in data_items:
            commit = id_commits.get(ditem.commitId)
            assert commit is not None
            if commit.seq > key_seq.get(ditem.key, 0):
                key_item[ditem.key] = ditem
                key_seq[ditem.key] = commit.seq
                
        changeset = ChangeSet()
        for ditem in key_item.values():
            if ditem.deleted:
                changeset.delete(ditem.key)
            else:
                changeset.set(ditem.key, ditem.value)

        return changeset


    def put_changeset_into_commit(self, commit: CommitRecord, changeset: ChangeSet):
        if changeset.is_empty():
            return
        
        # build data records
        data_items: List[DataRecord] = []
        for k, v in changeset.updates.items():
            ditem = DataRecord(
                id=f'{k}:{commit.id}',
                commitId=commit.id,
                key=k,
                value=v,
                deleted=False,
                _etag='',   # placeholder; set by Cosmos DB server
                _ts=0,
            )
            data_items.append(ditem)
        
        for k in changeset.deletions:
            ditem = DataRecord(
                id=f'{k}:{commit.id}',
                commitId=commit.id,
                key=k,
                value=None,
                deleted=True,
                _etag='',
                _ts=0,
            )
            data_items.append(ditem)
        
        # upsert items
        self._proxy.batch_upsert_data_items(self._app, data_items)


    def validate_ext_seq_inc(self, ext_seq: int):
        ''' Verify the incrementality of the external sequence
        '''
        if self.meta.topSeq == 0 or ext_seq < 0:
            return
        commit = self._commits[self.meta.topSeq]
        if ext_seq <= commit.extSeq:
            raise ExternalSequenceError(f'external seq violate incremental constraint: {commit.extSeq} to {ext_seq}') 


    @staticmethod
    def build_sub_commit_chain(
        commits: List[CommitRecord], seq_begin: int, seq_end: int, end_commit_id: str
    ) -> List[CommitRecord]:
        ''' Build commit chain.
            Return commit records in order from `seq_begin` to `seq_end`.
        '''
        assert seq_begin >= 1
        commitdict = {c.id: c for c in commits}
        chain = []
        commit_id = end_commit_id
        # After the loop completes, all transient commit records will be removed.
        for seq in range(seq_end, seq_begin - 1, -1):
            commit = commitdict.get(commit_id)
            if commit is None or commit.seq != seq:
                # Not expected error point.
                # Only if someone deliberately messes with the data.
                raise Exception(f'invalid commit {commit_id} at seq {seq}')
            chain.append(commit)
            commit_id = commit.parentId
        chain.reverse()
        return chain


class DynamicConfigWriter:
    ''' It should be created with `AsyncCosmosDataAccessProxy` in Prod.
    
        Csomos async client has high write performance, but there are more
        restrictive conditions to use it. Mainly they are:
        1. It's hard to be used in a multi-threaded environment. You have 
           to face unexpected errors.
        2. Cosmos async client will be bind to the event loop after the 
           first execution, and unable to replace it again.
    '''
    
    def __init__(
        self,
        proxy: DataAccessProxy,
        app: str,
    ):
        self._chainman = CommitChainManager(proxy, app)
        self._lock = RLock()
    
    
    @staticmethod
    def make(proxy: AsyncCosmosDataAccessProxy, app: str):
        ''' Make a writer with `AsyncCosmosDataAccessProxy`.
            Should use this instead of `__init__` in Prod.
        '''
        return DynamicConfigWriter(proxy, app)


    def reconcile(self, dataset: Dict[str, Any], ext_seq: Optional[int] = None) -> ChangeSet:
        ''' Make remote dataset consistent with input `dataset`. 
            Success of reconcile guarantee at that moment remote dataset
            is completely same with local input `dataset`.
            
            Args:
                dataset: Local full dataset to sync to remote.
                ext_seq: An extra external sequence. For provided values, require
                        them to be incremental in commit chain.
            
            Returns:
                The changeset updated to remote in new commit.
        '''
        with self._lock:
            return self._reconcile(dataset, ext_seq)
    
    
    def gc(self):
        ''' Garbage collect.
            Can be executed at any time. Include 2 steps:
            1. sqaush commit chain`
            2. collect commit garbage
        '''
        with self._lock:
            self._squash_commit_chain()
            self._collect_commit_garbage()
    
    
    def _reconcile(self, dataset: Dict[str, Any], ext_seq: Optional[int] = None) -> ChangeSet:
        # ext_seq
        if ext_seq is None:
            ext_seq = -1
        else:
            assert ext_seq >= 0

        # initialize
        next_pull_seq = 0
        remote_dataset = {}
        commit_changeset = ChangeSet()
        commit: CommitRecord = None  # type: ignore
        ts_start = time.time()
        
        for trial in range(MAX_WRITE_CONFLICT_RETRY_COUNT):
            self._chainman.refresh_chain()

            # has more remote data
            if next_pull_seq <= self._chainman.meta.topSeq:
                # get data
                pulled_data = self._chainman.fetch_changeset_of_chain(next_pull_seq)
                next_pull_seq = self._chainman.meta.topSeq + 1
                pulled_data.apply_on(remote_dataset)

                # get delta
                if trial == 0:
                    # full delta, for first time
                    delta = ChangeSet.make_from_datasets(remote_dataset, dataset)
                    if delta.is_empty():
                        # nothing to commit, success automatically
                        return commit_changeset
                else:
                    # incremental delta (save cost of value compare):
                    # 1. only in scope of keys in `pulled_data`
                    # 2. exclude Keys already in `commit_changeset`
                    delta = ChangeSet.make_from_datasets(
                        {k: v for k, v in remote_dataset.items() if k in pulled_data and k not in commit_changeset}, 
                        {k: v for k, v in dataset.items()        if k in pulled_data and k not in commit_changeset}, 
                    )

                # check ext seq
                # It is intentional to put it here, other than after refresh_chain.
                # The purpose is to make it possible to call `reconcile` with exact same 
                # parameters repeatly.
                self._chainman.validate_ext_seq_inc(ext_seq)
                
                # write delta
                if commit is None:
                    commit = self._chainman.create_commit(ext_seq)
                self._chainman.put_changeset_into_commit(commit, delta)
                commit_changeset.update(delta)
            
            # max duration check
            if time.time() - ts_start > MAX_COMMIT_DURATION_IN_SECONDS:
                raise Exception(f'timeout for commit duration')
            
            # try submit
            success = self._chainman.submit_change(commit)
            if success:
                return commit_changeset
                
        raise Exception('exceed max write conflict retries')

    
    def _squash_commit_chain(
        self, 
        max_commit_chain_length: int = MAX_COMMIT_CHAIN_LENGTH,
    ):
        ''' To avoid the commit chain being too long, need to quash the long chain.
            Read out the full dataset from remote, and submit the dataset in one
            commit to overwrite the old data.
        '''
        next_pull_seq = 0
        commit: CommitRecord = None  # type: ignore
        ts_start = time.time()
        
        for trial in range(MAX_WRITE_CONFLICT_RETRY_COUNT):
            self._chainman.refresh_chain(enable_init=False)
            # check chain length
            chain_len = self._chainman.meta.topSeq - self._chainman.meta.rootSeq + 1
            if chain_len <=  max_commit_chain_length:
                return
            
            if commit is None:
                # create commit record
                ext_seq = self._chainman.top_commit.extSeq
                commit = self._chainman.create_commit(ext_seq)
            else:
                # update extSeq
                commit.extSeq = self._chainman.top_commit.extSeq
                
            # has more remote data
            if next_pull_seq <= self._chainman.meta.topSeq:
                # get data
                pulled_data = self._chainman.fetch_changeset_of_chain(next_pull_seq)
                next_pull_seq = self._chainman.meta.topSeq + 1
                
                # remove deletions for first pull (full dataset, trail == 0)
                # the full dataset (ChangeSet) might still include meaningless deletions,
                # excluding them can help to reduce garbage data records in squash commit.
                # PS: The condition was supposed to be `next_pull_seq == 0` here. Since
                #     it's already increased, to avoid introducing an extra variable
                #     like `prev_pull_seq`, using `trial == 0` instead.
                if trial == 0:
                    pulled_data.deletions.clear()
                
                # write data
                self._chainman.put_changeset_into_commit(commit, pulled_data)
                
            # max duration check
            if time.time() - ts_start > MAX_COMMIT_DURATION_IN_SECONDS:
                raise Exception(f'timeout for commit duration')
            
            # try submit
            success = self._chainman.submit_change(commit, squash=True)
            if success:
                return
        
        # failed exceed max retry
        raise Exception('exceed max write conflict retries')
    

    def _collect_commit_garbage(
        self,
        garbage_retention_duration: float = MAX_COMMIT_DURATION_IN_SECONDS * 2,
    ):
        ''' Failed commits produce garbage. Need regular cleaning.
            Since can't distinguish garbage and ongoing commits easily, only
            clear commits meeting all following conditions:
            1. Not in chain
            2. seq <= topSeq
            3. Inactive for long enough (12 hours)
        '''
        self._chainman.refresh_chain(enable_init=False)
        meta = self._chainman.meta
        
        # build full commit chain
        commits_all = self._chainman._proxy.query_commits_by_seq_range(
            self._chainman._app, 1, meta.topSeq)
        
        chain = self._chainman.build_sub_commit_chain(
            commits_all, 1, meta.topSeq, meta.topCommitId)
        
        commits_in_chain = {c.id: c for c in chain}
        
        # get garbage commits to be deleted
        now = time.time()
        garbage_commits: List[CommitRecord] = []
        for commit in commits_all:
            # in chain
            if commit.id in commits_in_chain:
                continue
            # seq out of scope
            if commit.seq > meta.topSeq:
                continue
            # inactive not long enough
            if commit.ts > now - garbage_retention_duration:
                continue
            # put in garbage list
            garbage_commits.append(commit)

        # no garbage
        if not garbage_commits:
            return
        # get garbage data records
        garbage_data_items = self._chainman._proxy.query_data_items_by_commit_ids(
            self._chainman._app, [c.id for c in garbage_commits],
        )
        # delete garbage
        self._chainman._proxy.batch_delete_data_items(self._chainman._app, garbage_data_items)
        self._chainman._proxy.batch_delete_commits(garbage_commits)



class DynamicConfigConsumer:
    ''' It should be created with `CosmosDataAccessProxy` in Prod.
    '''    
    def __init__(
        self,
        proxy: DataAccessProxy,
        app: str,
    ):
        self._chainman = CommitChainManager(proxy, app)
        self._lock = RLock()
        self._next_pull_seq = 0
        

    @staticmethod
    def from_cosmos_client(client: CosmosClient, app: str) -> DynamicConfigConsumer:
        ''' Create dynamic config consumer with cosmos client.
        
            Args:
                client: cosmos client
                app: application name
                
            Returns:
                dynamic config consumer
        '''
        proxy = CosmosDataAccessProxy(client)
        return DynamicConfigConsumer(proxy, app)


    def pull(self) -> Optional[ChangeSet]:
        ''' Pull changesets incrementally.
            First time will get the full dataset.
            Returns:
                None if no newer commits; or will get the changeset.
        '''
        with self._lock:
            self._chainman.refresh_chain(enable_init=False)
            if self._next_pull_seq <= self._chainman.meta.topSeq:
                pulled_data = self._chainman.fetch_changeset_of_chain(self._next_pull_seq)
                self._next_pull_seq = self._chainman.meta.topSeq + 1
                return pulled_data
            else:
                return None
    
    
    def reset(self):
        ''' Reset the "_next_pull_seq".
            Will pull full dataset for next time.
        '''
        with self._lock:
            self._next_pull_seq = 0

