import json
from datetime import datetime
from pathlib import Path
from time import sleep

import pandas as pd
from PySide6 import QtCore, QtWidgets

from cray_freelas_bot.common.project import (
    create_browser_from_module,
    get_greeting_according_time,
    to_excel,
)
from cray_freelas_bot.domain.browser import IBrowser
from cray_freelas_bot.exceptions.project import ProjectError


class BrowserThread(QtCore.QThread):
    def run(self) -> None:
        browsers = self.create_browsers()
        while True:
            bots = json.load(open('.secrets.json'))['bots']
            for browser, bot in zip(browsers, bots):
                report_path = Path(bot['report_folder']) / 'result.xlsx'
                urls = pd.read_excel(report_path)['URL']
                projects_urls = browser.get_projects_urls(bot['category'])
                for project_url in projects_urls:
                    if project_url not in urls:
                        try:
                            project = browser.get_project(project_url)
                        except ProjectError:
                            continue
                        greeting = get_greeting_according_time(
                            datetime.now().time()
                        )
                        text = (
                            f'{greeting} {{b}}{project.client_name}{{/b}}, '
                            f'tudo bem?\n\n Ao ler sobre o seu projeto '
                            f'{{b}}"{project.name}"{{/b}}, percebi que ele '
                            'está alinhado com a minha expertise em '
                            f'{project.category}, gostaria de saber qual o '
                            'seu prazo ideal para a conclusão do projeto e se '
                            'você possui algum detalhe em específico que '
                            'considera fundamental?\n\n'
                            f'ass: {{b}}{browser.get_account_name()}{{/b}}'
                        )
                        message = browser.send_message(text, project_url)
                        to_excel([message], report_path)
            sleep(60)

    def create_browsers(self) -> list[IBrowser]:
        result = []
        bots = json.load(open('.secrets.json'))['bots']
        for bot in bots:
            browser = create_browser_from_module(
                bot['website'],
                user_data_dir=bot['user_data_dir'],
                visible=True,
            )
            result.append(browser)
        return result


class CreateBotThread(QtCore.QThread):
    finished = QtCore.Signal()

    def __init__(self, widget: QtWidgets.QWidget) -> None:
        super().__init__()
        self.widget = widget

    def run(self) -> None:
        data = json.load(open('.secrets.json'))
        username = self.widget.username_input.text().split("@")[0].replace(
            ".", "_"
        )
        bot = {
            'username': self.widget.username_input.text(),
            'password': self.widget.password_input.text(),
            'website': self.widget.WEBSITES[
                self.widget.website_combobox.currentText()
            ],
            'category': self.widget.category_combobox.currentText(),
            'report_folder': self.widget.report_folder_input.text(),
            'user_data_dir': f'.{username}_user_data',
        }
        browser = create_browser_from_module(
            bot['website'],
            user_data_dir=bot['user_data_dir'],
        )
        browser.make_login(bot['username'], bot['password'])
        to_excel([], Path(bot['report_folder']) / 'result.xlsx')
        data['bots'].append(bot)
        json.dump(data, open('.secrets.json', 'w'))
        self.finished.emit()
