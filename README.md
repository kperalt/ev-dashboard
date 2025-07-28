# ev-dashboard

A bilingual data dashboard analyzing Electric Vehicle (EV) market trends in China, created using **Streamlit**, **Pandas**, and **Matplotlib**.  
🌏 Built with global users in mind — supports both **English** and **Simplified Chinese**.

🚀 [View Live App](https://ev-dashboard-3anmsf2jrfjei9hksayahj.streamlit.app)

---

## 🗂️ Features

- **EV Sales Trends**: Track the evolution of EV unit sales over time
- **Stock Prices**: Visualize historical stock performance of Tesla, BYD, and NIO
- **Language Toggle**: Switch between English and Chinese with one click
- **Download Option**: Export sales data directly as CSV
- **Clean UI**: Built with Streamlit tabs and intuitive controls

---

## 📊 Project Structure
ev-dashboard/
├── app.py # Main Streamlit app
├── translations.py # Bilingual text dictionary
├── requirements.txt # Python dependencies
├── EV_Data/
│ ├── final_ev_sales.csv # EV sales data
│ └── stock_data.csv # Historical stock prices

---

## 🌐 Languages

- 🇺🇸 English
- 🇨🇳 简体中文 (Simplified Chinese)

---

## 🛠️ Tech Stack

| Tool        | Role                             |
|-------------|----------------------------------|
| Python      | Core programming language        |
| Streamlit   | Web app framework                |
| Pandas      | Data manipulation                |
| Matplotlib  | Data visualization               |
| Git + GitHub| Version control & deployment     |

---

## 🎯 Purpose

This dashboard was created by **Keyla Peralta Alberto**, Swarthmore student double majoring in **Computer Science** and **Chinese**, as part of a project aimed at:

- Gaining real-world data visualization experience
- Exploring global tech policy and EV market trends
- Showcasing bilingual tech communication

---

## 📁 Setup & Deployment

### To run locally:
```bash
git clone https://github.com/your-username/ev-dashboard.git
cd ev-dashboard
pip install -r requirements.txt
streamlit run app.py
