import dash
# import dash_breakpoints
from dash import html, dcc, dash_table, Input, Output, callback
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator

selected_roster=1

# Load data from CSV file into Pandas DataFrame and preprocess
df = pd.read_csv(r'fpts_per_salary_all_players.csv')
df2 = pd.read_csv(r'top400_thu_mon_rev2.csv')
df_top_roster = df2.sort_values(by='Tot Exp Pts',ascending=False).head(20)
# Calculate low and high ranges for all positions

df['range_high'] = df['FPTS_high']-df['FPTS']
df['range_low'] = df['FPTS']-df['FPTS_low']

columns = ['Player',
           'Position',
           'Salary',
           'FPTS',
           'range_high',
           'range_low']

df = df[columns]

color_seq = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
pos_list = ["TE","QB","RB","WR","DEF"]
color_map = dict(zip(pos_list,color_seq)) 

df['colors'] = df['Position'].map(color_map)

# Create Roster Maps for Slider
frames={}
for selected_roster in np.arange(0,df_top_roster.shape[0]):
    roster_list = df_top_roster.iloc[selected_roster-1].values.tolist()[1:10]
    df_ = df.copy()
    df_['text'] = df['Player'].map(lambda x: x if x in roster_list else "")
    # df_['text'] = np.where(df_.text !="", df_.text +": "+df_.Position,"")
    df_['size'] = df['Player'].map(lambda x: 3 if x in roster_list else 1)
    # df_['marker'] = df['Player'].map(lambda x: 10 if x in roster_list else 2)
    frames[selected_roster] = df_

# Generate Exposure Data
name_counts = {}
columns_to_iterate = ['WR1', 'WR2', 'WR3','RB1','RB2','FLEX','TE','QB','DST']
for column in columns_to_iterate:
    # Count the occurrences of each name in the current column
    counts = df_top_roster[column].value_counts().to_dict()
    
    # Update the name_counts dictionary with the counts from the current column
    for name, count in counts.items():
        if name in name_counts:
            name_counts[name] += count
        else:
            name_counts[name] = count
    a = {k: v / df_top_roster.shape[0] for k, v in name_counts.items()}
    df_totals = pd.DataFrame(a.items(),columns=['Player','Freq'])
    df_exposure_ = df_totals.sort_values(by=['Freq'],ascending=False)
    df_exposure = df_exposure_.merge(df[["Player","Position","Salary","FPTS"]],left_on="Player",right_on="Player",how="inner")
    df_full_exposure = df_exposure_.merge(df[["Player","Position","Salary","FPTS"]],left_on="Player",right_on="Player",how="outer")
    df_full_exposure['Freq'] = df_full_exposure['Freq'].fillna(0.01)

## Add plotly figures
top_row_bg = "#FFF"

fig1 = px.scatter(df, 
                  x='Salary', y='FPTS', 
                  color='Position',
                  color_discrete_map=color_map,
                     title='Hover to see player details, click on legend to filter positions',
                     error_y="range_high", error_y_minus ="range_low", 
                     trendline="lowess", 
                     hover_name='Player')

fig3 = px.bar(df_exposure, x='Player', y='Freq',
              color="Position",
              hover_data={"Salary":True},
              title="Player Exposure (% rostered in top 20 optimized rosters)",
                          color_discrete_map=color_map)

fig4 = px.scatter(df_full_exposure,
                x='Salary', 
                y='FPTS',
                color='Position',
                trendline='ols',
                color_discrete_map=color_map,
                hover_name='Player',
                size='Freq',
                title="Hover for player details and exposure level")

dash_app = dash.Dash(__name__)
dash_app.config.suppress_callback_exceptions=True
app = dash_app.server


dash_app.layout = html.Div([
    html.H1('Player Selection Dashboard'),
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
        dcc.Tab(label='Expected Pts by Salary', value='tab-1-example-graph'),
        dcc.Tab(label='Top 20 Optimized Rosters', value='tab-2-example-graph'),
        dcc.Tab(label='Player Exposure', value='tab-3-example-graph'),
        dcc.Tab(label='Exposure vs Exp Performance', value='tab-4-example-graph'),
    ]),
    html.Div(id='tabs-content-example-graph')
])


@callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
            html.H3('Expected Fantasy Points by Salary and Position (All Eligible Players)'),
            dcc.Graph(id='graph-2-tabs-dcc',
                figure=fig1,
                style={'height': '70vh'})
        ])
    elif tab == 'tab-2-example-graph':
        return html.Div([
            html.H3('Ranked Optimized Rosters'),
            dcc.Graph(id='graph-with-slider',style={'height': '70vh'}),
            dcc.Slider(
            1,
            20,
            step=1,
            value=1,
            id='roster-slider',
    )
        ])
        
    elif tab == 'tab-3-example-graph':
        return html.Div([
            html.H3('Player Exposure'),
            dcc.Graph(id='graph-3-tabs-dcc',
                figure=fig3,
                style={'height': '70vh'})
        ])

    elif tab == 'tab-4-example-graph':
        return html.Div([
            html.H3('Player Exposure Compared to Predicted Performance (All Players)'),
            dcc.Graph(id='graph-4-tabs-dcc',
                figure=fig4,
                style={'height': '70vh'})
        ])          

@callback(
    Output('graph-with-slider', 'figure'),
    Input('roster-slider', 'value'))
def update_figure(selected_roster):
    fig2 = go.Figure(layout=dict(template='plotly'))
    df_blah = frames[selected_roster]
    df_plot_sml = df_blah.loc[df_blah['size']<3]
    df_plot_lrg = df_blah.loc[df_blah['size']>=3]
    fig2 = px.scatter(df_plot_sml, x='Salary', y='FPTS', color='Position',
                    title='Use Slider to View Additional Lineups<br><sup>Roster#{} {}</sup>'.format(selected_roster,roster_list),
                    text ='text',
                    trendline="ols", 
                    opacity = 0.7,
                    hover_name='Player')
    
    fig2.add_trace(
        go.Scatter(
            visible=True,
            x=df_plot_lrg['Salary'],
            y=df_plot_lrg['FPTS'],
            mode="markers+text",
            marker_size = 30,
            marker_symbol="diamond-tall",
            marker_color = df_plot_lrg['colors'],
            text = df_plot_lrg["text"],
            name="roster picks",
            textposition="bottom center"
        ))
    return fig2


if __name__ == '__main__':
    dash_app.run_server(debug=True)
