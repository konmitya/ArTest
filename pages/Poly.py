import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np

def poly(model_data, ind1, ind2, x):
    curve_coef = np.polyfit(model_data[ind1], model_data[ind2], 3)
    curve_coef_list = curve_coef.tolist()
    curve_coef_list.reverse()
    z = curve_coef_list
    y = z[0] + z[1] * x + z[2] * x ** 2 + z[3] * x ** 3

    return y, z


# Загружаем Excel файл через Streamlit
uploaded_file = st.file_uploader("Выберите Excel-файл", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Читаем данные из Excel файла
        model_data = pd.read_excel(uploaded_file)

        # Если в файле нет заголовков, можно использовать:
        # df = pd.read_excel(uploaded_file, header=None, names=["Подача", "Напор", "NPSHr", "КПД", "Мощность"])

        # Переименовываем столбцы согласно требуемой схеме:
        model_data = model_data.rename(columns={
            "Подача": "Q",
            "Напор": "H",
            "NPSHr": "NPSH",
            "КПД": "EFF",
            "Мощность": "power"
        })

        st.subheader("Данные после загрузки и переименования столбцов:")
        st.write(model_data)

        # Задаем горизонтальную ось
        x = np.linspace(0, max(model_data['Q']), 200)

        # Задаем уравнения кривых для характеристик
        y_h, z1 = poly(model_data, 'Q', 'H', x)  # Напор

        st.write(f"{z1[0]} + {z1[1]} * x + {z1[2]} * x ** 2 + {z1[3]} * x ** 3")

        y_e, z2 = poly(model_data, 'Q', 'EFF', x)  # КПД
        y_p, z3 = poly(model_data, 'Q', 'power', x)  # Мощность
        y_np, z4 = poly(model_data, 'Q', 'NPSH', x)  #

    except Exception as e:
        st.error(f"Ошибка при обработке файла: {e}")
else:
    st.info("Пожалуйста, загрузите Excel-файл.")
