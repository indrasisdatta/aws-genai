import streamlit as st 
import importlib

st.set_page_config(page_title="Gen AI Apps", page_icon="🚀")

app_choice = st.sidebar.radio("Go to:", ['Home', 'ATS Tracking', 'Multi PDF Chat'])

if app_choice == 'Home':
    st.title("Home")
    st.write("Select an app from the sidebar.")
elif app_choice == 'ATS Tracking':
    ats_app = importlib.import_module("pages.ats.app")
    ats_app.main()
elif app_choice == 'Multi PDF Chat':
    pdf_app = importlib.import_module("pages.multi_pdf_chat.app")
    pdf_app.main()

