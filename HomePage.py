# This creates the main landing page for the Streamlit application.
# Contains an introduction to the project and guide users to other pages.

# Import Streamlit
import streamlit as st

# st.set_page_config() is used to configure the page's appearance in the browser tab.
# It's good practice to set this as the first Streamlit command in your script.
st.set_page_config(
    page_title="Soccer Conditioning Homepage",  # The title that appears in the browser tab
    page_icon="⚽",  # An emoji that appears as the icon in the browser tab
)

# WELCOME PAGE TITLE
st.title("Soccer Training & Weekly Conditioning Tracker ⚽‍️")

# INTRODUCTORY TEXT
st.write("""
This application is designed to track and visualize soccer training workload! Along a weekly conditioning goals.
You can navigate to the different pages using the sidebar on the left.

### How to use this app:
- **Visuals Page**: Go here and visit to see your baseline weekly targets visualized in a static and dynamic graph display.
- **Survey Page**: Go here to input your personalized training session data.

This project is part of CS 1301 Lab 2.
""")

# OPTIONAL: ADD AN IMAGE
# 1. Navigate to the 'images' folder in your project directory.
# 2. Place your image file (e.g., 'welcome_image.png') inside that folder.
# 3. Uncomment the line below and change the filename to match yours.
#
# st.image("images/welcome_image.png")
