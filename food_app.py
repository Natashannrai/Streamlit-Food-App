# Import library and read dataset
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3
from geopy.geocoders import Nominatim
from tqdm import tqdm
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import time
import os

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
st.title("Global Street Food App")
st.subheader("Home Page")

# Display dataset
st.dataframe(df_cleaned)

# Whats the cheapest food in the dataset
cheapest = df.loc[df["Typical Price (USD)"].idxmin()]

# Display
st.subheader("Cheapest Food in Dataset")
st.write(f"**{cheapest['Dish Name']}** is the cheapest food at **${cheapest['Typical Price (USD)']}**")

# Price range graph
st.subheader("Food Price Range")
# User choice
food_list = df["Dish Name"].unique()
food_choice = st.selectbox("Choose a food:", food_list)
filtered_df = df[df["Dish Name"] == food_choice]
# Creating the graph
if not filtered_df.empty:
    st.write(f"Found {len(filtered_df)} entries for '{food_choice}':")
    st.dataframe(filtered_df)

    # Create price range plot
    fig, ax = plt.subplots()
    ax.hist(filtered_df["Typical Price (USD)"], bins=5, color="skyblue", edgecolor="black")
    ax.set_title(f"Price Range for {food_choice.title()}")
    ax.set_xlabel("Price (USD)")
    ax.set_ylabel("Frequency")

    st.pyplot(fig)
else:
    st.warning("No data found for that food.")

# Graph of the dataset
col1, col2 = st.columns(2)

with col1:
    st.subheader("The distribution of Vegetarian and Non-Vegetarian Food")
    veg_counts = df_cleaned["Vegetarian"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(veg_counts.values, labels=veg_counts.index, autopct="%1.1f%%", colors=["green", "red"])
    st.pyplot(fig1)

with col2:
    st.subheader("The Distribution of Cooking Methods in The Dataset")
    cook_counts = df_cleaned["Cooking Method"].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(cook_counts.values, labels=cook_counts.index, autopct="%1.1f%%")
    st.pyplot(fig2)
