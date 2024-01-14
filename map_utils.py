import geopandas as gpd    
import math
import streamlit as st

# Dynamic zoom level adjustment
def calculate_zoom_level(width, height, states, gdf):
    zoom_levels = []

    for state in states:
        bounds = gdf[gdf['NAME'] == state].total_bounds  # minx, miny, maxx, maxy
    
        # Calculate the width and height of the bounding box
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
    
        # Calculate the zoom level based on the maximum dimension
        zoom_level = 8 - max(width, height)
        zoom_levels.append(zoom_level)

    # Calculate the zoom level for the overall bounding box
    bounds = gdf[gdf['NAME'].isin(states)].total_bounds  # minx, miny, maxx, maxy
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    overall_zoom_level = 8 - max(width, height)
    
    # Calculate the final zoom level as a weighted average of the individual and overall zoom levels
    zoom_level = 0.7 * max(zoom_levels) + 0.3 * overall_zoom_level
    return zoom_level
    
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

    zoom_level = calculate_zoom_level(width, height, states,gdf)

    if zoom_level<=3:
        zoom_level=3
    return center_lat,center_lon,zoom_level


