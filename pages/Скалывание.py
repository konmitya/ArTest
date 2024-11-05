import streamlit as st
import pandas as pd
from io import BytesIO
import string

def excel_column_to_index(column_name):
    index = 0
    for char in column_name:
        index = index * 26 + (ord(char.upper()) - ord('A') + 1)
    return index - 1


st.header("Страница 2: Сопоставление данных между листами Excel")

# Загрузка файла с двумя листами
uploaded_file = st.file_uploader("Загрузите файл Excel с двумя листами ('Лист1' и 'Лист2')", type="xlsx")

if uploaded_file:
    # Читаем оба листа
    sheet1 = pd.read_excel(uploaded_file, sheet_name="Лист1")
    sheet2 = pd.read_excel(uploaded_file, sheet_name="Лист2", header=None)

    # Ввод колонки для поиска модели на "Лист2"
    match_column_letter = st.text_input(
        "Введите букву колонки для поиска модели на 'Лист2' (например, A)").strip().upper()

    # Ввод колонок для переноса данных в формате Excel (например, "B, C, D")
    columns_range_input = st.text_input(
        "Введите буквы колонок для переноса данных с 'Лист2', разделенные запятыми (например, B, C, D)").strip().upper()
    columns_range_letters = [col.strip() for col in columns_range_input.split(",") if col.strip()]

    # Ввод количества строк для переноса
    rows_to_transfer = st.number_input("Введите количество строк для переноса", min_value=1, max_value=100, value=16)

    # Конвертируем буквы колонок в индексы
    try:
        match_column_index = excel_column_to_index(match_column_letter)
        selected_columns_indices = [excel_column_to_index(col) for col in columns_range_letters]
    except:
        st.error("Некорректное указание колонок. Проверьте правильность ввода.")

    # Создаем DataFrame для результата
    result_df = pd.DataFrame(columns=sheet1.columns.tolist() + columns_range_letters)

    if st.button("Выполнить обработку"):
        # Обрабатываем каждую строку из "Лист1"
        for idx, row in sheet1.iterrows():
            артикул = row[0]
            модель = row[1]

            # Находим соответствие модели на "Лист2"
            model_rows = sheet2[sheet2[match_column_index] == модель]

            if not model_rows.empty:
                # Получаем таблицу напротив найденного названия модели
                start_row = model_rows.index[0] + 1
                end_row = start_row + rows_to_transfer
                таблица = sheet2.iloc[start_row:end_row, selected_columns_indices]

                # Записываем текущую строку из Лист1 и добавляем таблицу
                result_df = pd.concat([result_df, pd.DataFrame([row.tolist() + [""] * len(columns_range_letters)],
                                                               columns=result_df.columns)])
                таблица.columns = result_df.columns[len(sheet1.columns):]  # Переименовываем колонки для вставки
                result_df = pd.concat([result_df, таблица], ignore_index=True)

        # Создаем Excel файл в памяти для скачивания
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            result_df.to_excel(writer, index=False, header=False, sheet_name="Результат")
        output.seek(0)

        # Кнопка для скачивания файла
        st.success("Файл успешно обработан!")
        st.download_button(
            label="Скачать обработанный файл",
            data=output,
            file_name="Обработанные_данные.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )