import random
import datetime

atm_scripts = {
    "Withdraw Cash": [
        "Insert Card",
        "Enter PIN",
        "Select Withdraw",
        "Enter Amount",
        "Confirm Transaction",
        "Dispense Cash",
        "Print Receipt"
    ],
    "Check Balance": [
        "Insert Card",
        "Enter PIN",
        "Check Balance",
        "Display Balance",
        "Print Receipt"
    ],
    "Deposit Money": [
        "Insert Card",
        "Enter PIN",
        "Select Deposit",
        "Enter Amount",
        "Confirm Deposit",
        "Print Receipt"
    ]
}


def predict_next_action(script, current_step):
    try:
        index = script.index(current_step)
        return script[index + 1]
    except IndexError:
        return "Transaction Complete"


def generate_receipt(txn_type, amount, balance):
    txn_id = random.randint(100000, 999999)
    now = datetime.datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    time_str = now.strftime("%H:%M:%S")
    receipt = f"""
================================
      NEXUS FINANCIAL ATM
       TERMINAL — 042
================================
TXN ID  : {txn_id}
DATE    : {date_str}
TIME    : {time_str}
--------------------------------
TYPE    : {txn_type}
AMOUNT  : Rs.{amount:,.0f}
BALANCE : Rs.{balance:,.0f}
--------------------------------
STATUS  : SUCCESS
AUTH    : APPROVED
================================
    Thank You For Banking!
================================
"""
    return receipt, txn_id
