from time import sleep

from PySide6 import QtCore, QtWidgets

from cray_freelas_bot.common.browser import create_browser_from_module
from cray_freelas_bot.domain.bot import Bot
from cray_freelas_bot.repositories.bot import BotRepository


class BrowserThread(QtCore.QThread):
    def run(self) -> None:
        bots = BotRepository().all()
        while True:
            for bot in bots:
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
        browsers_modules = ['nine_nine_freelas', 'workana']
        return Bot(
            username=self.widget.username_input.text(),
            password=self.widget.password_input.text(),
            browser=create_browser_from_module(
                browsers_modules[
                    self.widget.browser_module_combobox.currentIndex()
                ],
                user_data_dir=f'.{username}_user_data',
                visible=False,
            ),
            category=self.widget.category_combobox.currentText(),
            report_folder=self.widget.report_folder_input.text(),
            user_data_dir=f'.{username}_user_data',
            message=self.widget.message_text_edit.toPlainText(),
        )
