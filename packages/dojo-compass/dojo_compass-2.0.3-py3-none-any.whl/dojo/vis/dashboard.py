"""Dashboard to visualize simulation."""
import logging
import webbrowser
from enum import Enum
from threading import Timer

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from flask import Flask
from waitress import serve

from dojo.vis import variables
from dojo.vis.dashboard_api import register_api
from dojo.vis.dashboard_interactions import register_interactions

ActionType = Enum("ActionType", ["Trade", "Quote"])


def run_app(debug: bool = False, port: int = 8051, jupyter=False):
    """Start the dashboard.

    :param debug: True only for development purposes. Won't work in production.
    :param port: The port on which the dashboard is running. The plotter must send data
        to this port.
    :param jupyter: Set this to true if you want to run the dashboard inline within a
        Jupyter notebook.
    :raises ValueError: Temporarily removed Jupyter support.
    """

    def open_browser():
        webbrowser.open_new("http://0.0.0.0:{}".format(port))

    # Initialize the Flask application
    server = Flask(__name__)
    server = register_api(server)

    # Initialize the Dash application

    if jupyter is True:
        raise ValueError("Jupyter support has been removed(for now).")
    else:
        app = dash.Dash(
            __name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
    app.title = "dojo"
    app._favicon = "logo.svg"

    buttons_bar = dbc.Row(
        [
            dbc.Col(
                dbc.Button(
                    "Load",
                    color="secondary",
                    className="mybutton",
                    n_clicks=0,
                    id="button-load",
                ),
                width="auto",
            ),
            dbc.Col(
                dbc.Button(
                    "Save",
                    color="secondary",
                    className="mybutton",
                    n_clicks=0,
                    id="button-save",
                ),
                width="auto",
            ),
            dbc.Col(
                dbc.Button(
                    "Reset",
                    color="secondary",
                    className="mybutton",
                    n_clicks=0,
                    id="button-reset",
                ),
                width="auto",
            ),
        ],
        className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
        # align="right",
    )

    file_upload_success_modal = dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle("Choose the .json data file"),
                style={"background": "#1e1c2d"},
            ),
            dbc.ModalBody(
                [
                    html.P(
                        "Please be aware that data files created in older version of dojo might not load correctly."
                    ),
                    dcc.Upload(
                        id="upload-data",
                        children=html.Div(["Drag and Drop or ", html.A("Select File")]),
                        style={
                            "width": "100%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "margin": "10px",
                        },
                        # Allow multiple files to be uploaded
                        multiple=False,
                    ),
                ],
                style={"background": "#1e1c2d"},
            ),
        ],
        id="file_upload_success_modal",
        is_open=False,
    )

    navbar = dbc.Container(
        [
            dbc.Navbar(
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.A(
                                            # Use row and col to control vertical alignment of logo / brand
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        html.Img(
                                                            src="/assets/logo.svg",
                                                            height="50px",
                                                        ),
                                                        className="no_borders",
                                                    ),
                                                    dbc.Col(
                                                        dbc.NavbarBrand(
                                                            "Dojo Simulation Dashboard",
                                                            className="display-1 ms-2 h4",
                                                            style={
                                                                # "color": "#ff0000",
                                                                "font-size": "2rem",
                                                                "font-weight": "bold",
                                                            },
                                                        ),
                                                        className="no_borders h-4",
                                                    ),
                                                ],
                                                align="center",
                                                className="g-0",
                                            ),
                                            href="https://dojo.compasslabs.ai",
                                            style={"textDecoration": "none"},
                                        )
                                    ],
                                    width="auto",
                                ),
                                dbc.Col(
                                    [
                                        dbc.NavbarToggler(
                                            id="navbar-toggler", n_clicks=0
                                        ),
                                        dbc.Collapse(
                                            buttons_bar,
                                            id="navbar-collapse",
                                            is_open=False,
                                            navbar=True,
                                        ),
                                    ],
                                    width="auto",
                                ),
                                # dcc.Markdown("---")
                            ],
                            justify="between",
                        ),
                        # dcc.Markdown("---"),
                    ]
                ),
                # color="dark",
                # className="global-nav-card",
                dark=True,
                sticky="top"
                # style={"border-left": "None", "border-right": "None", "margin-left": "unset"},
            )
        ]
    )

    # data_table = dash.dash_table.DataTable(
    #     id="live-update-table",
    #     columns=[
    #         {"name": "block", "id": "block"},
    #         {"name": "reward", "id": "reward"},
    #         {"name": "actions", "id": "actions"},
    #     ],
    #     data=[
    #         {"block": 0, "reward": 0},
    #         {"block": 1, "reward": 1},
    #     ],
    #     page_size=10,
    # )

    # Create the layout of the dashboard
    app.layout = dbc.Container(
        [
            dcc.Download(id="download-csv"),
            dcc.Upload(id="upload-csv"),
            file_upload_success_modal,
            dcc.Store(id="data"),
            navbar,
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H6("Start Date"),
                                    dcc.Markdown(
                                        f"{variables.params.start_date}",
                                        id="info-start-date",
                                    ),
                                ]
                            ),
                            dbc.Col(
                                [
                                    html.H6("End Date"),
                                    dcc.Markdown(
                                        f"{variables.params.end_date}",
                                        id="info-end-date",
                                    ),
                                ]
                            ),
                            dbc.Col(
                                [
                                    html.H6("Pool"),
                                    dcc.Link(
                                        children=dcc.Markdown(
                                            f"{variables.params.token0} - {variables.params.token1} {variables.params.pool_fee*100}%",
                                            id="info-tokens",
                                        ),
                                        href=f"https://info.uniswap.org/#/pools/{variables.params.pool}",
                                        id="info-pool",
                                    ),
                                ]
                            ),
                            dbc.Col(
                                [
                                    html.H6("# Agents"),
                                    dcc.Markdown(
                                        f"{variables.params.num_agents}",
                                        id="info-num-agents",
                                    ),
                                ]
                            ),
                        ],
                        className="global-nav-card",
                    )
                ]
            ),
            dbc.Container(
                [
                    dbc.Col(
                        [
                            dbc.Progress(
                                label="Progress",
                                value=50,
                                id="progress-bar",
                                color="linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(9,9,121,1) 35%, rgba(0,212,255,1) 100%)",
                                # style={'background-color': '#ff0000'}
                            )
                        ],
                        style={"padding": "0px 0px 0px"},
                    ),
                    # dbc.
                ],
                className="global-nav-card",
            ),
            dbc.Container(
                [
                    dbc.Tabs(
                        [
                            dbc.Tab(
                                children=[
                                    html.P(" "),
                                    html.P(
                                        "This graph shows your agents reward over time",
                                        className="mt-2",
                                    ),
                                    dcc.Markdown(
                                        "**The Solid line** shows the reward value."
                                    ),
                                    dcc.Markdown(
                                        "**Dots** indicate blocks where your agent took actions. Hover over the dots to get more info."
                                    ),
                                    dcc.Graph(id="live-update-graph"),
                                ],
                                label="Reward graph",
                                label_style={"color": "#FF67C3"},
                                active_label_style={
                                    "color": "#FF67C3",
                                    "background-color": "rgba(255,255,255,0.1)",
                                },
                                style=dict(background="transparent"),
                            ),
                            dbc.Tab(
                                children=[
                                    html.P(" "),
                                    html.P(
                                        "This graph shows your positions in both tokens over time.",
                                        className="mt-2",
                                    ),
                                    # dbc.Container(
                                    #     [
                                    #         # dcc.Markdown('**Tokens:**  '),
                                    #         dcc.Markdown(
                                    #             f"**USDC{variables.params.token0}**", className="token0"
                                    #         ),
                                    #         dcc.Markdown(
                                    #             "**-**", style={"font-size": "1.5rem"}
                                    #         ),
                                    #         dcc.Markdown(
                                    #             "**WETH**", className="token1"
                                    #         ),
                                    #     ],
                                    #     className="center flex-h",
                                    # ),
                                    dcc.Graph(id="positions-graph"),
                                ],
                                label="Positions graph",
                                label_style={"color": "#FF67C3"},
                                active_label_style={
                                    "color": "#FF67C3",
                                    "background-color": "rgba(255,255,255,0.1)",
                                },
                            ),
                            dbc.Tab(
                                children=[
                                    html.P(" "),
                                    html.P(
                                        "This graph shows the token price as well as the total liquidity in the pool.",
                                        className="mt-2",
                                    ),
                                    dcc.Graph(id="graph-price"),
                                ],
                                label="Pool stats",
                                label_style={"color": "#FF67C3"},
                                active_label_style={
                                    "color": "#FF67C3",
                                    "background-color": "rgba(255,255,255,0.1)",
                                },
                            ),
                        ],
                        active_tab="tab-0",
                    )
                ],
                className="global-nav-card",
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(
                        dbc.ModalTitle("Data for selected block"),
                        style={"background": "#1e1c2d"},
                    ),
                    dbc.ModalBody(
                        html.Pre(id="click-data"), style={"background": "#1e1c2d"}
                    ),
                    # dbc.ModalFooter(
                    #     dbc.Button(
                    #         "Close", id="close", className="ms-auto", n_clicks=0
                    #     )
                    # ),
                ],
                id="inspector-modal",
                is_open=False,
                className="global-nav-card",
            ),
            dcc.Interval(
                id="interval-component",
                interval=2000,  # Refresh interval in milliseconds
                n_intervals=0,
            ),
            # dcc.Markdown("---"),
            dash.html.Footer("© 2023 - CompassLabs", className="center"),
        ],
        # className="mb-100",
        fluid=True,
        # style={"margin-left": "300px"},
    )

    app = register_interactions(app)

    Timer(2, open_browser).start()
    if jupyter is True:
        logging.getLogger("werkzeug").setLevel(logging.ERROR)
        app.run_server(debug=False, mode="inline", port=port)
    else:
        if debug:
            app.run_server(debug=True, port=port)
        else:
            host = "0.0.0.0"
            serve(app.server, host=host, port=port)


if __name__ == "__main__":
    # Run the application
    run_app(debug=True, port=8051)
