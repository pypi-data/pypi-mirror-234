# Copyright CNRS/Inria/UCA
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

from configparser import ConfigParser as config_parser_t

from openpyxl import Workbook as workbook_t

from conf_ini_g.extension.path import any_path_h, path_t
from conf_ini_g.light.ini import NewConfigFromPath as NewConfigFromINIPath
from conf_ini_g.light.xlsx import NewConfigFromPath as NewConfigFromXLSXPath


def INItoXLSX(
    ini_path: any_path_h, xlsx_path: any_path_h, /, *, should_overwrite: bool = False
) -> None:
    """"""
    ini_path, xlsx_path = _AsPaths(ini_path, xlsx_path)
    _CheckOverwriting(xlsx_path, should_overwrite)

    config = NewConfigFromINIPath(ini_path)

    workbook = workbook_t()
    # Remove the (a priori unique) default worksheet
    for worksheet in workbook.sheetnames:
        # The "remove" method is for worksheets, not names. Use this instead:
        del workbook[worksheet]
    for sct_name, content in config.items():
        worksheet = workbook.create_sheet(title=sct_name)
        for prm_name, value in content.items():
            worksheet.append((prm_name, str(value)))

    workbook.save(xlsx_path)


def XLSXtoINI(
    xlsx_path: any_path_h, ini_path: any_path_h, /, *, should_overwrite: bool = False
) -> None:
    """"""
    ini_path, xlsx_path = _AsPaths(ini_path, xlsx_path)
    _CheckOverwriting(ini_path, should_overwrite)

    config_as_dict = NewConfigFromXLSXPath(xlsx_path)
    config_as_dict = {
        _sct: {_prm: str(_vle) for _prm, _vle in _ctn.items()}
        for _sct, _ctn in config_as_dict.items()
    }

    config = config_parser_t()
    config.optionxform = lambda option: option  # To avoid automatic lowercasing
    config.read_dict(config_as_dict)
    with open(ini_path, "w") as accessor:
        config.write(accessor)


def _AsPaths(ini_path: any_path_h, xlsx_path: any_path_h, /) -> tuple[path_t, path_t]:
    """"""
    if isinstance(ini_path, str):
        ini_path = path_t(ini_path)
    if isinstance(xlsx_path, str):
        xlsx_path = path_t(xlsx_path)

    return ini_path, xlsx_path


def _CheckOverwriting(path: path_t, should_overwrite: bool, /) -> None:
    """"""
    if path.exists() and (path.is_dir() or (path.is_file() and not should_overwrite)):
        raise ValueError(f"{path}: Path already exists.")
