import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Regional Analysis", layout="wide")

from assets.ui import add_logo, kpi_card
add_logo()

@st.cache_data
def load_data():
    return pd.read_csv("dataset/dashboard_data.csv")

df = load_data()

st.markdown('''
# 🌍 Regional Analysis
### Regional performance and metrics.
''')

st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Forecast Sales", f"₹ {df['Predicted_Sales'].sum():,.0f}", "#3B82F6", "💰")
with c2:
    kpi_card("Customers", f"{df['Customers'].sum():,}", "#10B981", "👥")
with c3:
    kpi_card("Inventory", f"{df['Inventory'].sum():,}", "#F59E0B", "📦")
with c4:
    kpi_card("Stores", f"{df['Store_ID'].nunique()}", "#EF4444", "🏪")

st.markdown("---")

r1c1, r1c2 = st.columns(2)

with r1c1:
    st.subheader("📈 Forecast Sales by Region")
    region = df.groupby("Region")["Predicted_Sales"].sum().reset_index()
    region["Region"] = region["Region"].astype(str)
    fig = px.bar(region, x="Region", y="Predicted_Sales", color_discrete_sequence=["#3B82F6"])
    fig.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", xaxis=dict(type='category'), height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

with r1c2:
    st.subheader("👥 Customers by Region")
    cust = df.groupby("Region")["Customers"].sum().reset_index()
    cust["Region"] = cust["Region"].astype(str)
    fig2 = px.pie(cust, names="Region", values="Customers")
    fig2.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig2, use_container_width=True)

st.write("")

r2c1, r2c2 = st.columns(2)
with r2c1:
    st.subheader("📦 Inventory by Region")
    inv = df.groupby("Region")["Inventory"].sum().reset_index()
    inv["Region"] = inv["Region"].astype(str)
    fig3 = px.bar(inv, x="Region", y="Inventory", color_discrete_sequence=["#F59E0B"])
    fig3.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", xaxis=dict(type='category'), height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig3, use_container_width=True)

with r2c2:
    st.subheader("💼 Regional Sales Share")
    fig4 = px.pie(region, names="Region", values="Predicted_Sales")
    fig4.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.subheader("📈 Regional Sales Trend (Monthly)")
trend_region = df.groupby(["Month", "Region"])["Predicted_Sales"].sum().reset_index()
month_map = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
trend_region["Month_Name"] = trend_region["Month"].map(month_map)
fig_trend = px.line(trend_region, x="Month_Name", y="Predicted_Sales", color="Region", markers=True)
fig_trend.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", height=400, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")
st.subheader("📋 Regional Performance Summary")

summary = df.groupby("Region").agg(
    Sales_Forecast=("Predicted_Sales", "sum"),
    Inventory=("Inventory", "sum"),
    Customers=("Customers", "sum")
).reset_index()
st.dataframe(summary, use_container_width=True, hide_index=True)
