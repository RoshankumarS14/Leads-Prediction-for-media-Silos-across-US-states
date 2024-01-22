import plotly.graph_objects as go
import numpy as np
from plotly.io import to_image
from plotly.io._kaleido import to_image as to_image_kaleido
from openpyxl.drawing.image import Image as XLImage
from PIL import Image 
import io

def plot_gauge_Balance(value):
            
    current_price = value
    ask_price = 100
    bid_price = 50
    spread = 5

    trace = go.Indicator(
        mode="gauge+number+delta",
        title={'text': "Balance"},
        # delta={'reference': ask_price, 'relative': False, 'increasing': {'color': "RebeccaPurple"}},
        value=current_price,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'shape': 'angular',
            'axis': {'range': [bid_price - spread, ask_price + spread]},
            'bar': {'color': "black", 'thickness': 0.2},
            'bgcolor': 'black',
            'borderwidth': 2,
            'bordercolor': 'black',
            'steps': [
                {'range': [90, 100], 'color': 'green'},
                {'range': [85, 90], 'color': '#30F54B'},
                {'range': [80, 85], 'color': 'yellow'},
                {'range': [75, 80], 'color': 'orange'},
                {'range': [75, 50], 'color': 'red'}
            ],
            'threshold': {
                'line': {'color': 'blue', 'width': 6},
                'thickness': 0.75,
                'value': current_price,
            }
        }
    )
    return trace

def plot_gauge_APScale(value,title="AP Scale"):

    current_price = value
    ask_price = 100
    bid_price = 0
    spread = 10
            
    trace = go.Indicator(
        mode="gauge+number+delta",
        title={'text': title},
        value=current_price,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'shape': 'angular',
            'axis': {'range': [bid_price - spread, ask_price + spread]},
            'bar': {'color': "black", 'thickness': 0.2},
            'bgcolor': 'black',
            'borderwidth': 2,
            'bordercolor': 'black',
            'steps': [
                {'range': [80, 100], 'color': 'green'},
                {'range': [50, 80], 'color': '#30F54B'},
                {'range': [40, 50], 'color': 'yellow'},
                {'range': [30, 40], 'color': 'orange'},
                {'range': [0, 30], 'color': 'red'}
            ],
            'threshold': {
                'line': {'color': 'blue', 'width': 6},
                'thickness': 0.75,
                'value': current_price,
                        }
                    }
                )
    return trace

def calculate_rating(numbers):
    # Calculate the standard deviation
    std_dev = np.std(numbers)
    
    # Calculate the mean of the numbers
    mean = np.mean(numbers)
    
    # Normalize the standard deviation to a scale of 0 to 1
    normalized_std_dev = std_dev / mean if mean != 0 else 0
    
    # Calculate the rating
    rating = 100 * (1 - normalized_std_dev)
    
    # Make sure the rating is within the scale of 1 to 100
    rating = max(min(rating, 100), 1)
    
    return rating

def get_image(fig,new_width,new_height,crop=None):
    fig_bytes = to_image_kaleido(fig, format="png", scale=100)
    # fig_bytes = to_image(fig, format="png")
    img = Image.open(io.BytesIO(fig_bytes))
            
    if crop!=None:
        crop_area = crop
        img = img.crop(crop_area)
                
    # Resize the image
    width, height = img.size
    img = img.resize((new_width, new_height))

    # Save the resized image to a BytesIO object
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # Create an Image object from BytesIO object
    img = XLImage(io.BytesIO(img_byte_arr))
    return img
        
           
