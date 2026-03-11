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


# Fake ATM database
accounts = {
    "123456789012": {"name": "Rahul Sharma", "pin": "1234", "balance": 25000},
    "234567890123": {"name": "Priya Verma", "pin": "2345", "balance": 32000},
    "345678901234": {"name": "Amit Patel", "pin": "3456", "balance": 18000},
    "456789012345": {"name": "Sneha Gupta", "pin": "4567", "balance": 41000},
    "567890123456": {"name": "Vikram Singh", "pin": "5678", "balance": 15000},
    "678901234567": {"name": "Neha Joshi", "pin": "6789", "balance": 27000},
    "789012345678": {"name": "Rohit Mehta", "pin": "7890", "balance": 35000},
    "890123456789": {"name": "Anjali Nair", "pin": "1111", "balance": 22000},
    "901234567890": {"name": "Karan Kapoor", "pin": "2222", "balance": 50000},
    "112233445566": {"name": "Pooja Shah", "pin": "3333", "balance": 29000}
}


def predict_next_action(script, current_step):
    try:
        index = script.index(current_step)
        return script[index + 1]
    except IndexError:
        return "Transaction Complete"
