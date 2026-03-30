import streamlit as st
import pandas as pd # For data manipulation and analysis
import requests # For making HTTP requests to fetch the data
import io # For handling in-memory text streams
import matplotlib.pyplot as plt # For data visualization


@st.cache_data
def load_data():
    
    url = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_LFS@DF_IALFS_UNE_M,1.0/AUS+AUT+BEL+CAN+CHL+COL+CRI+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA+G7+EA+EU27_2020+OECD+BGR+HRV+ROU..._Z.Y._T.Y_GE15..Q?startPeriod=2015-Q1&dimensionAtObservation=AllDimensions&format=csvfile"
   
    response = requests.get(url)    
    df = pd.read_csv(io.StringIO(response.text))
    
    df_clean = df[['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE']]
    df_clean['OBS_VALUE'] = pd.to_numeric(df_clean['OBS_VALUE'], errors='coerce')
    #df_clean['TIME_PERIOD'] = pd.PeriodIndex(df_clean['TIME_PERIOD'], freq='Q')

    ## order the data by country and time period
    df_clean = df_clean.sort_values(by=['REF_AREA', 'TIME_PERIOD']) 
    
    return df_clean

df_clean = load_data()  
countries = df_clean['REF_AREA'].unique()

st.title("OECD Unemployment Rates Dashboard") # Set the title of the Streamlit app
st.write("This dashboard shows the unemployment rates for the United States, Portugal, France, and Germany from January 2015 to the most recent available data. The data is sourced from the OECD and is updated regularly. The plot allows you to compare the unemployment trends across these countries over time.")

# Create a multiselect widget for country selection with default values set to all unique countries in the dataset
country_selection = st.multiselect("Select countries to display:", options=list(countries), default=[countries[0]], key="country_selection") 

fig, ax1 = plt.subplots(figsize=(12, 6)) # Create a figure and a set of subplots with a specified size

for country in country_selection: # Loop through the selected countries
    country_data = df_clean[df_clean['REF_AREA'] == country] # Filter the data for the current country
    ax1.plot(country_data['TIME_PERIOD'], country_data['OBS_VALUE'], label=f"{country} Unemployment Rate") # Plot TIME_PERIOD vs unemployment_rate for the current country on ax1

ax1.set_xlabel('Time') # Set the x-axis label for ax1   
plt.xticks(rotation=45) # Rotate the x-axis tick labels by 45 degrees for better readability
ax1.set_ylabel('Unemployment Rate') # Set the y-axis label for ax1
ax1.set_title('OECD Unemployment Rates Over Time') # Set the title for the plot 
ax1.legend() # Combine the lines and labels from both axes and create a single legend in the upper left corner
ax1.xaxis.set_major_locator(plt.MaxNLocator(10)) # Set the maximum number of ticks on the x-axis to 10 for better readability
st.pyplot(fig) # Display the plot in the Streamlit app  


