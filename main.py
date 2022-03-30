import streamlit as st
import pandas as pd
import snowflake.connector

# Open a connection to Snowflake, using Streamlit's secrets management
# In real life, we’d use @st.cache or @st.experimental_memo to add caching
conn = snowflake.connector.connect(**st.secrets["snowflake"])

# Get a list of available counties from the State of California Covid Dataset
# Data set is available free here: https://app.snowflake.com/marketplace/listing/GZ1MBZAUJF
# More info on the data set: https://www.snowflake.com/datasets/state-of-california-california-covid-19-datasets/ 
counties = pd.read_sql("SELECT distinct area from open_data.vw_cases ORDER BY area asc;", conn)

# Ask the user to select a county
option = st.selectbox('Select an area:', counties)

# Query the data set to get the case counts for the last 30 days for the chosen county
cases = pd.read_sql(f"SELECT date day, SUM(cases) CASES FROM open_data.vw_cases WHERE date > dateadd('days', -30, current_date()) AND area = %(option)s GROUP BY day ORDER BY day asc;", conn, params={"option":option})
cases = cases.set_index(['DAY'])

# Render a line chart showing the cases
f"Daily Cases in {option} over the last 30 days"
st.line_chart(cases)