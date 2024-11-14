import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
from PIL import Image
import math

def poly(model_data, ind1, ind2, x):
    curve_coef = np.polyfit(model_data[ind1], model_data[ind2], 3)
    curve_coef_list = curve_coef.tolist()
    curve_coef_list.reverse()
    z = curve_coef_list
    y = z[0] + z[1] * x + z[2] * x ** 2 + z[3] * x ** 3

    return y

def curves_1(model_data, marker):


    # Задаем горизонтальную ось
    x = np.linspace(0, max(model_data['Q']), 50)

    # Задаем уравнения кривых для характеристик
    y_h = poly(model_data, 'Q', 'H', x)  # Напор
    y_e = poly(model_data, 'Q', 'EFF', x)  # КПД
    y_p = poly(model_data, 'Q', 'power', x)  # Мощность
    y_np = poly(model_data, 'Q', 'NPSH', x)  #NPSH

    # Создаем график с несколькими кривыми и задаем данные/настройки
    fig = make_subplots(vertical_spacing=0.08, rows=2, cols=1, row_heights=[0.7, 0.3],
                        specs=[[{"secondary_y": True}], [{"secondary_y": True}]])

    if marker == 1:
        x1 = np.linspace(0, max(model_data['Qv']), 50)

        y_h_new = poly(model_data, 'Qv', 'Hv', x1)  # Напор новый
        y_p_new = poly(model_data, 'Qv', 'Pv', x1)  # Мощность новая
        y_e_new = poly(model_data, 'Qv', 'EFFv', x1)  # КПД новое

        fig.add_trace(go.Scatter(x=x1, y=y_h_new, name=f'Характеристика насоса c другой вязкостью', mode='markers',
                                 line=dict(color='rgba(38, 63, 137, 1)')), secondary_y=False, row=1, col=1)

        fig.add_trace(go.Scatter(x=x1, y=y_e_new, name=f'КПД насоса с другой вязкостью', mode='markers',
                                 line=dict(color='rgba(25, 134, 101, 1)')), secondary_y=True, row=1, col=1)

        fig.add_trace(go.Scatter(x=x1, y=y_p_new, name=f'Мощность насоса c другой вязкостью', mode='markers',
                                 line=dict(color='rgba(80, 35, 137, 1)')), secondary_y=False, row=2, col=1)

    fig.add_trace(go.Scatter(x=x, y=y_h, name=f'Характеристика насоса', mode='lines',
                             line=dict(color='rgba(38, 63, 137, 1)')), secondary_y=False, row=1, col=1)


    fig.add_trace(go.Scatter(x=x, y=y_e, name=f'КПД насоса', mode='lines',
                             line=dict(color='rgba(25, 134, 101, 1)')), secondary_y=True, row=1, col=1)

    fig.add_trace(go.Scatter(x=x, y=y_p, name=f'Мощность насоса', mode='lines',
                             line=dict(color='rgba(80, 35, 137, 1)')), secondary_y=False, row=2, col=1)


    fig.add_trace(go.Scatter(x=x, y=y_np, name=f'NPSH насоса', mode='lines',
                             line=dict(color='rgba(202, 151, 39, 1)')), secondary_y=True, row=2, col=1)

    fig.update_yaxes(col=1, row=2, title_text='Мощность, кВт', secondary_y=False,
                     range=[0, max(model_data['Pv'] * 1.1)])

    fig.update_yaxes(col=1, row=2, title_text='NPSHr, м', secondary_y=True, range=[0, max(model_data['NPSH'] * 1.3)])

    fig.update_xaxes(col=1, row=2, title_text="Подача, м3/ч", range=[0, max(model_data['Q'] * 1.1)])

    # fig.add_trace(go.Scatter(x=[p_q], y=[p_h], name="Рабочая точка", mode="markers", marker=dict(
    #     symbol="cross-thin", size=20, line=dict(color='rgba(255, 0, 0, 1)', width=2))), secondary_y=False, row=1, col=1)

    fig.update_layout(legend_orientation="h", height=1000,
                      legend=dict(x=.5, xanchor="center", yanchor='bottom', y=-0.23),
                      title=f'Характеристика насоса', font_family="Arial",
                      xaxis=dict(title=dict(text="Подача, м3/ч"), range=[0, max(model_data['Q'] * 1.1)]),
                      yaxis_title="Напор, м", yaxis_range=[0, max(model_data['H']) * 1.1],
                      yaxis2_range=[0, 100], yaxis2_title='КПД, %',
                      margin=dict(l=40, r=0, t=30, b=0))

    st.plotly_chart(fig, use_container_width=True, theme=None)


st.title('Пересчет рабочих характеристик насоса с воды на вязкую жидкость')
st.title("Шаг 1. Загрузка файла с данными")

st.markdown("""
### Инструкция:
Пожалуйста, убедитесь, что ваш Excel-файл имеет следующий формат:
- Всего **5 колонок** с именами: `Q`, `H`, `EFF`, `power`, `NPSH`.
- **Первая строка** содержит названия колонок.
- В каждой колонке **ровно 16 строк данных** (первая строка — заголовок, и 15 строк данных).
- Пример структуры данных в Excel-файле:

| Q | H | EFF | power | NPSH |
|---|---|-----|-------|------|
| 1 | 10 | 0.75 | 5.5 | 3.1 |
| 2 | 20 | 0.78 | 6.0 | 3.3 |
| ... | ... | ... | ... | ... |
""")

# Шаг 2: Загрузка файла
uploaded_file = st.file_uploader("Загрузите Excel-файл", type="xlsx")

# Проверка загруженного файла
if uploaded_file is not None:
    st.title("Шаг 2. Задание параметров расчета")
    df = pd.read_excel(uploaded_file)

    po = st.number_input('Плотность, кг/м3', min_value=0, step=1,value=1000) # Плотность вязкой рабочей среды, кг/м3
    V = st.number_input('Вязкость перекачиваемой среды, сСт', min_value=0, value=1)

    s = po / 1000  # Удельная плотность относительно воды

    n = st.number_input('Частота вращения, об/мин', min_value=0, step=1, value=2900)  # Частота вращения, об/мин

    st.title("Шаг 3. Расчет характеристики насоса на новой вязкости")

    st.write("3.1 Определяем точку с максимальным КПД и значения подачи (Qbep) и напора (Hbep) в этой точке. Эти значения пригодятся в дальнейшем.")
    max_eff = df['EFF'].max()
    max_eff_index = df['EFF'].idxmax()

    Qbep = df.loc[max_eff_index, 'Q']
    Hbep = df.loc[max_eff_index, 'H']

    st.write(f"Индекс максимальной точки: {max_eff_index}. Qbep = {Qbep}. Hbep = {Hbep}")

    # Рассчитываем параметр B, основанный на известных параметрах
    B = 16.5 * ((V ** 0.5) * (Hbep ** 0.0625)) / ((Qbep ** 0.375) * (n ** 0.25))

    st.write(f"3.2 Начинаем процесс пересчета по вязкости. Рассчитываем коэффициент B по формуле:")
    image = Image.open(f'B.png')
    st.image(image)
    st.write(f"В нашем случае B = {B}. Далее необходимо выполнить проверку 1 < B < 40. Если B не лежит в этом диапазоне, то нужно выдать пользователю ошибку. Если подходит, то считаем дальше. Есди B меньше или равно 1, то характеристика остается такой же.")

    if B < 40:
        if B > 1:
            st.write("3.3 Рассчитываем коэффициент пересчета подачи по формуле:")
            image = Image.open(f'Cq.png')
            st.image(image)

            # Рассчитываем коэффициент пересчета подачи
            Cq = 2.71 ** (-0.165 * (math.log10(B)) ** (3.15))
            st.write(f"В нашем случае Cq = {Cq}")


            # Подача на вязкой жидкости в точке максимального КПД
            Qbepv = Cq * Qbep

            # Коэффициент пересчета напора по вязкости в точке максимального КПД
            Cbeph = Cq

            # Напор на вязкой жидкости в точке максимального КПД
            Hbeph = Cbeph * Hbep

            # Коэффициент пересчета КПД
            Cn = B ** (-0.0547 * B ** 0.69)

            st.write("3.4 Коэффициент пересчета по вязкости для напора в точке с максимальным КПД:")

            image = Image.open(f'Cbeph.png')
            st.image(image)

            st.write("3.4 далее необходимо рассчитать набор коэффициентов пересчета напора для каждой точки по формуле:")

            image = Image.open(f'Ch.png')
            st.image(image)

            # Расчет новых столбцов
            df['Qv'] = Cq * df['Q']
            df['Ch'] = 1 - ((1 - Cbeph) * (df['Q'] / Qbep) ** 0.75)
            df['Hv'] = df['Ch'] * df['H']
            df['EFFv'] = df['EFF'] * Cn

            st.write(
                "В нашем случае получается:")
            st.write(df['Ch'])
            st.write(
                "3.5 Рассчитываем коэффициент КПД по формуле:")

            image = Image.open(f'Cn.png')
            st.image(image)

            st.write(f"В нашем случае получается: {Cn}")

            st.write(
                "3.6 Пересчитываем все данные для графических характеристик по соответствующим формулам:")



            # Создание столбца Pv с условием для первого элемента
            df['Pv'] = df.apply(
                lambda row: row['power'] if row.name == 0 else (row['Qv'] * row['Hv'] * s*100) / (367 * row['EFFv']),
                axis=1
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("Q и H")
                st.dataframe(df[['Q', 'H']])
            with col2:
                st.write("Формулы для преобразования")
                image = Image.open(f'Qvis.png')
                st.image(image)
                image = Image.open(f'Hvis.png')
                st.image(image)
            with col3:
                st.write("Qv и Hv")
                st.dataframe(df[['Qv', 'Hv']])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("Q и EFF")
                st.dataframe(df[['Q', 'EFF']])
            with col2:
                st.write("Формулы для преобразования")
                image = Image.open(f'Qvis.png')
                st.image(image)
                image = Image.open(f'nvis.png')
                st.image(image)
            with col3:
                st.write("Qv и EFFv")
                st.dataframe(df[['Qv', 'EFFv']])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("Q и power")
                st.dataframe(df[['Q', 'power']])
            with col2:
                st.write("Формулы для преобразования")
                image = Image.open(f'Qvis.png')
                st.image(image)
                image = Image.open(f'Pvis.png')
                st.image(image)
            with col3:
                st.write("Qv и Pv")
                st.dataframe(df[['Qv', 'Pv']])

            curves_1(df, 1)