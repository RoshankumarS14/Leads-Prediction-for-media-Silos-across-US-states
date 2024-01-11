import geopandas as gpd    

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
    zoom_level = 15 - max(width, height)
    if zoom_level<=2.5:
        zoom_level=2.5

    return center_lat,center_lon,zoom_level
