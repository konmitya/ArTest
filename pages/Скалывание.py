import streamlit as st
import pandas as pd
from io import BytesIO

# Создаем пользовательский интерфейс с несколькими страницами
st.title("Обработка данных Excel")


# Вторая страница для обработки данных из двух листов

st.header("Страница 2: Сопоставление данных между листами Excel")

# Загружаем файл с двумя листами
uploaded_file = st.file_uploader("Загрузите файл Excel с двумя листами ('Лист1' и 'Лист2')", type="xlsx")

if uploaded_file:
    # Читаем оба листа
    sheet1 = pd.read_excel(uploaded_file, sheet_name="Лист1")
    sheet2 = pd.read_excel(uploaded_file, sheet_name="Лист2", header=None)

    # # Проверяем, что у листа "Лист1" есть две колонки
    # if len(sheet1.columns) < 2:
    #     st.error("Лист1 должен содержать 2 колонки: A (артикулы) и B (название модели).")
    #     return

    # Создаем DataFrame для результата
    result_df = pd.DataFrame(columns=sheet1.columns.tolist() + list(range(2, 8)))  # Колонки C:H для вставки данных

    # Обрабатываем каждую строку из "Лист1"
    for idx, row in sheet1.iterrows():
        артикул = row[0]
        модель = row[1]

        # Находим соответствие модели на Лист2
        model_rows = sheet2[sheet2[0] == модель]

        if not model_rows.empty:
            # Получаем таблицу напротив найденного названия модели (16 строк и 6 столбцов)
            таблица = sheet2.iloc[model_rows.index[0] + 1: model_rows.index[0] + 17, 1:7]

            # Записываем текущую строку из Лист1 и добавляем таблицу
            result_df = pd.concat([result_df, pd.DataFrame([row.tolist() + [""] * 6], columns=result_df.columns)])
            таблица.columns = result_df.columns[2:]  # Переименовываем колонки для вставки
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
