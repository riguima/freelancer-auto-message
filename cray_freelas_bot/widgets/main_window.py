import inspect
import json
from importlib import import_module
from pathlib import Path

import pandas as pd
from PySide6 import QtCore, QtWidgets
from rocketry import Rocketry

from cray_freelas_bot.common.project import to_excel
from cray_freelas_bot.domain.browser import IBrowser
from cray_freelas_bot.exceptions.widgets import ConfigError
from cray_freelas_bot.widgets.configuration_window import ConfigurationWindow
from cray_freelas_bot.widgets.helpers import Button


class MainWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px;')
        self.setFixedSize(200, 100)
        self.setWindowTitle('Tela Principal')

        self.rock_app = Rocketry()

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
        except KeyError:
            raise ConfigError('Crie primeiro os bots em Configurações')
        for bot in bots:
            self.start_browser_task(bot)
        self.rock_app.run()

    def start_browser_task(self, bot_data: dict) -> None:
        module = import_module(
            f'cray_freelas_bot.use_cases.{bot_data["website"]}'
        )
        browser = self.get_browser_from_module(module)
        browser.make_login(bot_data['username'], bot_data['password'])

        @self.rock_app.task('minutely')
        def browser_task(execution='thread'):
            report_path = Path(bot_data['report_folder'] / 'result.xlsx')
            urls = pd.read_excel(report_path)['URL']
            projects_urls = [
                p.url for p in browser.get_projects(bot_data['category'])
            ]
            for project_url in projects_urls:
                if project_url not in urls:
                    message = browser.send_message(project_url)
                    to_excel(message, report_path)

    def get_browser_from_module(self, module) -> IBrowser:
        for _, obj in inspect.getmembers(module):
            if obj in IBrowser.__subclasses__():
                return obj()
