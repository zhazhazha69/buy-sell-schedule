# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from sqlalchemy import *
import time
from datetime import datetime


app = dash.Dash(__name__, 
    update_title=None
        )


postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'
                .format(username="your_config",
                        password="your_config",
                        ipaddress="your_config",
                        port="your_config",
                        dbname="your_config"))


engine = create_engine(postgres_str)


app.index_string = '''
<!DOCTYPE html>
<html lang='ru'>
    <head>
        <title>Dash for buy-sell-schedule</title>
        <meta name="viewport" content="width=1800", initial-scale="1">
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@200&display=swap" rel="stylesheet">
        {%config%}
        {%scripts%}
        <style>
            body {margin: 0; padding: 0; background-color: #202020;}
            
            .header {
              padding: 30px 0px; margin: 0px 0px 30px;
              background-color: #FFCC29; text-align: center;}
            
            h1 {
              color: #393E46; font-size: 50px;
              font-family: 'Montserrat', sans-serif; margin: 0;}
            
            button {
              font-size: 40px; color: #f1e658;
              font-family: 'Montserrat', sans-serif;
              width: 400px; height: 100px;
              border-radius: 60px; border-width: 0px;
              background: #181818;
              box-shadow:  46px 46px 92px #121212,
                 -46px -46px 92px #2e2e2e;
              user-select: none; transition: 0.4s;}
            
            button:hover {transform: scale(1.06); transition: 0.4s;}

            #DivGraph_30th_long .svg-container {
              box-shadow:  9px 9px 18px #0a0a0a,
                -9px -9px 18px #262626;
              border-style: solid; border-width: 4px; border-color: #181818; border-radius: 15px;
              display: inline-flex; transition: 0.4s;}
            
            .svg-container:hover {transform: scale(1.06); transition: 0.4s;}
            
            #GraphDiv_1th, #GraphDiv_5th,
            #GraphDiv_10th, #GraphDiv_20th,
            #GraphDiv_30th, #GraphDiv_long {display: inline-grid; width: 290px;}

            #graph_1th, #graph_1th_scatter, #graph_5th, #graph_5th_scatter,
            #graph_10th, #graph_10th_scatter, #graph_20th, #graph_20th_scatter,
            #graph_30th, #graph_30th_scatter, #graph_long, #graph_long_scatter {
              width: 270px; height: 300px;}
            
            #graph_1th_scatter, #graph_5th_scatter, 
            #graph_10th_scatter, #graph_20th_scatter,
            #graph_30th_scatter, #graph_long_scatter {
              margin: 0 auto; margin-top: 20px;}
            
            @media (min-width: 1000px) {
              #GraphDiv_1th, #GraphDiv_5th,
              #GraphDiv_10th, #GraphDiv_20th,
              #GraphDiv_30th, #GraphDiv_long {width: 162px;}

              #graph_1th, #graph_5th,
              #graph_10th, #graph_20th,
              #graph_30th, #graph_long {width: 150px; height: 200px;}

              #graph_1th_scatter, #graph_5th_scatter, #graph_10th_scatter, 
              #graph_20th_scatter, #graph_30th_scatter, #graph_long_scatter {
                width: 150px; height: 300px;}
              
              #DivGraph_30th_long {margin-left: calc(calc(100% - 972px)/ 2);}
            }
            @media (min-width: 1100px) {
              #GraphDiv_1th, #GraphDiv_5th,
              #GraphDiv_10th, #GraphDiv_20th,
              #GraphDiv_30th, #GraphDiv_long {width: 180px;}

              #graph_1th, #graph_5th,
              #graph_10th, #graph_20th,
              #graph_30th, #graph_long {width: 156px; height: 210px;}

              #graph_1th_scatter, #graph_5th_scatter, #graph_10th_scatter, 
              #graph_20th_scatter, #graph_30th_scatter, #graph_long_scatter {
                width: 156px; height: 300px;}
              
              #DivGraph_30th_long {margin-left: calc(calc(100% - 1080px)/ 2);}
            }
            @media (min-width: 1200px) {
              #GraphDiv_1th, #GraphDiv_5th,
              #GraphDiv_10th, #GraphDiv_20th,
              #GraphDiv_30th, #GraphDiv_long {width: 195px;}

              #graph_1th, #graph_5th,
              #graph_10th, #graph_20th,
              #graph_30th, #graph_long {width: 178px; height: 230px;}

              #graph_1th_scatter, #graph_5th_scatter, #graph_10th_scatter, 
              #graph_20th_scatter, #graph_30th_scatter, #graph_long_scatter {
                width: 178px; height: 300px;}
              
              #DivGraph_30th_long {margin-left: calc(calc(100% - 1170px)/ 2);}
            }
            @media (min-width: 1400px) {
              #GraphDiv_1th, #GraphDiv_5th,
              #GraphDiv_10th, #GraphDiv_20th,
              #GraphDiv_30th, #GraphDiv_long {width: 230px;}
              
              #graph_1th, #graph_5th,
              #graph_10th, #graph_20th,
              #graph_30th, #graph_long {width: 212px; height: 255px;}

              #graph_1th_scatter, #graph_5th_scatter, #graph_10th_scatter, 
              #graph_20th_scatter, #graph_30th_scatter, #graph_long_scatter {
                width: 212px; height: 300px;}
              
              #DivGraph_30th_long {margin-left: calc(calc(100% - 1390px)/ 2);}
            }
            @media (min-width: 1600px) {
              #GraphDiv_1th, #GraphDiv_5th,
              #GraphDiv_10th, #GraphDiv_20th,
              #GraphDiv_30th, #GraphDiv_long {width: 260px;}
              #graph_1th, #graph_5th,
              #graph_10th, #graph_20th,
              #graph_30th, #graph_long {width: 250px; height: 280px;}

              #graph_1th_scatter, #graph_5th_scatter, #graph_10th_scatter, 
              #graph_20th_scatter, #graph_30th_scatter, #graph_long_scatter {
                width: 250px; height: 300px;}
              
              #DivGraph_30th_long {margin-left: calc(calc(100% - 1560px)/ 2);}
            }
            @media (min-width: 1760px) {
              #GraphDiv_1th, #GraphDiv_5th,
              #GraphDiv_10th, #GraphDiv_20th,
              #GraphDiv_30th, #GraphDiv_long {width: 290px;}

              #graph_1th, #graph_1th_scatter, #graph_5th, #graph_5th_scatter,
              #graph_10th, #graph_10th_scatter, #graph_20th, #graph_20th_scatter,
              #graph_30th, #graph_30th_scatter, #graph_long, #graph_long_scatter {
                width: 270px; height: 300px;}
              #graph_1th_scatter, #graph_5th_scatter, 
              #graph_10th_scatter, #graph_20th_scatter,
              #graph_30th_scatter, #graph_long_scatter {
                margin: 0 auto; margin-top: 20px;}
              
              #DivGraph_30th_long {margin-left: calc(calc(100% - 1740px)/ 2);}
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div(children=[
    html.Div(className = "header", children = [
        html.H1(children = "Synchronization - None trend", id = "sync"),
        ]),

    html.Div(children=[
        html.Div(children=[
            dcc.Graph(
            id = 'graph_1th', style = {'margin': '0 auto'}),
            dcc.Graph(
            id = 'graph_1th_scatter', style = {'margin-top': '20px'})
            ], id = 'GraphDiv_1th'),
        html.Div(children=[
            dcc.Graph(
            id = 'graph_5th', style = {'margin': '0 auto'}),
            dcc.Graph(
            id = 'graph_5th_scatter', style = {'margin-top': '20px'})
            ], id = 'GraphDiv_5th'),
        html.Div(children=[
            dcc.Graph(
            id = 'graph_10th', style = {'margin': '0 auto'}),
            dcc.Graph(
            id = 'graph_10th_scatter', style = {'margin-top': '20px'})
            ], id = 'GraphDiv_10th'),
        html.Div(children=[
            dcc.Graph(
            id = 'graph_20th', style = {'margin': '0 auto'}),
            dcc.Graph(
            id = 'graph_20th_scatter', style = {'margin-top': '20px'})
            ], id = 'GraphDiv_20th'),
        html.Div(children=[
            dcc.Graph(
            id = 'graph_30th', style = {'margin': '0 auto'}),
            dcc.Graph(
            id = 'graph_30th_scatter', style = {'margin-top': '20px'})
            ], id = 'GraphDiv_30th'),
        html.Div(children=[
            dcc.Graph(
            id = 'graph_long', style = {'margin': '0 auto'}),
            dcc.Graph(
            id = 'graph_long_scatter', style = {'margin-top': '20px'})
            ], id = 'GraphDiv_long'),

        ], id = 'DivGraph_30th_long', style = {"display": "none"}),

    html.Div(
        html.Button(children='Start', id='show_btn'),
        style={'text-align': 'center', 'padding': '50px 0px 0px'}
        ),
    
    dcc.Interval(
        id='interval',
        interval=2.5*1000,
        n_intervals=0
        )
    ])

good_trend = True
bad_trend = True
labels = ['Buy','Sale']

name = 'Buy Sale'

x_line_long, y_line_long_false, y_line_long_true = [], [], []
x_line_30th, y_line_30th_false, y_line_30th_true = [], [], []
x_line_20th, y_line_20th_false, y_line_20th_true = [], [], []
x_line_10th, y_line_10th_false, y_line_10th_true = [], [], []
x_line_5th, y_line_5th_false, y_line_5th_true = [], [], []
x_line_1th, y_line_1th_false, y_line_1th_true = [], [], []

def upload_trend(df_short, df_long):
    _false_fast = df_short[df_short["m"] == False]["q"].sum()
    _true_fast = df_short[df_short["m"] == True]["q"].sum()
    _false = df_long[df_long["m"] == False]["q"].sum()
    _true = df_long[df_long["m"] == True]["q"].sum()
    if _false > _true: return True, None
    elif _true > _false: return False, None

def upload_data_vector(df, x_line, y_line_false, y_line_true):
    _false = df[df["m"] == False]["q"].sum()
    _true = df[df["m"] == True]["q"].sum()
    add_x_vector = round((_false / (_true + _false)) * 100, 2)
    add_y_vector = round(((_true / (_false + _true)) * 100) * 1, 2)
    y_line_false.append(add_x_vector)
    y_line_true.append(add_y_vector)
    x_line.append(datetime.now())

@app.callback(
    Output("sync", "children"),
    Output("show_btn", "children"),
    Output("graph_1th", "figure"), Output("graph_1th_scatter", "figure"),
    Output("graph_5th", "figure"), Output("graph_5th_scatter", "figure"),
    Output("graph_10th", "figure"), Output("graph_10th_scatter", "figure"),
    Output("graph_20th", "figure"), Output("graph_20th_scatter", "figure"),
    Output("graph_30th", "figure"), Output("graph_30th_scatter", "figure"),
    Output("graph_long", "figure"), Output("graph_long_scatter", "figure"),
    Output("DivGraph_30th_long", 'style'),
    Input("show_btn", "n_clicks"), Input('interval', 'n_intervals'),
)
def change_text(n_clicks, n_intervals):
    if n_clicks is None:
        raise PreventUpdate

    elif n_clicks % 2 == 0:
        return "Synchronization - None trend", 'Start', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {"display": "none"}

    elif n_clicks % 2 != 0:
        df_long = pd.read_sql("""SELECT your_marker as M, sum(your_value) as Q FROM yourDatabase GROUP BY your_marker""", engine)
        df_30 = pd.read_sql("""SELECT your_date, your_value as Q, your_marker as M FROM yourDatabase ORDER BY your_date DESC LIMIT 30000""", engine)
        df_30th = df_30[:30000].groupby("m")["q"].sum().reset_index()
        df_20th = df_30[:20000].groupby("m")["q"].sum().reset_index()
        df_10th = df_30[:10000].groupby("m")["q"].sum().reset_index()
        df_5th = df_30[:5000].groupby("m")["q"].sum().reset_index()
        df_1th = df_30[:1000].groupby("m")["q"].sum().reset_index()
        

        upload_data_vector(df_long, x_line_long, y_line_long_false, y_line_long_true)
        upload_data_vector(df_30th, x_line_30th, y_line_30th_false, y_line_30th_true)
        upload_data_vector(df_20th, x_line_20th, y_line_20th_false, y_line_20th_true)
        upload_data_vector(df_10th, x_line_10th, y_line_10th_false, y_line_10th_true)
        upload_data_vector(df_5th, x_line_5th, y_line_5th_false, y_line_5th_true)
        upload_data_vector(df_1th, x_line_1th, y_line_1th_false, y_line_1th_true) 

        values_long = [df_long["q"].loc[0], df_long["q"].loc[1]]
        values_30th = [df_30th["q"].loc[0], df_30th["q"].loc[1]]
        values_20th = [df_20th["q"].loc[0], df_20th["q"].loc[1]]
        values_10th = [df_10th["q"].loc[0], df_10th["q"].loc[1]]
        values_5th = [df_5th["q"].loc[0], df_5th["q"].loc[1]]
        values_1th = [df_1th["q"].loc[0], df_1th["q"].loc[1]]
        
        graph_width = 270; graph_height = 300
        graph_margin = {
            "l": 30,
            "r": 30,
            "b": 30,
            "t": 80,
        }
        bgcolor = '#181818'; graph_colorway = ['#007965', '#FF0000']; graph_title_color = "#f1e658"
        
        fig_long = go.Figure(data = [go.Pie(labels = labels, values = values_long, hole = 0.3)])
        fig_long_scatter = make_subplots(1, 1, specs = [[{"type": "scatter"}]])
        fig_long_scatter.add_trace(go.Scatter(x = x_line_long, y = y_line_long_true, name = labels[0]), 1, 1)
        fig_long_scatter.add_trace(go.Scatter(x = x_line_long, y = y_line_long_false, name = labels[1]), 1, 1)

        fig_30th = go.Figure(data = [go.Pie(labels = labels, values = values_30th, hole = 0.3)])
        fig_30th_scatter = make_subplots(1, 1, specs = [[{"type": "scatter"}]])
        fig_30th_scatter.add_trace(go.Scatter(x = x_line_30th, y = y_line_30th_true, name = labels[0]), 1, 1)
        fig_30th_scatter.add_trace(go.Scatter(x = x_line_30th, y = y_line_30th_false, name = labels[1]), 1, 1)

        fig_20th = go.Figure(data = [go.Pie(labels = labels, values = values_20th, hole = 0.3)])
        fig_20th_scatter = make_subplots(1, 1, specs = [[{"type": "scatter"}]])
        fig_20th_scatter.add_trace(go.Scatter(x = x_line_20th, y = y_line_20th_true, name = labels[0]), 1, 1)
        fig_20th_scatter.add_trace(go.Scatter(x = x_line_20th, y = y_line_20th_false, name = labels[1]), 1, 1)

        fig_10th = go.Figure(data = [go.Pie(labels = labels, values = values_10th, hole = 0.3)])
        fig_10th_scatter = make_subplots(1, 1, specs = [[{"type": "scatter"}]])
        fig_10th_scatter.add_trace(go.Scatter(x = x_line_10th, y = y_line_10th_true, name = labels[0]), 1, 1)
        fig_10th_scatter.add_trace(go.Scatter(x = x_line_10th, y = y_line_10th_false, name = labels[1]), 1, 1)

        fig_5th = go.Figure(data = [go.Pie(labels = labels, values = values_5th, hole = 0.3)])
        fig_5th_scatter = make_subplots(1, 1, specs = [[{"type": "scatter"}]])
        fig_5th_scatter.add_trace(go.Scatter(x = x_line_5th, y = y_line_5th_true, name = labels[0]), 1, 1)
        fig_5th_scatter.add_trace(go.Scatter(x = x_line_5th, y = y_line_5th_false, name = labels[1]), 1, 1)
        
        fig_1th = go.Figure(data = [go.Pie(labels = labels, values = values_1th, hole = 0.3)])
        fig_1th_scatter = make_subplots(1, 1, specs = [[{"type": "scatter"}]])
        fig_1th_scatter.add_trace(go.Scatter(x = x_line_1th, y = y_line_1th_true, name = labels[0]), 1, 1)
        fig_1th_scatter.add_trace(go.Scatter(x = x_line_1th, y = y_line_1th_false, name = labels[1]), 1, 1)
        fig_long.update_layout(
            title = "Overall volume", title_font_color = graph_title_color, title_font_family = 'Montserrat', title_font_size = 22, margin = graph_margin, paper_bgcolor = bgcolor, colorway = graph_colorway, font = {"color": graph_title_color}, showlegend = False
            )
        fig_long_scatter.update_layout(
            title = "Overall volume", title_font_color = graph_title_color, title_font_family = 'Montserrat', title_font_size = 22, margin = graph_margin, paper_bgcolor = bgcolor, colorway = graph_colorway, font = {"color": graph_title_color}, showlegend = False
            )
        fig_30th.update_layout(
            title = "Volume 30К", title_font_color = graph_title_color, title_font_family = 'Montserrat', title_font_size = 22, margin = graph_margin, paper_bgcolor = bgcolor, colorway = graph_colorway, font = {"color": graph_title_color}, showlegend = False
            )
        fig_30th_scatter.update_layout(
            title = "Volume 30К", title_font_color = graph_title_color, title_font_family = 'Montserrat', title_font_size = 22, margin = graph_margin, paper_bgcolor = bgcolor, colorway = graph_colorway, font = {"color": graph_title_color}, showlegend = False
            )
        fig_20th.update_layout(
            title = "Volume 20К", title_font_color = graph_title_color, title_font_family = 'Montserrat', title_font_size = 22, margin = graph_margin, paper_bgcolor = bgcolor, colorway = graph_colorway, font = {"color": graph_title_color}, showlegend = False
            )
        fig_20th_scatter.update_layout(
            title = "Volume 20К", title_font_color = graph_title_color, title_font_family = 'Montserrat', title_font_size = 22, margin = graph_margin, paper_bgcolor = bgcolor, colorway = graph_colorway, font = {"color": graph_title_color}, showlegend = False
            )
        fig_10th.update_layout( 
            title = "Volume 10К", title_font_color = graph_title_color, title_font_family = 'Montserrat', title_font_size = 22, margin = graph_margin, paper_bgcolor = bgcolor, colorway = graph_colorway, font = {"color": graph_title_color}, showlegend = False
            )
        fig_10th_scatter.update_layout(
            title = "Volume 20К", title_font_color = graph_title_color, title_font_family = 'Montserrat', title_font_size = 22, margin = graph_margin, paper_bgcolor = bgcolor, colorway = graph_colorway, font = {"color": graph_title_color}, showlegend = False
            )
        fig_5th.update_layout(
            title = "Volume 5К", title_font_color = graph_title_color, title_font_family = 'Montserrat', title_font_size = 22, margin = graph_margin, paper_bgcolor = bgcolor, colorway = graph_colorway, font = {"color": graph_title_color}, showlegend = False
            )
        fig_5th_scatter.update_layout(
            title = "Volume 5К", title_font_color = graph_title_color, title_font_family = 'Montserrat', title_font_size = 22, margin = graph_margin, paper_bgcolor = bgcolor, colorway = graph_colorway, font = {"color": graph_title_color}, showlegend = False
            )
        fig_1th.update_layout(
            title = "Volume 1К", title_font_color = graph_title_color, title_font_family = 'Montserrat', title_font_size = 22, margin = graph_margin, paper_bgcolor = bgcolor, colorway = graph_colorway, font = {"color": graph_title_color}, showlegend = False
            )
        fig_1th_scatter.update_layout(
            title = "Volume 1К", title_font_color = graph_title_color, title_font_family = 'Montserrat', title_font_size = 22, margin = graph_margin, paper_bgcolor = bgcolor, colorway = graph_colorway, font = {"color": graph_title_color}, showlegend = False
            )

        good_trend, bad_trend = upload_trend(df_1th, df_long)
        request = engine.execute("""SELECT your_date FROM yourDatabase ORDER BY your_date DESC LIMIT 1""")
        new_time = request.fetchone()
        SYNC = round((round(time.time() + 10800, 3) - (new_time[0] / 1000)), 5)
        SYNC = f'Synchronization - {SYNC} trend - {good_trend}/{bad_trend}'

        return (
            SYNC,
            "Stop",
            fig_1th, fig_1th_scatter, fig_5th, fig_5th_scatter,
            fig_10th, fig_10th_scatter, fig_20th, fig_20th_scatter,
            fig_30th, fig_30th_scatter, fig_long, fig_long_scatter,
            {"display": "flow-root"},
            )

        
if __name__ == '__main__':
    app.run_server(debug=False)
