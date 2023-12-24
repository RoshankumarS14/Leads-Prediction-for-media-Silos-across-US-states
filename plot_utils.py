import plotly.graph_objects as go

def plot_gauge_Balance(value):
            
    current_price = value
    ask_price = 100
    bid_price = 50
    spread = 5

    trace = go.Indicator(
        mode="gauge+number+delta",
        title={'text': "Balance"},
        delta={'reference': ask_price, 'relative': False, 'increasing': {'color': "RebeccaPurple"}},
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

def plot_gauge_APScale(value):

    current_price = value
    ask_price = 100
    bid_price = 0
    spread = 10
            
    trace = go.Indicator(
        mode="gauge+number+delta",
        title={'text': "AP Scale"},
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
        
           
