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
from typing import Annotated, Any, Callable, Iterator, Sequence

from babelwidget.main import (
    backend_t,
    button_wgt_h,
    grid_lyt_h,
    hbox_lyt_h,
    library_wgt_h,
    scroll_container_h,
    tabs_wgt_h,
    vbox_lyt_h,
)
from babelwidget.path_chooser import NewSelectedOutputDocument

from conf_ini_g import NewRawConfig
from conf_ini_g.catalog.interface.window.parameter.boolean import boolean_wgt_t
from conf_ini_g.catalog.interface.window.parameter.path import path_wgt_t
from conf_ini_g.catalog.specification.parameter.boolean import boolean_t
from conf_ini_g.catalog.specification.parameter.path import path_t as path_annotation_t
from conf_ini_g.interface.constant import INI_COMMENT_MARKER
from conf_ini_g.interface.storage.config import SaveRawConfigToINIDocument
from conf_ini_g.interface.window.component.section import (
    controlled_section_t,
    section_t,
)
from conf_ini_g.phase.instance.config.main import config_t as config_instance_t
from conf_ini_g.phase.raw.config import AsStr, ini_config_h, typed_config_h
from conf_ini_g.phase.specification.parameter.main import (
    parameter_t as parameter_spec_t,
)
from conf_ini_g.phase.specification.parameter.type import type_t
from conf_ini_g.phase.specification.section.main import section_t as section_spec_t

any_section_h = section_t | controlled_section_t


@dtcl.dataclass(repr=False, eq=False)
class config_t:
    """
    The class cannot use slots because it disables weak referencing, which is required.
    See error message below when using slots:
    TypeError: cannot create weak reference to 'config_t' object
    [...]
    File "[...]conf_ini_g/catalog/interface/window/backend/pyqt5/widget/choices.py", line 41, in SetFunction
        self.clicked.connect(function)
        │                    └ <bound method config_t.ToogleAdvancedMode of <conf_ini_g.interface.window.config.config_t object at [...]>>
        └ <conf_ini_g.catalog.interface.window.backend.pyqt5.widget.choices.dot_button_wgt_t object at [...]>

    Widget might not cooperate well with list, in which case Python raises the
    following exception: TypeError: multiple bases have instance lay-out conflict
    To be safe, "sections" is a field instead of being part of the class definition.
    """

    instance: config_instance_t
    backend: backend_t
    library_wgt: library_wgt_h
    Action: Callable[[typed_config_h], None] = None
    sections: dict[str, any_section_h] = dtcl.field(init=False)
    _reference_keeper: tuple[library_wgt_h, ...] = dtcl.field(init=False)
    _action_button: button_wgt_h = dtcl.field(init=False)
    _close_button: button_wgt_h = dtcl.field(init=False)
    _category_selector: scroll_container_h | tabs_wgt_h = dtcl.field(
        init=False, default=None
    )

    @classmethod
    def NewFromConfig(
        cls,
        title: str | None,
        instance: config_instance_t,
        backend: backend_t,
        /,
        *,
        advanced_mode: bool = False,
        action: tuple[str, Callable[[typed_config_h], None]] = None,
    ) -> config_t:
        """"""
        if action is None:
            kwargs = {}
        else:
            kwargs = {"Action": action[1]}
        output = cls(
            instance=instance,
            backend=backend,
            library_wgt=backend.library_wgt_t(),
            **kwargs,
        )

        # --- Top-level widgets
        title_lyt, widget_1, close_button = _TitleLayout(title, instance, output)
        advanced_mode_lyt, widget_2 = _AdvancedModeLayout(advanced_mode, output)
        button_lyt, widgets = _ActionButtonsLayout(
            output, action, instance.ini_path is not None
        )
        output._reference_keeper = (widget_1, widget_2, *widgets)
        output._close_button = close_button

        # --- Sections
        output._CreateSectionsAndCategories(instance, backend)
        category_selector = output._category_selector

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

        output.ToogleAdvancedMode(advanced_mode)

        return output

    def _CreateSectionsAndCategories(
        self, instance: config_instance_t, backend: backend_t, /
    ) -> None:
        """"""
        categories = {}
        sections = {}
        controlled_sections = []

        # --- Section creation
        for section_spec in instance.specification:
            if (controller := section_spec.controller) is None:
                section = section_t.NewForSection(
                    section_spec, instance[section_spec.name], backend
                )
            else:
                section = controlled_section_t.NewForSection(
                    section_spec,
                    controller,
                    instance.GetValueOfController(controller),
                    instance[section_spec.name],
                    backend,
                )
                if section is not None:
                    controlled_sections.append((section, section_spec))
            if section is None:
                continue

            sections[section_spec.name] = section

            if (category := section_spec.category) not in categories:
                contents = backend.library_wgt_t()
                scroll_area = backend.scroll_container_t.NewForWidget(contents)
                layout = backend.vbox_lyt_t()
                contents.setLayout(layout)
                categories[category] = (layout, scroll_area)

            layout = categories[category][0]
            layout.addWidget(section.library_wgt)

        self.sections = sections

        # --- Controlled sections <-> Controllers
        for section, section_spec in controlled_sections:
            controller = section_spec.controller
            parameter = self[controller.section].parameters[controller.parameter]
            value_wgt = parameter.value
            if hasattr(value_wgt, "SetFunction"):
                value_wgt.SetFunction(section.page_stack.setCurrentIndex)
            else:
                backend.ShowErrorMessage(
                    f"{controller.section}.{controller.parameter}: "
                    f'Controller has no "SetFunction" method; Disabling control.'
                )

        # --- Section dispatch into categories
        missing_category_selector = self._category_selector is None
        if categories.__len__() > 1:
            if missing_category_selector:
                category_selector = backend.tabs_wgt_t()
            else:
                category_selector = self._category_selector
            for category, (_, scroll_area) in categories.items():
                category_selector.addTab(scroll_area, category)
            if missing_category_selector:
                self._category_selector = category_selector
        elif missing_category_selector:
            category = tuple(categories.keys())[0]
            self._category_selector = categories[category][1]

    def ToogleAdvancedMode(self, advanced_mode: bool, /) -> None:
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

    def UpdateWithNewINI(self, ini_path: pl_path_t, /) -> None:
        """"""
        raw_config = NewRawConfig(ini_path=ini_path)
        config, issues, _ = config_instance_t.NewFromRawConfig(
            raw_config, self.instance.specification, path=ini_path
        )
        if issues.__len__() > 0:
            self.backend.ShowErrorMessage("\n".join(issues), parent=self.library_wgt)
            return

        category_selector = self._category_selector
        if isinstance(category_selector, self.backend.tabs_wgt_t):
            # Note: idx^th layout: category_selector.widget(t_idx).widget().layout().
            while category_selector.count() > 0:
                category_selector.removeTab(0)
        else:
            layout = category_selector.widget().layout()
            while layout.count() > 0:
                layout.itemAt(0).widget().setParent(None)

        self.instance = config
        self._CreateSectionsAndCategories(config, self.backend)
        self.ToogleAdvancedMode(self._reference_keeper[1].true_btn.isChecked())

    def ReassignCloseButtonTarget(self) -> None:
        """"""
        current = self.library_wgt
        while current is not None:
            main_window = current
            current = current.parent()

        self._close_button.SetFunction(main_window.close)

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
                self._action_button.setEnabled(False)
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
                self._action_button.setEnabled(True)

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

    def __getitem__(self, key: str, /) -> section_t | controlled_section_t:
        """"""
        return self.sections[key]

    def __iter__(self) -> Iterator[str]:
        """"""
        return self.sections.keys()


def _TitleLayout(
    title: str | None, instance: config_instance_t, config: config_t, /
) -> tuple[vbox_lyt_h, path_wgt_t, button_wgt_h]:
    """"""
    layout = config.backend.hbox_lyt_t()
    inner_layout = config.backend.vbox_lyt_t()

    if title is None:
        title = "Conf-INI-g"
    title = (
        f'<h1 style="color: blue">{title}</h1>'
        f"<b><font face=monospace>SPEC:</font></b> {instance.specification.spec_path}"
    )
    title_wgt = config.backend.label_wgt_t(title)
    title_wgt.setAlignment(config.backend.ALIGNED_LEFT)

    if instance.ini_path is None:
        ini_path_wgt = path_layout = None
    else:
        ini_path_wgt = path_wgt_t.NewWithDetails(
            pl_path_t(instance.ini_path),
            path_annotation_t(
                target_type=path_annotation_t.TARGET_TYPE.document, is_input=True
            ),
            config.backend,
            None,
            editable=False,
            PostAssignmentFunction=config.UpdateWithNewINI,
        )
        label_wgt = config.backend.label_wgt_t(
            "<b><font face=monospace>INI: </font></b>"
        )
        label_wgt.setSizePolicy(config.backend.SIZE_FIXED, config.backend.SIZE_FIXED)
        path_layout = config.backend.hbox_lyt_t()
        path_layout.addWidget(label_wgt)
        path_layout.addWidget(ini_path_wgt.library_wgt)

    inner_layout.addWidget(title_wgt)
    if path_layout is not None:
        inner_layout.addLayout(path_layout)

    button = config.backend.button_wgt_t("CLOSE")
    button.SetFunction(config.library_wgt.close)
    button.setSizePolicy(config.backend.SIZE_FIXED, config.backend.SIZE_MINIMUM)

    layout.addLayout(inner_layout)
    layout.addWidget(button)

    return layout, ini_path_wgt, button


def _AdvancedModeLayout(
    advanced_mode: bool, config: config_t, /
) -> tuple[hbox_lyt_h, boolean_wgt_t]:
    """"""
    layout = config.backend.hbox_lyt_t()

    annotated_type = Annotated[bool, boolean_t(mode=boolean_t.MODE.on_off)]
    value_type = type_t.NewFromTypeHint(annotated_type)
    boolean = boolean_wgt_t.NewWithDetails(
        advanced_mode,
        value_type,
        config.backend,
        None,
    )
    boolean.true_btn.SetFunction(config.ToogleAdvancedMode)

    layout.addWidget(config.backend.label_wgt_t("<i>Advanced Mode</i>"))
    layout.addWidget(boolean.library_wgt)

    return layout, boolean


def _ActionButtonsLayout(
    config: config_t,
    action: tuple[str, Callable[[typed_config_h], None]] | None,
    has_ini_document: bool,
    /,
) -> tuple[grid_lyt_h, Sequence[button_wgt_h, ...]]:
    """"""
    layout = config.backend.grid_lyt_t()

    buttons = []
    geometries = []

    button = config.backend.button_wgt_t("Show in INI format")
    button.SetFunction(config.ShowInINIFormat)
    buttons.append(button)
    geometries.append((0, 0, 1, 2))

    button = config.backend.button_wgt_t("Save Config As")
    button.SetFunction(lambda: config.SaveConfig(True))
    buttons.append(button)
    if has_ini_document:
        geometries.append((1, 0, 1, 1))

        button = config.backend.button_wgt_t("Save/Overwrite Config")
        button.SetFunction(lambda: config.SaveConfig(False))
        buttons.append(button)
        geometries.append((1, 1, 1, 1))
    else:
        geometries.append((1, 0, 1, 2))

    if action is None:
        label = "CLOSE"
        Function = config.library_wgt.close
    else:
        label = action[0]
        Function = config.LaunchAction

    button = config.backend.button_wgt_t(label)
    button.SetFunction(Function)
    buttons.append(button)
    geometries.append((2, 0, 1, 2))

    config._action_button = button

    for button, geometry in zip(buttons, geometries):
        layout.addWidget(button, *geometry)
    layout.setContentsMargins(0, 0, 0, 0)

    return layout, buttons
