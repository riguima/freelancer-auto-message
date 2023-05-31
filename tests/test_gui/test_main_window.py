import os

import pytest
from PySide6 import QtCore

from cray_freelas_bot.widgets.main_window import MainWindow


@pytest.fixture(scope='module')
def main_window() -> MainWindow:
    return MainWindow()


def test_show_bots_window(qtbot, main_window: MainWindow) -> None:
    qtbot.addWidget(main_window)
    qtbot.mouseClick(main_window.bots_button, QtCore.Qt.LeftButton)
    assert main_window.bots_window.isVisible()


def test_run_without_bots(qtbot, main_window: MainWindow) -> None:
    qtbot.addWidget(main_window)
    qtbot.mouseClick(main_window.run_button, QtCore.Qt.LeftButton)
    assert main_window.message_box.text() == 'Crie primeiro os bots'


def test_run_without_bots(qtbot, main_window: MainWindow) -> None:
    qtbot.addWidget(main_window)
    os.remove('.bots.json')
    qtbot.mouseClick(main_window.run_button, QtCore.Qt.LeftButton)
    assert main_window.message_box.text() == 'Crie primeiro os bots'
