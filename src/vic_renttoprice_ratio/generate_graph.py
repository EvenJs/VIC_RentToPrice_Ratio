import requests
import pandas as pd
# import re
import plotly.graph_objects as go

mapbox_access_token = 'pk.eyJ1IjoiZXZlbnciLCJhIjoiY2ttdmpvZTRzMDJrYzJubzE4NW55a3FhaCJ9.hkBgcquyzZwavOoe6DbSZw'

# get geojson file from the link
url = 'https://data.gov.au/geoserver/vic-suburb-locality-boundaries-psma-administrative-boundaries/wfs?request=' \
      'GetFeature&typeName=ckan_af33dd8c_0534_4e18_9245_fc64440f742e&outputFormat=json'
res = requests.get(url)
# vic_map = json.loads(res)
vic_map = res.json()

# read the processed data

df = pd.read_csv("../../data/processed/raw_data.csv")
df = df.drop(columns=['Unnamed: 0'])


features = df.select_dtypes('float64').columns.to_list()

data = df.copy()
data = data[data["Year"] == int(2020)]

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
#fig.write_html("../../reports/VIC.html")
