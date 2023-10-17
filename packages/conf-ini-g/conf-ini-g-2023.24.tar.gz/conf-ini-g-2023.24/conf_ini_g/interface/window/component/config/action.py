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

from typing import Callable, Sequence

from babelwidget.main import backend_t, button_wgt_h, grid_lyt_h

from conf_ini_g.phase.raw.config import typed_config_h


def ActionButtonsLayout(
    action: tuple[str, Callable[[typed_config_h], None]] | None,
    has_ini_document: bool,
    backend: backend_t,
    ShowInINIFormat: Callable,
    SaveConfig: Callable,
    LaunchAction: Callable,
    Close: Callable,
    /,
) -> tuple[grid_lyt_h, button_wgt_h, Sequence[button_wgt_h]]:
    """"""
    layout = backend.grid_lyt_t()

    buttons = []
    geometries = []

    button = backend.button_wgt_t("Show in INI format")
    button.SetFunction(ShowInINIFormat)
    buttons.append(button)
    geometries.append((0, 0, 1, 2))

    button = backend.button_wgt_t("Save Config As")
    button.SetFunction(lambda: SaveConfig(True))
    buttons.append(button)
    if has_ini_document:
        geometries.append((1, 0, 1, 1))

        button = backend.button_wgt_t("Save/Overwrite Config")
        button.SetFunction(lambda: SaveConfig(False))
        buttons.append(button)
        geometries.append((1, 1, 1, 1))
    else:
        geometries.append((1, 0, 1, 2))

    if action is None:
        label = "CLOSE"
        Function = Close
    else:
        label = action[0]
        Function = LaunchAction

    button = backend.button_wgt_t(label)
    button.SetFunction(Function)
    buttons.append(button)
    geometries.append((2, 0, 1, 2))

    action_button = button

    for button, geometry in zip(buttons, geometries):
        layout.addWidget(button, *geometry)
    layout.setContentsMargins(0, 0, 0, 0)

    return layout, action_button, buttons
