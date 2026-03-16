import streamlit as st
import random
import datetime
import time
from scripts import atm_scripts, predict_next_action, accounts

# Page configuration
st.set_page_config(
    page_title="ATM Simulator",
    page_icon="🏧",
    layout="centered"
)

# Custom CSS for navy blue theme
st.markdown("""
<style>
    /* Global theme */
    .stApp {
        background: linear-gradient(135deg, #0B1E33 0%, #1A2F4A 100%);
    }
    
    /* Main container */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* ATM Header */
    .atm-header {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(135deg, #0A1929 0%, #1A3A4A 100%);
        border-radius: 15px;
        border: 1px solid #2C4C6B;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .atm-header h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: 2px;
    }
    
    .atm-header p {
        color: #A0C0E0;
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
    }
    
    /* Card styling */
    .atm-card {
        background: linear-gradient(135deg, #0F2A40 0%, #1C3F5C 100%);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid #2C5A7A;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        margin: 1rem 0;
        color: white;
    }
    
    .atm-card h3 {
        color: #B0E0FF;
        margin-top: 0;
        border-bottom: 2px solid #2C5A7A;
        padding-bottom: 0.75rem;
        font-size: 1.3rem;
    }
    
    /* Balance display */
    .balance-display {
        background: linear-gradient(135deg, #0A1E2F 0%, #15344D 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid #2C5A7A;
        margin: 1.5rem 0;
    }
    
    .balance-label {
        color: #A0C0E0;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .balance-amount {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Step indicator */
    .step-indicator {
        background: linear-gradient(135deg, #0A1E2F 0%, #1A3A50 100%);
        border-left: 5px solid #4A9EFF;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        font-size: 1.1rem;
        border: 1px solid #2C5A7A;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1A3F5C 0%, #2C5A7A 100%);
        color: white;
        border: 1px solid #4A9EFF;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2C5A7A 0%, #1A3F5C 100%);
        border-color: #6AB0FF;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(74, 158, 255, 0.3);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: #0A1E2F;
        border: 2px solid #2C5A7A;
        border-radius: 10px;
        color: white;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4A9EFF;
        box-shadow: 0 0 0 2px rgba(74, 158, 255, 0.2);
    }
    
    .stNumberInput > div > div > input {
        background: #0A1E2F;
        border: 2px solid #2C5A7A;
        border-radius: 10px;
        color: white;
    }
    
    /* Success/Error messages */
    .success-box {
        background: linear-gradient(135deg, #0A3A2A 0%, #1A4A3A 100%);
        border: 2px solid #2A9A7A;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        color: white;
        margin: 1rem 0;
        animation: fadeIn 0.5s ease;
    }
    
    .error-box {
        background: linear-gradient(135deg, #3A1A1A 0%, #4A2A2A 100%);
        border: 2px solid #9A4A4A;
        border-radius: 15px;
        padding: 1rem;
        color: white;
        margin: 1rem 0;
    }
    
    /* Receipt styling */
    .receipt-box {
        background: #0A1A2A;
        border: 2px dashed #4A9EFF;
        border-radius: 15px;
        padding: 1.5rem;
        font-family: 'Courier New', monospace;
        color: #B0E0FF;
        margin: 1rem 0;
    }
    
    /* Progress bar */
    .progress-container {
        background: #0A1A2A;
        border-radius: 10px;
        height: 8px;
        margin: 1rem 0;
        overflow: hidden;
        border: 1px solid #2C5A7A;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #4A9EFF 0%, #6AB0FF 100%);
        transition: width 0.3s ease;
    }
    
    /* Transaction grid */
    .txn-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin: 1rem 0;
    }
    
    /* Info text */
    .info-text {
        color: #A0C0E0;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    
    /* Confirmation box */
    .confirm-box {
        background: #0A1E2F;
        border: 2px solid #2C5A7A;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .confirm-row {
        display: flex;
        justify-content: space-between;
        padding: 0.75rem 0;
        border-bottom: 1px solid #2C5A7A;
        color: white;
    }
    
    .confirm-row:last-child {
        border-bottom: none;
    }
    
    .confirm-label {
        color: #A0C0E0;
    }
    
    .confirm-value {
        color: #4A9EFF;
        font-weight: bold;
    }
    
    /* History item */
    .history-item {
        background: #0A1E2F;
        border-left: 3px solid #4A9EFF;
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        color: white;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if "card_verified" not in st.session_state:
        st.session_state.card_verified = False
    if "pin_verified" not in st.session_state:
        st.session_state.pin_verified = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "amount" not in st.session_state:
        st.session_state.amount = 0
    if "transaction_type" not in st.session_state:
        st.session_state.transaction_type = None
    if "transaction_history" not in st.session_state:
        st.session_state.transaction_history = []

init_session_state()

# Header
st.markdown("""
<div class="atm-header">
    <h1>ATM</h1>
    <p>AI-Powered Banking Simulator</p>
</div>
""", unsafe_allow_html=True)

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Create two columns with equal width
col1, col2 = st.columns(2, gap="large")

# Left Column - ATM Interface
with col1:
    st.markdown('<div class="atm-card">', unsafe_allow_html=True)
    st.markdown("<h3>ATM Interface</h3>", unsafe_allow_html=True)
    
    # Card Verification
    if not st.session_state.card_verified:
        st.markdown('<div class="step-indicator">Step 1: Insert Card</div>', unsafe_allow_html=True)
        card_number = st.text_input("Card Number", 
                                    placeholder="1234 5678 9012",
                                    max_chars=12,
                                    key="card_input")
        
        if st.button("Insert Card", key="insert_btn"):
            if len(card_number) != 12 or not card_number.isdigit():
                st.markdown('<div class="error-box">Invalid card number</div>', unsafe_allow_html=True)
            elif card_number in accounts:
                st.session_state.user = accounts[card_number]
                st.session_state.card_verified = True
                st.rerun()
            else:
                st.markdown('<div class="error-box">Card not recognized</div>', unsafe_allow_html=True)
    
    # PIN Verification
    elif not st.session_state.pin_verified:
        st.markdown('<div class="step-indicator">Step 2: Enter PIN</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-text">Card: **** **** **** {st.session_state.user["card"][-4:]}</div>', unsafe_allow_html=True)
        
        pin = st.text_input("PIN", 
                           type="password",
                           placeholder="****",
                           max_chars=4,
                           key="pin_input")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Verify", key="verify_btn"):
                if pin == st.session_state.user["pin"]:
                    st.session_state.pin_verified = True
                    st.rerun()
                else:
                    st.markdown('<div class="error-box">Incorrect PIN</div>', unsafe_allow_html=True)
        
        with col_btn2:
            if st.button("Cancel", key="cancel_pin_btn"):
                st.session_state.card_verified = False
                st.session_state.user = None
                st.rerun()
    
    # Main ATM Operations
    else:
        # Account info
        st.markdown(f'<div class="info-text">Account: {st.session_state.user["name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-text">Card: **** **** **** {st.session_state.user["card"][-4:]}</div>', unsafe_allow_html=True)
        
        # Balance display
        st.markdown(f"""
        <div class="balance-display">
            <div class="balance-label">Current Balance</div>
            <div class="balance-amount">₹{st.session_state.user['balance']:,}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Transaction selection
        if st.session_state.step == 0:
            st.markdown('<div class="step-indicator">Select Transaction</div>', unsafe_allow_html=True)
            
            # Transaction buttons in 2x2 grid
            st.markdown('<div class="txn-grid">', unsafe_allow_html=True)
            
            col_txn1, col_txn2 = st.columns(2)
            with col_txn1:
                if st.button("Withdraw", key="withdraw_btn"):
                    st.session_state.transaction_type = "Withdraw Cash"
                    st.session_state.step = 1
                    st.rerun()
            
            with col_txn2:
                if st.button("Deposit", key="deposit_btn"):
                    st.session_state.transaction_type = "Deposit Money"
                    st.session_state.step = 1
                    st.rerun()
            
            col_txn3, col_txn4 = st.columns(2)
            with col_txn3:
                if st.button("Balance", key="balance_btn"):
                    st.session_state.transaction_type = "Check Balance"
                    st.session_state.step = 1
                    st.rerun()
            
            with col_txn4:
                if st.button("Logout", key="logout_btn"):
                    st.session_state.clear()
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Transaction flow
        else:
            script = atm_scripts[st.session_state.transaction_type]
            current_step = script[st.session_state.step]
            
            # Progress
            progress = (st.session_state.step) / (len(script) - 1)
            st.markdown(f"""
            <div class="progress-container">
                <div class="progress-bar" style="width: {progress*100}%;"></div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f'<div class="step-indicator">{current_step}</div>', unsafe_allow_html=True)
            
            # Handle steps
            if current_step == "Select Withdraw":
                if st.button("Continue to Withdraw", key="cont_withdraw"):
                    st.session_state.step += 1
                    st.rerun()
            
            elif current_step == "Select Deposit":
                if st.button("Continue to Deposit", key="cont_deposit"):
                    st.session_state.step += 1
                    st.rerun()
            
            elif current_step == "Check Balance":
                if st.button("View Balance", key="view_balance"):
                    st.session_state.step += 1
                    st.rerun()
            
            elif current_step == "Enter Amount":
                amount = st.number_input("Amount (₹)", 
                                        min_value=100, 
                                        step=100,
                                        value=100,
                                        key="amount_input")
                
                col_amt1, col_amt2 = st.columns(2)
                with col_amt1:
                    if st.button("Confirm", key="confirm_amt"):
                        st.session_state.amount = amount
                        st.session_state.step += 1
                        st.rerun()
                
                with col_amt2:
                    if st.button("Back", key="back_amt"):
                        st.session_state.step = 0
                        st.session_state.transaction_type = None
                        st.rerun()
            
            elif current_step == "Confirm Transaction":
                st.markdown(f"""
                <div class="confirm-box">
                    <div class="confirm-row">
                        <span class="confirm-label">Amount to Withdraw:</span>
                        <span class="confirm-value">₹{st.session_state.amount:,}</span>
                    </div>
                    <div class="confirm-row">
                        <span class="confirm-label">Current Balance:</span>
                        <span class="confirm-value">₹{st.session_state.user['balance']:,}</span>
                    </div>
                    <div class="confirm-row">
                        <span class="confirm-label">New Balance:</span>
                        <span class="confirm-value">₹{st.session_state.user['balance'] - st.session_state.amount:,}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.amount > st.session_state.user["balance"]:
                    st.markdown('<div class="error-box">Insufficient Balance</div>', unsafe_allow_html=True)
                else:
                    col_conf1, col_conf2 = st.columns(2)
                    with col_conf1:
                        if st.button("Confirm", key="conf_withdraw"):
                            st.session_state.user["balance"] -= st.session_state.amount
                            st.session_state.transaction_history.append({
                                'type': 'Withdrawal',
                                'amount': st.session_state.amount
                            })
                            st.session_state.step += 1
                            st.rerun()
                    
                    with col_conf2:
                        if st.button("Cancel", key="cancel_withdraw"):
                            st.session_state.step = 0
                            st.session_state.transaction_type = None
                            st.rerun()
            
            elif current_step == "Confirm Deposit":
                st.markdown(f"""
                <div class="confirm-box">
                    <div class="confirm-row">
                        <span class="confirm-label">Amount to Deposit:</span>
                        <span class="confirm-value">₹{st.session_state.amount:,}</span>
                    </div>
                    <div class="confirm-row">
                        <span class="confirm-label">Current Balance:</span>
                        <span class="confirm-value">₹{st.session_state.user['balance']:,}</span>
                    </div>
                    <div class="confirm-row">
                        <span class="confirm-label">New Balance:</span>
                        <span class="confirm-value">₹{st.session_state.user['balance'] + st.session_state.amount:,}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col_conf1, col_conf2 = st.columns(2)
                with col_conf1:
                    if st.button("Confirm", key="conf_deposit"):
                        st.session_state.user["balance"] += st.session_state.amount
                        st.session_state.transaction_history.append({
                            'type': 'Deposit',
                            'amount': st.session_state.amount
                        })
                        st.session_state.step += 1
                        st.rerun()
                
                with col_conf2:
                    if st.button("Cancel", key="cancel_deposit"):
                        st.session_state.step = 0
                        st.session_state.transaction_type = None
                        st.rerun()
            
            elif current_step == "Dispense Cash":
                st.markdown(f"""
                <div class="success-box">
                    <div style="font-size: 1.5rem; margin-bottom: 1rem;">✓ Cash Dispensed</div>
                    <div style="font-size: 2.5rem; font-weight: bold;">₹{st.session_state.amount:,}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Continue", key="cont_dispense"):
                    st.session_state.step += 1
                    st.rerun()
            
            elif current_step == "Display Balance":
                st.markdown(f"""
                <div class="success-box">
                    <div style="font-size: 1.2rem; margin-bottom: 1rem;">Available Balance</div>
                    <div style="font-size: 2.5rem; font-weight: bold;">₹{st.session_state.user['balance']:,}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Continue", key="cont_balance"):
                    st.session_state.step += 1
                    st.rerun()
            
            elif current_step == "Print Receipt":
                txn_id = random.randint(100000, 999999)
                
                st.markdown(f"""
                <div class="receipt-box">
                    <div style="text-align: center; margin-bottom: 1rem;">ATM Receipt</div>
                    <div style="border-top: 1px dashed #4A9EFF; border-bottom: 1px dashed #4A9EFF; padding: 1rem 0;">
                        <div style="display: flex; justify-content: space-between;">
                            <span>ID:</span> <span>{txn_id}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span>Type:</span> <span>{st.session_state.transaction_type}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span>Amount:</span> <span>₹{st.session_state.amount:,}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span>Balance:</span> <span>₹{st.session_state.user['balance']:,}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span>Date:</span> <span>{datetime.datetime.now().strftime("%d/%m/%y %H:%M")}</span>
                        </div>
                    </div>
                    <div style="text-align: center; margin-top: 1rem;">Thank You</div>
                </div>
                """, unsafe_allow_html=True)
                
                col_end1, col_end2 = st.columns(2)
                with col_end1:
                    if st.button("New Transaction", key="new_txn"):
                        st.session_state.step = 0
                        st.session_state.transaction_type = None
                        st.rerun()
                
                with col_end2:
                    if st.button("Logout", key="final_logout"):
                        st.session_state.clear()
                        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Right Column - AI Engine
with col2:
    st.markdown('<div class="atm-card">', unsafe_allow_html=True)
    st.markdown("<h3>AI Engine</h3>", unsafe_allow_html=True)
    
    if st.session_state.transaction_type and st.session_state.step > 0:
        script = atm_scripts[st.session_state.transaction_type]
        current_step = script[st.session_state.step]
        prediction = predict_next_action(script, current_step)
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0A1E2F 0%, #1A3A50 100%); 
                    border: 2px solid #4A9EFF;
                    border-radius: 15px; 
                    padding: 1.5rem; 
                    margin: 1rem 0;
                    text-align: center;">
            <div style="color: #A0C0E0; margin-bottom: 1rem;">Next Step Prediction</div>
            <div style="color: #4A9EFF; font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">{prediction}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Confidence
        confidence = random.randint(92, 99)
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; color: #A0C0E0; margin-bottom: 0.5rem;">
                <span>Confidence</span>
                <span>{confidence}%</span>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {confidence}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="info-text">AI predicts next step based on transaction patterns</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #0A1E2F; 
                    border: 2px solid #2C5A7A;
                    border-radius: 15px; 
                    padding: 2rem; 
                    text-align: center;
                    margin: 1rem 0;">
            <div style="color: #4A9EFF; font-size: 1.2rem; margin-bottom: 1rem;">🤖</div>
            <div style="color: #A0C0E0;">Ready to predict</div>
            <div style="color: #4A9EFF; font-size: 0.9rem; margin-top: 1rem;">Start a transaction</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Transaction History
    if st.session_state.transaction_history:
        st.markdown("<h3 style='color: #B0E0FF; margin: 1rem 0 0.5rem 0;'>History</h3>", unsafe_allow_html=True)
        for txn in st.session_state.transaction_history[-3:]:
            st.markdown(f"""
            <div class="history-item">
                <div style="display: flex; justify-content: space-between;">
                    <span>{txn['type']}</span>
                    <span style="color: #4A9EFF;">₹{txn['amount']:,}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Quick Tips
    st.markdown("<h3 style='color: #B0E0FF; margin: 1rem 0 0.5rem 0;'>Tips</h3>", unsafe_allow_html=True)
    tips = [
        "Min withdrawal: ₹100",
        "Keep PIN secure",
        "Check balance regularly",
        "Take your receipt"
    ]
    for tip in tips:
        st.markdown(f'<div class="info-text">• {tip}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
