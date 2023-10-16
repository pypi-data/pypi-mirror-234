# Created by msinghal at 11/09/23
from enum import Enum
from typing import List, Dict, Optional, Any

class StatusCode(str, Enum):
    """
    Enumeration for status codes.

    Attributes:
        SUCCESS (str): Represents a successful status.
        ERROR (str): Represents an error status.
    """

    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

    def __str__(self) -> str:
        return str(self.value)


class NetworkInfo:
    """
    Represents network information.

    Args:
        host_name (str, optional): The host name. Default is "fin01.example.com".
        ip_address (str, optional): The IP address. Default is "192.168.2.5".
        subnet (str, optional): The subnet. Default is "192.168.2.0/24".
    """

    def __init__(self, host_name: str = "fin01.example.com", ip_address: str = "192.168.2.5",
                 subnet: str = "192.168.2.0/24"):
        self.host_name = host_name
        self.ip_address = ip_address
        self.subnet = subnet

    def to_dict(self) -> Dict[str, any]:
        """
        Serialize the NetworkInfo object to a dictionary.

        Returns:
            Dict[str, any]: A dictionary representation of the object.
        """
        return {
            "host_name": self.host_name,
            "ip_address": self.ip_address,
            "subnet": self.subnet
        }


class NetworkInterface:
    """
    Represents a network interface.

    Args:
        name (str, optional): The name of the network interface. Default is "en0".
        mac (str, optional): The MAC address. Default is "bc:d0:74:0e:e8:2c".
    """

    def __init__(self, name: str = "en0", mac: str = "bc:d0:74:0e:e8:2c"):
        self.name = name
        self.mac = mac
        self.network = NetworkInfo()

    def to_dict(self) -> Dict[str, any]:
        """
        Serialize the NetworkInterface object to a dictionary.

        Returns:
            Dict[str, any]: A dictionary representation of the object.
        """
        return {
            'name': self.name,
            'mac': self.mac,
            'network': self.network.to_dict() if self.network else None
        }

    def get_name(self) -> str:
        """Get the name of the network interface."""
        return self.name

    def set_name(self, name: str) -> None:
        """Set the name of the network interface."""
        self.name = name

    def get_mac(self) -> str:
        """Get the MAC address of the network interface."""
        return self.mac

    def set_mac(self, mac: str) -> None:
        """Set the MAC address of the network interface."""
        self.mac = mac

    def get_network(self) -> NetworkInfo:
        """Get the network information associated with the network interface."""
        return self.network

    def set_network(self, network: NetworkInfo) -> None:
        """Set the network information associated with the network interface."""
        self.network = network

class MachineInfo:
    """
    Represents information about the machine.

    Args:
        operating_system (str, optional): The operating system. Default is "Linux".
        os_version (str, optional): The OS version. Default is "Ubuntu 20.04".
        total_memory (int, optional): Total memory in megabytes. Default is 8192.
        cpu_info (str, optional): CPU information. Default is "Intel Core i7".
        num_cores (int, optional): Number of CPU cores. Default is 4.
        architecture (str, optional): Machine architecture. Default is "x86_64".
        network_interfaces (List[NetworkInterface], optional): List of network interfaces. Default is None.
    """

    def __init__(self, operating_system: str = "Linux", os_version: str = "Ubuntu 20.04", total_memory: int = 8192,
                 cpu_info: str = "Intel Core i7", num_cores: int = 4, architecture: str = "x86_64",
                 network_interfaces: Optional[List[NetworkInterface]] = None):
        self.operating_system = operating_system
        self.os_version = os_version
        self.total_memory = total_memory
        self.cpu_info = cpu_info
        self.num_cores = num_cores
        self.architecture = architecture
        self.network_interfaces = network_interfaces if network_interfaces is not None else [NetworkInterface()]

    def to_dict(self) -> Dict[str, any]:
        """
        Serialize the MachineInfo object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the object.
        """
        return {
            "operating_system": self.operating_system,
            "os_version": self.os_version,
            "total_memory": self.total_memory,
            "cpu_info": self.cpu_info,
            "num_cores": self.num_cores,
            "architecture": self.architecture,
            "network_interfaces": [network_interface.to_dict() for network_interface in self.network_interfaces]
        }


class EnvironmentContext:
    """
    Represents context information about the environment.

    Args:
        environment_variables (Dict[str, str], optional): Dictionary of environment variables. Default is an empty dictionary.
        command_line_args (List[str], optional): List of command line arguments. Default is an empty list.
        log_files (List[str], optional): List of log files. Default is an empty list.
    """

    def __init__(self, environment_variables: Optional[Dict[str, str]] = None, command_line_args: Optional[List[str]] = None, log_files: Optional[List[str]] = None):
        self.environment_variables = environment_variables if environment_variables is not None else {}
        self.command_line_args = command_line_args if command_line_args is not None else []
        self.log_files = log_files if log_files is not None else []

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the EnvironmentContext object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the object.
        """
        return {
            "environment_variables": self.environment_variables,
            "command_line_args": self.command_line_args,
            "log_files": self.log_files
        }


class ProcessInfo:
    """
    Represents information about a process.

    Args:
        process_path (str, optional): The path to the process. Default is "python chat_bot_app.py".
        process_id (int, optional): The process ID. Default is 10000.
        status (str, optional): The status of the process. Default is "running".
        listen_ports (List[int], optional): List of listening ports. Default is an empty list.
        environment_context (EnvironmentContext, optional): The environment context associated with the process. Default is None.
    """

    def __init__(self, process_path: str = "python chat_bot_app.py", process_id: int = 10000, status: str = "running", listen_ports: Optional[List[int]] = None,
                 environment_context: Optional[EnvironmentContext] = None):
        self.process_path = process_path
        self.process_id = process_id
        self.status = status
        self.listen_ports = listen_ports if listen_ports is not None else []
        self.environment_context = environment_context if environment_context is not None else EnvironmentContext()

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the ProcessInfo object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the object.
        """
        return {
            "process_path": self.process_path,
            "process_id": self.process_id,
            "status": self.status,
            "listen_ports": self.listen_ports,
            "environment_context": self.environment_context.to_dict()
        }


class RuntimeEnvironment:
    """
    Represents information about the runtime environment.

    Args:
        lang_runtime (str, optional): The language runtime. Default is "python".
        lang_runtime_version (str, optional): The version of the language runtime. Default is "3.11.4".
        entry_point (str, optional): The entry point for the application. Default is "main.py".
        virtual_environment (str, optional): The virtual environment used. Default is "CONDA".
        environment (str, optional): The environment name. Default is "llm-security".
    """

    def __init__(self, lang_runtime: str = "python", lang_runtime_version: str = "3.11.4", entry_point: str = "main.py", virtual_environment: str = "CONDA", environment: str = "llm-security"):
        self.lang_runtime = lang_runtime
        self.lang_runtime_version = lang_runtime_version
        self.entry_point = entry_point
        self.virtual_environment = virtual_environment
        self.environment = environment

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the RuntimeEnvironment object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the object.
        """
        return {
            "lang_runtime": self.lang_runtime,
            "lang_runtime_version": self.lang_runtime_version,
            "entry_point": self.entry_point,
            "virtual_environment": self.virtual_environment,
            "environment": self.environment
        }


class SecurityContext:
    """
    Represents security context information.

    Args:
        user_id (str, optional): The user ID. Default is "root".
        group_id (str, optional): The group ID. Default is "wheel".
    """

    def __init__(self, user_id: str = "root", group_id: str = "wheel"):
        self.user_id = user_id
        self.group_id = group_id

    def to_dict(self) -> Dict[str, str]:
        """
        Serialize the SecurityContext object to a dictionary.

        Returns:
            Dict[str, str]: A dictionary representation of the object.
        """
        return {
            "user_id": self.user_id,
            "group_id": self.group_id
        }


class RequestSecurityContext:
    """
    Represents request security context information.

    Args:
        user_id (str, optional): The user ID. Default is "amit".
        group_id (str, optional): The group ID. Default is "engineering".
    """

    def __init__(self, user_id: str = "amit", group_id: str = "engineering"):
        self.user_id = user_id
        self.group_id = group_id

    def to_dict(self) -> Dict[str, str]:
        """
        Serialize the RequestSecurityContext object to a dictionary.

        Returns:
            Dict[str, str]: A dictionary representation of the object.
        """
        return {
            "user_id": self.user_id,
            "group_id": self.group_id
        }


class FileSystemInfo:
    """
    Represents file system information.

    Args:
        working_directory (str, optional): The working directory. Default is "/apps/app1".
        total_disk_space_mbs (int, optional): Total disk space in megabytes. Default is 102400.
        file_system_paths (List[str], optional): List of file system paths. Default is an empty list.
    """

    def __init__(self, working_directory: str = "/apps/app1", total_disk_space_mbs: int = 102400, file_system_paths: Optional[List[str]] = None):
        self.working_directory = working_directory
        self.total_disk_space_mbs = total_disk_space_mbs
        self.file_system_paths = file_system_paths if file_system_paths is not None else []

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the FileSystemInfo object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the object.
        """
        return {
            "working_directory": self.working_directory,
            "total_disk_space_mbs": self.total_disk_space_mbs,
            "file_system_paths": self.file_system_paths
        }


class DeploymentInfo:
    """
    Represents deployment information.

    Args:
        name (str, optional): The name of the deployment. Default is "SampleDeployment".
        version (str, optional): The version of the deployment. Default is "1.0.0".
        deployment_environment (str, optional): The deployment environment. Default is "Production".
        metadata (List[Dict[str, str]], optional): List of metadata items. Default is an empty list.
    """

    def __init__(self, name: str = "SampleDeployment", version: str = "1.0.0", deployment_environment: str = "Production", metadata: Optional[List[Dict[str, str]]] = None):
        self.name = name
        self.version = version
        self.deployment_environment = deployment_environment
        self.metadata = metadata if metadata is not None else []

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the DeploymentInfo object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the object.
        """
        return {
            "name": self.name,
            "version": self.version,
            "deployment_environment": self.deployment_environment,
            "metadata": self.metadata
        }


class FrameworkInfo:
    """
    Represents framework information.

    Args:
        used_frameworks (List[str], optional): List of used frameworks. Default is an empty list.
        dependencies (List[str], optional): List of dependencies. Default is an empty list.
    """

    def __init__(self, used_frameworks: Optional[List[str]] = None, dependencies: Optional[List[str]] = None):
        self.used_frameworks = used_frameworks if used_frameworks is not None else []
        self.dependencies = dependencies if dependencies is not None else []

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the FrameworkInfo object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the object.
        """
        return {
            "used_frameworks": self.used_frameworks,
            "dependencies": self.dependencies
        }


from typing import List, Dict, Optional, Any


class AppFrameworkMetadata:
    def __init__(self, key: str = "frameworkKey1", value: str = "frameworkValue1", tags: Optional[List[str]] = None):
        """
        Initialize AppFrameworkMetadata.

        Args:
            key (str, optional): The key for the metadata. Default is "frameworkKey1".
            value (str, optional): The value for the metadata. Default is "frameworkValue1".
            tags (List[str], optional): A list of tags for the metadata. Default is an empty list.
        """
        self.key = key
        self.value = value
        self.tags = tags if tags is not None else []

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the AppFrameworkMetadata object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the object.
        """
        return {
            "key": self.key,
            "value": self.value,
            "tags": self.tags
        }


class ApplicationFramework:
    def __init__(self, app_framework: str = "LANG_CHAIN", version: str = "1.0", app_framework_metadata: Optional[List[AppFrameworkMetadata]] = None):
        """
        Initialize ApplicationFramework.

        Args:
            app_framework (str, optional): The application framework name. Default is "LANG_CHAIN".
            version (str, optional): The version of the application framework. Default is "1.0".
            app_framework_metadata (List[AppFrameworkMetadata], optional): A list of AppFrameworkMetadata objects. Default is an empty list.
        """
        self.app_framework = app_framework
        self.version = version
        self.app_framework_metadata = app_framework_metadata if app_framework_metadata is not None else []

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the ApplicationFramework object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the object.
        """
        return {
            "app_framework": self.app_framework,
            "version": self.version,
            "app_framework_metadata": [metadata.to_dict() for metadata in self.app_framework_metadata]
        }


class Metadata:
    def __init__(self, key: str = "k1", value: str = "value1", tags: Optional[List[str]] = None):
        """
        Initialize Metadata.

        Args:
            key (str, optional): The key for the metadata. Default is "k1".
            value (str, optional): The value for the metadata. Default is "value1".
            tags (List[str], optional): A list of tags for the metadata. Default is an empty list.
        """
        self.key = key
        self.value = value
        self.tags = tags if tags is not None else []

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the Metadata object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the object.
        """
        return {
            "key": self.key,
            "value": self.value,
            "tags": self.tags
        }


class ApplicationMetadata:
    def __init__(self, name: str = "app1", version: str = "1.0", description: str = "", owner: str = "madan", metadata: Optional[List[Metadata]] = None):
        """
        Initialize ApplicationMetadata.

        Args:
            name (str, optional): The name of the application. Default is "app1".
            version (str, optional): The version of the application. Default is "1.0".
            description (str, optional): A description of the application. Default is an empty string.
            owner (str, optional): The owner of the application. Default is "madan".
            metadata (List[Metadata], optional): A list of Metadata objects. Default is an empty list.
        """
        self.name = name
        self.version = version
        self.description = description
        self.owner = owner
        self.metadata = metadata if metadata is not None else []

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the ApplicationMetadata object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the object.
        """
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "owner": self.owner,
            "metadata": [metadata.to_dict() for metadata in self.metadata]
        }




class Environment:
    def __init__(self, machine: Optional[MachineInfo] = None, networks: Optional[List[NetworkInfo]] = None,
                 process: Optional[ProcessInfo] = None, runtime_environment: Optional[RuntimeEnvironment] = None,
                 security_context: Optional[SecurityContext] = None, request_security_context: Optional[RequestSecurityContext] = None,
                 file_system: Optional[FileSystemInfo] = None, deployment: Optional[DeploymentInfo] = None,
                 framework: Optional[FrameworkInfo] = None, application_framework: Optional[ApplicationFramework] = None,
                 application_metadata: Optional[ApplicationMetadata] = None):
        """
        Initialize Environment.

        Args:
            machine (MachineInfo, optional): Information about the machine. Default is None.
            networks (List[NetworkInfo], optional): List of network information. Default is a list containing one NetworkInfo object.
            process (ProcessInfo, optional): Information about the process. Default is None.
            runtime_environment (RuntimeEnvironment, optional): Information about the runtime environment. Default is None.
            security_context (SecurityContext, optional): Security context information. Default is None.
            request_security_context (RequestSecurityContext, optional): Request security context information. Default is None.
            file_system (FileSystemInfo, optional): File system information. Default is None.
            deployment (DeploymentInfo, optional): Deployment information. Default is None.
            framework (FrameworkInfo, optional): Framework information. Default is None.
            application_framework (ApplicationFramework, optional): Application framework information. Default is None.
            application_metadata (ApplicationMetadata, optional): Application metadata. Default is None.
        """
        self.machine = machine if machine else MachineInfo()
        self.networks = networks if networks else [NetworkInfo()]
        self.process = process if process else ProcessInfo()
        self.runtime_environment = runtime_environment if runtime_environment else RuntimeEnvironment()
        self.security_context = security_context if security_context else SecurityContext()
        self.request_security_context = request_security_context if request_security_context else RequestSecurityContext()
        self.file_system = file_system if file_system else FileSystemInfo()
        self.deployment = deployment if deployment else DeploymentInfo()
        self.framework = framework if framework else FrameworkInfo()
        self.application_framework = application_framework if application_framework else ApplicationFramework()
        self.application_metadata = application_metadata if application_metadata else ApplicationMetadata()

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the Environment object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the object.
        """
        return {
            "machine": self.machine.to_dict() if self.machine is not None else None,
            "networks": [network.to_dict() for network in self.networks],
            "process": self.process.to_dict() if self.process is not None else None,
            "runtime_environment": self.runtime_environment.to_dict() if self.runtime_environment is not None else None,
            "security_context": self.security_context.to_dict() if self.security_context is not None else None,
            "request_security_context": self.request_security_context.to_dict() if self.request_security_context else None,
            "file_system": self.file_system.to_dict() if self.file_system is not None else None,
            "deployment": self.deployment.to_dict() if self.deployment is not None else None,
            "framework": self.framework.to_dict() if self.framework is not None else None,
            "application_framework": self.application_framework.to_dict() if self.application_framework is not None else None,
            "application_metadata": self.application_metadata.to_dict() if self.application_metadata is not None else None
        }

    def add_attribute(self, key: str, value: Any) -> None:
        """
        Add an attribute to the environment.

        Args:
            key (str): The key of the attribute.
            value (Any): The value of the attribute.

        Returns:
            None
        """
        if self.attributes is None:
            self.attributes = {}
        self.attributes[key] = value
