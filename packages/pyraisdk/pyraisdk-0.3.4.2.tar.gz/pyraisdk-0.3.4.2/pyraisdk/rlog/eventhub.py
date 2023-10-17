import queue
import sys
import threading
import time
import traceback
from typing import List, Optional, Union
from azure.eventhub import EventHubProducerClient, EventData, EventDataBatch
from azure.eventhub._constants import JWT_TOKEN_SCOPE
from azure.identity import (
    DefaultAzureCredential,
    ManagedIdentityCredential,
)
from .log import (
    ERR_PREFIX, 
    LOGGING_QUEUE_CAPACITY,
    SINK_BATCH_MAX_IDLE_SECS,
    SINK_BATCH_MAX_SIZE,
    EventSink,
    Event,
    TerminateEvent
)


AzureCredentialTyping = Union[
    DefaultAzureCredential,
    ManagedIdentityCredential,
]


class EventHubSink(EventSink):
    def __init__(
        self,
        name: str,
        hostname: Optional[str] = None,
        credential: Optional[AzureCredentialTyping] = None,
        conn_str: Optional[str] = None,
    ):
        '''
        Args:
            name: eventhub name
            hostname: Fully Qualified Namespace aka EH Endpoint URL (*.servicebus.windows.net)
            credential: token with access to eventhub
            conn_str: connection string of eventhub namespace

        Note: 
            either (hostname, credential) or conn_str you should provide
        '''
        # eventhub parameters
        if not conn_str and not (hostname and credential):
            raise Exception('neither (hostname, credential) nor conn_str is provided')
        self.name = name
        self.hostname = hostname
        self.credential = credential
        self.conn_str = conn_str
        self._verify_credential()

        # Critical: 
        #   EventHubSink is created in main process, but it's actually used in sub process. If you're reading 
        #   this piece of code, please keep in mind that all the variables set to `self` here will be copied to sub process. 
        #   Different references will exist in both processes at the same time, but they are not shared (unless it's a 
        #   multiprocess object like mp.Queue). 
        #   Again, __init__ funtion only set the initial value, and they will be copied to sub process. All the other 
        #   things are happend in sub process.
        #   Some variables have the problem that can't be serialized. So they will be assigned in `start` function, which 
        #   happenes in sub process.
        
        self.mutex = threading.RLock()
        self.terminated = threading.Event()
        self.q: queue.Queue[Event] = queue.Queue(maxsize=LOGGING_QUEUE_CAPACITY)
        ## This object (self.client) can only be created, consumed, and re-created in the same process where it will be used.
        self.client: Optional[EventHubProducerClient] = None
        self.loop_thread: Optional[threading.Thread] = None


    def __del__(self):
        self.close()


    def sink(self, evt: Event):
        try:
            self.q.put_nowait(evt)
        except queue.Full:
            msg = f'{ERR_PREFIX} EventHubSink shedding an event. Buff grew faster than stream could be written.'
            print(msg, file=sys.stderr)


    def start(self):
        with self.mutex:
            if self.loop_thread:
                return
            self.loop_thread = threading.Thread(target=self._loop_run, daemon=True)
            self.loop_thread.start()
    

    def close(self):
        with self.mutex:
            if not self.loop_thread:
                return
            if not self.terminated.is_set():
                self.terminated.set()
                try:
                    self.q.put_nowait(TerminateEvent())
                except queue.Full:
                    pass
        self.loop_thread.join()


    def _create_eventhub_client(self):
        if self.conn_str:
            return EventHubProducerClient.from_connection_string(self.conn_str, eventhub_name=self.name)
        elif self.hostname and self.credential:
            return EventHubProducerClient(self.hostname, self.name, self.credential)
        else:
            raise Exception('neither (hostname, credential) nor conn_str is provided')


    def _verify_credential(self):
        # case hostname and credential used for eventhub client
        if (not self.conn_str) and (self.hostname and self.credential):
            self.credential.get_token(JWT_TOKEN_SCOPE)


    def _require_eventhub_client(self):
        if not self.client:
            self.client = self._create_eventhub_client()


    def _reset_eventhub_client(self):
        self.client = None


    def _loop_run(self):
        while True:
            try:
                self._loop_run_inner()
            except Exception:
                traceback.print_exc()

            self._reset_eventhub_client()
            if self.terminated.is_set():
                break
            else:
                time.sleep(3)


    def _loop_run_inner(self):
        ''' condition to trigger a flush
            1. [buff size] >= SINK_BATCH_MAX_SIZE
            2. [now] - [last flush time] >= SINK_BATCH_MAX_IDLE_SECS
        '''
        buff: List[Event] = []
        last_flush_time = time.perf_counter()

        while not self.terminated.is_set():
            # get from q without block & check empty
            try:
                evt = self.q.get_nowait()
                if isinstance(evt, TerminateEvent):
                    continue
                else:
                    buff.append(evt)
            except queue.Empty:
                evt = None

            # q is empty and still have time left, get from q with timeout
            if evt is None:
                timeout = SINK_BATCH_MAX_IDLE_SECS - (time.perf_counter() - last_flush_time)
                if timeout > 0:
                    try:
                        evt = self.q.get(block=True, timeout=timeout)
                        if isinstance(evt, TerminateEvent):
                            continue
                        else:
                            buff.append(evt)
                    except queue.Empty:
                        evt = None

            # here msg is None means timeout
            # timeout or reached max size, trigger flush
            if evt is None or len(buff) >= SINK_BATCH_MAX_SIZE:
                if buff:
                    self._flush(buff)
                    buff = []
                last_flush_time = time.perf_counter()

        # terminated, flush all
        while True:
            try:
                evt = self.q.get_nowait()
                if isinstance(evt, TerminateEvent):
                    continue
                else:
                    buff.append(evt)
            except queue.Empty:
                break
        if buff:
            self._flush(buff)


    def _flush(self, evts: List[Event]):
        self._require_eventhub_client()
        batch = self.client.create_batch()  # type: ignore
        count = 0    # current batch count
        cursor = 0
        while cursor < len(evts):
            # insert batch, until full
            msg = evts[cursor].serialize_json()
            try:
                batch.add(EventData(msg))
                count += 1
                cursor += 1
                continue
            except ValueError:
                pass

            # unexpected error
            if count == 0:
                raise Exception('unexpected error in EventHubSink: batch size is 0 while exceed max bytes')
            
            # send with retries, duration 100ms
            self._send_batch_with_retry(batch, 2, 0.1)

            # send successfully
            self._require_eventhub_client()
            batch = self.client.create_batch()  # type: ignore
            count = 0
            
        if count > 0:
            self._send_batch_with_retry(batch, 2, 0.1)
        
        
    def _send_batch_with_retry(self, batch: EventDataBatch, retry: int, duration: float):
        for retry_id in range(1, retry + 1):
            try:
                self._require_eventhub_client()
                self.client.send_batch(batch)  # type: ignore
                return
            except Exception:
                self._reset_eventhub_client()
                if retry_id == retry:
                    raise
                else:
                    time.sleep(duration)
