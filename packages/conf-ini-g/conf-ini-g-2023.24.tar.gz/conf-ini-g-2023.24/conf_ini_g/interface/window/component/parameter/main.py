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
from types import UnionType

from babelwidget.main import (
    backend_t,
    choices_list_wgt_h,
    label_wgt_h,
    library_wgt_h,
    text_wgt_h,
)
from str_to_obj.type.hint_tree import hint_tree_t

from conf_ini_g.catalog.interface.window.parameter.directory import WidgetTypeForType
from conf_ini_g.catalog.interface.window.parameter.multitype import multitype_wgt_t
from conf_ini_g.interface.constant import INI_UNIT_SEPARATOR
from conf_ini_g.interface.window.component.parameter.type import TypeSelector
from conf_ini_g.interface.window.generic import FormattedName
from conf_ini_g.phase.instance.parameter.main import instance_t
from conf_ini_g.phase.specification.parameter.main import (
    parameter_t as parameter_spec_t,
)


@dtcl.dataclass(slots=True, repr=False, eq=False)
class parameter_t:
    """
    In order to leave the section widget put the name, type, and input widgets of each parameter in columns,
    parameter_t is not a container widget. Instead, it just stores its component widgets for later addition to a layout.
    """

    name: label_wgt_h = dtcl.field(init=False, default=None)
    type: label_wgt_h | choices_list_wgt_h = dtcl.field(init=False, default=None)
    value: library_wgt_h = dtcl.field(init=False, default=None)
    unit: text_wgt_h = dtcl.field(init=False, default=None)
    comment: str = dtcl.field(init=False, default=None)

    @classmethod
    def NewForParameter(
        cls,
        parameter_spec: parameter_spec_t,
        instance: instance_t,
        backend: backend_t,
        /,
    ) -> parameter_t:
        """"""
        output = cls()

        formatted_name = FormattedName(parameter_spec.name, " ")
        comment = (
            f"{formatted_name}\n{parameter_spec.definition}.\n\n"
            f"{parameter_spec.description}."
        )
        if instance.comment is not None:
            comment += f"\n\n{instance.comment}."
        output.name = backend.label_wgt_t(formatted_name)
        output.name.setToolTip(comment)
        output.comment = comment

        type_ = parameter_spec.type
        value, issues = instance.TypedValue(type_)
        if issues.__len__() > 0:
            issues = "\n".join(issues)
            backend.ShowErrorMessage(
                f'Error(s) when creating the widget for "{parameter_spec.name}":\n'
                f"{issues}"
            )
            value = None
        if isinstance(type_, hint_tree_t) and (type_.type is UnionType):
            hint_options = type_.elements
            type_wgt = TypeSelector(hint_options, backend)
            value_wgt = multitype_wgt_t.NewForHints(
                value,
                hint_options,
                type_wgt,
                backend,
            )
        else:
            type_wgt = backend.label_wgt_t(type_.template_as_str)
            widget_type = WidgetTypeForType(type_)
            value_wgt = widget_type.NewWithDetails(
                value,
                type_,
                backend,
                parameter_spec,
            )
        output.type = type_wgt
        output.value = value_wgt

        if (unit := getattr(instance, "unit", None)) is not None:
            output.unit = backend.text_wgt_t(unit)

        name_style = "padding-right: 5px;"
        if parameter_spec.optional:
            name_style += "color: gray;"
        output.name.setStyleSheet(name_style)
        output.type.setStyleSheet(name_style)

        return output

    def SetVisible(self, visible: bool, /) -> None:
        """"""
        self.name.setVisible(visible)
        self.type.setVisible(visible)
        self.value.library_wgt.setVisible(visible)
        if self.unit is not None:
            self.unit.setVisible(visible)

    def Text(self) -> str:
        """"""
        text = self.value.Text()

        if self.unit is None:
            return text

        return f"{text}{INI_UNIT_SEPARATOR}{self.unit.Text()}"
