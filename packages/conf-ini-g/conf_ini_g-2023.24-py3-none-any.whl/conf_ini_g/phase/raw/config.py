# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import configparser as cfpr
import sys as sstm
from typing import Any, Literal, get_args

from conf_ini_g.extension.path import any_path_h
from conf_ini_g.extension.string import Flattened
from conf_ini_g.interface.constant import (
    INI_COMMENT_MARKER,
    INI_VALUE_ASSIGNMENT,
    PARAMETER_COLOR,
    SECTION_COLOR,
)

ini_config_h = dict[str, dict[str, str]]  # Without value interpretation
typed_config_h = dict[
    str, dict[str, Any]
]  # With interpreted values, and possibly units
any_raw_config_h = ini_config_h | typed_config_h


color_modes_h = Literal["rich", "html", None]


def NewRawConfig(
    *,
    ini_path: any_path_h | None = None,
    arguments: typed_config_h = None,
) -> ini_config_h:
    """"""
    if ini_path is None:
        ini_config = {}
    else:
        ini_config = cfpr.ConfigParser(
            delimiters=INI_VALUE_ASSIGNMENT,
            comment_prefixes=INI_COMMENT_MARKER,
            empty_lines_in_values=False,
            interpolation=None,
        )
        ini_config.optionxform = lambda option: option
        # Returns DEFAULT <Section: DEFAULT> if path does not exist or is a folder.
        ini_config.read(ini_path, encoding=sstm.getfilesystemencoding())

    output = {
        section: {parameter: value for parameter, value in parameters.items()}
        for section, parameters in ini_config.items()
        if section != cfpr.DEFAULTSECT
    }
    if arguments is not None:
        for sct_name, parameters in arguments.items():
            if sct_name not in output:
                output[sct_name] = {}
            for prm_name, value in parameters.items():
                output[sct_name][prm_name] = value

    return output


def AsStr(
    config: any_raw_config_h,
    /,
    *,
    color: color_modes_h = None,
    section_color: str = None,
    parameter_color: str = None,
) -> str:
    """"""
    output = []

    if section_color is None:
        section_color = SECTION_COLOR
    if parameter_color is None:
        parameter_color = PARAMETER_COLOR

    if color is None:
        section_color = ""
        parameter_color = ""
        color_reset = ""
        newline = "\n"
        indentation = " "
        bracket_escape = ""
    elif color == "rich":
        section_color = f"[{section_color}]"
        parameter_color = f"[{parameter_color}]"
        color_reset = "[/]"
        newline = "\n"
        indentation = " "
        bracket_escape = "\\"
    elif color == "html":
        section_color = f'<span style="color:{section_color}">'
        parameter_color = f'<span style="color:{parameter_color}">'
        color_reset = "</span>"
        newline = "<br/>"
        indentation = "&nbsp;"
        bracket_escape = ""
    else:
        raise ValueError(
            f"{color}: Invalid color mode; Expected=one of {get_args(color_modes_h)}."
        )

    longest = 0
    for section, parameters in config.items():
        if parameters.__len__() == 0:
            continue

        inner_output = []
        lengths = []
        for name, value in parameters.items():
            length = name.__len__()
            lengths.append(length)
            longest = max(longest, length)

            flattened = Flattened(str(value))
            inner_output.append(f"{parameter_color}{name}{color_reset}@= {flattened}")

        output.append(
            (
                f"{section_color}{bracket_escape}[{section}]{color_reset}",
                inner_output,
                lengths,
            )
        )

    output = (
        f"{_sct}{newline}"
        + newline.join(
            _lne.replace("@", (longest - _lgt + 1) * indentation, 1)
            for _lne, _lgt in zip(_prm, _lgs)
        )
        for _sct, _prm, _lgs in output
    )

    return f"{newline}{newline}".join(output)
