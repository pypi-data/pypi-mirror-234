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

from conf_ini_g.interface.constant import STD_UNIT_CONVERSIONS
from conf_ini_g.phase.specification.parameter.main import parameter_t
from conf_ini_g.phase.specification.parameter.type import type_t


@dtcl.dataclass(slots=True, repr=False, eq=False)
class unit_t(parameter_t):
    def __post_init__(self) -> None:
        """
        Unit parameter are never part of a specification. They can appear in INI
        documents, and are therefore only instantiated programmatically.
        """
        self.type = type_t.NewFromTypeHint(float)

    def Issues(self) -> list[str]:
        """"""
        if self.name in STD_UNIT_CONVERSIONS.keys():
            return [
                f"{self.name}: Redefinition of a standard unit; Please use another unit name."
            ]

        return []

    @property
    def optional(self) -> bool:
        """"""
        return True
