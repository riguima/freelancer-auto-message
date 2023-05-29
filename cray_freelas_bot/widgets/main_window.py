from PySide6 import QtCore, QtWidgets

from cray_freelas_bot.repositories.bot import BotRepository
from cray_freelas_bot.widgets.bots_window import BotsWindow
from cray_freelas_bot.widgets.helpers import Button
from cray_freelas_bot.widgets.threads import BrowserThread


class MainWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px;')
        self.setFixedSize(200, 100)
        self.setWindowTitle('Tela Principal')

        self.browsers = []
        self.browser_thread = BrowserThread()

        self.message_box = QtWidgets.QMessageBox()
        self.message_box.setWindowTitle('Aviso')

        self.bots_window = BotsWindow(self)

        self.bots_button = Button('Bots')
        self.bots_button.clicked.connect(self.show_bots_window)

        self.run_button = Button('Rodar')
        self.run_button.clicked.connect(self.run_browsers)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.bots_button)
        self.layout.addWidget(self.run_button)

    @QtCore.Slot()
    def show_bots_window(self) -> None:
        self.bots_window.show()
        self.close()

    @QtCore.Slot()
    def run_browsers(self) -> None:
        self.browsers = []
        bots = BotRepository().all()
        if bots:
            self.browser_thread.start()
        else:
            self.message_box.setText('Crie primeiro os bots')
            self.message_box.show()
