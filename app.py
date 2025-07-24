import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Sales CSV
df_wide = pd.read_csv("EV_Data/data/final_ev_sales.csv")
# Convert date column to datetime
df_wide['Date'] = pd.to_datetime(df_wide['Date'])

# Melt wide to long format
df_sales_long = df_wide.melt(
    id_vars=['Date'],
    value_vars=['BYD', 'Tesla', 'NIO'],
    var_name='Company',
    value_name='Sales'
)

# Clean company names
df_sales_long['Company'] = df_sales_long['Company'].str.replace('_sales', '').str.capitalize()

# Load Stock CSV
df_stock = pd.read_csv("EV_Data/data/cleaned_stock_data.csv")
# Convert date column to datetime
df_stock['Date'] = pd.to_datetime(df_stock['Date'])

# Melt stock data to long format
df_stock_long = df_stock.melt(
    id_vars=['Date'],
    value_vars=['Tesla_Close', 'BYD_Close', 'NIO_Close'],
    var_name='Company',
    value_name='Close'
)
df_stock_long['Company'] = df_stock_long['Company'].str.replace('_Close', '').str.capitalize()


# Ready Streamlit dashboard
st.title("EV Market Insights Dashboard")

# Create tabs: tab1 = Sales and tab2 = Stock
tab1, tab2 = st.tabs(["📈 EV Sales", "💹 Stock Prices"])

#tab1
with tab1:
    st.header("EV Sales Over Time")

    # Sidebar date filter
    min_date = df_sales_long['Date'].min()
    max_date = df_sales_long['Date'].max()
    start_date = st.sidebar.date_input("Start date", min_value=min_date, value=min_date)
    end_date = st.sidebar.date_input("End date", min_value=min_date, value=max_date)

    if start_date > end_date:
        st.error("End date must be after start date.")
    else:
        filtered_sales = df_sales_long[
            (df_sales_long['Date'] >= pd.to_datetime(start_date)) &
            (df_sales_long['Date'] <= pd.to_datetime(end_date))
        ]
        st.write(f"Showing sales data from **{start_date}** to **{end_date}**")
        st.dataframe(filtered_sales)
        # Line Chart
        sales_chart_data = filtered_sales.pivot(index='Date', columns='Company', values='Sales')
        st.line_chart(sales_chart_data)

#tab2
with tab2:
    st.header("EV Stock Prices Over Time")

    # Company selection
    company_options = ['Tesla', 'BYD', 'NIO']
    selected_company = st.selectbox("Select a company", company_options)

    # Filter stock data
    company_stock = df_stock_long[df_stock_long['Company'] == selected_company]

    # Date slider
    min_stock_date = company_stock['Date'].min()
    max_stock_date = company_stock['Date'].max()
    stock_range = st.slider(
        "Select date range",
        min_value=min_stock_date,
        max_value=max_stock_date,
        value=(min_stock_date, max_stock_date)
    )

    filtered_stock = company_stock[
        (company_stock['Date'] >= stock_range[0]) &
        (company_stock['Date'] <= stock_range[1])
    ]

    st.write(f"Showing stock prices for **{selected_company}** from **{stock_range[0]}** to **{stock_range[1]}**")
    st.line_chart(filtered_stock.set_index('Date')['Close'])
