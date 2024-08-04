import streamlit as st
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

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
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Title
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title = Paragraph("Electronics Plan Details", title_style)
    elements.append(title)

    # Customer Name and Date/Item Info
    info_style = styles['Normal']
    customer_info = Paragraph(f"Customer: {customer_name}", info_style)
    date_info = Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", info_style)
    item_info = Paragraph(f"Item: {item_name}", info_style)
    
    elements.append(customer_info)
    elements.append(date_info)
    elements.append(item_info)

    # Table Data
    data = [
        ["Plan", "Advance Payment", "Total Payment", "Monthly Installment"]
    ]

    for plan in plans:
        data.append([
            plan['Plan'],
            f"${plan['Advance Payment']:.2f}",
            f"${plan['Total Payment in Installments']:.2f}",
            f"${plan['Monthly Installment']:.2f}"
        ])

    # Table Style
    table = Table(data, colWidths=[2*inch]*4, rowHeights=0.5*inch)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Add table to elements
    elements.append(table)

    # Footer
    footer_style = styles['Normal']
    footer_address = Paragraph("Opp. Tariq Cash And Carry Sunder Road, Raiwind", footer_style)
    footer_credit = Paragraph("Made by Patla", footer_style)
    
    elements.append(footer_address)
    elements.append(footer_credit)
    
    doc.build(elements)
    
    buffer.seek(0)
    return buffer

# Streamlit interface
st.title("Installment Plan Calculator")

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
