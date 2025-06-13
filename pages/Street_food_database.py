import pandas as pd
import streamlit as st
import sqlite3

# Konek database
conn = sqlite3.connect("global_street_food.db")

# Query data
df = pd.read_sql_query("SELECT * FROM global_street_food", conn)

# Streamlit code
st.title("Input/Edit Database")

# Edit dataset
df = st.data_editor(df, num_rows="dynamic")