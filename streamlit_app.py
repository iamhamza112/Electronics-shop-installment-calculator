import streamlit as st
from fpdf import FPDF
from io import BytesIO
from datetime import datetime

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

# Function to generate PDF
def generate_pdf(item_name, customer_name, plans):
    buffer = BytesIO()
    
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Electronics Plan Details', 0, 1, 'C')
            self.ln(10)
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, 'Opp. Tariq Cash And Carry Sunder Road, Raiwind', 0, 0, 'L')
            self.set_y(-10)
            self.cell(0, 10, 'Made by Patla', 0, 0, 'C')
    
    pdf = PDF()
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Customer: {customer_name}', 0, 1, 'L')
    pdf.cell(0, 10, f'Date: {datetime.now().strftime("%Y-%m-%d")}', 0, 1, 'L')
    pdf.cell(0, 10, f'Item: {item_name}', 0, 1, 'L')
    pdf.ln(10)
    
    # Table headers
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(45, 10, 'Plan', 1)
    pdf.cell(45, 10, 'Advance Payment', 1)
    pdf.cell(45, 10, 'Total Payment', 1)
    pdf.cell(45, 10, 'Monthly Installment', 1)
    pdf.ln()
    
    # Table rows
    pdf.set_font('Arial', '', 12)
    for plan in plans:
        pdf.cell(45, 10, plan['Plan'], 1)
        pdf.cell(45, 10, f"${plan['Advance Payment']:.2f}", 1)
        pdf.cell(45, 10, f"${plan['Total Payment in Installments']:.2f}", 1)
        pdf.cell(45, 10, f"${plan['Monthly Installment']:.2f}", 1)
        pdf.ln()
    
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

# Streamlit interface
st.title("Installment Plan c")

# Inputs
item_name = st.text_input("Item Name", value="Sample Item")
customer_name = st.text_input("Customer Name", value="John Doe")
principal = st.number_input("Principal Amount", value=1000)
annual_rate = st.number_input("Annual Interest Rate (%)", value=5.0)
advance_payment = st.number_input("Advance Payment", value=100)

# Calculation and Display
if st.button("Calculate"):
    if principal >= 0 and annual_rate >= 0 and advance_payment >= 0:
        # Plans
        plan_durations = [1, 4, 8, 12]
        plans = []

        st.header("Available Plans")
        
        for months in plan_durations:
            installment = calculate_installment(principal, annual_rate, months)
            total_payment = calculate_total_payment(installment, months, advance_payment)
            
            plan_details = {
                "Plan": f"{months} Month Plan",
                "Advance Payment": advance_payment,
                "Total Payment in Installments": total_payment,
                "Monthly Installment": installment
            }
            
            plans.append(plan_details)

            with st.container():
                cols = st.columns(4)
                cols[0].markdown(f"**{months} Month Plan**")
                cols[1].markdown(f"Advance Payment: {advance_payment}")
                cols[2].markdown(f"Total Payment in Installments: {total_payment:.2f}")
                cols[3].markdown(f"Monthly Installment: {installment:.2f}")
        
        # Generate PDF
        buffer = generate_pdf(item_name, customer_name, plans)
        st.download_button(
            label="Download PDF",
            data=buffer,
            file_name=f"{item_name}_Installment_Plan.pdf",
            mime="application/pdf"
        )
    else:
        st.write("Please enter valid inputs.")
