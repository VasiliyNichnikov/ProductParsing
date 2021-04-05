"""
    Данный скрипт запускает парсинг с введенными параметрами
"""
from LeroyMerlin.parsing_page import ParsingPage
from basic_parameters import NAME_SITE, DELAY_ERROR, DELAY_AD, CAPTCHA, NAME_EXCEL_TABLE, LINKS
from LeroyMerlin.parsing_ad import ParsingAd
from database.LeroyMerlin.ad_leroy_merlin import AdModelLeroyMerlin
from database import db_session
from errors import ErrorInformationPageNotFound
from widget_add_site import AddSiteProgram
from database.Program.site import Site
from database.Program.links import Link
import os
import pandas as pd
from time import sleep
import json
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem
from item_site import WidgetItem, ButtonAddItem
# from interface import Ui_MainWindow, Ui_AddUrl
from new_interface import Ui_MainWindow
import sys

# Путь до настроек
path_settings = '../files/settings.json'
# Путь до БД
path_db = '../files/database/program.db'
# Путь до Excel таблицы
path_excel = '../files/excel spreadsheets/'


class Program(QtWidgets.QMainWindow):

    delay_after_error = 0
    delay_between_pages = 0
    delay_between_ads = 0
    working_with_captchas = 'None'
    file_name = 'None'
    list_links = []
    window_opened = False
    widgets_sites = []

    def __init__(self):
        super(Program, self).__init__()
        self.UI = Ui_MainWindow()
        # Для работы с excel таблицей
        self.df = pd.DataFrame()

        # Инициализация БД
        db_session.global_init(path_db)

        self.load_interface()
        self.connect_buttons()
        self.load_data_db_interface()

    def load_interface(self):
        self.UI.setupUi(self)
        self.setWindowTitle('Парсер сайтов')

    def connect_buttons(self):
        button_add_item = self.add_item_button(ButtonAddItem())
        button_add_item.button_add.clicked.connect(self.open_widget_add_site)

    # Добавление элемента кнопки в список
    def add_item_button(self, class_item) -> ButtonAddItem:
        list_widget_item = QListWidgetItem(self.UI.ListWidget)
        list_widget_item.setSizeHint(class_item.sizeHint())
        self.UI.ListWidget.addItem(list_widget_item)
        self.UI.ListWidget.setItemWidget(list_widget_item, class_item)
        return class_item

    # Добавление элемента виджета в список
    def add_item_widget(self, class_item) -> (WidgetItem, QListWidgetItem):
        list_widget_item = QListWidgetItem(self.UI.ListWidget)
        list_widget_item.setSizeHint(class_item.sizeHint())
        self.UI.ListWidget.addItem(list_widget_item)
        self.UI.ListWidget.setItemWidget(list_widget_item, class_item)
        return class_item, list_widget_item

    # Передача параметров для добавление блоков сайтов
    def transfer_values(self, values, save_block=False) -> None:
        self.window_opened = False
        if save_block is False:
            self.save_data_db(values)
            self.add_block_to_list(values)
        else:
            self.edit_data_db(values)

    # Добавление блоков в список
    def add_block_to_list(self, values):
        label = values[NAME_SITE] + '-' + values[NAME_EXCEL_TABLE]
        item_widget, list_widget_item = self.add_item_widget(WidgetItem())
        item_widget.select_name_widget(label)
        item_widget.name_excel_table = values[NAME_EXCEL_TABLE]
        self.widgets_sites.append(list_widget_item)
        # Действие при нажатии на кнопку "Редактировать"
        item_widget.button_edit.clicked.connect(self.edit_widget_site)
        # Дейсвтие при нажатии на кнопку "Удалить"
        item_widget.button_remove.clicked.connect(self.remove_site)

    # Удаление элемента из списка ссылок
    def remove_site(self):
        for item in self.widgets_sites:
            widget = self.UI.ListWidget.itemWidget(item)
            if widget.button_remove == self.sender():
                index_remove_item = self.UI.ListWidget.row(item)
                session = db_session.create_session()
                site = session.query(Site).filter(Site.NAME_EXCEL_TABLE == widget.name_excel_table).first()
                session.delete(site)
                session.commit()
                self.widgets_sites.remove(item)
                self.UI.ListWidget.takeItem(index_remove_item)
                break

    # Открытие окна для добавления нового блога
    def open_widget_add_site(self) -> None:
        if not self.window_opened:
            self.window_opened = True
            widget_add_site = AddSiteProgram(self)
            widget_add_site.show()

    # Редактирование блока
    def edit_widget_site(self):
        if not self.window_opened:
            site = None

            for item in self.widgets_sites:
                widget = self.UI.ListWidget.itemWidget(item)
                if widget.button_edit == self.sender():
                    session = db_session.create_session()
                    site = session.query(Site).filter(Site.NAME_EXCEL_TABLE == widget.name_excel_table).first()
                    break

            if site is not None:
                self.window_opened = True
                widget = AddSiteProgram(self)
                widget.load_values({
                    NAME_SITE: site.NAME_SITE,
                    DELAY_ERROR: site.DELAY_ERROR,
                    DELAY_AD: site.DELAY_AD,
                    CAPTCHA: site.CAPTCHA,
                    NAME_EXCEL_TABLE: site.NAME_EXCEL_TABLE,
                    LINKS: [link.LINK for link in site.LINKS]
                })
                widget.id = site.ID
                widget.show()
            else:
                # FIXME: Ошибка, если сайт не найден
                pass

    def edit_data_db(self, values):
        session = db_session.create_session()
        site = session.query(Site).filter(Site.ID == values['ID']).first()
        if site is not None:
            site.NAME_SITE = values[NAME_SITE]
            site.DELAY_ERROR = values[DELAY_ERROR]
            site.DELAY_AD = values[DELAY_AD]
            site.CAPTCHA = values[CAPTCHA]
            site.NAME_EXCEL_TABLE = values[NAME_EXCEL_TABLE]

            for link in values[LINKS]:
                link_db = Link(LINK=link)
                site.LINKS.append(link_db)
            session.commit()
        else:
            # FIXME: Должна быть ошибка
            pass

    # Сохранение информации в БД
    @staticmethod
    def save_data_db(values) -> None:
        session = db_session.create_session()
        site = Site(
            NAME_SITE=values[NAME_SITE],
            DELAY_ERROR=int(values[DELAY_ERROR]),
            DELAY_AD=int(values[DELAY_AD]),
            CAPTCHA=values[CAPTCHA],
            NAME_EXCEL_TABLE=values[NAME_EXCEL_TABLE]
        )
        session.add(site)
        for link in values[LINKS]:
            link_db = Link(LINK=link)
            site.LINKS.append(link_db)
        session.commit()

    # Загрузка информации из БД в интерфейс
    def load_data_db_interface(self):
        session = db_session.create_session()
        sites = session.query(Site).all()
        for site in sites:
            dict_values = {
                NAME_SITE: site.NAME_SITE,
                DELAY_ERROR: site.DELAY_ERROR,
                DELAY_AD: site.DELAY_AD,
                CAPTCHA: site.CAPTCHA,
                NAME_EXCEL_TABLE: site.NAME_EXCEL_TABLE,
                LINKS: [link.LINK for link in site.LINKS]
            }
            self.add_block_to_list(dict_values)

    # Парсинг объявления
    def __parsing_ad(self, link):
        for i in range(10):
            try:
                data_ad = ParsingAd(link, delay_after_error=self.delay_after_error, path_images='../files/photos')
                info = data_ad.get_info()
                print(f'Получение информации из ссылки - {info}')

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
                    OTHER=f"{info['OTHER']}",
                    URL=f"{info['URL']}"
                )
                session.add(ad)
                session.commit()
                sleep(self.delay_between_ads)
                break
            except ErrorInformationPageNotFound as e:
                print('Ошибка %s' % e)

    # Показать QMessageBox
    def __show_QMessageBox(self):
        QMessageBox.information(self, 'Работа завершена', 'Парсер завершил свою работу', QMessageBox.Ok)

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
        self.df['Дополнительная информация'] = [i[0] for i in session.query(AdModelLeroyMerlin.OTHER).all()]

        print(path_excel + f'{self.file_name}')
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
        worksheet.set_column('S:S', 100)  # Дополнительная информация

        for col_num, value in enumerate(self.df.columns.values):
            if value in ['№', 'Ссылки на дополнительные фото', 'Артикул фото', 'Описание', 'Страна изготовитель',
                         'Кол-во товара']:
                worksheet.write(0, col_num, value, header_format_blue)
            elif value in ['Объем, л.']:
                worksheet.write(0, col_num, value, header_format_yellow)
            else:
                worksheet.write(0, col_num, value, header_format_red)
        session.close()
        os.remove(path_db + f'{self.file_name}.db')
        print('Файл в excel')
        writer.save()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = Program()
    application.show()

    sys.exit(app.exec())
