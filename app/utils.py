import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Dictionary to store the unique ID for each country's file from the Google Drive link
# https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing
FILE_IDS = {
    'Ethiopia': '1DALTpw0L-g1NT58UshD1L84LXLFDybcZ',
    'Kenya': '1p9HhITzz6Dohj2OShMs1R8vTNvHF6c_y',
    'Nigeria': '1cj2qSO7vbBEJ2qQabHsaEiFFIdfhxvU_',
    'Sudan': '1vfytxD_QrCdSt9OmNdrAtW5OxBIOL1KF',
    'Tanzania': '1JKCUpwPn_Vsw1SikRF8Kmxovl3TCCj1t',
}

@st.cache_data
def load_data():
    """Load all country data directly from public Google Drive links."""
    all_data = []
    
    for country, file_id in FILE_IDS.items():
        # Create a direct download link
        url = f'https://drive.google.com/uc?export=download&id={file_id}'
        
        # Fetch the file from the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            st.error(f"Failed to load data for {country}. Status code: {response.status_code}")
            continue
            
        # Read the CSV content into a pandas DataFrame
        # We wrap the content in BytesIO because pd.read_csv expects a file-like object
        df_country = pd.read_csv(BytesIO(response.content))
        
        # Add the country name as a new column
        df_country['Country'] = country
        
        all_data.append(df_country)
    
    # Combine all data into one DataFrame
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df['Date'] = pd.to_datetime(combined_df['Date'])
        combined_df['Year'] = combined_df['Date'].dt.year
        combined_df['Month'] = combined_df['Date'].dt.month
        return combined_df
    else:
        st.error("No data could be loaded.")
        return pd.DataFrame()

@st.cache_data
def filter_data(df, countries, year_range):
    """Filter data by selected countries and year range"""
    mask = (df['Country'].isin(countries)) & (df['Year'].between(year_range[0], year_range[1]))
    return df[mask].copy()

def aggregate_monthly(df, variable):
    """Aggregate data to monthly averages"""
    return df.groupby(['Country', df['Date'].dt.to_period('M')])[variable].mean().reset_index()

def calculate_summary_stats(df, variable):
    """Calculate summary statistics by country"""
    return df.groupby('Country')[variable].agg([
        ('Mean', 'mean'),
        ('Median', 'median'),
        ('Std Dev', 'std'),
        ('Min', 'min'),
        ('Max', 'max')
    ]).round(2)

def get_variable_label(variable):
    """Get human-readable variable labels"""
    labels = {
        'T2M': 'Mean Temperature (°C)',
        'T2M_MAX': 'Max Temperature (°C)',
        'T2M_MIN': 'Min Temperature (°C)',
        'PRECTOTCORR': 'Precipitation (mm/day)',
        'RH2M': 'Relative Humidity (%)',
        'WS2M': 'Wind Speed (m/s)',
        'QV2M': 'Specific Humidity (g/kg)'
    }
    return labels.get(variable, variable)

def get_variable_unit(variable):
    """Get units for variables"""
    units = {
        'T2M': '°C',
        'T2M_MAX': '°C',
        'T2M_MIN': '°C',
        'PRECTOTCORR': 'mm/day',
        'RH2M': '%',
        'WS2M': 'm/s',
        'QV2M': 'g/kg'
    }
    return units.get(variable, '')