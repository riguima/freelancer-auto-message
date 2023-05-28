import json

from PySide6 import QtCore, QtWidgets

from cray_freelas_bot.common.project import create_browser_from_module
from cray_freelas_bot.widgets.helpers import (
    Button,
    DirectoryDialog,
    HorizontalLayout,
)
from cray_freelas_bot.widgets.tables_models import BotTableModel
from cray_freelas_bot.widgets.threads import CreateBotThread


class BotsWindow(QtWidgets.QWidget):
    def __init__(self, return_window: QtWidgets.QWidget) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px;')
        self.setWindowTitle('Bots')

        self.return_window = return_window

        self.create_bot_thread = CreateBotThread(self)

        self.message_box = QtWidgets.QMessageBox()
        self.message_box.setWindowTitle('Aviso')

        self.username_label = QtWidgets.QLabel('Usuario/Email:')
        self.username_input = QtWidgets.QLineEdit()
        self.username_layout = HorizontalLayout(
            self.username_label,
            self.username_input,
        )

        self.password_label = QtWidgets.QLabel('Senha:')
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_layout = HorizontalLayout(
            self.password_label,
            self.password_input,
        )

        self.WEBSITES = {
            '99Freelas': 'nine_nine_freelas',
            'Workana': 'workana',
        }

        self.website_label = QtWidgets.QLabel('Plataforma:')
        self.website_combobox = QtWidgets.QComboBox()
        self.website_combobox.addItems(list(self.WEBSITES.keys()))
        self.website_combobox.currentIndexChanged.connect(self.set_categories)
        self.website_layout = HorizontalLayout(
            self.website_label,
            self.website_combobox,
        )

        self.category_label = QtWidgets.QLabel('Categoria: ')
        self.category_combobox = QtWidgets.QComboBox()
        self.category_layout = HorizontalLayout(
            self.category_label,
            self.category_combobox,
        )
        self.set_categories()

        self.report_folder_label = QtWidgets.QLabel('Pasta do relatório:')
        self.report_folder_input = QtWidgets.QLineEdit()
        self.report_folder_dialog = DirectoryDialog(
            self,
            self.report_folder_input,
        )
        self.report_folder_layout = QtWidgets.QVBoxLayout()
        self.report_folder_layout.addWidget(self.report_folder_label)
        self.report_folder_layout.addLayout(self.report_folder_dialog)

        self.message_label = QtWidgets.QLabel('Mensagem:')
        self.message_text_edit = QtWidgets.QTextEdit()

        self.create_bot_button = Button('Adicionar bot')
        self.create_bot_button.clicked.connect(self.create_bot)

        self.bot_table = QtWidgets.QTableView()
        self.update_bot_table_data()
        self.bot_table.setColumnWidth(0, 300)
        self.bot_table.setColumnWidth(1, 150)
        self.bot_table.setColumnWidth(2, 150)
        self.bot_table.setColumnWidth(3, 300)

        self.remove_bot_button = Button('Remover bot')
        self.remove_bot_button.clicked.connect(self.remove_bot)

        self.return_button = Button('Voltar')
        self.return_button.clicked.connect(self.return_to_window)

        self.inputs_layout = QtWidgets.QVBoxLayout()
        self.inputs_layout.addLayout(self.username_layout)
        self.inputs_layout.addLayout(self.password_layout)
        self.inputs_layout.addLayout(self.website_layout)
        self.inputs_layout.addLayout(self.category_layout)
        self.inputs_layout.addLayout(self.report_folder_layout)
        self.inputs_layout.addWidget(self.message_label)
        self.inputs_layout.addWidget(self.message_text_edit)
        self.inputs_layout.addWidget(self.create_bot_button)
        self.inputs_layout.addWidget(self.return_button)

        self.bot_table_layout = QtWidgets.QVBoxLayout()
        self.bot_table_layout.addWidget(self.bot_table)
        self.bot_table_layout.addWidget(self.remove_bot_button)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addLayout(self.inputs_layout)
        self.layout.addLayout(self.bot_table_layout)

    def update_bot_table_data(self) -> None:
        try:
            bots = json.load(open('.secrets.json'))['bots']
        except FileNotFoundError:
            bots = []
            json.dump({'bots': []}, open('.secrets.json', 'w'))
        data = [
            [
                b['username'],
                b['password'],
                list(self.WEBSITES.keys())[
                    list(self.WEBSITES.values()).index(b['website'])
                ],
                b['category'],
                b['report_folder'],
            ]
            for b in bots
        ]
        headers = [
            'Usuario/Email',
            'Senha',
            'Plataforma',
            'Categoria',
            'Pasta do relatório',
        ]
        if not data:
            data = [''] * len(headers)
        self.bot_table.setModel(BotTableModel(data, headers))

    @QtCore.Slot()
    def return_to_window(self) -> None:
        self.return_window.show()
        self.close()

    @QtCore.Slot()
    def set_categories(self) -> None:
        self.category_combobox.clear()
        browser = create_browser_from_module(
            self.WEBSITES[self.website_combobox.currentText()],
            user_data_dir='default_user_data',
            visible=False,
        )
        self.category_combobox.addItems(browser.get_all_categories())
        browser.driver.close()

    @QtCore.Slot()
    def create_bot(self) -> None:
        self.message_box.setText('Faça o login')
        self.message_box.show()
        self.create_bot_thread.start()
        self.create_bot_thread.finished.connect(self.show_created_bot_message)

    @QtCore.Slot()
    def show_created_bot_message(self) -> None:
        self.message_box.setText('Bot adicionado')
        self.message_box.show()
        self.clear_inputs()
        self.update_bot_table_data()

    @QtCore.Slot()
    def remove_bot(self) -> None:
        for index in self.bot_table.selectedIndexes():
            data = json.load(open('.secrets.json'))
            data['bots'].pop(index.row())
            json.dump(data, open('.secrets.json', 'w'))
        self.update_bot_table_data()

    def clear_inputs(self) -> None:
        widgets_inputs = [
            self.username_input,
            self.password_input,
            self.report_folder_input,
        ]
        for widget_input in widgets_inputs:
            widget_input.setText('')