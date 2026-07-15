import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Overview", layout="wide")

from assets.ui import add_logo, kpi_card
add_logo()

@st.cache_data
def load_data():
    return pd.read_csv("dataset/dashboard_data.csv")

df = load_data()

st.markdown('''
# 🛒 Retail Demand Forecasting Dashboard
### Machine Learning Based Retail Analytics Platform
''')
st.markdown("---")

total_sales = df["Predicted_Sales"].sum()
total_customers = int(df["Customers"].sum())
total_inventory = int(df["Inventory"].sum())
avg_sales = df["Predicted_Sales"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("Forecast Sales", f"₹ {total_sales:,.0f}", "#3B82F6", "💰")
with col2:
    kpi_card("Customers", f"{total_customers:,}", "#10B981", "👥")
with col3:
    kpi_card("Inventory", f"{total_inventory:,}", "#F59E0B", "📦")
with col4:
    kpi_card("Average Sales", f"{avg_sales:.2f}", "#EF4444", "📈")

st.write("")
st.subheader("📈 Monthly Sales Trend")

month_map = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
             7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

monthly = df.groupby("Month")["Predicted_Sales"].sum().reset_index()
monthly["Month_Name"] = monthly["Month"].map(month_map)
monthly = monthly.sort_values("Month")

fig = px.line(monthly, x="Month_Name", y="Predicted_Sales", markers=True, color_discrete_sequence=["#3B82F6"])
fig.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", font=dict(color="white"), height=350, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

c1, c2 = st.columns(2)
with c1:
    st.subheader("🌍 Sales by Region")
    region = df.groupby("Region")["Predicted_Sales"].sum().reset_index()
    region["Region"] = region["Region"].astype(str)
    fig1 = px.bar(region, x="Region", y="Predicted_Sales", color_discrete_sequence=["#10B981"])
    fig1.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", xaxis=dict(type='category'), height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("🛍 Sales by Category")
    category = df.groupby("Category")["Predicted_Sales"].sum().reset_index()
    fig2 = px.pie(category, names="Category", values="Predicted_Sales", hole=0.45)
    fig2.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

left, right = st.columns([2,1])
with left:
    st.subheader("🏆 Top Categories")
    top_cat = df.groupby("Category")["Predicted_Sales"].sum().sort_values(ascending=False).reset_index()
    top_cat["Category"] = top_cat["Category"].astype(str)
    fig3 = px.bar(top_cat, x="Predicted_Sales", y="Category", orientation="h", color_discrete_sequence=["#3B82F6"])
    fig3.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", yaxis=dict(type='category'), height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig3, use_container_width=True)

with right:
    st.subheader("🤖 Dataset Summary")
    st.write("")
    m1, m2 = st.columns(2)
    with m1:
        kpi_card("Stores", df["Store_ID"].nunique(), "#3B82F6", "🏪")
        st.write("")
        kpi_card("Regions", df["Region"].nunique(), "#F59E0B", "🌍")
    with m2:
        kpi_card("Products", df["Product_ID"].nunique(), "#10B981", "📦")
        st.write("")
        kpi_card("Categories", df["Category"].nunique(), "#EF4444", "📂")

st.markdown("---")

st.markdown("---")
st.subheader("🔗 Price vs Sales Correlation")
fig_scatter = px.scatter(df, x="Price", y="Predicted_Sales", color="Category", opacity=0.7)
fig_scatter.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", height=400, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")
st.subheader("📄 Forecast Preview")
preview = df[["Store_ID", "Product_ID", "Category", "Region", "Customers", "Inventory", "Predicted_Sales"]].head(15)
st.dataframe(preview, use_container_width=True, hide_index=True)

st.info("Retail Demand Forecasting Dashboard")
