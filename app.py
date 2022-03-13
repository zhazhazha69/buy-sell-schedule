# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from sqlalchemy import *
import time
from datetime import datetime
from exchange_data import get_data


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

            #GraphDiv_pie .svg-container {
              box-shadow:  34px 34px 49px #0a0a0a,
                -34px -34px 49px #262626;
              border-style: solid; border-width: 21px; border-color: #181818; border-radius: 70px;
              display: inline-flex; transition: 0.4s; width: 50%;}    
            #GraphDiv_indicator .svg-container {
              box-shadow:  9px 9px 18px #0a0a0a,
                -9px -9px 18px #262626;
              background: #181818;
              border-style: solid; border-width: 8px; border-color: #181818; border-radius: 26px;
              display: inline-flex; transition: 0.4s; width: 50%;}

            #graph_indicator_dropdown .Select,
            #graph_pie_dropdown .Select {
              font-size: 23px;
              font-family: 'Montserrat', sans-serif;
            }
            #GraphDiv_dropdown .Select-menu-outer {
              background-color: #f1e658;
              border: 0px solid #f1e658;
              border-radius: 15px;}

            #GraphDiv_dropdown .Select-menu-outer::-webkit-scrollbar-track {
              background: #181818;}

            #GraphDiv_dropdown .Select-menu-outer::-webkit-scrollbar-thumb {
              background: #f1e658;
              border-radius: 10px;
            }
            #GraphDiv_dropdown .Select-control {
              background: #f1e658;
              border-style: solid; 
              border-width: 8px; 
              border-color: #f1e658; 
              border-radius: 26px;
              box-shadow:  -9px -9px 18px #605c23,
                9px 9px 18px #ffff8d;
              color: #333;
              display: table;
              height: 36px;
              overflow: hidden;
              transition: 0.4s;}

            #graph_indicator1 .svg-container,
            #graph_indicator2 .svg-container {
              border-color: #f1e658;
              box-shadow:  -9px -9px 18px #605c23,
                9px 9px 18px #ffff8d;}

            .svg-container:hover {transform: scale(1.06); transition: 0.4s;}
            
            #GraphDiv_pie {display: inline-grid; width: 35%;}
            
            #GraphDiv_indicator_dropdown {display: grid; width: 63%;}

            #graph_pie {width: 75%; height: 440px;}
            
            #graph_pie_dropdown,
            #graph_indicator_dropdown {width: 75%; margin: 0 auto;}

            #GraphDiv_indicator {
              width: 100%; display: flex; align-self: flex-start; margin: 70px auto;
            }

            #GraphDiv_dropdown {width: 100%; display: grid;}

            #graph_indicator1, #graph_indicator2, #graph_indicator3,
            #graph_indicator4, #graph_indicator5 {width: 15%; height: 200px;}
            @media (min-width: 1300px) {
              #GraphDiv_pie {width: 31%;}

              #graph_pie {height: 400px;}

              #GraphDiv_indicator_dropdown {width: 68%;}
            }
            @media (min-width: 1400px) {
              #GraphDiv_pie {width: 35%;}

              #graph_pie {height: 420px;}

              #GraphDiv_indicator_dropdown {width: 63%;}
            }
            @media (min-width: 1550px) {
              #GraphDiv_pie {width: 37%;}

              #graph_pie {height: 440px;}

              #GraphDiv_indicator_dropdown {width: 62%;}
            }
            @media (min-width: 1700px) {
              #GraphDiv_pie {width: 37%;}

              #GraphDiv_indicator_dropdown {width: 60%;}
            }
            @media (min-width: 1800px) {
              #GraphDiv_pie {width: 40%;}

              #GraphDiv_indicator_dropdown {width: 59%;}
            }

            @media (min-width: 2000px) {
              #graph_indicator1, #graph_indicator2, #graph_indicator3,
              #graph_indicator4, #graph_indicator5 {height: 230px;}

              #graph_pie {height: 475px;}

              #GraphDiv_pie {width: 43%;}

              #GraphDiv_indicator_dropdown {width: 64%;}
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

    html.Div(children = [
        html.Div(children = [
            dcc.Graph(
                id = 'graph_pie', style = {'margin': '40px auto'}),
            ], id = 'GraphDiv_pie'),

        html.Div(children = [
            html.Div(children = [
                dcc.Graph(id = 'graph_indicator1', style = {'margin': '0 auto'}),
                dcc.Graph(id = 'graph_indicator2', style = {'margin': '0 auto'}),
                dcc.Graph(id = 'graph_indicator3', style = {'margin': '0 auto'}),
                dcc.Graph(id = 'graph_indicator4', style = {'margin': '0 auto'}),
                dcc.Graph(id = 'graph_indicator5', style = {'margin': '0 auto'}),
            ], id = 'GraphDiv_indicator'),
            
            html.Div(children = [
                dcc.Dropdown(
                    id='graph_indicator_dropdown', value='35',
                    searchable=False, clearable=False,
                    options=[
                        {'label': '85', 'value': '85'},
                        {'label': '75', 'value': '75'},
                        {'label': '65', 'value': '65'},
                        {'label': '55', 'value': '55'},
                        {'label': '45', 'value': '45'},
                        {'label': '35', 'value': '35'},
                        {'label': '25', 'value': '25'},
                        {'label': '15', 'value': '15'},
                    ],),
                dcc.Dropdown(
                    id='graph_pie_dropdown', value='30',
                    searchable=False, clearable=False,
                    options=[
                        {'label': 'Volume 30К', 'value': '30'},
                        {'label': 'Volume 15К', 'value': '15'},
                        {'label': 'Volume 10К', 'value': '10'},
                        {'label': 'Volume 5К', 'value': '5'},
                    ],),

            ], id = 'GraphDiv_dropdown')

        ], id = 'GraphDiv_indicator_dropdown'),

    ], id = 'DivGraph', style = {"display": "none"}),

    html.Div(
        html.Button(children = 'Запустить', id = 'show_btn'),
        style={'text-align': 'center', 'margin': '60px 0px 0px'}
        ),
    
    dcc.Interval(
        id='interval',
        interval=2.5*1000,
        n_intervals=0
        )
    ])

good_trend = True
bad_trend = True
labels = ['Buy', 'Sale']

def upload_trend(df_short, df_long):
    _false_fast = df_short[df_short["m"] == False]["q"].sum()
    _true_fast = df_short[df_short["m"] == True]["q"].sum()
    _false = df_long[df_long["m"] == False]["q"].sum()
    _true = df_long[df_long["m"] == True]["q"].sum()
    if _false > _true: return True, None
    elif _true > _false: return False, None

@app.callback(
    Output("sync", "children"), Output("show_btn", "children"),
    Output("graph_pie", "figure"), Output("graph_indicator1", "figure"),
    Output("graph_indicator2", "figure"), Output("graph_indicator3", "figure"),
    Output("graph_indicator4", "figure"), Output("graph_indicator5", "figure"),
    Output("DivGraph", 'style'),

    Input("show_btn", "n_clicks"), 
    Input('interval', 'n_intervals'),
    Input('graph_pie_dropdown', 'value'),
    Input('graph_indicator_dropdown', 'value')
)
def change_text(n_clicks, n_intervals, pie_value, indicator_value):
    if n_clicks is None:
        raise PreventUpdate

    elif n_clicks % 2 == 0:
        return "Synchronization - None trend", 'Run', {}, {}, {}, {}, {}, {}, {"display": "none"}

    elif n_clicks % 2 != 0:
        df = pd.read_sql(f"""SELECT your_date, your_value as Q , your_marker as M FROM yourDatabase ORDER BY your_date DESC LIMIT {pie_value}000""", engine)
        df_pie = df.groupby("m")["q"].sum().reset_index()
        df_1500 = df[:1000].groupby("m")["q"].sum().reset_index()
        
        values_pie = [df_pie["q"].loc[0], df_pie["q"].loc[1]]
        
        graph_margin = { "l": 30, "r": 30, "b": 30, "t": 80,}
        graph_indicator_margin = { "l": 30, "r": 30, "b": 30, "t": 60,}
        bgcolor = '#181818'; graph_colorway = ['#007965', '#FF0000']; graph_title_color = "#f1e658"
        
        index_limit, buy_percent, sell_percent, total_buy_quantity, total_sell_quantity, total_quantity = get_data(int(indicator_value))

        fig_pie = go.Figure(data = [go.Pie(labels = labels, values = values_pie, hole = 0.3)])        
        delta_indicator = {'position': "bottom", 'reference': 320}
        mode_indicator = "number+delta"
        fig_indicator1 = go.Figure(go.Indicator(
            mode = mode_indicator, value = buy_percent, delta = delta_indicator,))
        fig_indicator2 = go.Figure(go.Indicator(
            mode = mode_indicator, value = sell_percent, delta = delta_indicator,))
        fig_indicator3 = go.Figure(go.Indicator(
            mode = mode_indicator, value = round(total_buy_quantity),delta = delta_indicator,))
        fig_indicator4 = go.Figure(go.Indicator(
            mode = mode_indicator,value = round(total_sell_quantity),delta = delta_indicator,))
        fig_indicator5 = go.Figure(go.Indicator(
            mode = mode_indicator,value = round(total_quantity),delta = delta_indicator,))

        fig_pie.update_layout(
            title = f"Volume {pie_value}", title_font_color = graph_title_color, title_font_family = 'Montserrat', title_font_size = 35, margin = graph_margin, paper_bgcolor = bgcolor, colorway = graph_colorway, font = {"color": graph_title_color, "size": 28}, showlegend = False
            )
        fig_indicator1.update_layout(
            title = "Percentage<br>of purchase<br>requests", title_font_color = bgcolor, title_font_family = 'Montserrat', title_font_size = 20, margin = graph_indicator_margin, paper_bgcolor = graph_title_color, colorway = ["#FF0000"], font = {"color": bgcolor}, showlegend = False
            )
        fig_indicator2.update_layout(
            title = "Percentage<br>of purchase<br>requests", title_font_color = bgcolor, title_font_family = 'Montserrat', title_font_size = 20, margin = graph_indicator_margin, paper_bgcolor = graph_title_color, colorway = ["#FF0000"], font = {"color": bgcolor}, showlegend = False
            )
        fig_indicator3.update_layout(
            title = "Volume<br>of buy<br>orders", title_font_color = graph_title_color, title_font_family = 'Montserrat', title_font_size = 20, margin = graph_indicator_margin, paper_bgcolor = bgcolor, colorway = graph_colorway, font = {"color": graph_title_color}, showlegend = False
            )
        fig_indicator4.update_layout(
            title = "Volume<br>of orders<br>for sale", title_font_color = graph_title_color, title_font_family = 'Montserrat', title_font_size = 20, margin = graph_indicator_margin, paper_bgcolor = bgcolor, colorway = graph_colorway, font = {"color": graph_title_color}, showlegend = False
            )
        fig_indicator5.update_layout(
            title = "Total<br>volume of<br>applications", title_font_color = graph_title_color, title_font_family = 'Montserrat', title_font_size = 20, margin = graph_indicator_margin, paper_bgcolor = bgcolor, colorway = graph_colorway, font = {"color": graph_title_color}, showlegend = False
            )

        good_trend, bad_trend = upload_trend(df_1500, df_pie)

        request = engine.execute("""SELECT your_date FROM yourDatabase ORDER BY your_date DESC LIMIT 1""")
        new_time = request.fetchone()
        SYNC = round((round(time.time() + 10800, 3) - (new_time[0] / 1000)), 5)
        SYNC = f'Synchronization - {SYNC} trend - {good_trend}/{bad_trend}'

        return (
            SYNC,
            "Stop",
            fig_pie, fig_indicator1, fig_indicator2, fig_indicator3, fig_indicator4, fig_indicator5,
            {"display": "flex"},
            )


if __name__ == '__main__':
    app.run_server(debug = True)