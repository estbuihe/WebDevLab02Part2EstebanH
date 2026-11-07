# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page will display graphs based on your baseline weekly goals and the training session info that you give in the survey.")


# --- PART 1: BASELINE WEEKLY GOALS (JSON DATA) ---
st.divider()
st.header("Part 1: Baseline Weekly Goals ")

if os.path.exists("data.json"):
    with open("data.json", "r") as file:
        json_data = json.load(file)
    st.success("Baseline JSON data loaded successfully!")
else:
    st.error("Error! 'data.json' file was not found.")
    json_data = {"chart_title": "No data", "data_points": []}

if json_data["data_points"]:
    labels = [item["label"] for item in json_data["data_points"]]
    values = [item["value"] for item in json_data["data_points"]]
    json_df = pd.DataFrame({"Goal Category": labels, "Target Minutes": values}).set_index("Goal Category")

    # 1. Static Graph for JSON
    st.subheader("Static Graph, Baseline Weekly Targets")
    st.bar_chart(json_df)
    st.caption("This static chart shows the baseline of the weekly target minutes defined in the JSON file.")

    # 2. Dynamic Graph with Radio Toggle for JSON
    st.subheader("Dynamic Graph: Interactive View Switcher")
    
    if "json_chart_type" not in st.session_state:
        st.session_state.json_chart_type = "Bar Chart"

    # NEW - st.radio: allows the user to select the chart type view dynamically
    chart_choice = st.radio(
        "Select chart view type:", 
        ["Bar Chart", "Line Chart"], 
        index=0 if st.session_state.json_chart_type == "Bar Chart" else 1
    )
    st.session_state.json_chart_type = chart_choice

    if chart_choice == "Bar Chart":
        st.bar_chart(json_df)
    else:
        st.line_chart(json_df)

    st.caption(f"Displaying dynamic visualization for '{json_data['chart_title']}'. Use the radio buttons above in order to switch the view instantly!")
else:
    st.warning("No JSON data available for visualization.")


# --- PART 2: SESSION PROGRESSION (CSV DATA) ---
st.divider()
st.header("Part 2: Logged Session Progression (CSV)")

if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    csv_data = pd.read_csv('data.csv')
    st.success("✅ CSV session data loaded successfully!")
else:
    csv_data = pd.DataFrame(columns=["Training Category", "Minutes"])

# 1. Static Summary Graph from CSV
st.subheader("Static Graph, total Minutes by the three categories")
if not csv_data.empty:
    summary_df = csv_data.groupby("Training Category")["Minutes"].sum()
    st.bar_chart(summary_df)
    st.caption("This static chart shows the total minutes you've logged for each training category.")
else:
    st.warning("No CSV data logged yet. Use the Survey page to add sessions!")

# 2. Dynamic Progression Graph & Metrics from CSV
st.subheader("Dynamic Graph: Category Session Progression")
if not csv_data.empty:
    categories = csv_data["Training Category"].unique()
    
    if "selected_cat" not in st.session_state:
        st.session_state.selected_cat = categories[0]

    # NEW - st.selectbox: allows the user to filter progression history by category
    selected_category = st.selectbox(
        "Choose a category to view individual session history:",
        categories,
        index=list(categories).index(st.session_state.selected_cat) if st.session_state.selected_cat in categories else 0
    )
    st.session_state.selected_cat = selected_category

    filtered_df = csv_data[csv_data["Training Category"] == selected_category].reset_index(drop=True)
    filtered_df["Session Number"] = range(1, len(filtered_df) + 1)
    
    # NEW - st.line_chart: renders the progress trend over time dynamically
    line_chart_data = filtered_df.set_index("Session Number")["Minutes"]
    st.line_chart(line_chart_data)
    st.caption(f"Showing progression for {selected_category} across {len(filtered_df)} logged session(s).")

    # Extra Credit / Summary Statistics Components
    st.write("---")
    st.subheader("Summary Statistics")
    
    mean_val = round(filtered_df["Minutes"].mean(), 1) if not filtered_df.empty else 0
    median_val = round(filtered_df["Minutes"].median(), 1) if not filtered_df.empty else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f"Average ({selected_category})", value=f"{mean_val} mins")
    with col2:
        st.metric(label=f"Median ({selected_category})", value=f"{median_val} mins")
    
    st.caption("These summary statistics update dynamically as you switch between categories or log new sessions.")
else:
    st.info("Log training sessions on the survey page in order to see your progression graph and your personalized statistics!")
