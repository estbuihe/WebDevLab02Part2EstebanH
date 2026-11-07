# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Soccer Training Tracker",
    page_icon="⚽",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("⚽ Soccer Training Tracker")
st.write("Log your soccer training sessions to track your progress over time!")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("training_form"):
    # Dropdown selectbox with categories matching your visualizations exactly
    training_category = st.selectbox(
        "Select the type of training:",
        ["Technical Drills", "Stamina & Cardio", "Strength & Weight Lifting"]
    )
    
    # Number input specifying minutes practiced
    minutes = st.number_input(
        "Enter minutes practiced:", 
        min_value=0, 
        step=5
    )

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Session")

    # This will only run once the submit button is clicked.
    if submitted:
        # --- YOUR LOGIC GOES HERE ---
        # TO DO:
        # 1. Create a new row of data from inputs matching Visuals.py columns ("Training Category" and "Minutes").
        new_data = pd.DataFrame({
            "Training Category": [training_category],
            "Minutes": [minutes]
        })
        
        # 2. Append this new row to the 'data.csv' file.
        #    - Make sure to open the file in 'append' mode ('a').
        if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
            new_data.to_csv('data.csv', mode='a', header=False, index=False)
        else:
            new_data.to_csv('data.csv', index=False)
   
        st.success("✅ Your training session has been recorded!")
        st.write(f"**Category:** {training_category}, **Minutes:** {minutes}")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("📄 Current Training Data")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")

# CLEAR DATA OPTION
st.divider()
st.subheader("⚠️ Reset Data")
st.write("Made a mistake? You can clear all training data and start fresh.")

col1, col2 = st.columns([1, 2])

with col1:
    if st.button("🗑️ Clear All Training Sessions", type="secondary"):
        if os.path.exists('data.csv'):
            pd.DataFrame(columns=["Training Category", "Minutes"]).to_csv('data.csv', index=False)
            st.success("✅ All data cleared! You can start logging fresh sessions.")
            st.rerun()
        else:
            st.info("No data to clear.")

with col2:
    st.caption("⚠️ **Warning:** This will permanently delete all your logged training sessions. This action cannot be undone.")
