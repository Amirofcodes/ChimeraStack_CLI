"""
Port allocation management for ChimeraStack CLI
"""
from typing import Dict, Optional, Set
from dataclasses import dataclass
from .port_scanner import PortScanner

@dataclass
class PortRange:
    start: int
    end: int
    allocated: Set[int] = None

    def __post_init__(self):
        if self.allocated is None:
            self.allocated = set()

class PortAllocator:
    def __init__(self):
        self.scanner = PortScanner()
        self.ranges = {
            'frontend': {
                'react': PortRange(3000, 3999),
                'vue': PortRange(4000, 4999)
            },
            'backend': {
                'php': PortRange(8000, 8999),
                'node': PortRange(9000, 9999)
            },
            'database': {
                'mysql': PortRange(3300, 3399),
                'mariadb': PortRange(3400, 3499),
                'postgres': PortRange(5432, 5632)
            },
            'admin': {
                'phpmyadmin': PortRange(8081, 8180),
                'pgadmin': PortRange(8181, 8280)
            }
        }

    def get_available_port(self, service_type: str, service_name: str) -> Optional[int]:
        if service_type not in self.ranges:
            return None

        ranges = self.ranges[service_type]
        used_ports = self.scanner.scan()['ports']

        # Find specific range for service
        port_range = None
        for key, range_obj in ranges.items():
            if key in service_name.lower():
                port_range = range_obj
                break

        if port_range is None:
            port_range = next(iter(ranges.values()))

        # Find first available port in range
        for port in range(port_range.start, port_range.end + 1):
            if port not in used_ports:
                return port

        return None

    def release_port(self, port: int) -> None:
        for ranges in self.ranges.values():
            for port_range in ranges.values():
                if port_range.start <= port <= port_range.end:
                    port_range.allocated.discard(port)
                    return