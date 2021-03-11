from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout


class WidgetItem(QWidget):
    def __init__(self, parent=None):
        super(WidgetItem, self).__init__(parent)
        self.horizontal_box_layout = QHBoxLayout()
        self.name_widget = QLabel('Название Блока')
        self.button_remove = QPushButton('Удалить')
        self.button_edit = QPushButton('Редактировать')
        self.horizontal_box_layout.addWidget(self.name_widget)
        self.horizontal_box_layout.addWidget(self.button_edit)
        self.horizontal_box_layout.addWidget(self.button_remove)
        self.name_excel_table = ''
        self.setLayout(self.horizontal_box_layout)

    # Выбор имени элемента
    def select_name_widget(self, text):
        self.name_widget.setText(text)


class ButtonAddItem(QWidget):
    def __init__(self, parent=None):
        super(ButtonAddItem, self).__init__(parent)
        self.button_box_layout = QHBoxLayout()
        self.button_add = QPushButton("Добавить сайт")
        self.button_box_layout.addWidget(self.button_add)
        self.setLayout(self.button_box_layout)
        # self.button_add.clicked.connect(self.open_widget_add_site)
        # self.window_add_site_open = False
        # self.parent = parent


