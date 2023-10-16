# Importing necessary modules
# Created by msinghal at 12/09/23
import platform  # Module for platform information
import os
import socket
import psutil  # Modules for OS, networking, and process information
from functools import lru_cache  # Importing LRU cache decorator

def get_memory() -> int:
    """
    Get the total available memory in bytes.

    Returns:
        int: Total available memory in bytes.
    """
    try:
        memory_info = psutil.virtual_memory()
        total_memory = memory_info.total
    except ImportError:
        # If psutil is not available, attempt to calculate total memory using os.sysconf
        total_memory = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    return total_memory

def get_process() -> dict:
    """
    Get information about the current process.

    Returns:
        dict: A dictionary containing information about the current process.
            - 'process_id': Process ID (PID) as an integer.
            - 'process_name': Name of the process as a string.
            - 'process_status': Status of the process as a string.
            - 'process_start_time': Process start time in seconds since the epoch as a float.
    """
    current_pid = os.getpid()
    current_process = psutil.Process(current_pid)
    return {
        "process_id": current_pid,
        "process_name": current_process.name(),
        "process_status": current_process.status(),
        "process_start_time": current_process.create_time()
    }

@lru_cache(maxsize=1)  # Using LRU cache with a maximum size of 1
def get_runtime_environment() -> dict:
    """
    Get information about the runtime environment.

    Returns:
        dict: A dictionary containing information about the runtime environment.
            - 'library_version': Version of the 'langchain' library as a string.
            - 'langchain_version': Version of 'langchain' as a string (assuming it's imported from the module).
            - 'library': Name of the library as a string.
            - 'platform': Platform information as a string.
            - 'runtime': Name of the runtime as a string ('python').
            - 'runtime_version': Version of Python as a string.
            - 'platform_architecture': Platform architecture as a string.
            - 'platform_node': Node name as a string.
            - 'platform_version': Platform version as a string.
            - 'platform_cpu': Number of CPUs as an integer.
            - 'platform_memory': Total available memory in bytes as an integer.
            - 'node_name': Hostname as a string.
            - 'node_ip': IP address of the hostname as a string.
            - 'node_fqdn': Fully qualified domain name as a string.
            - 'process_name': Name of the current process as a string.
            - 'process_id': Process ID (PID) of the current process as an integer.
            - 'process_status': Status of the current process as a string.
            - 'process_start_time': Start time of the current process in seconds since the epoch as a float.
    """
    # Lazy import to avoid circular imports
    from langchain import __version__  # Assuming the version information is imported from langchain module
    current_process_info = get_process()
    return {
        "library_version": __version__,
        "langchain_version": __version__,
        "library": "langchain",
        "platform": platform.platform(),
        "runtime": "python",
        "runtime_version": platform.python_version(),
        "platform_architecture": ''.join(platform.architecture()),
        "platform_node": platform.node(),
        "platform_version": platform.version(),
        "platform_cpu": os.cpu_count(),
        "platform_memory": get_memory(),
        "node_name": socket.gethostname(),
        "node_ip": socket.gethostbyname(socket.gethostname()),
        "node_fqdn": socket.getfqdn(),
        "process_name": current_process_info["process_name"],
        "process_id": current_process_info["process_id"],
        "process_status": current_process_info["process_status"],
        "process_start_time": current_process_info["process_start_time"],
    }

if __name__ == '__main__':
    get_runtime_environment()
