import inspect
import json
from importlib import import_module
from pathlib import Path

from PySide6 import QtCore, QtWidgets

from cray_freelas_bot.common.project import to_excel
from cray_freelas_bot.domain.browser import IBrowser
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
        self.browser_thread = BrowserThread(self.browsers)

        self.message_box = QtWidgets.QMessageBox()
        self.message_box.setWindowTitle('Aviso')

        self.configuration_window = ConfigurationWindow(self)

        self.configuration_button = Button('Configurações')
        self.configuration_button.clicked.connect(self.show_configuration)

        self.run_button = Button('Rodar')
        self.run_button.clicked.connect(self.run)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.configuration_button)
        self.layout.addWidget(self.run_button)

    @QtCore.Slot()
    def show_configuration(self) -> None:
        self.configuration_window.show()

    @QtCore.Slot()
    def run(self) -> None:
        try:
            bots = json.load(open('.secrets.json'))['bots']
            for bot in bots:
                module = import_module(
                    f'cray_freelas_bot.use_cases.{bot["website"]}'
                )
                browser = self.get_browser_from_module(module)
                browser.make_login(bot['username'], bot['password'])
                to_excel([], Path(bot['report_folder']) / 'result.xlsx')
                self.browsers.append(browser)
            self.browser_thread.start()
        except KeyError:
            self.message_box.setText('Crie primeiro os bots em Configurações')
            self.message_box.show()

    def get_browser_from_module(self, module) -> IBrowser:
        for _, obj in inspect.getmembers(module):
            if obj in IBrowser.__subclasses__():
                return obj()
