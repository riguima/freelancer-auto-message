import json

from PySide6 import QtCore, QtWidgets

from cray_freelas_bot.widgets.helpers import (
    Button,
    DirectoryDialog,
    HorizontalLayout,
)


class ConfigurationWindow(QtWidgets.QWidget):
    def __init__(self, return_window: QtWidgets.QWidget) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px;')
        self.setFixedSize(500, 250)
        self.setWindowTitle('Tela Principal')

        self.return_window = return_window

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
        self.password_layou = HorizontalLayout(
            self.password_label,
            self.password_input,
        )

        self.browser_label = QtWidgets.QLabel('Navegador:')
        self.browser_combobox = QtWidgets.QComboBox()
        self.browser_layout = HorizontalLayout(
            self.browser_label,
            self.browser_combobox,
        )

        self.report_folder_label = QtWidgets.QLabel('Pasta do relatório:')
        self.report_folder_input = QtWidgets.QLineEdit()
        self.report_folder_dialog = DirectoryDialog(
            self,
            self.report_folder_input,
        )
        self.report_folder_layout = QtWidgets.QVBoxLayout()
        self.report_folder_layout.addWidget(self.report_folder_label)
        self.report_folder_layout.addLayout(self.report_folder_dialog)

        self.add_browser_button = Button('Adicionar')
        self.add_browser_button.clicked.connect(self.save_configuration)

        self.return_button = Button('Voltar')
        self.return_button.clicked.connect(self.return_to_window)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.username_layout)
        self.layout.addLayout(self.password_layout)
        self.layout.addLayout(self.browser_layout)
        self.layout.addLayout(self.report_folder_layout)
        self.layout.addWidget(self.add_browser_button)
        self.layout.addWidget(self.return_button)

    @QtCore.Slot()
    def return_to_window(self) -> None:
        self.return_window.show()
        self.close()

    @QtCore.Slot()
    def add_browser(self) -> None:
        data = json.load(open('.secrets.json'))
        data['accounts'].update({
            'username': self.username_input.text(),
            'password': self.password_input.text(),
            'browser': self.browser_combobox.currentText(),
            'report_folder': self.report_folder_input.text(),
        })
        self.message_box.setText('Configuração salva')
        self.message_box.show()
