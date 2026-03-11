import streamlit as st
import random
import datetime
from scripts import atm_scripts, predict_next_action

st.set_page_config(page_title="AI ATM Simulator", layout="wide")

st.title("🤖 AI ATM Transaction Simulator")

# CARD VERIFICATION
if not st.session_state.card_verified:

    card_number = st.text_input("Enter 12 Digit ATM Card Number")

    if st.button("Insert Card"):

        # check card format
        if len(card_number) != 12 or not card_number.isdigit():
            st.error("Card number must be 12 digits")

        elif card_number in accounts:

            # load user data
            st.session_state.user = accounts[card_number]
            st.session_state.card_verified = True

            st.success(f"Welcome {accounts[card_number]['name']}")

        else:
            st.error("Invalid Card Number")

# PIN VERIFICATION
elif not st.session_state.pin_verified:

    pin = st.text_input("Enter 4 Digit PIN", type="password")

    if st.button("Verify PIN"):

        if pin == st.session_state.user["pin"]:

            st.session_state.pin_verified = True
            st.success("PIN Verified Successfully")

        else:
            st.error("Incorrect PIN")

# initialize session variables
if "step" not in st.session_state:
    st.session_state.step = 0

if "balance" not in st.session_state:
    st.session_state.balance = 25000

if "transaction_type" not in st.session_state:
    st.session_state.transaction_type = "Withdraw Cash"

if "amount" not in st.session_state:
    st.session_state.amount = 0

# transaction selection
st.session_state.transaction_type = st.selectbox(
    "Select Transaction Type",
    list(atm_scripts.keys())
)

script = atm_scripts[st.session_state.transaction_type]

# reset step if transaction type changes
if st.session_state.step >= len(script):
    st.session_state.step = 0

current_step = script[st.session_state.step]

col1, col2 = st.columns(2)

# LEFT SIDE - ATM INTERFACE
with col1:

    st.subheader("🏧 ATM Interface")

    st.write("Current Balance: ₹", st.session_state.balance)

    st.write("Current Step:", current_step)

    # INSERT CARD
    if current_step == "Insert Card":

        if st.button("Insert Card"):
            st.session_state.step += 1
            st.rerun()

    # ENTER PIN
    elif current_step == "Enter PIN":

        pin = st.text_input("Enter 4 Digit PIN", type="password")

        if st.button("Submit PIN") and len(pin) == 4:
            st.session_state.step += 1
            st.rerun()

    # WITHDRAW OPTION
    elif current_step == "Select Withdraw":

        if st.button("Withdraw Cash"):
            st.session_state.step += 1
            st.rerun()

    # DEPOSIT OPTION
    elif current_step == "Select Deposit":

        if st.button("Deposit Money"):
            st.session_state.step += 1
            st.rerun()

    # CHECK BALANCE
    elif current_step == "Check Balance":

        if st.button("Check Balance"):
            st.session_state.step += 1
            st.rerun()

    # ENTER AMOUNT
    elif current_step == "Enter Amount":

        amount = st.number_input("Enter Amount", min_value=100, step=100)

        if st.button("Confirm Amount"):

            st.session_state.amount = amount
            st.session_state.step += 1
            st.rerun()

    # CONFIRM TRANSACTION
    elif current_step == "Confirm Transaction":

        if st.session_state.amount > st.session_state.balance:
            st.error("Insufficient Balance")
        else:
            if st.button("Confirm Withdrawal"):
                st.session_state.balance -= st.session_state.amount
                st.session_state.step += 1
                st.rerun()

    # CONFIRM DEPOSIT
    elif current_step == "Confirm Deposit":

        if st.button("Confirm Deposit"):
            st.session_state.balance += st.session_state.amount
            st.session_state.step += 1
            st.rerun()

    # DISPENSE CASH
    elif current_step == "Dispense Cash":

        st.success(f"₹{st.session_state.amount} Dispensed Successfully")

        if st.button("Continue"):
            st.session_state.step += 1
            st.rerun()

    # DISPLAY BALANCE
    elif current_step == "Display Balance":

        st.success(f"Your Balance is ₹{st.session_state.balance}")

        if st.button("Continue"):
            st.session_state.step += 1
            st.rerun()

    # PRINT RECEIPT
    elif current_step == "Print Receipt":

        st.success("Receipt Generated")

        txn_id = random.randint(100000, 999999)

        receipt = f"""
        -----------------------------
              ATM TRANSACTION
        -----------------------------
        Transaction ID : {txn_id}
        Date : {datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}

        Transaction Type : {st.session_state.transaction_type}

        Amount : ₹{st.session_state.amount}

        Available Balance : ₹{st.session_state.balance}

        Status : SUCCESS
        -----------------------------
        Thank You For Banking
        -----------------------------
        """

        st.code(receipt)

        st.download_button(
            label="Download Receipt",
            data=receipt,
            file_name="atm_receipt.txt",
            mime="text/plain"
        )

        if st.button("Finish Transaction"):
            st.session_state.step = 0
            st.session_state.amount = 0
            st.rerun()


# RIGHT SIDE - AI PREDICTION
with col2:

    st.subheader("🧠 AI Prediction Engine")

    prediction = predict_next_action(script, current_step)

    st.info(f"Predicted Next Step: {prediction}")

    st.write("AI is predicting the next user action based on stored transaction scripts.")
