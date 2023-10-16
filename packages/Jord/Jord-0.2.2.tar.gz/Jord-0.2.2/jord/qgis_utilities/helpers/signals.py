#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Lindbjerg"
__doc__ = r"""

           Created on 02-12-2020
           """

__all__ = ["disconnect_signal", "connect_signal", "reconnect_signal"]

from logging import warning

# noinspection PyUnresolvedReferences
from qgis.PyQt import QtCore

IS_DEBUGGING = False


def connect_signal(signal: QtCore.pyqtSignal, new_handler: callable = None) -> None:
    """

    :param signal:
    :param new_handler:
    :return:
    """
    if new_handler is not None:  # if new_handler is not None, connect it
        signal.connect(new_handler)
    else:
        if IS_DEBUGGING:
            raise Exception("new_handler is None")
        warning("new_handler is None")


def disconnect_signal(signal: QtCore.pyqtSignal, old_handler: callable = None) -> None:
    """

    :param signal:
    :param old_handler:
    :return:
    """
    if signal is not None:
        try:
            if old_handler is not None:  # disconnect old_handler(s)
                while True:
                    # the loop is needed for safely disconnecting a specific handler,
                    # because it may have been connected multple times,
                    # and disconnect(slot) only removes one connection at a time.
                    signal.disconnect(old_handler)
            else:  # disconnect all, only available when old_handler is None and we are debugging, as this is bad practice
                if IS_DEBUGGING:
                    signal.disconnect()
        except TypeError:
            pass


def reconnect_signal(
    signal: QtCore.pyqtSignal,
    new_handler: callable = None,
    old_handler: callable = None,
) -> None:
    """

    :param signal:
    :type signal: QtCore.pyqtSignal
    :param new_handler:
    :type new_handler: callable
    :param old_handler:
    :type old_handler: callable
    :return:
    :rtype: None
    """
    disconnect_signal(signal, old_handler)
    connect_signal(signal, new_handler)
