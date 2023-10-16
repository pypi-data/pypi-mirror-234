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
from typing import Annotated, Sequence

from str_to_obj import annotation_t
from str_to_obj.type.hint import annotated_hint_t


@dtcl.dataclass(repr=False, eq=False)
class choices_t(annotation_t):
    ACCEPTED_TYPES = (str,)
    options: Sequence[str]

    @classmethod
    def NewAnnotatedType(cls, options: Sequence[str], /) -> annotated_hint_t:
        """"""
        return Annotated[str, cls(tuple(options))]

    def Issues(self) -> list[str]:
        """"""
        output = []

        for option in self.options:
            if not isinstance(option, str):
                output.append(
                    f"{type(option).__name__}: Invalid type of option {option} "
                    f"in {self}; Expected=str"
                )

        return output

    def ValueIsCompliant(self, value: str, /) -> list[str]:
        """"""
        if (self.options.__len__() == 0) or (value in self.options):
            # Options can be empty for a controlling parameter whose controlled section
            # has not been specified. In a GUI context, such controlled section should
            # have been populated programmatically.
            return []

        options = map(lambda _elm: f'"{_elm}"', self.options)
        options = " or ".join(options)

        return [f"{value}: Invalid choice; Expected={options}."]
