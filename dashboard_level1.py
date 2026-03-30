import streamlit as st
import pandas as pd # For data manipulation and analysis
import requests # For making HTTP requests to fetch the data
import io # For handling in-memory text streams
import matplotlib.pyplot as plt # For data visualization


countries = ["US","PRT","FRA","DEU"]

# URL of the OECD unemployment data

url = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_LFS@DF_IALFS_UNE_M,1.0/USA+PRT+DEU+FRA..PT_LF_SUB._Z.Y._T.Y_GE15..M?startPeriod=2015-01&dimensionAtObservation=AllDimensions&format=csvfile"

response = requests.get(url)    

df = pd.read_csv(io.StringIO(response.text))

df_clean = df[['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE']]
df_clean['OBS_VALUE'] = pd.to_numeric(df_clean['OBS_VALUE'], errors='coerce')
df_clean['TIME_PERIOD'] = pd.to_datetime(df_clean['TIME_PERIOD'], format='%Y-%m')

## order the data by country and time period
df_clean = df_clean.sort_values(by=['REF_AREA', 'TIME_PERIOD']) 


st.title("OECD Unemployment Rates Dashboard") # Set the title of the Streamlit app
st.write("This dashboard shows the unemployment rates for the United States, Portugal, France, and Germany from January 2015 to the most recent available data. The data is sourced from the OECD and is updated regularly. The plot allows you to compare the unemployment trends across these countries over time.")

fig, ax1 = plt.subplots(figsize=(12, 6)) # Create a figure and a set of subplots with a specified size

for country in countries:
    country_data = df_clean[df_clean['REF_AREA'] == country] # Filter the data for the current country
    ax1.plot(country_data['TIME_PERIOD'], country_data['OBS_VALUE'], label=f"{country} Unemployment Rate") # Plot TIME_PERIOD vs unemployment_rate for the current country on ax1

ax1.set_xlabel('Time') # Set the x-axis label for ax1   
plt.xticks(rotation=45) # Rotate the x-axis tick labels by 45 degrees for better readability
ax1.set_ylabel('Unemployment Rate') # Set the y-axis label for ax1
ax1.set_title('OECD Unemployment Rates Over Time') # Set the title for the plot 
ax1.legend() # Combine the lines and labels from both axes and create a single legend in the upper left corner
st.pyplot(fig) # Display the plot in the Streamlit app  


