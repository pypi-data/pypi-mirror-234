from __future__ import annotations
import asyncclick as ac
import typing as t
import json
from xoa_utils.clicks.click_commands.group import xoa_util
from xoa_utils.clicks import click_backend as cb
from xoa_utils.cmds import CmdContext
from xoa_driver.hlfuncs import (
    anlt_ll_debug as debug_utils,
)
import time
import json
import csv
from xoa_utils.clis import (
    format_debug_init
)


@xoa_util.group(cls=cb.XenaGroup)
def debug():
    """
    Commands for debugging.\n
    """


# --------------------------
# command: init
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def init(context: ac.Context, serdes: int) -> str:
    """
    Debug: Initialize debug

        <SERDES>: Serdes index.
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    inf = await debug_utils.init(port_obj, serdes)
    storage.store_anlt_low(serdes, inf)
    inf_dic = {
        "base": inf.base,
        "rx_gtm_base": inf.rx_gtm_base,
        "tx_gtm_base": inf.tx_gtm_base,
        "rx_serdes": inf.rx_serdes,
        "tx_serdes": inf.tx_serdes
    }
    return format_debug_init(inf_dic)


async def _help_get(func: t.Callable, context: ac.Context, serdes: int) -> str:
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    or_inf = inf = storage.retrieve_anlt_low()
    if storage.retrieve_anlt_serdes() == serdes or or_inf is not None:
        inf = or_inf
    else:
        inf = await debug_utils.init(port_obj, serdes)
        storage.store_anlt_low(serdes, inf)
    return str(await func(port_obj, serdes, inf=inf))


async def _help_set(
    func: t.Callable, context: ac.Context, serdes: int, value: int
) -> str:
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    or_inf = inf = storage.retrieve_anlt_low()
    if storage.retrieve_anlt_serdes() == serdes or or_inf is not None:
        inf = or_inf
    else:
        inf = await debug_utils.init(port_obj, serdes)
        storage.store_anlt_low(serdes, inf)
    await func(port_obj, serdes, value=value, inf=inf)
    return ""


# --------------------------
# command: serdes-reset
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def serdes_reset(context: ac.Context, serdes: int) -> str:
    """
    Debug: Reset serdes

        <SERDES>: Serdes index.
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    or_inf = inf = storage.retrieve_anlt_low()
    if storage.retrieve_anlt_serdes() == serdes or or_inf is not None:
        inf = or_inf
    else:
        inf = await debug_utils.init(port_obj, serdes)
        storage.store_anlt_low(serdes, inf)
    await debug_utils.serdes_reset(port_obj, serdes, inf=inf)
    return ""


# --------------------------
# command: mode-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def mode_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Get mode

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.mode_get, context, serdes)


# --------------------------
# command: mode-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def mode_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Set mode

        <SERDES>: Serdes index.

        <VALUE>: Value.
    """

    return await _help_set(debug_utils.mode_set, context, serdes, value)


# --------------------------
# command: an-tx-config-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def an_tx_config_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read AN TX config

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.an_tx_config_get, context, serdes)


# --------------------------
# command: an-tx-config-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def an_tx_config_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Write AN TX config

        <SERDES>: Serdes index.

        <VALUE>: Value.
    """
    return await _help_set(debug_utils.an_tx_config_set, context, serdes, value)


# --------------------------
# command: an-rx-config-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def an_rx_config_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read AN RX config

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.an_rx_config_get, context, serdes)


# --------------------------
# command: an-rx-config-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def an_rx_config_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Write AN RX config

        <SERDES>: Serdes index.

        <VALUE>: Value.
    """
    return await _help_set(debug_utils.an_rx_config_set, context, serdes, value)


# --------------------------
# command: an-rx-dme-mv-range-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def an_rx_dme_mv_range_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read AN MV range

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.an_rx_dme_mv_range_get, context, serdes)

# --------------------------
# command: an-rx-dme-mv-range-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def an_rx_dme_mv_range_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Write AN MV range

        <SERDES>: Serdes index.

        <VALUE>: Value.
    """
    return await _help_set(debug_utils.an_rx_dme_mv_range_set, context, serdes, value)

# --------------------------
# command: an-rx-dme-bit-range-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def an_rx_dme_bit_range_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read AN TX config of the serdes.

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.an_rx_dme_bit_range_get, context, serdes)

# --------------------------
# command: an-rx-dme-bit-range-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def an_rx_dme_bit_range_set(context: ac.Context, serdes: int, value:int) -> str:
    """
    Debug: Write AN MV range

        <SERDES>: Serdes index.

        <VALUE>: Value.
    """
    return await _help_set(debug_utils.an_rx_dme_bit_range_set, context, serdes, value)

# --------------------------
# command: an-status
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def an_status(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read AN status

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.an_status, context, serdes)


# --------------------------
# command: an-tx-page0-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def an_tx_page0_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read AN TX page0

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.an_tx_page0_get, context, serdes)


# --------------------------
# command: an-tx-page0-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def an_tx_page0_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Write AN PAGE (page0, page1)


        <SERDES>: Serdes index.

        <VALUE>: Value.
    """
    return await _help_set(debug_utils.an_tx_page0_set, context, serdes, value)


# --------------------------
# command: an-tx-page1-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def an_tx_page1_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read AN TX page1

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.an_tx_page1_get, context, serdes)


# --------------------------
# command: an-tx-page1-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def an_tx_page1_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Set page1 of AN page


        <SERDES>: Serdes index.

        <VALUE>: Value.
    """
    return await _help_set(debug_utils.an_tx_page1_set, context, serdes, value)


# --------------------------
# command: an-rx-page0-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def an_rx_page0_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read AN RX page0

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.an_rx_page0_get, context, serdes)


# --------------------------
# command: an-rx-page1-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def an_rx_page1_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read AN RX page1

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.an_rx_page1_get, context, serdes)


# --------------------------
# command: lt-tx-config-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_tx_config_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT TX config

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.lt_tx_config_get, context, serdes)


# --------------------------
# command: lt-tx-config-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_tx_config_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Write LT TX config

        <SERDES>: Serdes index.

        <VALUE>: Value.
    """
    return await _help_set(debug_utils.lt_tx_config_set, context, serdes, value)


# --------------------------
# command: lt-rx-config-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_rx_config_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT RX config

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.lt_rx_config_get, context, serdes)


# --------------------------
# command: lt-rx-config-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_rx_config_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Write LT RX config

        <SERDES>: Serdes index.

        <VALUE>: Value.
    """
    return await _help_set(debug_utils.lt_rx_config_set, context, serdes, value)


# --------------------------
# command: lt-tx-tf-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_tx_tf_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT TX Training Frames

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.lt_tx_tf_get, context, serdes)


# --------------------------
# command: lt-tx-tf-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_tx_tf_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Write LT TX Test Frame

        <SERDES>: Serdes index.

        <VALUE>: Value.
    """
    return await _help_set(debug_utils.lt_tx_tf_set, context, serdes, value)


# --------------------------
# command: lt-rx-tf-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_rx_tf_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT RX Test Frame

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.lt_rx_tf_get, context, serdes)


# --------------------------
# command: lt-rx-error-stat0-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_rx_error_stat0_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT RX Error Stat0

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.lt_rx_error_stat0_get, context, serdes)


# --------------------------
# command: lt-rx-error-stat1-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_rx_error_stat1_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT RX Error Stat1

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.lt_rx_error_stat1_get, context, serdes)


# --------------------------
# command: lt-status
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_status(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT status

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.lt_status, context, serdes)


# --------------------------
# command: lt-prbs-ber
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_prbs_ber(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT BRPS-13 BER

        <SERDES>: Serdes index.
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    or_inf = inf = storage.retrieve_anlt_low()
    if storage.retrieve_anlt_serdes() == serdes or or_inf is not None:
        inf = or_inf
    else:
        inf = await debug_utils.init(port_obj, serdes)
        storage.store_anlt_low(serdes, inf)
    dic = await debug_utils.lt_prbs(port_obj, serdes, inf=inf)
    return json.dumps(dic, indent=2)


# --------------------------
# command: xla-config-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def xla_config_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read Xena Logic Analyzer config

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.xla_config_get, context, serdes)


# --------------------------
# command: xla-config-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def xla_config_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Write Xena Logic Analyzer config

        <SERDES>: Serdes index.

        <VALUE>: Value.
    """
    await _help_set(debug_utils.xla_config_set, context, serdes, value)
    return ""


# --------------------------
# command: xla-trig-mask-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def xla_trig_mask_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read Xena Logic Analyzer trigger mask

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.xla_trig_mask_get, context, serdes)


# --------------------------
# command: xla-trig-mask-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def xla_trig_mask_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Write Xena Logic Analyzer trigger mask

        <SERDES>: Serdes index.

        <VALUE>: Value.
    """
    await _help_set(debug_utils.xla_trig_mask_set, context, serdes, value)
    return ""


# --------------------------
# command: xla-status-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def xla_status_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read Xena Logic Analyzer status

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.xla_status_get, context, serdes)


# --------------------------
# command: xla-rd-addr-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def xla_rd_addr_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read Xena Logic Analyzer RD Address

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.xla_rd_addr_get, context, serdes)


# --------------------------
# command: xla-rd-addr-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def xla_rd_addr_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Write Xena Logic Analyzer RD Address

        <SERDES>: Serdes index.

        <VALUE>: Value.
    """
    await _help_set(debug_utils.xla_rd_addr_set, context, serdes, value)
    return ""


# --------------------------
# command: xla-rd-page-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def xla_rd_page_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read Xena Logic Analyzer RD Page

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.xla_rd_page_get, context, serdes)


# --------------------------
# command: xla-rd-page-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def xla_rd_page_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Write Xena Logic Analyzer RD Page

        <SERDES>: Serdes index.

        <VALUE>: Value.
    """
    await _help_set(debug_utils.xla_rd_page_set, context, serdes, value)
    return ""


# --------------------------
# command: xla-rd-data-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def xla_rd_data_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read Xena Logic Analyzer RD Data

        <SERDES>: Serdes index.
    """
    return await _help_get(debug_utils.xla_rd_data_get, context, serdes)


# --------------------------
# command: xla-dump
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.option("-f", "--filename", type=ac.STRING, default="")
@ac.pass_context
async def xla_dump(context: ac.Context, serdes: int, filename: str) -> str:
    """
    Debug: Show the Xena Logic Analyzer dump

        <SERDES>: Serdes index.
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    or_inf = inf = storage.retrieve_anlt_low()
    if storage.retrieve_anlt_serdes() == serdes or or_inf is not None:
        inf = or_inf
    else:
        inf = await debug_utils.init(port_obj, serdes)
        storage.store_anlt_low(serdes, inf)
    ret_dict = await debug_utils.xla_dump(port_obj, serdes, inf=inf)
    fieldnames = []
    for key in ret_dict.keys():
        fieldnames.append(key)
    if filename:
        with open(filename, "w+") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
            writer.writeheader()
            writer.writerow(ret_dict)
        return "Result stored in csv file"
    else:
        return json.dumps(ret_dict, indent=2)


# --------------------------
# command: xla-trig-n-dump
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.option("-m", "--mask", type=ac.STRING, default="0x00000FF0")
@ac.option("-o", "--window-offset", type=ac.STRING, default="0x0080")
@ac.option("-s", "--trigger-select", type=ac.STRING, default="0x0001")
@ac.option("-f", "--filename", type=ac.STRING, default="xla_dump.csv")
@ac.pass_context
async def xla_trig_n_dump(context: ac.Context, serdes: int, mask: str, window_offset: str, trigger_select: str, filename: str) -> str:
    """
    Debug: Trigger and dump the Xena Logic Analyzer data

        <SERDES>: Serdes index.
    """
    if not mask.startswith("0x"):
        return "Missing 0x for --mask option"
    if not window_offset.startswith("0x"):
        return "Missing 0x for --window-offset option"
    if not trigger_select.startswith("0x"):
        return "Missing 0x for --trigger-select option"
    
    # Set the XLA trigger mask and verify the result
    try:
        mask_value = int(mask, 16)
        await _help_set(debug_utils.xla_trig_mask_set, context, serdes, mask_value)
        resp = await _help_get(debug_utils.xla_trig_mask_get, context, serdes)
        if int(resp) != mask_value:
            return f"Setting mask failed. (expecting {mask} but get {resp:#010x})"
    except ValueError:
        return "Invalid hex string for --mask option"
    
    # Config the XLA trigger and verify the result
    try:
        window_offset_value = int(window_offset, 16) << 16
        trigger_select_value = int(trigger_select, 16)
        config_value = window_offset_value + trigger_select_value
        await _help_set(debug_utils.xla_config_set, context, serdes, config_value)
        resp = await _help_get(debug_utils.xla_config_get, context, serdes)
        if int(resp) != window_offset_value:
            return f"Configuring trigger failed. (expecting {window_offset_value:#010x} but get {resp:#010x})"
    except ValueError:
        return "Invalid hex string for --window-offset and/or --trigger-select options"
    
    # Check status and dump data
    xla_status = 0
    for _ in range(10):
        xla_status = await _help_get(debug_utils.xla_status_get, context, serdes)
        if int(xla_status) == 1:
            break
        else:
            time.sleep(1)
    if int(xla_status) == 0:
        return "XLA status time out"
    
    # Dump data
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    or_inf = inf = storage.retrieve_anlt_low()
    if storage.retrieve_anlt_serdes() == serdes or or_inf is not None:
        inf = or_inf
    else:
        inf = await debug_utils.init(port_obj, serdes)
        storage.store_anlt_low(serdes, inf)
    ret_dict = await debug_utils.xla_dump(port_obj, serdes, inf=inf)
    fieldnames = []
    for key in ret_dict.keys():
        fieldnames.append(key)
    if filename:
        with open(filename, "w+") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
            writer.writeheader()
            writer.writerow(ret_dict)
        return "Result stored in csv file"
    else:
        return json.dumps(ret_dict, indent=2)
    

# --------------------------
# command: px-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("page", type=ac.INT)
@ac.argument("reg", type=ac.STRING)
@ac.pass_context
async def px_get(context: ac.Context, page: int, reg: str) -> str:
    """
    Debug: Get register value.

        <PAGE_ADDRESS>: Page address in decimal.

        <REG_ADDRESS>: Register address in HEX string.
    """
    if not reg.startswith("0x"):
        return "Missing 0x for <REG_ADDRESS>"
    
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()

    resp = await debug_utils.px_get(port_obj, page_address=page, register_address=int(reg,16))
    if resp[0] == False:
        return f"\033[91mDEAD Error\033[0m: PAGE_ADDRESS: {page}, REG_ADDRESS: {reg}, value: {resp[1]}"
    else:
        return f"PAGE_ADDRESS: {page}, REG_ADDRESS: {reg}, value: {resp[1]}"

# --------------------------
# command: px-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("page", type=ac.INT)
@ac.argument("reg", type=ac.STRING)
@ac.argument("value", type=ac.STRING)
@ac.pass_context
async def px_set(context: ac.Context, page: int, reg: str, value: str) -> str:
    """
    Debug: Set register value

        <PAGE_ADDRESS>: Page address in decimal.

        <REG_ADDRESS>: Register address in HEX string.

        <VALUE>: Value to write in HEX string
    """
    
    if not reg.startswith("0x"):
        return "Missing 0x for <REG_ADDRESS>"
    if not value.startswith("0x"):
        return "Missing 0x for <VALUE>"
    
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()

    await debug_utils.px_set(port_obj, page_address=page, register_address=int(reg,16), value=int(value,16))
    resp = await debug_utils.px_get(port_obj, page_address=page, register_address=int(reg,16))
    if resp[0] == False:
        return f"\033[91mFailed\033[0m: PAGE_ADDRESS: {page}, REG_ADDRESS: {reg}, value: {resp[1]}"
    else:
        return f"\033[92mSuccess\033[0m: PAGE_ADDRESS: {page}, REG_ADDRESS: {reg}, value: {resp[1]}"
    

# --------------------------
# command: xla-dump-ctrl
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.option("--on/--off", type=ac.BOOL, default=True)
@ac.pass_context
async def xla_dump_ctrl(context: ac.Context, on: bool) -> str:
    """
    Debug: Control XLA auto dump
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    await debug_utils.xla_dump_ctrl(port_obj, on)
    return f"XLA auto dump {'on' if on else 'off'}"