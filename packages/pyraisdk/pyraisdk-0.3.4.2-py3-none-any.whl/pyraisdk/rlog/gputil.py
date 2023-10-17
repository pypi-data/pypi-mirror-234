# refer to GPUtil
# https://github.com/anderskm/gputil/blob/master/GPUtil/GPUtil.py


from dataclasses import dataclass
import math
import os
import platform
import subprocess
from distutils import spawn
from typing import Dict, List, Optional

import psutil


@dataclass
class GPUInfo:
    index: int
    uuid: str
    utilization_gpu: float
    memory_total: float
    memory_used: float
    memory_free: float
    driver_version: str
    name: str
    gpu_serial: str
    display_active: str
    display_mode: str
    temperature_gpu: float
    

@dataclass
class GPUSummary:
    count: int
    utilization: float
    memory_utilization: float


def get_gpus() -> List[GPUInfo]:
    nvidia_smi = _get_nvidia_smi()
    fields = [
        'index',
        'uuid',
        'utilization.gpu',
        'memory.total',
        'memory.used',
        'memory.free',
        'driver_version',
        'name',
        'gpu_serial',
        'display_active',
        'display_mode',
        'temperature.gpu',
    ]
    if psutil.POSIX:
        # set high niceness for posix
        proc = subprocess.Popen(
            [nvidia_smi, f"--query-gpu={','.join(fields)}", "--format=csv,noheader,nounits"],
            preexec_fn=lambda : os.nice(19),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    else:
        proc = subprocess.Popen(
            [nvidia_smi, f"--query-gpu={','.join(fields)}", "--format=csv,noheader,nounits"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    try:
        outs, errs = proc.communicate(timeout=10)
    finally:
        if proc.poll() is None:
            proc.kill()

    if proc.poll() != 0:
        errstr = errs.decode('UTF-8')
        raise RuntimeError(f'nvidia-smi exit with code {proc.returncode}, error: {errstr}')
        
    outstr = outs.decode('UTF-8')
    lines = [line for line in outstr.split(os.linesep) if line.strip()]
    gpus = []
    for line in lines:
        values = [v.strip() for v in line.split(',')]
        if len(fields) != len(values):
            raise RuntimeError(f'nvidia-smi invalid output line: {line}')
        d = dict(zip(fields, values))
        g = GPUInfo(
            index = int(d['index']),
            uuid = d['uuid'],
            utilization_gpu = _get_float(d, 'utilization.gpu') / 100,
            memory_total = _get_float(d, 'memory.total'),
            memory_used = _get_float(d, 'memory.used'),
            memory_free = _get_float(d, 'memory.free'),
            driver_version = d['driver_version'],
            name = d['name'],
            gpu_serial = d['gpu_serial'],
            display_active = d['display_active'],
            display_mode = d['display_mode'],
            temperature_gpu = _get_float(d, 'temperature.gpu'),
        )
        gpus.append(g)
    return gpus


def get_gpu_summary() -> Optional[GPUSummary]:
    gpus = get_gpus()
    if not gpus:
        return None
    summary = GPUSummary(
        count = len(gpus),
        utilization = sum(g.utilization_gpu for g in gpus) / len(gpus),
        memory_utilization = sum(g.memory_used for g in gpus) / sum(g.memory_total for g in gpus),
    )
    return summary
    

def _get_float(d: Dict[str, str], name: str) -> float:
    s = d[name]
    try:
        v = float(s)
    except ValueError:
        raise RuntimeError(f'could not convert "{s}" (field {name}) to float')
    
    if not math.isfinite(v):
        raise RuntimeError(f'not finite float "{s}" (field {name})')
    return v


def _get_nvidia_smi() -> str:
    if platform.system() == "Windows":
        # If the platform is Windows and nvidia-smi 
        # could not be found from the environment path, 
        # try to find it from system drive with default installation path
        nvidia_smi = spawn.find_executable('nvidia-smi')
        if nvidia_smi is None:
            nvidia_smi = "%s\\Program Files\\NVIDIA Corporation\\NVSMI\\nvidia-smi.exe" % os.environ['systemdrive']
    else:
        nvidia_smi = "nvidia-smi"
    return nvidia_smi
