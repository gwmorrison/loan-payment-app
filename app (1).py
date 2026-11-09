# ============================================================
# Loan Payment Calculator - a beginner-friendly Streamlit app
# Answers a common finance question: "If I borrow money, what
# will I pay each month, and how much interest will it cost me?"
# ============================================================

# --- SECTION 1: Import libraries ---
# Streamlit builds the web page. Pandas organizes data into tables
# (it is installed automatically with Streamlit, so no extra setup).
import streamlit as st
import pandas as pd


# --- SECTION 2: Page setup ---
# Must be the first Streamlit command. Sets the tab title and icon.
st.set_page_config(
    page_title="Loan Calculator",
    page_icon="💰",
    layout="centered",
)


# --- SECTION 3: The finance math (as a function) ---
def calculate_monthly_payment(principal, annual_rate_percent, years):
    """
    Standard loan payment formula:
        M = P × r × (1 + r)^n / ((1 + r)^n − 1)
    where:
        P = loan amount, r = monthly interest rate, n = number of monthly payments
    """
    n = years * 12                            # total number of monthly payments
    r = annual_rate_percent / 100 / 12        # yearly percent -> monthly decimal

    # Special case: with 0% interest the formula would divide by zero,
    # so we simply split the loan evenly across all months.
    if r == 0:
        return principal / n

    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


# --- SECTION 4: Title and description ---
st.title("💰 Loan Payment Calculator")
st.write("Find out your monthly payment and the total interest on a loan.")
st.divider()


# --- SECTION 5: User inputs ---
# number_input = a box for typing numbers; slider = a draggable bar.
loan_amount = st.number_input(
    "Loan amount ($)",
    min_value=0.0,       # no negative loans
    value=20000.0,       # starting value
    step=1000.0,         # how much the +/- buttons change it
)

interest_rate = st.number_input(
    "Annual interest rate (%)",
    min_value=0.0,
    max_value=40.0,
    value=6.5,
    step=0.1,
)

loan_years = st.slider(
    "Loan length (years)",
    min_value=1,
    max_value=30,
    value=5,
)

# If the loan amount is zero there is nothing to calculate,
# so we show a message and stop the script here.
if loan_amount == 0:
    st.info("Enter a loan amount above $0 to see your results.")
    st.stop()


# --- SECTION 6: Do the calculations ---
monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_years)
number_of_payments = loan_years * 12
total_paid = monthly_payment * number_of_payments
total_interest = total_paid - loan_amount


# --- SECTION 7: Display the results ---
st.divider()

# st.columns splits the page into side-by-side sections.
col1, col2, col3 = st.columns(3)
# ":,.2f" means: add commas to big numbers and show 2 decimal places.
col1.metric("Monthly payment", f"${monthly_payment:,.2f}")
col2.metric("Total paid", f"${total_paid:,.2f}")
col3.metric("Total interest", f"${total_interest:,.2f}")


# --- SECTION 8: Show the formula used ---
st.subheader("Formula used")
st.code("M = P × r × (1 + r)^n / ((1 + r)^n − 1)", language=None)
st.write(
    f"- **P** (loan amount) = ${loan_amount:,.2f}\n"
    f"- **r** (monthly rate) = {interest_rate}% ÷ 12 = {interest_rate / 12:.4f}%\n"
    f"- **n** (number of payments) = {loan_years} years × 12 = {number_of_payments}"
)


# --- SECTION 9: Chart of the remaining balance ---
# We simulate each month: interest is added, then the payment is subtracted.
monthly_rate = interest_rate / 100 / 12
balance = loan_amount
balances = [balance]  # a list that starts with the full loan amount

for month in range(number_of_payments):
    interest_this_month = balance * monthly_rate
    balance = balance + interest_this_month - monthly_payment
    balances.append(max(balance, 0))  # max() prevents tiny negative rounding errors

# Put the data in a table (DataFrame), then draw a line chart.
balance_table = pd.DataFrame(
    {"Month": range(number_of_payments + 1), "Remaining balance ($)": balances}
).set_index("Month")

st.subheader("Remaining balance over time")
st.line_chart(balance_table)


# --- SECTION 10: Friendly note ---
st.caption("This is an estimate for learning purposes, not financial advice.")
