from PySide6 import QtWidgets


class Button(QtWidgets.QPushButton):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setStyleSheet('background-color: #187bcd; color: white')


class HorizontalLayout(QtWidgets.QHBoxLayout):

    def __init__(
        self, label: QtWidgets.QLabel, input_widget: QtWidgets.QLineEdit
    ) -> None:
        super().__init__()
        self.addWidget(label, 1)
        self.addWidget(input_widget, 3)


class DirectoryDialog(QtWidgets.QHBoxLayout):

    def __init__(
        self, window: QtWidgets.QWidget, directory_input: QtWidgets.QLineEdit
    ) -> None:
        super().__init__()
        self.window = window
        self.directory_input = directory_input

        self.button = Button('Selecionar')
        self.button.clicked.connect(self.open_directory_dialog)

        self.addWidget(self.directory_input, 4)
        self.addWidget(self.button, 1)

    def open_directory_dialog(self) -> None:
        result = str(QtWidgets.QFileDialog.getExistingDirectory(
            self.window, 'Selecione uma pasta'
        ))
        self.directory_input.setText(result)
