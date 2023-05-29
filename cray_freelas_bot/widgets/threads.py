from time import sleep

from PySide6 import QtCore, QtWidgets

from cray_freelas_bot.common.project import (
    create_browser_from_module,
    get_bots,
)
from cray_freelas_bot.domain.models import Bot
from cray_freelas_bot.repositories.bot import BotRepository


class BrowserThread(QtCore.QThread):
    def run(self) -> None:
        while True:
            for bot in get_bots():
                bot.run()
            sleep(60)


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
        return Bot(
            username=self.widget.username_input.text(),
            password=self.widget.password_input.text(),
            browser_module=self.widget.WEBSITES[
                self.widget.website_combobox.currentText()
            ],
            category=self.widget.category_combobox.currentText(),
            report_folder=self.widget.report_folder_input.text(),
            user_data_dir=f'.{username}_user_data',
            message=self.widget.message_text_edit.toPlainText(),
        )
