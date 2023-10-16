import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_cytoscape as cyto

from dotenv import load_dotenv, find_dotenv


from pygraphgpt.domain.utils import (
    format_nested_list_to_cytoscape,
    load_json,
    parse_gpt_response_to_relations
)

from pygraphgpt.domain.graph import find_relations
from pygraphgpt.controller.constants import PATH_CYTO_STYLE_CONFIG

load_dotenv(find_dotenv())


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
stylesheet = load_json(PATH_CYTO_STYLE_CONFIG)


cyto_layout = html.Div(
            [
                cyto.Cytoscape(
                    id='cytoscape-responsive-layout',
                    stylesheet=stylesheet,
                    style={'width': '100%', 'height': '1000px'},
                    layout={
                        'name': 'cose'
                    }
                )
            ],
            id="div",
            style={"display": "block", 'width': '100%', 'height': '1000px'}
        )


result_panel = html.Div(dbc.Tabs([
        dbc.Tab(cyto_layout, label='Graph'),
        dbc.Tab([
                    html.Br(),
                    html.Code("...", id="raw_output")],
                    label='Raw')
    ]))

app.layout = html.Div([
    dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            html.Br(), html.Br(),
            dbc.Label('Paste a text:'),
            dbc.Textarea(id='user_text', rows=15), html.Br(),
            dbc.Button('Extract graph', id='submit_button'), html.Br(),html.Br(),html.Br(),
            dcc.Loading(html.Div(id='output')),
            result_panel
        ] + [html.Br() for i in range(15)], lg=10)
    ])
])

default_openai_responses = """[['Obi Wan Kenobi', 'Mentor', 'Anakin Skywalker'],
 ['Obi Wan Kenobi', 'Mentor', 'Luke Skywalker'],
 ['Darth Vader', 'Formerly', 'Anakin Skywalker'],
 ['Darth Vader', 'Father', 'Luke'],
 ['Darth Vader', 'Father', 'Leia'],
 ['Yoda', 'Teacher', 'Luke']]"""

@app.callback(
    [
        Output("cytoscape-responsive-layout", "elements"),
        Output('raw_output', 'children')
    ],
    [
        Input('submit_button', 'n_clicks'),
        Input('user_text', 'value')
     ], prevent_initial_call=True)
def extract_entities(n_clicks, user_text):
    if not n_clicks:
        raise PreventUpdate
    openai_responses = default_openai_responses
    #openai_responses = find_relations(user_text)
    relations = parse_gpt_response_to_relations(openai_responses)
    relations_cyto = format_nested_list_to_cytoscape(relations)
    return relations_cyto, f"{relations}"


def start():
    app.run_server(debug=True)


if __name__ == "__main__":
    app.run_server(debug=True)
