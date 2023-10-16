from __future__ import annotations
from asyncclick.shell_completion import ShellComplete, CompletionItem
from asyncclick import BaseCommand
import typing as t
from xoa_utils.clicks import xoa_util
from xoa_utils.clicks import cmd_main
from xoa_utils.hub import HubManager
from xoa_utils.clis import ReadConfig, run_coroutine_as_sync, format_error
import asyncssh as ah
import asyncclick as ac
import os
import asyncio
from xoa_driver import exceptions as driver_ex
from xoa_utils.cmds.cmd_context import CmdContext

if t.TYPE_CHECKING:
    from asyncssh.process import SSHServerProcess
    from asyncssh.editor import SSHLineEditorChannel


class AutoCompleter(ShellComplete):
    """
    Extends ShellComplete. https://click.palletsprojects.com/en/8.1.x/shell-completion/
    """

    def __init__(
        self,
        cli: BaseCommand,
        ctx_args: dict[str, t.Any],
        prog_name: str,
        complete_var: str,
        args_raw: list[str],
    ) -> None:
        super().__init__(cli, ctx_args, prog_name, complete_var)
        self.args_raw = args_raw

    def get_completion_args(self) -> tuple[list[str], str]:
        """Use the self.args to return a tuple of ``args, incomplete``."""
        args = self.args_raw[:-1] if self.args_raw else []
        incomplete = str(self.args_raw[-1]) if self.args_raw else ""
        return args, incomplete

    def format_completion(self, item: CompletionItem) -> str:
        """Format a completion item into the form recognized by the
        shell script.

        :param item: Completion item to format.
        """
        return f"{item.value}"

    async def complete(self) -> str:
        """Produce the completion data to send back to the shell.

        By default this calls :meth:`get_completion_args`, gets the
        completions, then calls :meth:`format_completion` for each
        completion.
        """
        args, incomplete = self.get_completion_args()
        completions = await self.get_completions(args, incomplete)
        out = [self.format_completion(item) for item in completions]
        return "\t".join(out)


async def shell_complete(cli: BaseCommand, args_raw: list[str]) -> str:
    """Perform shell completion for the given CLI program.
    Mimic of :func: asyncclick.shell_completion.shell_complete.

    :param cli: Command being called.

    :return: String after completion
    """
    prog_name = "xoa_utils"
    ctx_args = {}
    completer = AutoCompleter(cli, ctx_args, prog_name, "", args_raw)
    completed = await completer.complete()
    return completed


class CmdWorker:
    def __init__(
        self,
        process: "SSHServerProcess",
        base_prompt: str = "xoa-utils",
    ) -> None:
        self.process: "SSHServerProcess" = process
        self.base_prompt: str = base_prompt
        self.channel: "SSHLineEditorChannel" = self.process.channel  # type: ignore
        self.hub_manager: t.Optional["HubManager"] = None
        self.hub_enable: bool = False
        self.hub_msg_list: list = []
        self.context = CmdContext()
        self.show_prompt = True
        self.register_keys()

    def autocomplete(self, line: str, pos: int) -> tuple[str, int]:
        if not line:
            return line, pos
        args_raw = line.split()
        coro = shell_complete(xoa_util, args_raw)
        completed = str(run_coroutine_as_sync(coro))
        if not completed:
            pass
        elif "\t" in completed:
            self.write(f"{line}\n{completed}\n\n{self.make_prompt()}")
        elif args_raw and completed.startswith(args_raw[-1]):
            new_l = args_raw[:-1] + [completed]
            line = " ".join(new_l)
        else:
            line = completed
        pos = len(line)
        return line, pos

    def register_keys(self) -> None:
        TAB = "\t"
        CTRL_Z = "\x1a"
        self.channel.register_key(TAB, self.autocomplete)
        self.channel.register_key(CTRL_Z, self.stop_coro)

    def stop_coro(self, line: str, pos: int) -> tuple[str, int]:
        self.context.clear_loop_coro()
        self.show_prompt = True
        return line, pos

    def finish(self) -> None:
        self.process.exit(0)

    def write(self, msg: str) -> None:
        self.process.stdout.write(msg)

    def put_hub_record(self, request: str, response: str, success: bool) -> None:
        if self.hub_enable and self.hub_manager:
            self.hub_msg_list.append((os.getpid(), request, response, success))  # type: ignore

    def make_prompt(self, end_prompt: str = ">") -> str:
        return self.context.prompt(self.base_prompt, end_prompt)

    def show_prompts(self, end_prompt: str) -> None:
        if self.show_prompt:
            self.write(f"\n{self.make_prompt(end_prompt)}")
        else:
            self.show_prompt = True

    async def run_interactive(self) -> None:
        self.show_prompts(">")
        request = (await self.process.stdin.readline()).strip()
        response = None
        success = False
        try:
            response = await self.dispatch(request)
            success = True
            if isinstance(response, int):
                response = self.context.get_error()
                success = False
        except ac.UsageError as error:
            response = format_error(error)
            success = False
        except driver_ex.XoaException as ee:
            response = f"{type(ee).__name__}: Driver error.\n"
            success = False
        except Exception as e:
            response = f"{type(e).__name__}: {getattr(e, 'msg', str(e))}\n"
            success = False
        if response is not None:
            self.write(f"{response}")
            self.put_hub_record(request, response, success)

    async def run_coroutine(self) -> None:
        async_func, kw = self.context.get_loop_coro()
        if async_func is not None:
            try:
                self.show_prompts("!")
                result = await async_func(self.context, **kw)
                if result:
                    self.write(f"{result}\n")
                else:
                    self.show_prompt = False
                await asyncio.sleep(self.context.get_coro_interval())
            except Exception as e:
                self.write(f"{type(e).__name__}: {e}\n")
                self.context.clear_loop_coro()

    async def run(self, config: ReadConfig) -> None:
        self.connect_hub(config)
        while not self.process.stdin.at_eof():
            try:
                if self.context.has_loop_coro():
                    await self.run_coroutine()
                else:
                    await self.run_interactive()
            except ah.TerminalSizeChanged:
                self.show_prompt = False
            except ah.BreakReceived:
                self.finish()

    def connect_hub(self, config: ReadConfig) -> None:
        self.hub_enable = config.hub_enabled
        if config.hub_enabled:
            self.hub_manager = HubManager(
                address=(config.hub_host, config.hub_port), authkey=b""
            )
            self.hub_manager.connect()
            self.hub_msg_list = self.hub_manager.get_list()  # type: ignore

    async def dispatch(self, msg: str) -> str:
        if not msg:
            return ""
        if msg.lower() == "exit":
            await cmd_main(self.context, msg)
            self.finish()
            return ""
        return await cmd_main(self.context, msg)
