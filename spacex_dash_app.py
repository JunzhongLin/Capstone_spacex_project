# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("./data_from_course/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'ALL sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    ],
                                    value='ALL',
                                    placeholder='Select a Launch Site here: ',
                                    searchable=True,
                                    style={'width': '80%',
                                           'padding': '3px', 'font-size': '20px',
                                           'text-align-last': 'center'},

                                ),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Br(),

                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, max=10000, step=100,
                                    marks={
                                        0: {'label': 0, 'style':         {'font-size': '20px'}},
                                        2500: {'label': 2500, 'style':   {'font-size': '20px'}},
                                        5000: {'label': 5000, 'style':   {'font-size': '20px'}},
                                        7500: {'label': 7500, 'style':   {'font-size': '20px'}},
                                        10000: {'label': 10000, 'style': {'font-size': '20px'}},
                                    },
                                    value=[min_payload, max_payload]
                                ),

                                html.Br(),
                                html.Br(),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    [
        Output(component_id='success-pie-chart', component_property='figure'),
     ],
    [
        Input(component_id='site-dropdown', component_property='value'),
     ]
)
def get_graph(launch_site):

    if launch_site == 'ALL':
        pie_data = spacex_df.groupby(['Launch Site']).count()['class'].reset_index()
        # pie_data = spacex_df.groupby(['class'])['class'].count().reset_index(name='counts')
        pie_fig = px.pie(pie_data, values='class', names='Launch Site',
                         title='total success launches by Sites')
    else:
        pie_data = spacex_df[spacex_df['Launch Site'] == launch_site].groupby(['class'])['class'].count().\
          reset_index(name='counts')

        pie_fig = px.pie(pie_data, values='counts', names='class',
                         title='total success launches for {}'.format(launch_site))

    return [pie_fig]

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    [
        Output(component_id='success-payload-scatter-chart', component_property='figure'),
     ],
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value'),
     ]
)
def get_graph_cat(launch_site, payload):

    if launch_site == 'ALL':
        # cat_data = spacex_df.groupby(['Launch Site']).count()['class'].reset_index()
        # pie_data = spacex_df.groupby(['class'])['class'].count().reset_index(name='counts')
        cat_data = spacex_df[
            (spacex_df['Payload Mass (kg)'] < payload[1]) & (spacex_df['Payload Mass (kg)'] > payload[0])
        ]
        success_rate = cat_data['class'].mean()
        cat_fig = px.scatter(cat_data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                             title='correlation between payload and '
                                   'success for all sites (sucess rate= {})'.format(success_rate))
    else:
        cat_data = spacex_df[spacex_df['Launch Site'] == launch_site][
            (spacex_df['Payload Mass (kg)'] < payload[1]) & (spacex_df['Payload Mass (kg)'] > payload[0])
        ]
        success_rate = cat_data['class'].mean()
        cat_fig = px.scatter(cat_data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                             title='correlation between payload and '
                                   'success for site: {}, success_rate={}'.format(launch_site, success_rate))

    return [cat_fig]

# Run the app
if __name__ == '__main__':
    app.run_server()
