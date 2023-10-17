import decimal
import inspect
import re
from collections import deque
from types import FrameType
from typing import Any, Deque

from memoization import cached
from rich.console import Console
from rich.highlighter import ReprHighlighter
from rich.pretty import pprint  # noqa
from rich.table import Table
from rich.theme import Theme

from logrich.config import config


console = Console()


def combine_regex(*regexes: str) -> str:
    """Combine a number of regexes in to a single regex.

    Returns:
        str: New regex with all regexes ORed together.
    """
    return "|".join(regexes)


class MyReprHighlighter(ReprHighlighter):
    """подсветка вывода на основе регул. выражений"""

    # https://regex101.com/r/zR2hP5/1
    base_style = "repr."
    highlights = [
        r"'(?P<str>[\S\s]*)'",
        r":\s\'(?P<value>.+)\'",
        r"['](?P<string_list_tuple>\w+)[']",
        r"(?P<digit2>\d*)[\"\s,[,(](?P<digit>\d*\.?\s?-?\d*-?\.?\d+)",
        combine_regex(
            r"(?P<brace>[][{}()])",  # noqa
            r"\'(?P<key>[\w-]+)\'(?P<colon>:)",
            r"(?P<comma>,)\s",
        ),
        r"(?P<quotes>\')",
        r"(?P<equal>=)",  # noqa
        r"(?P<class_name>[A-Z].*)\(",
        r'(?P<attrib_name>[\w_]{1,50})=(?P<attrib_value>"?[\w_]+"?)?',
        r"\b(?P<bool_true>True)\b|\b(?P<bool_false>False)\b|\b(?P<none>None)\b",
    ]


color_of_digit = "bold magenta"

theme = Theme(
    # https://www.w3schools.com/colors/colors_picker.asp
    # https://htmlcolorcodes.com/color-names/
    # https://colorscheme.ru/
    {
        "repr.brace": "bold black",
        "repr.str": "green",
        "repr.attrib_name": "#0099ff",
        "repr.equal": "red dim",
        "repr.digit": color_of_digit,
        "repr.digit2": color_of_digit,
        "repr.colon": "#D2691E",
        "repr.quotes": "#778899",
        "repr.comma": "#778899",
        "repr.key": "#08e8de",
        "repr.bool_true": "bold blue",
        "repr.none": "blue",
        "repr.bool_false": "yellow",
        "repr.class_name": "magenta bold",
        "repr.string_list_tuple": "green",
        "trace_msg": "#05a7f7",
        "debug_msg": "#e64d00",
        "info_msg": "#33ccff",
        "success_msg": "green",
        "warning_msg": "yellow",
        "error_msg": "#ff5050",
        "critical_msg": "#de0b2e",
    },
)

# инстанс консоли rich
console_dict = Console(
    highlighter=MyReprHighlighter(),
    theme=theme,
    markup=True,
    log_time=False,
    log_path=False,
    safe_box=True,
)


@cached
class Log:
    """Extension log, use in tests."""

    def __init__(self, config: dict, **kwargs):
        self.deque: Deque = deque()
        self.config = config
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def print(self, msg: str, frame: FrameType | None = None, **kwargs) -> None:
        """Extension log."""
        if not (level := self.deque.pop()):  # noqa WPS332
            return
        frame = frame or inspect.currentframe().f_back  # type: ignore
        file_name = kwargs.get("file_name", frame.f_code.co_filename)[-30:]  # type: ignore
        line = kwargs.get("line", frame.f_lineno)  # type: ignore
        title = kwargs.get("title", "---")

        if isinstance(msg, (str, int, float, bool, type(decimal), type(None))):
            self.print_tbl(message=msg, file=file_name, line=line, level=level)
        elif isinstance(msg, (dict, tuple, list)):
            # TODO add message for dict, tuple etc.
            self.print_tbl(message=title, file=file_name, line=line, level=level)
            self.format_extra_obj(message=msg)
        else:
            self.print_tbl(message=msg, file=file_name, line=frame.f_lineno, level=level)

    def print_tbl(
        self,
        level: str,
        file: str,
        line: int,
        message: str = "",
    ) -> str:
        """Форматирует вывод логгера в табличном виде"""
        level_key = f"LOG_LEVEL_{level.upper()}_TPL"
        level_style = self.config.get(level_key, "").strip('"')
        table = Table(
            highlight=True,
            show_header=False,
            padding=0,
            collapse_padding=True,
            show_footer=False,
            expand=True,
            box=None,
        )
        stamp = f"{level_style:<9}"
        # LEVEL
        table.add_column(
            justify="left",
            min_width=9,
            max_width=15,
        )
        try:
            style = getattr(self, f"{level}_style")
        except AttributeError:
            style = re.match(r"^\[(.*)].", level_style).group(1)  # type: ignore
            if style:
                style = style.replace("reverse", "")  # type: ignore
        # MESSAGE
        table.add_column(ratio=100, overflow="fold", style=style)
        # FILE
        table.add_column(justify="right", ratio=50, overflow="fold")
        # LINE
        table.add_column(ratio=2, overflow="crop")  # для паддинга справа
        msg = f"{message}"
        file_info = f"[grey42]{file}...[/][red]{line}[/]"

        table.add_row(stamp, msg, file_info)

        with console.capture() as capture:
            console_dict.print(table, markup=True)
        return capture.get()  # noqa WPS441

    def __getattr__(self, *args, **kwargs):
        """
        метод __getattr__ определяет поведение,
        когда наш атрибут, который мы пытаемся получить, не найден
        """
        name = args[0]
        if name.endswith(("style",)):
            return object.__getattribute__(self, name)  # noqa WPS609
        self.deque.append(name)
        return self.print

    @staticmethod
    def print_message_for_table(message: Any) -> str:
        # инстанс консоли rich
        console_ = Console(
            no_color=True,
            markup=False,
            safe_box=True,
            highlight=False,
        )

        with console_.capture() as capture:
            console_.print(
                message,
                markup=False,
                width=80,
            )
        return capture.get()  # noqa WPS441

    def format_extra_obj(self, message: Any) -> None:
        """форматирует вывод исключений в цвете и в заданной ширине, исп-ся rich"""
        table = Table(
            padding=(0, 2),
            highlight=True,
            show_footer=False,
            box=None,
        )

        table.add_column()

        # MESSAGE
        table.add_row(self.print_message_for_table(message=message))

        console_dict.print(table, markup=True)


log = Log(
    config=config,
    dev_style="blue",
    run_style="cyan",
    end_style="cyan",
    start_style="cyan",
    trace_style="turquoise2",
    debug_style="dark_orange3",
)
