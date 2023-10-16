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
import inspect as nspt
from pathlib import Path as pl_path_t
from typing import Any, Callable, Iterator, Sequence

from babelwidget.main import backend_t, library_wgt_h
from babelwidget.path_chooser import NewSelectedOutputDocument

from conf_ini_g import NewRawConfig
from conf_ini_g.interface.constant import INI_COMMENT_MARKER
from conf_ini_g.interface.storage.config import SaveRawConfigToINIDocument
from conf_ini_g.interface.window.component.config.action import ActionButtonsLayout
from conf_ini_g.interface.window.component.config.advanced import AdvancedModeLayout
from conf_ini_g.interface.window.component.config.title import TitleLayout
from conf_ini_g.interface.window.component.section.collection import (
    SectionsAndCategories,
    any_section_h,
)
from conf_ini_g.interface.window.component.section.main import controlled_section_t
from conf_ini_g.phase.instance.config.main import config_t as config_instance_t
from conf_ini_g.phase.raw.config import AsStr, ini_config_h, typed_config_h
from conf_ini_g.phase.specification.parameter.main import (
    parameter_t as parameter_spec_t,
)
from conf_ini_g.phase.specification.section.main import section_t as section_spec_t


@dtcl.dataclass(repr=False, eq=False)
class config_t:
    """
    The class cannot use slots because it disables weak referencing, which is required.
    See error message below when using slots:
    TypeError: cannot create weak reference to 'config_t' object
    [...]
    File "[...]conf_ini_g/catalog/interface/window/backend/pyqt5/widget/choices.py", line 41, in SetFunction
        self.clicked.connect(function)
        │                    └ <bound method config_t.ToggleAdvancedMode of <conf_ini_g.interface.window.config.config_t object at [...]>>
        └ <conf_ini_g.catalog.interface.window.backend.pyqt5.widget.choices.dot_button_wgt_t object at [...]>

    Widget might not cooperate well with list, in which case Python raises the
    following exception: TypeError: multiple bases have instance lay-out conflict
    To be safe, "sections" is a field instead of being part of the class definition.
    """

    instance: config_instance_t
    backend: backend_t
    library_wgt: library_wgt_h
    UpdateHistory: Callable[[pl_path_t | str], None] | None
    #
    Action: Callable[[typed_config_h], None] = None
    #
    sections: dict[str, any_section_h] = dtcl.field(init=False, default=None)
    # Both an access for interacting with widgets, and a reference keeper to prevent
    # autonomous widgets from loosing their "liveness".
    _widget: dict[str, library_wgt_h] = dtcl.field(init=False, default_factory=dict)

    @classmethod
    def NewFromConfig(
        cls,
        title: str | None,
        instance: config_instance_t,
        backend: backend_t,
        /,
        *,
        history: Sequence[str] | None = None,
        UpdateHistory: Callable[[pl_path_t | str], None] | None,
        advanced_mode: bool = False,
        action: tuple[str, Callable[[typed_config_h], None]] = None,
    ) -> config_t:
        """"""
        if instance.ini_path is not None:
            if UpdateHistory is not None:
                UpdateHistory(instance.ini_path)
            as_str = str(instance.ini_path)
            if history is None:
                history = (as_str,)
            elif as_str not in history:
                history = list(history)
                history.append(as_str)

        if action is None:
            kwargs = {}
        else:
            kwargs = {"Action": action[1]}

        output = cls(
            instance=instance,
            backend=backend,
            library_wgt=backend.library_wgt_t(),
            UpdateHistory=UpdateHistory,
            **kwargs,
        )

        # --- Top-level widgets
        (
            title_lyt,
            ini_path_wgt,
            history_button,
            history_menu,
            close_button,
        ) = TitleLayout(
            title,
            instance,
            history,
            backend,
            output.UpdateWithNewINI,
            output.library_wgt.close,
        )
        advanced_mode_lyt, adv_mode_wgt = AdvancedModeLayout(
            advanced_mode, backend, output.ToggleAdvancedMode
        )
        button_lyt, action_button, action_wgts = ActionButtonsLayout(
            action,
            instance.ini_path is not None,
            backend,
            output.ShowInINIFormat,
            output.SaveConfig,
            output.LaunchAction,
            output.library_wgt.close,
        )
        output._widget["ini_path"] = ini_path_wgt
        output._widget["history_button"] = history_button
        output._widget["history_menu"] = history_menu
        output._widget["adv_mode"] = adv_mode_wgt
        output._widget["action"] = action_button
        output._widget["action_buttons"] = action_wgts
        output._widget["close"] = close_button

        # --- Sections
        output.sections, controlled_sections, category_selector = SectionsAndCategories(
            instance, None, backend
        )
        output._AssociateSectionsAndControllers(controlled_sections)
        output._widget["category_selector"] = category_selector

        # --- Layout...
        layout = backend.grid_lyt_t()
        if title_lyt is None:
            first_available_row = 0
        else:
            layout.addLayout(title_lyt, 0, 0, 1, 1)
            first_available_row = 1
        layout.addWidget(category_selector, first_available_row, 0, 1, 1)
        layout.addLayout(advanced_mode_lyt, first_available_row + 1, 0, 1, 1)
        layout.addLayout(button_lyt, first_available_row + 2, 0, 1, 1)

        output.library_wgt.setLayout(layout)
        # --- ...Layout

        output.ToggleAdvancedMode(advanced_mode)

        return output

    def _AssociateSectionsAndControllers(
        self,
        controlled_sections: Sequence[tuple[controlled_section_t, section_spec_t]],
        /,
    ) -> None:
        """"""
        for section, section_spec in controlled_sections:
            controller = section_spec.controller
            parameter = self[controller.section].parameters[controller.parameter]
            value_wgt = parameter.value
            if hasattr(value_wgt, "SetFunction"):
                value_wgt.SetFunction(section.page_stack.setCurrentIndex)
            else:
                self.backend.ShowErrorMessage(
                    f"{controller.section}.{controller.parameter}: "
                    f'Controller has no "SetFunction" method; Disabling control.'
                )

    def ToggleAdvancedMode(self, advanced_mode: bool, /) -> None:
        """"""
        for section_name, section in self.sections.items():
            section_spec = self.instance.specification[section_name]
            if section_spec.basic:
                should_check_parameters = True
            elif advanced_mode:
                section.library_wgt.setVisible(True)
                should_check_parameters = True
            else:
                section.library_wgt.setVisible(False)
                should_check_parameters = False

            if should_check_parameters:
                parameters = section.active_parameters.values()
                parameter_specs = self.SectionActiveParameterSpec(section_spec)
                for parameter, parameter_spec in zip(parameters, parameter_specs):
                    if not parameter_spec.basic:
                        if advanced_mode:
                            parameter.SetVisible(True)
                        else:
                            parameter.SetVisible(False)

    def ReassignCloseButtonTarget(self) -> None:
        """"""
        current = self.library_wgt
        while current is not None:
            main_window = current
            current = current.parent()

        self._widget["close"].SetFunction(main_window.close)

    def UpdateWithNewINI(self, ini_path: pl_path_t | str, /) -> None:
        """"""
        if isinstance(ini_path, str):
            ini_path = pl_path_t(ini_path)

        raw_config = NewRawConfig(ini_path=ini_path)
        config, issues, _ = config_instance_t.NewFromRawConfig(
            raw_config, self.instance.specification, path=ini_path
        )
        if issues.__len__() > 0:
            self.backend.ShowErrorMessage("\n".join(issues), parent=self.library_wgt)
            return

        category_selector = self._widget["category_selector"]
        if isinstance(category_selector, self.backend.tabs_wgt_t):
            # Note: idx^th layout: category_selector.widget(t_idx).widget().layout().
            while category_selector.count() > 0:
                category_selector.removeTab(0)
        else:
            layout = category_selector.widget().layout()
            while layout.count() > 0:
                layout.itemAt(0).widget().setParent(None)

        self.instance = config
        self.sections, controlled_sections, _ = SectionsAndCategories(
            self.instance, category_selector, self.backend
        )
        self._AssociateSectionsAndControllers(controlled_sections)
        self.ToggleAdvancedMode(self._widget["adv_mode"].true_btn.isChecked())

        self._widget["ini_path"].Assign(ini_path, None)
        self._widget["history_button"].setEnabled(True)
        if str(ini_path) not in (
            _elm.text() for _elm in self._widget["history_menu"].actions()
        ):
            self._widget["history_menu"].addAction(str(ini_path))

        if self.UpdateHistory is not None:
            self.UpdateHistory(ini_path)

    def SectionActiveParameterSpec(
        self, section_spec: section_spec_t, /
    ) -> Sequence[parameter_spec_t]:
        """"""
        if (controller := section_spec.controller) is None:
            output = section_spec
        else:
            controller = self[controller.section].parameters[controller.parameter]
            output = section_spec.ActiveParameters(controller.Text())

        return output

    def SynchronizeInstance(self) -> list[str]:
        """"""
        for section_name, section in self.sections.items():
            section_spec = self.instance.specification[section_name]
            parameters = section.active_parameters.values()
            parameter_specs = self.SectionActiveParameterSpec(section_spec)
            for parameter, parameter_spec in zip(parameters, parameter_specs):
                if parameter.unit is None:
                    unit_kwarg = {}
                else:
                    unit_kwarg = {"unit": parameter.unit.Text()}
                instance = self.instance[section_spec.name][parameter_spec.name]
                instance.SetINIorInterfaceOrDefaultValue(
                    parameter.Text(),
                    INI_COMMENT_MARKER,
                    **unit_kwarg,
                )

        return self.instance.Issues()

    def LaunchAction(self) -> None:
        """"""
        issues = self.SynchronizeInstance()
        if issues.__len__() > 0:
            self.backend.ShowErrorMessage("\n".join(issues), parent=self.library_wgt)
        else:
            typed_config, issues = self.instance.AsTypedConfig()
            if issues.__len__() > 0:
                self.backend.ShowErrorMessage(
                    "\n".join(issues), parent=self.library_wgt
                )
            else:
                self._widget["action"].setEnabled(False)
                self.backend.qt_core_app_t.processEvents()
                try:
                    self.Action(typed_config)
                except Exception as exception:
                    trace = nspt.trace()[-1]
                    context = "\n".join(trace.code_context)
                    self.backend.ShowErrorMessage(
                        f"{trace.filename}@{trace.lineno}:{trace.function}\n"
                        f"{context}\n"
                        f"{exception}",
                        parent=self.library_wgt,
                    )
                self._widget["action"].setEnabled(True)

    def AsINIConfig(self) -> ini_config_h | None:
        """"""
        issues = self.SynchronizeInstance()
        if issues.__len__() > 0:
            output = None
            self.backend.ShowErrorMessage("\n".join(issues), parent=self)
        else:
            output = self.instance.AsINIConfig()

        return output

    def ShowInINIFormat(self) -> None:
        """"""
        config = self.AsINIConfig()
        if config is None:
            return

        config = AsStr(config, color="html")
        self.backend.ShowMessage("INI Config", "<tt>" + config + "<tt/>")

    def SaveConfig(self, new_ini: bool, /) -> None:
        """"""
        if new_ini:
            path = NewSelectedOutputDocument(
                "Save Config As",
                "Save Config As",
                self.backend,
                mode="document",
                valid_types={"Config files": ("ini", "INI")},
            )
        else:
            path = self.instance.ini_path  # Will overwrite current INI document

        if path is not None:
            config = self.AsINIConfig()
            issues = SaveRawConfigToINIDocument(config, path)
            if issues.__len__() > 0:
                self.backend.ShowErrorMessage("\n".join(issues), parent=self)
            else:
                self.instance.ini_path = path

    def __getattr__(self, attribute: str, /) -> Any:
        """
        E.g., used for "show".
        """
        try:
            output = super().__getattr__(attribute)
        except AttributeError:
            output = getattr(self.library_wgt, attribute)

        return output

    def __contains__(self, key: str, /) -> bool:
        """"""
        return key in self.sections

    def __getitem__(self, key: str, /) -> any_section_h:
        """"""
        return self.sections[key]

    def __iter__(self) -> Iterator[str]:
        """"""
        return self.sections.keys()
