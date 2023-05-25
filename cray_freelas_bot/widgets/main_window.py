import inspect
import json
from importlib import import_module
from threading import Thread

from PySide6 import QtCore, QtWidgets

from cray_freelas_bot.domain.browser import IBrowser
from cray_freelas_bot.exceptions.widgets import ConfigError
from cray_freelas_bot.widgets.configuration_window import ConfigurationWindow
from cray_freelas_bot.widgets.helpers import Button


class MainWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px;')
        self.setFixedSize(500, 250)
        self.setWindowTitle('Tela Principal')

        self.configuration_window = ConfigurationWindow()

        self.configuration_button = Button('Configuração')
        self.configuration_button.clicked.connect(self.show_configuration)

        self.run_button = Button('Rodar')
        self.run_button.clicked.connect(self.run)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.configuration_button)

    @QtCore.Slot()
    def show_configuration(self) -> None:
        self.configuration_window.show()

    @QtCore.Slot()
    def run(self) -> None:
        try:
            accounts = json.load(open('.secrets.json'))['accounts']
        except KeyError:
            raise ConfigError(
                'Defina o login para as contas no arquivo .secrets.json'
            )
        for account in accounts:
            module = import_module(
                f'cray_freelas_bot.use_cases.{account["browser"]}'
            )
            browser = self.get_browser_from_module(module)
            Thread(browser.run).start()

    def get_browser_from_module(self, module) -> IBrowser:
        for _, obj in inspect.getmembers(module):
            if obj in IBrowser.__subclasses__():
                return obj()
