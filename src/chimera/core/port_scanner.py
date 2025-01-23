"""
Docker port and network scanner for ChimeraStack CLI
"""
import docker
from typing import Dict, Set, List

class PortScanner:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.used_ports: Set[int] = set()
        self.container_names: Set[str] = set()
    
    def scan(self) -> Dict[str, Set]:
        self.used_ports.clear()
        self.container_names.clear()

        containers = self.docker_client.containers.list(all=True)
        for container in containers:
            # Get port mappings
            ports = container.attrs['NetworkSettings']['Ports']
            if ports:
                for port_map in ports.values():
                    if port_map:
                        self.used_ports.add(int(port_map[0]['HostPort']))
            
            # Track container names
            self.container_names.add(container.name)

        return {
            'ports': self.used_ports,
            'names': self.container_names
        }

    def is_port_used(self, port: int) -> bool:
        return port in self.used_ports

    def get_project_containers(self, project_prefix: str) -> List[str]:
        return [name for name in self.container_names 
                if name.startswith(project_prefix)]