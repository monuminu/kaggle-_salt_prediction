# -*- coding: utf-8 -*-
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests

from data import *

fig = make_subplots(
    rows=5, cols=6,horizontal_spacing = 0.05,vertical_spacing = 0.01,
    specs=[
        [{"type": "indicator"},None, {"type": "indicator"},{"type": "bar","rowspan" : 2, "colspan": 3}, None,None],
        [{"type": "Table", "rowspan" : 2, "colspan" : 3}, None, None, None, None, None],
        [None, None, None, {"type": "bar","rowspan" : 2, "colspan": 3}, None, None],        
        [{"type": "Table", "rowspan" : 2, "colspan" : 3}, None, None, {"type": "bar","rowspan" : 2, "colspan": 3}, None, None],
        [None, None, None, None, None, None]
    ]
)

fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_deposit,
        title="Total Deposit",
    ),
    row=1, col=1
)

fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_withdrawl,
        title="Total Withdrawl",
    ),
    row=1, col=3
)

fig.add_trace(
    go.Bar(
        name = "Debit", x=df_deposit_withdrawl["Txn Date"], y=df_deposit_withdrawl["Debit"],marker=dict(color="Red"),showlegend=True),
        row=1, col=4
)

fig.add_trace(
    go.Bar(
        name = "Credit", x=df_deposit_withdrawl["Txn Date"], y=df_deposit_withdrawl["Credit"],marker=dict(color="Green"),showlegend=True),
        row=1, col=4
)


fig.add_trace(
    go.Line(
        name = "Balance", x=df_balance["Txn Date"], y=df_balance["Balance"],marker=dict(color="Blue"),showlegend=True),
        row=4, col=4
)



fig.add_trace(
    go.Table(
            columnwidth=[0.8, 0.47, 0.48, 0.60],
            header=dict(                
                values=['Txn Date', 'Debit(D)', 'Credit(C)', 'Gross Income(C - D)'],
                fill = dict(color='#C2D4FF'),
            ),
            cells=dict(
                values=[df_deposit_withdrawl[k].tolist() for k in df_deposit_withdrawl.columns],
                format = [None, '.2f', '.2f', '.2f'],
            ),
        
    ),
        row=2, col=1
)

fig.add_trace(
    go.Table(
            columnwidth=[0.8, 0.47],
            header=dict(                
                values=['Month', 'Balance'],
                fill = dict(color='#C2D4FF'),
            ),
            cells=dict(
                values=[df_balance_monthly[k].tolist() for k in df_balance_monthly.columns],
                #format = [None, '.2f'],
            ),
        
    ),
        row=4, col=1
)

fig.update_layout(
    template="simple_white",
    title="AI Enabled Bank Statement Analysis",
    showlegend=True,
    legend_orientation="h",
    legend=dict(x=0.8, y=0.9),
    annotations=[
        dict(
            text="",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.35,
            y=0)
    ]
)

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(style={'textAlign': 'Center'},  children=[

    dcc.Graph(
        style={"height": "100vh"},
        figure=fig,
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)