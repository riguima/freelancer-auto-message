from PySide6 import QtCore

from cray_freelas_bot.widgets.main_window import MainWindow


def test_show_bots_window(qtbot) -> None:
    widget = MainWindow()
    qtbot.addWidget(widget)
    qtbot.mouseClick(widget.bots_button, QtCore.Qt.LeftButton)
    assert widget.bots_window.isVisible()
