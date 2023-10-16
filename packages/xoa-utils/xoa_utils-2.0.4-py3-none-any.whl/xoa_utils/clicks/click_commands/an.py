from __future__ import annotations
import asyncclick as ac
from xoa_driver.hlfuncs import anlt as anlt_utils
from xoa_utils.clicks import click_backend as cb
from xoa_utils.clis import format_an_status, format_an_config
from xoa_utils.clicks.click_commands.group import xoa_util
from xoa_utils.clicks import click_help as h
from xoa_utils.cmds import CmdContext


# --------------------------
# command: an
# --------------------------
@xoa_util.group(cls=cb.XenaGroup)
def an():
    """
    Commands for Auto-Negotiation.
    """


# **************************
# Type: Config
# **************************
# **************************
# sub-command: an config
# **************************
@an.command(cls=cb.XenaCommand, name="config")
@ac.option("--on/--off", type=ac.BOOL, help=h.HELP_AN_CONFIG_ON, default=True)
@ac.option(
    "--loopback/--no-loopback",
    type=ac.BOOL,
    help=h.HELP_AN_CONFIG_LOOPBACK,
    default=False,
)
@ac.pass_context
async def an_config(context: ac.Context, on: bool, loopback: bool) -> str:
    """
    Configure AN of the working port.
    """
    storage: CmdContext = context.obj
    storage.retrieve_port()
    storage.store_an_allow_loopback(loopback)
    storage.store_should_do_an(on)
    return format_an_config(storage)


# **************************
# Type: Statistics
# **************************
# **************************
# sub-command: an status
# **************************
@an.command(cls=cb.XenaCommand, name="status")
@ac.pass_context
async def an_status(context: ac.Context) -> str:
    """
    Show AN status of the working port.
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    status_dic = await anlt_utils.autoneg_status(port_obj)
    return format_an_status(status_dic)
