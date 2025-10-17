import streamlit as st
import pandas as pd
import plotly.express as px

# Page title
st.set_page_config(page_title="Lulu UAE Dashboard", layout="wide")
st.title("🛍️ Lulu UAE Business Insights Dashboard")

# Load dataset
uploaded_file = "lulu_uae_master_2000_copy.csv"
df = pd.read_csv(uploaded_file)

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Sidebar filters
st.sidebar.header("🔍 Filters")
city = st.sidebar.multiselect("Select City", options=df['city'].unique())
brand = st.sidebar.multiselect("Select Brand", options=df['brand'].unique())
gender = st.sidebar.multiselect("Select Gender", options=df['gender'].unique())

filtered_df = df.copy()
if city:
    filtered_df = filtered_df[filtered_df['city'].isin(city)]
if brand:
    filtered_df = filtered_df[filtered_df['brand'].isin(brand)]
if gender:
    filtered_df = filtered_df[filtered_df['gender'].isin(gender)]

# KPIs
st.subheader("📊 Key Performance Indicators")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue (AED)", f"{filtered_df['total_value'].sum():,.0f}")
col2.metric("Total Orders", f"{filtered_df['order_id'].nunique():,}")
col3.metric("Average Order Value", f"{filtered_df['total_value'].mean():,.0f}")

# 1️⃣ Sales by Brand and Gender
st.subheader("🧍 Sales by Brand and Gender")
fig1 = px.bar(filtered_df, x="brand", y="total_value", color="gender", barmode="group")
st.plotly_chart(fig1, use_container_width=True)

# 2️⃣ Promo Impact on Quantity
if "discount_%" in filtered_df.columns:
    st.subheader("💸 Discount % vs Quantity Sold")
    fig2 = px.scatter(filtered_df, x="discount_%", y="quantity", color="brand", title="Promo Impact on Quantity")
    st.plotly_chart(fig2, use_container_width=True)

# 3️⃣ City-Wise Sales
st.subheader("📍 City-Wise Total Sales")
city_sales = filtered_df.groupby("city", as_index=False)["total_value"].sum()
fig3 = px.bar(city_sales, x="city", y="total_value", title="Total Sales by City")
st.plotly_chart(fig3, use_container_width=True)

# 4️⃣ Age Group vs Brand
if "age_group" in filtered_df.columns:
    st.subheader("🎯 Brand Preference by Age Group")
    fig4 = px.bar(filtered_df, x="brand", y="total_value", color="age_group", barmode="group")
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("© 2025 Lulu UAE Insights | Developed by Rakshanda Dhote")
