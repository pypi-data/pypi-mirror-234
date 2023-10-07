"""Pipedocs
Base class for Pipedocs commands
"""
import argparse
import os
from pathlib import Path
from typing import Any, Dict, Optional
import inspect

from pipedocs.exceptions import UsageError
from pipedocs.utils.conf import arglist_to_dict, exporter_process_params_from_cli
from pipedocs.utils.misc import _import_file

class PipedocsCommand:
    requires_project = False

    # default settings to be used for this command instead of global defaults
    default_settings: Dict[str, Any] = {}

    exitcode = 0

    def __init__(self) -> None:
        self.settings: Any = None  # set in pipedocs.cmdline

    def set_crawler(self, crawler):
        if hasattr(self, "_crawler"):
            raise RuntimeError("crawler already set")
        self._crawler = crawler

    def syntax(self):
        """
        Command syntax (preferably one-line). Do not include command name.
        """
        return ""

    def short_desc(self):
        """
        A short description of the command
        """
        return ""

    def long_desc(self):
        """A long description of the command. Return short description when not
        available. It cannot contain newlines since contents will be formatted
        by optparser which removes newlines and wraps text.
        """
        return self.short_desc()

    def help(self):
        """An extensive help for the command. It will be shown when using the
        "help" command. It can contain newlines since no post-formatting will
        be applied to its contents.
        """
        return self.long_desc()

    def add_options(self, parser):
        """
        Populate option parse with options available for this command
        """
        group = parser.add_argument_group(title="Global Options")
        group.add_argument(
            "--logfile", metavar="FILE", help="log file. if omitted stderr will be used"
        )
        group.add_argument(
            "-L",
            "--loglevel",
            metavar="LEVEL",
            default=None,
            help=f"log level (default: {self.settings['LOG_LEVEL']})",
        )
        group.add_argument(
            "--nolog", action="store_true", help="disable logging completely"
        )
        group.add_argument(
            "--profile",
            metavar="FILE",
            default=None,
            help="write python cProfile stats to FILE",
        )
        group.add_argument("--pidfile", metavar="FILE", help="write process ID to FILE")
        group.add_argument(
            "-s",
            "--set",
            action="append",
            default=[],
            metavar="NAME=VALUE",
            help="set/override setting (may be repeated)",
        )
        group.add_argument("--pdb", action="store_true", help="enable pdb on failure")

    def process_options(self, args, opts):
        try:
            self.settings.setdict(arglist_to_dict(opts.set), priority="cmdline")
        except ValueError:
            raise UsageError("Invalid -s value, use -s NAME=VALUE", print_help=False)

        if opts.logfile:
            self.settings.set("LOG_ENABLED", True, priority="cmdline")
            self.settings.set("LOG_FILE", opts.logfile, priority="cmdline")

        if opts.loglevel:
            self.settings.set("LOG_ENABLED", True, priority="cmdline")
            self.settings.set("LOG_LEVEL", opts.loglevel, priority="cmdline")

        if opts.nolog:
            self.settings.set("LOG_ENABLED", False, priority="cmdline")

        if opts.pidfile:
            Path(opts.pidfile).write_text(
                str(os.getpid()) + os.linesep, encoding="utf-8"
            )

        if opts.pdb:
            # TODO
            #twisted.python.failure.startDebugMode()
            pass

    def run(self, args, opts):
        """
        Entry point for running commands
        """
        raise NotImplementedError


class BaseRunCommand(PipedocsCommand):
    """
    Common class used to share functionality among some commands
    """

    def add_options(self, parser):
        PipedocsCommand.add_options(self, parser)
        parser.add_argument(
            "-a",
            dest="spargs",
            action="append",
            default=[],
            metavar="NAME=VALUE",
            help="set documenter argument (may be repeated)",
        )
        parser.add_argument(
            "-o",
            "--input",
            metavar="FOLDER",
            action="append",
            help="where the json files are",
        )
        parser.add_argument(
            "-o",
            "--output",
            metavar="FILE",
            action="append",
            help="append scraped items to the end of FILE (use - for stdout),"
            " to define format set a colon at the end of the output URI (i.e. -o FILE:FORMAT)",
        )
        parser.add_argument(
            "-O",
            "--overwrite-output",
            metavar="FILE",
            action="append",
            help="dump scraped items into FILE, overwriting any existing file,"
            " to define format set a colon at the end of the output URI (i.e. -O FILE:FORMAT)",
        )
        parser.add_argument(
            "-t",
            "--output-format",
            metavar="FORMAT",
            help="format to use for dumping items",
        )

    def process_options(self, args, opts):
        PipedocsCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)
        if opts.output or opts.overwrite_output:
            exporters = exporter_process_params_from_cli(
                self.settings,
                opts.output,
                opts.output_format,
                opts.overwrite_output,
            )
            self.settings.set("EXPORTERS", exporters, priority="cmdline")

    def _classes_from_args(self, class_, class_name: str, args, opts):
        if len(args) != 1:
            raise UsageError()
        filename = Path(args[0])
        if not filename.exists():
            raise UsageError(f"File not found: {filename}\n")
        try:
            module = _import_file(filename)
        except (ImportError, ValueError) as e:
            raise UsageError(f"Unable to load {str(filename)!r}: {e}\n")
        classes = list(iter_classes(module, class_))
        if not classes:
            raise UsageError(f"No {class_name} found in file: {filename}\n")
        return classes

class PipedocsHelpFormatter(argparse.HelpFormatter):
    """
    Help Formatter for pipedocs command line help messages.
    """

    def __init__(self, prog, indent_increment=2, max_help_position=24, width=None):
        super().__init__(
            prog,
            indent_increment=indent_increment,
            max_help_position=max_help_position,
            width=width,
        )

    def _join_parts(self, part_strings):
        parts = self.format_part_strings(part_strings)
        return super()._join_parts(parts)

    def format_part_strings(self, part_strings):
        """
        Underline and title case command line help message headers.
        """
        if part_strings and part_strings[0].startswith("usage: "):
            part_strings[0] = "Usage\n=====\n  " + part_strings[0][len("usage: ") :]
        headings = [
            i for i in range(len(part_strings)) if part_strings[i].endswith(":\n")
        ]
        for index in headings[::-1]:
            char = "-" if "Global Options" in part_strings[index] else "="
            part_strings[index] = part_strings[index][:-2].title()
            underline = "".join(["\n", (char * len(part_strings[index])), "\n"])
            part_strings.insert(index + 1, underline)
        return part_strings

def iter_classes(module, class_): # TODO: move to utils?
    """Return an iterator over all classes defined in the given module
    that can be instantiated (i.e. which have name)
    """
    for obj in vars(module).values():
        if (
            inspect.isclass(obj)
            and issubclass(obj, class_)
            and obj.__module__ == module.__name__
            and getattr(obj, "name", None)
        ):
            yield obj