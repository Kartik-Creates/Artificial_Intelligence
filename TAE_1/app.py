import streamlit as st
import random
import datetime
from scripts import atm_scripts, accounts, predict_next_action

st.title("🤖 AI ATM Simulator")

# session variables
if "step" not in st.session_state:
    st.session_state.step = 0

if "user" not in st.session_state:
    st.session_state.user = None

if "card_verified" not in st.session_state:
    st.session_state.card_verified = False

if "pin_verified" not in st.session_state:
    st.session_state.pin_verified = False


# STEP 1 : CARD VERIFICATION
if not st.session_state.card_verified:

    card = st.text_input("Enter 12 Digit ATM Card Number")

    if st.button("Verify Card"):

        if card in accounts:
            st.session_state.user = accounts[card]
            st.session_state.card_verified = True
            st.success(f"Welcome {accounts[card]['name']}")

        else:
            st.error("Invalid Card Number")


# STEP 2 : PIN VERIFICATION
elif not st.session_state.pin_verified:

    pin = st.text_input("Enter 4 Digit PIN", type="password")

    if st.button("Verify PIN"):

        if pin == st.session_state.user["pin"]:
            st.session_state.pin_verified = True
            st.success("PIN Verified")

        else:
            st.error("Incorrect PIN")


# STEP 3 : ATM TRANSACTIONS
else:

    st.write("Account Holder:", st.session_state.user["name"])
    st.write("Balance: ₹", st.session_state.user["balance"])

    transaction = st.selectbox(
        "Select Transaction",
        ["Withdraw Cash", "Check Balance", "Deposit Money"]
    )

    # withdraw
    if transaction == "Withdraw Cash":

        amount = st.number_input("Enter Amount", min_value=100)

        if st.button("Withdraw"):

            if amount > st.session_state.user["balance"]:
                st.error("Insufficient Balance")

            else:
                st.session_state.user["balance"] -= amount
                st.success(f"₹{amount} withdrawn successfully")

    # deposit
    elif transaction == "Deposit Money":

        amount = st.number_input("Enter Amount")

        if st.button("Deposit"):
            st.session_state.user["balance"] += amount
            st.success("Deposit Successful")

    # check balance
    elif transaction == "Check Balance":

        st.success(f"Your Balance is ₹{st.session_state.user['balance']}")
