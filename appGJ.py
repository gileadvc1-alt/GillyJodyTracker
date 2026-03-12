import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration & Apple-style UI
st.set_page_config(page_title="GJ Ex - Tracker", page_icon="🇿🇦", layout="wide")

# Custom CSS for "Luxury Dark Mode" - specifically using Gold and Emerald accents
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #FFFFFF; }
    .stButton>button {
        background: linear-gradient(45deg, #FFD700, #00C853);
        color: black; border: none; border-radius: 10px; font-weight: bold;
    }
    .metric-card {
        background-color: #161B22; border: 1px solid #30363D;
        padding: 20px; border-radius: 15px; text-align: center;
    }
    h1, h2, h3 { font-family: 'SF Pro Display', sans-serif; letter-spacing: -1px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Login Logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login():
    st.title("🛡️ GJ Private Access")
    password = st.text_input("Enter Passcode", type="password")
    if st.button("Unlock Wealth"):
        if password == "genius2026": 
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Access Denied.")

if not st.session_state['logged_in']:
    login()
else:
    # 3. Sidebar Navigation
    st.sidebar.title("GJ Ex - Tracker")
    menu = st.sidebar.radio("Navigation", ["Overview", "Add Transaction", "Wealth Forecast"])
    
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

    # 4. Dashboard Logic
    if menu == "Overview":
        st.title("Family Wealth Overview 🇿🇦")
        
        # Dashboard Metrics in ZAR
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown('<div class="metric-card"><h3>Income</h3><h2 style="color:#00C853">R45,000</h2></div>', unsafe_allow_html=True)
        with col2: st.markdown('<div class="metric-card"><h3>Expenses</h3><h2 style="color:#FF4B4B">R18,200</h2></div>', unsafe_allow_html=True)
        with col3: st.markdown('<div class="metric-card"><h3>Savings Rate</h3><h2 style="color:#FFD700">60%</h2></div>', unsafe_allow_html=True)
        with col4: st.markdown('<div class="metric-card"><h3>Net Profit</h3><h2>R26,800</h2></div>', unsafe_allow_html=True)

        # Spending Breakdown Chart
        st.subheader("Monthly Flow (ZAR)")
        df = pd.DataFrame({
            "Category": ["Groceries", "Fuel", "Take Outs", "Household", "Investments"],
            "Amount": [4500, 2200, 1500, 3000, 26800]
        })
        fig = px.pie(df, values='Amount', names='Category', hole=.7, 
                     color_discrete_sequence=px.colors.sequential.Greens_r)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "Add Transaction":
        st.title("New Entry ✍️")
        with st.form("entry_form"):
            date = st.date_input("Date")
            category = st.selectbox("Category", ["Income", "Groceries", "Fuel", "Take Outs", "Household"])
            amount = st.number_input("Amount (R)", min_value=0.0)
            note = st.text_input("Note (e.g., Checkers/Woolies run)")
            
            if st.form_submit_button("Record Transaction"):
                st.balloons()
                st.success(f"Recorded R{amount:,.2f} to {category}!")

    elif menu == "Wealth Forecast":
        st.title("Genius Forecaster 🚀")
        st.write("Visualizing the path to South African Wealth...")
        
        monthly_invest = st.slider("Monthly Investment (R)", 1000, 50000, 15000)
        years = st.slider("Years to Forecast", 1, 30, 10)
        
        # Forecast Math (using 10% ROI for local market growth)
        data = []
        balance = 0
        for i in range(years * 12):
            balance = (balance + monthly_invest) * (1 + 0.10/12)
            data.append(balance)
        
        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Scatter(y=data, mode='lines', line=dict(color='#00C853', width=4), fill='tozeroy'))
        fig_forecast.update_layout(title="Projected Wealth Path (10% ROI)", template="plotly_dark", 
                                  yaxis_tickprefix="R", yaxis_tickformat=",")
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        st.success(f"In {years} years, at this rate, your joint venture will be worth: **R{balance:,.2f}**")