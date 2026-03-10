# scripts.py

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