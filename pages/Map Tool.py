import os
import streamlit.components.v1 as components
import geopy.distance
import pandas as pd
import streamlit as st
from geopy.geocoders import Nominatim

_RELEASE = False

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/build")
_component_func = components.declare_component("my_component", path=build_dir)

if "selected_states" not in st.session_state:
    st.session_state["selected_states"]=[]


def my_component(key=None):
    component_value = _component_func(key=key, default=0)
    return component_value

def get_state_name(lat, lon):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    address = location.raw['address']
    state = address.get('state', '')
    return state


if not _RELEASE:
    st.subheader("Population Map - US")
    clicked_coords = my_component()
    # st.markdown(clicked_coords)
    if not (type(clicked_coords)==list):
        # st.write(clicked_coords.get("lat"), clicked_coords.get("lng"))
        try:
            selected_state = get_state_name(clicked_coords.get("lat"), clicked_coords.get("lng")) 
            if selected_state not in st.session_state["selected_states"]:
                st.session_state["selected_states"].append(selected_state)
        except:
            pass    

# Read the csv file into a pandas dataframe
data = pd.read_csv("US_Population.csv")

# US state names and abbreviations
us_state_abbreviations = {
    'Alabama': 'AL','Alaska': 'AK','Arizona': 'AZ','Arkansas': 'AR','California': 'CA','Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE',
    'Florida': 'FL','Georgia': 'GA','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY',
    'Louisiana': 'LA','Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO',
    'Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY',
    'North Carolina': 'NC','North Dakota': 'ND','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA','Rhode Island': 'RI',
    'South Carolina': 'SC','South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT','Vermont': 'VT','Virginia': 'VA',
    'Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'
}

# Define a function to calculate the distance between two points
def distance(point1, point2):
    return geopy.distance.distance(point1, point2).km

states = st.multiselect("Selected States:",st.session_state["selected_states"],st.session_state["selected_states"])

calculate = st.button("Get Population")

if calculate:
    st.balloons()
    # Get the center and radius from the typescript component

    dfs = []
    if type(clicked_coords)==list:
        for coords in clicked_coords:
            center = coords.get("center")
            radius = coords.get("radius")/1000

            # Filter the dataframe to keep only the cities that are within the radius
            df_filtered = data[data.apply(lambda row: distance((center["lat"],center["lng"]), (row["lat"], row["lon"])) <= radius, axis=1)]
            dfs.append(df_filtered)
    states = [us_state_abbreviations[state] for state in states]
    if len(states)>=1:
        dfs.append(data[data["state"].isin(states)])

    df = pd.concat(dfs,ignore_index=True)
    df.drop_duplicates(inplace=True)
    # Calculate the total population of the filtered cities
    total_population = df["population"].sum()

    # Display the result
    # st.write(f"The total population of the cities within {radius} km of {center} is {total_population}.")
    st.write(f"The total population of the cities within the circle is {total_population}.")
    
    state_wise_pop = pd.DataFrame(df["state"].value_counts()/len(df)*100)
    state_wise_pop = state_wise_pop.rename(columns={"state":"Percentage Population"})
    state_wise_pop["Percentage Population"] = state_wise_pop["Percentage Population"].apply(lambda a : round(a,2))
    st.write(state_wise_pop)
