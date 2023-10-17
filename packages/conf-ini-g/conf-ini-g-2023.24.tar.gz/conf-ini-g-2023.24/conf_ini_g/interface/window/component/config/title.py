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

from typing import Callable, Sequence

from babelwidget.main import backend_t, button_wgt_h, menu_wgt_h, vbox_lyt_h

from conf_ini_g.catalog.interface.window.parameter.path import path_wgt_t
from conf_ini_g.catalog.specification.parameter.path import path_t as path_annotation_t
from conf_ini_g.phase.instance.config.main import config_t as config_instance_t


def TitleLayout(
    title: str | None,
    instance: config_instance_t,
    history: Sequence[str] | None,
    backend: backend_t,
    UpdateWithNewINI: Callable,
    Close: Callable,
    /,
) -> tuple[vbox_lyt_h, path_wgt_t, button_wgt_h, menu_wgt_h, button_wgt_h]:
    """"""
    if title is None:
        title = "Conf-INI-g"

    layout = backend.hbox_lyt_t()
    inner_layout = backend.vbox_lyt_t()

    title = (
        f'<h1 style="color: blue">{title}</h1>'
        f"<b><font face=monospace>SPEC:</font></b> {instance.specification.spec_path}"
    )
    title_wgt = backend.label_wgt_t(title)
    title_wgt.setAlignment(backend.ALIGNED_LEFT)

    label_wgt = backend.label_wgt_t("<b><font face=monospace>INI: </font></b>")
    ini_path_wgt = path_wgt_t.NewWithDetails(
        instance.ini_path,
        path_annotation_t(
            target_type=path_annotation_t.TARGET_TYPE.document, is_input=True
        ),
        backend,
        None,
        editable=False,
        PostAssignmentFunction=UpdateWithNewINI,
    )
    history_button = backend.button_wgt_t("🕑")
    history_menu = backend.menu_wgt_t.NewWithFunction(UpdateWithNewINI)
    if history is None:
        history_button.setEnabled(False)
    else:
        for choice in history:
            history_menu.addAction(choice)
    history_button.setMenu(history_menu)
    #
    label_wgt.setSizePolicy(backend.SIZE_FIXED, backend.SIZE_FIXED)
    history_button.setSizePolicy(backend.SIZE_FIXED, backend.SIZE_MINIMUM)
    #
    path_layout = backend.hbox_lyt_t()
    path_layout.addWidget(label_wgt)
    path_layout.addWidget(ini_path_wgt.library_wgt)
    path_layout.addWidget(history_button)

    inner_layout.addWidget(title_wgt)
    inner_layout.addLayout(path_layout)

    close_button = backend.button_wgt_t("CLOSE")
    close_button.SetFunction(Close)
    close_button.setSizePolicy(backend.SIZE_FIXED, backend.SIZE_MINIMUM)

    layout.addLayout(inner_layout)
    layout.addWidget(close_button)

    return layout, ini_path_wgt, history_button, history_menu, close_button
