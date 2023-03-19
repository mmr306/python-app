""" Creater: Melissa Robertson"""
import os
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html
from dash import dcc
from gpx_converter import Converter
import pandas as pd
import numpy as np
import glob
from dash.dependencies import Input, Output, State
import base64
px.set_mapbox_access_token(open(os.path.join(os.getcwd(),'map-app',".mapbox_token")).read())

class TrailProcessing:
    def __init__(self, filename):
        self.trailDataFrame = self.parse_csv(filename)
    def parse_csv(self, filename):
        return pd.read_csv(filename)
    
    def parse_multiple(self, path, outputfile):
        files = glob.glob(os.path.join(path,'*.gpx'))
        df = pd.DataFrame()
        for file in files:
            print (file)
            df = pd.concat(objs=[df, Converter(input_file=file).gpx_to_dataframe()])
        df.to_csv(outputfile, index=False)    

    def parse_upload_contents(self, contents, filename, date):
        try:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            with open("output.gpx","w+") as f:
                    f.write(decoded.decode('utf-8'))#.decode("utf-8"))
        except Exception as e:
            print(str(e))
        self.trailDataFrame = pd.concat(objs=[self.trailDataFrame, Converter(input_file="output.gpx").gpx_to_dataframe()])

    def parse_file_contents(self,file):
        self.trailDataFrame = pd.concat(objs=[self.trailDataFrame, Converter(input_file=file).gpx_to_dataframe()])

    def create_fig(self):
        fig2 = px.scatter_mapbox(self.trailDataFrame, lat="latitude", lon="longitude", color_discrete_sequence=["fuchsia"], zoom=3, height=700)
        middle = self.get_middle()
        print (middle)
        fig2.update_layout(hovermode='closest',
                        mapbox=dict(style="dark",
                                    #accesstoken="pk.eyJ1IjoibW1yMzA2IiwiYSI6ImNsZmFhMGMzNDAzamszc21ld3phd2xid2MifQ.MfmOecF0mCUyi67_GBQVFQ",
                                    bearing=0,
                                    center=go.layout.mapbox.Center(lat=middle['latitude'],lon=middle['longitude']), #center=go.layout.mapbox.Center(lat=44,lon=-73), 
                                    zoom=middle['zoom'],pitch=0))
        fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig2
    def get_middle(self):
        max_bound = max(abs(self.trailDataFrame.latitude.max()-self.trailDataFrame.latitude.min()), abs(self.trailDataFrame.longitude.max()-self.trailDataFrame.longitude.min())) * 111
        zoom = 11.5 - np.log(max_bound)
        return {
            'latitude': ((self.trailDataFrame.latitude.max() + self.trailDataFrame.latitude.min()) / 2.0),
            'longitude': ((self.trailDataFrame.longitude.max() + self.trailDataFrame.longitude.min()) / 2.0),
            'zoom': zoom
            }


trail = TrailProcessing("trail_output2.csv")
#trail.parse_multiple(r'/directory', "trail_output2.csv")
app = dash.Dash()

app.layout = html.Div([html.H1("Vermont Hiking"), 
                       html.Hr(), 
                       html.Div(children=[dcc.Graph(id='fig2', figure=trail.create_fig())], id='output-data-upload'),
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
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def parse_upload_contents(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        trail.parse_upload_contents(list_of_contents, list_of_names, list_of_dates)
        return [dcc.Graph(figure=trail.create_fig())]
    else:
        return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)
