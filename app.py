# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from sqlalchemy import *
import time


app = dash.Dash(__name__, 
    update_title=None,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=0.5"}]
        )


postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'
                .format(username="your_config",
                        password="your_config",
                        ipaddress="your_config",
                        port="your_config",
                        dbname="your_config"))


engine = create_engine(postgres_str)


labels = ['Buy','Sale']


app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Dash for buy-sell-schedule</title>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@200&display=swap" rel="stylesheet">
    </head>
    <style>
        body {
          margin: 0;
          padding: 0;
          background-color: #202020;
        }
        .header {
          padding: 30px 0px; 
          margin: 0px 0px 80px;
          background-color: #f1e658;
          text-align: center;
        }
        h1 {
          color: #202020;
          font-size: 50px;
          font-family: 'Montserrat', sans-serif;
          margin: 0;
        }
        button {
          font-size: 40px;
          width: 400px;
          height: 100px;
          color: #f1e658;
          font-family: 'Montserrat', sans-serif;
          user-select: none;
          border-radius: 60px;
          background: #181818;
          box-shadow:  46px 46px 92px #121212,
             -46px -46px 92px #2e2e2e;
          border-width: 0px;       
          transition: 0.4s;
        }
        button:hover {
          transform: scale(1.06);
          transition: 0.4s;
        }
        .plot-container {
          border-radius: 38px;
          background: #181818;
          box-shadow:  46px 46px 92px #0e0e0e,
             -46px -46px 92px #323232;
          display: inline-flex;
          border-style: solid;
          border-width: 11px;
          border-color: #181818;
          transition: 0.4s;
        }
        .plot-container:hover {
          transform: scale(1.06);
          transition: 0.4s;
        }
        #GraphDiv1,
        #GraphDiv2 {
          display: inline-flex; 
          width: 50%;
        }
        @media (max-width: 1300px) {
          #GraphDiv1 {
            width: 100%;
          }
          #GraphDiv2 {
            width: 100%;
            padding-top: 120px;
          }
        }
    </style>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


app.layout = html.Div(children=[
    html.Div(className="header", children=[
        html.H1(children="Trend - None", id="sync"),
        ]),
    
    html.Div(children=[
        html.Div(children=[
            dcc.Graph(
            id='graph1',
            style={
            "float": "left", 
            'margin': '0 auto'})
            ], id='GraphDiv1'),
        html.Div(children=[
            dcc.Graph(
            id='graph2',
            style={
            "float": "right", 
            'margin': '0 auto'})
            ], id='GraphDiv2'),
        ], id='DivGraph', style={"display": "none"}),

    html.Div(
        html.Button(children='Start', id='show_btn'),
        style={'text-align': 'center', 'padding': '94px 0px'}
        ),
    
    dcc.Interval(
            id='interval',
            interval=1*1000,
            n_intervals=0
        )
    ])


@app.callback(
    Output("sync", "children"),
    Output("show_btn", "children"),
    Output("graph1", "figure"),
    Output("graph2", "figure"),
    Output("DivGraph", 'style'),
    Input("show_btn", "n_clicks"),
    Input('interval', 'n_intervals'),
)
def change_text(n_clicks, n_intervals):
    if n_clicks is None:
        raise PreventUpdate

    elif n_clicks % 2 == 0:
        return "Trend - None", 'Start', {}, {}, {"display": "none"}

    elif n_clicks % 2 != 0:
        df = pd.read_sql("""SELECT date, your_value as Q , your_value_marker as M FROM yourDatabase ORDER BY date DESC LIMIT 1500""", engine)
        df1 = df.groupby("m")["q"].sum().reset_index()
        df2 = pd.read_sql("""SELECT your_value_marker as M, sum(your_value) as Q FROM yourDatabase GROUP BY your_value_marker""", engine)
        values1 = [df1["q"].loc[0], df1["q"].loc[1]]
        values2 = [df2["q"].loc[0], df2["q"].loc[1]]
        
        fig1 = go.Figure(data=[go.Pie(labels=labels, values=values1, hole=0.8)])
        fig2 = go.Figure(data=[go.Pie(labels=labels, values=values2, hole=0.8)])
        fig1.update_layout(
            title="Quick volume",title_font_color="#f1e658",title_font_family='Montserrat',title_font_size=35,width=550,height=500,legend_bgcolor='#181818',legend_bordercolor='#181818',paper_bgcolor='#181818',colorway=['#008001', '#fe0000']
            )
        fig2.update_layout(
            title="Overall volume",title_font_color="#f1e658",title_font_family='Montserrat',title_font_size=35,width=550,height=500,legend_bgcolor='#181818',legend_bordercolor='#181818',paper_bgcolor='#181818',colorway=['#008001', '#fe0000']
            )

        request = engine.execute("""SELECT date FROM yourDatabase ORDER BY date DESC LIMIT 1""")        
        new_time = request.fetchone()
        SYNC = round((round(time.time() + 10800, 3) - (new_time[0] / 1000)), 5)
        SYNC = f'Trend - {SYNC}'

        return (
            SYNC,
            "Stop",
            fig1,fig2,
            {"display": "flow-root"},
            )

        
if __name__ == '__main__':
    app.run_server(debug=False)