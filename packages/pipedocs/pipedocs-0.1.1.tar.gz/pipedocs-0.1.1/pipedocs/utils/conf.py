import numbers
import os
import sys
import warnings
from configparser import ConfigParser
from operator import itemgetter
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pipedocs.exceptions import PipedocsDeprecationWarning, UsageError
from pipedocs.utils.python import without_none_values

def closest_pipedocs_cfg():
    pass

def get_config():
    pass

def init_env(project="default", set_syspath=True):
    """Initialize environment to use command-line tool from inside a project
    dir. This sets the Pipedocs settings module and modifies the Python path to
    be able to locate the project module.
    """
    # TODO
    #cfg = get_config()
    #if cfg.has_option("settings", project):
    #    os.environ["PIPEDOCS_SETTINGS_MODULE"] = cfg.get("settings", project)
    #closest = closest_pipedocs_cfg()
    #if closest:
    #    projdir = str(Path(closest).parent)
    #    if set_syspath and projdir not in sys.path:
    #        sys.path.append(projdir)

def arglist_to_dict(arglist):
    """Convert a list of arguments like ['arg1=val1', 'arg2=val2', ...] to a
    dict
    """
    return dict(x.split("=", 1) for x in arglist)

def exporter_process_params_from_cli(
    settings,
    output: List[str],
    output_format=None,
    overwrite_output: Optional[List[str]] = None,
):
    """
    Receives export params (from the 'crawl' or 'runspider' commands),
    checks for inconsistencies in their quantities and returns a dictionary
    suitable to be used as the EXPORTERS setting.
    """
    valid_output_formats = without_none_values(
        settings.getwithbase("DOC_EXPORTERS")
    ).keys()

    def check_valid_format(output_format):
        if output_format not in valid_output_formats:
            raise UsageError(
                f"Unrecognized output format '{output_format}'. "
                f"Set a supported one ({tuple(valid_output_formats)}) "
                "after a colon at the end of the output URI (i.e. -o/-O "
                "<URI>:<FORMAT>) or as a file extension."
            )

    overwrite = False
    if overwrite_output:
        if output:
            raise UsageError(
                "Please use only one of -o/--output and -O/--overwrite-output"
            )
        if output_format:
            raise UsageError(
                "-t/--output-format is a deprecated command line option"
                " and does not work in combination with -O/--overwrite-output."
                " To specify a format please specify it after a colon at the end of the"
                " output URI (i.e. -O <URI>:<FORMAT>)."
            )
        output = overwrite_output
        overwrite = True

    if output_format:
        if len(output) == 1:
            check_valid_format(output_format)
            message = (
                "The -t/--output-format command line option is deprecated in favor of "
                "specifying the output format within the output URI using the -o/--output or the"
                " -O/--overwrite-output option (i.e. -o/-O <URI>:<FORMAT>). See the documentation"
                " of the -o or -O option or the following examples for more information. "
            )
            warnings.warn(message, PipedocsDeprecationWarning, stacklevel=2)
            return {output[0]: {"format": output_format}}
        raise UsageError(
            "The -t command-line option cannot be used if multiple output "
            "URIs are specified"
        )

    result: Dict[str, Dict[str, Any]] = {}
    for element in output:
        try:
            exporter_uri, exporter_format = element.rsplit(":", 1)
        except ValueError:
            exporter_uri = element
            exporter_format = Path(element).suffix.replace(".", "")
        else:
            if exporter_uri == "-":
                exporter_uri = "stdout:"
        check_valid_format(exporter_format)
        result[exporter_uri] = {"format": exporter_format}
        if overwrite:
            result[exporter_uri]["overwrite"] = True

    # EXPORTERS setting should take precedence over the matching CLI options
    result.update(settings.getdict("EXPORTERS"))

    return result