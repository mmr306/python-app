""" Creater: Melissa Robertson"""
import os
import glob
import base64
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from gpx_converter import Converter
import pandas as pd
import numpy as np

with open(os.path.join(os.getcwd(),'map-app',".mapbox_token"), "r", encoding="utf8") as map_file:
    mapbox_token = map_file.read()
px.set_mapbox_access_token(mapbox_token)

class TrailProcessing:
    """ Class: TrailProcessing"""
    def __init__(self, filename):
        """ Function: """
        self.trail_data_frame = self.parse_csv(filename)

    @staticmethod
    def parse_csv(filename):
        """ Function: """
        return pd.read_csv(filename)

    @staticmethod
    def parse_multiple(path, outputfile):
        """ Function: """
        files = glob.glob(os.path.join(path,'*.gpx'))
        data_frame = pd.DataFrame()
        for file in files:
            print (file)
            data_frame = pd.concat(objs=[data_frame, Converter(input_file=file).gpx_to_dataframe()])
        data_frame.to_csv(outputfile, index=False)

    def parse_upload_contents(self, contents):
        """ Function: """
        try:
            content_string = contents.split(',')
            decoded = base64.b64decode(content_string[1])
            with open("output.gpx", "w+", encoding="utf-8") as output_write_file:
                output_write_file.write(decoded.decode('utf-8'))
        except ValueError as except_output:
            print(str(except_output))
        except OSError as except_output:
            print(str(except_output))
        self.trail_data_frame = pd.concat(objs=[self.trail_data_frame,
                            Converter(input_file="output.gpx").gpx_to_dataframe()])

    def parse_file_contents(self,file):
        """ Function: """
        self.trail_data_frame = pd.concat(objs=[self.trail_data_frame,
                            Converter(input_file=file).gpx_to_dataframe()])

    def create_fig(self):
        """ Function: """
        fig2 = px.scatter_mapbox(self.trail_data_frame, lat="latitude", lon="longitude",
                                color_discrete_sequence=["fuchsia"], zoom=3, height=700)
        middle = self.get_middle()
        print (middle)
        fig2.update_layout(hovermode='closest',
                        mapbox={"style" : "dark",
                                    "bearing" : 0,
                                    "center" : go.layout.mapbox.Center(lat=middle['latitude'],\
                                                                    lon=middle['longitude']),
                                    "zoom" : middle['zoom'],
                                    "pitch" : 0})
        fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig2

    def get_middle(self):
        """ Function: """
        max_bound = max(abs(self.trail_data_frame.latitude.max()-\
                            self.trail_data_frame.latitude.min()),\
                        abs(self.trail_data_frame.longitude.max()-\
                            self.trail_data_frame.longitude.min())) * 111
        zoom = 11.5 - np.log(max_bound)
        return {
            'latitude': ((self.trail_data_frame.latitude.max() + \
                            self.trail_data_frame.latitude.min()) / 2.0),
            'longitude': ((self.trail_data_frame.longitude.max() + \
                            self.trail_data_frame.longitude.min()) / 2.0),
            'zoom': zoom
            }


trail = TrailProcessing("trail_output2.csv")
#trail.parse_multiple(r'/directory', "trail_output2.csv")
app = dash.Dash()

app.layout = html.Div([html.H1("Vermont Hiking"),
                       html.Hr(),
                       html.Div(children=[dcc.Graph(id='fig2', figure=trail.create_fig())],
                                            id='output-data-upload'),
                       dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            # Allow multiple files to be uploaded
                            multiple=False
                       ),
                    ])



@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'))
def parse_upload_contents(list_of_contents):
    """ Function: """
    if list_of_contents is not None:
        trail.parse_upload_contents(list_of_contents)
        return [dcc.Graph(figure=trail.create_fig())]
    return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)
