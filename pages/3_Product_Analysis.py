import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Product Analysis", layout="wide")

from assets.ui import add_logo, kpi_card
add_logo()

@st.cache_data
def load_data():
    return pd.read_csv("dataset/dashboard_data.csv")

df = load_data()

st.markdown('''
# 📦 Product Analysis
### Product performance and metrics.
''')

st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Total Products", df["Product_ID"].nunique(), "#3B82F6", "📦")
with c2:
    kpi_card("Forecast Sales", f"₹ {df['Predicted_Sales'].sum():,.0f}", "#10B981", "💰")
with c3:
    kpi_card("Total Inventory", f"{df['Inventory'].sum():,}", "#F59E0B", "🏭")
with c4:
    kpi_card("Average Price", f"₹ {df['Price'].mean():.2f}", "#EF4444", "📈")

st.markdown("---")

r1c1, r1c2 = st.columns(2)

with r1c1:
    st.subheader("🥇 Top 10 Products by Sales")
    top_prod = df.groupby("Product_ID")["Predicted_Sales"].sum().sort_values().tail(10).reset_index()
    top_prod["Product_ID"] = top_prod["Product_ID"].astype(str)
    fig = px.bar(top_prod, x="Predicted_Sales", y="Product_ID", orientation="h", color_discrete_sequence=["#3B82F6"])
    fig.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", yaxis=dict(type='category'), height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

with r1c2:
    st.subheader("🥧 Category Sales Share")
    cat = df.groupby("Category")["Predicted_Sales"].sum().reset_index()
    fig2 = px.pie(cat, names="Category", values="Predicted_Sales", hole=0.4)
    fig2.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig2, use_container_width=True)

st.write("")

r2c1, r2c2 = st.columns(2)
with r2c1:
    st.subheader("🎯 Inventory vs Forecast Sales")
    fig3 = px.scatter(df, x="Inventory", y="Predicted_Sales", color="Category")
    fig3.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig3, use_container_width=True)

with r2c2:
    st.subheader("📊 Demand Distribution")
    demand = df.copy()
    demand["Demand Level"] = pd.cut(demand["Predicted_Sales"], bins=3, labels=["Low Demand", "Medium Demand", "High Demand"])
    dist = demand["Demand Level"].value_counts().reset_index()
    dist.columns = ["Demand Level", "Count"]
    fig4 = px.pie(dist, names="Demand Level", values="Count")
    fig4.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.subheader("📦 Sales Distribution by Category (Box Plot)")
fig_box = px.box(df, x="Category", y="Predicted_Sales", color="Category")
fig_box.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", height=400, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")
st.subheader("📋 Product Summary (Top 20)")
table = df[["Product_ID", "Category", "Price", "Inventory", "Predicted_Sales"]].sort_values("Predicted_Sales", ascending=False).head(20)
st.dataframe(table, use_container_width=True, hide_index=True)
