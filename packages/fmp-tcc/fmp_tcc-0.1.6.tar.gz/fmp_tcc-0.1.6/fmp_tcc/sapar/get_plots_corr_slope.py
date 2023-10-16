import plotly.express as px

from plotly.subplots import make_subplots
import plotly.graph_objects as go

def plot_coef_corr_countryGroup(data_frame, palette):
    
    slope = {}
    correlation = {}

    for region in set(data_frame['countryGroup']):
        slope[region] = go.Scatter(x=data_frame[data_frame['countryGroup'] == region]['date'], 
                              y=data_frame[data_frame['countryGroup'] == region]['slope'],
                              name='slope of ' + region, legendgroup='slope of ' + region,
                              line=dict(color=palette[region]))

    
        correlation[region] = go.Scatter(x=data_frame[data_frame['countryGroup']==region]['date'], 
                              y=data_frame[data_frame['countryGroup']==region]['correlation'], 
                              name='correlation of ' + region, 
                              legendgroup='correlation of ' + region,
                              line=dict(color=palette[region]), opacity=0.5)
        
    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3])

    for key in slope.keys():
        fig.append_trace(slope[key], row=1, col=1)
    for key in correlation.keys():    
        fig.append_trace(correlation[key], row=2, col=1)

    
    return fig

def plot_coef_corr_industry(data_frame, palette):

    slope = {}
    correlation = {}

    for industry in set(data_frame['industry']):
        slope[industry] = go.Scatter(x=data_frame[data_frame['industry']==industry]['date'], 
                              y=data_frame[data_frame['industry']==industry]['slope'],
                              name='slope of ' + industry, legendgroup='slope of ' + industry, 
                              line=dict(color=palette[industry]))

    
        correlation[industry] = go.Scatter(x=data_frame[data_frame['industry']==industry]['date'], 
                              y=data_frame[data_frame['industry']==industry]['correlation'], 
                              name='correlation of ' + industry, 
                              legendgroup='correlation of ' + industry, 
                              line=dict(color=palette[industry]), opacity=0.5)
        
    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3])

    for key in slope.keys():
        fig.append_trace(slope[key], row=1, col=1)
    for key in correlation.keys():    
        fig.append_trace(correlation[key], row=2, col=1)
    
    return fig

def camel_case_split(s):
    # use map to add an underscore before each uppercase letter
    modified_string = list(map(lambda x: ' ' + x if x.isupper() else x, s))
    modified_string[0] = modified_string[0].upper()
    split_string = ''.join(modified_string)

    return split_string