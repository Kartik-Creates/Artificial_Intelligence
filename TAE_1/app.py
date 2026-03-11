import streamlit as st
import random
import datetime
from scripts import atm_scripts, accounts, predict_next_action

st.set_page_config(page_title="AI ATM Simulator", layout="wide")

st.title("🤖 AI Powered ATM Transaction System")

# session variables
if "step" not in st.session_state:
    st.session_state.step = 0

if "user" not in st.session_state:
    st.session_state.user = None

if "card_verified" not in st.session_state:
    st.session_state.card_verified = False

if "pin_verified" not in st.session_state:
    st.session_state.pin_verified = False

if "amount" not in st.session_state:
    st.session_state.amount = 0

col1, col2 = st.columns(2)

# LEFT SIDE (ATM INTERFACE)
with col1:

    st.subheader("🏧 ATM Interface")

    # CARD VERIFICATION
    if not st.session_state.card_verified:

        card = st.text_input("Enter 12 Digit Card Number")

        if st.button("Insert Card"):

            if card in accounts:
                st.session_state.user = accounts[card]
                st.session_state.card_verified = True
                st.success(f"Welcome {accounts[card]['name']}")
                st.session_state.current_step = "Insert Card"

            else:
                st.error("Invalid Card Number")

    # PIN VERIFICATION
    elif not st.session_state.pin_verified:

        pin = st.text_input("Enter 4 Digit PIN", type="password")

        if st.button("Enter PIN"):

            if pin == st.session_state.user["pin"]:
                st.session_state.pin_verified = True
                st.success("PIN Verified")
                st.session_state.current_step = "Enter PIN"

            else:
                st.error("Incorrect PIN")

    # TRANSACTIONS
    else:

        st.write("Account Holder:", st.session_state.user["name"])
        st.write("Balance: ₹", st.session_state.user["balance"])

        transaction_type = st.selectbox(
            "Select Transaction",
            list(atm_scripts.keys())
        )

        script = atm_scripts[transaction_type]

        current_step = st.selectbox("Current Step", script)

        # WITHDRAW
        if current_step == "Enter Amount":

            amount = st.number_input("Enter Amount", min_value=100)

            if st.button("Confirm Amount"):
                st.session_state.amount = amount

        if current_step == "Confirm Transaction":

            if st.button("Confirm Withdrawal"):

                if st.session_state.amount > st.session_state.user["balance"]:
                    st.error("Insufficient Balance")

                else:
                    st.session_state.user["balance"] -= st.session_state.amount
                    st.success("Cash Dispensed")

        # DEPOSIT
        if current_step == "Confirm Deposit":

            if st.button("Confirm Deposit"):
                st.session_state.user["balance"] += st.session_state.amount
                st.success("Deposit Successful")

        # DISPLAY BALANCE
        if current_step == "Display Balance":
            st.success(f"Your Balance is ₹{st.session_state.user['balance']}")

        # PRINT RECEIPT
        if current_step == "Print Receipt":

            txn_id = random.randint(100000, 999999)

            receipt = f"""
-------------------------------
ATM TRANSACTION RECEIPT
-------------------------------
Transaction ID: {txn_id}
Name: {st.session_state.user['name']}
Transaction Type: {transaction_type}
Amount: ₹{st.session_state.amount}
Balance: ₹{st.session_state.user['balance']}
Date: {datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
Status: SUCCESS
-------------------------------
"""

            st.code(receipt)

            st.download_button(
                label="Download Receipt",
                data=receipt,
                file_name="atm_receipt.txt",
                mime="text/plain"
            )


# RIGHT SIDE (AI PREDICTION)
with col2:

    st.subheader("🧠 AI Prediction Engine")

    if st.session_state.card_verified and st.session_state.pin_verified:

        try:
            prediction = predict_next_action(script, current_step)
            st.info(f"Predicted Next Step: {prediction}")
        except:
            st.write("Start transaction to see prediction")
