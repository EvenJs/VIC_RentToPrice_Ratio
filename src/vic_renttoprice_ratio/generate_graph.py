import os
import requests
import pandas as pd
import read_csv
# import re
import plotly.graph_objects as go

# get your own access token from the mapbox website
mapbox_access_token = os.getenv("mapbox_access_token")
url = 'https://data.gov.au/geoserver/vic-suburb-locality-boundaries-psma-administrative-boundaries/wfs?request=' \
      'GetFeature&typeName=ckan_af33dd8c_0534_4e18_9245_fc64440f742e&outputFormat=json'


def get_geojson(link):
    # get geojson file from the link
    res = requests.get(link)
    # vic_map = json.loads(res)
    vic_json = res.json()
    return vic_json

# read the processed data
'''
df = pd.read_csv("../../data/processed/raw_data.csv")
df = df.drop(columns=['Unnamed: 0'])

df = read_csv.main()
print(df.info())
features = df.select_dtypes('float64').columns.to_list()

data = df.copy()
data = data[data["Year"] == str(2020)]
print(data)
'''


def generate_graph(data, vic_map):
    trace = []
    # Set the data for the map
    for i in features:
        trace.append(go.Choroplethmapbox(
            geojson=vic_map,
            locations=data['NAME'],
            z=data[i],
            # text=data.NAME,
            # hovertemplate="<b>%{text}</b><br>" +"%{z}<br>" + "<extra></extra>",
            colorbar=dict(thickness=10, ticklen=3, outlinewidth=0),
            featureidkey="properties.vic_loca_2",
            # marker_line_width=1, marker_opacity=0.8,
            # colorscale="Blues_r",
            visible=False)
        )
    trace[0]['visible'] = True  # set the visibility of the first entry class's visibility content

    lst = []
    ii = -1
    for i in features:
        ii += 1
        tlist = [False for z in range(len(features))]
        tlist[ii] = True
        temp = dict(args=['visible', tlist], label=i, method='restyle')
        lst.append(temp)

    # add a dropdown menu in the layout
    # layout.update(height=500,updatemenus=list([dict(x=0.8,y=1.1,xanchor='left',yanchor='middle',buttons=lst)]))

    # The rest is the same
    fig = go.Figure(data=trace)
    fig.update_layout(title_text='Vic property price and rent', title_x=0.01)
    fig.update_layout(
        # hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            # bearing=90,
            center={"lat": -37.813611, "lon": 144.963056},
            pitch=0,
            zoom=6,

        ),
        mapbox_style="open-street-map",
    )
    fig.update_layout(height=800, updatemenus=list([dict(x=0.8, y=1.1, xanchor='left', yanchor='middle', buttons=lst)]))

    fig.show()
    # fig.write_html("../../reports/VIC.html")


if __name__ == '__main__':
    df = read_csv.main()
    print(df.info())
    features = df.select_dtypes('float64').columns.to_list ()

    data = df.copy()
    data = data[data["Year"] == str(2020)]
    vic_map = get_geojson(url)
    generate_graph(data, vic_map)