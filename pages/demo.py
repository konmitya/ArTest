import streamlit as st
import openai
import base64
from PIL import Image
import io
import os

# Настройки страницы
st.set_page_config(page_title="Распознавание визитки", layout="centered")

# Ввод ключа OpenAI (можно через secrets, если на Streamlit Cloud)
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🧾 Распознавание визитки")
st.write("Загрузите изображение, чтобы извлечь контактные данные с помощью GPT-4o.")

uploaded_file = st.file_uploader("Загрузите изображение визитки", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Загруженное изображение", use_column_width=True)

    if st.button("🔍 Распознать"):
        with st.spinner("Обработка изображения..."):
            # Преобразование изображения в base64
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()

            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Ты помощник, который извлекает данные с визитки."},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Извлеки с этой визитки следующие данные в формате JSON:\n"
                                        "- full_name\n"
                                        "- position\n"
                                        "- company_name\n"
                                        "- email\n"
                                        "- website\n"
                                        "- address"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_base64}"
                                },
                            },
                        ],
                    },
                ],
                temperature=0.2,
            )

            result_text = response.choices[0].message.content
            st.subheader("📋 Результат:")
            st.code(result_text, language="json")