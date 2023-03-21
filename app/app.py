""" Creater: Melissa Robertson"""
import os
import glob
import base64
import plotly.graph_objects as go
import plotly.express as px
import dash
import flask
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from gpx_converter import Converter
import pandas as pd
import numpy as np

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
server = app.server
with open(os.path.join(os.getcwd(),".mapbox_token"), "r", encoding="utf8") as map_file:
    mapbox_token = map_file.read()
px.set_mapbox_access_token(mapbox_token)

class TrailProcessing:
    """
    A class used to represent an Trail processing data

    ...

    Attributes
    ----------
    trail_data_frame : DataFrame
        a data frame that represents the latitude and longitude of imported gpx data

    Methods
    -------
    parse_multiple(filename)
        Reads in multiple gpx files and outputs into one csv file
    parse_upload_contents(contents)
        Takes gpx data uploaded from site and imports it into data frame
    parse_file_contents(file)
        Takes a gpx file and imports it into data frame
    create_fig
        Creates figure based on current datagrame
    get_middle
        Takes dataframe and gets middle points and zoom data for map figure

    """
    def __init__(self, filename):
        """
        Parameters
        ----------
        filename : str
            The name of the initial csv file to load
        """
        self.trail_data_frame = pd.read_csv(filename)

    @staticmethod
    def parse_multiple(path, outputfile):
        """Combines gpx data into a csv if no files are found returns empty file.

        Parameters
        ----------
        outputfile : str
            File name used to output combined csv

        """
        files = glob.glob(os.path.join(path,'*.gpx'))
        data_frame = pd.DataFrame()
        for file in files:
            print (file)
            data_frame = pd.concat(objs=[data_frame, Converter(input_file=file).gpx_to_dataframe()])
        data_frame.to_csv(outputfile, index=False)

    def parse_upload_contents(self, contents):
        """Takes uploaded gpx data and adds it to current dataframe

        Parameters
        ----------
        contents : str
            Gpx content used as input to create combined dataframe

        """
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
        """Takes gpx data and adds it to current dataframe

        Parameters
        ----------
        file : str
            File name (*.gpx) used as input to create combined dataframe

        """
        self.trail_data_frame = pd.concat(objs=[self.trail_data_frame,
                            Converter(input_file=file).gpx_to_dataframe()])

    def create_fig(self):
        """Takes dataframe and creates map"""
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
        """Takes dataframe and gets middle points and zoom data for map figure"""
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


trail = TrailProcessing("trail_output.csv")
#trail.parse_multiple(r'\python-app\test-app', "outputtest.csv")


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
                            multiple=False
                       ),
                    ])



@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'))
def parse_upload_contents(list_of_contents):
    """Function to process uploaded file from website """
    if list_of_contents is not None:
        trail.parse_upload_contents(list_of_contents)
        return [dcc.Graph(figure=trail.create_fig())]
    return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='8080')
