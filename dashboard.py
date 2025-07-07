# Tours and Travels Dashboard using Streamlit

import streamlit as st
import pandas as pd
import plotly.express as px

# Load sample or user-provided data
@st.cache_data
def load_data():
    # For demo, you can replace this with pd.read_csv('your_data.csv')
    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv")
    df.rename(columns={"iata": "Destination", "cnt": "Bookings"}, inplace=True)
    df['Revenue'] = df['Bookings'] * 350  # dummy revenue
    df['Rating'] = (4 + (df['Bookings'] % 2) * 0.5)  # dummy rating
    df['Booking_Date'] = pd.date_range("2023-01-01", periods=len(df))
    df['Age'] = 20 + (df['Bookings'] % 30)
    df['Gender'] = ['Male' if i % 2 == 0 else 'Female' for i in range(len(df))]
    return df

# Load data
df = load_data()

# Sidebar Filters
st.sidebar.title("Filters")
selected_destinations = st.sidebar.multiselect("Select Destinations", df['Destination'].unique(), default=df['Destination'].unique())
min_age, max_age = st.sidebar.slider("Age Range", int(df['Age'].min()), int(df['Age'].max()), (20, 50))

# Filter Data
df_filtered = df[(df['Destination'].isin(selected_destinations)) & (df['Age'] >= min_age) & (df['Age'] <= max_age)]

# KPIs
st.title("\U0001F30E Global Tours & Travels Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Bookings", int(df_filtered['Bookings'].sum()))
col2.metric("Total Revenue", f"${df_filtered['Revenue'].sum():,.0f}")
col3.metric("Average Rating", round(df_filtered['Rating'].mean(), 2))

# Booking Heatmap (simulated with coordinates)
fig_map = px.scatter_geo(df_filtered, lat="lat", lon="long", hover_name="Destination",
                         size="Bookings", projection="natural earth", title="Global Bookings Distribution")
st.plotly_chart(fig_map)

# Bookings over Time
fig_time = px.line(df_filtered, x='Booking_Date', y='Bookings', title='Bookings Over Time')
st.plotly_chart(fig_time)

# Destination Rankings
fig_dest = px.bar(df_filtered.groupby('Destination')["Bookings"].sum().sort_values(ascending=False).head(10).reset_index(),
                  x='Destination', y='Bookings', title='Top 10 Destinations')
st.plotly_chart(fig_dest)

# Age Distribution
fig_age = px.histogram(df_filtered, x="Age", nbins=10, title="Traveler Age Distribution")
st.plotly_chart(fig_age)

# Gender Pie
fig_gender = px.pie(df_filtered, names='Gender', title='Gender Distribution')
st.plotly_chart(fig_gender)

# Rating Distribution
fig_rating = px.histogram(df_filtered, x="Rating", title="Customer Ratings")
st.plotly_chart(fig_rating)

# Data Table
st.subheader("Detailed Booking Data")
st.dataframe(df_filtered)
