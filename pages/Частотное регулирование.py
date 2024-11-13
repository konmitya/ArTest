import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
from PIL import Image

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
        x1 = np.linspace(0, max(model_data['Q_new']), 50)

        y_h_new = poly(model_data, 'Q_new', 'H_new', x1)  # Напор новый
        y_p_new = poly(model_data, 'Q_new', 'power_new', x1)  # Мощность новая
        y_e_new = poly(model_data, 'Q_new', 'EFF', x1)  # КПД новое

        fig.add_trace(go.Scatter(x=x1, y=y_h_new, name=f'Характеристика насоса c другой частотой', mode='markers',
                                 line=dict(color='rgba(38, 63, 137, 1)')), secondary_y=False, row=1, col=1)

        fig.add_trace(go.Scatter(x=x1, y=y_e_new, name=f'КПД насоса с другой частотой', mode='markers',
                                 line=dict(color='rgba(25, 134, 101, 1)')), secondary_y=True, row=1, col=1)

        fig.add_trace(go.Scatter(x=x1, y=y_p_new, name=f'Мощность насоса c другой частотой', mode='markers',
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
                     range=[0, max(model_data['power'] * 1.1)])

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
    # Шаг 3: Чтение данных из Excel
    df1 = pd.read_excel(uploaded_file)
    st.title("Шаг 2. Построение базового графика")
    st.write(df1)

    curves_1(df1, 0)

    st.title("Шаг 3. Построение измененного графика")

    # Поля для ввода базовой и новой частоты вращения насоса
    n = st.number_input("Введите базовую частоту вращения насоса (n) в об/мин", min_value=0, step=1)
    n1 = st.number_input("Введите новую частоту вращения насоса (n1) в об/мин", min_value=0, step=1)

    if n > 0:
        # Рассчитываем коэффициент преобразования
        ratio = n1 / n

        # Добавляем новые колонки с преобразованными значениями
        df1['Q_new'] = df1['Q'] * ratio
        df1['H_new'] = df1['H'] * (ratio ** 2)
        df1['power_new'] = df1['power'] * (ratio ** 3)

        # Присваиваем индексы для наглядности
        df1.index = range(1, len(df1) + 1)

        st.write("DataFrame с исходными и преобразованными значениями:")
        st.dataframe(df1)
    else:
        st.error("Базовая частота вращения (n) должна быть больше 0.")

    curves_1(df1, 1)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Q и H")
        st.dataframe(df1[['Q', 'H']])
    with col2:
        image = Image.open(f'1.png')
        st.image(image)
    with col3:
        st.write("Q_new и H_new")
        st.dataframe(df1[['Q_new', 'H_new']])

    # 2. Вторая строка с Q и EFF в первом и Q_new и EFF в третьем столбце
    st.write("### Ряд 2: Q и EFF в первом столбце, Q_new и EFF в третьем")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Q и EFF")
        st.dataframe(df1[['Q', 'EFF']])
    with col2:
        image2 = Image.open(f'2.png')
        st.image(image2)
    with col3:
        st.write("Q_new и EFF")
        st.dataframe(df1[['Q_new', 'EFF']])

    # 3. Третья строка с Q и power в первом и Q_new и power_new в третьем столбце
    st.write("### Ряд 3: Q и power в первом столбце, Q_new и power_new в третьем")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Q и power")
        st.dataframe(df1[['Q', 'power']])
    with col2:
        image3 = Image.open(f'3.png')
        st.image(image3)
    with col3:
        st.write("Q_new и power_new")
        st.dataframe(df1[['Q_new', 'power_new']])



