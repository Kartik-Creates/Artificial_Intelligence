# scripts.py

atm_scripts = {
    "Withdraw Cash": [
        "Select Withdraw",
        "Enter Amount",
        "Confirm Transaction",
        "Dispense Cash",
        "Print Receipt"
    ],

    "Check Balance": [
        "Check Balance",
        "Display Balance",
        "Print Receipt"
    ],

    "Deposit Money": [
        "Select Deposit",
        "Enter Amount",
        "Confirm Deposit",
        "Print Receipt"
    ]
}

# Fake ATM database with card objects
accounts = {
    "123456789012": {
        "name": "Rahul Sharma", 
        "pin": "1234", 
        "balance": 25000,
        "card": "123456789012"
    },
    "234567890123": {
        "name": "Priya Verma", 
        "pin": "2345", 
        "balance": 32000,
        "card": "234567890123"
    },
    "345678901234": {
        "name": "Amit Patel", 
        "pin": "3456", 
        "balance": 18000,
        "card": "345678901234"
    },
    "456789012345": {
        "name": "Sneha Gupta", 
        "pin": "4567", 
        "balance": 41000,
        "card": "456789012345"
    },
    "567890123456": {
        "name": "Vikram Singh", 
        "pin": "5678", 
        "balance": 15000,
        "card": "567890123456"
    },
    "678901234567": {
        "name": "Neha Joshi", 
        "pin": "6789", 
        "balance": 27000,
        "card": "678901234567"
    },
    "789012345678": {
        "name": "Rohit Mehta", 
        "pin": "7890", 
        "balance": 35000,
        "card": "789012345678"
    },
    "890123456789": {
        "name": "Anjali Nair", 
        "pin": "1111", 
        "balance": 22000,
        "card": "890123456789"
    },
    "901234567890": {
        "name": "Karan Kapoor", 
        "pin": "2222", 
        "balance": 50000,
        "card": "901234567890"
    },
    "112233445566": {
        "name": "Pooja Shah", 
        "pin": "3333", 
        "balance": 29000,
        "card": "112233445566"
    }
}

def predict_next_action(script, current_step):
    try:
        index = script.index(current_step)
        if index + 1 < len(script):
            return script[index + 1]
        return "Transaction Complete"
    except ValueError:
        return "Start Transaction"
