# Created by msinghal at 12/09/23
from singulr_client.data_contracts.env.environment import MachineInfo
from singulr_client.data_contracts.env.environment  import ProcessInfo, NetworkInfo
from singulr_client.data_contracts.env.environment  import RuntimeEnvironment, Environment, RequestSecurityContext, SecurityContext
from langchain.callbacks.tracers.schemas import Run


class EnvironmentGenerator(object):

    def _extract_machine_info(self, run: Run):
        machine_info = {}
        machine_info["operating_system"] = run.extra["runtime"]["platform"]
        machine_info["os_version"] = run.extra["runtime"]["platform_version"]
        machine_info["total_memory"] = run.extra["runtime"]["platform_memory"]
        machine_info["cpu_info"] = run.extra["runtime"]["platform"]
        machine_info["num_cores"] = run.extra["runtime"]["platform_cpu"]
        machine_info["architecture"] = str(run.extra["runtime"]["platform_architecture"])
        return MachineInfo(**machine_info)

    def _extract_process_info(self, run: Run):
        process_info = {}
        process_info["process_path"] = run.extra["runtime"]["process_name"]
        process_info["process_id"] = run.extra["runtime"]['process_id']
        process_info["status"] = run.extra["runtime"]["process_status"]
        # process_info["process_start_time"] = run.extra["runtime"]["process_start_time"]
        return ProcessInfo(**process_info)

    # extract network information
    def _extract_network_info(self, run: Run):
        network_info = {}
        network_info["host_name"] = run.extra["runtime"]["node_name"]
        network_info["ip_address"] = run.extra["runtime"]["node_ip"]
        network_info["subnet"] = None
        return [NetworkInfo(**network_info)]

    def _extract_runtime_env(self, run: Run):
        runtime_info = {}
        runtime_info["lang_runtime"] = "python"
        runtime_info["lang_runtime_version"] = run.extra["runtime"]["langchain_version"]
        runtime_info["entry_point"] = "main.py"
        runtime_info["virtual_environment"] = "conda"
        runtime_info["environment"] = "llm-security"
        return RuntimeEnvironment(**runtime_info)

    def _extract_security_context(self, run: Run):
        security_info = {}
        security_info["user_id"] = "madan"
        security_info["group_id"] = "group-101"
        return SecurityContext(**security_info)


    def _extract_file_system_info(self, run: Run):
        file_system_info = {}
        file_system_info["working_directory"] = "/path/to/working/directory"
        file_system_info["total_disk_space_mbs"] = 102400
        file_system_info["file_system_paths"] = ["/data", "/var/logs"]

    def process_environments(self, run: Run):
        env = Environment(machine=self._extract_machine_info(run),
                          networks=self._extract_network_info(run),
                          process=self._extract_process_info(run),
                          file_system=self._extract_file_system_info(run),
                          security_context=self._extract_security_context(run),
                          request_security_context=RequestSecurityContext(),
                          runtime_environment=self._extract_runtime_env(run),
                          )
        return env
