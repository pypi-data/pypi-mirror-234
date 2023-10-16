from __future__ import annotations

import argparse
import os
from argparse import Namespace
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import asdict, is_dataclass

from .argformat import HelpAction
from .arguments import add_arguments
from .perf import timeit
from .plugin import discover_plugins_command


def newparser(subparsers: argparse._SubParsersAction, commandcls: Command):
    """Add a subparser to the parser for the command"""
    parser = subparsers.add_parser(
        commandcls.name,
        description=commandcls.help(),
        add_help=False,
    )
    parser.add_argument(
        "-h", "--help", action=HelpAction, help="show this help message and exit"
    )
    return parser


@contextmanager
def chdir(root):
    """change directory and revert back to previous directory"""
    old = os.getcwd()
    os.chdir(root)

    yield
    os.chdir(old)


class Command:
    """Base class for all commands"""

    name: str

    @classmethod
    def help(cls) -> str:
        """Return the help text for the command"""
        return cls.__doc__ or ""

    @classmethod
    def argument_class(cls):
        return cls.Arguments

    @classmethod
    def arguments(cls, subparsers):
        """Define the arguments of this command"""
        with timeit(f"{cls.name}.arguments"):
            parser = newparser(subparsers, cls)
            add_arguments(parser, cls.argument_class())

    @staticmethod
    def execute(args) -> int:
        """Execute the command"""
        raise NotImplementedError()

    @staticmethod
    def examples() -> list[str]:
        """returns a list of examples"""
        return []


def command_builder(args: dict | Namespace, ignore=None) -> list[str]:
    """Convert a namespace of arguments into a list of command line arguments for unreal engine.
    Supports dataclasses (even nested) and custom command generation through the ``to_ue_cmd`` method.

    Examples
    --------
    >>> from dataclasses import dataclass

    >>> command_builder(dict(log=True, map='/Game/Map/TopDown'))
    ['-log', '-map=/Game/Map/TopDown']

    >>> @dataclass
    ... class Arguments:
    ...     flag       : bool = False
    ...     goalscore  : Optional[float] = None
    ...     something  : Optional[str] = None

    >>> command_builder(dict(vector=Arguments(flag=True, goalscore=2, something=None)))
    ['-flag', '-goalscore=2']

    >>> command_builder(dict(vector=Arguments(flag=False, goalscore=2)))
    ['-goalscore=2']


    >>> @dataclass
    ... class Vector:
    ...     x: Optional[float] = 0
    ...     y: Optional[float] = 0
    ...     z: Optional[float] = 0
    ...     def to_ue_cmd(self, name, cmd):
    ...         cmd.append(f"-{name}=(X={self.x},Y={self.y},Z={self.z})")

    >>> command_builder(dict(vector=Vector(x=1, y=2, z=3)))
    ['-vector=(X=1,Y=2,Z=3)']

    >>> command_builder(Namespace(vector=Vector(x=1, y=2, z=3)))
    ['-vector=(X=1,Y=2,Z=3)']

    """

    with timeit("command_builder"):
        if ignore is None:
            ignore = set()

        args = deepcopy(args)

        if isinstance(args, Namespace):
            args = vars(args)

        if not isinstance(args, dict):
            args = asdict(args)

        # Note: we do not NEED to pop them, UE ignore unknown arguments
        if isinstance(args, dict):
            args.pop("command", None)
            args.pop("cli", None)
            args.pop("dry", None)

        cmd = []

        _command_builder(cmd, args, ignore)

    return cmd


def _command_builder(cmd, args, ignore):
    for k, v in args.items():
        if v is None:
            continue

        if k in ignore:
            continue

        if isinstance(v, bool):
            if v is not None and v is True:
                cmd.append(f"-{k}")

        elif isinstance(v, (str, int)):
            cmd.append(f"-{k}={v}")

        elif hasattr(v, "to_ue_cmd"):
            v.to_ue_cmd(k, cmd)

        elif is_dataclass(v):
            _command_builder(cmd, asdict(v), ignore)


class ParentCommand(Command):
    """Loads child module as subcommands"""

    dispatch: dict = dict()

    @staticmethod
    def module():
        return None

    @staticmethod
    def command_field():
        return "subcommand"

    @classmethod
    def arguments(cls, subparsers):
        parser = newparser(subparsers, cls)
        cls.shared_arguments(parser)
        subparsers = parser.add_subparsers(dest=cls.command_field(), help=cls.help())
        cmds = cls.fetch_commands()
        cls.register(cls, subparsers, cmds)

    @classmethod
    def shared_arguments(cls, subparsers):
        pass

    @classmethod
    def fetch_commands(cls):
        """Fetch commands using importlib, assume each command is inside its own module"""
        with timeit(f"{cls.name}.fetch_commands"):
            return discover_plugins_command(cls.module())

    @staticmethod
    def register(cls, subsubparsers, commands):
        name = cls.module().__name__
        for cmd in commands:
            cmd.arguments(subsubparsers)
            assert (name, cmd.name) not in cls.dispatch
            cls.dispatch[(name, cmd.name)] = cmd

    @classmethod
    def execute(cls, args):
        cmd = cls.module().__name__
        subcmd = vars(args).pop(cls.command_field())

        cmd = cls.dispatch.get((cmd, subcmd), None)
        if cmd:
            return cmd.execute(args)

        raise RuntimeError(f"Subcommand {cls.name} {subcmd} is not defined")
