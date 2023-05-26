import json

from PySide6 import QtCore, QtWidgets

from cray_freelas_bot.common.project import create_browser_from_module
from cray_freelas_bot.widgets.configuration_window import ConfigurationWindow
from cray_freelas_bot.widgets.helpers import Button
from cray_freelas_bot.widgets.threads import BrowserThread


class MainWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px;')
        self.setFixedSize(200, 100)
        self.setWindowTitle('Tela Principal')

        self.browsers = []
        self.browser_thread = BrowserThread(self)

        self.message_box = QtWidgets.QMessageBox()
        self.message_box.setWindowTitle('Aviso')

        self.configuration_window = ConfigurationWindow(self)

        self.configuration_button = Button('Configurações')
        self.configuration_button.clicked.connect(self.show_configuration)

        self.run_button = Button('Rodar')
        self.run_button.clicked.connect(self.run_browsers)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.configuration_button)
        self.layout.addWidget(self.run_button)

    @QtCore.Slot()
    def show_configuration(self) -> None:
        self.configuration_window.show()

    @QtCore.Slot()
    def run_browsers(self) -> None:
        self.browsers = []
        bots = json.load(open('.secrets.json'))['bots']
        if bots:
            for bot in bots:
                browser = create_browser_from_module(bot['website'])
                browser.make_login(bot['username'], bot['password'])
                self.browsers.append(browser)
            self.browser_thread.start()
        else:
            self.message_box.setText('Crie primeiro os bots em Configurações')
            self.message_box.show()
