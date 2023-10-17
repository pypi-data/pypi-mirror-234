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

from configparser import ConfigParser as config_t
from configparser import ExtendedInterpolation

from conf_ini_g.extension.path import any_path_h
from conf_ini_g.phase.raw.config import ini_config_h

_DEFAULT_OPTIONS = (
    ("delimiters", ("=",)),
    ("comment_prefixes", ("#",)),
    ("inline_comment_prefixes", ("#",)),
    ("interpolation", ExtendedInterpolation()),
)


def NewConfigFromPath(path: any_path_h, /, **kwargs) -> ini_config_h:
    """"""
    options = kwargs.copy()
    for name, value in _DEFAULT_OPTIONS:
        if name not in options:
            options[name] = value

    config = config_t(**options)
    config.optionxform = lambda option: option  # To avoid automatic lowercasing
    config.read(path)

    # config.sections(): Does not include the default section named configparser.DEFAULTSECT
    return {_nme: dict(config[_nme]) for _nme in config.sections()}
    # return {
    #     _nme: {
    #         _prm: _vle for _prm, _vle in config[_nme].items()
    #     }
    #     for _nme in config.sections()
    # }
