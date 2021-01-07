import streamlit as st
from app import explore
from app import explorebyauthor
from app import tryit
from app import author_choropleth

# top-level config
st.set_page_config(
        page_title="fryetag",
        page_icon=":book:",
        layout="wide",
        initial_sidebar_state="auto"
)

Pages = {
    'Home': explore,
    'Explore by Author': explorebyauthor,
    "Sound Like The Author": tryit,
    "GPT2 text generator": author_choropleth
}

selection = st.sidebar.radio("", list(Pages.keys()))
page = Pages[selection]
page.app()
