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
from typing import ClassVar

from str_to_obj import annotation_t

number_h = int | float


@dtcl.dataclass(repr=False, eq=False)
class number_t(annotation_t):
    INFINITY_NEG: ClassVar[float] = -float("inf")
    INFINITY_POS: ClassVar[float] = float("inf")
    INFINITE_PRECISION: ClassVar[float] = 0.0

    ACCEPTED_TYPES = (int, float)
    min: number_h = INFINITY_NEG
    max: number_h = INFINITY_POS
    min_inclusive: bool = True
    max_inclusive: bool = True
    precision: number_h = INFINITE_PRECISION

    def Issues(self) -> list[str]:
        """"""
        output = []

        self_class = self.__class__
        if (self.min != self_class.INFINITY_NEG) and not isinstance(
            self.min, number_h.__args__
        ):
            output.append(
                f"{type(self.min)}: Invalid type for min value {self.min} "
                f"in {self}; Expected={number_h}"
            )
        if (self.max != self_class.INFINITY_POS) and not isinstance(
            self.max, number_h.__args__
        ):
            output.append(
                f"{type(self.max)}: Invalid type for max value {self.max} "
                f"in {self}; Expected={number_h}"
            )
        if (self.precision != self_class.INFINITE_PRECISION) and not isinstance(
            self.precision, number_h.__args__
        ):
            output.append(
                f"{type(self.precision)}: Invalid type for precision {self.precision} "
                f"in {self}; Expected={number_h}"
            )
        if self.precision < 0:
            output.append(f"{self.precision}: Negative precision in {self}")
        if (self.min > self.max) or (
            (self.min == self.max) and not (self.min_inclusive and self.max_inclusive)
        ):
            if self.min_inclusive:
                opening = "["
            else:
                opening = "]"
            if self.max_inclusive:
                closing = "]"
            else:
                closing = "["
            output.append(
                f"{opening}{self.min},{self.max}{closing}: Empty value interval in {self}"
            )

        return output

    def ValueIsCompliant(self, value: number_h, /) -> list[str]:
        """"""
        if self.min <= value <= self.max:
            if ((value == self.min) and not self.min_inclusive) or (
                (value == self.max) and not self.max_inclusive
            ):
                return [f"{value}: Value outside prescribed interval."]

            if (self.precision != self.__class__.INFINITE_PRECISION) and (
                self.precision * int(value / self.precision) != value
            ):
                return [f"{value}: Value of higher precision than the prescribed one."]

            return []
        else:
            return [f"{value}: Value outside prescribed interval."]
