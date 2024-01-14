import geopandas as gpd    
import math
import streamlit as st

# Dynamic zoom level adjustment
def calculate_zoom_level(width, height, num_states):
    base_zoom = 8  # starting point for zoom level
    area_factor = width * height  # area covered by the states
    distribution_factor = math.sqrt(num_states)  # accounts for the number of states

    # Adjust zoom based on the area and distribution of states
    adjusted_zoom = base_zoom - (area_factor / distribution_factor)
    st.write(max(0, min(adjusted_zoom, 12)))
    return max(3, min(adjusted_zoom, 12))  # Ensure zoom level is within reasonable bounds
    
def get_centre_zoom(json_data,states):
    # Convert the GeoJSON data to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features((json_data))

    # Calculate the centroid of each state
    gdf['centroid'] = gdf['geometry'].centroid

    # Extract the latitude and longitude
    gdf['longitude'] = gdf['centroid'].x
    gdf['latitude'] = gdf['centroid'].y

    bounds = gdf[gdf['NAME'].isin(states)].total_bounds  # minx, miny, maxx, maxy

    # Calculate the width and height of the bounding box
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]

    # Calculate the center of your selected states
    center_lat = gdf[gdf['NAME'].isin(states)]['latitude'].mean()
    center_lon = gdf[gdf['NAME'].isin(states)]['longitude'].mean()

    # Calculate the zoom level based on the maximum dimension
    zoom_level = 8 - max(width, height)
    if zoom_level<=3:
        zoom_level=3

    # return center_lat,center_lon,zoom_level
    return center_lat,center_lon,calculate_zoom_level(width, height, len(states))


