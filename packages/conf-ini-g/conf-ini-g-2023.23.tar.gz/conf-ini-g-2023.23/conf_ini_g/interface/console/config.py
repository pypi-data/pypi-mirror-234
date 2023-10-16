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

import re as rgex
from argparse import ArgumentParser as argument_parser_t
from pathlib import Path as path_t
from typing import Any, Iterator, Sequence

from conf_ini_g.extension.string import Flattened
from conf_ini_g.phase.raw.config import typed_config_h
from conf_ini_g.phase.specification.config.main import config_t
from conf_ini_g.phase.specification.parameter.value import MISSING_REQUIRED_VALUE

parsed_arguments_h = dict[str, str]


# Specified INI document file is stored in _INI_DOCUMENT_VARIABLE
_INI_DOCUMENT_VARIABLE = "ini_path"

_ADVANCED_MODE_OPTION = "advanced-mode"
_ADVANCED_MODE_VARIABLE = "advanced_mode"

# Usage: {section_name}{_SECTION_PARAMETER_SEPARATOR}{parameter_name}
_SECTION_PARAMETER_SEPARATOR = "-"


def CommandLineParser(
    description: str | None, specification: config_t, /
) -> argument_parser_t:
    """"""
    output = argument_parser_t(description=description, allow_abbrev=False)
    # This argument is optional because all parameters can be explicitly passed as
    # arguments (CLI mode), or nothing can be passed at all (GUI mode).
    output.add_argument(
        dest=_INI_DOCUMENT_VARIABLE,
        help="Path to INI configuration file",
        default=None,
        nargs="?",
        metavar="INI_config_file",
    )

    options = []
    for section in specification:
        for parameter in section.all_parameters:
            option = f"{section.name}{_SECTION_PARAMETER_SEPARATOR}{parameter.name}"
            if option == _ADVANCED_MODE_OPTION:
                # Raising an exception is adapted here since execution has been launched from command line
                raise ValueError(
                    f"{option}: Command-line option for parameter is identical to advanced mode option. "
                    f"Please change parameter specification (section name and/or parameter name)."
                )
            if option in options:
                # This can happen in controlled sections whose alternatives share equally named parameters.
                continue

            attribute = f"{section.name}{_SECTION_PARAMETER_SEPARATOR}{parameter.name}"

            # Default is a missing_required_value_t instance to avoid overwriting if in
            # INI but not passed.
            default = MISSING_REQUIRED_VALUE

            if parameter.optional:
                if isinstance(parameter.default, str):
                    delimiter = '"'
                else:
                    delimiter = ""
                type_and_value = (
                    f"Type: {parameter.type}. "
                    f"Default: [green]{delimiter}{parameter.default}{delimiter}[/]"
                )
            else:
                type_and_value = str(default)
            flattened = Flattened(type_and_value)
            definition = f"{parameter.definition}. {flattened}"

            # Type could be TypeOfAnnotatedHint(cmd_line_type). However, to allow passing any of the allowed types,
            # deferring type validation to functional config instantiation, this parameter is not passed.
            output.add_argument(
                f"--{option}",
                dest=attribute,
                help=definition,
                default=default,
                metavar=attribute,
            )
            options.append(option)

    output.add_argument(
        f"--{_ADVANCED_MODE_OPTION}",
        dest=_ADVANCED_MODE_VARIABLE,
        help="Toggle display of advanced sections and parameters",
        action="store_true",
    )

    return output


def ParsedArguments(
    parser: argument_parser_t, /, *, arguments: Sequence[str] = None
) -> tuple[path_t | None, bool, typed_config_h]:
    """"""
    parsed, unknowns = parser.parse_known_args(args=arguments)
    parsed = vars(parsed)

    advanced_mode = parsed[_ADVANCED_MODE_VARIABLE]
    del parsed[_ADVANCED_MODE_VARIABLE]

    ini_path = parsed[_INI_DOCUMENT_VARIABLE]
    del parsed[_INI_DOCUMENT_VARIABLE]
    if ini_path is not None:
        try:
            ini_path = path_t(ini_path).resolve(strict=True)
        except (FileNotFoundError, RuntimeError):
            raise FileNotFoundError(f"Nonexistent or invalid path: {ini_path}")

    pattern = rgex.compile(
        r"--(\w+)" + _SECTION_PARAMETER_SEPARATOR + r"(\w+)=(.+)", flags=rgex.ASCII
    )
    for unknown in unknowns:
        match = pattern.fullmatch(unknown)
        if match is None:
            # Raising an exception is adapted here since execution has been launched from command line
            raise ValueError(
                f"{unknown}: Invalid option syntax; Expected=--SECTION-PARAMETER=VALUE"
            )

        section, parameter, value = match.groups()
        parsed[f"{section}{_SECTION_PARAMETER_SEPARATOR}{parameter}"] = value

    raw_config = {}
    for sct_name, prm_name, value in _SectionParameterValueIterator(parsed):
        if sct_name in raw_config:
            raw_config[sct_name][prm_name] = value
        else:
            raw_config[sct_name] = {prm_name: value}

    return ini_path, advanced_mode, raw_config


def _SectionParameterValueIterator(
    arguments: parsed_arguments_h,
) -> Iterator[tuple[str, str, Any]]:
    """"""
    for prm_uid, value in arguments.items():
        # See CommandLineParser for why this can happen.
        if value is MISSING_REQUIRED_VALUE:
            continue

        section, parameter = prm_uid.split(_SECTION_PARAMETER_SEPARATOR)
        yield section, parameter, value
