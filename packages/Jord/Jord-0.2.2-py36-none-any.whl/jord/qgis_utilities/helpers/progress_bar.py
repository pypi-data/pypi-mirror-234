#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Lindbjerg"
__doc__ = r"""

           Created on 02-12-2020
           """

from typing import Tuple

# noinspection PyUnresolvedReferences
from qgis.PyQt import QtGui, QtWidgets

__all__ = ["dialog_progress_bar"]


def dialog_progress_bar(
    progress: int = 0, *, minimum_width: int = 300
) -> Tuple[QtWidgets.QDialog, QtWidgets.QProgressBar]:
    """
    Create a progress bar dialog.

    :param progress: The progress to display.
    :type progress: int
    :param minimum_width: The minimum width of the dialog.
    :type minimum_width: int
    :return: The dialog.
    :rtype: Tuple[QtWidgets.QDialog, QtWidgets.QProgressBar]
    """
    dialog = QtGui.QProgressDialog()
    dialog.setWindowTitle("Progress")
    dialog.setLabelText("text")

    bar = QtWidgets.QProgressBar(dialog)
    bar.setTextVisible(True)
    bar.setValue(progress)

    dialog.setBar(bar)
    dialog.setMinimumWidth(minimum_width)
    dialog.show()

    return dialog, bar


if __name__ == "__main__":

    def calc(x, y):
        from time import sleep

        dialog, bar = dialog_progress_bar(0)
        bar.setValue(0)
        bar.setMaximum(100)
        sum_ = 0
        for i in range(x):
            for j in range(y):
                k = i + j
                sum_ += k
            i += 1
            bar.setValue((float(i) / float(x)) * 100)
            sleep(0.1)
        print(sum_)

    # calc(10000, 2000)
