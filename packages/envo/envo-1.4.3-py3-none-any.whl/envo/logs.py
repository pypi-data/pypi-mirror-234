import re
import sys
import traceback
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from pygments.styles import get_style_by_name
from rhei import Stopwatch
from xonsh.pyghooks import XonshConsoleLexer

from envo.environ import environ
from envo.vendored.colorizer import Colorizer, AnsiParser
from envo import console


class Level(int, Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


@dataclass
class Msg:
    level: Level
    body: str
    time: float  # s
    descriptor: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    level_to_format = {
        Level.DEBUG: lambda m: f"<blue>{m}</blue>",
        Level.INFO: lambda m: f"<bold>{m}</bold>",
        Level.WARNING: lambda m: f"<bold><yellow>{m}</yellow></bold>",
        Level.ERROR: lambda m: f"<bold><red>{m}</red></bold>"
    }

    def __post_init__(self) -> None:
        self.body = str(self.body).lstrip()

    def print(self, add_color: bool = True, add_time: bool = False, add_level: bool = False, highlight_body: bool = False) -> None:
        msg = self.render(add_color=add_color, add_time=add_time, add_level=add_level, highlight_body=highlight_body)
        if self.level >= Level.WARNING:
            sys.stderr.write(msg + "\n")
            sys.stderr.flush()
        else:
            print(msg)

    def _fix_formatting(self, text: str) -> str:
        parser = AnsiParser()

        for match in parser._regex_tag.finditer(text):
            markup, tag = match.group(0), match.group(1)

            if tag not in {"lvl", "level"}:
                ansi = parser._get_ansicode(tag)
                if ansi is None:
                    text = text.replace(markup, markup.replace("<", "< ").replace(">", " >"))

        return text

    def render(self, add_color: bool = True, add_time: bool = False, add_level: bool = False, highlight_body: bool = False) -> str:
        if not environ.colors:
            add_color = False

        def colored(clr: str) -> str:
            if add_color:
                return clr
            else:
                return ""

        from pygments import highlight
        from pygments.formatters.terminal import TerminalFormatter

        parts = []

        if add_level:
            parts.append(f"[{self.time:.4f}]")

        if add_time:
            parts.append(f"[{self.level.name:<5}]")

        if add_level or add_time:
            parts.append(" ")

        if self.descriptor:
            descriptor = f"{colored('<green>')}({str(self.descriptor)}) {colored('</green>')}"
            parts.append(f"{descriptor}")

        if add_color:
            if highlight_body:
                lines = []
                for l in self.body.splitlines():
                    spaces = len(l) - len(l.lstrip())
                    l = l.lstrip()
                    l = self._fix_formatting(l)
                    l = highlight(
                        l,
                        XonshConsoleLexer(),
                        TerminalFormatter(style=get_style_by_name("emacs")),
                    )
                    lines.append(" " * spaces + l)
                parts.append("".join(lines))
            else:
                part = self.level_to_format[self.level](self.body)
                parts.append(part)
        else:
            parts.append(self.body)

        if self.metadata:
            parts.append(f"; {self.metadata}")

        msg = "".join(parts)
        msg = Colorizer.ansify(msg)
        msg = msg.strip()
        return msg

    def __repr__(self) -> str:
        return self.render(add_color=False)


@dataclass
class MsgFilter:
    level: Optional[Level] = None
    body_re: Optional[str] = None
    time_later: Optional[float] = None
    time_before: Optional[float] = None
    metadata_re: Optional[Dict[str, Any]] = None

    # matchers
    def matches_level(self, msg: Msg) -> bool:
        return self.level is None or msg.level == self.level

    def matches_body(self, msg: Msg) -> bool:
        return self.body_re is None or bool(re.match(self.body_re, msg.body, re.DOTALL))

    def matches_time_later(self, msg: Msg) -> bool:
        return self.body_re is None or msg.time >= self.time_later

    def matches_time_before(self, msg: Msg) -> bool:
        return self.body_re is None or msg.time < self.time_before

    def matches_metadata(self, msg: Msg) -> bool:
        if not self.metadata_re:
            return True

        for k, v in self.metadata_re.items():
            msg_value = msg.metadata.get(k)
            if msg_value is None:
                return False

            if not re.match(v, msg_value, re.DOTALL):
                return False

        return True

    def matches_all(self, msg: Msg) -> bool:
        return (
            self.matches_level(msg)
            and self.matches_body(msg)
            and self.matches_time_later(msg)
            and self.matches_time_before(msg)
            and self.matches_metadata(msg)
        )


class Messages(list):
    content = List[Msg]

    def print(self) -> None:
        ret = []

        for m in self:
            m.print()

        ret = "\n".join(ret)

        print(ret)


@dataclass
class Logger:
    name: str
    parent: Optional["Logger"] = None
    descriptor: Optional[str] = None
    log_exception_repr: bool = False

    colors: bool = True

    messages: Messages = field(init=False, default_factory=Messages)
    level: Level = field(init=False, default=Level.INFO)
    sw: Stopwatch = field(init=False, default_factory=Stopwatch)

    def __post_init__(self) -> None:
        self.sw.start()

    def create_child(self, name: str, descriptor: str) -> "Logger":
        logger = Logger(parent=self, name=name, descriptor=descriptor)
        logger.sw = self.sw
        return logger

    def clean(self) -> None:
        self.messages = Messages()

    def set_level(self, level: Level) -> None:
        self.level = level

    def _log(self, msg: Msg) -> None:
        self.messages.append(msg)

    def log(self, message: str, level: Level, metadata: Optional[Dict[str, Any]] = None, print_msg: bool = True, highlight_body: bool = False) -> None:
        msg = Msg(
            level,
            message,
            self.sw.value,
            metadata=metadata or {},
            descriptor=self.descriptor,
        )

        if level >= self.level and print_msg:
            msg.print(highlight_body=highlight_body)

        self._log(msg)

        if self.parent:
            self.parent._log(msg)

    def debug(self, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.log(message, Level.DEBUG, metadata)

    def info(self, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.log(message, Level.INFO, metadata)

    def warning(self, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.log(message, Level.WARNING, metadata)

    def error(self, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.log(message, Level.ERROR, metadata)

    def traceback(self) -> None:
        from envo.exceptions import user_code
        with user_code():
            msg = ''.join(traceback.format_exc()).strip()

        self.log(msg, level=Level.ERROR, highlight_body=True)

    def get_msgs(self, filter: MsgFilter) -> List[Msg]:
        filtered: List[Msg] = []
        for m in self.messages:
            if filter.matches_all(m):
                filtered.append(m)

        return filtered

    def print_all(self, color: bool = True) -> None:
        for m in self.messages:
            m.print(add_color=color, add_time=True, add_level=True)

    def tail(self, messages_n: int) -> None:
        for m in self.messages[-messages_n:]:
            m.print()

    def save(self, file: Path) -> None:
        pass


logger = Logger(name="root")
