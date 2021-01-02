"""
    Данный скрипт запускает парсинг с введенными параметрами
"""
from scripts.LeroyMerlin.ParsingPage import ParsingPage
from scripts.LeroyMerlin.ParsingAd import ParsingAd
from scripts.database.LeroyMerlin.ad_leroy_merlin import AdModelLeroyMerlin
from scripts.database import db_session
from threading import Thread
import os
import pandas as pd
from time import sleep
import json
from PyQt5 import QtWidgets, QtGui, QtCore
from scripts.interface import Ui_MainWindow, Ui_AddUrl
import sys

path_settings = '../files/settings.json'
path_db = '../files/database/'
path_excel = '../files/excel spreadsheets/'


class Program(QtWidgets.QMainWindow):
    def __init__(self):
        super(Program, self).__init__()
        self.UI = Ui_MainWindow()
        self.UI.setupUi(self)

        self.delay_after_error = 0
        self.delay_between_pages = 0
        self.delay_between_ads = 0
        self.working_with_captchas = 'None'
        self.file_name = 'None'
        self.list_links = []

        # Для работы с excel таблицей
        self.df = pd.DataFrame()

        # Выбранный элемент в списке
        self.selected_item_index = None

        # Работа с кнопками
        self.UI.button_save.clicked.connect(self.__save_changes)
        self.UI.button_start.clicked.connect(self.__start_parser)
        self.UI.button_add_url.clicked.connect(self.__add_url)
        # Выделение item из списка
        self.UI.listWidget_list_links.itemSelectionChanged.connect(self.__select_url_in_list)

        # Получаем данные из json файла
        with open(path_settings, encoding='utf-8') as read_file:
            data = json.load(read_file)
            # Задержка после ошибки
            self.delay_after_error = data['delay_after_error']
            # Задержка между страницами
            self.delay_between_pages = data['delay_between_pages']
            # Задержка между объявлениями
            self.delay_between_ads = data['delay_between_ads']
            # Работа с капчами
            self.working_with_captchas = data['working_with_captchas']
            # Название получившегося файла
            self.file_name = data['file_name']
            # Список ссылок
            self.list_links = data['list_links']

            # Перенос параметров в интерфейс
            self.UI.spinBox_delay_after_error.setValue(self.delay_after_error)
            self.UI.spinBox_delay_between_pages.setValue(self.delay_between_pages)
            self.UI.spinBox_delay_between_ads.setValue(self.delay_between_ads)
            self.UI.lineEdit_file_name.setText(self.file_name)
            self.UI.listWidget_list_links.clear()

            for item in self.list_links:
                self.UI.listWidget_list_links.addItem(item)

        # Инициализация БД
        db_session.global_init(path_db + f'{self.file_name}.db')

    # Проверка нажатия кнопок на клавиатуре
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Backspace and self.selected_item_index is not None:
            self.UI.listWidget_list_links.takeItem(self.selected_item_index)

    # Парсинг объявления
    def __parsing_ad(self, link):
        data_ad = ParsingAd(link, delay_after_error=self.delay_after_error)
        info = data_ad.get_info()

        session = db_session.create_session()
        ad = AdModelLeroyMerlin(
            NAME=f"{info['NAME']}",
            PRICE=f"{info['PRICE']}",
            WEIGHT=f"{info['WEIGHT']}",
            WIDTH=f"{info['WIDTH']}",
            HEIGHT=f"{info['HEIGHT']}",
            MODEL=f"{info['MODEL']}",
            TYPE_MODEL=f"{info['TYPE_MODEL']}",
            BRAND=f"{info['BRAND']}",
            MANUFACTURER=f"{info['MANUFACTURER']}",
            VOLUME=f"{info['VOLUME']}",
            MAIN_PHOTO=f"{info['MAIN_PHOTO']}",
            ADDITIONAL_PHOTOS=f"{info['ADDITIONAL_PHOTOS']}",
            PHOTO_ARTICLES=f"{info['PHOTO_ARTICLES']}",
            DESCRIPTION=f"{info['DESCRIPTION']}",
            QUANTITY_GOODS=f"{info['QUANTITY_GOODS']}",
            URL=f"{info['URL']}"
        )
        session.add(ad)
        session.commit()
        sleep(self.delay_between_ads)

    # Сохранение настроек в json файл
    def __save_changes(self):
        self.delay_after_error = self.UI.spinBox_delay_after_error.value()
        self.delay_between_pages = self.UI.spinBox_delay_between_pages.value()
        self.delay_between_ads = self.UI.spinBox_delay_between_ads.value()
        self.working_with_captchas = 'None'
        self.file_name = self.UI.lineEdit_file_name.text()
        self.list_links = [self.UI.listWidget_list_links.item(i).text() for i in
                           range(self.UI.listWidget_list_links.count())]

        dict_json = {
            'delay_after_error': self.delay_after_error,
            'delay_between_pages': self.delay_between_pages,
            'delay_between_ads': self.delay_between_ads,
            'working_with_captchas': 'None',
            'file_name': self.file_name,
            'list_links': self.list_links
        }
        with open(path_settings, 'w', encoding='utf-8') as write_file:
            json.dump(dict_json, write_file)

    # Включение/Выключение кнопок
    def __on_off_buttons(self, condition):
        self.UI.button_start.setEnabled(condition)
        self.UI.button_save.setEnabled(condition)
        self.UI.button_add_url.setEnabled(condition)

    # Выбор ссылки из списка
    def __select_url_in_list(self):
        # print(self.UI.listWidget_list_links.currentRow(self.selected_item))
        if self.UI.listWidget_list_links.count() > 0:
            for i in range(self.UI.listWidget_list_links.count()):
                if self.UI.listWidget_list_links.item(i) == self.UI.listWidget_list_links.selectedItems()[0]:
                    self.selected_item_index = i
                    break

                # Запуск программы

    def __start_parser(self):
        self.__on_off_buttons(False)
        thread = Thread(target=self.__parser)
        thread.start()

    # Добавление ссылок
    def __add_url(self):
        dialog_add_url = Ui_AddUrl(self)
        dialog_add_url.exec_()
        if dialog_add_url.ready_url.replace(' ', '') != '':
            self.UI.listWidget_list_links.addItem(dialog_add_url.ready_url)

    # Парсер
    def __parser(self):
        for url in self.list_links:
            parsing_page = ParsingPage(url=url, start_page=1, delay_after_error=self.delay_after_error)
            while parsing_page.page <= parsing_page.max_page:
                print(f'Страница - {parsing_page.page}; Максимальная страница - {parsing_page.max_page}')
                list_links = parsing_page.get_urls()

                for link in list_links:
                    self.__parsing_ad(link)
                parsing_page.page += 1
                sleep(self.delay_between_pages)
        self.__translation_to_excel_table()
        self.__on_off_buttons(True)

    # Перевод из .db в excel
    def __translation_to_excel_table(self):
        session = db_session.create_session()

        self.df['№'] = [i[0] for i in session.query(AdModelLeroyMerlin.ENTRY_ID).all()]
        self.df['Артикул'] = [' ' for i in session.query(AdModelLeroyMerlin.ENTRY_ID).all()]
        self.df['Название товара'] = [i[0] for i in session.query(AdModelLeroyMerlin.NAME).all()]
        self.df['Цена, руб.*'] = [i[0] for i in session.query(AdModelLeroyMerlin.PRICE).all()]
        self.df['Вес в упаковке, г*'] = [i[0] for i in session.query(AdModelLeroyMerlin.WEIGHT).all()]
        self.df['Ширина упаковки, мм*'] = [i[0] for i in session.query(AdModelLeroyMerlin.WIDTH).all()]
        self.df['Высота упаковки, мм*'] = [i[0] for i in session.query(AdModelLeroyMerlin.HEIGHT).all()]
        self.df['Ссылка на главное фото*'] = [i[0] for i in session.query(AdModelLeroyMerlin.MAIN_PHOTO).all()]
        self.df['Ссылки на дополнительные фото'] = [i[0] for i in
                                                    session.query(AdModelLeroyMerlin.ADDITIONAL_PHOTOS).all()]
        self.df['Артикул фото'] = [i[0] for i in session.query(AdModelLeroyMerlin.PHOTO_ARTICLES).all()]
        self.df['Название модели*'] = [i[0] for i in session.query(AdModelLeroyMerlin.MODEL).all()]
        self.df['Тип*'] = [i[0] for i in session.query(AdModelLeroyMerlin.TYPE_MODEL).all()]
        self.df['Бренд*'] = [i[0] for i in session.query(AdModelLeroyMerlin.BRAND).all()]
        self.df['Объем, л.'] = [i[0] for i in session.query(AdModelLeroyMerlin.VOLUME).all()]
        self.df['Описание'] = [i[0] for i in session.query(AdModelLeroyMerlin.DESCRIPTION).all()]
        self.df['Страна изготовитель'] = [i[0] for i in session.query(AdModelLeroyMerlin.MANUFACTURER).all()]
        self.df['Кол-во товара'] = [i[0] for i in session.query(AdModelLeroyMerlin.QUANTITY_GOODS).all()]
        self.df['Прямая ссылка на товар на сайте '] = [i[0] for i in session.query(AdModelLeroyMerlin.URL).all()]

        writer = pd.ExcelWriter(path_excel + f'{self.file_name}', engine='xlsxwriter',
                                options={'strings_to_urls': False})
        workbook = writer.book
        self.df.to_excel(writer, sheet_name='Шаблон для поставщика', index=False)
        worksheet = writer.sheets['Шаблон для поставщика']

        header_format_red = workbook.add_format({'text_wrap': True,
                                                 'valign': 'top',
                                                 'fg_color': '#FF0000',
                                                 'border': 1})

        header_format_blue = workbook.add_format({'text_wrap': True,
                                                  'valign': 'top',
                                                  'fg_color': '#CFE2F3',
                                                  'border': 1})

        header_format_yellow = workbook.add_format({'text_wrap': True,
                                                    'valign': 'top',
                                                    'fg_color': '#FFD966',
                                                    'border': 1})

        worksheet.set_column('A:A', 10)  # Номер товара
        worksheet.set_column('B:B', 20)  # Артикул товара
        worksheet.set_column('C:C', 30)  # Название товара
        worksheet.set_column('D:D', 20)  # Цена товара
        worksheet.set_column('E:E', 20)  # Вес в упаковке
        worksheet.set_column('F:F', 20)  # Ширина упаковки
        worksheet.set_column('G:G', 20)  # Высота упаковки
        worksheet.set_column('H:H', 100)  # Ссылка на главное фото
        worksheet.set_column('I:I', 100)  # Ссылки на доп.фото
        worksheet.set_column('J:J', 30)  # Артикул фото
        worksheet.set_column('K:K', 30)  # Название модели
        worksheet.set_column('L:L', 20)  # Тип
        worksheet.set_column('M:M', 30)  # Бренд
        worksheet.set_column('N:N', 10)  # Объем
        worksheet.set_column('O:O', 30)  # Описание
        worksheet.set_column('P:P', 30)  # Страна изготовитель
        worksheet.set_column('Q:Q', 100)  # Кол-во товара
        worksheet.set_column('R:R', 100)  # Прямая ссылка на товар

        for col_num, value in enumerate(self.df.columns.values):
            if value in ['№', 'Ссылки на дополнительные фото', 'Артикул фото', 'Описание', 'Страна изготовитель',
                         'Кол-во товара']:
                worksheet.write(0, col_num, value, header_format_blue)
            elif value in ['Объем, л.']:
                worksheet.write(0, col_num, value, header_format_yellow)
            else:
                worksheet.write(0, col_num, value, header_format_red)

        os.remove(path_db + f'{self.file_name}.db')
        writer.save()


app = QtWidgets.QApplication([])
application = Program()
application.show()

sys.exit(app.exec())
