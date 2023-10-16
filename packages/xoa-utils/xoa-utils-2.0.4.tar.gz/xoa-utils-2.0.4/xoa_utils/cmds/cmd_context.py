from __future__ import annotations
import typing as t
from xoa_driver.testers import L23Tester
from xoa_driver.modules import GenericL23Module
from xoa_driver.ports import GenericL23Port
from xoa_utils.exceptions import (
    NotInStoreError,
    NotConnectedError,
    NoSuchIDError,
    NoWorkingPort,
    NotCorrectSerdesError,
)
from xoa_driver.hlfuncs import mgmt as mgmt_utils
from xoa_driver.hlfuncs import anlt_ll_debug as debug_utils
from xoa_driver.enums import NRZPreset, LinkTrainEncoding, LinkTrainAlgorithm
from functools import partialmethod


class ErrorString:
    def __init__(self) -> None:
        self.err_str: str = ""

    def set_val(self, value: str) -> None:
        self.err_str = value

    clear = partialmethod(set_val, "")


class TesterState:
    def __init__(self) -> None:
        self.serial: str = ""
        self.con_info: str = ""
        self.username: str = ""
        self.obj: t.Optional[L23Tester] = None


class ModuleState:
    def __init__(self) -> None:
        self.modules: dict[str, GenericL23Module] = {}
        self.module_str: str = ""


class PortState:
    def __init__(self) -> None:
        self.ports: dict[str, GenericL23Port] = {}
        self.port_str: str = ""
        self.port_serdes_num: dict[str, int] = {}


class ANState:
    def __init__(self) -> None:
        self.allow_loopback: bool = False
        self.do: bool = False


class LTState:
    def __init__(self) -> None:
        self.do: bool = False
        self.preset0: NRZPreset = NRZPreset.NRZ_NO_PRESET
        self.interactive: bool = False
        self.initial_mod: dict[str, LinkTrainEncoding] = {}
        self.algorithm: dict[str, LinkTrainAlgorithm] = {}


class LoopFuncState:
    def __init__(self) -> None:
        self.func: t.Optional[t.Callable] = None
        self.interval: int = 1
        self.kw: dict = {}


class AnltLowState:
    def __init__(self) -> None:
        self.serdes: int = -1
        self.low: t.Optional[debug_utils.AnLtLowLevelInfo] = None


class CmdContext:
    def __init__(self) -> None:
        self.clear_all()

    def clear_all(self) -> None:
        self._tr_state: TesterState = TesterState()
        self._md_state: ModuleState = ModuleState()
        self._pt_state: PortState = PortState()
        self._error: ErrorString = ErrorString()
        self._an_state: ANState = ANState()
        self._lt_state: LTState = LTState()
        self._fn_state: LoopFuncState = LoopFuncState()
        self._anlt_low_state: AnltLowState = AnltLowState()

    def get_coro_interval(self) -> int:
        return self._fn_state.interval

    def has_loop_coro(self) -> bool:
        return self._fn_state.func is not None and callable(self._fn_state.func)

    def get_loop_coro(self) -> tuple[t.Optional[t.Callable], dict]:
        return self._fn_state.func, self._fn_state.kw

    def set_loop_coro(self, coro: t.Optional[t.Callable], dic: dict) -> None:
        self._fn_state.func = coro
        self._fn_state.kw = dic

    clear_loop_coro = partialmethod(set_loop_coro, None, {})

    def prompt(self, base_prompt: str = "", end_prompt: str = ">") -> str:
        s = self.retrieve_tester_serial()
        serial = f"[{s}]" if s else ""
        p = self.retrieve_port_str()
        port_str = f"[{p}]" if p else ""
        return f"{base_prompt}{serial}{port_str} {end_prompt} "

    def store_anlt_low(self, serdes: int, low: debug_utils.AnLtLowLevelInfo) -> None:
        self._anlt_low_state.low = low
        self._anlt_low_state.serdes = serdes

    def store_lt_initial_mod(self, serdes: int, encoding: str) -> None:
        e = LinkTrainEncoding[
            {"pam4pre": "PAM4_WITH_PRECODING"}.get(encoding, encoding).upper()
        ]
        self._lt_state.initial_mod[str(serdes)] = e

    def store_lt_algorithm(self, serdes: int, algorithm: str) -> None:
        e = LinkTrainAlgorithm[algorithm.upper()]
        self._lt_state.algorithm[str(serdes)] = e

    def store_an_allow_loopback(self, do: bool) -> None:
        self._an_state.allow_loopback = do

    def store_should_do_an(self, do: bool) -> None:
        self._an_state.do = do

    def store_should_do_lt(self, do: bool) -> None:
        self._lt_state.do = do

    def store_lt_interactive(self, do: bool) -> None:
        self._lt_state.interactive = do

    def store_lt_preset0(self, preset0: str) -> None:
        if preset0 == "standard":
            self._lt_state.preset0 = NRZPreset.NRZ_NO_PRESET
        else:
            self._lt_state.preset0 = NRZPreset.NRZ_WITH_PRESET

    def store_current_module_str(self, current_module_str: str) -> None:
        if current_module_str not in self._md_state.modules:
            raise NotInStoreError(current_module_str)
        self._md_state.module_str = current_module_str

    def store_current_port_str(self, current_port_str: str) -> None:
        if current_port_str not in self._pt_state.ports:
            raise NotInStoreError(current_port_str)
        self._pt_state.port_str = current_port_str
        self._anlt_low_state = AnltLowState()

    def store_current_tester(
        self, username: str, con_info: str, tester: L23Tester
    ) -> None:
        self.clear_all()
        self._tr_state.con_info = con_info
        self._tr_state.serial = str(tester.info.serial_number)
        self._tr_state.username = username
        self._tr_state.obj = tester

    def get_all_ports(self) -> dict[str, GenericL23Port]:
        return self.obtain_physical_ports("*", False)

    def retrieve_anlt_low(self) -> t.Optional[debug_utils.AnLtLowLevelInfo]:
        return self._anlt_low_state.low

    def retrieve_anlt_serdes(self) -> int:
        return self._anlt_low_state.serdes

    def retrieve_an_enable(self) -> bool:
        return self._an_state.do

    def retrieve_an_loopback(self) -> bool:
        return self._an_state.allow_loopback

    def retrieve_lt_initial_mod(self) -> dict[str, LinkTrainEncoding]:
        return self._lt_state.initial_mod

    def retrieve_lt_initial_mod_serdes(self, serdes: int) -> LinkTrainEncoding:
        if str(serdes) not in self._lt_state.initial_mod:
            raise NotInStoreError(str(serdes))
        return self._lt_state.initial_mod[str(serdes)]

    def retrieve_lt_algorithm(self) -> dict[str, LinkTrainAlgorithm]:
        return self._lt_state.algorithm

    def retrieve_lt_algorithm_serdes(self, serdes: int) -> LinkTrainAlgorithm:
        if str(serdes) not in self._lt_state.algorithm:
            raise NotInStoreError(str(serdes))
        return self._lt_state.algorithm[str(serdes)]

    def retrieve_lt_interactive(self) -> bool:
        return self._lt_state.interactive

    def retrieve_lt_enable(self) -> bool:
        return self._lt_state.do

    def retrieve_lt_preset0(self) -> NRZPreset:
        return self._lt_state.preset0

    def retrieve_ports(self) -> dict[str, GenericL23Port]:
        return self._pt_state.ports

    def retrieve_modules(self) -> dict[str, GenericL23Module]:
        return self._md_state.modules

    def retrieve_tester_username(self) -> str:
        return self._tr_state.username

    def retrieve_tester_con_info(self) -> str:
        return self._tr_state.con_info

    def retrieve_tester_serial(self) -> str:
        return self._tr_state.serial

    def retrieve_tester(self) -> t.Optional[L23Tester]:
        return self._tr_state.obj

    def retrieve_port_str(self) -> str:
        return self._pt_state.port_str

    def store_module(self, exact_module_id: str, module_obj: GenericL23Module) -> None:
        self._md_state.modules[exact_module_id] = module_obj

    def store_port(
        self, exact_port_id: str, port_obj: GenericL23Port, port_serdes_num: int
    ) -> None:
        self._pt_state.ports[exact_port_id] = port_obj
        self._pt_state.port_serdes_num[exact_port_id] = port_serdes_num

    def retrieve_module(self, exact_module_id: str = "current") -> GenericL23Module:
        if self.retrieve_tester() is None:
            raise NotConnectedError()
        if exact_module_id == "current":
            if not self._md_state.module_str:
                raise NoWorkingPort()
            exact_module_id = self._md_state.module_str
        if exact_module_id in self._md_state.modules:
            return self._md_state.modules[exact_module_id]
        raise NotInStoreError(exact_module_id)

    def retrieve_port(self, exact_port_id: str = "current") -> GenericL23Port:
        if self.retrieve_tester() is None:
            raise NotConnectedError()
        if exact_port_id == "current":
            if not self._pt_state.port_str:
                raise NoWorkingPort()
            exact_port_id = self._pt_state.port_str
        if exact_port_id in self._pt_state.ports:
            return self._pt_state.ports[exact_port_id]
        raise NotInStoreError(exact_port_id)

    def validate_current_serdes(self, serdes: int) -> None:
        current_port_id = self._pt_state.port_str
        if current_port_id not in self._pt_state.port_serdes_num:
            raise NotInStoreError(current_port_id)
        if serdes not in range(self._pt_state.port_serdes_num[self._pt_state.port_str]):
            raise NotCorrectSerdesError(current_port_id, serdes)

    def remove_module(self, exact_module_id: str) -> None:
        if exact_module_id in self._md_state.modules:
            del self._md_state.modules[exact_module_id]

    def remove_port(self, exact_port_id: str) -> None:
        if exact_port_id in self._pt_state.ports:
            del self._pt_state.ports[exact_port_id]

    def remove_ports(self) -> None:
        self._pt_state = PortState()

    def set_error(self, error_str: str) -> None:
        self._error.set_val(error_str)

    clear_error = partialmethod(set_error, "")

    def get_error(self) -> str:
        return self._error.err_str

    def obtain_physical_modules(
        self, id_str: str = "*", update=True
    ) -> dict[str, GenericL23Module]:
        tester = self.retrieve_tester()
        if tester is None:
            raise NotConnectedError()
        m_dics = {}
        if id_str == "*":
            for m in mgmt_utils.get_modules(tester):
                m_dics[str(m.module_id)] = m
        else:
            module_id = id_str.split("/")[0]
            m = mgmt_utils.get_module(tester, int(module_id))
            m_dics[str(m.module_id)] = m

        if update:
            self._md_state.modules.update(m_dics)
        return m_dics

    def obtain_physical_ports(
        self, id_str: str = "*", update: bool = True
    ) -> dict[str, GenericL23Port]:
        tester = self.retrieve_tester()
        if tester is None:
            raise NotConnectedError()

        p_dics = {}
        if id_str == "*":
            m_id = p_id = -1
            for i in mgmt_utils.get_all_ports(tester):
                p_dics[f"{i.kind.module_id}/{i.kind.port_id}"] = i
        else:
            splitted = id_str.split("/")
            if len(splitted) == 1:
                m_id = splitted[0]
                p_id = -1
                try:
                    m_id = int(m_id)
                    for i in mgmt_utils.get_ports(tester, m_id):
                        p_dics[f"{i.kind.module_id}/{i.kind.port_id}"] = i
                except ValueError:
                    raise NoSuchIDError(id_str)
            elif len(splitted) == 2:
                m_id, p_id = splitted
                try:
                    m_id = int(m_id)
                    p_id = int(p_id)
                    i = mgmt_utils.get_port(tester, m_id, p_id)
                    p_dics[f"{i.kind.module_id}/{i.kind.port_id}"] = i
                except ValueError:
                    raise NoSuchIDError(id_str)
            else:
                raise NoSuchIDError(id_str)
        if update:
            self._pt_state.ports.update(p_dics)
        return p_dics
