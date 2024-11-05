import streamlit as st
import pandas as pd
from io import BytesIO

st.header("Страница 2: Сопоставление данных между листами Excel")

# Загрузка файла с двумя листами
uploaded_file = st.file_uploader("Загрузите файл Excel с двумя листами ('Лист1' и 'Лист2')", type="xlsx")

if uploaded_file:
    # Читаем оба листа
    sheet1 = pd.read_excel(uploaded_file, sheet_name="Лист1")
    sheet2 = pd.read_excel(uploaded_file, sheet_name="Лист2", header=None)

    # Отображаем список колонок для выбора в "Лист2"
    columns = sheet2.columns
    selected_match_column = st.selectbox("Выберите колонку на 'Лист2' для поиска модели", columns)
    selected_columns_range = st.multiselect("Выберите колонки для переноса данных с 'Лист2'", columns,
                                            default=columns[1:7])
    rows_to_transfer = st.number_input("Введите количество строк для переноса", min_value=1, max_value=100, value=16)

    # Создаем DataFrame для результата
    result_df = pd.DataFrame(columns=sheet1.columns.tolist() + list(
        range(len(sheet1.columns), len(sheet1.columns) + len(selected_columns_range))))

    if st.button("Выполнить обработку"):
        # Обрабатываем каждую строку из "Лист1"
        for idx, row in sheet1.iterrows():
            артикул = row[0]
            модель = row[1]

            # Находим соответствие модели на "Лист2"
            model_rows = sheet2[sheet2[selected_match_column] == модель]

            if not model_rows.empty:
                # Получаем таблицу напротив найденного названия модели
                start_row = model_rows.index[0] + 1
                end_row = start_row + rows_to_transfer
                таблица = sheet2.iloc[start_row:end_row, selected_columns_range]

                # Записываем текущую строку из Лист1 и добавляем таблицу
                result_df = pd.concat([result_df, pd.DataFrame([row.tolist() + [""] * len(selected_columns_range)],
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
