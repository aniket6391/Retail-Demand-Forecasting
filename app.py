import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="Retail Demand Forecasting",
    page_icon="🛒",
    layout="wide"
)

from assets.ui import add_logo, kpi_card
add_logo()

# Load dataset for live landing page data
@st.cache_data
def load_data():
    return pd.read_csv("dataset/dashboard_data.csv")

df = load_data()

# ==========================================================
# HERO SECTION
# ==========================================================
st.markdown("""
<div style="padding: 20px 0px 30px 0px; text-align: center;">
    <h1 style="background: -webkit-linear-gradient(45deg, #3B82F6, #10B981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.8em; font-weight: 800; margin-bottom: 0; letter-spacing: -1px;">
        Demand Forecasting Command Center
    </h1>
    <h3 style="color: #94A3B8; font-weight: 300; font-size: 1.4em; margin-top: 10px;">
        Real-time Sales & Inventory Optimization
    </h3>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================================
# EFFICIENT KPI RIBBON (2 Rows of Metrics)
# ==========================================================
top_region = df.groupby("Region")["Predicted_Sales"].sum().idxmax()
top_category = df.groupby("Category")["Predicted_Sales"].sum().idxmax()
avg_inv = df["Inventory"].mean()
total_stores = df["Store_ID"].nunique()

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total Forecast Sales", f"₹ {df['Predicted_Sales'].sum():,.0f}", "#3B82F6", "💰")
with k2:
    kpi_card("Total Customers", f"{df['Customers'].sum():,}", "#10B981", "👥")
with k3:
    kpi_card("Top Region", top_region, "#F59E0B", "👑")
with k4:
    kpi_card("Top Category", top_category, "#8B5CF6", "🏆")

st.write("")

k5, k6, k7, k8 = st.columns(4)
with k5:
    kpi_card("Active Products", f"{df['Product_ID'].nunique()}", "#3B82F6", "📦")
with k6:
    kpi_card("Total Stores", f"{total_stores}", "#10B981", "🏪")
with k7:
    kpi_card("Avg Product Price", f"₹ {df['Price'].mean():.1f}", "#F59E0B", "🏷️")
with k8:
    kpi_card("Average Inventory", f"{avg_inv:,.0f} units", "#EF4444", "🏭")

st.write("")
st.write("")

# ==========================================================
# ROW 1: TRENDS & CATEGORIES
# ==========================================================
col_chart, col_pie = st.columns([1.5, 1])

with col_chart:
    st.markdown("<h3 style='color: white; margin-bottom: 10px;'>📉 Year-to-Date Sales Trend</h3>", unsafe_allow_html=True)
    month_map = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
    trend = df.groupby("Month")["Predicted_Sales"].sum().reset_index()
    trend["Month_Name"] = trend["Month"].map(month_map)

    fig1 = px.area(trend, x="Month_Name", y="Predicted_Sales", markers=True, color_discrete_sequence=["#3B82F6"])
    fig1.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", height=320, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig1, use_container_width=True)

with col_pie:
    st.markdown("<h3 style='color: white; margin-bottom: 10px;'>🥧 Sales by Category</h3>", unsafe_allow_html=True)
    cat_sales = df.groupby("Category")["Predicted_Sales"].sum().reset_index()
    fig2 = px.pie(cat_sales, names="Category", values="Predicted_Sales", hole=0.45)
    fig2.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", height=320, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig2, use_container_width=True)

# ==========================================================
# ROW 2: REGIONAL ALERTS & TOP PERFORMERS
# ==========================================================
st.write("")
col_bar, col_table = st.columns([1, 1.5])

with col_bar:
    st.markdown("<h3 style='color: white; margin-bottom: 10px;'>🌍 Regional Performance</h3>", unsafe_allow_html=True)
    reg_sales = df.groupby("Region")["Predicted_Sales"].sum().reset_index()
    fig3 = px.bar(reg_sales, x="Region", y="Predicted_Sales", color_discrete_sequence=["#10B981"])
    fig3.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", height=300, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig3, use_container_width=True)

with col_table:
    st.markdown("<h3 style='color: #EF4444; margin-bottom: 10px;'>⚠️ Critical Low Inventory Alerts</h3>", unsafe_allow_html=True)
    # Get the 6 products with the lowest inventory
    low_inv = df[["Store_ID", "Product_ID", "Category", "Inventory", "Predicted_Sales"]].sort_values("Inventory", ascending=True).head(6).reset_index(drop=True)
    
    st.dataframe(
        low_inv,
        use_container_width=True,
        hide_index=True,
        height=240
    )

st.divider()

# ==========================================================
# QUICK NAVIGATION FOOTER
# ==========================================================
st.markdown("<h4 style='color: #94A3B8;'>⚡ Navigate via Sidebar for Deep Analytics:</h4>", unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
c1.success(f"📊 **Overview**\n\nTotal Sales: ₹{df['Predicted_Sales'].sum():,.0f}")
c2.success(f"🌍 **Regional**\n\nTop Region: {top_region}")
c3.success(f"📦 **Products**\n\nActive Items: {df['Product_ID'].nunique()}")
c4.warning(f"🤖 **Forecasting**\n\nAI Predictions")
c5.info(f"📈 **Model Metrics**\n\nAccuracy: 74.1%")

st.write("")
st.divider()

# ==========================================================
# RECENT DATA SNAPSHOT
# ==========================================================
st.markdown("<h4 style='color: white; margin-bottom: 10px;'>📊 Recent Sales Forecasts Snapshot</h4>", unsafe_allow_html=True)
sample_data = df[["Store_ID", "Category", "Region", "Inventory", "Predicted_Sales"]].tail(5).reset_index(drop=True)
sample_data["Predicted_Sales"] = sample_data["Predicted_Sales"].apply(lambda x: f"₹ {x:,.0f}")
st.dataframe(sample_data, use_container_width=True, hide_index=True)

st.write("")
st.caption("© Retail Demand Forecasting System")
