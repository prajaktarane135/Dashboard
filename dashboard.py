# Tours and Travels Dashboard using Streamlit

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load sample or user-provided data
@st.cache_data
def load_data():
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

# Apply custom theme colors
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f7fa;
    }
    .css-1v0mbdj, .css-12oz5g7 {
        color: #1f4e79;
    }
    .css-1d391kg {
        background-color: #ffa500 !important;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.title("Filters")
selected_destinations = st.sidebar.multiselect("Select Destinations", df['Destination'].unique(), default=df['Destination'].unique())
min_age, max_age = st.sidebar.slider("Age Range", int(df['Age'].min()), int(df['Age'].max()), (20, 50))

# Filter Data
df_filtered = df[(df['Destination'].isin(selected_destinations)) & (df['Age'] >= min_age) & (df['Age'] <= max_age)]

# KPIs
st.title("\U0001F30E Global Tours & Travels Dashboard")
st.markdown("### Key Performance Indicators")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Bookings", int(df_filtered['Bookings'].sum()))
kpi2.metric("Total Revenue", f"${df_filtered['Revenue'].sum():,.0f}")
kpi3.metric("Average Rating", round(df_filtered['Rating'].mean(), 2))

# Layout for charts
chart1, chart2 = st.columns(2)
with chart1:
    fig_map = px.scatter_geo(df_filtered, lat="lat", lon="long", hover_name="Destination",
                             size="Bookings", projection="natural earth", title="Global Bookings Distribution",
                             color_discrete_sequence=["#1f4e79"])
    st.plotly_chart(fig_map, use_container_width=True)

with chart2:
    fig_time = px.line(df_filtered, x='Booking_Date', y='Bookings', title='Bookings Over Time',
                       color_discrete_sequence=["#ffa500"])
    st.plotly_chart(fig_time, use_container_width=True)

# Destination Rankings
st.markdown("### Destination Rankings and Demographics")
col4, col5 = st.columns(2)
with col4:
    fig_dest = px.bar(df_filtered.groupby('Destination')["Bookings"].sum().sort_values(ascending=False).head(10).reset_index(),
                      x='Destination', y='Bookings', title='Top 10 Destinations',
                      color_discrete_sequence=["#1f4e79"])
    st.plotly_chart(fig_dest, use_container_width=True)

with col5:
    fig_age = px.histogram(df_filtered, x="Age", nbins=10, title="Traveler Age Distribution",
                           color_discrete_sequence=["#ffa500"])
    st.plotly_chart(fig_age, use_container_width=True)

# Gender and Ratings
col6, col7 = st.columns(2)
with col6:
    fig_gender = px.pie(df_filtered, names='Gender', title='Gender Distribution',
                        color_discrete_sequence=["#1f4e79", "#ffa500"])
    st.plotly_chart(fig_gender, use_container_width=True)

with col7:
    fig_rating = px.histogram(df_filtered, x="Rating", title="Customer Ratings",
                              color_discrete_sequence=["#1f4e79"])
    st.plotly_chart(fig_rating, use_container_width=True)

# Data Table
st.markdown("### Detailed Booking Data")
st.dataframe(df_filtered, use_container_width=True)
