### Now my take on a dash app

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.tools as tls
import pandas as  pd
import getData 

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


ds = getData.handle_ds(getData.prepare_data()).sort_values("group_id")
bySprint = ds.groupby(ds.group_id)["Estimado","Realizado"].sum()
app = dash.Dash("Going2 Power !")

server = app.server

app.layout = html.Div([
    html.Div([
        html.H2("Going 2 Power Up!"),
    ], style={
            'textAlign': 'center',
            'color': colors['text']
        }),
    html.Div([
        html.Div(children="Team Speed ", style={
            'textAlign': 'center',
            'color': colors['text']
            }
        ),
        html.Div([
            dcc.Graph(
                id='team_speed',
                figure = go.Figure(
                    data=[
                        go.Bar(
                            x=ds["group_id"].unique(),
                            y= bySprint["Estimado"],
                            name = "Estimado"
                        ),
                        go.Bar(
                            x=ds["group_id"].unique(),
                            y=bySprint["Realizado"],
                            name = "Realizado"
                        )
                    ],
                    layout=go.Layout(
                    title='Estimativa geral por Sprint',
                    showlegend=True,
                    legend=go.Legend(
                    x=0,
                    y=1.0
            ),
            margin=go.Margin(l=40, r=0, t=40, b=30)
        )

                )
            ),
        ], className='teamSpeed'),
        dcc.Interval(id='wind-speed-update', interval=1000, n_intervals=0),
    ], className='row wind-speed-row'),

], style={'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "900px",
          'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}

)

if __name__ == '__main__':
    app.run_server()