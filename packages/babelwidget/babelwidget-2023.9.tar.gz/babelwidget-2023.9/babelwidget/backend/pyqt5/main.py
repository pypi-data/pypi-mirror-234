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

import PyQt5.QtWidgets as wdgt
from PyQt5.QtCore import QCoreApplication as qt_core_app_t

from babelwidget.backend.pyqt5.widget.main import library_wgt_t


class event_loop_t(wdgt.QApplication):
    def Run(self) -> int:
        """"""
        return self.exec_()


def ShowMessage(title: str, message: str, /, *, parent: library_wgt_t = None) -> None:
    """"""
    dialog = wdgt.QMessageBox(parent=parent)
    dialog.setWindowTitle(title)
    dialog.setText("<b>" + title + "</b>")
    dialog.setInformativeText(message)
    dialog.setStandardButtons(wdgt.QMessageBox.StandardButton.Close)
    dialog.setDefaultButton(wdgt.QMessageBox.StandardButton.Close)
    dialog.exec_()


def ShowErrorMessage(message: str, /, *, parent: library_wgt_t = None) -> None:
    """"""
    wdgt.QMessageBox.critical(parent, "Error", message)
