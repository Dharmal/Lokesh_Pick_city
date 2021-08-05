import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# from code import *

import os
import json
from pandas.io.json import json_normalize
import requests
import pandas as pd


def _pick_city(alpha):
    # url = 'https://samples.openweathermap.org/data/2.5/box/city?bbox=12,32,15,37,10&appid=b6907d289e10d714a6e88b30761fae22'
    # resp = requests.get(url=url)
    with open('data.txt', 'r') as fobj:
        data = json.load(fobj)
    # data = resp.json()
    df = json_normalize(data['list'])
    city_list = []
    new_df = df.loc[df['name'].str.startswith(alpha)].copy()
    no_of_rows = new_df.shape[0]
    city_lst = list(new_df['name'])
    return no_of_rows, city_lst


# app = dash.Dash()
app = dash.Dash()
colors = {
    'background': '#87D653',
    'text': '#ff0033'
}

app.layout = html.Div(children = [
    html.H1(children=' *** PICK CITY UI *** ',
            style={
            'background-image': 'url(https://upload.wikimedia.org/wikipedia/commons/2/22/North_Star_-_invitation_background.png)',
            'textAlign': 'center',
            'color': 'yellow'}),
    html.Br(),
    html.Label("Enter The City Alphabet and hit TAB: ",style={'color': 'blue', 'fontSize': 16}),
    html.Br(),
    html.Br(),
    dcc.Input(id='my-id', value='', type='text',placeholder="", style={'marginRight': '10px'}),
    html.Br(),
    html.Br(),
    html.Div(id='my-div',style={'color': 'blue', 'fontSize': 16})
])


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    print(input_value)
    if input_value == '':
        no_of_rows = ''
        city_lst = ''
    else:
        input_value = input_value.upper()
        no_of_rows, city_lst = _pick_city(input_value)

    #text1 = "Number of cities beginning with letter " + input_value + "are" + no_of_rows + "."
    #text2 = "Cities are: " + city_lst
    if no_of_rows ==0:
        return 'No CITY found starting with letter - " {} "'.format(input_value)
    elif no_of_rows >0:
        return 'Number of cities beginning with letter " {} " is/are {}.'.format(input_value,
                                                                         no_of_rows), '   Here are the City Names: {} "'.format(city_lst)
   
if __name__ == '__main__':
    app.run_server()
