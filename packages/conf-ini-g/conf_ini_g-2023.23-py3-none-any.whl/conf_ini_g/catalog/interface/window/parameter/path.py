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
from pathlib import Path as pl_path_t
from typing import Callable

from babelwidget.main import backend_t, library_wgt_h, text_wgt_h
from babelwidget.path_chooser import (
    NewSelectedInputDocument,
    NewSelectedOutputDocument,
    document_selection_fct_h,
)

from conf_ini_g.catalog.specification.parameter.path import path_t
from conf_ini_g.interface.constant import PATH_SELECTOR_WIDTH
from conf_ini_g.interface.window.component.parameter.protocol import parameter_a
from conf_ini_g.phase.specification.parameter.main import parameter_t
from conf_ini_g.phase.specification.parameter.type import type_t


@dtcl.dataclass(repr=False, eq=False)
class path_wgt_t(parameter_a):
    """
    Cannot use slots (weak reference issue).
    """

    PostAssignmentFunction: Callable[[pl_path_t], None]
    library_wgt: library_wgt_h
    editable: bool
    backend: backend_t
    target_type: path_t.TARGET_TYPE = dtcl.field(init=False, default=None)
    path: text_wgt_h = dtcl.field(init=False, default=None)
    _NewSelectedDocument: document_selection_fct_h = dtcl.field(
        init=False, default=None
    )

    @classmethod
    def NewWithDetails(
        cls,
        value: pl_path_t | None,
        value_type: type_t | path_t | None,
        backend: backend_t,
        _: parameter_t | None,
        /,
        *,
        editable: bool = True,
        PostAssignmentFunction: Callable[[pl_path_t], None] = None,
    ) -> path_wgt_t:
        """
        If value_type does not contain the necessary details, the target type is set to any and considered as input, and
        the selection button label ends with an exclamation point.
        """
        output = cls(
            PostAssignmentFunction=PostAssignmentFunction,
            library_wgt=backend.library_wgt_t(),
            editable=editable,
            backend=backend,
        )

        value = _ValidStrValue(value, editable)

        default_parameters = (path_t.TARGET_TYPE.any, True, True)
        if value_type is None:
            target_type, is_input, misses_details = default_parameters
        else:
            if isinstance(value_type, type_t):
                annotation = value_type.FirstAnnotationWithAttribute(
                    ("target_type", "is_input")
                )
            else:
                annotation = value_type
            if annotation is None:
                target_type, is_input, misses_details = default_parameters
            else:
                target_type = annotation.target_type
                is_input = annotation.is_input
                misses_details = False

        output.target_type = target_type
        if is_input:
            output._NewSelectedDocument = NewSelectedInputDocument
        else:
            output._NewSelectedDocument = NewSelectedOutputDocument

        if target_type is path_t.TARGET_TYPE.document:
            selector_label = "🗋"
        elif target_type is path_t.TARGET_TYPE.folder:
            selector_label = "📂"
        else:
            selector_label = "📂🗋"
        if misses_details:
            selector_label += " !"
        if is_input:
            selector_color = "green"
        else:
            selector_color = "red"
        if editable:
            path = backend.text_wgt_t(value, parent=output.library_wgt)
        else:
            path = backend.label_wgt_t(value, parent=output.library_wgt)
        path_selector = backend.button_wgt_t(selector_label, parent=output.library_wgt)
        path_selector.SetFunction(output.SelectDocument)

        output.path = path

        path_selector.setStyleSheet(f"color: {selector_color};")
        path_selector.setFixedWidth(PATH_SELECTOR_WIDTH)

        layout = backend.hbox_lyt_t()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(path)
        layout.addWidget(path_selector)
        output.library_wgt.setLayout(layout)

        return output

    def Assign(self, value: pl_path_t | None, _: type_t | path_t | None, /) -> None:
        """"""
        value = _ValidStrValue(value, self.editable)
        self.path.setText(value)

    def Text(self) -> str:
        """"""
        return self.path.Text()

    def SelectDocument(self) -> None:
        """"""
        current_path = self.Text()
        current_doc = pl_path_t(current_path).resolve()

        if self.target_type is path_t.TARGET_TYPE.document:
            title = "Select File"
        elif self.target_type is path_t.TARGET_TYPE.folder:
            title = "Select Folder"
        else:
            title = "Select File or Folder"

        selection = self._NewSelectedDocument(
            title,
            title,
            self.backend,
            mode=self.target_type.name,
            start_folder=current_doc.parent,
            initial_selection=current_doc,
        )
        if selection is None:
            return

        self.Assign(selection, None)
        # Put post-assignment call here instead of in the Assign method in case Assign
        # is also called at initialization time, in NewWithDetails, one day. Indeed, the
        # post-assignment task should have been done already, or will be done, when
        # instantiating the interface.
        if self.PostAssignmentFunction is not None:
            self.PostAssignmentFunction(selection)


def _ValidStrValue(value: pl_path_t | None, editable: bool, /) -> str:
    """"""
    if value is None:
        output = ""
    else:
        if not editable:
            value = value.relative_to(pl_path_t.home())
        output = str(value)

    return output
