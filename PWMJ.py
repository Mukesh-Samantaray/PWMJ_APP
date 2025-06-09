# streamlit_app.py

import streamlit as st
import pickle
import pandas as pd

# Load the trained model from pickle
with open("hw_model.pkl", "rb") as f:
    model = pickle.load(f)

# Title
st.title("🔋 PJM Hourly Energy Forecast")
st.markdown("""
This app forecasts **energy consumption (MW)** for up to 30 days (hourly) using the Exponential Smoothing model.  
Use the slider below to select how many hours to forecast.  
""")

# Slider to choose how many hours to forecast (up to 30 days)
n_steps = st.slider("⏳ Select forecast horizon (in hours):", min_value=1, max_value=720, value=24, step=1)

# Forecasting
forecast = model.forecast(n_steps)

# Create datetime index for forecast
last_timestamp = model.model._index[-1]
forecast_index = pd.date_range(start=last_timestamp + pd.Timedelta(hours=1), periods=n_steps, freq='H')
forecast_df = pd.DataFrame({'Forecasted_PJMW_MW': forecast}, index=forecast_index)

# Show summary info
days = n_steps // 24
hours = n_steps % 24
st.subheader(f"📅 Forecast for next {days} day(s) and {hours} hour(s)")

# Display first 10 values for quick reference
st.write("🔢 Preview of forecasted values (first 10 rows):")
st.dataframe(forecast_df.head(10).style.format("{:.2f}"))

# Line chart
st.subheader("📈 Forecast Trend")
st.line_chart(forecast_df)

# Optional full data
with st.expander("📋 Show all forecasted values"):
    st.dataframe(forecast_df.style.format("{:.2f}"))
