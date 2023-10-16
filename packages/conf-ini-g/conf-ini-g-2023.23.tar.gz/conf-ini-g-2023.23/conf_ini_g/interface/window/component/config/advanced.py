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

from typing import Annotated, Callable

from babelwidget.main import backend_t, hbox_lyt_h

from conf_ini_g.catalog.interface.window.parameter.boolean import boolean_wgt_t
from conf_ini_g.catalog.specification.parameter.boolean import boolean_t
from conf_ini_g.phase.specification.parameter.type import type_t


def AdvancedModeLayout(
    advanced_mode: bool, backend: backend_t, ToggleAdvancedMode: Callable, /
) -> tuple[hbox_lyt_h, boolean_wgt_t]:
    """"""
    layout = backend.hbox_lyt_t()

    annotated_type = Annotated[bool, boolean_t(mode=boolean_t.MODE.on_off)]
    value_type = type_t.NewFromTypeHint(annotated_type)
    boolean = boolean_wgt_t.NewWithDetails(
        advanced_mode,
        value_type,
        backend,
        None,
    )
    boolean.true_btn.SetFunction(ToggleAdvancedMode)

    layout.addWidget(backend.label_wgt_t("<i>Advanced Mode</i>"))
    layout.addWidget(boolean.library_wgt)

    return layout, boolean
