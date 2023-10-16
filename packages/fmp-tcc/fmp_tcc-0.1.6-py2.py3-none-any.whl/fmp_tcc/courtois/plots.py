import pandas as pd

import plotly.graph_objects as go

def format_string(input_string):
    formatted_string = ''
    for char in input_string:
        if char.isupper():
            formatted_string += ' '
        formatted_string += char
    formatted_string = formatted_string.replace('_', ' ')
    formatted_string = formatted_string.strip()
    formatted_string = formatted_string.title()
    return formatted_string

def line_graph(field, data):
    x_values = data['date']
    y_values = data[field]
    
    trace = go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines',
    name='Line Graph'
    )
    
    layout = go.Layout(
    title='Line Graph Example',
    xaxis=dict(title='date'),
    yaxis=dict(title=format_string(field))
    )
    
    return go.Figure(data=[trace], layout=layout)

