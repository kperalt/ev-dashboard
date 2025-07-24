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

# Date filters in sidebar
min_date = df_long['Date'].min()
max_date = df_long['Date'].max()

start_date = st.sidebar.date_input('Start date', min_date)
end_date = st.sidebar.date_input('End date', max_date)

if start_date > end_date:
    st.error("Error: End date must be after start date.")
else:
    # Filter data by date range
    filtered_data = df_long[(df_long['Date'] >= pd.to_datetime(start_date)) &
                            (df_long['Date'] <= pd.to_datetime(end_date))]

st.write(f"Data from {start_date} to {end_date}")
st.dataframe(filtered_data)

# Line chart
chart_data = df_long.pivot(index='Date', columns='Company', values='Sales')
st.line_chart(chart_data)
