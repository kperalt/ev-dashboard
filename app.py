import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df_wide = pd.read_csv("EV_Data/data/final_ev_sales.csv") 

# Convert date column to datetime
df_wide['Date'] = pd.to_datetime(df_wide['Date'])

# Melt wide to long format
df_long = df_wide.melt(
    id_vars=['Date'], 
    value_vars=['BYD', 'Tesla', 'NIO'],
    var_name='Company',
    value_name='Sales'
)

# Clean company names
df_long['Company'] = df_long['Company'].str.replace('_sales', '').str.capitalize()

# Ready Streamlit dashboard
st.title("EV Sales Dashboard")
st.dataframe(df_long)

chart_data = df_long.pivot(index='Date', columns='Company', values='Sales')
st.line_chart(chart_data)
