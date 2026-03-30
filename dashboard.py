import streamlit as st
import pandas as pd # For data manipulation and analysis
import requests # For making HTTP requests to fetch the data
import io # For handling in-memory text streams
import matplotlib.pyplot as plt # For data visualization

indicator_options = {
    "Unemployment Rate": "TPS,DSD_LFS@DF_IALFS_UNE_M",
    "Employment Rate": "TPS,DSD_LFS@DF_IALFS_EMP_WAP_Q",
    "Population outside the labour force": "TPS,DSD_LFS@DF_IALFS_OLF_WAP_Q"
}

indicator_options_explanations = {
    "Unemployment Rate": "The unemployment rate is the percentage of the labor force that is unemployed and actively seeking employment. It is calculated as (Number of Unemployed / Labor Force) * 100.",
    "Employment Rate": "The employment rate is the percentage of the working-age population that is currently employed. It is calculated as (Number of Employed / Working-Age Population) * 100.",
    "Population outside the labour force": "The population outside the labour force is the percentage of the working-age population that is not part of the labour force. It is calculated as (Population outside the labour force / Working-Age Population) * 100."
}

@st.cache_data

def load_data(selected_indicator, start_period):
    
    indicator_code = indicator_options.get(selected_indicator, 'Unknown')
    
    url= f"https://sdmx.oecd.org/public/rest/data/OECD.SDD.{indicator_code},1.0/AUS+AUT+BEL+CAN+CHL+COL+CRI+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA+G7+EA+EU27_2020+OECD+BGR+HRV+ROU..._Z.Y._T.Y_GE15..Q?startPeriod={start_period}&dimensionAtObservation=AllDimensions&format=csvfile"
   
    response = requests.get(url) # Make a GET request to the specified URL to fetch the data
    df= pd.read_csv(io.StringIO(response.text))
    
    df_clean = df[['REF_AREA', 
                   'TIME_PERIOD', 
                   'OBS_VALUE', 
                   'MEASURE']]
    
    df_clean['OBS_VALUE'] = pd.to_numeric(df_clean['OBS_VALUE'], errors='coerce')
    #df_clean['TIME_PERIOD'] = pd.PeriodIndex(df_clean['TIME_PERIOD'], freq='Q')

    ## order the data by country and time period
    df_clean = df_clean.sort_values(by=['REF_AREA', 'TIME_PERIOD']) 
    
    return df_clean

st.title(f"OECD Indicators Dashboard") # Set the title of the Streamlit app

## controls into a siderbar

with st.sidebar:
    # Indicator and country selection
    selected_indicator = st.selectbox("Select the indicator:", options=list(indicator_options.keys())) # Create a selectbox widget for indicator selection with options from the indicator_options dictionary
    start_period = st.text_input("Enter the start date for the data (e.g., 2015-Q1):", value="2015-Q1") # Create a text input widget for the user to enter the start date with a default value of "2015-Q1"
     

# set a subtitle
st.subheader(f"{selected_indicator}") # Set the title of the Streamlit app
st.write(f"This dashboard shows the {selected_indicator} from {start_period} to the most recent available data. The data is sourced from the OECD and is updated regularly. The plot allows you to compare the trends across these countries over time.") 
st.write(indicator_options_explanations.get(selected_indicator, "No explanation available for this indicator.")) # Write the explanation for the selected indicator

df_clean = load_data(selected_indicator, start_period) # Load the data using the selected indicator and start period
countries = df_clean['REF_AREA'].unique()

with st.sidebar:
    country_selection = st.multiselect(
        "Select countries to display:", 
        options=list(countries), 
        default=[list(countries)[0]], 
        key="country_selection"
    )

## Plotting the data
fig, ax1 = plt.subplots(figsize=(12, 6)) 

for country in country_selection: # Loop through the selected countries
    country_data = df_clean[df_clean['REF_AREA'] == country] 
    ax1.plot(country_data['TIME_PERIOD'], 
             country_data['OBS_VALUE'], 
             label=f"{country} {selected_indicator}") 

ax1.set_xlabel('Time') 
plt.xticks(rotation=45) 
ax1.set_ylabel(f'{selected_indicator}') 
ax1.set_title(f'OECD {selected_indicator} Over Time') 
ax1.legend()
plt.legend(loc='upper center', #
           bbox_to_anchor=(0.5, -0.15), #
           ncol=3) #
ax1.xaxis.set_major_locator(plt.MaxNLocator(10)) 
st.pyplot(fig) # Display the plot in the Streamlit app  

with st.sidebar:
     ## Single quarter time period selection for bar chart
    time_period_options = df_clean['TIME_PERIOD'].unique()
    time_period_options = [None] + list(time_period_options)
    ## time period selection, but empty by default, so the user has to select one
    time_period_barchart = st.selectbox(
        "Select specific time period:", 
        options=list(time_period_options), 
        index=0, 
        key="time_period_barchart"
    )

if time_period_barchart: # Check if a time period has been selected

    st.subheader(f"{selected_indicator} - {time_period_barchart}") 
    st.write(f"This bar chart shows the {selected_indicator} for the selected countries in the specific time period of {time_period_barchart}. It allows you to compare the values across countries for that particular quarter.")
 
    df_bar = df_clean[(df_clean['TIME_PERIOD'] == time_period_barchart)] 
    fig, ax2 = plt.subplots(figsize=(12, 6))
    
    for country in country_selection: 
        country_data = df_bar[df_bar['REF_AREA'] == country] 
        ax2.bar(country_data['REF_AREA'], country_data['OBS_VALUE'], label=f"{country} {selected_indicator}") 

    plt.xlabel('Country') # Set the x-axis label
    plt.xticks(rotation=45)
    plt.ylabel(f'{selected_indicator}') # Set the y-axis label   
    plt.title(f'OECD {selected_indicator} - {time_period_barchart}') # Set the title for the plot
    plt.legend() # Display the legend´
    
    #legend on the bottom of the plot
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3) # Place the legend at the bottom of the plot, centered horizontally, with 3 columns
    st.pyplot(fig) # Display the plot in the Streamlit app


## I didn't do this alone. I was tired and asked claude to do it  I will add more indicators and visualizations in the future, related with my PhD thesis.

with st.sidebar:
    time_period_summary_start = st.selectbox(
        "Summary stats from:", 
        options=[None] + list(time_period_options), 
        index=0, 
        key="summary_start"
    )
    time_period_summary_end = st.selectbox(
        "Summary stats to:", 
        options=[None] + list(time_period_options), 
        index=0, 
        key="summary_end"
    )

if time_period_summary_start and time_period_summary_end:
    # Level 5 -- Summary Statistics Panel
    st.subheader(f"{selected_indicator} - Summary Statistics")
    # Filter for selected countries and time range
    df_summary = df_clean[
        (df_clean['REF_AREA'].isin(country_selection)) &
        (df_clean['TIME_PERIOD'] >= time_period_summary_start) &
        (df_clean['TIME_PERIOD'] <= time_period_summary_end)
    ]

    # Build one row per country
    rows = []
    for country in country_selection:
        df_country = df_summary[df_summary['REF_AREA'] == country].reset_index(drop=True)
        if df_country.empty:
            continue
        max_val = df_country['OBS_VALUE'].max()
        max_date = df_country.loc[df_country['OBS_VALUE'].idxmax(), 'TIME_PERIOD']
        min_val = df_country['OBS_VALUE'].min()
        min_date = df_country.loc[df_country['OBS_VALUE'].idxmin(), 'TIME_PERIOD']
        std_val = df_country['OBS_VALUE'].std().round(2)
#peak_dates_unemp = df_merged.loc[df_merged.groupby("REF_AREA")["unemployment_rate"].idxmax()][["REF_AREA", "TIME_PERIOD"]]
        rows.append({
            'Country': country,
            'Peak Value': max_val,
            'Peak Date': max_date,
            'Trough Value': min_val,
            'Trough Date': min_date,
            'Std Dev': std_val
        })

    df_stats = pd.DataFrame(rows).reset_index(drop=True)
    st.dataframe(df_stats)

## AI chat panel
st.subheader("Ask about the data")
st.write(f"Ask a question about the {selected_indicator} data for the selected countries: {', '.join(country_selection)}.")

user_question = st.chat_input("Type your question here...")

if user_question:
    df_to_string = df_clean[df_clean['REF_AREA'].isin(country_selection)].to_string(index=False)
    
    system_prompt = f"""You are an assistant helping a user analyse OECD labour market data. 
The user has selected the following indicator: {selected_indicator}, for the following countries: {', '.join(country_selection)}, from {start_period} to the most recent available data. 
The data available is: {df_to_string}. 
Only answer questions about the data provided. Do not make up values or reference countries or periods not present in the data.
Keep answers concise and analytical."""

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"Content-Type": "application/json"},
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1000,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_question}]
        }
    )
    
    answer = response.json()["content"][0]["text"]
    
    with st.chat_message("user"):
        st.write(user_question)
    with st.chat_message("assistant"):
        st.write(answer)


## In the future I will add other indicators and with other types of visualizations, related with my PhD thesis.