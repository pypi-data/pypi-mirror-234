from __future__ import annotations
import asyncclick as ac
import typing as t

if t.TYPE_CHECKING:
    from xoa_utils.cmds import CmdContext


class XenaGroup(ac.Group):
    def __init__(self, *args: t.Any, **attrs: dict) -> None:
        attrs.setdefault("context_settings", {})
        attrs["context_settings"].update({"help_option_names": ["-h", "--help"]})
        super().__init__(*args, **attrs)

    def get_help(self, ctx: ac.Context) -> str:
        e = super().get_help(ctx)
        e = e.replace("python -m entry ", "")
        storage: CmdContext = ctx.obj
        storage.set_error(f"{e}\n")
        return e


class XenaCommand(ac.Command):
    def __init__(self, *args: t.Any, **attrs: dict) -> None:
        attrs.setdefault("context_settings", {})
        attrs["context_settings"].update({"help_option_names": ["-h", "--help"]})
        super().__init__(*args, **attrs)

    def get_help(self, ctx: ac.Context) -> str:
        e = super().get_help(ctx)
        e = e.replace("python -m entry ", "")
        storage: CmdContext = ctx.obj
        storage.set_error(f"{e}\n")
        return e
