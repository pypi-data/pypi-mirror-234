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

from math import pi as PI

INI_UNIT_SECTION = "UNITS"  # In uppercase

INI_VALUE_ASSIGNMENT = "="
INI_UNIT_SEPARATOR = ":IN:"
INI_COMMENT_MARKER = "#"


_STD_UNIT_CONVERSIONS = (
    # unit, unit name, parent unit (None if none), conversion factor (1.0 if None)
    ("si", "site", None, 1.0),  # Synonym for sample, pixel, voxel...
    #
    ("km", "kilometer", "m", 1000.0),
    ("m", "meter", "si", 1.0),
    ("cm", "centimeter", "m", 1.0e-2),
    ("mm", "millimeter", "m", 1.0e-3),
    ("um", "micrometer", "m", 1.0e-6),
    ("nm", "nanometer", "m", 1.0e-9),
    ("mi", "mile", "m", 1.0 / 0.00062137),
    ("yd", "yard", "m", 0.9144),
    ("ft", "foot", "m", 1.0 / 3.2808),
    ("in", "inch", "m", 1.0 / 39.37),
    #
    ("r", "radian", "si", 1.0),
    ("d", "degree", "r", PI / 180.0),
    #
    ("wk", "week", "s", 604800.0),
    ("dy", "day", "s", 86400.0),
    ("h", "hour", "s", 3600.0),
    ("mn", "minute", "s", 60.0),
    ("s", "second", "si", 1.0),
    ("ms", "millisecond", "s", 1.0e-3),
    ("us", "microsecond", "s", 1.0e-6),
    ("ns", "nanosecond", "s", 1.0e-9),
)
STD_UNIT_CONVERSIONS = {_elm[0]: _elm[-1] for _elm in _STD_UNIT_CONVERSIONS}


STD_ABBREVIATIONS = {
    "fct": "function",
    "mod": "module",
    "n": "number of",
    "o": "of",
    "prm": "parameter",
    "rng": "range",
}


SECTION_COLOR = "green"
PARAMETER_COLOR = "blue"


PATH_SELECTOR_WIDTH = 100
