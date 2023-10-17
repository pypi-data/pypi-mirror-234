
from __future__ import annotations
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
import heapq
import json
import logging
from threading import Condition, RLock, Thread
import time
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from azure.core.credentials import TokenCredential
from azure.cosmos import CosmosClient
from pyraisdk import rlog
from .core import CommitChainManager
from .proxy import CosmosDataAccessProxy, DataAccessProxy


class ConfigMonitor(ABC):
    ''' Base class for Dynamic Config Monitors to inherit from.
    '''
    def __init__(
        self,
        url: str,
        credential: Union[str, Dict[str, str], TokenCredential],
        app: str,
        poll_interval: float = 10,
    ):
        ''' Constructor. Won't really run until 'start' called.
            Args:
                url: The URL of the Cosmos DB account.
                credential: Can be the account key, or a dictionary of resource tokens.
                app: Application name of dynamic config.
                poll_interval: Poll interval in seconds. Default 10.
        '''
        self.__url = url
        self.__credential = credential
        self.__app = app
        self.__poll_interval = poll_interval
        # init load status
        self.__init_load_done: bool = False
        self.__init_load_cond = Condition()
        self.__init_load_excepted: Optional[Exception] = None
    

    def _set_init_load_status(self, excepted: Optional[Exception]):
        ''' Should only be called in `_MonitorManager`.
            Strictly speaking it is not a private function. Naming as private method is
            to remind monitor users not to call it directly.
        '''
        with self.__init_load_cond:
            if self.__init_load_done:
                return
            if excepted is None:
                self.__init_load_done = True
                self.__init_load_excepted = None
            else:
                self.__init_load_excepted = excepted
            self.__init_load_cond.notify_all()


    def wait_init_load(self, timeout: Optional[float] = None):
        ''' Wait for initial loading '''
        with self.__init_load_cond:
            if self.__init_load_done:
                return
            elif self.__init_load_excepted is not None:
                raise self.__init_load_excepted
        
            notified = self.__init_load_cond.wait(timeout)
            if notified:
                if self.__init_load_done:
                    return
                elif self.__init_load_excepted is not None:
                    raise self.__init_load_excepted
                else:
                    raise Exception('unexpected error')
            else:
                raise TimeoutError('initial loading timeout')


    def start(self, blocking: bool = False, timeout: Optional[float] = None):
        ''' Start config monitor
            Args:
                blocking: If True, block until initial loading complete for fail;
                    If False, return immediately.
                timeout: When blocking is True and it blocks exceed 'timeout', will
                    raise the TimeoutError exception. None for no timeout limitation.
        '''
        _manager.start_config_monitor(
            self, self.__url, self.__credential, self.__app, self.__poll_interval
        )
        if blocking:
            self.wait_init_load(timeout)
        

    def stop(self):
        ''' Stop config monitor '''
        _manager.stop_config_monitor(self)
        with self.__init_load_cond:
            self.__init_load_done = False
            self.__init_load_excepted = None


    @abstractmethod
    def apply(self, updates: Dict[str, Any], deletions: Set[str]):
        ''' Monitor apply function.
        
            Abstract method which need to be implemented in subclass. It receives
            a changeset (include updates and deletions) of one/multiple commits.

	        If `apply` fails, for any reason, it won't retry automatically. But the pointer
	        of "last successfully applied" will remain unchanged. When any new data is pushed,
	        it will start consuming data again from the pointer of "last successfully applied".
	        In other words, the data that failed last time will be consumed and applied again
	        when new data coming.
            
            Args:
                updates: key-value to be updated
                deletions: keys to be deleted
        '''
        pass



@dataclass
class _MonitorHandler:
    app: str
    monitor: ConfigMonitor
    poll_interval: float
    chainman: CommitChainManager
    next_pull_seq: int = 0
    next_apply_seq: int = 0
    next_ts: float = 0
    lock: RLock = field(default_factory=RLock)


class _MonitorManager:
    def __init__(self):
        self._handlers: Dict[int, _MonitorHandler] = {}
        self._handler_heap: List[Tuple[float, _MonitorHandler]] = []
        self._clients: Dict[str, CosmosClient] = {}
        self._cond = Condition()
        self._pool = ThreadPoolExecutor()
        self._worker: Optional[Thread] = None
        
    
    def start_config_monitor(
        self,
        monitor: ConfigMonitor,
        url: str,
        credential: Union[str, Dict[str, str], TokenCredential],
        app: str,
        poll_interval: float,
    ):
        # get cosmos client
        with self._cond:
            if url in self._clients:
                client = self._clients[url]
            else:
                client = CosmosClient(url, credential)
                self._clients[url] = client
        
        # start
        # TODO: Reuse proxy
        proxy = CosmosDataAccessProxy(client)
        self._start_config_monitor_with_access_proxy(monitor, proxy, app, poll_interval)


    def _start_config_monitor_with_access_proxy(
        self,
        monitor: ConfigMonitor,
        proxy: DataAccessProxy,
        app: str,
        poll_interval: float,
    ):
        chainman = CommitChainManager(proxy, app)
        handler = _MonitorHandler(app, monitor, poll_interval, chainman)
        monitor_id = id(monitor)
        with self._cond:
            # set handler
            if monitor_id in self._handlers:
                raise Exception(f'ConfigMonitor {monitor_id} already started')
            else:
                heapq.heappush(self._handler_heap, (handler.next_ts, handler))
                self._handlers[monitor_id] = handler

            # init or resume worker
            if self._worker is None:
                self._worker = Thread(target=self._worker_run, daemon=True)
                self._worker.start()
            else:
                self._cond.notify_all()


    def stop_config_monitor(self, monitor: ConfigMonitor):
        with self._cond:
            monitor_id = id(monitor)
            if monitor_id in self._handlers:
                self._handlers.pop(monitor_id)


    def _worker_run(self):
        while True:
            try:
                self._worker_run_inner()
            except Exception as ex:
                if rlog._logger_initialized:
                    rlog.errorcf('', -1, ex, f'{EVENT_KEY_PREFIX}: unexpected error in manager worker')
                else:
                    logging.exception(f'{EVENT_KEY_PREFIX}: unexpected error in manager worker')
                time.sleep(3)


    def _worker_run_inner(self):
        with self._cond:
            while True:
                if len(self._handler_heap) == 0:
                    self._cond.wait()
                else:
                    # pop handler that is ready to execute next
                    _, handler = heapq.heappop(self._handler_heap)
                    notified = self._cond.wait(handler.next_ts - time.time())
                    
                    # new handler added
                    if notified:
                        heapq.heappush(self._handler_heap, (handler.next_ts, handler))
                        continue
                    
                    # current handler deleted
                    if id(handler.monitor) not in self._handlers:
                        continue
                    
                    # next ts
                    handler.next_ts = time.time() + handler.poll_interval
                    heapq.heappush(self._handler_heap, (handler.next_ts, handler))
                    
                    # pull & apply
                    self._pool.submit(self._pull_and_apply, handler)


    def _pull_and_apply(self, handler: _MonitorHandler):
        # If handler is already executing, skip current iteration.
        acquired = handler.lock.acquire(blocking=False)
        if not acquired:
            return
        try:
            # pull
            pull_start_ts = time.perf_counter()
            try:
                # refresh chain
                handler.chainman.refresh_chain(enable_init=False)
                # no newer commits, skip
                if handler.next_pull_seq > handler.chainman.meta.topSeq:
                    rlog.event(
                        EventKey_MonitorPull, "EMPTY",
                        time.perf_counter() - pull_start_ts,
                        json.dumps({'App': handler.app, 'Count': 0}),
                    )
                    return
                # pull, from next_apply_seq
                pulled_data = handler.chainman.fetch_changeset_of_chain(handler.next_apply_seq)
                handler.next_pull_seq = handler.chainman.meta.topSeq + 1
                # pull success
                rlog.event(
                    EventKey_MonitorPull, "OK",
                    time.perf_counter() - pull_start_ts,
                    json.dumps({'App': handler.app, 'Count': pulled_data.count}),
                )
            except Exception as ex:
                rlog.event(
                    EventKey_MonitorPull, "FAIL",
                    time.perf_counter() - pull_start_ts,
                    json.dumps({'App': handler.app, 'Count': 0}),
                )
                raise

            # apply
            apply_start_ts = time.perf_counter()
            try:
                handler.monitor.apply(pulled_data.updates, pulled_data.deletions)
                handler.next_apply_seq = handler.chainman.meta.topSeq + 1
                rlog.event(
                    EventKey_MonitorApply, "OK",
                    time.perf_counter() - apply_start_ts,
                    json.dumps({'App': handler.app}),
                )
            except Exception as ex:
                rlog.event(
                    EventKey_MonitorApply, "FAIL",
                    time.perf_counter() - apply_start_ts,
                    json.dumps({'App': handler.app}),
                )
                raise

            # init load success
            handler.monitor._set_init_load_status(None)
            
        except Exception as ex:
            # init load status
            handler.monitor._set_init_load_status(ex)
            # logging
            if rlog._logger_initialized:
                rlog.errorcf('', -1, ex, f'{EVENT_KEY_PREFIX}: monitor process error, app: {handler.app}')
            else:
                logging.error(f'{EVENT_KEY_PREFIX}: monitor process error, app: {handler.app}', exc_info=ex)
            
        finally:
            handler.lock.release()


# logging key prefix for monitor
EVENT_KEY_PREFIX = 'pyraidynconf'

# Structured Event indicating one "Pull" operation in Monitor.
# code: OK, FAIL, EMPTY
# numeric: the latency of pull
# detail: `{ "App": "%s", "Count": %d }`
EventKey_MonitorPull = f'{EVENT_KEY_PREFIX}_MonitorPull'

# Structured Event indicating one "Apply" operation in Monitor.
# code: OK, FAIL
# numeric: the latency of apply
# detail: `{ "App": "%s" }`
EventKey_MonitorApply = f'{EVENT_KEY_PREFIX}_MonitorApply'

# singleton
_manager = _MonitorManager()

