import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="About Project", page_icon="ℹ️", layout="wide")

from assets.ui import add_logo
add_logo()

@st.cache_data
def load_data():
    return pd.read_csv("dataset/dashboard_data.csv")

df = load_data()

# HEADER
st.markdown("""
<div style="text-align: center; padding: 10px 0px 20px 0px;">
    <h1 style="color: #3B82F6; font-size: 3em; margin-bottom: 0;">Retail Demand Forecasting</h1>
    <h3 style="color: #94A3B8; font-weight: 300;">Interactive Documentation & Data Profiler</h3>
</div>
""", unsafe_allow_html=True)

st.write("Welcome to the interactive documentation. Explore the project architecture, deep-dive into the dataset, and understand the machine learning pipeline below.")
st.write("")

# SECTION 1: PROJECT ARCHITECTURE (Interactive Expanders)
st.subheader("🏗️ Project Architecture & Stack")

with st.expander("📖 1. Project Overview & Objectives", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Overview:**")
        st.write("An advanced Machine Learning platform designed to predict future product demand using historical retail data. It empowers retailers to analyze patterns, optimize inventory, and forecast sales.")
    with col2:
        st.markdown("**Objectives:**")
        st.write("- ✔ Predict Future Demand accurately")
        st.write("- ✔ Improve Inventory Planning")
        st.write("- ✔ Prevent Stock-outs")
        st.write("- ✔ Analyze Regional & Product Performance")

with st.expander("💻 2. Technology Stack"):
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("🐍 **Python** (Core Language)")
        st.markdown("👑 **Streamlit** (UI Framework)")
    with t2:
        st.markdown("🐼 **Pandas** (Data Processing)")
        st.markdown("📊 **Plotly** (Visualizations)")
    with t3:
        st.markdown("🤖 **Scikit-Learn** (Machine Learning)")
        st.markdown("💾 **Joblib** (Model Deployment)")

with st.expander("🤖 3. Machine Learning Details"):
    st.info("""
    **Algorithm:** Random Forest Regressor  
    **Type:** Supervised Machine Learning  
    **Target Variable:** `Predicted_Sales`  

    **Features Used:** `Region`, `Category`, `Price`, `Inventory`, `Customers`, `Month_Name`
    """)

st.write("")
st.divider()

# SECTION 2: INTERACTIVE DATA PROFILER
st.subheader("🔍 Interactive Dataset Profiler")
st.write("Explore the underlying dataset dynamically. Select a variable below to generate an instant data distribution chart.")

# Interactive Selection
selected_col = st.selectbox("Select a Feature to Analyze:", ["Category", "Region", "Month_Name", "Price", "Inventory", "Customers", "Predicted_Sales"])

# Dynamic Chart Generation
if selected_col in ["Category", "Region", "Month_Name"]:
    # Categorical
    counts = df[selected_col].value_counts().reset_index()
    counts.columns = [selected_col, "Count"]
    fig = px.bar(counts, x=selected_col, y="Count", color=selected_col, title=f"Distribution of {selected_col}")
else:
    # Numerical
    fig = px.histogram(df, x=selected_col, nbins=30, title=f"Distribution of {selected_col}", color_discrete_sequence=["#3B82F6"])

fig.update_layout(template="plotly_dark", paper_bgcolor="#0F172A", plot_bgcolor="#1E293B", height=350, margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig, use_container_width=True)

# SECTION 3: DEEP DATASET INSIGHTS
st.subheader("📊 Extended Dataset Insights")

with st.expander("Live Summary Statistics (Numerical)", expanded=False):
    st.dataframe(df[["Price", "Inventory", "Customers", "Predicted_Sales"]].describe(), use_container_width=True)

with st.expander("Data Dictionary & Types", expanded=False):
    dtypes = pd.DataFrame(df.dtypes, columns=["Data Type"]).reset_index()
    dtypes.columns = ["Column Name", "Data Type"]
    descriptions = {
        "Store_ID": "Store identifier", "Product_ID": "Product identifier", 
        "Category": "Product categorization", "Region": "Geographical region", 
        "Inventory": "Current stock", "Price": "Price in INR", 
        "Customers": "Footfall/Customers", "Month": "Month Number", 
        "Month_Name": "Month Name", "Predicted_Sales": "Target Sales Volume"
    }
    dtypes["Description"] = dtypes["Column Name"].map(descriptions)
    st.dataframe(dtypes, use_container_width=True, hide_index=True)

st.write("")
st.divider()

# SECTION 4: ROADMAP
st.subheader("🚀 Project Roadmap")
# A visual interactive timeline using columns and metrics
r1, r2, r3, r4 = st.columns(4)
r1.metric("Phase 1", "Dashboard UI", "✅ Completed")
r2.metric("Phase 2", "ML Integration", "✅ Completed")
r3.metric("Phase 3", "Real-time API", "⏳ Upcoming")
r4.metric("Phase 4", "Cloud Deploy", "⏳ Future")

st.write("")
st.caption("© Retail Demand Forecasting | MCA Final Year Project")
