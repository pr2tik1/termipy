"""
Resource-related commands for TermiPy.

This module contains commands that deal with system resource usage.
"""

import psutil
import time 
from typing import List
from termipy.base_command import Command

class ResourceUsageCommand(Command):
    def __init__(self):
        self.max_width = self.calculate_max_width()

    def calculate_max_width(self) -> int:
        """Calculate the maximum width needed for all resource sections."""
        titles = [
            "CPU Usage",
            "Memory Usage",
            "Disk Usage",
            "Network Usage",
            "Process Usage"
        ]
        
        content_widths = [
            len(f"CPU Usage: 100%"),
            len(f"Memory Usage: 100%"),
            len(f"Disk Usage: 100%"),
            len(f"Network Bytes Sent: 100 MB"),
            len(f"PID: 9999, Name: ProcessName, CPU: 100%")
        ]
        
        return max(max(len(title) for title in titles), max(content_widths)) + 4  

    def print_in_block(self, title: str, content: List[str]):
        """Encloses the title and content inside a rectangular block."""
        block_width = self.max_width

        print(f"┌{'─' * block_width}┐")
        print(f"│ {title.ljust(block_width - 2)} │")
        print(f"├{'─' * block_width}┤")
        for line in content:
            print(f"│ {line.ljust(block_width - 2)} │")
        print(f"└{'─' * block_width}┘\n")

    def cpu_usage(self):
        """Displays CPU usage."""
        cpu_percent = psutil.cpu_percent(interval=1)
        title = "CPU Usage"
        content = [
            f"CPU Usage: {cpu_percent}%"
        ]
        self.print_in_block(title, content)

    def memory_usage(self):
        """Displays memory usage."""
        memory = psutil.virtual_memory()
        title = "Memory Usage"
        content = [
            f"Memory Usage: {memory.percent}%",
            f"Total Memory: {memory.total / (1024 ** 3):.2f} GB",
            f"Available Memory: {memory.available / (1024 ** 3):.2f} GB"
        ]
        self.print_in_block(title, content)

    def disk_usage(self):
        """Displays disk usage."""
        disk = psutil.disk_usage('/')
        title = "Disk Usage"
        content = [
            f"Disk Usage: {disk.percent}%",
            f"Total Disk Space: {disk.total / (1024 ** 3):.2f} GB",
            f"Free Disk Space: {disk.free / (1024 ** 3):.2f} GB"
        ]
        self.print_in_block(title, content)

    def network_usage(self):
        """Displays network usage."""
        net_io = psutil.net_io_counters()
        title = "Network Usage"
        content = [
            f"Network Bytes Sent: {net_io.bytes_sent / (1024 ** 2):.2f} MB",
            f"Network Bytes Received: {net_io.bytes_recv / (1024 ** 2):.2f} MB"
        ]
        self.print_in_block(title, content)

    def process_usage(self):
        """Displays top 5 CPU-consuming processes."""
        processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']),
                           key=lambda x: x.info['cpu_percent'], reverse=True)[:5]
        title = "Process Usage (Top-5)"
        content = [f"PID: {proc.info['pid']}, Name: {proc.info['name']}, CPU: {proc.info['cpu_percent']}%" for proc in processes]
        self.print_in_block(title, content)

    def execute(self, args: List[str]) -> bool:
        """Continuously monitor and display resource usage until interrupted."""
        try:
            while True:
                print("\033c", end="")
                self.cpu_usage()
                self.memory_usage()
                self.disk_usage()
                self.network_usage()
                self.process_usage()
                print("\nPress Ctrl+C to STOP monitoring.\n")

                time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nStopped monitoring resource usage.")
        
        return True
