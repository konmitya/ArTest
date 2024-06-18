import streamlit as st
import hashlib
import sqlite3

# Подключение к базе данных SQLite
conn = sqlite3.connect('articuls.db')
c = conn.cursor()

# Создание таблицы, если ее еще нет
c.execute('''
CREATE TABLE IF NOT EXISTS articuls (
    articul TEXT PRIMARY KEY,
    model_name TEXT UNIQUE
)
''')
conn.commit()


def model_to_articul(model_name):
    # Получить хеш модели
    hash_object = hashlib.sha256(model_name.encode())
    hex_dig = hash_object.hexdigest()

    # Преобразовать хеш в десятичное число
    decimal_number = int(hex_dig, 16)

    # Взять последние 10 цифр
    articul = str(decimal_number)[-10:]

    return articul


def save_articul_model(articul, model_name):
    c.execute('INSERT OR IGNORE INTO articuls (articul, model_name) VALUES (?, ?)', (articul, model_name))
    conn.commit()


def get_model_by_articul(articul):
    c.execute('SELECT model_name FROM articuls WHERE articul = ?', (articul,))
    result = c.fetchone()
    if result:
        return result[0]
    else:
        return None


st.title("Генерация артикулов для насосов CNP")

# Ввод модели и генерация артикула
model_name = st.text_input("Введите модель насоса для генерации артикула:", "")
if model_name:
    articul = model_to_articul(model_name)
    save_articul_model(articul, model_name)
    st.write(f"Модель: {model_name}")
    st.write(f"Артикул: {articul}")

# Обратное преобразование артикула в модель
input_articul = st.text_input("Введите артикул для поиска модели:", "")
if input_articul:
    found_model = get_model_by_articul(input_articul)
    if found_model:
        st.write(f"Артикул: {input_articul}")
        st.write(f"Модель: {found_model}")
    else:
        st.write(f"Модель для артикула {input_articul} не найдена.")