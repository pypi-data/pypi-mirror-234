import os
import socket
import threading
from typing import Optional
import uuid

from azure.identity import ManagedIdentityCredential

from .eventhub import EventHubSink
from .log import EventLogger
from .logimp import AsyncEventLogger, StdoutSink
from .reporter import SystemMetricsReporter

__all__ = [
    "infof", 
    "infocf", 
    "warnf", 
    "warncf", 
    "errorf", 
    "errorcf", 
    "fatalf",
    "fatalcf",
    "event",
    "initialize",
]

# create logger
_logger: EventLogger = AsyncEventLogger()


# logger interface
infof = _logger.infof
infocf = _logger.infocf
warnf = _logger.warnf
warncf = _logger.warncf
errorf = _logger.errorf
errorcf = _logger.errorcf
fatalf = _logger.fatalf
fatalcf = _logger.fatalcf
event = _logger.event


# logger init
_logger_init_lock = threading.Lock()
_logger_initialized: bool = False
_sys_metrics_reporter: Optional[SystemMetricsReporter] = None


def initialize(
    eh_hostname: Optional[str] = None,
    client_id: Optional[str] = None,
    eh_conn_str: Optional[str] = None,
    eh_structured: Optional[str] = None,
    eh_unstructured: Optional[str] = None,
    role: Optional[str] = None,
    instance: Optional[str] = None,
    sys_metrics_enable: bool = True,
):
        '''
        Args:
            eh_hostname: Fully Qualified Namespace aka EH Endpoint URL (*.servicebus.windows.net). Default, read `${EVENTHUB_NAMESPACE}.servicebus.windows.net`
            client_id: client_id of service principal. Default, read $UAI_CLIENT_ID
            eh_conn_str: connection string of eventhub namespace. Default, read $EVENTHUB_CONN_STRING
            eh_structured: structured eventhub name. Default, read $EVENTHUB_AUX_STRUCTURED
            eh_unstructured: unstructured eventhub name. Default, read $EVENTHUB_AUX_UNSTRUCTURED
            role: role, Default: `RemoteModel`
            instance: instance, Default: `${MODEL_NAME}|${ENDPOINT_VERSION}|{hostname}` or `${MODEL_NAME}|${ENDPOINT_VERSION}|{_probably_unique_id()}`
            sys_metrics_enable: Whether to enable auto metrics reporting periodically for system info like gpu, memory and gpu. Default: True
        
        Note: 
            1. either (eh_hostname, eh_structured or eh_unstructured) 
               or (eh_conn_str, eh_structured or eh_unstructured) is provided, 
               event hub sink will be added
            2. If client_id is not provided in any way, will get credential without specifying client_id 
               if necessary. It's helpful for testing aml endpoint without user assigned identity.
               Only need to authorize eventhub to aml endpoint.
        '''
        global _logger_initialized
        global _sys_metrics_reporter
        with _logger_init_lock:
            # skip
            if _logger_initialized:
                return
        
            # set default value
            if eh_hostname is None:
                eh_namespace = os.getenv('EVENTHUB_NAMESPACE')
                if eh_namespace:
                    eh_hostname = f'{eh_namespace}.servicebus.windows.net'
            if client_id is None:
                client_id = os.getenv('UAI_CLIENT_ID')
            if eh_conn_str is None:
                eh_conn_str = os.getenv('EVENTHUB_CONN_STRING')
            if eh_structured is None:
                eh_structured = os.getenv('EVENTHUB_AUX_STRUCTURED')
            if eh_unstructured is None:
                eh_unstructured = os.getenv('EVENTHUB_AUX_UNSTRUCTURED')
            if role is None:
                role = 'RemoteModel'
            if instance is None:
                model_name = os.getenv('MODEL_NAME', 'unknown')
                endpoint_version = os.getenv('ENDPOINT_VERSION', 'unknown')
                # Using `socket.gethostname()` to get hostname, because `os.uname` doesn't work on windows, 
                # and will be truncated in some systems. Even official doc of `os.uname` recommends to use 
                # `socket.gethostname()`. https://docs.python.org/3.5/library/os.html#os.uname
                hostname = socket.gethostname()
                if len(hostname) <= 60:
                    instance = f'{model_name}|{endpoint_version}|{hostname}'
                else:
                    instance = f'{model_name}|{endpoint_version}|{_probably_unique_id()}'

            
            # set variables
            _logger.role = role
            _logger.instance = instance
            
            # event hub sink
            if eh_conn_str:
                if eh_structured:
                    structured_sink = EventHubSink(conn_str=eh_conn_str, name=eh_structured)
                    _logger.add_sink_structured(structured_sink)
                if eh_unstructured:
                    unstructured_sink = EventHubSink(conn_str=eh_conn_str, name=eh_unstructured)
                    _logger.add_sink_unstructured(unstructured_sink)
                
            elif eh_hostname:
                if client_id:
                    credential = ManagedIdentityCredential(client_id=client_id)
                else:
                    credential = ManagedIdentityCredential()
                if eh_structured:
                    structured_sink = EventHubSink(hostname=eh_hostname, credential=credential, name=eh_structured)
                    _logger.add_sink_structured(structured_sink)
                if eh_unstructured:
                    unstructured_sink = EventHubSink(hostname=eh_hostname, credential=credential, name=eh_unstructured)
                    _logger.add_sink_unstructured(unstructured_sink)
                
            else:
                print('WARNING: logger eventhub sink is disabled')
        
            # stdout sink
            _logger.add_sink_structured(StdoutSink())
            _logger.add_sink_unstructured(StdoutSink())

            # start
            _logger.start()

            # system auto metrics
            if sys_metrics_enable:
                _sys_metrics_reporter = SystemMetricsReporter(_logger, report_interval=60, measure_interval=30)

            # success
            _logger_initialized = True
        
                
def _probably_unique_id() -> str:
	u = str(uuid.uuid4())
	return "%s-%s%s" % (u[0:5], u[5:8], u[9:11])
