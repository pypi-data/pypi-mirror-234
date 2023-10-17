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

import PyQt5.QtGui as visl
import PyQt5.QtWidgets as wdgt
from numpy import ndarray as n_array_t
from PyQt5.QtCore import QPoint as point_t

SIZE_FIXED = wdgt.QSizePolicy.Fixed


class image_wgt_t(wdgt.QLabel):
    def __init__(self, *args, **kwargs) -> None:
        """"""
        super().__init__(*args, **kwargs)
        self.setSizePolicy(SIZE_FIXED, SIZE_FIXED)
        self.setScaledContents(True)
        # Must be kept alive in instance.
        self.q_image = None

    def SetImage(self, rgb_image: n_array_t, /) -> None:
        """
        QImage call taken from:
        https://github.com/baoboa/pyqt5/blob/master/examples/widgets/imageviewer.py
        """
        self.q_image = visl.QImage(
            rgb_image.data,
            rgb_image.shape[1],
            rgb_image.shape[0],
            3 * rgb_image.shape[1],
            visl.QImage.Format_RGB888,
        )
        self.setPixmap(visl.QPixmap.fromImage(self.q_image))

    def DrawPoints(
        self,
        points: tuple[n_array_t, n_array_t],
        color: tuple[int, int, int],
        /,
        *,
        bbox_width: int = 1,
        bbox_height: int = 1,
    ) -> None:
        """"""
        contour_qpoints = tuple(point_t(point[1], point[0]) for point in zip(*points))
        pixmap = visl.QPixmap(self.pixmap())

        painter = visl.QPainter()
        painter.begin(pixmap)
        painter.setPen(visl.QPen(visl.QColor(*color)))  # Must be after call to begin
        for point in contour_qpoints:
            # TODO: Check why -1's are necessary.
            painter.drawPoint(point.x() + bbox_width - 1, point.y() + bbox_height - 1)
        painter.end()

        self.setPixmap(pixmap)
