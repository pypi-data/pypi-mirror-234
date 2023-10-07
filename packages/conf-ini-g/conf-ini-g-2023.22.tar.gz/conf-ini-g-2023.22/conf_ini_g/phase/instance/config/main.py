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

from __future__ import annotations

import dataclasses as dtcl
import textwrap as text
from typing import Any, Sequence

from rich.text import Text as text_t
from str_to_obj.interface.console import TypeAsRichStr

from conf_ini_g.extension.path import any_path_h, path_t
from conf_ini_g.extension.string import AlignedOnSeparator
from conf_ini_g.interface.constant import (
    INI_COMMENT_MARKER,
    INI_UNIT_SECTION,
    STD_UNIT_CONVERSIONS,
)
from conf_ini_g.phase.instance.parameter.main import instance_t
from conf_ini_g.phase.instance.parameter.unit import unit_instance_t
from conf_ini_g.phase.raw.config import ini_config_h, typed_config_h
from conf_ini_g.phase.specification.config.main import config_t as specification_t
from conf_ini_g.phase.specification.parameter.unit import unit_t
from conf_ini_g.phase.specification.parameter.value import MISSING_REQUIRED_VALUE
from conf_ini_g.phase.specification.section.main import controller_t
from conf_ini_g.phase.specification.section.unit import IsUnitSection


@dtcl.dataclass(slots=True, repr=False, eq=False)
class config_t(dict[str, dict[str, instance_t | unit_instance_t]]):
    specification: specification_t
    ini_path: path_t | None = None

    @classmethod
    def NewFromRawConfig(
        cls,
        ini_config: ini_config_h,
        specification: specification_t,
        /,
        *,
        path: any_path_h = None,
    ) -> tuple[config_t, list[str], Sequence[tuple[str, str]]]:
        """"""
        config = cls(specification=specification)

        if path is not None:
            config.ini_path = path_t(path)

        issues, for_deferred_check = config._InstantiateFromINIConfig(ini_config)
        config._ManageDefaults()

        return config, issues, for_deferred_check

    def _InstantiateFromINIConfig(
        self, ini_config: ini_config_h, /
    ) -> tuple[list[str], Sequence[tuple[str, str]]]:
        """"""
        issues = []
        for_deferred_check = []

        for section_name, parameters in ini_config.items():
            if section_name not in self:
                self[section_name] = {}

            is_specified = section_name in self.specification
            if (not is_specified) and IsUnitSection(section_name):
                self.specification.AddUnitSection()
                is_specified = True

            if is_specified:
                section_spec = self.specification[section_name]
                for name, value in parameters.items():
                    if name in section_spec:
                        parameter_spec = section_spec[name]
                    elif section_spec.is_growable:
                        if (controller := section_spec.controller) is None:
                            controlling_value = None
                        else:
                            controlling_value = self.GetValueOfController(controller)
                        parameter_spec = self.specification.AddINIParameter(
                            section_spec,
                            name,
                            value,
                            controlling_value=controlling_value,
                        )
                        for_deferred_check.append((section_name, name))
                    else:
                        parameter_spec = None
                        issues.append(
                            f"{section_name}.{name}: Attempt to add an unspecified "
                            f"parameter to a section accepting none."
                        )
                    if parameter_spec is not None:
                        if isinstance(parameter_spec, unit_t):
                            instance = unit_instance_t()
                        else:
                            instance = instance_t()
                        instance.SetINIorInterfaceOrDefaultValue(
                            value, INI_COMMENT_MARKER
                        )
                        self[section_name][name] = instance
            elif IsUnitSection(section_name, possibly_fuzzy=True):
                issues.append(
                    f"{section_name}: Unit section must respect the following case "
                    f'"{INI_UNIT_SECTION}".'
                )
            else:
                issues.append(
                    f"{section_name}: Invalid section; "
                    f"Expected={self.specification.section_names}."
                )

        return issues, for_deferred_check

    def _ManageDefaults(self) -> None:
        """"""
        for section_spec in self.specification:
            # Leave here, otherwise parameter_spec.name not in self[section_spec.name]
            # below might fail.
            if section_spec.name not in self:
                self[section_spec.name] = {}

            for parameter_spec in section_spec.all_parameters:
                if parameter_spec.name not in self[section_spec.name]:
                    if parameter_spec.optional:
                        instance = instance_t(value=parameter_spec.default)
                        self[section_spec.name][parameter_spec.name] = instance
                    else:
                        self[section_spec.name][
                            parameter_spec.name
                        ] = MISSING_REQUIRED_VALUE

    def GetValueOfController(self, controller: controller_t, /) -> Any:
        """"""
        return self[controller.section][controller.parameter].value

    def AsTypedConfig(self) -> tuple[typed_config_h, list[str]]:
        """
        Units are interpreted
        """
        typed_config = {}
        issues = []

        unit_conversions = dict(STD_UNIT_CONVERSIONS)
        if INI_UNIT_SECTION in self.specification:
            for unit_spec in self.specification[INI_UNIT_SECTION]:
                unit_name = unit_spec.name
                expected_type = unit_spec.type
                instance = self[INI_UNIT_SECTION][unit_name]
                if instance is MISSING_REQUIRED_VALUE:
                    issues.append(
                        f"{INI_UNIT_SECTION}.{unit_name}: Missing required unit."
                    )
                else:
                    value, current_issues = instance.TypedValue(expected_type)
                    if current_issues.__len__() > 0:
                        issues.extend(
                            f"/{INI_UNIT_SECTION}.{unit_name}/ {_iss}"
                            for _iss in current_issues
                        )
                    else:
                        unit_conversions[unit_name] = value

        for section_spec in self.specification:
            raw_section = {}

            # Note: Method interface.window.config.config_t.SectionActiveParameterSpec
            # is defined using a similar piece of code.
            if (controller := section_spec.controller) is None:
                parameters = section_spec
            else:
                controller_value = self.GetValueOfController(controller)
                parameters = section_spec.ActiveParameters(controller_value)
            for parameter_spec in parameters:
                instance = self[section_spec.name][parameter_spec.name]
                if instance is MISSING_REQUIRED_VALUE:
                    value = None
                    current_issues = ["Missing required parameter."]
                else:
                    value, current_issues = instance.TypedValue(
                        parameter_spec.type, units=unit_conversions
                    )

                if current_issues.__len__() > 0:
                    issues.extend(
                        f"/{section_spec.name}.{parameter_spec.name}/ {_iss}"
                        for _iss in current_issues
                    )
                else:
                    raw_section[parameter_spec.name] = value

            typed_config[section_spec.name] = raw_section

        return typed_config, issues

    def AsINIConfig(self) -> ini_config_h:
        """"""
        output = {}

        for section_name, section in self.items():
            section_spec = self.specification[section_name]
            if (controller := section_spec.controller) is None:
                raw_section = {_p_nme: _prm.Text() for _p_nme, _prm in section.items()}
            else:
                controller_value = self.GetValueOfController(controller)
                raw_section = {
                    _p_spec.name: section[_p_spec.name].Text()
                    for _p_spec in section_spec.ActiveParameters(controller_value)
                }

            output[section_name] = raw_section

        return output

    def Issues(self) -> list[str]:
        """"""
        output = self.specification.Issues()

        valid_units = list(STD_UNIT_CONVERSIONS.keys())
        if INI_UNIT_SECTION in self.specification:
            valid_units.extend(
                _unt.name for _unt in self.specification[INI_UNIT_SECTION]
            )

        for section in self.specification:
            section_name = section.name

            issues = []
            for parameter in section:
                if (instance := self[section.name].get(parameter.name)) is not None:
                    issues.extend(
                        f"/{section.name}.{parameter.name}/ {_iss}"
                        for _iss in instance.Issues()
                    )
                    # Unit validation cannot be done at the parameter level since the
                    # unit section is needed.
                    if ((unit := getattr(instance, "unit", None)) is not None) and (
                        unit not in valid_units
                    ):
                        issues.append(
                            f"{unit}: Invalid unit of parameter "
                            f"{section_name}.{parameter.name}"
                        )

            output.extend(issues)

        return output

    def __str__(self) -> str:
        """"""
        return text_t.from_markup(self.__rich__()).plain

    def __rich__(self) -> str:
        """"""
        output = [
            "[grey50]--- Specification[/]",
            TypeAsRichStr(self),
            f"    [blue]ini_path[/]={self.ini_path}"
            f"[yellow]:{type(self.ini_path).__name__}[/]",
            text.indent(self.specification.__rich__(), "    "),
            "[grey50]--- Instance[/]",
        ]

        for section_name, section in self.items():
            output.append(f"{section_name}:")
            for parameter_name, parameter in section.items():
                output.append(f"    {parameter_name}@:@{parameter.__rich__()}")

        output = AlignedOnSeparator(output, "@:@", ": ")

        return "\n".join(output)
