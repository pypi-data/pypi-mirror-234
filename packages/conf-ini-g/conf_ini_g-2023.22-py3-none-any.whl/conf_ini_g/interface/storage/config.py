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

import sys as sstm
from argparse import ArgumentParser as argument_parser_t

from str_to_obj import ObjectFromStr

from conf_ini_g.extension.path import (
    ValidateInputPath,
    ValidateOutputPath,
    any_path_h,
    path_t,
)
from conf_ini_g.phase.raw.config import AsStr, NewRawConfig, any_raw_config_h
from conf_ini_g.phase.specification.parameter.main import parameter_t
from conf_ini_g.phase.specification.section.main import section_t
from conf_ini_g.phase.specification.section.unit import IsUnitSection

_SECTIONS = "SECTIONS"


def DraftSpecificationFromINIDocument(path: any_path_h, /) -> str | None:
    """"""
    ini_config = NewRawConfig(ini_path=path)
    if ini_config is None:
        return None

    sections = []
    for section_name, parameters in ini_config.items():
        # possibly_fuzzy=True: in case the raw config is not valid in that respect
        if IsUnitSection(section_name, possibly_fuzzy=True):
            continue

        parameters_as_lst = []
        for parameter_name, value_as_str in parameters.items():
            value, _ = ObjectFromStr(value_as_str)
            parameter = (
                f"{parameter_t.__name__}(\n"
                f'                name="{parameter_name}",\n'
                f"                type={type(value).__name__},\n"
                f"            )"
            )
            parameters_as_lst.append(parameter)

        parameters_as_str = ",\n            ".join(parameters_as_lst)
        section = (
            f"    {section_t.__name__}(\n"
            f'        name="{section_name}",\n'
            f"        parameters=[\n"
            f"            {parameters_as_str}\n"
            f"        ]\n"
            f"    )"
        )
        sections.append(section)

    imports = (
        f"# To use this specification file:\n"
        f"#     1. import the object {_SECTIONS}\n"
        f"#     2. instantiate a conf_ini_g.specification.config.config_t from it\n"
        f"from conf_ini_g.specification.parameter.main "
        f"import {parameter_t.__name__}\n"
        f"from conf_ini_g.specification.section.main import {section_t.__name__}\n"
    )

    return imports + f"\n{_SECTIONS} = (\n" + ",\n".join(sections) + ",\n)\n"


def SaveRawConfigToINIDocument(
    config: any_raw_config_h,
    path: any_path_h,
    /,
    *,
    should_overwrite: bool = False,
    should_raise_on_error: bool = False,
) -> list[str]:
    """"""
    path = path_t(path)
    issues = ValidateOutputPath(
        path,
        should_overwrite=should_overwrite,
        should_raise_on_error=should_raise_on_error,
    )
    if issues.__len__() > 0:
        return issues

    encoding = sstm.getfilesystemencoding()

    with path.open("w", encoding=encoding) as ini_writer:
        print(AsStr(config), file=ini_writer)
        print(f"", file=ini_writer)

    return []


if __name__ == "__main__":
    """
    Run with: python -m conf_ini_g.interface.storage.config
    from package base folder.
    """
    main_encoding = sstm.getfilesystemencoding()

    parser = argument_parser_t(
        prog="python -m conf_ini_g.interface.storage.config",
        description="Display or save a draft config specification "
        "based on an INI file.",
        allow_abbrev=False,
    )
    # type=argparse.FileType() => automatic file opening
    parser.add_argument(
        dest="ini_path",
        help="Input: Path to INI configuration file",
        metavar="INI_config_file",
    )
    # type=argparse.FileType('w', encoding=main_encoding) => automatic creation of file
    parser.add_argument(
        dest="draft_specification",
        help="Output: Path to draft config specification file. "
        "If not passed, specification is displayed in console.",
        default=None,
        nargs="?",
        metavar="draft_spec_file",
    )
    parser.add_argument(
        "--overwrite",
        dest="should_overwrite",
        action="store_true",
        help="Allows overwriting of draft config specification file.",
    )

    arguments = parser.parse_args()
    ini_path = path_t(arguments.ini_path)
    draft_path = arguments.draft_specification
    main_should_overwrite = arguments.should_overwrite

    issues_ = ValidateInputPath(ini_path)
    if issues_.__len__() > 0:
        print("\n".join(issues_) + "\n")
        parser.print_help()
        sstm.exit(-1)

    if draft_path is not None:
        draft_path = path_t(draft_path)
        issues_ = ValidateOutputPath(draft_path, should_overwrite=main_should_overwrite)
        if issues_.__len__() > 0:
            print("\n".join(issues_) + "\n")
            parser.print_help()
            sstm.exit(-1)

    draft = DraftSpecificationFromINIDocument(ini_path)
    if draft is None:
        print(f"{ini_path}: Not a valid INI document")
        sstm.exit(-1)

    if draft_path is None:
        print(draft)
    else:
        with draft_path.open("w", encoding=main_encoding) as draft_writer:
            draft_writer.write(draft)
