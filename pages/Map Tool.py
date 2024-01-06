import os
import streamlit.components.v1 as components
import geopy.distance
import pandas as pd
import streamlit as st

_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "my_component",
        url="https://a60b-2405-201-e060-2007-9531-e2a4-d93a-3dab.ngrok-free.app/",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("my_component", path=build_dir)


def my_component(key=None):
    component_value = _component_func(key=key, default=0)
    return component_value


if not _RELEASE:
    import streamlit as st
    st.subheader("Population Map - US")
    clicked_coords = my_component()
    # st.markdown(clicked_coords)

# Read the csv file into a pandas dataframe
data = pd.read_csv("US_Population.csv")

calculate = st.button("Get Population")

# Define a function to calculate the distance between two points
def distance(point1, point2):
    return geopy.distance.distance(point1, point2).km

if calculate:
    st.balloons()
    # Get the center and radius from the typescript component

    dfs = []
    for coords in clicked_coords:
        center = coords.get("center")
        radius = coords.get("radius")/1000

        # Filter the dataframe to keep only the cities that are within the radius
        df_filtered = data[data.apply(lambda row: distance((center["lat"],center["lng"]), (row["lat"], row["lon"])) <= radius, axis=1)]
        dfs.append(df_filtered)

    df = pd.concat(dfs,ignore_index=True)
    # Calculate the total population of the filtered cities
    total_population = df["population"].sum()

    # Display the result
    # st.write(f"The total population of the cities within {radius} km of {center} is {total_population}.")
    st.write(f"The total population of the cities within the circle is {total_population}.")
    
    state_wise_pop = pd.DataFrame(df["state"].value_counts()/len(df)*100)
    state_wise_pop = state_wise_pop.rename(columns={"count":"Percentage Population"})
    state_wise_pop["Percentage Population"] = state_wise_pop["Percentage Population"].apply(lambda a : round(a,2))
    st.write(state_wise_pop)

