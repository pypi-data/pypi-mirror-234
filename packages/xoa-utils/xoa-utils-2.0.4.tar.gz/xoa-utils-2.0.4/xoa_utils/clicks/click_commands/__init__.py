from __future__ import annotations
import typing as t
from xoa_utils.cmds import CmdContext
from xoa_utils.clicks.click_commands import an
from xoa_utils.clicks.click_commands import lt
from xoa_utils.clicks.click_commands import management
from xoa_utils.clicks.click_commands import anlt
from xoa_utils.clicks.click_commands import debug
from xoa_utils.clicks.click_commands.group import xoa_util


async def cmd_main(context: CmdContext, cmd_str: str) -> t.Any:
    context.clear_error()
    args = cmd_str.split()
    result = await xoa_util.main(args=args, standalone_mode=False, obj=context)
    return result
