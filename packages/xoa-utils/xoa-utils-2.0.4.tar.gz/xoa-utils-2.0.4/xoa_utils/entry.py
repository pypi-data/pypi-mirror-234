import asyncssh
import asyncio
import asyncclick
import sys
import os
import typing as t

grandpa = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if grandpa not in sys.path:
    sys.path.append(grandpa)

from xoa_utils import __version__ as XOA_UTILS_VERSION  # noqa: E402
from xoa_utils.clis import ReadConfig  # noqa: E402
from xoa_utils.hub import Hub  # noqa: E402
from xoa_utils.ssh_server import XenaSSHServer  # noqa: E402
from xoa_utils.cmds import CmdWorker  # noqa: E402


class XenaSSHCLIHandle:
    def __init__(self, config: ReadConfig) -> None:
        self.config = config

    async def handle_client(self, process: asyncssh.SSHServerProcess) -> None:
        out = process.stdout
        setattr(out, "flush", out._chan._flush_send_buf)
        # patch the flush() method since it doesn't exist.
        asyncclick.echo(
            f"Hello {process.get_extra_info('username')}, welcome to Xena OpenAutomation Utilities server ({XOA_UTILS_VERSION})",
            file=t.cast(t.IO, out),
        )
        worker = CmdWorker(process)
        await worker.run(self.config)


async def start_server(config: ReadConfig) -> None:
    Hub.check_hub_process(config)
    print(
        f"(PID: {os.getpid()}) Xena OpenAutomation Utilities server ({XOA_UTILS_VERSION}) running on 0.0.0.0:{config.conn_port}"
    )
    server = await asyncssh.create_server(
        XenaSSHServer,
        "0.0.0.0",
        config.conn_port,
        server_host_keys=[config.conn_host_keys],
        process_factory=XenaSSHCLIHandle(config).handle_client,
    )
    await server.wait_closed()


async def xoa_utility() -> None:
    argv = (sys.argv[1],) if len(sys.argv) >= 2 else tuple()
    config = ReadConfig(*argv)
    try:
        await start_server(config)
    except (OSError, asyncssh.Error) as exc:
        sys.exit(f"Error starting server: <{type(str(exc))}> {exc}")
    except KeyboardInterrupt:
        os.remove(config.hub_pid_path)


def main() -> None:
    asyncio.run(xoa_utility())


if __name__ == "__main__":
    main()
