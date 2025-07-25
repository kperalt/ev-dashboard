import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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
# Clean company names
df_stock_long['Company'] = df_stock_long['Company'].str.replace('_Close', '', regex=False)
df_stock_long['Company'] = df_stock_long['Company'].replace({
    'Tesla': 'Tesla',
    'BYD': 'BYD',
    'NIO': 'NIO'
})

# Ready Streamlit dashboard
st.title("EV Market Insights Dashboard")
st.markdown("""
Welcome to my EV Market Insights Dashboard! Here you can explore:
- Stock price trends of major EV companies in China.
- Monthly EV sales data.
  
Use the tabs below to navigate between Sales and Stock data.
""")

with st.sidebar:
    st.header("Instructions")
    st.markdown("""
    1. Select a company from the dropdown (in Stock tab).
    2. Adjust the date ranges to filter data.
    3. Explore trends and data interactively.
    """)

# Create tabs: tab1 = Sales and tab2 = Stock
tab1, tab2 = st.tabs(["📊 EV Sales", "📈 Stock Prices"])

#tab1
with tab1:
    st.header("EV Sales Over Time")

    # Sidebar date filter
    min_date = df_sales_long['Date'].min().date()
    max_date = df_sales_long['Date'].max().date()
    
    start_date = st.sidebar.date_input("Start date", min_value=min_date, value=min_date)
    end_date = st.sidebar.date_input("End date", min_value=min_date, value=max_date)

    if start_date > end_date:
        st.error("End date must be after start date.")
    else:
        filtered_sales = df_sales_long[
            (df_sales_long['Date'] >= pd.to_datetime(start_date)) &
            (df_sales_long['Date'] <= pd.to_datetime(end_date))
        ]
        
        st.markdown(f"**Showing data from {start_date} to {end_date}**")
        st.dataframe(filtered_sales)

        # Line chart with formatted y-axis
        sales_chart_data = filtered_sales.pivot(index='Date', columns='Company', values='Sales')
        fig, ax = plt.subplots(figsize=(10, 4))
        colors = {'Tesla': 'red', 'BYD': 'blue', 'NIO': 'green'}
        for company in sales_chart_data.columns:
            ax.plot(sales_chart_data.index, sales_chart_data[company], label=company, color=colors[company])
        ax.set_title("EV Sales Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Sales Volume")
        ax.legend()
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    st.markdown("---")
#tab2
with tab2:
    st.header("EV Stock Prices Over Time")

    # Company selection
    company_options = ['Tesla', 'BYD', 'NIO']
    selected_company = st.selectbox("Select a company", company_options)

    # Filter stock data
    company_stock = df_stock_long[df_stock_long['Company'] == selected_company]

    # Date selection
    if company_stock.empty:
        st.warning(f"No stock data available for {selected_company}.")
    else:
        min_stock_date = company_stock['Date'].min().date()
        max_stock_date = company_stock['Date'].max().date()

        stock_date_range = st.date_input(
            "Select date range",
            value=(min_stock_date, max_stock_date),
            min_value=min_stock_date,
            max_value=max_stock_date,
            key="stock_date_range"
        )
            # Unpack selected dates from date_input
        if isinstance(stock_date_range, tuple) and len(stock_date_range) == 2:
            start_stock_date, end_stock_date = stock_date_range
        else:
            start_stock_date = end_stock_date = stock_date_range

        if start_stock_date > end_stock_date:
            st.error("Error: End date must be after start date.")
        else:
            # Filter stock data within selected date range
            filtered_stock = company_stock[
                (company_stock['Date'] >= pd.to_datetime(start_stock_date)) &
                (company_stock['Date'] <= pd.to_datetime(end_stock_date))
            ]
            
            st.markdown(f"**Showing stock prices for {selected_company} from {start_stock_date} to {end_stock_date}**")
            st.dataframe(filtered_stock)

            # Line chart for stock
            ig2, ax2 = plt.subplots(figsize=(10, 4))
            color_map = {'Tesla': 'red', 'BYD': 'blue', 'NIO': 'green'}
            ax2.plot(filtered_stock['Date'], filtered_stock['Close'], color=color_map[selected_company])
            ax2.set_title(f"{selected_company} Stock Prices")
            ax2.set_xlabel("Date")
            ax2.set_ylabel("Closing Price (USD)")
            ax2.tick_params(axis='x', rotation=45)
            st.pyplot(fig2)
            
        st.markdown("---")
