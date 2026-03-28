import streamlit as st
import datetime
from scripts import atm_scripts, predict_next_action, generate_receipt

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI ATM Simulator",
    page_icon="🏧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&family=Orbitron:wght@400;700;900&display=swap');

/* ── Reset & Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #060a0f !important;
    color: #c8e6ff !important;
    font-family: 'Rajdhani', sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse at 20% 50%, rgba(0,100,160,.08) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(0,200,100,.05) 0%, transparent 50%),
        repeating-linear-gradient(0deg,  transparent, transparent 40px, rgba(0,200,255,.015) 40px, rgba(0,200,255,.015) 41px),
        repeating-linear-gradient(90deg, transparent, transparent 60px, rgba(0,200,255,.01)  60px, rgba(0,200,255,.01)  61px),
        #060a0f !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"], footer { display:none !important; }
[data-testid="stSidebar"] { display:none !important; }
section[data-testid="stMain"] > div { padding-top: 1.5rem !important; }
div.block-container { padding: 0 2rem 2rem !important; max-width: 1200px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width:4px }
::-webkit-scrollbar-track { background:#0c1420 }
::-webkit-scrollbar-thumb { background:#1a3a5c; border-radius:2px }

/* ── Streamlit widgets: dark override ── */
div[data-baseweb="select"] > div {
    background:#0c1420 !important;
    border:1px solid #1a3a5c !important;
    border-radius:3px !important;
    color:#c8e6ff !important;
    font-family:'Share Tech Mono',monospace !important;
    font-size:13px !important;
}
div[data-baseweb="select"] * { cursor:pointer !important; color:#c8e6ff !important; }
[data-baseweb="popover"] { background:#0c1420 !important; border:1px solid #1a3a5c !important; }
li[role="option"]:hover { background:rgba(0,200,255,.1) !important; }

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    background:#0c1420 !important;
    border:1px solid #1a3a5c !important;
    color:#ffffff !important;
    font-family:'Share Tech Mono',monospace !important;
    font-size:15px !important;
    letter-spacing:3px !important;
    border-radius:3px !important;
    caret-color:#00c8ff !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
    border-color:#00c8ff !important;
    box-shadow:0 0 15px rgba(0,200,255,.15) !important;
    outline:none !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label {
    color:#4a7090 !important;
    font-family:'Share Tech Mono',monospace !important;
    font-size:11px !important;
    letter-spacing:2px !important;
}
div[data-testid="stNumberInput"] button {
    background:#101c2e !important;
    border-color:#1a3a5c !important;
    color:#4a7090 !important;
}

/* Streamlit buttons */
div[data-testid="stButton"] > button {
    background:linear-gradient(135deg,rgba(0,200,255,.12),rgba(0,200,255,.05)) !important;
    border:1px solid #00c8ff !important;
    color:#00c8ff !important;
    font-family:'Rajdhani',sans-serif !important;
    font-size:13px !important;
    font-weight:700 !important;
    letter-spacing:3px !important;
    text-transform:uppercase !important;
    border-radius:3px !important;
    width:100% !important;
    padding:12px !important;
    transition:all .2s !important;
    cursor:pointer !important;
}
div[data-testid="stButton"] > button:hover {
    background:linear-gradient(135deg,rgba(0,200,255,.22),rgba(0,200,255,.12)) !important;
    box-shadow:0 0 20px rgba(0,200,255,.25) !important;
    transform:none !important;
}
div[data-testid="stButton"] > button:active { transform:scale(.98) !important; }

div[data-testid="stDownloadButton"] > button {
    background:transparent !important;
    border:1px solid #0af0b4 !important;
    color:#0af0b4 !important;
    font-family:'Rajdhani',sans-serif !important;
    font-size:13px !important;
    font-weight:600 !important;
    letter-spacing:2px !important;
    border-radius:3px !important;
    width:100% !important;
    padding:10px !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background:rgba(10,240,180,.08) !important;
    box-shadow:0 0 15px rgba(10,240,180,.2) !important;
}

/* Alert / info / success / error boxes */
div[data-testid="stAlert"] {
    border-radius:3px !important;
    font-family:'Share Tech Mono',monospace !important;
    font-size:12px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
defaults = {
    "step": 0,
    "balance": 25000,
    "txn_type": "Withdraw Cash",
    "amount": 0,
    "txn_count": 0,
    "session_amount": 0,
    "session_id": f"{datetime.datetime.now().strftime('%H%M%S')}-NX042",
    "alert": None,          # ("type", "message")  type ∈ success|error|info|warning
    "pin_ok": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def fmt(n):
    return f"₹{n:,.0f}"


def script():
    return atm_scripts[st.session_state.txn_type]


def cur_step():
    return script()[st.session_state.step]


def advance():
    s = script()
    if st.session_state.step + 1 < len(s):
        st.session_state.step += 1
    st.session_state.alert = None
    st.rerun()


def reset():
    st.session_state.step = 0
    st.session_state.amount = 0
    st.session_state.pin_ok = False
    st.session_state.alert = None
    st.rerun()


def go_to(step_name):
    s = script()
    if step_name in s:
        st.session_state.step = s.index(step_name)
    st.session_state.alert = None
    st.rerun()


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-bottom:24px">
  <div style="font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:6px;color:#4a7090;margin-bottom:4px">NEXUS FINANCIAL NETWORK</div>
  <div style="font-family:'Orbitron',sans-serif;font-size:28px;font-weight:900;color:#00c8ff;
              text-shadow:0 0 30px rgba(0,200,255,.5);letter-spacing:4px">AI ATM SIMULATOR</div>
  <div style="font-size:12px;letter-spacing:3px;color:#4a7090;margin-top:4px">
    <span style="display:inline-block;width:7px;height:7px;background:#00e676;border-radius:50%;
                 box-shadow:0 0 8px #00e676;margin-right:8px;animation:pulse 2s infinite"></span>
    SYSTEM ONLINE — SECURE SESSION
  </div>
</div>
""", unsafe_allow_html=True)

# ── Layout: two columns ───────────────────────────────────────────────────────
col_atm, col_ai = st.columns([1, 1], gap="large")


# ════════════════════════════════════════════════════════════════════════════════
#  LEFT COLUMN — ATM TERMINAL
# ════════════════════════════════════════════════════════════════════════════════
with col_atm:

    # Panel wrapper
    st.markdown("""
    <div style="background:#0c1420;border:1px solid #1a3a5c;border-radius:4px;padding:22px;
                box-shadow:0 0 20px rgba(0,200,255,.1);position:relative;margin-bottom:0">
      <div style="position:absolute;top:0;left:20px;right:20px;height:1px;
                  background:linear-gradient(90deg,transparent,#00c8ff,transparent);opacity:.4"></div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:3px;
                  color:#4a7090;margin-bottom:18px;display:flex;align-items:center;gap:10px">
        ATM TERMINAL
        <div style="flex:1;height:1px;background:#1a3a5c"></div>
      </div>
    """, unsafe_allow_html=True)

    # ── Transaction type selector ──────────────────────────────────────────────
    txn_options = list(atm_scripts.keys())
    new_txn = st.selectbox(
        "SELECT TRANSACTION TYPE",
        txn_options,
        index=txn_options.index(st.session_state.txn_type),
        label_visibility="visible"
    )
    if new_txn != st.session_state.txn_type:
        st.session_state.txn_type = new_txn
        st.session_state.step = 0
        st.session_state.amount = 0
        st.session_state.alert = None
        st.session_state.pin_ok = False
        st.rerun()

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── ATM Screen ─────────────────────────────────────────────────────────────
    step_name = cur_step()
    s = script()
    n_steps = len(s)
    step_idx = st.session_state.step

    # progress dots
    dots_html = ""
    for i in range(n_steps):
        if i < step_idx:
            col = "#00e676"; shadow = "0 0 6px #00e676"
        elif i == step_idx:
            col = "#00c8ff"; shadow = "0 0 8px #00c8ff"
        else:
            col = "#1a3a5c"; shadow = "none"
        dots_html += f'<div style="width:7px;height:7px;border-radius:50%;background:{col};box-shadow:{shadow};margin:0 2px"></div>'

    # screen messages per step
    screen_msgs = {
        "Insert Card":         ('<span style="color:#00c8ff">Please insert your card to begin.</span>', ""),
        "Enter PIN":           ('<span>Enter your 4-digit PIN securely.</span>',
                                '<span style="color:#4a7090;font-size:11px">Your PIN is encrypted end-to-end</span>'),
        "Select Withdraw":     ('<span>Select <b style="color:#00c8ff">WITHDRAW CASH</b> to proceed.</span>', ""),
        "Select Deposit":      ('<span>Select <b style="color:#00c8ff">DEPOSIT MONEY</b> to proceed.</span>', ""),
        "Check Balance":       ('<span>Select <b style="color:#00c8ff">CHECK BALANCE</b> to query your account.</span>', ""),
        "Enter Amount":        (f'<span>Enter the amount to {"deposit" if st.session_state.txn_type == "Deposit Money" else "withdraw"}.</span>',
                                f'<span style="color:#4a7090;font-size:11px">Min ₹100 &nbsp;|&nbsp; Max {fmt(st.session_state.balance)}</span>'),
        "Confirm Transaction": (
            ('<span style="color:#ff3d3d">⚠ INSUFFICIENT FUNDS<br>'
             f'<span style="font-size:11px">Requested {fmt(st.session_state.amount)} &gt; Available {fmt(st.session_state.balance)}</span></span>', "")
            if st.session_state.amount > st.session_state.balance else
            (f'<span>Confirm withdrawal of <b style="color:#0af0b4">{fmt(st.session_state.amount)}</b></span>',
             f'<span style="color:#4a7090;font-size:11px">Balance after: {fmt(st.session_state.balance - st.session_state.amount)}</span>')
        ),
        "Confirm Deposit":     (f'<span>Confirm deposit of <b style="color:#0af0b4">{fmt(st.session_state.amount)}</b></span>',
                                f'<span style="color:#4a7090;font-size:11px">Balance after: {fmt(st.session_state.balance + st.session_state.amount)}</span>'),
        "Dispense Cash":       (f'<span style="color:#00e676">✓ CASH DISPENSED<br>{fmt(st.session_state.amount)} ready for collection</span>',
                                '<span style="color:#4a7090;font-size:11px">Please collect your cash and card</span>'),
        "Display Balance":     (f'<span style="color:#00e676">✓ ACCOUNT BALANCE<br>Available: <b>{fmt(st.session_state.balance)}</b></span>',
                                '<span style="color:#4a7090;font-size:11px">Ledger balance matches available</span>'),
        "Print Receipt":       ('<span style="color:#00e676">✓ TRANSACTION COMPLETE</span>',
                                '<span style="color:#4a7090;font-size:11px">Your receipt is ready below</span>'),
    }

    msg_main, msg_sub = screen_msgs.get(step_name, (step_name, ""))
    now_str = datetime.datetime.now().strftime("%H:%M:%S")

    st.markdown(f"""
    <div style="background:#050e18;border:1px solid #1a3a5c;border-radius:3px;padding:18px;
                min-height:200px;margin:10px 0 14px;position:relative;
                box-shadow:inset 0 0 30px rgba(0,0,0,.5);overflow:hidden;
                font-family:'Share Tech Mono',monospace">
      <!-- scanlines -->
      <div style="position:absolute;inset:0;pointer-events:none;
                  background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,200,255,.018) 3px,rgba(0,200,255,.018) 4px)"></div>

      <!-- top bar -->
      <div style="display:flex;justify-content:space-between;align-items:center;
                  margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid rgba(0,200,255,.1)">
        <span style="font-size:9px;letter-spacing:3px;color:#00c8ff;opacity:.6">NEXUS ATM // {st.session_state.session_id}</span>
        <span style="font-size:9px;color:#4a7090">{now_str}</span>
      </div>

      <!-- balance -->
      <div style="display:flex;align-items:baseline;gap:6px;margin-bottom:14px">
        <span style="font-size:10px;color:#4a7090;letter-spacing:2px">BALANCE</span>
        <span style="font-size:10px;color:#0af0b4;opacity:.7">₹</span>
        <span style="font-family:'Orbitron',sans-serif;font-size:26px;font-weight:700;
                     color:#0af0b4;text-shadow:0 0 20px rgba(10,240,180,.4);letter-spacing:2px">
          {st.session_state.balance:,.0f}
        </span>
      </div>

      <!-- step dots -->
      <div style="display:flex;margin-bottom:14px">{dots_html}</div>

      <!-- message -->
      <div style="font-size:13px;letter-spacing:1px;line-height:1.7;margin-bottom:6px">{msg_main}</div>
      <div style="line-height:1.5">{msg_sub}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Alert ──────────────────────────────────────────────────────────────────
    if st.session_state.alert:
        atype, amsg = st.session_state.alert
        if atype == "success":
            st.success(amsg)
        elif atype == "error":
            st.error(amsg)
        elif atype == "warning":
            st.warning(amsg)
        else:
            st.info(amsg)

    # ── Step-specific controls ─────────────────────────────────────────────────

    if step_name == "Insert Card":
        if st.button("▶  INSERT CARD", key="insert"):
            st.session_state.alert = ("info", "Card detected — reading chip…")
            advance()

    elif step_name == "Enter PIN":
        pin = st.text_input("4-DIGIT PIN", type="password", max_chars=4, key="pin_input",
                             placeholder="••••")
        if st.button("▶  SUBMIT PIN", key="submit_pin"):
            if len(pin) != 4 or not pin.isdigit():
                st.session_state.alert = ("error", "PIN must be exactly 4 digits.")
                st.rerun()
            else:
                st.session_state.pin_ok = True
                st.session_state.alert = ("info", "PIN verified — access granted.")
                advance()

    elif step_name == "Select Withdraw":
        if st.button("▶  WITHDRAW CASH", key="sel_withdraw"):
            advance()

    elif step_name == "Select Deposit":
        if st.button("▶  DEPOSIT MONEY", key="sel_deposit"):
            advance()

    elif step_name == "Check Balance":
        if st.button("▶  CHECK BALANCE", key="chk_bal"):
            advance()

    elif step_name == "Enter Amount":
        # Quick presets
        st.markdown('<div style="font-family:\'Share Tech Mono\',monospace;font-size:10px;letter-spacing:2px;color:#4a7090;margin-bottom:6px">QUICK SELECT</div>', unsafe_allow_html=True)
        pc1, pc2, pc3, pc4 = st.columns(4)
        for col_p, amt in zip([pc1, pc2, pc3, pc4], [500, 1000, 2000, 5000]):
            with col_p:
                if st.button(f"₹{amt:,}", key=f"preset_{amt}"):
                    st.session_state["_preset_amount"] = amt
                    st.rerun()

        default_amt = st.session_state.get("_preset_amount", st.session_state.amount if st.session_state.amount else 100)
        amount = st.number_input("ENTER AMOUNT (₹)", min_value=100, max_value=st.session_state.balance if st.session_state.txn_type != "Deposit Money" else 10_000_000,
                                  step=100, value=int(default_amt), key="amt_input")
        if st.button("▶  CONFIRM AMOUNT", key="confirm_amt"):
            st.session_state.amount = int(amount)
            if "_preset_amount" in st.session_state:
                del st.session_state["_preset_amount"]
            advance()

    elif step_name == "Confirm Transaction":
        if st.session_state.amount > st.session_state.balance:
            if st.button("◀  CHANGE AMOUNT", key="change_amt"):
                go_to("Enter Amount")
        else:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✓  CONFIRM", key="confirm_txn"):
                    st.session_state.balance -= st.session_state.amount
                    st.session_state.txn_count += 1
                    st.session_state.session_amount += st.session_state.amount
                    advance()
            with c2:
                if st.button("✕  CANCEL", key="cancel_txn"):
                    go_to("Enter Amount")

    elif step_name == "Confirm Deposit":
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✓  CONFIRM", key="confirm_dep"):
                st.session_state.balance += st.session_state.amount
                st.session_state.txn_count += 1
                st.session_state.session_amount += st.session_state.amount
                advance()
        with c2:
            if st.button("✕  CANCEL", key="cancel_dep"):
                go_to("Enter Amount")

    elif step_name == "Dispense Cash":
        st.markdown('<div style="text-align:center;font-size:40px;padding:10px 0">💵</div>', unsafe_allow_html=True)
        if st.button("▶  COLLECT & CONTINUE", key="collect"):
            advance()

    elif step_name == "Display Balance":
        if st.button("▶  CONTINUE", key="cont_bal"):
            advance()

    elif step_name == "Print Receipt":
        receipt_text, txn_id = generate_receipt(
            st.session_state.txn_type,
            st.session_state.amount,
            st.session_state.balance
        )
        st.markdown(f"""
        <pre style="background:#f5f0e0;color:#1a1a1a;font-family:'Share Tech Mono',monospace;
                    font-size:11px;padding:16px;border-radius:2px;
                    border-top:6px dashed #bbb;border-bottom:6px dashed #bbb;
                    white-space:pre;line-height:1.7;margin-bottom:10px">{receipt_text}</pre>
        """, unsafe_allow_html=True)
        st.download_button(
            label="↓  DOWNLOAD RECEIPT",
            data=receipt_text,
            file_name=f"atm_receipt_{txn_id}.txt",
            mime="text/plain",
            key="dl_receipt"
        )
        if st.button("↺  NEW TRANSACTION", key="new_txn"):
            reset()

    st.markdown("</div>", unsafe_allow_html=True)   # close panel div


# ════════════════════════════════════════════════════════════════════════════════
#  RIGHT COLUMN — AI ENGINE
# ════════════════════════════════════════════════════════════════════════════════
with col_ai:

    prediction = predict_next_action(script(), cur_step())

    st.markdown(f"""
    <div style="background:#0c1420;border:1px solid #1a3a5c;border-radius:4px;padding:22px;
                box-shadow:0 0 20px rgba(0,200,255,.1);position:relative">
      <div style="position:absolute;top:0;left:20px;right:20px;height:1px;
                  background:linear-gradient(90deg,transparent,#0af0b4,transparent);opacity:.4"></div>

      <!-- Label -->
      <div style="font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:3px;
                  color:#4a7090;margin-bottom:18px;display:flex;align-items:center;gap:10px">
        AI ENGINE
        <div style="flex:1;height:1px;background:#1a3a5c"></div>
      </div>

      <!-- AI header -->
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px">
        <div style="width:40px;height:40px;border-radius:50%;
                    background:linear-gradient(135deg,rgba(10,240,180,.2),rgba(0,200,255,.1));
                    border:1px solid #0af0b4;display:flex;align-items:center;justify-content:center;
                    font-size:18px;box-shadow:0 0 15px rgba(10,240,180,.2)">🧠</div>
        <div>
          <div style="font-family:'Orbitron',sans-serif;font-size:13px;color:#0af0b4;letter-spacing:2px">PREDICTION ENGINE</div>
          <div style="font-size:11px;color:#4a7090;letter-spacing:1px">TRANSACTION FLOW ANALYSIS</div>
        </div>
      </div>

      <!-- Prediction box -->
      <div style="background:rgba(10,240,180,.04);border:1px solid rgba(10,240,180,.2);
                  border-radius:3px;padding:16px;margin-bottom:20px;position:relative;overflow:hidden">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;
                    background:linear-gradient(90deg,transparent,#0af0b4,transparent);opacity:.6"></div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:3px;
                    color:#4a7090;margin-bottom:8px">PREDICTED NEXT STEP</div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:16px;color:#0af0b4;
                    text-shadow:0 0 15px rgba(10,240,180,.4);letter-spacing:2px">
          <span style="color:#4a7090;margin-right:8px">▶</span>{prediction}
        </div>
      </div>
    """, unsafe_allow_html=True)

    # ── Transaction Flow Visualizer ────────────────────────────────────────────
    st.markdown("""
    <div style="background:#101c2e;border:1px solid #1a3a5c;border-radius:3px;padding:16px;margin-bottom:16px">
      <div style="font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:3px;
                  color:#4a7090;margin-bottom:14px">TRANSACTION FLOW</div>
    """, unsafe_allow_html=True)

    s = script()
    flow_html = ""
    for i, sname in enumerate(s):
        if i < step_idx:
            node_col   = "#00e676"; node_bg = "rgba(0,230,118,.15)"
            icon       = "✓"
            name_col   = "#00e676"; name_op = ".7"
            badge      = '<span style="margin-left:auto;font-size:8px;letter-spacing:2px;padding:2px 7px;border-radius:2px;background:rgba(0,230,118,.1);color:#00e676;border:1px solid rgba(0,230,118,.2)">DONE</span>'
            line_col   = "rgba(0,230,118,.3)"
        elif i == step_idx:
            node_col   = "#00c8ff"; node_bg = "rgba(0,200,255,.15)"
            icon       = "▶"
            name_col   = "#ffffff"; name_op = "1"
            badge      = '<span style="margin-left:auto;font-size:8px;letter-spacing:2px;padding:2px 7px;border-radius:2px;background:rgba(0,200,255,.1);color:#00c8ff;border:1px solid rgba(0,200,255,.3)">ACTIVE</span>'
            line_col   = "#1a3a5c"
        elif i == step_idx + 1:
            node_col   = "#0af0b4"; node_bg = "rgba(10,240,180,.08)"
            icon       = "○"
            name_col   = "#0af0b4"; name_op = ".6"
            badge      = '<span style="margin-left:auto;font-size:8px;letter-spacing:2px;padding:2px 7px;border-radius:2px;background:rgba(10,240,180,.06);color:#0af0b4;border:1px solid rgba(10,240,180,.15);opacity:.7">NEXT</span>'
            line_col   = "#1a3a5c"
        else:
            node_col   = "#1a3a5c"; node_bg = "#0c1420"
            icon       = "○"
            name_col   = "#4a7090"; name_op = "1"
            badge      = ""
            line_col   = "#1a3a5c"

        connector = (
            f'<div style="position:absolute;left:9px;top:26px;width:1px;'
            f'height:calc(100% - 6px);background:{line_col}"></div>'
            if i < len(s) - 1 else ""
        )
        flow_html += f"""
        <div style="display:flex;align-items:center;gap:10px;padding:7px 0;position:relative">
          {connector}
          <div style="width:18px;height:18px;border-radius:50%;border:1px solid {node_col};
                      background:{node_bg};display:flex;align-items:center;justify-content:center;
                      font-size:8px;color:{node_col};flex-shrink:0;z-index:1">{icon}</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:11px;
                      color:{name_col};opacity:{name_op};letter-spacing:1px">{sname.upper()}</div>
          {badge}
        </div>"""

    st.markdown(flow_html + "</div></div>", unsafe_allow_html=True)

    # ── Stats ──────────────────────────────────────────────────────────────────
    status_map = {
        "Insert Card": "WAITING", "Enter PIN": "AUTH",
        "Select Withdraw": "MENU", "Select Deposit": "MENU",
        "Check Balance": "QUERY", "Enter Amount": "INPUT",
        "Confirm Transaction": "PENDING", "Confirm Deposit": "PENDING",
        "Dispense Cash": "ACTIVE", "Display Balance": "QUERY",
        "Print Receipt": "DONE"
    }

    sc1, sc2 = st.columns(2)
    sd1, sd2 = st.columns(2)

    def stat_card(label, value, color="#ffffff"):
        return f"""
        <div style="background:#101c2e;border:1px solid #1a3a5c;border-radius:3px;padding:12px">
          <div style="font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;
                      color:#4a7090;margin-bottom:4px">{label}</div>
          <div style="font-family:'Orbitron',sans-serif;font-size:17px;font-weight:700;color:{color}">{value}</div>
        </div>"""

    with sc1:
        st.markdown(stat_card("STEP", f"{step_idx + 1} / {len(s)}", "#00c8ff"), unsafe_allow_html=True)
    with sc2:
        st.markdown(stat_card("TRANSACTIONS", str(st.session_state.txn_count), "#00e676"), unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    with sd1:
        st.markdown(stat_card("SESSION AMT", f"₹{st.session_state.session_amount:,}", "#ffffff"), unsafe_allow_html=True)
    with sd2:
        st.markdown(stat_card("STATUS", status_map.get(cur_step(), "ACTIVE"), "#00c8ff"), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)   # close ai panel

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;margin-top:18px;font-family:'Share Tech Mono',monospace;
            font-size:10px;letter-spacing:2px;color:#1a3a5c">
  SECURED BY 256-BIT ENCRYPTION &nbsp;|&nbsp; SESSION: {st.session_state.session_id}
</div>
""", unsafe_allow_html=True)
