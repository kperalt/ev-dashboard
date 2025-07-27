import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.dates import AutoDateLocator, AutoDateFormatter

# Add bilingual translations
LANGUAGES = {
    'English': 'en',
    '中文': 'zh'
}

translations = {
    'en': {
        'title': "EV Market Insights Dashboard",
        'welcome': "Welcome to my EV Market Insights Dashboard! Here you can explore:\n- Stock price trends of major EV companies in China.\n- Monthly EV sales data.\n\nUse the tabs below to navigate between Sales and Stock data.",
        'sales_tab': "📊 EV Sales",
        'stock_tab': "📈 Stock Prices",
        'instructions': """
1. Select a company from the dropdown (in Stock tab).
2. Adjust the date ranges to filter data.
3. Explore trends and data interactively.
        """,
        'select_company': "Select a company",
        'start_date': "Start date",
        'end_date': "End date",
        'error_end_before_start': "End date must be after start date.",
        'showing_data': "**Showing data from {} to {}**",
        'latest_sales': "{} Latest Sales",
        'peak': "Peak: {:,.0f}",
        'key_metrics': "📌 Key Metrics",
        'closing_price': "Latest Closing Price",
        'average_price': "Average Price in Range",
        'no_stock_data': "No stock data available for {}.",
    },
    'zh': {
        'title': "电动车市场洞察仪表板",
        'welcome': "欢迎使用我的电动车市场洞察仪表板！您可以探索以下内容：\n- 中国主要电动车企业的股价趋势。\n- 月度电动车销量数据。\n\n使用下面的标签在销量和股价数据之间切换。",
        'sales_tab': "📊 电动车销量",
        'stock_tab': "📈 股价趋势",
        'instructions': """
1. 在“股价”标签中选择一家企业。
2. 调整日期范围以筛选数据。
3. 交互式探索趋势和数据。
        """,
        'select_company': "选择企业",
        'start_date': "开始日期",
        'end_date': "结束日期",
        'error_end_before_start': "结束日期必须在开始日期之后。",
        'showing_data': "**显示从 {} 到 {} 的数据**",
        'latest_sales': "{} 最新销量",
        'peak': "峰值: {:,.0f}",
        'key_metrics': "📌 关键指标",
        'closing_price': "最新收盘价",
        'average_price': "选定时间内平均价格",
        'no_stock_data': "没有 {} 的股价数据。",
    }
}

# Sidebar language toggle
with st.sidebar:
    language = st.selectbox("🌐 Select Language / 选择语言", list(LANGUAGES.keys()))
lang_code = LANGUAGES[language]
t = translations[lang_code]

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
    
    min_date = df_sales_long['Date'].min().date()
    max_date = df_sales_long['Date'].max().date()
    start_date = st.date_input(t['start_date'], min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input(t['end_date'], min_value=min_date, max_value=max_date, value=max_date)

# Create tabs: tab1 = Sales and tab2 = Stock
tab1, tab2 = st.tabs(["📊 EV Sales", "📈 Stock Prices"])

#tab1
with tab1:
    st.header("EV Sales Over Time")
    
    # add KPI section
    st.subheader("📌 Key Metrics")
    latest_date = df_sales_long['Date'].max()
    latest_sales = df_sales_long[df_sales_long['Date'] == latest_date]

    col1, col2, col3 = st.columns(3)
    for col, company in zip([col1, col2, col3], ['Tesla', 'BYD', 'NIO']):
        latest_value = latest_sales[latest_sales['Company'] == company]['Sales'].values[0]
        max_value = df_sales_long[df_sales_long['Company'] == company]['Sales'].max()
        col.metric(label=f"{company} Latest Sales", value=f"{latest_value:,.0f}", delta=f"Peak: {max_value:,.0f}")

    
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
        ax.xaxis.set_major_locator(AutoDateLocator())
        ax.xaxis.set_major_formatter(AutoDateFormatter(AutoDateLocator()))
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
            
            # add KPI section
            st.subheader("📌 Key Metrics")
            if not filtered_stock.empty:
                latest_stock_price = filtered_stock.iloc[-1]['Close']
                avg_price = filtered_stock['Close'].mean()
                st.metric(label="Latest Closing Price", value=f"${latest_stock_price:,.2f}")
                st.metric(label="Average Price in Range", value=f"${avg_price:,.2f}")

            # Line chart for stock
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            color_map = {'Tesla': 'red', 'BYD': 'blue', 'NIO': 'green'}
            ax2.plot(filtered_stock['Date'], filtered_stock['Close'], color=color_map[selected_company])
            ax2.set_title(f"{selected_company} Stock Prices")
            ax2.set_xlabel("Date")
            ax2.set_ylabel("Closing Price (USD)")
            ax2.xaxis.set_major_locator(AutoDateLocator())
            ax2.xaxis.set_major_formatter(AutoDateFormatter(AutoDateLocator()))
            ax2.tick_params(axis='x', rotation=45)
            st.pyplot(fig2)
            
        st.markdown("---")
