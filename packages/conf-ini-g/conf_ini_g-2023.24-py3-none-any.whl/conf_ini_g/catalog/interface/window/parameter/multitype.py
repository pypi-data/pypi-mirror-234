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
from typing import Any, Sequence

from babelwidget.main import backend_t, choices_list_wgt_h, library_wgt_h, stack_wgt_h
from str_to_obj.type.hint_tree import hint_tree_t

from conf_ini_g.catalog.interface.window.parameter.directory import WidgetTypeForType


@dtcl.dataclass(slots=True, repr=False, eq=False)
class multitype_wgt_t:
    hints: Sequence[hint_tree_t]
    library_wgt: stack_wgt_h
    controller_wgt: choices_list_wgt_h
    values: tuple[library_wgt_h] | None = dtcl.field(init=False, default=None)

    @classmethod
    def NewForHints(
        cls,
        value: Any,
        hints: Sequence[hint_tree_t],
        controller: choices_list_wgt_h,
        backend: backend_t,
        /,
    ) -> multitype_wgt_t:
        """"""
        value_stack = backend.stack_wgt_t()
        controller.SetFunction(value_stack.setCurrentIndex)

        output = cls(hints=hints, library_wgt=value_stack, controller_wgt=controller)

        values = []
        for t_idx, hint in enumerate(hints):
            if isinstance(value, hint.type):
                initial_value = value
            else:
                initial_value = None
            widget_type = WidgetTypeForType(hint)
            value_wgt = widget_type.NewWithDetails(
                initial_value,
                hint,
                backend,
                None,
            )
            values.append(value_wgt)
            value_stack.addWidget(value_wgt.library_wgt)
        output.values = tuple(values)

        value_stack.setSizePolicy(backend.SIZE_EXPANDING, backend.SIZE_FIXED)

        output.Assign(value, None)

        return output

    def Assign(self, value: Any, _: Any | None, /) -> None:
        """
        Second parameter: For coherence with single-type parameters.
        """
        initial_index = 0
        for t_idx, hint in enumerate(self.hints):
            if isinstance(value, hint.type):
                initial_index = t_idx
        self.controller_wgt.setCurrentIndex(initial_index)

    def Text(self) -> str:
        """"""
        return self.values[self.controller_wgt.currentIndex()].Text()
