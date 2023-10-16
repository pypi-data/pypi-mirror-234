from __future__ import annotations

# import configparser
import os
import typing as t
import asyncclick as ac
from xoa_driver import enums
from enum import Enum

if t.TYPE_CHECKING:
    from xoa_driver.ports import GenericL23Port
    from xoa_utils.cmds.cmd_context import CmdContext

class ASCIIStyle(Enum):
    DARKRED = "\033[31m"
    DARKGREEN = "\033[32m"
    DARKYELLOW = "\033[33m"
    DARKBLUE = "\033[34m"
    DARKMAGENTA = "\033[35m"
    DARKCYAN = "\033[36m"

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"

    DARKRED_BG = "\033[41m"
    DARKGREEN_BG = "\033[42m"
    DARKYELLOW_BG = "\033[43m"
    DARKBLUE_BG = "\033[44m"
    DARKMAGENTA_BG = "\033[45m"
    DARKCYAN_BG = "\033[46m"

    RED_BG = "\033[101m"
    GREEN_BG = "\033[102m"
    YELLOW_BG = "\033[103m"
    BLUE_BG = "\033[104m"
    MAGENTA_BG = "\033[105m"
    CYAN_BG = "\033[106m"

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

def _ascii_styler(str: str, fg_style: list[ASCIIStyle]) -> str:
        style = "".join(s.value for s in fg_style)
        return f"{style}{str}{ASCIIStyle.END.value}"

class ReadConfig:
    def __init__(
        self,
        ssh_port: str = "22622",
        ssh_key_path: str = os.path.join(os.path.expanduser("~"), ".ssh", "id_rsa"),
        hub_host: str = "localhost",
        hub_port: str = "10000",
        hub_enable: str = "false",
        hub_pid_path: str = os.path.join(
            os.path.expanduser("~"), "XenaNetworks", "XOA-UTILITIES", "hub.pid"
        ),
    ) -> None:
        try:
            ssh_port_int = int(ssh_port)
        except Exception:
            ssh_port_int = 22622
        try:
            hub_port_int = int(hub_port)
        except Exception:
            hub_port_int = 10000
        self.conn_port = ssh_port_int
        self.conn_host_keys = ssh_key_path
        self.hub_enabled = str(hub_enable).lower() == "true"
        self.hub_host = hub_host
        self.hub_port = hub_port_int
        self.hub_pid_path = hub_pid_path
        self.hub_pid = self._read_hub_pid()

    def _touch(self, realpath: str) -> None:
        realpath = os.path.abspath(realpath)
        folder = os.path.dirname(realpath)
        if not os.path.isfile(realpath):
            try:
                os.remove(realpath)
            except Exception:
                pass
            os.makedirs(folder, exist_ok=True)
            with open(realpath, "w"):
                pass

    def _read_hub_pid(self) -> int:
        pid = 0
        self._touch(self.hub_pid_path)
        with open(self.hub_pid_path, "r") as f:
            content = f.read().strip()
            try:
                pid = int(content)
            except ValueError:
                pass
        return pid


def run_coroutine_as_sync(coro: t.Coroutine) -> t.Any:
    while True:
        try:
            next(coro.__await__())
        except StopIteration as done:
            return done.value


def format_error(error: ac.UsageError) -> str:
    hint = ""
    result = ""
    if (
        error.ctx is not None
        and error.ctx.command.get_help_option(error.ctx) is not None
    ):
        hint = f"Try '{error.ctx.command_path} {error.ctx.help_option_names[0]}' for help.\n\n"
    if error.ctx is not None:
        result += f"{error.ctx.get_usage()}\n{hint}"
    result += f"Error: {error.format_message()}\n"
    result = result.replace("python -m entry", "")
    return result


def _port_dic_status(current_id: str, port_dic: dict[str, GenericL23Port]) -> str:
    string = f"------------------------------\nPort      Sync      Owner     \n------------------------------\n"
    for name, port in port_dic.items():
        new_name = f"*{name}" if current_id == name else name
        owner = "You" if port.is_reserved_by_me() else "Others"
        sync_status = str(port.info.sync_status.name)
        string += f"{new_name:10}{sync_status:10}{owner:10}\n"

    return string


def format_tester_status(storage: "CmdContext") -> str:
    serial_number = storage.retrieve_tester_serial()
    con_info = storage.retrieve_tester_con_info()
    username = storage.retrieve_tester_username()
    result_str = f"\nTester  :      {serial_number}\nConInfo :      {con_info}\nUsername:      {username}\n\n"
    result_str += _port_dic_status(
        storage.retrieve_port_str(), storage.retrieve_ports()
    )
    return result_str


def format_ports_status(storage: "CmdContext", all: bool) -> str:
    if all:
        port_dic = storage.get_all_ports()
    else:
        port_dic = storage.retrieve_ports()
    result_str = _port_dic_status(storage.retrieve_port_str(), port_dic)
    return result_str


def format_port_status(status: dict, storage: "CmdContext") -> str:
    ims = {}
    algs = {}

    for key, val in storage.retrieve_lt_initial_mod().items():
        ims[key] = enums.LinkTrainEncoding(val).name
    for key, val in storage.retrieve_lt_algorithm().items():
        algs[key] = enums.LinkTrainAlgorithm(val).name

    return f"""
{_ascii_styler("[ACTUAL CONFIG]", [ASCIIStyle.DARKGREEN_BG])}
    Link recovery         : {status['link_recovery']}
    Serdes count          : {status['serdes_count']}

    Auto-negotiation      : {status['autoneg_enabled']} ({'allow' if status['autoneg_allow_loopback'] else 'not allow'} loopback)
    Link training         : {'on' if status['link_training_mode'] != "disabled" else 'off'} ({'interactive' if status['link_training_mode'] == "interactive" else 'auto'}) (preset0: {'standard tap' if status['link_training_preset0'] == 'nrz_no_preset' else 'existing tap'} values) (timeout: {status['link_training_timeout']})
- - - - - - - - - - - - - - - - - - - - - - - - - - -
{_ascii_styler("[SHADOW CONFIG]", [ASCIIStyle.MAGENTA_BG])}
    Auto-negotiation      : {'on' if storage.retrieve_an_enable() else 'off'} ({'allow' if storage.retrieve_an_loopback() else 'not allow'} loopback)
    Link training         : {'on' if storage.retrieve_lt_enable() else 'off'} ({'interactive' if storage.retrieve_lt_interactive() else 'auto'}) (preset0: {'standard tap' if storage.retrieve_lt_preset0() == enums.NRZPreset.NRZ_NO_PRESET else 'existing tap'} values)
        Initial Mod.      : {ims}
        Algorithm         : {algs}
"""


def format_an_status(dic: dict) -> str:
    return f"""
[AN STATUS]
    Mode                  : {'enabled' if dic['is_enabled'] else 'disabled'}
    Loopback              : {dic['loopback']}

    Duration              : {dic['duration']:,} µs {'(N/A)' if dic['duration'] == 0 else ''}

    Successful runs       : {dic['successes']}
    Timeouts              : {dic['timeouts']}
    Loss of sync          : {dic['loss_of_sync']}
    FEC negotiation fails : {dic['fec_negotiation_fails']}
    HCD negotiation fails : {dic['hcd_negotiation_fails']}
                                RX    TX
    Link codewords        : {dic['link_codewords']['rx']:6}{dic['link_codewords']['tx']:6}
    Next-page messages    : {dic['next_page_messages']['rx']:6}{dic['next_page_messages']['tx']:6}
    Unformatted pages     : {dic['unformatted_pages']['rx']:6}{dic['unformatted_pages']['tx']:6}
    """


def format_lt_config(storage: CmdContext) -> str:
    ims = {}
    algs = {}

    for key, val in storage.retrieve_lt_initial_mod().items():
        ims[key] = enums.LinkTrainEncoding(val).name
    for key, val in storage.retrieve_lt_algorithm().items():
        algs[key] = enums.LinkTrainAlgorithm(val).name

    return f"""
<!>LT config to be on port {storage.retrieve_port_str()}
{_ascii_styler("[SHADOW CONFIG]", [ASCIIStyle.MAGENTA_BG])}
    Auto-negotiation      : {'on' if storage.retrieve_an_enable() else 'off'} ({'allow' if storage.retrieve_an_loopback() else 'not allow'} loopback)
    Link training         : {'on' if storage.retrieve_lt_enable() else 'off'} ({'interactive' if storage.retrieve_lt_interactive() else 'auto'}) (preset0: {'standard tap' if storage.retrieve_lt_preset0() == enums.NRZPreset.NRZ_NO_PRESET else 'existing tap'} values)
        Initial Mod.      : {ims}
        Algorithm         : {algs}
"""


def format_lt_im(status: dict, storage: CmdContext, serdes: int) -> str:
    ims = {}
    algs = {}

    for key, val in storage.retrieve_lt_initial_mod().items():
        ims[key] = enums.LinkTrainEncoding(val).name
    for key, val in storage.retrieve_lt_algorithm().items():
        algs[key] = enums.LinkTrainAlgorithm(val).name

    return f"""
{_ascii_styler("[ACTUAL CONFIG]", [ASCIIStyle.DARKGREEN_BG])}
    Link training         :
        Initial mod.      : {status['initial_mods']}
- - - - - - - - - - - - - - - - - - - - - - - - - - -
<!>LT initial modulation to be {storage.retrieve_lt_initial_mod_serdes(serdes).name} on Serdes {serdes}
{_ascii_styler("[SHADOW CONFIG]", [ASCIIStyle.MAGENTA_BG])}
    Auto-negotiation      : {'on' if storage.retrieve_an_enable() else 'off'} ({'allow' if storage.retrieve_an_loopback() else 'not allow'} loopback)
    Link training         : {'on' if storage.retrieve_lt_enable() else 'off'} ({'interactive' if storage.retrieve_lt_interactive() else 'auto'}) (preset0: {'standard tap' if storage.retrieve_lt_preset0() == enums.NRZPreset.NRZ_NO_PRESET else 'existing tap'} values)
        Initial Mod.      : {ims}
        Algorithm         : {algs}
    """


def format_lt_algorithm(status: dict, storage: CmdContext, serdes: int) -> str:
    ims = {}
    algs = {}

    for key, val in storage.retrieve_lt_initial_mod().items():
        ims[key] = enums.LinkTrainEncoding(val).name
    for key, val in storage.retrieve_lt_algorithm().items():
        algs[key] = enums.LinkTrainAlgorithm(val).name

    return f"""
{_ascii_styler("[ACTUAL CONFIG]", [ASCIIStyle.DARKGREEN_BG])}
    Link training         :
        Algorithm         : {status['algorithms']}
- - - - - - - - - - - - - - - - - - - - - - - - - - -
<!>LT algorithm to be {storage.retrieve_lt_algorithm_serdes(serdes).name} on Serdes {serdes}
{_ascii_styler("[SHADOW CONFIG]", [ASCIIStyle.MAGENTA_BG])}
    Auto-negotiation      : {'on' if storage.retrieve_an_enable() else 'off'} ({'allow' if storage.retrieve_an_loopback() else 'not allow'} loopback)
    Link training         : {'on' if storage.retrieve_lt_enable() else 'off'} ({'interactive' if storage.retrieve_lt_interactive() else 'auto'}) (preset0: {'standard tap' if storage.retrieve_lt_preset0() == enums.NRZPreset.NRZ_NO_PRESET else 'existing tap'} values)
        Initial Mod.      : {ims}
        Algorithm         : {algs}
    """


def format_an_config(storage: CmdContext) -> str:
    ims = {}
    algs = {}

    for key, val in storage.retrieve_lt_initial_mod().items():
        ims[key] = enums.LinkTrainEncoding(val).name
    for key, val in storage.retrieve_lt_algorithm().items():
        algs[key] = enums.LinkTrainAlgorithm(val).name

    return f"""
<!>AN config to be on port {storage.retrieve_port_str()}
{_ascii_styler("[SHADOW CONFIG]", [ASCIIStyle.MAGENTA_BG])}
    Auto-negotiation      : {'on' if storage.retrieve_an_enable() else 'off'} ({'allow' if storage.retrieve_an_loopback() else 'not allow'} loopback)
    Link training         : {'on' if storage.retrieve_lt_enable() else 'off'} ({'interactive' if storage.retrieve_lt_interactive() else 'auto'}) (preset0: {'standard tap' if storage.retrieve_lt_preset0() == enums.NRZPreset.NRZ_NO_PRESET else 'existing tap'} values)
        Initial Mod.      : {ims}
        Algorithm         : {algs}
"""


def format_recovery(storage: CmdContext, on: bool) -> str:
    enable = "on" if on else "off"
    return f"Port {storage.retrieve_port_str()} link recovery: {enable}\n"


def format_lt_inc_dec(
    storage: CmdContext, serdes: int, emphasis: str, increase: bool, response: str
) -> str:
    change = {
        "pre3": "c(-3)",
        "pre2": "c(-2)",
        "pre": "c(-1)",
        "main": "c(0)",
        "post": "c(1)",
    }[emphasis]
    action = "increase" if increase else "decrease"
    return f"Port {storage.retrieve_port_str()}: {action} {change} by 1 on Serdes {serdes} ({response})\n"


def format_lt_no_eq(
    storage: CmdContext, serdes: int, emphasis: str, response: str
) -> str:
    change = {
        "pre3": "c(-3)",
        "pre2": "c(-2)",
        "pre": "c(-1)",
        "main": "c(0)",
        "post": "c(1)",
    }[emphasis]
    return f"Port {storage.retrieve_port_str()}: Turning off equalizer on {change} on Serdes {serdes} ({response})\n"


def format_lt_encoding(
    storage: CmdContext, serdes: int, encoding: str, response: str
) -> str:
    e = enums.LinkTrainEncoding[
        {"pam4pre": "PAM4_WITH_PRECODING"}.get(encoding, encoding).upper()
    ]
    return f"Port {storage.retrieve_port_str()}: use {e.name} on Serdes {serdes} ({response})\n"


def format_lt_preset(
    storage: CmdContext, serdes: int, preset: int, response: str
) -> str:
    return f"Port {storage.retrieve_port_str()}: use preset {preset} on Serdes {serdes} ({response})\n"


def format_lt_trained(storage: CmdContext, serdes: int, response: str) -> str:
    return f"Port {storage.retrieve_port_str()} requests: Serdes {serdes} is trained ({response})\n"


def format_txtap_get(serdes: int, dic: dict) -> str:
    return f"""
Local Coefficient Serdes({serdes}) :           c(-3)       c(-2)       c(-1)        c(0)        c(1)
    Current level           :              {dic['c(-3)']}           {dic['c(-2)']}           {dic['c(-1)']}           {dic['c(0)']}           {dic['c(1)']}
"""


def format_txtap_set(
    serdes: int, pre3: int, pre2: int, pre: int, main: int, post: int
) -> str:
    return format_txtap_get(
        serdes, {"c(-3)": pre3, "c(-2)": pre2, "c(-1)": pre, "c(0)": main, "c(1)": post}
    )


def format_lt_status(dic: dict) -> str:
    return f"""
[LT STATUS]
    Mode              : {'enabled' if dic['is_enabled'] else 'disabled'}
    Status            : {'trained' if dic['is_trained'] else 'not trained'}
    Failure           : {dic['failure']}

    Initial mod.      : {dic['init_modulation']}
    Preset0 (oos)     : {"standard tap" if dic['preset0'] else "existing tap"} values

    Total bits        : {dic['total_bits']:,}
    Total err. bits   : {dic['total_errored_bits']:,}
    BER               : {dic['ber']}

    Duration          : {dic['duration']:,} µs {'(N/A)' if dic['duration'] == 0 else ''}

    Lock lost         : {dic['lock_lost']}
    Frame lock        : {dic['frame_lock']}
    Remote frame lock : {dic['remote_frame_lock']}

    Frame errors      : {dic['frame_errors']:,}
    Overrun errors    : {dic['overrun_errors']:,}

    Last IC received  : {dic['last_ic_received']}
    Last IC sent      : {dic['last_ic_sent']}

    TX Coefficient              :          c(-3)       c(-2)       c(-1)        c(0)        c(1)
        Current level           :{dic['c(-3)']['current_level']:15}{dic['c(-2)']['current_level']:12}{dic['c(-1)']['current_level']:12}{dic['c(0)']['current_level']:12}{dic['c(1)']['current_level']:12}
                                :         RX  TX      RX  TX      RX  TX      RX  TX      RX  TX
        + req                   :{dic['c(-3)']['+req']['rx']:11}{dic['c(-3)']['+req']['tx']:4}{dic['c(-2)']['+req']['rx']:8}{dic['c(-2)']['+req']['tx']:4}{dic['c(-1)']['+req']['rx']:8}{dic['c(-1)']['+req']['tx']:4}{dic['c(0)']['+req']['rx']:8}{dic['c(0)']['+req']['tx']:4}{dic['c(1)']['+req']['rx']:8}{dic['c(1)']['+req']['tx']:4}
        - req                   :{dic['c(-3)']['-req']['rx']:11}{dic['c(-3)']['-req']['tx']:4}{dic['c(-2)']['-req']['rx']:8}{dic['c(-2)']['-req']['tx']:4}{dic['c(-1)']['-req']['rx']:8}{dic['c(-1)']['-req']['tx']:4}{dic['c(0)']['-req']['rx']:8}{dic['c(0)']['-req']['tx']:4}{dic['c(1)']['-req']['rx']:8}{dic['c(1)']['-req']['tx']:4}
        coeff/eq limit reached  :{dic['c(-3)']['coeff_and_eq_limit_reached']['rx']:11}{dic['c(-3)']['coeff_and_eq_limit_reached']['tx']:4}{dic['c(-2)']['coeff_and_eq_limit_reached']['rx']:8}{dic['c(-2)']['coeff_and_eq_limit_reached']['tx']:4}{dic['c(-1)']['coeff_and_eq_limit_reached']['rx']:8}{dic['c(-1)']['coeff_and_eq_limit_reached']['tx']:4}{dic['c(0)']['coeff_and_eq_limit_reached']['rx']:8}{dic['c(0)']['coeff_and_eq_limit_reached']['tx']:4}{dic['c(1)']['coeff_and_eq_limit_reached']['rx']:8}{dic['c(1)']['coeff_and_eq_limit_reached']['tx']:4}
        eq limit reached        :{dic['c(-3)']['eq_limit_reached']['rx']:11}{dic['c(-3)']['eq_limit_reached']['tx']:4}{dic['c(-2)']['eq_limit_reached']['rx']:8}{dic['c(-2)']['eq_limit_reached']['tx']:4}{dic['c(-1)']['eq_limit_reached']['rx']:8}{dic['c(-1)']['eq_limit_reached']['tx']:4}{dic['c(0)']['eq_limit_reached']['rx']:8}{dic['c(0)']['eq_limit_reached']['tx']:4}{dic['c(1)']['eq_limit_reached']['rx']:8}{dic['c(1)']['eq_limit_reached']['tx']:4}
        coeff not supported     :{dic['c(-3)']['coeff_not_supported']['rx']:11}{dic['c(-3)']['coeff_not_supported']['tx']:4}{dic['c(-2)']['coeff_not_supported']['rx']:8}{dic['c(-2)']['coeff_not_supported']['tx']:4}{dic['c(-1)']['coeff_not_supported']['rx']:8}{dic['c(-1)']['coeff_not_supported']['tx']:4}{dic['c(0)']['coeff_not_supported']['rx']:8}{dic['c(0)']['coeff_not_supported']['tx']:4}{dic['c(1)']['coeff_not_supported']['rx']:8}{dic['c(1)']['coeff_not_supported']['tx']:4}
        coeff at limit          :{dic['c(-3)']['coeff_at_limit']['rx']:11}{dic['c(-3)']['coeff_at_limit']['tx']:4}{dic['c(-2)']['coeff_at_limit']['rx']:8}{dic['c(-2)']['coeff_at_limit']['tx']:4}{dic['c(-1)']['coeff_at_limit']['rx']:8}{dic['c(-1)']['coeff_at_limit']['tx']:4}{dic['c(0)']['coeff_at_limit']['rx']:8}{dic['c(0)']['coeff_at_limit']['tx']:4}{dic['c(1)']['coeff_at_limit']['rx']:8}{dic['c(1)']['coeff_at_limit']['tx']:4}
"""

def format_debug_init(dic: dict) -> str:
    return f"""
    base:        0x{dic["base"]:0>8X}
    rx_gtm_base: 0x{dic["rx_gtm_base"]:0>8X}
    rx_serdes:   {dic["rx_serdes"]}
    tx_gtm_base: 0x{dic["tx_gtm_base"]:0>8X}
    tx_serdes:   {dic["tx_serdes"]}
"""

def format_strict(storage: CmdContext, on: bool) -> str:
    enable = "on" if on else "off"
    return f"Port {storage.retrieve_port_str()} ANLT strict mode: {enable}\n"

def format_log_control(
        storage: CmdContext, 
        debug: bool, 
        an_trace: bool, 
        lt_trace: bool, 
        alg_trace: bool,
        fsm_port: bool,
        fsm_an: bool,
        fsm_an_stimuli: bool,
        fsm_lt: bool,
        fsm_lt_coeff: bool,
        fsm_lt_stimuli: bool,
        fsm_lt_alg0: bool,
        fsm_lt_algn1: bool
        ) -> str:
    return f"""
Port {storage.retrieve_port_str()} log control:
    Type debug:             {'on' if debug else 'off'}
    Type AN trace:          {'on' if an_trace else 'off'}
    Type LT trace:          {'on' if lt_trace else 'off'}
    Type ALG trace:         {'on' if alg_trace else 'off'}
    Type FSM port:          {'on' if fsm_port else 'off'}
    Type FSM AN:            {'on' if fsm_an else 'off'}
    Type FSM AN Stimuli:    {'on' if fsm_an_stimuli else 'off'}
    Type FSM LT:            {'on' if fsm_lt else 'off'}
    Type FSM LT Coeff:      {'on' if fsm_lt_coeff else 'off'}
    Type FSM LT Stimuli:    {'on' if fsm_lt_stimuli else 'off'}
    Type FSM LT ALG  0:     {'on' if fsm_lt_alg0 else 'off'}
    Type FSM LT ALG -1:     {'on' if fsm_lt_algn1 else 'off'}
"""