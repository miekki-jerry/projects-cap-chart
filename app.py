import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path
import plotly.graph_objects as go  # Import Plotly Graph Objects for more control over the chart

# Initialize the data directory and file
DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_FILE = DATA_DIR / "projects.json"

# Ensure the data directory exists
if not DATA_DIR.exists():
    os.makedirs(DATA_DIR)

# Load or initialize projects data
if DATA_FILE.is_file():
    with open(DATA_FILE, "r") as file:
        projects = json.load(file)
else:
    projects = {}

# Define custom color scheme for categories
category_colors = {
    'Paid work': '#1f8b4c',  # Example color
    'Guitar': '#be32d0',
    'MemeMatch': '#ebcb38',
    'AI Projects': '#3498db',
    'Relationship': '#95a5a6',
    'Sport': '#2ecc71',
    'Self development': '#f39c12',
    'Personal brand': '#e74c3c',
    '👀 new job':'#54ca12'
}

# UI Components
st.title('Project Capacity Manager')

# Placeholder for the chart
chart_placeholder = st.empty()

# Function to create and display the customized chart
def display_chart(projects_data):
    if projects_data:
        # Convert the projects data into a DataFrame
        chart_data = pd.DataFrame([
            {
                'Project': project,
                'Capacity': details['capacity'],
                'Category': details['category']
            }
            for project, details in projects_data.items()
        ])

        # Sort the DataFrame by 'Capacity' in descending order
        chart_data = chart_data.sort_values(by='Capacity', ascending=False)

        # Create a blank figure with the desired background color
        fig = go.Figure(layout={
            'paper_bgcolor': 'rgba(0,0,0,0)', 
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'xaxis': {'showgrid': False},
            'yaxis': {'showgrid': False}
        })

        # Add each bar as a separate trace
        for category, color in category_colors.items():
            category_data = chart_data[chart_data['Category'] == category]
            fig.add_trace(go.Bar(
                x=category_data['Capacity'],
                y=category_data['Project'],
                name=category,  # This will be the legend title
                marker=dict(color=color),
                orientation='h'
            ))

        # Update the layout to match the style of the image
        fig.update_layout(
            xaxis_title='Capacity',
            yaxis_title=None,
            barmode='stack',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        chart_placeholder.plotly_chart(fig, use_container_width=True)

# Display the chart initially if there are projects
display_chart(projects)

# Project form for input
with st.form("project_form", clear_on_submit=True):
    project_name = st.text_input("Project Name")
    project_capacity = st.number_input("Percentage of Capacity", min_value=0, max_value=100, step=1)
    project_category = st.selectbox("Project Category", options=list(category_colors.keys()))

    submitted = st.form_submit_button("Add Project")
    if submitted:
        # Update projects data with a dictionary for each project
        projects[project_name] = {
            'capacity': project_capacity,
            'category': project_category
        }
        # Save the updated projects to the file
        with open(DATA_FILE, "w") as file:
            json.dump(projects, file)
        st.success(f"Project '{project_name}' added with {project_capacity}% capacity.")
        # Clear the old chart and display the updated chart
        chart_placeholder.empty()
        display_chart(projects)

# Button to clear all projects
if st.button('Clear All Projects'):
    projects = {}  # Reset the projects dictionary
    with open(DATA_FILE, "w") as file:
        json.dump(projects, file)  # Save the empty projects to the file
    chart_placeholder.empty()  # Clear the chart
    st.success("All projects have been cleared.")
