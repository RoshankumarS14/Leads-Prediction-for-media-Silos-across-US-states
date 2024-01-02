import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(
    page_title="US Population Map",
    page_icon="🗺️",
    initial_sidebar_state="collapsed"
)

st.title("🗺️ US Population Map")
# Path to your HTML file with the Leaflet map
html_file_path = 'Map.html'

# Path to your CSV file
csv_file_path = 'US_Population.csv'

# Read the contents of the CSV file and encode it to base64
with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    csv_content = csv_file.read()
    csv_base64 = base64.b64encode(csv_content.encode()).decode()

# Embed the base64 encoded CSV content into the HTML
with open(html_file_path, 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()
    html_content = html_content.replace('fetch(\'US_cities_population.csv\')',
                                        f'fetch(\'data:text/csv;base64,{csv_base64}\')')

# Use Streamlit's components API to render the HTML, CSS, and JavaScript
components.html(html_content, height=600)
