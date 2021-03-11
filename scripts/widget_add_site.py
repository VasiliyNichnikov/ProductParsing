from PyQt5 import QtWidgets, QtGui
from add_site_interface import Ui_MainWindow


class WidgetUrlItem(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WidgetUrlItem, self).__init__(parent)
        self.horizontal_box_layout = QtWidgets.QHBoxLayout()
        self.line_url = QtWidgets.QLineEdit()
        self.line_url.setPlaceholderText('Введите url адрес')
        self.button_remove = QtWidgets.QPushButton('Удалить')
        self.horizontal_box_layout.addWidget(self.line_url)
        self.horizontal_box_layout.addWidget(self.button_remove)
        self.setLayout(self.horizontal_box_layout)

    def select_url(self, url):
        self.line_url.setText(url)


class ButtonAddItem(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ButtonAddItem, self).__init__(parent)
        self.button_box_layout = QtWidgets.QVBoxLayout()
        self.button_add = QtWidgets.QPushButton("Добавить сайт")
        self.button_box_layout.addWidget(self.button_add)
        self.setLayout(self.button_box_layout)
        # self.button_add.clicked.connect(self.open_widget_add_site)
        # self.window_add_site_open = False


class AddSiteProgram(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AddSiteProgram, self).__init__(parent)
        self.UI = Ui_MainWindow()
        self.parent = parent
        self.UI.setupUi(self)
        self.UI.LineEditNameExcelFile.setPlaceholderText('Введите название файла excel')
        self.setWindowTitle('Добавление сайта')
        # Список всех ссылок
        self.list_widgets_item_urls = []
        self.save_block = False
        # Кнопка, отвечающая за добавление нового элемента
        item = self.add_item(ButtonAddItem())[0]
        # Нажатие на кнопку "Сохранить"
        self.UI.BushButtonSave.clicked.connect(self.get_info_values)
        item.button_add.clicked.connect(self.add_new_url)

    # Добавление элемента в список
    def add_item(self, class_item):
        list_widget_item = QtWidgets.QListWidgetItem(self.UI.ListWidgetListLinks)
        list_widget_item.setSizeHint(class_item.sizeHint())
        self.UI.ListWidgetListLinks.addItem(list_widget_item)
        self.UI.ListWidgetListLinks.setItemWidget(list_widget_item, class_item)
        return class_item, list_widget_item

    # Добавление нового элемента в список ссылок
    def add_new_url(self):
        item, list_widget_item = self.add_item(WidgetUrlItem(self))
        self.list_widgets_item_urls.append(list_widget_item)
        item.button_remove.clicked.connect(self.remove_url)

    # Добавление новой ссылки в список, а также обозначение url
    def add_new_url_and_take_url(self, url):
        item, list_widget_item = self.add_item(WidgetUrlItem(self))
        self.list_widgets_item_urls.append(list_widget_item)
        item.button_remove.clicked.connect(self.remove_url)
        item.select_url(url)

    # Удаление элемента из списка ссылок
    def remove_url(self):
        for item in self.list_widgets_item_urls:
            widget = self.UI.ListWidgetListLinks.itemWidget(item)
            if widget.button_remove == self.sender():
                self.list_widgets_item_urls.remove(item)
                index_remove_item = self.UI.ListWidgetListLinks.row(item)
                self.UI.ListWidgetListLinks.takeItem(index_remove_item)
                break

    # Передача параметров в функцию основной программы
    def get_info_values(self) -> None:
        dict_values = {'ComboBoxSite': self.UI.ComboBoxSite.currentText(),
                       'SpinBoxDelayError': self.UI.SpinBoxDelayError.value(),
                       'SpinBoxCaptcha': self.UI.SpinBoxCaptcha.value(),
                       'ComboBoxBypassingCaptchas': self.UI.ComboBoxBypassingCaptchas.currentText(),
                       'LineEditNameExcelFile': self.UI.LineEditNameExcelFile.text(),
                       'ListWidgetListLinks': [self.UI.ListWidgetListLinks.itemWidget(item).line_url.text() for item in
                                               self.list_widgets_item_urls
                                               if self.UI.ListWidgetListLinks.itemWidget(item).line_url.text() != '']}

        if self.parent is not None:
            self.parent.transfer_values(dict_values, self.save_block)
        else:
            # FIXME: Должна быть ошибка
            print('error, нет родителя')
        self.close()

    # Загрузка данных в блок
    def load_values(self, dict_values):
        self.save_block = True
        self.UI.ComboBoxSite.setCurrentText(dict_values['ComboBoxSite'])
        self.UI.SpinBoxDelayError.setValue(dict_values['SpinBoxDelayError'])
        self.UI.SpinBoxCaptcha.setValue(dict_values['SpinBoxCaptcha'])
        self.UI.ComboBoxBypassingCaptchas.setCurrentText(dict_values['ComboBoxBypassingCaptchas'])
        self.UI.LineEditNameExcelFile.setText(dict_values['LineEditNameExcelFile'])
        for url in dict_values['ListWidgetListLinks']:
            self.add_new_url_and_take_url(url)

    # Закрытие окна
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.parent is not None:
            self.parent.window_add_site_open = False
        else:
            # FIXME: Должна быть ошибка
            print('error, нет родителя')
