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

def get_state_name(lat, lon):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    address = location.raw['address']
    state = address.get('state', '')
    return state

def create_circle_feature(center, radius_miles, num_points=64, properties=None):
    """
    Create a GeoJSON feature representing a circle with a given center, radius, and number of points.
    :param center: Tuple of (longitude, latitude)
    :param radius: Radius in degrees (small values)
    :param num_points: Number of points to generate the circle
    :param properties: Dictionary of properties for the feature
    :return: GeoJSON feature dictionary
    """
    if properties is None:
        properties = {}

    # Earth's radius in miles
    earth_radius_miles = 3960.0

    # Calculate the radius in degrees latitude
    radius_lat = radius_miles / earth_radius_miles * (180 / math.pi)

    # Calculate the radius in degrees longitude, adjusting for the latitude
    radius_lng = radius_miles / (earth_radius_miles * math.cos(math.radians(center[1]))) * (180 / math.pi)

    # Apply the scale factor to the radius
    radius_lat *= 0.6
    radius_lng *= 0.6

    # Calculate the points of the circle
    circle_points = []
    for i in range(num_points):
        angle = math.radians(float(i) / num_points * 360)
        dx = radius_lng * math.cos(angle)
        dy = radius_lat * math.sin(angle)
        point = (center[0] + dx, center[1] + dy)
        circle_points.append(point)
    circle_points.append(circle_points[0])  # Ensure the polygon is closed

    # Create the GeoJSON feature
    feature = {
        "type": "Feature",
        "properties": properties,
        "geometry": {
            "type": "Polygon",
            "coordinates": [circle_points]
        }
    }
    return feature


