import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(page_title="Lulu UAE Simple Dashboard", layout="wide")
st.title("🛍️ Lulu UAE Business Insights Dashboard (Numbers Focus)")

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
department = st.sidebar.multiselect("Select Department", options=get_column_options("department"))

# Apply filters
filtered_df = df.copy()
if city:
    filtered_df = filtered_df[filtered_df['city'].isin(city)]
if brand:
    filtered_df = filtered_df[filtered_df['brand'].isin(brand)]
if gender:
    filtered_df = filtered_df[filtered_df['gender'].isin(gender)]
if department:
    filtered_df = filtered_df[filtered_df['department'].isin(department)]

# -------------------------------
# KPIs
# -------------------------------
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
total_revenue = filtered_df['tlv'].sum() if 'tlv' in filtered_df.columns else 0
col1.metric("Total Revenue (AED)", f"{total_revenue:,.0f}")
total_orders = filtered_df['order_id'].nunique() if 'order_id' in filtered_df.columns else 0
col2.metric("Total Orders", f"{total_orders:,}")
avg_order_value = filtered_df['tlv'].mean() if 'tlv' in filtered_df.columns and not filtered_df.empty else 0
col3.metric("Average Order Value (AED)", f"{avg_order_value:,.0f}")

# -------------------------------
# 1️⃣ Stacked Bar: Region x Gender
# -------------------------------
if 'region' in filtered_df.columns and 'gender' in filtered_df.columns:
    st.subheader("📊 Revenue by Region and Gender")
    region_gender = filtered_df.groupby(['region','gender'], as_index=False)['tlv'].sum()
    fig1 = px.bar(region_gender, x='region', y='tlv', color='gender', barmode='stack',
                  title="Stacked Revenue: Region vs Gender")
    st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# 2️⃣ Trend Line: Month of Year
# -------------------------------
if 'order_date' in filtered_df.columns:
    st.subheader("📈 Monthly Revenue Trend")
    filtered_df['order_date'] = pd.to_datetime(filtered_df['order_date'], errors='coerce')
    filtered_df['month'] = filtered_df['order_date'].dt.month
    month_trend = filtered_df.groupby('month', as_index=False)['tlv'].sum()
    fig2 = px.line(month_trend, x='month', y='tlv', markers=True,
                   title="Revenue Trend by Month", labels={'tlv':'Revenue (AED)','month':'Month'})
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# 3️⃣ Pie Charts: Brand, Gender, Age
# -------------------------------
if 'brand' in filtered_df.columns and 'gender' in filtered_df.columns and 'age' in filtered_df.columns:
    st.subheader("🥧 Revenue Distribution by Brand, Gender, and Age Group")
    # Brand
    brand_pie = filtered_df.groupby('brand', as_index=False)['tlv'].sum()
    fig3 = px.pie(brand_pie, names='brand', values='tlv', title='Revenue by Brand')
    st.plotly_chart(fig3, use_container_width=True)
    # Gender
    gender_pie = filtered_df.groupby('gender', as_index=False)['tlv'].sum()
    fig4 = px.pie(gender_pie, names='gender', values='tlv', title='Revenue by Gender')
    st.plotly_chart(fig4, use_container_width=True)
    # Age groups
    bins = [0,18,25,35,50,100]
    labels = ['<18','18-25','26-35','36-50','50+']
    filtered_df['age_group'] = pd.cut(filtered_df['age'], bins=bins, labels=labels)
    age_pie = filtered_df.groupby('age_group', as_index=False)['tlv'].sum()
    fig5 = px.pie(age_pie, names='age_group', values='tlv', title='Revenue by Age Group')
    st.plotly_chart(fig5, use_container_width=True)

# -------------------------------
# 4️⃣ Additional Simple Charts
# -------------------------------
st.subheader("📊 Additional Insights")
# Top 5 brands by revenue
if 'brand' in filtered_df.columns:
    top_brands = filtered_df.groupby('brand', as_index=False)['tlv'].sum().sort_values('tlv', ascending=False).head(5)
    fig6 = px.bar(top_brands, x='brand', y='tlv', title="Top 5 Brands by Revenue", text='tlv')
    st.plotly_chart(fig6, use_container_width=True)

# Orders by department
if 'department' in filtered_df.columns:
    dept_orders = filtered_df.groupby('department', as_index=False)['order_id'].nunique()
    fig7 = px.bar(dept_orders, x='department', y='order_id', title="Number of Orders by Department", text='order_id')
    st.plotly_chart(fig7, use_container_width=True)
