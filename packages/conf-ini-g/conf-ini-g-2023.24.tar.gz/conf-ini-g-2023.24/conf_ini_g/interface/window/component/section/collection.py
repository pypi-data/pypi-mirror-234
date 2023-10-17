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

from typing import Sequence

from babelwidget.main import backend_t, scroll_container_h, tabs_wgt_h

from conf_ini_g.interface.window.component.section.main import (
    controlled_section_t,
    section_t,
)
from conf_ini_g.phase.instance.config.main import config_t as config_instance_t
from conf_ini_g.phase.specification.section.main import section_t as section_spec_t

any_section_h = section_t | controlled_section_t


def SectionsAndCategories(
    instance: config_instance_t,
    category_selector: scroll_container_h | tabs_wgt_h | None,
    backend: backend_t,
    /,
) -> tuple[
    dict[str, any_section_h],
    Sequence[tuple[controlled_section_t, section_spec_t]],
    scroll_container_h | tabs_wgt_h,
]:
    """"""
    sections = {}
    controlled_sections = []
    categories = {}

    # --- Sections and categories
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

    # --- Section dispatch into categories
    missing_category_selector = category_selector is None
    if categories.__len__() > 1:
        if missing_category_selector:
            category_selector = backend.tabs_wgt_t()
        for category, (_, scroll_area) in categories.items():
            category_selector.addTab(scroll_area, category)
    elif missing_category_selector:
        category = tuple(categories.keys())[0]
        category_selector = categories[category][1]

    return sections, controlled_sections, category_selector
