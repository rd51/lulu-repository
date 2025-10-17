import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(page_title="Lulu UAE Dashboard", layout="wide")
st.title("🛍️ Lulu UAE Business Insights Dashboard")

# -------------------------------
# Load dataset
# -------------------------------
uploaded_file = "lulu_uae_master_2000_copy.csv"

try:
    df = pd.read_csv(uploaded_file)
except FileNotFoundError:
    st.error(f"File not found: {uploaded_file}")
    st.stop()

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# -------------------------------
# Sidebar filters
# -------------------------------
st.sidebar.header("🔍 Filters")

def get_column_options(col_name):
    return df[col_name].unique() if col_name in df.columns else []

city = st.sidebar.multiselect("Select City", options=get_column_options("city"))
brand = st.sidebar.multiselect("Select Brand", options=get_column_options("brand"))
gender = st.sidebar.multiselect("Select Gender", options=get_column_options("gender"))

# Apply filters
filtered_df = df.copy()
if city:
    filtered_df = filtered_df[filtered_df['city'].isin(city)]
if brand:
    filtered_df = filtered_df[filtered_df['brand'].isin(brand)]
if gender:
    filtered_df = filtered_df[filtered_df['gender'].isin(gender)]

# -------------------------------
# Key Performance Indicators
# -------------------------------
st.subheader("📊 Key Performance Indicators")
col1, col2, col3 = st.columns(3)

# Total Revenue
total_revenue = filtered_df['tlv'].sum() if 'tlv' in filtered_df.columns else 0
col1.metric("Total Revenue (AED)", f"{total_revenue:,.0f}")

# Total Orders
total_orders = filtered_df['order_id'].nunique() if 'order_id' in filtered_df.columns else 0
col2.metric("Total Orders", f"{total_orders:,}")

# Average Order Value
avg_order_value = filtered_df['tlv'].mean() if 'tlv' in filtered_df.columns and not filtered_df.empty else 0
col3.metric("Average Order Value", f"{avg_order_value:,.0f}")

# -------------------------------
# 1️⃣ Sales by Brand and Gender
# -------------------------------
if 'brand' in filtered_df.columns and 'tlv' in filtered_df.columns:
    color_col = 'gender' if 'gender' in filtered_df.columns else None
    st.subheader("🧍 Sales by Brand and Gender")
    fig1 = px.bar(filtered_df, x="brand", y="tlv", color=color_col, barmode="group")
    st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# 2️⃣ Promo Impact on Quantity
# -------------------------------
if 'discount_percentage' in filtered_df.columns and 'quantity' in filtered_df.columns:
    st.subheader("💸 Discount % vs Quantity Sold")
    fig2 = px.scatter(
        filtered_df,
        x="discount_percentage",
        y="quantity",
        color="brand" if 'brand' in filtered_df.columns else None)
