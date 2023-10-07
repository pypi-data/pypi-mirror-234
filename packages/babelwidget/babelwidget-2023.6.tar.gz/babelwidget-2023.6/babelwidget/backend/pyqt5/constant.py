# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2023)
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

import PyQt5.QtCore as core
import PyQt5.QtGui as visl
import PyQt5.QtWidgets as wdgt

ALIGNED_CENTER = core.Qt.AlignmentFlag.AlignCenter
ALIGNED_HCENTER = core.Qt.AlignmentFlag.AlignHCenter
ALIGNED_LEFT = core.Qt.AlignmentFlag.AlignLeft
ALIGNED_RIGHT = core.Qt.AlignmentFlag.AlignRight
ALIGNED_TOP = core.Qt.AlignmentFlag.AlignTop
BASE_PALETTE = visl.QPalette.Base
DIALOG_ACCEPTATION = wdgt.QDialog.Accepted
DIALOG_ACCEPT_OPEN = wdgt.QFileDialog.AcceptOpen
DIALOG_ACCEPT_SAVE = wdgt.QFileDialog.AcceptSave
DIALOG_AUTO_OVERWRITE = wdgt.QFileDialog.DontConfirmOverwrite
DIALOG_MODE_ANY = wdgt.QFileDialog.AnyFile
DIALOG_MODE_EXISTING_FILE = wdgt.QFileDialog.ExistingFile
DIALOG_MODE_FOLDER = wdgt.QFileDialog.Directory
FORMAT_RICH = core.Qt.TextFormat.RichText
LINE_NO_WRAP = wdgt.QTextEdit.LineWrapMode.NoWrap
SELECTABLE_TEXT = core.Qt.TextInteractionFlag.TextSelectableByMouse
SIZE_EXPANDING = wdgt.QSizePolicy.Expanding
SIZE_FIXED = wdgt.QSizePolicy.Fixed
SIZE_MINIMUM = wdgt.QSizePolicy.Minimum
TAB_POSITION_EAST = wdgt.QTabWidget.East
WIDGET_TYPE = core.Qt.WindowType.Widget
WORD_NO_WRAP = visl.QTextOption.WrapMode.NoWrap


def Color(name: str, /) -> visl.QColorConstants:
    """"""
    return getattr(visl.QColorConstants, name)
