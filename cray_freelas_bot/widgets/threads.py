import json
from datetime import datetime
from pathlib import Path
from time import sleep

import pandas as pd
from PySide6 import QtCore, QtWidgets

from cray_freelas_bot.common.project import (
    create_browser_from_module,
    get_bots,
    get_greeting_according_time,
    to_excel,
)
from cray_freelas_bot.domain.browser import IBrowser
from cray_freelas_bot.domain.models import Project
from cray_freelas_bot.exceptions.project import ProjectError


class BrowserThread(QtCore.QThread):
    def __init__(self) -> None:
        self.browsers = self.create_browsers()

    def run(self) -> None:
        while True:
            for browser, bot in zip(self.browsers, get_bots()):
                report_path = Path(bot['report_folder']) / 'result.xlsx'
                urls = pd.read_excel(report_path)['URL']
                projects_urls = browser.get_projects_urls(bot['category'])
                for project_url in projects_urls:
                    if project_url not in urls:
                        try:
                            project = browser.get_project(project_url)
                        except ProjectError:
                            continue
                        text = self.get_browser_message_text(
                            self.browsers.index(browser), project
                        )
                        message = browser.send_message(text, project_url)
                        to_excel([message], report_path)
            sleep(60)

    def create_browsers(self) -> list[IBrowser]:
        result = []
        for bot in get_bots():
            browser = create_browser_from_module(
                bot['website'],
                user_data_dir=bot['user_data_dir'],
                visible=False,
            )
            result.append(browser)
        return result

    def get_browser_message_text(
        self, browser_index: int, project: Project
    ) -> list[str]:
        browser = self.browsers[browser_index]
        text = get_bots()[browser_index]['message']
        greeting = get_greeting_according_time(datetime.now().time())
        text.replace('{saudação}', greeting)
        text.replace('{nome do cliente}', project.client_name)
        text.replace('{nome do projeto}', project.name)
        text.replace('{categoria}', project.category)
        text.replace('{nome da conta}', browser.get_account_name())
        return text


class CreateBotThread(QtCore.QThread):
    finished = QtCore.Signal()

    def __init__(self, widget: QtWidgets.QWidget) -> None:
        super().__init__()
        self.widget = widget

    def run(self) -> None:
        bots = get_bots()
        username = (
            self.widget.username_input.text().split('@')[0].replace('.', '_')
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
            'message': self.widget.message_text_edit.toPlainText(),
        }
        browser = create_browser_from_module(
            bot['website'],
            user_data_dir=bot['user_data_dir'],
        )
        if not browser.is_logged():
            browser.make_login(bot['username'], bot['password'])
        bots.append(bot)
        json.dump({'bots': bots}, open('.secrets.json', 'w'))
        self.finished.emit()
