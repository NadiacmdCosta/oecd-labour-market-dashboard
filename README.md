# OECD Interactive Labour Market Dashboard

An interactive data dashboard built with Python and Streamlit, pulling live labour market data from the OECD API. This is a portfolio project built as part of a broader journey into Python, data science, and applied economic research.

---

## What This Project Is

This dashboard lets you explore key labour market indicators across OECD countries -- unemployment rate, employment rate, and population outside the labour force -- with interactive controls for country selection, time period, and chart type.

It was built as **Project 3** in a structured Python learning path, with the goal of applying programming skills directly to the kind of data and questions that come up in labour economics research. The project is also a portfolio piece demonstrating that Python skills are being developed with real analytical intent, not just syntax exercises.

---

## Background: Learning Python Through Research-Relevant Projects

I completed a PhD in Engineering and Management at Instituto Superior Técnico (IST), Lisbon, with a focus on Labour Economics. My quantitative toolkit during the PhD was built around Stata -- survival duration models, multinomial logit, large-scale microdata from sources like EU-SILC and Quadros de Pessoal.

This project is part of a deliberate effort to expand that toolkit into Python, working progressively from basic scripts toward data pipelines, interactive dashboards, and eventually machine learning. Each project in the series is designed to be both a learning exercise and something genuinely useful or presentable.

The learning process was supported by Claude (Anthropic's AI assistant), used as a coding instructor in a Socratic style -- meaning the focus was on reasoning through problems before writing code, understanding the *why* behind each decision, not just copying solutions. The code in this repository was written by me through that guided process.

---

## Project Structure

The entire dashboard lives in a single file: `dashboard.py`. This was a deliberate architectural decision -- rather than splitting across files at each stage, the file grows level by level, which makes it easier to see how each new feature connects to what already exists.

The project was built in six levels:

**Level 1 -- Streamlit Hello World**
Getting a static chart to render in the browser. The main challenge here was understanding the matplotlib figure/axes model (`fig, ax = plt.subplots()`) and how Streamlit's `st.pyplot()` replaces `plt.show()`.

**Level 2 -- Interactive Controls**
Adding country selection via `st.multiselect()` and connecting it to the chart. This introduced `@st.cache_data` to avoid repeated API calls on every interaction, and the logic of how Streamlit reruns the script on each user action.

**Level 3 -- Multiple Indicators**
Allowing the user to switch between indicators (unemployment rate, employment rate, population outside the labour force). Each indicator maps to a different OECD API endpoint. A dictionary at the top of the file maps readable labels to API codes -- a pattern borrowed from how imports work: declare dependencies before they are used.

**Level 4 -- Chart Type and Layout**
Moving all controls into a sidebar using `st.sidebar`, and adding a conditional bar chart that appears only when the user selects a specific time period. The bar chart is designed around a single-quarter snapshot across countries, which is analytically cleaner than averaging across periods.

**Level 5 -- Peak and Trough Panel**
A summary table showing, for each selected country and a user-defined time range: the peak value and the date it occurred, the trough value and date, and the standard deviation as a measure of volatility. Plain averages were deliberately excluded -- they hide variability and are less interpretable for quarterly labour market data. The table is built using a list-of-dictionaries pattern, one row per country, assembled in a loop.

**Level 6 -- AI Chat Panel** *(work in progress)*
A chat panel at the bottom of the dashboard that will allow the user to ask questions about the data currently displayed. The system prompt is designed to constrain the model to the visible data and prevent hallucination of figures not in scope. The API key integration via `.env` and `python-dotenv` is in place; full wiring is pending.

---

## Technical Stack

- **Python 3.14**
- **Streamlit** -- dashboard framework
- **pandas** -- data manipulation
- **matplotlib** -- charting
- **requests** -- API calls
- **python-dotenv** -- API key management (for Level 6)
- **Data source:** OECD SDMX REST API (Labour Force Statistics)

---

## How to Run

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the dashboard:
   ```
   python -m streamlit run dashboard.py
   ```
4. For Level 6 (AI chat), create a `.env` file in the project root with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_key_here
   ```

---

## Status

| Level | Feature | Status |
|---|---|---|
| 1 | Static chart in Streamlit | Complete |
| 2 | Country selection + caching | Complete |
| 3 | Multi-indicator API calls | Complete |
| 4 | Sidebar layout + bar chart | Complete |
| 5 | Peak and trough panel | Complete |
| 6 | AI chat panel | Work in progress |

---

## Disclaimer

This project is part of an active learning process. The AI chat panel (Level 6) is not yet fully functional -- the structure and system prompt are in place, but the API integration is pending completion. The rest of the dashboard is fully working.

---

## About the Data

All data is fetched live from the [OECD SDMX REST API](https://data.oecd.org/api/sdmx-json-documentation/). No data files are stored in this repository. Coverage includes all OECD member countries plus selected aggregates (G7, Euro Area, EU27, OECD average).
