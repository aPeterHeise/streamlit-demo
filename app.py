import streamlit as st
import pandas as pd
import snowflake.connector

st.title("❄️ Snowflake Orders Dashboard")

st.markdown("""
This dashboard provides a view of daily orders from a sample Snowflake database.
Use the dropdown below to select a country and view the corresponding order data.
""")

# Open a connection to Snowflake, using Streamlit's secrets management
# In real life, we’d use @st.cache or @st.experimental_memo to add caching
conn = snowflake.connector.connect(**st.secrets["snowflake"])

# Get a list of available counties.
counties = pd.read_sql("SELECT distinct N_NAME from NATION order by N_NAME;", conn)

# Ask the user to select a county
option = st.sidebar.selectbox('Select an area:', counties)

# Query the data set to get the order counts
with st.spinner(f"Fetching order data for {option}..."):
    cases = pd.read_sql(f"""
        SELECT O.O_ORDERDATE, count(1) as NUM_ORDERS
        FROM CUSTOMER
        JOIN NATION on NATION.N_NATIONKEY=CUSTOMER.C_NATIONKEY
        JOIN "ORDERS" O on O.O_CUSTKEY=CUSTOMER.C_CUSTKEY
        WHERE NATION.N_NAME='{option}'
        GROUP BY O.O_ORDERDATE
        ORDER BY O.O_ORDERDATE;
        """, conn, params={"option":option})
    cases = cases.set_index(['O_ORDERDATE'])

# Render a line chart showing the cases
st.subheader(f"Daily Orders in {option}")
st.line_chart(cases)