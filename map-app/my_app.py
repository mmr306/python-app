""" Creater: Melissa Robertson"""
import os
import plotly.graph_objects as go
import dash
from dash import html
from dash import dcc

app = dash.Dash()

mapbox_access_token = os.environ['mapbox_access_token']
fig = go.Figure(go.Scattermapbox(
        lat=['45.5017'],
        lon=['-73.5673'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14
        ),
        text=['Montreal'],
    ))

fig.update_layout(
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        style="mapbox://styles/mmr306/clfa9p7ps000e01mtz8vrufms",
        center=go.layout.mapbox.Center(
            lat=45,
            lon=-73
        ),
        pitch=0,
        zoom=5
    )
)
app.layout = html.Div(dcc.Graph(id='fig1', figure=fig))
app.run_server(debug=True)
