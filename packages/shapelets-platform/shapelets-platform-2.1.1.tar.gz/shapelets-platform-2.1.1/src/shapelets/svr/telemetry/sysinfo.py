
from typing import Any, Dict, List

import platform
import sys
import psutil
import cpuinfo


def capacity(n: float) -> str:
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10

    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def python_version() -> str:
    """
    Generates a normalized string to report Python's version

    Returns
    -------
    str
        Formatted versioned number, including if the environment is a 
        32 or 64 bits.
    """
    psize = {2**31 - 1: '32 bit', 2**63 - 1: '64 bit'}.get(sys.maxsize) or 'unknown bits'
    version = "{0}.{1}.{2}.{3}.{4}".format(*sys.version_info)
    return "{0} ({1})".format(version, psize)


def platform_info() -> Dict[str, Any]:
    """
    Returns a dictionary describing the properties of the platform
    where the code is running 
    """
    return {
        'os_type': platform.system(),
        'os_version': platform.release(),
        'machine': platform.machine(),
        'platform': platform.platform(),
        'memory': capacity(psutil.virtual_memory().total)
    }


def cpu_info() -> Dict[str, Any]:
    """
    Creates a dictionary describing the number and capabilities of the cores 
    running this code.
    """
    base = cpuinfo.get_cpu_info()
    remove = [
        'python_version', 'cpuinfo_version', 'cpuinfo_version_string',
        'hz_advertised_friendly', 'hz_actual_friendly',
        'hz_advertised', 'hz_actual'
    ]
    for prop in remove:
        if prop in base:
            del base[prop]

    return base


def storage_info() -> List[Dict[str, Any]]:
    """
    Returns information about the different storage types attached 
    to this machine
    """
    result = list()
    for partition in psutil.disk_partitions():
        part_info = dict()
        du = psutil.disk_usage(partition.mountpoint)
        part_info['total'] = capacity(du.total)
        part_info['free'] = capacity(du.free)
        part_info['fs_type'] = partition.fstype
        part_info['mount_point'] = partition.mountpoint
        result.append(part_info)

    return result


def system_info() -> Dict[str, Any]:
    """
    Returns a dictionary describing the python version, platform, 
    cpu and storage environment where the code is running 
    """
    return {
        'python_version': python_version(),
        'platform': platform_info(),
        'cpu': cpu_info(),
        'storage': storage_info()
    }
