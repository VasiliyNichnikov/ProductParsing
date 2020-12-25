from scripts.database.LeroyMerlin.ad_leroy_merlin import AdModelLeroyMerlin
from scripts.database import db_session
import pandas as pd

df = pd.DataFrame()
# Инициализация БД
db_session.global_init('../files/database/sample.xlsx.db')
session = db_session.create_session()

df['№'] = [i[0] for i in session.query(AdModelLeroyMerlin.ENTRY_ID).all()]
df['Артикул'] = [' ' for i in session.query(AdModelLeroyMerlin.ENTRY_ID).all()]
df['Название товара'] = [i[0] for i in session.query(AdModelLeroyMerlin.NAME).all()]
df['Цена, руб.*'] = [i[0] for i in session.query(AdModelLeroyMerlin.PRICE).all()]
df['Вес в упаковке, г*'] = [i[0] for i in session.query(AdModelLeroyMerlin.WEIGHT).all()]
df['Ширина упаковки, мм*'] = [i[0] for i in session.query(AdModelLeroyMerlin.WIDTH).all()]
df['Высота упаковки, мм*'] = [i[0] for i in session.query(AdModelLeroyMerlin.HEIGHT).all()]
df['Ссылка на главное фото*'] = [i[0] for i in session.query(AdModelLeroyMerlin.MAIN_PHOTO).all()]
df['Ссылки на дополнительные фото'] = [i[0] for i in session.query(AdModelLeroyMerlin.ADDITIONAL_PHOTOS).all()]
df['Артикул фото'] = [i[0] for i in session.query(AdModelLeroyMerlin.PHOTO_ARTICLES).all()]
df['Название модели*'] = [i[0] for i in session.query(AdModelLeroyMerlin.MODEL).all()]
df['Тип*'] = [i[0] for i in session.query(AdModelLeroyMerlin.TYPE_MODEL).all()]
df['Бренд*'] = [i[0] for i in session.query(AdModelLeroyMerlin.BRAND).all()]
df['Объем, л.'] = [i[0] for i in session.query(AdModelLeroyMerlin.VOLUME).all()]
df['Описание'] = [i[0] for i in session.query(AdModelLeroyMerlin.DESCRIPTION).all()]
df['Страна изготовитель'] = [i[0] for i in session.query(AdModelLeroyMerlin.MANUFACTURER).all()]
df['Кол-во товара'] = [i[0] for i in session.query(AdModelLeroyMerlin.QUANTITY_GOODS).all()]
df['Прямая ссылка на товар на сайте '] = [i[0] for i in session.query(AdModelLeroyMerlin.URL).all()]

writer = pd.ExcelWriter(f'../files/excel spreadsheets/sample_2.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
workbook = writer.book
df.to_excel(writer, sheet_name='Шаблон для поставщика', index=False)

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

for col_num, value in enumerate(df.columns.values):
    if value in ['№', 'Ссылки на дополнительные фото', 'Артикул фото', 'Описание', 'Страна изготовитель', 'Кол-во товара']:
        worksheet.write(0, col_num, value, header_format_blue)
    elif value in ['Объем, л.']:
        worksheet.write(0, col_num, value, header_format_yellow)
    else:
        worksheet.write(0, col_num, value, header_format_red)

writer.save()
