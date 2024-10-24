"""
Resource-related commands for TermiPy.

This module contains commands that deal with system resource usage.
"""
import re
import psutil
import shutil
import GPUtil
import time
import lib_platform
import os
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from termipy.base_command import Command
from colorama import Fore, Style, init

@dataclass
class ResourceData:
    """Dataclass to store resource information."""
    title: str
    data: Dict[str, Any]

class ResourceMonitor(ABC):
    """Abstract base class for resource monitors."""
    
    @abstractmethod
    def collect_data(self) -> ResourceData:
        """Collect and return resource data."""
        pass

class SystemMonitor(ResourceMonitor):
    """Monitor for system and hardware information."""
    
    def collect_data(self) -> ResourceData:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = shutil.disk_usage("/")
        net_io = psutil.net_io_counters()
        
        return ResourceData(
            title="System and Hardware Information",
            data={
                "OS": self._get_os_info(),
                "CPU": self._get_cpu_info(),
                "Total RAM": self._get_total_ram(),
                "Uptime": self._get_uptime(),
                "CPU Usage": f"{cpu_percent:.1f}%",
                "Memory Usage": f"{memory.percent:.1f}%",
                "Available Memory": f"{memory.available / (1024 ** 3):.2f} GB",
                "Disk Usage": f"{(disk.used / disk.total) * 100:.1f}%",
                "Free Disk Space": f"{disk.free / (1024 ** 3):.2f} GB",
                "Network Sent": f"{net_io.bytes_sent / (1024 ** 2):.2f} MB",
                "Network Recv": f"{net_io.bytes_recv / (1024 ** 2):.2f} MB"
            }
        )

    def _get_os_info(self):
        return f"{lib_platform.system}"

    def _get_cpu_info(self):
        return f"{psutil.cpu_count(logical=False)} cores ({psutil.cpu_count()} threads)"

    def _get_total_ram(self):
        total_ram = psutil.virtual_memory().total
        return f"{total_ram / (1024**3):.2f} GB"
    
    def _get_uptime(self):
        uptime = int(time.time() - psutil.boot_time())
        days, remainder = divmod(uptime, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{days}d {hours}h {minutes}m {seconds}s"

class TemperatureMonitor(ResourceMonitor):
    """Monitor for temperature and battery information."""
    
    def collect_data(self) -> ResourceData:
        data = {}
        
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    for entry in entries:
                        data[f"CPU Temp ({name})"] = f"{entry.current}°C"
            else:
                data["Temperature"] = "Information not available"
        else:
            data["Temperature"] = "Monitoring not supported on this system"

        battery = psutil.sensors_battery()
        if battery:
            data["Battery"] = f"{battery.percent:.1f}%"
            data["Power Plugged"] = "Yes" if battery.power_plugged else "No"
            data["Time Left"] = f"{battery.secsleft // 3600}h {(battery.secsleft % 3600) // 60}m"
        else:
            data["Battery"] = "No battery detected"

        return ResourceData(title="Temperature and Battery", data=data)

class ProcessMonitor(ResourceMonitor):
    """Monitor for process and GPU usage."""
    
    def collect_data(self) -> ResourceData:
        data = {}
        
        processes = sorted(
            (proc for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']) if proc.info['cpu_percent'] is not None),
            key=lambda x: x.info['cpu_percent'],
            reverse=True
        )[:5]
        
        for i, proc in enumerate(processes, 1):
            data[f"Process {i}"] = f"PID: {proc.info['pid']:<6} Name: {proc.info['name'][:15]:<20} CPU: {proc.info['cpu_percent']:.1f}%"

        gpus = GPUtil.getGPUs()
        if gpus:
            for i, gpu in enumerate(gpus):
                data[f"GPU {i}"] = f"{gpu.name}"
                data[f"GPU {i} Usage"] = f"{gpu.load * 100:.1f}%"
                data[f"GPU {i} Memory"] = f"{gpu.memoryUtil * 100:.1f}%"
                data[f"GPU {i} Temperature"] = f"{gpu.temperature}°C"
        else:
            data["GPU"] = "No GPU detected"

        return ResourceData(title="Process and GPU Usage", data=data)

class ConsoleDisplay:
    """Manages the display of resource information in the console."""
    
    def __init__(self):
        self.clear_command = 'cls' if os.name == 'nt' else 'clear'
        init(autoreset=True)
        self.output = []

    def clear_screen(self):
        os.system(self.clear_command)

    def display(self, resource_data: List[ResourceData]):
        self.clear_screen()
        self.output = []
        for data in resource_data:
            self._add_section(data)
        print("\n".join(self.output))
        print("\nPress Ctrl+C to exit.")

    def _add_section(self, data: ResourceData):
        block_width = 80
        title = data.title
        content = self._format_content(data.data)

        self.output.append(f"┌{'─' * block_width}┐")
        self.output.append(f"│ {Fore.CYAN}{title.ljust(block_width - 2)}{Style.RESET_ALL} │")
        self.output.append(f"├{'─' * block_width}┤")
        for line in content:
            stripped_line = self.strip_ansi(line)
            padding = block_width - len(stripped_line) - 2
            self.output.append(f"│ {line}{' ' * padding} │")
        self.output.append(f"└{'─' * block_width}┘")
        self.output.append("")

    def _format_content(self, data: Dict[str, Any]) -> List[str]:
        formatted = []
        for key, value in data.items():
            color = self._get_color_for_value(key, value)
            formatted.append(f"{key}: {color}{value}{Style.RESET_ALL}")
        return formatted

    @staticmethod
    def _get_color_for_value(key: str, value: str) -> str:
        if "Usage" in key or "%" in value:
            try:
                percentage = float(value.rstrip('%'))
                if percentage < 50:
                    return Fore.GREEN
                elif percentage < 80:
                    return Fore.YELLOW
                else:
                    return Fore.RED
            except ValueError:
                return Fore.WHITE
        elif "Temperature" in key:
            try:
                temp = float(value.rstrip('°C'))
                if temp < 60:
                    return Fore.GREEN
                elif temp < 80:
                    return Fore.YELLOW
                else:
                    return Fore.RED
            except ValueError:
                return Fore.WHITE
        elif "Process" in key:
            return Fore.MAGENTA
        elif "GPU" in key:
            return Fore.BLUE
        else:
            return Fore.WHITE

    @staticmethod
    def strip_ansi(text):
        """Remove ANSI escape sequences from a string."""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

class ResourceUsageCommand(Command):
    """Display system resource usage information."""

    def __init__(self):
        self.monitors = [
            SystemMonitor(),
            TemperatureMonitor(),
            ProcessMonitor()
        ]
        self.display = ConsoleDisplay()

    def execute(self, args: List[str]) -> bool:
        if self.handle_help_flag(args):
            return True
        
        try:
            self._run_monitor()
        except KeyboardInterrupt:
            print("\nStopped monitoring resource usage.")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {str(e)}")
        
        return True

    def _run_monitor(self):
        while True:
            resource_data = [monitor.collect_data() for monitor in self.monitors]
            self.display.display(resource_data)
            time.sleep(2)  # Update every 2 seconds

    def print_help(self):
        super().print_help()
        print("\nOptions:")
        print("  No options available. Press Ctrl+C to exit.")
        print("\nExample:")
        print("  resource")
