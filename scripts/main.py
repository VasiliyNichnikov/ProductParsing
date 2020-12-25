"""
    Данный скрипт запускает парсинг с введенными параметрами
"""
from scripts.LeroyMerlin.ParsingPage import ParsingPage
from scripts.LeroyMerlin.ParsingAd import ParsingAd
from scripts.database.LeroyMerlin.ad_leroy_merlin import AdModelLeroyMerlin
from scripts.database import db_session
from threading import Thread
import pandas as pd
from time import sleep
import json
from PyQt5 import QtWidgets, QtGui
from scripts.interface import Ui_MainWindow, Ui_AddUrl
import sys

path_settings = '../files/settings.json'


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

        # Работа с кнопками
        self.UI.button_save.clicked.connect(self.__save_changes)
        self.UI.button_start.clicked.connect(self.__start_parser)
        self.UI.button_add_url.clicked.connect(self.__add_url)

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
        db_session.global_init(f'../files/database/{self.file_name}.db')

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

    # Запуск программы
    def __start_parser(self):
        self.__on_off_buttons(False)
        thread = Thread(target=self.__parser)
        thread.start()

    # Добавление ссылок
    def __add_url(self):
        dialog_add_url = Ui_AddUrl(self)
        dialog_add_url.exec_()
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
        self.__on_off_buttons(True)


app = QtWidgets.QApplication([])
application = Program()
application.show()

sys.exit(app.exec())

# name_bd = 'sample_2'
# # list_urls = ['https://leroymerlin.ru/search/?q=шкаф']
# list_urls = ['https://leroymerlin.ru/search/?q=шкаф',
#              'https://leroymerlin.ru/search/?q=стол',
#              'https://leroymerlin.ru/search/?q=лион&family=garderobnye-sistemy-panelnye-201709&suggest=true',
#              'https://leroymerlin.ru/search/?q=раковина',
#              'https://leroymerlin.ru/search/?q=зеркало&family=5a35c540-a696-11ea-b381-49b4680b1a6a&suggest=true']
# # number_threads = 3
#
# df = pd.DataFrame()

#
#
#
#     # print('------------------------------------------------')
#
#


# Работа с БД
# session = db_session.create_session()
#
# df['№'] = [i[0] for i in session.query(AdModelLeroyMerlin.ENTRY_ID).all()]
# df['Артикул'] = [' ' for i in session.query(AdModelLeroyMerlin.ENTRY_ID).all()]
# df['Название товара'] = [i[0] for i in session.query(AdModelLeroyMerlin.NAME).all()]
# df['Цена, руб.*'] = [i[0] for i in session.query(AdModelLeroyMerlin.PRICE).all()]
# # df['Коммерческий тип*'] = []
# # df['Штрихкод (Серийный номер / EAN)'] = []
# df['Вес в упаковке, г*'] = [i[0] for i in session.query(AdModelLeroyMerlin.WEIGHT).all()]
# df['Ширина упаковки, мм*'] = [i[0] for i in session.query(AdModelLeroyMerlin.WIDTH).all()]
# df['Высота упаковки, мм*'] = [i[0] for i in session.query(AdModelLeroyMerlin.HEIGHT).all()]
# # df['Длина упаковки, мм*'] = []
# df['Ссылка на главное фото*'] = [i[0] for i in session.query(AdModelLeroyMerlin.MAIN_PHOTO).all()]
# df['Ссылки на дополнительные фото'] = [i[0] for i in session.query(AdModelLeroyMerlin.ADDITIONAL_PHOTOS).all()]
# # df['Ссылки на фото 360'] = []
# # df['Ссылки на фото аннотаций'] = []
# df['Артикул фото'] = [i[0] for i in session.query(AdModelLeroyMerlin.PHOTO_ARTICLES).all()]
# df['Название модели*'] = [i[0] for i in session.query(AdModelLeroyMerlin.MODEL).all()]
# df['Тип*'] = [i[0] for i in session.query(AdModelLeroyMerlin.TYPE_MODEL).all()]
# # df['Условия хранения*'] = []
# # df['Минимальная температура*'] = []
# # df['Максимальная температура*'] = []
# # df['Срок годности в днях*'] = []
# df['Бренд*'] = [i[0] for i in session.query(AdModelLeroyMerlin.BRAND).all()]
# # df['Единиц в одном товаре*'] = []
# # df['Состав*'] = []
# # df['Вкус.'] = []
# df['Объем, л.'] = [i[0] for i in session.query(AdModelLeroyMerlin.VOLUME).all()]
# df['Описание'] = [i[0] for i in session.query(AdModelLeroyMerlin.DESCRIPTION).all()]
# df['Страна изготовитель'] = [i[0] for i in session.query(AdModelLeroyMerlin.MANUFACTURER).all()]
# df['Кол-во товара'] = [i[0] for i in session.query(AdModelLeroyMerlin.QUANTITY_GOODS).all()]
# df['Прямая ссылка на товар на сайте '] = [i[0] for i in session.query(AdModelLeroyMerlin.URL).all()]


# writer = pd.ExcelWriter(f'../files/excel spreadsheets/{name_bd}.xlsx', engine='xlsxwriter')
# workbook = writer.book
# df.to_excel(writer, sheet_name='Шаблон для поставщика', index=False)
#
# work_sheet = writer.sheets['Шаблон для поставщика']
#
# header_format_red = workbook.add_format({'fg_color': '#FF0000'})
# header_format_blue = workbook.add_format({'fg_color': '#CFE2F3'})
# header_format_yellow = workbook.add_format({'fg_color': '#FFD966'})
#
# work_sheet.set_column('A1', 10, cell_format=header_format_blue)  # Номер товара
# work_sheet.set_column('B1', 20, cell_format=header_format_red)  # Артикул товара
# work_sheet.set_column('C1', 30, cell_format=header_format_blue)  # Название товара
# work_sheet.set_column('D1', 20, cell_format=header_format_red)  # Цена товара
# work_sheet.set_column('E1', 20, cell_format=header_format_red)  # Вес в упаковке
# work_sheet.set_column('F1', 20, cell_format=header_format_red)  # Ширина упаковки
# work_sheet.set_column('G1', 20, cell_format=header_format_red)  # Высота упаковки
# work_sheet.set_column('H1', 100, cell_format=header_format_red)  # Ссылка на главное фото
# work_sheet.set_column('I1', 100, cell_format=header_format_blue)  # Ссылки на доп.фото
# work_sheet.set_column('J1', 30, cell_format=header_format_blue)  # Артикул фото
# work_sheet.set_column('K1', 30, cell_format=header_format_red)  # Название модели
# work_sheet.set_column('L1', 20, cell_format=header_format_red)  # Тип
# work_sheet.set_column('M1', 30, cell_format=header_format_red)  # Бренд
# work_sheet.set_column('N1', 10, cell_format=header_format_yellow)  # Объем
# work_sheet.set_column('O1', 30, cell_format=header_format_blue)  # Описание
# work_sheet.set_column('P1', 30, cell_format=header_format_blue)  # Страна изготовитель
# work_sheet.set_column('Q1', 100, cell_format=header_format_blue)  # Кол-во товара
# work_sheet.set_column('R1', 100, cell_format=header_format_red)  # Прямая ссылка на товар
#
# writer.save()
