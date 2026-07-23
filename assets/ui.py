import streamlit as st
import base64

@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def add_logo():
    # Adding logo directly to sidebar as an image to make it larger
    try:
        col1, col2, col3 = st.sidebar.columns([1, 8, 1])
        with col2:
            st.image("assets/logo.png", use_column_width=True)
        st.sidebar.markdown("<br>", unsafe_allow_html=True)
    except Exception:
        pass

def kpi_card(title, value, color, icon):
    st.markdown(f'''
<div style="
    background:#1E293B;
    padding:15px;
    border-radius:10px;
    border-left:5px solid {color};
    height:110px;
    display: flex;
    flex-direction: column;
    justify-content: center;
">
    <p style="color:#94A3B8; font-size:14px; margin-bottom:5px; margin-top:0;">{icon} {title}</p>
    <h3 style="color:white; margin:0px; font-weight:600;">{value}</h3>
</div>
''', unsafe_allow_html=True)
