"""
Resource-related commands for TermiPy.

This module contains commands that deal with system resource usage.
"""

import psutil
import shutil
import GPUtil
import time
from typing import List
from termipy.base_command import Command
from colorama import Fore, Back, Style, init
import re

init(autoreset=True)

class ResourceUsageCommand(Command):
    """Display system resource usage information."""
    def __init__(self):
        self.max_width = self.calculate_max_width()
        self.output = []

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
            len(f"PID: 9999, Name: VeryLongProcessNameThatCanTakeMuchOfTheSpaceButMoreIsGood?, CPU: 100%")
        ]
        
        return max(max(len(title) for title in titles), max(content_widths)) + 4

    def strip_ansi(self, text):
        """Remove ANSI escape codes from a string."""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def print_in_block(self, title: str, content: List[str]):
        """Encloses the title and content inside a rectangular block."""
        block_width = self.max_width

        self.output.append(f"┌{'─' * block_width}┐")
        self.output.append(f"│ {Fore.CYAN}{title.ljust(block_width - 2)}{Style.RESET_ALL} │")
        self.output.append(f"├{'─' * block_width}┤")
        for line in content:
            stripped_line = self.strip_ansi(line)
            padding = block_width - len(stripped_line) - 2
            self.output.append(f"│ {line}{' ' * padding} │")
        self.output.append(f"└{'─' * block_width}┘")
        self.output.append("")

    def color_percentage(self, percentage: float) -> str:
        """Returns a colored string based on the percentage."""
        if percentage >= 90:
            return f"{Fore.RED}{percentage:.1f}%{Style.RESET_ALL}"
        elif percentage >= 70:
            return f"{Fore.YELLOW}{percentage:.1f}%{Style.RESET_ALL}"
        else:
            return f"{Fore.GREEN}{percentage:.1f}%{Style.RESET_ALL}"

    def cpu_usage(self):
        """Displays CPU usage."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            title = "CPU Usage"
            content = [
                f"CPU Usage: {self.color_percentage(cpu_percent)}"
            ]
            self.print_in_block(title, content)
        except Exception as e:
            self.print_in_block("CPU Usage", [f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}"])

    def memory_usage(self):
        """Displays memory usage."""
        try:
            memory = psutil.virtual_memory()
            title = "Memory Usage"
            content = [
                f"Memory Usage: {self.color_percentage(memory.percent)}",
                f"Total Memory: {memory.total / (1024 ** 3):.2f} GB",
                f"Available Memory: {Fore.CYAN}{memory.available / (1024 ** 3):.2f} GB{Style.RESET_ALL}"
            ]
            self.print_in_block(title, content)
        except Exception as e:
            self.print_in_block("Memory Usage", [f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}"])

    def disk_usage(self):
        """Displays disk usage."""
        try:
            # Get disk usage statistics
            total, used, free = shutil.disk_usage("/")
            total_gb = total / (1024 ** 3)  # Convert bytes to GB
            used_gb = used / (1024 ** 3)
            free_gb = free / (1024 ** 3)
            percent_used = (used / total) * 100

            # Prepare the output
            title = "Disk Usage"
            content = [
                f"Disk Usage: {self.color_percentage(percent_used)}%",
                f"Total Disk Space: {total_gb:.2f} GB",
                f"Used Disk Space: {Fore.YELLOW}{used_gb:.2f} GB{Style.RESET_ALL}",
                f"Free Disk Space: {Fore.CYAN}{free_gb:.2f} GB{Style.RESET_ALL}"
            ]
            self.print_in_block(title, content)
        except Exception as e:
            self.print_in_block("Disk Usage", [f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}"])


    def network_usage(self):
        """Displays network usage."""
        try:
            net_io = psutil.net_io_counters()
            title = "Network Usage"
            content = [
                f"Network Bytes Sent: {Fore.YELLOW}{net_io.bytes_sent / (1024 ** 2):.2f} MB{Style.RESET_ALL}",
                f"Network Bytes Received: {Fore.YELLOW}{net_io.bytes_recv / (1024 ** 2):.2f} MB{Style.RESET_ALL}"
            ]
            self.print_in_block(title, content)
        except Exception as e:
            self.print_in_block("Network Usage", [f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}"])

    def process_usage(self):
        """Displays top 10 CPU-consuming processes."""
        try:
            # Get the top 10 CPU-consuming processes
            processes = sorted(
                (proc for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']) if proc.info['cpu_percent'] is not None),
                key=lambda x: x.info['cpu_percent'],
                reverse=True
            )[:10]
            
            title = "Process Usage (Top-10)"
            pid_col_width = 10
            name_col_width = 30
            cpu_col_width = 10
            content = [
                f"{'PID:':<{pid_col_width}} {Fore.CYAN}{str(proc.info['pid']):<{pid_col_width}}{Style.RESET_ALL} "
                f"{'Name:':} {Fore.YELLOW}{proc.info['name'][:name_col_width]:<{name_col_width}}{Style.RESET_ALL} " 
                f"{'CPU:':<{cpu_col_width}} {self.color_percentage(proc.info['cpu_percent']):<{cpu_col_width}}"
                for proc in processes
            ]
            self.print_in_block(title, content)
            
        except Exception as e:
            self.print_in_block("Process Usage", [f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}"])


    def gpu_usage(self):
        """Displays GPU usage information."""
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                title = "GPU Usage"
                content = []
                for i, gpu in enumerate(gpus):
                    content.extend([
                        f"GPU {i}: {gpu.name}",
                        f"GPU Usage: {self.color_percentage(gpu.load * 100)}",
                        f"GPU Memory: {self.color_percentage(gpu.memoryUtil * 100)}",
                        f"GPU Temperature: {Fore.YELLOW}{gpu.temperature}°C{Style.RESET_ALL}"
                    ])
                self.print_in_block(title, content)
            else:
                self.print_in_block("GPU Usage", ["No GPU detected"])
        except Exception as e:
            self.print_in_block("GPU Usage", [f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}"])

    def temperature(self):
        """Displays CPU temperature if available."""
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    title = "CPU Temperature"
                    content = []
                    for name, entries in temps.items():
                        for entry in entries:
                            content.append(f"{name}: {Fore.YELLOW}{entry.current}°C{Style.RESET_ALL}")
                    self.print_in_block(title, content)
                else:
                    self.print_in_block("CPU Temperature", ["Temperature information not available"])
            else:
                self.print_in_block("CPU Temperature", ["Temperature monitoring not supported on this system"])
        except Exception as e:
            self.print_in_block("CPU Temperature", [f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}"])

    def battery_info(self):
        """Displays battery information for laptops."""
        try:
            battery = psutil.sensors_battery()
            if battery:
                title = "Battery Information"
                content = [
                    f"Battery Percentage: {self.color_percentage(battery.percent)}",
                    f"Power Plugged: {'Yes' if battery.power_plugged else 'No'}",
                    f"Time Left: {Fore.CYAN}{battery.secsleft // 3600}h {(battery.secsleft % 3600) // 60}m{Style.RESET_ALL}"
                ]
                self.print_in_block(title, content)
            else:
                self.print_in_block("Battery Information", ["No battery detected"])
        except Exception as e:
            self.print_in_block("Battery Information", [f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}"])

    def system_info(self):
        """Displays general system information."""
        try:
            title = "System Information"
            content = [
                f"OS: {platform.system()} {platform.release()}",
                f"Python Version: {platform.python_version()}",
                f"Uptime: {Fore.CYAN}{self.get_uptime()}{Style.RESET_ALL}"
            ]
            self.print_in_block(title, content)
        except Exception as e:
            self.print_in_block("System Information", [f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}"])

    def get_uptime(self):
        """Returns the system uptime as a formatted string."""
        uptime = int(time.time() - psutil.boot_time())
        days, remainder = divmod(uptime, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{days}d {hours}h {minutes}m {seconds}s"

    def execute(self, args: List[str]) -> bool:
        if self.handle_help_flag(args):
            return True
        
        try:
            while True:
                self.output = []
                self.system_info()
                self.cpu_usage()
                self.memory_usage()
                self.disk_usage()
                self.network_usage()
                self.process_usage()
                self.gpu_usage()
                self.temperature()
                self.battery_info()
                self.output.append(f"{Fore.YELLOW}Press Ctrl+C to STOP monitoring.{Style.RESET_ALL}")
                print("\033[2J\033[H", end="")
                print("\n".join(self.output))
                time.sleep(1)

        except KeyboardInterrupt:
            print(f"\n{Fore.GREEN}Stopped monitoring resource usage.{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}")
        
        return True

    def print_help(self):
        super().print_help()
        print("\nOptions:")
        print("  No options available. Press Ctrl+C to stop monitoring.")
        print("\nExample:")
        print("  resource")