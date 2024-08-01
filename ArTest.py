import streamlit as st

st.title("Ипотечный калькулятор")

# Ввод стоимости квартиры
property_value = st.number_input("Стоимость квартиры (в рублях)", min_value=0, value=1000000, step=10000, format="%d")

# Ввод первоначального взноса
down_payment = st.number_input("Первоначальный взнос (в рублях)", min_value=0, value=200000, step=10000)

# Ввод процентной ставки
interest_rate = st.number_input("Ставка кредита (в %)", min_value=0.0, value=10.0, step=0.1)

# Ввод срока кредита
loan_term_years = st.number_input("Срок кредита (в годах)", min_value=1, value=20, step=1)

# Ввод типа ежемесячных платежей
payment_type = st.radio("Тип ежемесячных платежей", ["Аннуитетные", "Дифференцированные"])

rest_start = property_value - down_payment

# Расчет дифференцированных платежей
if payment_type == "Дифференцированные":
    arr = [] # пустой массив для наполнения месячными платежами
    mp_cnt = loan_term_years * 12 # количество месяцев в сроке кредита
    rest = rest_start
    mp_real = rest_start / (loan_term_years * 12.0)

    while mp_cnt != 0:
        mp = mp_real + (rest * interest_rate / 1200)
        arr.append(round(mp, 2))
        rest = rest - mp_real
        mp_cnt = mp_cnt - 1

    suma = round(sum(arr)+down_payment, 2) # общая заплаченная сумма
    proc = round(sum(arr), 2) - rest_start
    st.write (arr)
    st.write(f'Общая стоимость квартиры: {suma}. Сумма процентов составляет {proc}')

else:
    f = 7