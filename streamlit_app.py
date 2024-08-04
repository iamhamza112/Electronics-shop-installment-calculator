import streamlit as st
import numpy as np

# Function to calculate monthly installment
def calculate_installment(principal, annual_rate, months):
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:
        installment = principal / months
    else:
        installment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    return installment

# Function to calculate the total payment including interest
def calculate_total_payment(installment, months, advance_payment):
    return (installment * months) + advance_payment

# Streamlit interface
st.title("Installment Plan Calculator")

# Inputs
principal = st.number_input("Principal Amount", value=1000)
annual_rate = st.number_input("Annual Interest Rate (%)", value=5.0)
advance_payment = st.number_input("Advance Payment", value=100)

# Calculation and Display
if st.button("Calculate"):
    if principal >= 0 and annual_rate >= 0 and advance_payment >= 0:
        # Plans
        plans = [1, 4, 8, 12]
        
        st.header("Available Plans")
        
        for months in plans:
            installment = calculate_installment(principal, annual_rate, months)
            total_payment = calculate_total_payment(installment, months, advance_payment)
            
            with st.container():
                cols = st.columns(4)
                cols[0].markdown(f"**{months} Month Plan**")
                cols[1].markdown(f"Advance Payment: {advance_payment}")
                cols[2].markdown(f"Total Payment in Installments: {total_payment:.2f}")
                cols[3].markdown(f"Monthly Installment: {installment:.2f}")
    else:
        st.write("Please enter valid inputs.")
