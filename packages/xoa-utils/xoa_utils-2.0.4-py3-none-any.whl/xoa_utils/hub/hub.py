from __future__ import annotations
import multiprocessing
from multiprocessing import managers
from signal import SIGTERM
import os
import sys
from typing import Optional
import psutil
from xoa_utils.clis import ReadConfig

global_list = []


class HubManager(managers.SyncManager):
    pass


HubManager.register("get_list", lambda: global_list, managers.ListProxy)


class Hub:
    def __init__(self, server: str, run_port: int) -> None:
        self.manager = HubManager(address=(server, run_port), authkey=b"")

    def serve(self) -> None:
        server = self.manager.get_server()
        server.serve_forever()

    @staticmethod
    def serve_hub(server: str, run_port: int, pid_path: str) -> None:
        pid = os.getpid()
        print(f"(PID: {pid}) Starting a new hub.")
        with open(pid_path, "w") as f:
            f.write(f"{os.getpid()}")
        hub = Hub(server, run_port)
        hub.serve()

    @staticmethod
    def kill_hub(pid_path: str, pid: int) -> None:
        if pid == 0:
            return
        try:
            print(f"(PID: {pid}) Killing existing hub.")
            os.kill(int(pid), SIGTERM)
            with open(pid_path, "w"):
                pass
        except Exception as e:
            print(e)

    @staticmethod
    def start_hub(config: Optional[ReadConfig] = None):
        if config is None:
            config = ReadConfig()
        if len(sys.argv) >= 2 and sys.argv[1] == "kill":
            Hub.kill_hub(config.hub_pid_path, config.hub_pid)
        else:
            Hub.kill_hub(config.hub_pid_path, config.hub_pid)
            Hub.serve_hub(
                config.hub_host,
                config.hub_port,
                config.hub_pid_path,
            )

    @staticmethod
    def start_hub_in_process(config: ReadConfig) -> None:
        args = (config,)
        process = multiprocessing.Process(name="Hub", target=Hub.start_hub, args=args)
        process.start()

    @staticmethod
    def check_hub_process(config: ReadConfig) -> None:
        if not config.hub_enabled:
            Hub.kill_hub(config.hub_pid_path, config.hub_pid)
            return
        pid = config.hub_pid
        if not pid:
            Hub.start_hub_in_process(config)
        else:
            try:
                psutil.Process(pid)
            except psutil.NoSuchProcess:
                Hub.start_hub_in_process(config)


if __name__ == "__main__":
    Hub.start_hub()
