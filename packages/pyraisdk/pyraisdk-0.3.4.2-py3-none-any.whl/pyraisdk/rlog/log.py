
import sys

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from datetime import datetime
from enum import Enum
import threading
import traceback
from typing import Any, List, Optional


ERR_PREFIX = "CRITICAL: UNEXPECTED LOGGING ISSUE! (This logline appears only in stderr). Detail: "
LOGGING_QUEUE_CAPACITY = 10000
SINK_BATCH_MAX_SIZE = 1000
SINK_BATCH_MAX_IDLE_SECS = 5


class LogLevel(str, Enum):
    INFO = 'INFO'
    WARN = 'WARN'
    ERROR = 'ERROR'
    FATAL = 'FATAL'


class Event(ABC):
    @abstractmethod
    def friendly_string(self) -> str:
        pass
    
    @abstractmethod
    def serialize_json(self) -> str:
        pass


class TerminateEvent(Event):
    def friendly_string(self) -> str:
        return ''
    
    def serialize_json(self) -> str:
        return ''


class EventSink(ABC):
    @abstractmethod
    def sink(self, evt: Event):
        pass

    def start(self):
        pass
    
    def close(self):
        pass


class EventLogger(ABC):
    def __init__(self):
        self.mutex = threading.RLock()
        self.unstruct_sinks: List[EventSink] = []
        self.struct_sinks: List[EventSink] = []

    def start(self):
        pass

    # Structured events
    @abstractmethod
    def event(self, key: str, code: str, numeric: float, detail: str='', corr_id: str='', elem: int=-1):
        pass

    # Unstructured events
    @abstractmethod
    def log(self, level: LogLevel, msg: str, corr_id: str='', elem: int=-1):
        pass

    def infof(self, format: str, *args: Any):
        msg = format % tuple(args) if args else format
        self.log(LogLevel.INFO, msg)

    def infocf(self, corr_id: str, elem: int, format: str, *args: Any):
        msg = format % tuple(args) if args else format
        self.log(LogLevel.INFO, msg, corr_id=corr_id, elem=elem)

    def warnf(self, format: str, *args: Any):
        msg = format % tuple(args) if args else format
        self.log(LogLevel.WARN, msg)

    def warncf(self, corr_id: str, elem: int, format: str, *args: Any):
        msg = format % tuple(args) if args else format
        self.log(LogLevel.WARN, msg, corr_id=corr_id, elem=elem)

    def errorf(self, format: str, *args: Any):
        msg = format % tuple(args) if args else format
        self.log(LogLevel.ERROR, msg)

    def errorcf(self, corr_id: str, elem: int, ex: Optional[Exception], format: str, *args: Any):
        msg = format % tuple(args) if args else format
        if ex:
            msg += '\n' + get_format_ex(ex, limit=4)
        self.log(LogLevel.ERROR, msg, corr_id=corr_id, elem=elem)

    def fatalf(self, format: str, *args: Any):
        msg = format % tuple(args) if args else format
        self.log(LogLevel.FATAL, msg)

    def fatalcf(self, corr_id: str, elem: int, ex: Optional[Exception], format: str, *args: Any):
        msg = format % tuple(args) if args else format
        if ex:
            msg += '\n' + get_format_ex(ex, limit=4)
        self.log(LogLevel.FATAL, msg, corr_id=corr_id, elem=elem)

    # sink register
    def add_sink_unstructured(self, sink: EventSink):
        with self.mutex:
            self.unstruct_sinks.append(sink)        
    
    def add_sink_structured(self, sink: EventSink):
        with self.mutex:
            self.struct_sinks.append(sink)


@dataclass_json
@dataclass
class UnstructuredEvent(Event):
    level: LogLevel     = field(metadata=config(field_name='Level'))
    role: str           = field(metadata=config(field_name='Role'))
    instance: str       = field(metadata=config(field_name='Instance'))
    context: str        = field(metadata=config(field_name='Context'))
    message: str        = field(metadata=config(field_name='Message'))
    correlation_id: str = field(metadata=config(field_name='CorrelationId'))
    element: int        = field(metadata=config(field_name='Element'))
    timestamp: datetime = field(
            default_factory=datetime.utcnow,
            metadata=config(field_name='Timestamp', encoder=lambda x: datetime.isoformat(x, sep=' '))
        )
    
    def friendly_string(self) -> str:
        corr_suffix = ''
        if self.correlation_id:
            corr_suffix = "  {CorrId: %s, Elem: %d}" % (self.correlation_id, self.element)
            
        return "%s  %s(%s)  %s  %s]  %s%s\n" % (
            self.timestamp.isoformat(sep=' '), 
            self.role, self.instance,
            self.level,
            self.context, self.message,
            corr_suffix
        )
            
    def serialize_json(self) -> str:
        return self.to_json()  # type: ignore


@dataclass_json
@dataclass
class StructuredEvent(Event):
    key: str            = field(metadata=config(field_name='Key'))
    role: str           = field(metadata=config(field_name='Role'))
    instance: str       = field(metadata=config(field_name='Instance'))
    correlation_id: str = field(metadata=config(field_name='CorrelationId'))
    element: int        = field(metadata=config(field_name='Element'))
    code: str           = field(metadata=config(field_name='Code'))
    numeric: float      = field(metadata=config(field_name='Numeric'))
    detail: str         = field(metadata=config(field_name='Detail'))
    timestamp: datetime = field(
            default_factory=datetime.utcnow,
            metadata=config(field_name='Timestamp', encoder=lambda x: datetime.isoformat(x, sep=' '))
        )

    def friendly_string(self) -> str:
        corr_suffix = ''
        if self.correlation_id:
            corr_suffix = "  {CorrId: %s, Elem: %d}" % (self.correlation_id, self.element)
            
        return "%s  %s(%s)  %s:  { %s %f %s }%s\n" % (
            self.timestamp.isoformat(sep=' '), 
            self.role, self.instance,
            self.key, self.code, self.numeric, self.detail,
            corr_suffix
        )
        
    def serialize_json(self) -> str:
        return self.to_json()  # type: ignore
    
    
def get_format_ex(ex: BaseException, limit: Optional[int] = None) -> str:
    ''' limit: limit of stack frames number
    '''
    _limit = -limit if limit is not None and limit > 0 else None
    tbstr = ''.join(traceback.format_tb(ex.__traceback__, limit = _limit))
    stack = f'{type(ex).__name__}: {ex}\nTraceback\n{tbstr}'
    return stack.strip()


def _get_curr_format_ex() -> Optional[str]:
    _, ex, _ = sys.exc_info()
    if ex:
        return get_format_ex(ex)
    else:
        return None
    