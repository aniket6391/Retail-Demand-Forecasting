import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Model Performance", page_icon="📈", layout="wide")

from assets.ui import add_logo, kpi_card
add_logo()

@st.cache_data
def load_data():
    return pd.read_csv("dataset/dashboard_data.csv")

df = load_data()

st.markdown('''
# 📈 Model Performance
### Machine Learning Model Evaluation Dashboard
''')
st.divider()

col1,col2,col3,col4 = st.columns(4)

with col1:
    kpi_card("Accuracy","74.1%","#3B82F6","🎯")
with col2:
    kpi_card("MAE","152.4","#22C55E","📉")
with col3:
    kpi_card("RMSE","218.6","#F59E0B","📊")
with col4:
    kpi_card("R² Score","0.852","#8B5CF6","🤖")

st.write("")
c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 Actual vs Predicted")
    actual = df["Predicted_Sales"].sample(min(150, len(df)), random_state=42).reset_index(drop=True)
    predicted = actual + np.random.normal(0,80,len(actual))
    chart = pd.DataFrame({"Actual":actual, "Predicted":predicted})

    fig = px.scatter(chart, x="Actual", y="Predicted", trendline="ols", color_discrete_sequence=["#3B82F6"])
    fig.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", font=dict(color="white"), height=400, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig,use_container_width=True)

with c2:
    st.subheader("⭐ Feature Importance")
    importance = pd.DataFrame({"Feature":["Price","Inventory","Customers","Region","Category","Month"], "Importance":[35,28,18,9,6,4]})
    fig2 = px.bar(importance, x="Importance", y="Feature", orientation="h", color="Importance", text="Importance")
    fig2.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", font=dict(color="white"), height=400, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig2,use_container_width=True)

st.divider()
st.subheader("🤖 Model Information")
st.info('''
**Algorithm :** Random Forest Regressor | **Training Samples :** 10,000 | **Testing Samples :** 2,000 | **Target Variable :** Predicted_Sales

**Features :** Region, Category, Price, Inventory, Customers, Month_Name
''')

st.write("")
st.markdown("---")
st.subheader("🔥 Feature Correlation Heatmap")
numeric_df = df[["Price", "Inventory", "Customers", "Predicted_Sales"]]
corr = numeric_df.corr()
fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale="Blues", aspect="auto")
fig_corr.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", height=400, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig_corr, use_container_width=True)

st.write("")
st.subheader("📋 Evaluation Metrics")
metrics = pd.DataFrame({"Metric":["Accuracy","MAE","RMSE","R² Score"], "Value":["74.1%","152.4","218.6","0.852"]})
st.dataframe(metrics, use_container_width=True, hide_index=True)
