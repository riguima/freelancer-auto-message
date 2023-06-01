from time import sleep

from pathlib import Path
from PySide6 import QtCore, QtWidgets
from selenium.common.exceptions import TimeoutException

from cray_freelas_bot.common.browser import create_browser_from_module
from cray_freelas_bot.common.project import to_excel
from cray_freelas_bot.domain.browser import IBrowser
from cray_freelas_bot.domain.bot import Bot
from cray_freelas_bot.domain.message_sent import MessageSent
from cray_freelas_bot.exceptions.project import ProjectError
from cray_freelas_bot.repositories.bot import BotRepository
from cray_freelas_bot.repositories.message_sent import MessageSentRepository


class BrowserThread(QtCore.QThread):
    def run(self) -> None:
        bots = BotRepository().all()
        while True:
            for bot in bots:
                self.run_bot(bot)
            sleep(60)

    def run_bot(self, bot: Bot) -> None:
        browser = create_browser_from_module(bot.browser_module)
        if not browser.is_logged():
            browser.make_login(bot.username, bot.password)
        breakpoint()
        for url in self.get_valid_projects_urls(bot, browser):
            try:
                self.send_message(bot, browser, url)
            except TimeoutException:
                continue

    def get_valid_projects_urls(
        self, bot: Bot, browser: IBrowser
    ) -> list[str]:
        result = []
        urls = [m.url for m in MessageSentRepository().all()]
        for url in browser.get_projects_urls(bot.category):
            if url not in urls:
                try:
                    browser.get_project(url)
                except ProjectError:
                    continue
                result.append(url)
        return result

    def send_message(
        self, bot: Bot, browser: IBrowser, project_url: str
    ) -> None:
        text = browser.format_message(
            bot.message, browser.get_project(project_url)
        )
        report_path = Path(bot.report_folder) / 'result.xlsx'
        message = browser.send_message(project_url, text)
        to_excel([message], report_path)
        MessageSentRepository().create(MessageSent(url=project_url))


class CreateBotThread(QtCore.QThread):
    finished = QtCore.Signal()

    def __init__(self, widget: QtWidgets.QWidget) -> None:
        super().__init__()
        self.widget = widget

    def run(self) -> None:
        bot = self.create_bot()
        BotRepository().create(bot)
        self.finished.emit()

    def create_bot(self) -> dict:
        username = (
            self.widget.username_input.text().split('@')[0].replace('.', '_')
        )
        browsers_modules = ['nine_nine_freelas', 'workana']
        return Bot(
            username=self.widget.username_input.text(),
            password=self.widget.password_input.text(),
            browser_module=browsers_modules[
                self.widget.browser_module_combobox.currentIndex()
            ],
            category=self.widget.category_combobox.currentText(),
            report_folder=self.widget.report_folder_input.text(),
            user_data_dir=f'.{username}_user_data',
            message=self.widget.message_text_edit.toPlainText(),
        )
