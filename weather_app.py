import streamlit as st
import weather
import pandas as pd

#basic page configuration
st.set_page_config(
    page_title="Weather Data Analyzer",
    page_icon="🌤️",
    layout="wide"
)

#Page title and description
st.title("Weather Data Analyzer 🌡️")
st.write("This app analyzes weather data from CSV files")

#Selection header
st.header("Choose Sample Data")

#dropdown
sample_options = {
    "Example One": "tests/data/example_one.csv",
    "Example Two": "tests/data/example_two.csv",
    "Example Three": "tests/data/example_three.csv"
}

selected_sample = st.selectbox(
    "Select a sample dataset:",
    options=list(sample_options.keys())
)

#get filepath
sample_path = sample_options[selected_sample]

#load selected csv
data = weather.load_data_from_csv(sample_path)

#confirmation message
st.success(f"Loaded {len(data)} days from {selected_sample}")


#FUNCTIONS SECTION
def display_analysis(data):
    if not data:
        st.error("No weather data available for analysis. Please select a different dataset.")
        return
    
    st.header("Weather Analysis")
    
    #summary
    st.subheader("Overall Summary")
    summary = weather.generate_summary(data)
    st.text(summary)  # Using text to preserve formatting
    
    #daily summary
    with st.expander("Show Daily Details"):
        daily_summary = weather.generate_daily_summary(data)
        st.text(daily_summary)

def display_weather_data(data):
    if not data:
        st.warning("No data to display")
        return
    
    #preview header
    st.subheader("Data Preview")
    
    #first few records 
    st.write("First few records from the dataset:")
    preview_df = pd.DataFrame(data[:3], columns=["Date", "Min Temp (F)", "Max Temp (F)"])
    preview_df["Formatted Date"] = preview_df["Date"].apply(weather.convert_date)
    st.dataframe(preview_df[["Formatted Date", "Min Temp (F)", "Max Temp (F)"]])
    
    #rest of the data
    st.subheader("Complete Dataset")
    
    #raw data display??
    with st.expander("View raw data structure"):
        st.write("Sample of raw data:", data[0] if data else "No data")
    
    #creating a dataframe
    if len(data) > 0 and len(data[0]) >= 3:
        #format is [date, min_temp, max_temp]
        df = pd.DataFrame(data)
        #rename columns
        df.columns = ["Date", "Min Temp (F)", "Max Temp (F)"][:len(df.columns)]
        
        #convert temps
        df["Min Temp (C)"] = df["Min Temp (F)"].apply(weather.convert_f_to_c)
        df["Max Temp (C)"] = df["Max Temp (F)"].apply(weather.convert_f_to_c)
        
        #after creating dataframe
        df["Formatted Date"] = df["Date"].apply(weather.convert_date)
        st.dataframe(df[["Formatted Date", "Min Temp (C)", "Max Temp (C)", "Min Temp (F)", "Max Temp (F)"]])
    else:
        st.error("Data format is not as expected")

#tabs for different sections
if 'data' in locals():
    tabs = st.tabs(["Summary", "Data"])
    
    with tabs[0]:
        display_analysis(data)
    
    with tabs[1]:
        display_weather_data(data)

#footer??
st.write("---")
st.write("Created with Streamlit © 2025")
