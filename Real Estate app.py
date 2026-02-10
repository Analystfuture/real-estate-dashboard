import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Setup Page
st.set_page_config(page_title="Real Estate Ops", layout="wide")
st.title("🏙️ Real Estate Live Leads Dashboard")
st.markdown("### Powered by n8n & Supabase")

# 2. Connect to Database (We will add secrets later)
# Initialize connection.
# Uses st.secrets to keep API keys safe
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# 3. Fetch Data
def load_data():
    response = supabase.table('leads').select("*").execute()
    data = response.data
    return pd.DataFrame(data)

# 4. Display Metrics
try:
    df = load_data()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Leads", len(df))
    col2.metric("Buyers", len(df[df['intent'] == 'Buyer']))
    col3.metric("Investors", len(df[df['intent'] == 'Investor']))

    # 5. Display Table
    st.subheader("Recent Leads")
    st.dataframe(df)

except Exception as e:
    st.error(f"Error connecting to DB: {e}")
