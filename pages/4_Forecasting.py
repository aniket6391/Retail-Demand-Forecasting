import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(page_title="AI Demand Forecasting", page_icon="🤖", layout="wide")

from assets.ui import add_logo, kpi_card
add_logo()

@st.cache_data
def load_data():
    return pd.read_csv("dataset/dashboard_data.csv")

df = load_data()

model = joblib.load("models/model.pkl")
encoders = joblib.load("models/encoders.pkl")

st.markdown('''
# 🤖 AI Demand Forecasting
### Predict Future Retail Demand Using Machine Learning
''')
st.divider()

st.subheader("📝 Enter Product Details")
st.write("")

region_map = {1: "North India", 2: "South India", 3: "West India"}
category_map = {0: "Electronics", 1: "Apparel", 2: "Home & Kitchen", 3: "Sports", 5: "Health & Beauty", 6: "Toys & Games"}
month_map = {0: "January", 1: "February", 2: "March", 3: "April", 4: "May", 5: "June", 6: "July", 7: "August", 8: "September", 9: "October", 10: "November", 11: "December"}

col1, col2 = st.columns(2)

with col1:
    region = st.selectbox("Region", sorted(df["Region"].unique()), format_func=lambda x: region_map.get(x, f"Region {x}"))
    category = st.selectbox("Category", sorted(df["Category"].unique()), format_func=lambda x: category_map.get(x, f"Category {x}"))
    inventory = st.slider("Inventory Levels", min_value=0, max_value=1500, value=100, step=10)

with col2:
    price = st.number_input("Product Price (₹)", min_value=1.0, value=100.0, step=5.0)
    customers = st.slider("Expected Customers", min_value=1, max_value=1000, value=50, step=5)
    month = st.selectbox("Forecast Month", sorted(df["Month_Name"].unique()), format_func=lambda x: month_map.get(x, f"Month {x}"))

st.write("")
predict = st.button("🚀 Predict Sales", use_container_width=True, type="primary")

if predict:
    st.divider()
    region_encoded = encoders["Region"].transform([region])[0]
    category_encoded = encoders["Category"].transform([category])[0]
    month_encoded = encoders["Month_Name"].transform([month])[0]

    input_df = pd.DataFrame({
        "Region": [region_encoded],
        "Category": [category_encoded],
        "Price": [price],
        "Inventory": [inventory],
        "Customers": [customers],
        "Month_Name": [month_encoded]
    })

    prediction = model.predict(input_df)[0]

    if prediction >= 700:
        level = "High Demand"
        color = "#22C55E"
        recommendation = "Increase inventory to avoid stock-outs."
    elif prediction >= 400:
        level = "Medium Demand"
        color = "#F59E0B"
        recommendation = "Maintain current inventory."
    else:
        level = "Low Demand"
        color = "#EF4444"
        recommendation = "Reduce inventory and monitor demand."

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Predicted Sales", f"{prediction:.2f}", "#3B82F6", "📈")
    with c2:
        kpi_card("Demand Level", level, color, "📊")
    with c3:
        kpi_card("Recommendation", "✔ Ready", "#8B5CF6", "💡")

    st.write("")
    st.info(f"💡 {recommendation}")
    st.divider()

    st.subheader("📉 Historical Average vs Forecast")
    history = df.groupby("Month_Name")["Predicted_Sales"].mean().reset_index()
    future = pd.DataFrame({"Month_Name": ["Forecast"], "Predicted_Sales": [prediction]})
    chart = pd.concat([history, future])
    
    fig = px.line(chart, x="Month_Name", y="Predicted_Sales", markers=True, color_discrete_sequence=["#3B82F6"])
    fig.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", font=dict(color="white"), height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📌 Prediction Summary")
    st.success(f'''
Region : {region_map.get(region, region)} | Category : {category_map.get(category, category)} | Forecast Month : {month_map.get(month, month)} | Predicted Sales : ₹ {prediction:.2f} | Demand Level : {level}
''')

st.divider()
st.subheader("📋 Sample Forecast Dataset")
preview = df[["Region", "Category", "Price", "Inventory", "Customers", "Predicted_Sales"]].head(20)
st.dataframe(preview, use_container_width=True, hide_index=True)

st.write("")
st.caption("© Retail Demand Forecasting Dashboard | AI Forecast Module")
