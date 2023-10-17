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
from typing import Any, Sequence

from rich.text import Text as text_t
from str_to_obj import CastValue, ObjectFromStr, annotation_t
from str_to_obj.type.hint_tree import hint_tree_t

from conf_ini_g.phase.instance.parameter.value import INVALID_VALUE


@dtcl.dataclass(slots=True, repr=False, eq=False)
class type_t(hint_tree_t):
    def Issues(self) -> list[str]:
        """"""
        output = []

        for annotation in self.all_annotations:
            output.extend(
                f"/{type(self).__name__}.{id(self)}/ {_iss}"
                for _iss in annotation.Issues()
            )

        return output

    def FirstAnnotationWithAttribute(
        self, attribute: str | Sequence[str], /
    ) -> annotation_t | None:
        """"""
        # Do not test isinstance(attribute, Sequence) since str is a sequence.
        if isinstance(attribute, str):
            attributes = (attribute,)
        else:
            attributes = attribute

        for annotation in self.all_annotations:
            if all(hasattr(annotation, _ttr) for _ttr in attributes):
                return annotation

        return None

    def ValueIsCompliant(self, value: Any, /) -> list[str]:
        """"""
        return CastValue(value, self, only_check_validity=True)

    def InterpretedValueOf(self, value: Any, /) -> tuple[Any, list[str]]:
        """"""
        if isinstance(value, str):
            typed_value, issues = ObjectFromStr(value, expected_type=self)
        else:
            typed_value, issues = CastValue(value, self)

        if issues.__len__() > 0:
            return INVALID_VALUE, issues

        return typed_value, []

    def __str__(self) -> str:
        """"""
        return text_t.from_markup(self.__rich__()).plain

    def __rich__(self) -> str:
        """"""
        output = [f"[white]{self.template_as_str}[/]"]

        for annotation in self.all_annotations:
            output.append(type(annotation).__name__)

        return "[yellow]" + "::".join(output) + "[/]"


@dtcl.dataclass(slots=True, repr=False, eq=False)
class _any_type_t(type_t):
    def Issues(self) -> list[str]:
        """"""
        return []

    def FirstAnnotationWithAttribute(
        self, attribute: str | Sequence[str], /
    ) -> annotation_t | None:
        """"""
        return None

    def ValueIsCompliant(self, value: Any, /) -> list[str]:
        """"""
        return []

    def InterpretedValueOf(self, value: Any, /) -> tuple[Any, list[str]]:
        """"""
        return value, []


ANY_TYPE = _any_type_t.NewFromTypeHint(Any)
