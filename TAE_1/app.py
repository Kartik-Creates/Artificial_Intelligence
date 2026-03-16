import streamlit as st
import random
import datetime
import time
from scripts import atm_scripts, predict_next_action, accounts

# Page configuration
st.set_page_config(
    page_title="ATM Transaction Simulator",
    page_icon="🏧",
    layout="wide"
)

# Custom CSS for better styling and animations
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Card styling */
    .atm-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
    }
    
    /* Balance display */
    .balance-display {
        background: linear-gradient(135deg, #141E30 0%, #243B55 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        font-size: 2rem;
        font-weight: bold;
    }
    
    /* Step indicator */
    .step-indicator {
        background-color: #f8f9fa;
        border-left: 5px solid #667eea;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        animation: slideIn 0.5s ease;
    }
    
    /* Animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Success message animation */
    .success-message {
        animation: slideIn 0.5s ease;
        padding: 1rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #155724;
    }
    
    /* Receipt styling */
    .receipt {
        background-color: #fff;
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 1.5rem;
        font-family: monospace;
        animation: slideIn 0.5s ease;
    }
    
    /* Progress bar */
    .progress-container {
        background-color: #e9ecef;
        border-radius: 10px;
        height: 10px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transition: width 0.3s ease;
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
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #2c3e50;">ATM Transaction Simulator</h1>
    <p style="color: #7f8c8d; font-size: 1.1rem;">Experience AI-powered banking transactions</p>
</div>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([3, 2], gap="large")

# Left column - ATM Interface
with col1:
    st.markdown('<div class="atm-card">', unsafe_allow_html=True)
    st.markdown("### ATM Interface")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Card Verification
    if not st.session_state.card_verified:
        st.markdown('<div class="step-indicator">Step 1: Card Verification</div>', unsafe_allow_html=True)
        card_number = st.text_input("Enter 12-digit ATM Card Number", 
                                    placeholder="e.g., 123456789012",
                                    max_chars=12)
        
        if st.button("Insert Card", use_container_width=True):
            if len(card_number) != 12 or not card_number.isdigit():
                st.error("Please enter a valid 12-digit card number")
            elif card_number in accounts:
                st.session_state.user = accounts[card_number]
                st.session_state.card_verified = True
                st.success(f"Welcome, {accounts[card_number]['name']}!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Invalid card number. Please try again.")
    
    # PIN Verification
    elif not st.session_state.pin_verified:
        st.markdown('<div class="step-indicator">Step 2: PIN Verification</div>', unsafe_allow_html=True)
        st.info(f"Card Holder: {st.session_state.user['name']}")
        
        pin = st.text_input("Enter 4-digit PIN", 
                           type="password",
                           placeholder="****",
                           max_chars=4)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Verify PIN", use_container_width=True):
                if pin == st.session_state.user["pin"]:
                    st.session_state.pin_verified = True
                    st.success("PIN verified successfully!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Incorrect PIN. Please try again.")
        
        with col_btn2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.card_verified = False
                st.session_state.user = None
                st.rerun()
    
    # Main ATM Operations
    else:
        # Account info and balance
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.markdown(f"**Account Holder:** {st.session_state.user['name']}")
        with col_info2:
            st.markdown(f"**Card:** **** **** **** {st.session_state.user['card'][-4:]}")
        
        st.markdown(f"""
        <div class="balance-display">
            Current Balance<br>
            <span style="font-size: 2.5rem;">₹{st.session_state.user['balance']:,}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Transaction selection (only shown at step 0)
        if st.session_state.step == 0:
            st.markdown('<div class="step-indicator">Select Transaction Type</div>', unsafe_allow_html=True)
            
            # Transaction buttons in grid
            col_txn1, col_txn2, col_txn3 = st.columns(3)
            
            with col_txn1:
                if st.button("💰 Withdraw Cash", use_container_width=True):
                    st.session_state.transaction_type = "Withdraw Cash"
                    st.session_state.step = 1
                    st.rerun()
            
            with col_txn2:
                if st.button("📥 Deposit Money", use_container_width=True):
                    st.session_state.transaction_type = "Deposit Money"
                    st.session_state.step = 1
                    st.rerun()
            
            with col_txn3:
                if st.button("📊 Check Balance", use_container_width=True):
                    st.session_state.transaction_type = "Check Balance"
                    st.session_state.step = 1
                    st.rerun()
            
            # Logout button
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.clear()
                st.rerun()
        
        # Transaction flow
        else:
            script = atm_scripts[st.session_state.transaction_type]
            current_step = script[st.session_state.step]
            
            # Progress bar
            progress = (st.session_state.step) / (len(script) - 1)
            st.markdown(f"""
            <div class="progress-container">
                <div class="progress-bar" style="width: {progress*100}%;"></div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f'<div class="step-indicator">Step {st.session_state.step}/{len(script)-1}: {current_step}</div>', unsafe_allow_html=True)
            
            # Handle different steps
            if current_step == "Select Withdraw":
                if st.button("Proceed to Withdraw", use_container_width=True):
                    st.session_state.step += 1
                    st.rerun()
            
            elif current_step == "Select Deposit":
                if st.button("Proceed to Deposit", use_container_width=True):
                    st.session_state.step += 1
                    st.rerun()
            
            elif current_step == "Check Balance":
                if st.button("Check Balance", use_container_width=True):
                    st.session_state.step += 1
                    st.rerun()
            
            elif current_step == "Enter Amount":
                amount = st.number_input("Enter amount (₹100 min)", 
                                        min_value=100, 
                                        step=100,
                                        value=100)
                
                col_amt1, col_amt2 = st.columns(2)
                with col_amt1:
                    if st.button("Confirm Amount", use_container_width=True):
                        st.session_state.amount = amount
                        st.session_state.step += 1
                        st.rerun()
                
                with col_amt2:
                    if st.button("Cancel", use_container_width=True):
                        st.session_state.step = 0
                        st.session_state.transaction_type = None
                        st.rerun()
            
            elif current_step == "Confirm Transaction":
                st.markdown(f"""
                <div style="background: #e8f4f8; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <h4>Confirm Withdrawal</h4>
                    <p>Amount: <strong>₹{st.session_state.amount:,}</strong></p>
                    <p>Available Balance: <strong>₹{st.session_state.user['balance']:,}</strong></p>
                    <p>New Balance: <strong>₹{st.session_state.user['balance'] - st.session_state.amount:,}</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.amount > st.session_state.user["balance"]:
                    st.error("Insufficient balance for this withdrawal")
                else:
                    col_conf1, col_conf2 = st.columns(2)
                    with col_conf1:
                        if st.button("✅ Confirm", use_container_width=True):
                            st.session_state.user["balance"] -= st.session_state.amount
                            st.session_state.transaction_history.append({
                                'type': 'Withdrawal',
                                'amount': st.session_state.amount,
                                'date': datetime.datetime.now()
                            })
                            st.session_state.step += 1
                            st.rerun()
                    
                    with col_conf2:
                        if st.button("❌ Cancel", use_container_width=True):
                            st.session_state.step = 0
                            st.session_state.transaction_type = None
                            st.rerun()
            
            elif current_step == "Confirm Deposit":
                st.markdown(f"""
                <div style="background: #e8f4f8; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <h4>Confirm Deposit</h4>
                    <p>Amount: <strong>₹{st.session_state.amount:,}</strong></p>
                    <p>New Balance: <strong>₹{st.session_state.user['balance'] + st.session_state.amount:,}</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                col_conf1, col_conf2 = st.columns(2)
                with col_conf1:
                    if st.button("✅ Confirm Deposit", use_container_width=True):
                        st.session_state.user["balance"] += st.session_state.amount
                        st.session_state.transaction_history.append({
                            'type': 'Deposit',
                            'amount': st.session_state.amount,
                            'date': datetime.datetime.now()
                        })
                        st.session_state.step += 1
                        st.rerun()
                
                with col_conf2:
                    if st.button("❌ Cancel", use_container_width=True):
                        st.session_state.step = 0
                        st.session_state.transaction_type = None
                        st.rerun()
            
            elif current_step == "Dispense Cash":
                st.markdown(f"""
                <div class="success-message">
                    <h3 style="margin:0;">✅ Cash Dispensed Successfully</h3>
                    <p style="font-size: 2rem; margin:0;">₹{st.session_state.amount:,}</p>
                    <p>Please collect your cash</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Continue", use_container_width=True):
                    st.session_state.step += 1
                    st.rerun()
            
            elif current_step == "Display Balance":
                st.markdown(f"""
                <div class="success-message">
                    <h3 style="margin:0;">💰 Current Balance</h3>
                    <p style="font-size: 2rem; margin:0;">₹{st.session_state.user['balance']:,}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Continue", use_container_width=True):
                    st.session_state.step += 1
                    st.rerun()
            
            elif current_step == "Print Receipt":
                txn_id = random.randint(100000, 999999)
                
                st.markdown(f"""
                <div class="receipt">
                    <h4 style="text-align: center; margin-bottom: 1rem;">ATM Transaction Receipt</h4>
                    <hr>
                    <p><strong>Transaction ID:</strong> {txn_id}</p>
                    <p><strong>Account Holder:</strong> {st.session_state.user['name']}</p>
                    <p><strong>Date & Time:</strong> {datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}</p>
                    <p><strong>Transaction Type:</strong> {st.session_state.transaction_type}</p>
                    <p><strong>Amount:</strong> ₹{st.session_state.amount:,}</p>
                    <p><strong>Available Balance:</strong> ₹{st.session_state.user['balance']:,}</p>
                    <hr>
                    <p style="text-align: center; color: #28a745;">✓ Transaction Successful</p>
                    <p style="text-align: center; font-size: 0.9rem;">Thank you for banking with us</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Download receipt
                receipt_text = f"""
ATM TRANSACTION RECEIPT
------------------------
Transaction ID: {txn_id}
Account Holder: {st.session_state.user['name']}
Date: {datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
Transaction Type: {st.session_state.transaction_type}
Amount: ₹{st.session_state.amount:,}
Available Balance: ₹{st.session_state.user['balance']:,}
Status: SUCCESS
------------------------
Thank you for banking with us
                """
                
                st.download_button(
                    label="📥 Download Receipt",
                    data=receipt_text,
                    file_name=f"receipt_{txn_id}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
                col_end1, col_end2 = st.columns(2)
                with col_end1:
                    if st.button("New Transaction", use_container_width=True):
                        st.session_state.step = 0
                        st.session_state.transaction_type = None
                        st.session_state.amount = 0
                        st.rerun()
                
                with col_end2:
                    if st.button("Logout", use_container_width=True):
                        st.session_state.clear()
                        st.rerun()

# Right column - AI Prediction and History
with col2:
    st.markdown('<div class="atm-card">', unsafe_allow_html=True)
    st.markdown("### AI Prediction Engine")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.transaction_type and st.session_state.step > 0:
        script = atm_scripts[st.session_state.transaction_type]
        current_step = script[st.session_state.step]
        
        prediction = predict_next_action(script, current_step)
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; 
                    border-radius: 15px; 
                    color: white;
                    margin: 1rem 0;">
            <h4 style="margin:0 0 1rem 0;">Next Step Prediction</h4>
            <p style="font-size: 1.2rem; margin:0;">Current: {current_step}</p>
            <div style="font-size: 3rem; text-align: center; margin: 1rem 0;">⬇️</div>
            <p style="font-size: 1.5rem; margin:0; text-align: center;">{prediction}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Confidence meter
        confidence = random.randint(85, 99)
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <p>Prediction Confidence</p>
            <div class="progress-container">
                <div class="progress-bar" style="width: {confidence}%;"></div>
            </div>
            <p style="text-align: right;">{confidence}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("AI analyzes transaction patterns to predict the next step in real-time")
    
    # Transaction history
    if st.session_state.transaction_history:
        st.markdown("### Recent Transactions")
        for txn in st.session_state.transaction_history[-3:]:
            st.markdown(f"""
            <div style="background: #f8f9fa; 
                        padding: 0.75rem; 
                        border-radius: 8px; 
                        margin: 0.5rem 0;
                        border-left: 3px solid #667eea;">
                <strong>{txn['type']}</strong> - ₹{txn['amount']:,}<br>
                <small>{txn['date'].strftime("%H:%M:%S")}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Quick tips
    st.markdown("### Quick Tips")
    tips = [
        "Minimum withdrawal amount: ₹100",
        "Always collect your card after transaction",
        "Check balance regularly to avoid overdraft",
        "Keep your PIN confidential"
    ]
    for tip in tips:
        st.markdown(f"• {tip}")
