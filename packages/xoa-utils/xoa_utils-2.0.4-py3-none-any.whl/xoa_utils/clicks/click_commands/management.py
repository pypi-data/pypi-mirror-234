from __future__ import annotations
import asyncclick as ac
import asyncio
from xoa_utils.clicks import click_backend as cb
from xoa_driver.hlfuncs import anlt as anlt_utils
from xoa_driver.hlfuncs import mgmt as mgmt_utils
from xoa_driver.testers import L23Tester
from xoa_driver.enums import MediaConfigurationType
from xoa_utils.clis import format_tester_status, format_ports_status, format_port_status
from xoa_utils.clicks.click_commands.group import xoa_util
from xoa_utils.clicks import click_help as h
from xoa_utils.cmds import CmdContext
from xoa_utils import exceptions as ex

# --------------------------
# command: connect
# --------------------------


@xoa_util.command(cls=cb.XenaCommand)
@ac.argument("device", type=ac.STRING)
@ac.argument("username", type=ac.STRING)
@ac.option("-p", "--ports", type=ac.STRING, help=h.HELP_CONNECT_PORT_LIST, default="")
@ac.option("--reset/--no-reset", type=ac.BOOL, help=h.HELP_CONNECT_RESET, default=True)
@ac.option("--force/--no-force", type=ac.BOOL, help=h.HELP_CONNECT_FORCE, default=True)
@ac.option("-P", "--password", type=ac.STRING, help=h.HELP_CONNECT_PWD, default="xena")
@ac.option("-t", "--tcp", type=ac.INT, help=h.HELP_CONNECT_TCP_PORT, default=22606)
@ac.pass_context
async def connect(
    context: ac.Context,
    device: str,
    username: str,
    ports: str,
    reset: bool,
    force: bool,
    password: str,
    tcp: int,
) -> str:
    """
    Connect to a tester for the current session.

        <DEVICE>: The chassis address to connect. Address can be in IPv4 format (e.g. 10.10.10.10), or a host name (e.g. demo.xenanetworks.com)

        <USERNAME>: Username for port reservation.
    """
    storage: CmdContext = context.obj
    real_port_list = [i.strip() for i in ports.split(",")] if ports else []
    tester = await L23Tester(device, username, password, tcp)
    con_info = f"{device}:{tcp}"
    storage.store_current_tester(username, con_info, tester)
    count = 0
    first_id = ""
    for id_str in real_port_list:
        this_module_dic = storage.obtain_physical_modules(id_str)
        for module_id, module_obj in this_module_dic.items():
            storage.store_module(module_id, module_obj)
        this_port_dic = storage.obtain_physical_ports(id_str)
        for port_id, port_obj in this_port_dic.items():
            if force:
                await mgmt_utils.reserve_port(port_obj, force)
            if reset:
                await mgmt_utils.reset_port(port_obj)
            port_serdes_num = (await anlt_utils.anlt_status(port_obj))["serdes_count"]
            storage.store_port(port_id, port_obj, port_serdes_num)
            if count == 0:
                first_id = port_id
            count += 1
    if real_port_list:
        storage.store_current_module_str(first_id.split("/")[0])
        storage.store_current_port_str(first_id)
    if force or reset:
        await asyncio.sleep(2)
        # status will change when you reserve_port or reset_port, need to wait
    return format_tester_status(storage)


# --------------------------
# command: exit
# --------------------------
@xoa_util.command(cls=cb.XenaCommand)
@ac.option("--reset/--no-reset", type=ac.BOOL, help=h.HELP_CONNECT_RESET, default=True)
@ac.option(
    "--release/--no-release", type=ac.BOOL, help=h.HELP_EXIT_RELEASE, default=True
)
@ac.pass_context
async def exit(context: ac.Context, reset: bool, release: bool) -> str:
    """
    Exit the session. Exit by terminating port reservations, disconnecting from the chassis, releasing system resources, and removing the specified port configurations.
    """
    storage: CmdContext = context.obj
    for module_id, module_obj in storage.retrieve_modules().copy().items():
        if release:
            await mgmt_utils.free_module(module_obj)
        storage.remove_module(module_id)
    for port_id, port_obj in storage.retrieve_ports().copy().items():
        if reset:
            await mgmt_utils.reset_port(port_obj)
        if release:
            await mgmt_utils.free_port(port_obj)
        storage.remove_port(port_id)

    return ""


# --------------------------
# command: port
# --------------------------
@xoa_util.command(cls=cb.XenaCommand)
@ac.argument("port", type=ac.STRING)
@ac.option("--reset/--no-reset", type=ac.BOOL, help=h.HELP_CONNECT_RESET, default=False)
@ac.option("--force/--no-force", type=ac.BOOL, help=h.HELP_CONNECT_FORCE, default=True)
@ac.pass_context
async def port(context: ac.Context, port: str, reset: bool, force: bool) -> str:
    """
    Switch the working port. If the port is not yet reserved, reserve the port. Update the working port in the cache.

        <PORT>: The port on the specified device host. Specify a port using the format slot/port, e.g. 0/0
    """
    storage: CmdContext = context.obj
    module_id = port.split("/")[0]
    try:
        storage.store_current_module_str(module_id)
        p_obj = storage.retrieve_module(module_id)
    except ex.NotInStoreError:
        module_dic = storage.obtain_physical_modules(module_id)
        for m_id, m_obj in module_dic.items():
            storage.store_module(m_id, m_obj)
            storage.store_current_module_str(m_id)
    try:
        storage.store_current_port_str(port)
        p_obj = storage.retrieve_port()
        port_serdes_num = (await anlt_utils.anlt_status(p_obj))["serdes_count"]
        storage.store_port(port, p_obj, port_serdes_num)
    except ex.NotInStoreError:
        port_dic = storage.obtain_physical_ports(port)
        for p_id, p_obj in port_dic.items():
            port_serdes_num = (await anlt_utils.anlt_status(p_obj))["serdes_count"]
            storage.store_port(p_id, p_obj, port_serdes_num)
            storage.store_current_port_str(p_id)
    port_obj = storage.retrieve_port()
    port_id = storage.retrieve_port_str()
    tester_obj = storage.retrieve_tester()

    if force:
        module_obj = mgmt_utils.get_module(tester_obj, int(module_id))
        await mgmt_utils.free_module(module_obj)
        await mgmt_utils.reserve_port(port_obj, force)
    if reset:
        await mgmt_utils.reset_port(port_obj)
    if force or reset:
        await asyncio.sleep(2)
        # status will change when you reserve_port or reset_port, need to wait
    status_dic = await anlt_utils.anlt_status(port_obj)
    return f"{format_ports_status(storage, False)}{format_port_status(status_dic, storage)}"


# --------------------------
# command: ports
# --------------------------
@xoa_util.command(cls=cb.XenaCommand)
@ac.option("--all/--no-all", type=ac.BOOL, help=h.HELP_PORTS_ALL, default=False)
@ac.pass_context
async def ports(context: ac.Context, all: bool) -> str:
    """
    List all the ports reserved by the current session.
    """
    storage: CmdContext = context.obj
    return format_ports_status(storage, all)


# --------------------------
# command: module-config
# --------------------------
@xoa_util.command(cls=cb.XenaCommand)
@ac.argument("module", type=ac.INT)
@ac.argument(
    "media",
    type=ac.Choice(
        [
            "cfp4",
            "cxp",
            "sfp28",
            "qsfp28_nrz",
            "qsfp28_pam4",
            "qsfp56_pam4",
            "qsfpdd_pam4",
            "sfp56",
            "sfpdd",
            "sfp112",
            "qsfpdd_nrz",
            "cfp",
            "base_t1",
            "base_t1s",
            "qsfpdd800",
            "qsfp112",
            "osfp800",
            "qsfpdd800_anlt",
            "qsfp112_anlt",
            "osfp800_anlt"
        ]
    ),
)
@ac.argument("port_count", type=ac.INT)
@ac.argument(
    "port_speed",
    type=ac.Choice(
        [
            "10g",
            "25g",
            "50g",
            "100g",
            "200g",
            "400g",
            "800g",

        ]
    ),
)
@ac.option("--force/--no-force", type=ac.BOOL, help=h.HELP_CONNECT_FORCE, default=True)
@ac.pass_context
async def module_config(
    context: ac.Context,
    module: int,
    media: str,
    port_count: int,
    port_speed: str,
    force: bool,
) -> str:
    """
    Change module media configuration

        <MODULE>: Specifies the module on the specified device host. Specify a module using the format slot, e.g. 0

        <MEDIA>: Specifies the media configuration type of the module. Allowed values: cfp4 | cxp | sfp28 | qsfp28_nrz | qsfp28_pam4 | qsfp56_pam4 | qsfpdd_pam4 | sfp56 | sfpdd | sfp112 | qsfpdd_nrz | cfp | base_t1 | base_t1s | qsfpdd800 | qsfp112 | osfp800 | qsfpdd800_anlt | qsfp112_anlt | osfp800_anlt

        <PORT_COUNT>: Specifies the port count of the module.

        <PORT_SPEED>: Specifies the port speed in Gbps of the module. Allowed values: 800g | 400g | 200g | 100g | 50g | 25g | 10g

    """
    storage: CmdContext = context.obj
    module_obj = storage.retrieve_module(str(module))
    await mgmt_utils.set_module_media_config(
        module_obj, MediaConfigurationType[media.upper()], force
    )
    await mgmt_utils.set_module_port_config(
        module_obj, port_count, int(
            port_speed.replace("g", "000")), force
    )
    storage.remove_ports()
    return ""
