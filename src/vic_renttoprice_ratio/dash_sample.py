import pandas as pd
import requests
# import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ---------- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
mapbox_access_token = 'pk.eyJ1IjoiZXZlbnciLCJhIjoiY2ttdmpvZTRzMDJrYzJubzE4NW55a3FhaCJ9.hkBgcquyzZwavOoe6DbSZw'

# get geojson file from the link
url = 'https://data.gov.au/geoserver/vic-suburb-locality-boundaries-psma-administrative-boundaries/wfs?request=' \
      'GetFeature&typeName=ckan_af33dd8c_0534_4e18_9245_fc64440f742e&outputFormat=json'
res = requests.get(url)
# vic_map = json.loads(res)
vic_map = res.json()

data = pd.read_csv("../../data/processed/raw_data.csv")
data = data.drop(columns=['Unnamed: 0'])


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2020", "value": 2020},
                     {"label": "2019", "value": 2019},
                     {"label": "2018", "value": 2018},
                     {"label": "2017", "value": 2017}],
                 multi=False,
                 value=2020,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
# function to generate graph
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = data.copy()
    dff = dff[dff["Year"] == option_slctd]

    '''
    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )
    '''
    # Plotly Graph Objects (GO)
    fig = go.Figure(
        data=[go.Choroplethmapbox(
            geojson=vic_map,
            featureidkey="properties.vic_loca_2",

            locations=dff.NAME,
            z=dff.House_Price,
        )]
    )

    fig.update_layout(
        title_text="Bees Affected by Mites in the USA",
        title_xanchor="center",
        title_font=dict(size=24),
        title_x=0.5,
        mapbox_style="open-street-map",
        mapbox=dict(
            center={"lat": -37.813611, "lon": 144.963056},
            zoom=7,
            accesstoken=mapbox_access_token,
        ),

    )
    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
