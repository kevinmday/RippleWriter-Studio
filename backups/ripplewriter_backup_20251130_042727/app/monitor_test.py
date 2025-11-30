import streamlit as st

# Correct import relative to monitor_test.py location
from refactor_regions.monitor_region import render_monitor_region

st.set_page_config(layout="wide")

render_monitor_region()
