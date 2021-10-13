"""
The entry point of the program. It launches the main application - i.e. it starts
whatever represents the mainloop in the chosen GUI toolkit.
"""
from __future__ import annotations
import argparse
from abc import ABC, abstractmethod
from typing import Dict, List

from . import APP_NAME
from .config import APP_LONG_NAME, AUTO_PLUGINS, NOTEBOOK_LAYOUT, PLUGINS, TAB_STYLE
from .core import MainApp
from .logging import logger

logger.app_name = APP_NAME


class SubCommand(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser):
        pass

    @abstractmethod
    def run(self, args: argparse.Namespace):
        pass


class RunSubCommand(SubCommand):
    def __init__(self):
        super().__init__("run", f"Run '{APP_NAME}' as a standalone app.")

    def add_arguments(self, parser: argparse.ArgumentParser):
        pass

    def run(self, args: argparse.Namespace):
        app = MainApp(
            title=APP_LONG_NAME,
            plugins_list=PLUGINS + AUTO_PLUGINS,
            notebook_layout=NOTEBOOK_LAYOUT,
            tab_style=TAB_STYLE,
        )
        app.MainLoop()


class InitSubCommand(SubCommand):
    def __init__(self):
        super().__init__(
            "init", "Initialises the current directory with an skeleton of a GUI app"
        )

    def add_arguments(self, parser: argparse.ArgumentParser):
        pass

    def run(self, args: argparse.Namespace):
        print("Initialising...")


SUB_COMMANDS: List[SubCommand] = [RunSubCommand(), InitSubCommand()]

SUB_COMMAND_BY_NAME: Dict[str, SubCommand] = {
    sub_command.name: sub_command for sub_command in SUB_COMMANDS
}


def parse_args(argv: List[str] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True
    for sub_command in SUB_COMMANDS:
        sub_parser = subparsers.add_parser(
            sub_command.name, help=sub_command.description
        )
        sub_command.add_arguments(sub_parser)

    args = parser.parse_args(argv)
    return args


def run(args: argparse.Namespace):
    sub_command = SUB_COMMAND_BY_NAME[args.command]
    sub_command.run(args)


def main(argv: List[str] = None):
    args = parse_args(argv)
    run(args)
