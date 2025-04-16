import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- Настройки страницы ---
st.set_page_config(layout="wide", page_title="Поле характеристик насосов")

# --- Загрузка данных из NIS.xlsx ---
@st.cache_data
def load_base_data():
    return pd.read_excel("NIS.xlsx")

# --- Интерфейс ---
st.title("📊 Поле графических характеристик насосов")

# --- Настройки графика ---
with st.sidebar:
    st.header("⚙️ Настройки графика")
    plot_width = st.number_input("Ширина графика (px)", min_value=600, max_value=2000, value=1000, step=100)
    plot_height = st.number_input("Высота графика (px)", min_value=400, max_value=1500, value=750, step=50)

# --- Загрузка модели ---
uploaded_file = st.file_uploader("📤 Загрузите Excel-файл со списком моделей насосов (колонка A)", type=["xlsx"])

if uploaded_file:
    models_df = pd.read_excel(uploaded_file)
    selected_models = models_df.iloc[:, 0].dropna().astype(str).tolist()

    base_df = load_base_data()

    fig = go.Figure()

    for i, model in enumerate(selected_models):
        model_row = base_df[base_df.iloc[:, 1].astype(str).str.strip() == model]

        if not model_row.empty:
            row_idx = model_row.index[0]

            flow = base_df.iloc[row_idx + 1:row_idx + 16, 13]
            head = base_df.iloc[row_idx + 1:row_idx + 16, 14]

            label_pos = [0, 7, 14][i % 3]
            label_texts = ["" for _ in range(15)]
            label_texts[label_pos] = model

            fig.add_trace(go.Scatter(
                x=flow,
                y=head,
                mode='lines+text',
                name=model,
                text=label_texts,
                textposition="top center",
                line=dict(width=3)  # Более жирная линия
            ))
        else:
            st.warning(f"⚠️ Модель «{model}» не найдена в базе данных.")

    fig.update_layout(
        title=dict(
            text="Поле графических характеристик насосов",
            x=0.5,
            font=dict(size=24),
        ),
        xaxis=dict(
            title="Расход, м³/ч",
            titlefont=dict(size=18),
            tickfont=dict(size=14),
            showgrid=True,
            gridcolor="#eeeeee"
        ),
        yaxis=dict(
            title="Напор, м",
            titlefont=dict(size=18),
            tickfont=dict(size=14),
            showgrid=True,
            gridcolor="#eeeeee"
        ),
        legend=dict(
            title="Модели насосов",
            font=dict(size=14)
        ),
        template="plotly_white",
        height=plot_height,
        width=plot_width,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=False)
else:
    st.info("⬆️ Пожалуйста, загрузите файл со списком моделей для отображения.")
