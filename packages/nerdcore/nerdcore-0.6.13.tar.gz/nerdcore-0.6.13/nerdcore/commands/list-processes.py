import os

import psutil

from nerdcore.base_entities.command_class import Command
from nerdcore.utils.nerd.theme_functions import print_table, print_t, apply_t


class ListProcesses(Command):
    def run(self):
        nerd_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if 'nerd' in proc.info['name'] or ' nerd ' in cmdline:
                    nerd_processes.append([str(proc.info['pid']), cmdline])
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        process_row_data = [process for process in nerd_processes]

        if not process_row_data:
            print_t("No ongoing nerd processes.", "important")
            return

        for process in process_row_data:
            process.append(f"taskkill /PID {process[0]} /F" if os.name == 'nt' else f"kill {process[0]}")

        table = {
            "show_headers": True,
            "header_color": "magenta",
            "row_colors": ["cyan", "yellow", "dark_grey"],
            "headers": ["PID", "Command", "Kill Command"],
            "rows": process_row_data
        }

        print_table(table, apply_t("Nerd CLI Processes", 'nerd'))
