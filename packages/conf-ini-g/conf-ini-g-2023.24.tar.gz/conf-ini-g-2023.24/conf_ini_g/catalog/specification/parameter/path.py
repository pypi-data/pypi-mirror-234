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

import dataclasses as dtcl
from enum import Enum as enum_t
from pathlib import Path as pl_path_t
from typing import Annotated

from str_to_obj import annotation_t
from str_to_obj.type.hint import annotated_hint_t


@dtcl.dataclass(slots=True, repr=False, eq=False)
class path_t(annotation_t):
    class TARGET_TYPE(enum_t):
        document = 1
        folder = 2
        any = 3

    ACCEPTED_TYPES = (pl_path_t,)
    target_type: enum_t
    is_input: bool

    @classmethod
    def NewAnnotatedType(
        cls, target_type: TARGET_TYPE, is_input: bool, /
    ) -> annotated_hint_t:
        """"""
        return Annotated[pl_path_t, cls(target_type=target_type, is_input=is_input)]

    def ValueIsCompliant(self, value: pl_path_t | None, /) -> list[str]:
        """
        None: Unspecified path.
        """
        if value is None:
            return []

        if not self.is_input:
            return []

        if value.exists():
            if self.target_type is path_t.TARGET_TYPE.any:
                if value.is_file() or value.is_dir():
                    return []
                else:
                    return [f"{value}: Not a valid file or folder."]

            if (self.target_type is path_t.TARGET_TYPE.document) and value.is_file():
                return []

            if (self.target_type is path_t.TARGET_TYPE.folder) and value.is_dir():
                return []

        return [
            f"{value}: Non-existent file or folder, or file for folder, or folder for file."
        ]
