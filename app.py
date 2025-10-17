import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(page_title="Lulu UAE Advanced Dashboard", layout="wide")
st.title("🛍️ Lulu UAE Advanced Business Insights Dashboard")

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
# Key Performance Indicators
# -------------------------------
st.subheader("📊 Key Performance Indicators")
col1, col2, col3 = st.columns(3)

total_revenue = filtered_df['tlv'].sum() if 'tlv' in filtered_df.columns else 0
col1.metric("Total Revenue (AED)", f"{total_revenue:,.0f}")

total_orders = filtered_df['order_id'].nunique() if 'order_id' in filtered_df.columns else 0
col2.metric("Total Orders", f"{total_orders:,}")

avg_order_value = filtered_df['tlv'].mean() if 'tlv' in filtered_df.columns and not filtered_df.empty else 0
col3.metric("Average Order Value", f"{avg_order_value:,.0f}")

# -------------------------------
# 1️⃣ Top 10 SKUs by Revenue
# -------------------------------
if 'sku_id' in filtered_df.columns and 'tlv' in filtered_df.columns:
    st.subheader("🏆 Top 10 SKUs by Revenue")
    sku_sales = filtered_df.groupby("sku_id", as_index=False)["tlv"].sum().sort_values(by="tlv", ascending=False).head(10)
    fig1 = px.bar(sku_sales, x="tlv", y="sku_id", orientation="h", title="Top 10 SKUs by Revenue", text="tlv")
    st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# 2️⃣ Revenue by Brand & Department (Stacked)
# -------------------------------
if 'brand' in filtered_df.columns and 'department' in filtered_df.columns and 'tlv' in filtered_df.columns:
    st.subheader("🏷️ Revenue by Brand and Department")
    brand_dept = filtered_df.groupby(['brand','department'], as_index=False)['tlv'].sum()
    fig2 = px.bar(brand_dept, x="brand", y="tlv", color="department", barmode="stack",
                  title="Stacked Revenue: Brand vs Department")
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# 3️⃣ Heatmap: City vs Hour of Day
# -------------------------------
if 'city' in filtered_df.columns and 'hour_of_day' in filtered_df.columns and 'tlv' in filtered_df.columns:
    st.subheader("🌡️ City vs Hour of Day Revenue Heatmap")
    heatmap_df = filtered_df.groupby(['city','hour_of_day'], as_index=False)['tlv'].sum()
    heatmap_pivot = heatmap_df.pivot(index='city', columns='hour_of_day', values='tlv').fillna(0)
    fig3 = ff.create_annotated_heatmap(
        z=heatmap_pivot.values,
        x=list(heatmap_pivot.columns),
        y=list(heatmap_pivot.index),
        colorscale='Viridis',
        showscale=True
    )
    st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# 4️⃣ Treemap: Revenue by Category and Brand
# -------------------------------
if 'category' in filtered_df.columns and 'brand' in filtered_df.columns and 'tlv' in filtered_df.columns:
    st.subheader("📊 Revenue Treemap: Category & Brand")
    fig4 = px.treemap(filtered_df, path=['brand','category'], values='tlv',
                      color='tlv', color_continuous_scale='Viridis',
                      title="Revenue Distribution by Brand and Category")
    st.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# 5️⃣ Discount % vs TLV per Brand with Trendline
# -------------------------------
if 'discount_percentage' in filtered_df.columns and 'tlv' in filtered_df.columns and 'brand' in filtered_df.columns:
    st.subheader("💸 Discount % vs Revenue per Brand")
    scatter_df = filtered_df[['discount_percentage','tlv','brand']].dropna()
    try:
        fig5 = px.scatter(scatter_df, x="discount_percentage", y="tlv", color="brand",
                          trendline="ols", title="Impact of Discounts on Revenue by Brand")
    except:
        fig5 = px.scatter(scatter_df, x="discount_percentage", y="tlv", color="brand",
                          title="Impact of Discounts on Revenue by Brand (trendline unavailable)")
    st.plotly_chart(fig5, use_container_width=True)

# -------------------------------
# 6️⃣ New: Stacked Bar – Region, Gender, Marketing
# -------------------------------
if 'region' in filtered_df.columns and 'gender' in filtered_df.columns and 'marketing' in filtered_df.columns:
    st.subheader("📊 Revenue by Region, Gender, and Marketing Channel")
    region_gender_marketing = filtered_df.groupby(['region','gender','marketing'], as_index=False)['tlv'].sum()
    fig6 = px.bar(region_gender_marketing, x='region', y='tlv', color='gender',
                  barmode='stack', facet_col='marketing',
                  title="Stacked Revenue: Region vs Gender vs Marketing")
    st.plotly_chart(fig6, use_container_width=True)

# -------------------------------
# 7️⃣ New: Trend Line – Month of Year
# -------------------------------
if 'order_date' in filtered_df.columns:
    st.subheader("📈 Revenue Trend Across Months")
    filtered_df['order_date'] = pd.to_datetime(filtered_df['order_date'], errors='coerce')
    filtered_df['month'] = filtered_df['order_date'].dt.month
    month_trend = filtered_df.groupby('month', as_index=False)['tlv'].sum()
    fig7 = px.line(month_trend, x='month', y='tlv', markers=True,
                   title="Monthly Revenue Trend",
                   labels={'tlv': 'Revenue (AED)', 'month': 'Month'})
    st.plotly_chart(fig7, use_container_width=True)

# -------------------------------
# 8️⃣ New: Pie Charts – Brand, Gender, Age
# -------------------------------
if 'brand' in filtered_df.columns and 'gender' in filtered_df.columns and 'age' in filtered_df.columns:
    st.subheader("🥧 Revenue Distribution by Brand, Gender, and Age")
    
    # Brand Pie
    brand_pie = filtered_df.groupby('brand', as_index=False)['tlv'].sum()
    fig8 = px.pie(brand_pie, names='brand', values='tlv', title='Revenue Distribution by Brand')
    st.plotly_chart(fig8, use_container_width=True)
    
    # Gender Pie
    gender_pie = filtered_df.groupby('gender', as_index=False)['tlv'].sum()
    fig9 = px.pie(gender_pie, names='gender', values='tlv', title='Revenue Distribution by Gender')
    st.plotly_chart(fig9, use_container_width=True)
    
    # Age Pie
    bins = [0, 18, 25, 35, 50, 100]
    labels = ['<18','18-25','26-35','36-50','50+']
    filtered_df['age_group'] = pd.cut(filtered_df['age'], bins=bins, labels=labels)
    age_pie = filtered_df.groupby('age_group', as_index=False)['tlv'].sum()
    fig10 = px.pie(age_pie, names='age_group', values='tlv', title='Revenue Distribution by Age Group')
    st.plotly_chart(fig10, use_container_width=True)

# -------------------------------
# Footer
# -------------------------------
st.markdown("© 2025 Lulu UAE Insights | Developed by Rakshanda Dhote")