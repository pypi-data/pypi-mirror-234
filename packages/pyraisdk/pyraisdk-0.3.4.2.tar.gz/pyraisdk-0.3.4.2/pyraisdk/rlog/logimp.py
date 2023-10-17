
import multiprocessing as mp
import os
import queue
import sys
import signal
import threading
import time
import traceback

from typing import List, Optional

import psutil

from .log import (
    LOGGING_QUEUE_CAPACITY,
    SINK_BATCH_MAX_IDLE_SECS,
    Event,
    EventLogger,
    EventSink,
    LogLevel,
    UnstructuredEvent,
    StructuredEvent,
    TerminateEvent,
    ERR_PREFIX,
)


class AsyncEventLogger(EventLogger):
    def __init__(self, role: str = '', instance: str=''):
        super(AsyncEventLogger, self).__init__()
        self.role = role 
        self.instance = instance
        self.unstruct_queue: mp.Queue[Event] = mp.Queue(maxsize=LOGGING_QUEUE_CAPACITY)
        self.struct_queue: mp.Queue[Event] = mp.Queue(maxsize=LOGGING_QUEUE_CAPACITY)
        self.backend_loop: Optional[_AsyncEventLoggerBackendLoop] = None
    
    def log(self, level: LogLevel, msg: str, corr_id: str='', elem: int=-1):
        # check logger started
        if self.backend_loop is None:
            return
        evt = UnstructuredEvent(
                level = level,
                role = self.role,
                instance = self.instance,
                context = '',
                message = msg,
                correlation_id = corr_id,
                element = elem,
            )
        try:
            self.unstruct_queue.put_nowait(evt)
        except queue.Full:
            msg = f'{ERR_PREFIX} AsyncEventLogger shedding an event. Unstruct buffer grew faster than stream could be written.'
            print(msg, file=sys.stderr)

    def event(self, key: str, code: str, numeric: float, detail: str='', corr_id: str='', elem: int=-1):
        # check logger started
        if self.backend_loop is None:
            return
        evt = StructuredEvent(
            key = key,
            role = self.role,
            instance = self.instance,
            correlation_id = corr_id,
            element = elem,
            code = code,
            numeric = numeric,
            detail = detail,
        )
        try:
            self.struct_queue.put_nowait(evt)
        except queue.Full:
            msg = f'{ERR_PREFIX} AsyncEventLogger shedding an event. Struct buffer grew faster than stream could be written.'
            print(msg, file=sys.stderr)

    def start(self):
        with self.mutex:
            if self.backend_loop:
                return
            self.backend_loop = _AsyncEventLoggerBackendLoop(
                self.unstruct_queue,
                self.unstruct_sinks,
                self.struct_queue,
                self.struct_sinks
            )
            self.backend_loop.start()
    
    def close(self):
        with self.mutex:
            if self.backend_loop is not None:
                self.backend_loop.close()

    def __del__(self):
        self.close()


class _AsyncEventLoggerBackendLoop:
    def __init__(
        self,
        unstruct_queue: mp.Queue,
        unstruct_sinks: List[EventSink],
        struct_queue: mp.Queue,
        struct_sinks: List[EventSink],
    ):
        self.categories_q: List[mp.Queue[Event]] = [unstruct_queue, struct_queue]
        self.categories_sinks: List[List[EventSink]] = [unstruct_sinks, struct_sinks]
        self.categories_sinks_ready: Optional[List[List[EventSink]]] = None
        self.terminated = mp.Event()
        self.mutex = mp.RLock()
        self.process: Optional[mp.Process] = None
        self.loop_threads: List[threading.Thread] = []
        
    def start(self):
        with self.mutex:
            if self.process:
                return
            self.process = mp.Process(target=self.main, daemon=True)
            self.process.start()
        
    def main(self):
        ''' entrance of backend process
        '''
        # set high niceness for posix
        if psutil.POSIX:
            os.nice(19)
        
        with self.mutex:
            # set quit signal
            signal.signal(signal.SIGINT, self.handle_signal)
            signal.signal(signal.SIGTERM, self.handle_signal)
            # start sinks
            self.categories_sinks_ready = [
                self._get_ready_sinks(sinks) for sinks in self.categories_sinks
            ]
            # start threads
            for q, sinks in zip(self.categories_q, self.categories_sinks_ready):
                t = threading.Thread(target=self.run_q, args=(q, sinks), daemon=True)
                t.start()
                self.loop_threads.append(t)

        for t in self.loop_threads:
            t.join()
        
        # close sinks at the end (not exit by handle_signal)
        for sinks in self.categories_sinks_ready:
            for sink in sinks:
                sink.close()

    def _get_ready_sinks(self, sinks: List[EventSink]) -> List[EventSink]:
        result = []
        for sink in sinks:
            try:
                sink.start()
                result.append(sink)
            except Exception:
                msg = ERR_PREFIX + ' AsyncEventLogger failed to start a sink. Removed it from sink list of logger\n' + traceback.format_exc()
                print(msg, file=sys.stderr)
        return result

    def run_q(self, q: mp.Queue, sinks: List[EventSink]):
        ''' If run_q_inner failed somehow, sleep 3 seconds and retry
            until process terminated
        '''
        while True:
            try:
                self.run_q_inner(q, sinks)
            except Exception:
                traceback.print_exc()

            if self.terminated.is_set():
                break
            else:
                time.sleep(3)

    def run_q_inner(self, q: mp.Queue, sinks: List[EventSink]):
        ''' Fetch events from q, and put them into sinks
        '''
        while not self.terminated.is_set():
            try:
                evt = q.get(block=True, timeout=SINK_BATCH_MAX_IDLE_SECS)
                if isinstance(evt, TerminateEvent):
                    continue
            except queue.Empty:
                continue
            for sink in sinks:
                try:
                    sink.sink(evt)
                except Exception:
                    msg = ERR_PREFIX + f' AsyncEventLogger failed to call sink of {type(sink)}.\n' + traceback.format_exc()
                    print(msg, file=sys.stderr)

        # terminated, flush all
        while True:
            try:
                # Set a small timeout here, to ensure `q` is really consumed up on exiting.
                # To avoid the deadlock issue occuring with a low probability.
                evt = q.get(block=True, timeout=0.1)
                if isinstance(evt, TerminateEvent):
                    continue
                for sink in sinks:
                    try:
                        sink.sink(evt)
                    except Exception:
                        msg = ERR_PREFIX + f' AsyncEventLogger failed to call sink of {type(sink)}.\n' + traceback.format_exc()
                        print(msg, file=sys.stderr)

            except queue.Empty:
                break

    def handle_signal(self, signum, frame):
        with self.mutex:
            self.terminated.set()
            for q in self.categories_q:
                try:
                    q.put_nowait(TerminateEvent())
                except queue.Full:
                    pass
            for t in self.loop_threads:
                t.join()
            if self.categories_sinks_ready:
                for sinks in self.categories_sinks_ready:
                    for sink in sinks:
                        sink.close()

    def close(self):
        with self.mutex:
            if self.terminated.is_set():
                return
            self.terminated.set()
            for q in self.categories_q:
                try:
                    q.put_nowait(TerminateEvent())
                except queue.Full:
                    pass


    def __del__(self):
        self.close()


class StdoutSink(EventSink):
    def sink(self, evt: Event):
        msg = evt.friendly_string()
        sys.stdout.write(msg)

