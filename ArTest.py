# import streamlit as st
# import hashlib
# import sqlite3
#
# # Подключение к базе данных SQLite
# conn = sqlite3.connect('articuls.db')
# c = conn.cursor()
#
# # Создание таблицы, если ее еще нет
# c.execute('''
# CREATE TABLE IF NOT EXISTS articuls (
#     articul TEXT PRIMARY KEY,
#     model_name TEXT UNIQUE
# )
# ''')
# conn.commit()
#
#
# def model_to_articul(model_name):
#     # Получить хеш модели
#     hash_object = hashlib.sha256(model_name.encode())
#     hex_dig = hash_object.hexdigest()
#
#     # Преобразовать хеш в десятичное число
#     decimal_number = int(hex_dig, 16)
#
#     # Взять последние 10 цифр
#     articul = str(decimal_number)[-10:]
#
#     return articul
#
#
# def save_articul_model(articul, model_name):
#     c.execute('INSERT OR IGNORE INTO articuls (articul, model_name) VALUES (?, ?)', (articul, model_name))
#     conn.commit()
#
#
# def get_model_by_articul(articul):
#     c.execute('SELECT model_name FROM articuls WHERE articul = ?', (articul,))
#     result = c.fetchone()
#     if result:
#         return result[0]
#     else:
#         return None
#
#
# st.title("Генерация артикулов для насосов CNP")
#
# # Ввод модели и генерация артикула
# model_name = st.text_input("Введите модель насоса для генерации артикула:", "")
# if model_name:
#     articul = model_to_articul(model_name)
#     save_articul_model(articul, model_name)
#     st.write(f"Модель: {model_name}")
#     st.write(f"Артикул: {articul}")
#
# # Обратное преобразование артикула в модель
# input_articul = st.text_input("Введите артикул для поиска модели:", "")
# if input_articul:
#     found_model = get_model_by_articul(input_articul)
#     if found_model:
#         st.write(f"Артикул: {input_articul}")
#         st.write(f"Модель: {found_model}")
#     else:
#         st.write(f"Модель для артикула {input_articul} не найдена.")

import streamlit as st
import pandas as pd
from io import BytesIO


#st.title("Ипотечный калькулятор")

# def format_number(number):
#     return f"{number:,.0f}".replace(",", " ")


# # Ввод стоимости квартиры
# property_value = st.number_input("Стоимость квартиры (в рублях)", min_value=0, value=1000000, step=10000)
#
# # Ввод первоначального взноса
# down_payment = st.number_input("Первоначальный взнос (в рублях)", min_value=0, value=200000, step=10000)
#
# # Ввод процентной ставки
# interest_rate = st.number_input("Ставка кредита (в %)", min_value=0.0, value=10.0, step=0.1)
#
# # Ввод срока кредита
# loan_term_years = st.number_input("Срок кредита (в годах)", min_value=1, value=20, step=1)
#
# # Ввод типа ежемесячных платежей
# payment_type = st.radio("Тип ежемесячных платежей", ["Аннуитетные", "Дифференцированные"])
#
# rest_start = property_value - down_payment
#
# # Расчет дифференцированных платежей
# if payment_type == "Дифференцированные":
# arr = [] # пустой массив для наполнения месячными платежами
# mp_cnt = loan_term_years * 12 # количество месяцев в сроке кредита
# rest = rest_start # Сумма кредита
# mp_real = rest_start / (loan_term_years * 12.0)
#
# while mp_cnt != 0:
#     mp = mp_real + (rest * interest_rate / 1200)
#     arr.append(round(mp, 2))
#     rest = rest - mp_real
#     mp_cnt = mp_cnt - 1
#
# suma = round(sum(arr) + down_payment, 2) # общая заплаченная сумма
# proc = round(sum(arr), 2) - rest_start
#
# st.write ('Ежемесячные платежи:')
# st.write (arr)
# st.write(f'Общая стоимость квартиры: {format_number(suma)}.')
# st.write(f'Сумма процентов: {format_number(proc)}.')
#
# else:
# # Аннуитетные платежи
# mp_cnt = loan_term_years * 12
# r = interest_rate / 1200.0
# ak = (r * (1 + r) ** mp_cnt) / (((1 + r) ** mp_cnt) - 1)
# mp = rest_start * ak
# total = mp * mp_cnt
# suma = round(total+down_payment, 2)
# proc = round(total - rest_start, 2)
#
# st.write(f'Ежемесячный платеж составит: {format_number(round(mp, 2))}.')
# st.write(f'Общая стоимость квартиры: {format_number(suma)}.')
# st.write(f'Сумма процентов: {format_number(proc)}.')



# Создаем пользовательский интерфейс Streamlit
st.title("Объединение данных из Excel файлов")

# Загружаем файлы
uploaded_files = st.file_uploader("Загрузите файлы Excel", accept_multiple_files=True, type="xls")

# Кнопка для запуска объединения файлов
if st.button("Объединить файлы"):
    if not uploaded_files:
        st.warning("Загрузите хотя бы один файл.")
    else:
        # Создаем пустой DataFrame для хранения всех данных
        combined_data = []

        # Обрабатываем каждый загруженный файл
        for file in uploaded_files:
            # Читаем файл Excel и получаем первые 16 строк и 6 столбцов
            df = pd.read_excel(file, header=None, nrows=16, usecols="A:F")

            # Добавляем название файла в столбец A для первой строки и пустые значения для остальных 15 строк
            file_name_column = [file.name] + [""] * 15
            df.insert(0, "Файл", file_name_column)

            # Добавляем обработанные данные в общий список
            combined_data.append(df)

        # Объединяем все данные в один DataFrame без промежуточных пустых строк
        final_df = pd.concat(combined_data, ignore_index=True)

        # Создаем Excel файл в памяти
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            final_df.to_excel(writer, index=False, header=False, sheet_name="Объединенные данные")
        output.seek(0)

        # Отображаем кнопку для скачивания файла
        st.success("Файл успешно создан!")
        st.download_button(
            label="Скачать объединенный файл",
            data=output,
            file_name="Объединенные_данные.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


