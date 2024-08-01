import streamlit as st

st.title("Ипотечный калькулятор")

# Ввод стоимости квартиры
property_value = st.number_input("Стоимость квартиры (в рублях)", min_value=0, value=1000000, step=10000)

# Ввод первоначального взноса
down_payment = st.number_input("Первоначальный взнос (в рублях)", min_value=0, value=200000, step=10000)

# Ввод процентной ставки
interest_rate = st.number_input("Ставка кредита (в %)", min_value=0.0, value=10.0, step=0.1)

# Ввод срока кредита
loan_term_years = st.number_input("Срок кредита (в годах)", min_value=1, value=20, step=1)

# Ввод типа ежемесячных платежей
payment_type = st.checkbox("Тип ежемесячных платежей", ["Аннуитетные", "Дифференцированные"])