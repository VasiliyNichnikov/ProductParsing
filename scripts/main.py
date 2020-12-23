"""
    Данный скрипт запускает парсинг с введенными параметрами
"""
from scripts.LeroyMerlin.ParsingPage import ParsingPage
from scripts.LeroyMerlin.ParsingAd import ParsingAd
from scripts.database.LeroyMerlin.ad_leroy_merlin import AdModelLeroyMerlin
from scripts.database import db_session
import pandas as pd


name_bd = 'sample_2'
# list_urls = ['https://leroymerlin.ru/search/?q=шкаф']
list_urls = ['https://leroymerlin.ru/search/?q=шкаф',
             'https://leroymerlin.ru/search/?q=стол',
             'https://leroymerlin.ru/search/?q=лион&family=garderobnye-sistemy-panelnye-201709&suggest=true',
             'https://leroymerlin.ru/search/?q=раковина',
             'https://leroymerlin.ru/search/?q=зеркало&family=5a35c540-a696-11ea-b381-49b4680b1a6a&suggest=true']
# number_threads = 3

df = pd.DataFrame()
# Инициализация БД
db_session.global_init(f'../files/database/{name_bd}.db')


def parsing_ad(link):
    data_ad = ParsingAd(link)
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

    # print('------------------------------------------------')


for url in list_urls:
    parsing_page = ParsingPage(url=url, start_page=1)
    while parsing_page.page <= parsing_page.max_page:
        print(f'Страница - {parsing_page.page}; Максимальная страница - {parsing_page.max_page}')
        list_links = parsing_page.get_urls()

        for link in list_links:
            parsing_ad(link)
        parsing_page.page += 1

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
