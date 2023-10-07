import builtins
import glob
import importlib
import inspect
import os
import pathlib
from typing import List

from bec_lib.core import bec_logger
from pylint import lint
from pylint.message import Message
from pylint.reporters import CollectingReporter
from rich.console import Console
from rich.table import Table

logger = bec_logger.logger

try:
    from bec_plugins import bec_client as client_plugins
except ImportError:
    client_plugins = None


class UserScriptsMixin:
    def __init__(self) -> None:
        super().__init__()
        self._scripts = {}

    def load_all_user_scripts(self) -> None:
        """Load all scripts from the `scripts` directory."""
        self.forget_all_user_scripts()

        # load all scripts from the scripts directory
        current_path = pathlib.Path(__file__).parent.resolve()
        script_files = glob.glob(os.path.abspath(os.path.join(current_path, "../scripts/*.py")))

        # load all scripts from the user's script directory in the home directory
        user_script_dir = os.path.join(os.path.expanduser("~"), "bec", "scripts")
        if os.path.exists(user_script_dir):
            script_files.extend(glob.glob(os.path.abspath(os.path.join(user_script_dir, "*.py"))))

        # load scripts from the plugins
        if client_plugins:
            plugin_scripts_dir = os.path.join(client_plugins.__path__[0], "scripts")
            if os.path.exists(plugin_scripts_dir):
                script_files.extend(
                    glob.glob(os.path.abspath(os.path.join(plugin_scripts_dir, "*.py")))
                )

        for file in script_files:
            self.load_user_script(file)
        builtins.__dict__.update({name: v["cls"] for name, v in self._scripts.items()})

    def forget_all_user_scripts(self) -> None:
        """unload / remove loaded user scripts from builtins. The files will remain on disk though!"""
        for name in self._scripts:
            builtins.__dict__.pop(name)
        self._scripts.clear()

    def load_user_script(self, file: str) -> None:
        """load a user script file and import all its definitions

        Args:
            file (str): Full path to the script file.
        """
        self._run_linter_on_file(file)
        module_members = self._load_script_module(file)
        for name, cls in module_members:
            if not callable(cls):
                continue
            # ignore imported classes
            if cls.__module__ != "scripts":
                continue
            if name in self._scripts:
                logger.warning(f"Conflicting definitions for {name}.")
            logger.info(f"Importing {name}")
            self._scripts[name] = {"cls": cls, "fname": file}

    def forget_user_script(self, name: str) -> None:
        """unload / remove a user scripts. The file will remain on disk."""
        if not name in self._scripts:
            logger.error(f"{name} is not a known user script.")
            return
        builtins.__dict__.pop(name)
        self._scripts.pop(name)

    def list_user_scripts(self):
        """display all currently loaded user functions"""
        console = Console()
        table = Table(title="User scripts")
        table.add_column("Name", justify="center")
        table.add_column("Location", justify="center", overflow="fold")

        for name, content in self._scripts.items():
            table.add_row(name, content.get("fname"))
        console.print(table)

    def _load_script_module(self, file) -> List:
        module_spec = importlib.util.spec_from_file_location("scripts", file)
        plugin_module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(plugin_module)
        module_members = inspect.getmembers(plugin_module)
        return module_members

    def _run_linter_on_file(self, file) -> None:
        accepted_vars = ",".join([key for key in builtins.__dict__ if not key.startswith("_")])
        reporter = CollectingReporter()
        lint.Run(
            [file, "--errors-only", f"--additional-builtins={accepted_vars}"],
            exit=False,
            reporter=reporter,
        )
        if not reporter.messages:
            return

        def _format_pylint_output(msg: Message):
            return f"Line {msg.line}, column {msg.column}: {msg.msg}."

        for msg in reporter.messages:
            logger.error(
                f"During the import of {file}, the following error was detected: \n{_format_pylint_output(msg)}.\nThe script was imported but may not work as expected."
            )
