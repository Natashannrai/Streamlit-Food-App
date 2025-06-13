# Import library and read dataset
import pandas as pd
import streamlit as st
import sqlite3

# Konek database
conn = sqlite3.connect("global_street_food.db")

# Query data
df = pd.read_sql_query("SELECT * FROM global_street_food", conn)

data_clean = df.drop(columns=["Typical Price (USD)"])

###Clean duplicate data
for col in data_clean.columns:
    duplicate_count = data_clean[col].duplicated().sum()
    print(f"Column '{col}' has {duplicate_count}")

df_cleaned = data_clean.apply(lambda x: x.str.strip().str.lower() if x.dtype == "object" else x)
df_cleaned = data_clean.drop_duplicates()

# Streamlit code
st.title("Search Food Around The World")

# Sidebar filters
region = st.sidebar.selectbox("Select Region", sorted(df_cleaned['Region/City'].dropna().unique()))
country_options = df_cleaned[df_cleaned['Region/City'] == region]['Country'].dropna().unique()
country = st.sidebar.selectbox("Select Country", sorted(country_options))

# Filter data
filtered_df = df_cleaned[(df_cleaned['Region/City'] == region) & (df_cleaned['Country'] == country)]

st.subheader(f"Street Foods in {country}")
for i, row in filtered_df.iterrows():
    st.markdown(f"### {row['Dish Name']}")
    st.markdown(f"Description: {row['Description']}")
    st.markdown(f"Ingredients: {row['Ingredients']}")
    st.markdown("---")
