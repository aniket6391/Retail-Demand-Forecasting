import streamlit as st
import base64

@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def add_logo():
    try:
        # Use native st.logo to keep it at the TOP
        st.logo("assets/logo.png")
        
        # Inject CSS to force the native logo to be larger
        st.markdown(
            """
            <style>
            /* Target the Streamlit logo container */
            [data-testid="stLogo"] {
                height: 8rem !important;
            }
            [data-testid="stLogo"] img {
                max-height: 8rem !important;
                height: 8rem !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
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
