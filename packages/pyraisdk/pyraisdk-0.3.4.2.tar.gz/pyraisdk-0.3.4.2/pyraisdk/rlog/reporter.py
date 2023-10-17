from typing import List, Optional
import psutil
import time

from threading import Thread

from .log import EventLogger
from .gputil import get_gpu_summary


EVENT_KEY_PREFIX = 'pyraisys'


class Avarager:
    def __init__(self):
        self.count: int = 0
        self.sum: float = 0.0

    def push(self, val: float):
        self.sum += val
        self.count += 1
        
    def pop(self) -> Optional[float]:
        if self.count == 0:
            return None
        r = self.sum / self.count
        self.count = 0
        self.sum = 0.0
        return r


class SystemMetricsReporter:

    def __init__(self, logger: EventLogger, report_interval: float, measure_interval: float, initial_wait: float = 3):
        assert report_interval >= 1
        assert measure_interval >= 1
        assert initial_wait >= 0
        assert report_interval >= measure_interval

        self.logger = logger
        self.report_interval = report_interval
        self.measure_interval = measure_interval
        self.initial_wait = initial_wait

        self.gputil_success = True
        self.next_measure_ts = time.perf_counter()
        self.next_report_ts = time.perf_counter()
        self.cpu_util_avg = Avarager()
        self.mem_util_avg = Avarager()
        self.gpu_util_avg = Avarager()
        self.gpu_mem_util_avg = Avarager()
        
        self.alive = True
        self.worker = Thread(target=self._worker_run, daemon=True)
        self.worker.start()


    def close(self):
        self.alive = False


    def __del__(self):
        self.close()


    def _worker_run(self):
        # wait a number of seconds before first reporting, psutil.cpu_percent() will 
        # return a meaningless value if execute immediately after its importing 
        time.sleep(self.initial_wait)

        while self.alive:
            try:
                if self.next_measure_ts <= self.next_report_ts:
                    # try measure process
                    now = time.perf_counter()
                    if now >= self.next_measure_ts:
                        self.next_measure_ts = max(now, self.next_measure_ts + self.measure_interval)
                        self._measure_process()
                else:
                    # try report process
                    now = time.perf_counter()
                    if now >= self.next_report_ts:
                        self.next_report_ts = max(now, self.next_report_ts + self.report_interval)
                        self._report_process()

                sleep_time = min(self.next_report_ts, self.next_measure_ts) - time.perf_counter()
                if sleep_time > 0:
                    time.sleep(sleep_time)

            except Exception as ex:
                # unexpected error
                self.logger.errorcf('', -1, ex, f'{EVENT_KEY_PREFIX}: unexpected error in _worker_run')
                time.sleep(3)


    def _measure_process(self):
        # cpu
        cpu_percent = psutil.cpu_percent()
        self.cpu_util_avg.push(cpu_percent)

        # memory
        memory_percent = psutil.virtual_memory().percent
        self.mem_util_avg.push(memory_percent)

        # gpu
        # Only for the first time (partial first time) unable to get gpu info, log
        # will be pushed. To avoid frequently being disturbed by cpu error/warn logs.
        gpu_ex = None
        gpu_summary = None
        try:
            gpu_summary = get_gpu_summary()
        except Exception as ex:
            gpu_ex = ex

        if gpu_ex:
            # gpu error, only push log when succeeded last time
            if self.gputil_success:
                self.gputil_success = False
                self.logger.errorcf('', -1, gpu_ex, f'{EVENT_KEY_PREFIX}: failed to get gpu info')

        elif gpu_summary is None:
            # no gpu, only push log when succeeded last time
            if self.gputil_success:
                self.gputil_success = False
                self.logger.warnf(f'{EVENT_KEY_PREFIX}: no gpu available')

        else:
            # success
            self.gputil_success = True
            self.gpu_util_avg.push(gpu_summary.utilization)
            self.gpu_mem_util_avg.push(gpu_summary.memory_utilization)


    def _report_process(self):
        # cpu
        cpu_util_val = self.cpu_util_avg.pop()
        if cpu_util_val is not None:
            self.logger.event(f'{EVENT_KEY_PREFIX}_CpuUtilization', '', cpu_util_val)
        
        # memory
        mem_util_val = self.mem_util_avg.pop()
        if mem_util_val is not None:
            self.logger.event(f'{EVENT_KEY_PREFIX}_MemoryUtilization', '', mem_util_val)
        
        # gpu
        gpu_util_val = self.gpu_util_avg.pop()
        if gpu_util_val is not None:
            self.logger.event(f'{EVENT_KEY_PREFIX}_GpuUtilization', '', gpu_util_val)
            
        # gpu mem
        gpu_mem_util_val = self.gpu_mem_util_avg.pop()
        if gpu_mem_util_val is not None:
            self.logger.event(f'{EVENT_KEY_PREFIX}_GpuMemoryUtilization', '', gpu_mem_util_val)
