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

from pathlib import Path as path_t
from types import NoneType, UnionType

from babelwidget.main import library_wgt_h
from str_to_obj import annotation_t
from str_to_obj.type.hint_tree import hint_tree_t

from conf_ini_g.catalog.interface.window.parameter.boolean import boolean_wgt_t
from conf_ini_g.catalog.interface.window.parameter.choices import choices_wgt_t
from conf_ini_g.catalog.interface.window.parameter.none import none_wgt_t
from conf_ini_g.catalog.interface.window.parameter.path import path_wgt_t
from conf_ini_g.catalog.interface.window.parameter.sequence import sequence_wgt_t
from conf_ini_g.catalog.interface.window.parameter.text import default_entry_wgt_t
from conf_ini_g.catalog.specification.parameter.choices import choices_t
from conf_ini_g.phase.specification.parameter.type import type_t

# Widgets can be mapped from types or annotations. Since annotations are more specific
# than types, they must be placed first to ensure they get a chance to be selected.
_TYPE_WIDGET_TRANSLATOR: dict[type, type[library_wgt_h]] = {
    # Annotations
    choices_t: choices_wgt_t,
    # Types
    NoneType: none_wgt_t,
    UnionType: choices_wgt_t,
    bool: boolean_wgt_t,
    float: default_entry_wgt_t,
    int: default_entry_wgt_t,
    list: sequence_wgt_t,
    path_t: path_wgt_t,
    set: sequence_wgt_t,
    str: default_entry_wgt_t,
    tuple: sequence_wgt_t,
}


def WidgetTypeForType(type_: type_t | hint_tree_t, /) -> type[library_wgt_h]:
    """"""
    base_hint = type_.type
    nnts = type_.all_annotations

    for registered_type, widget_type in _TYPE_WIDGET_TRANSLATOR.items():
        if (base_hint is registered_type) or any(
            issubclass(type(_nnt), registered_type) for _nnt in nnts
        ):
            return widget_type

    return default_entry_wgt_t


def RegisterNewTranslation(
    new_type: type | annotation_t, widget_type: type[library_wgt_h], /
) -> None:
    """"""
    if new_type in _TYPE_WIDGET_TRANSLATOR:
        # Raising an exception is adapted here since it is a developer-oriented function
        raise ValueError(
            f'{new_type.__name__}: Type already registered with "{_TYPE_WIDGET_TRANSLATOR[new_type]}" '
            f"in type-to-widget translations."
        )

    _TYPE_WIDGET_TRANSLATOR[new_type] = widget_type
