"""Callbacks for the dashboard."""
import base64
import json
from enum import Enum

import jsons
import plotly.io as pio
from dash import Dash
from dash.dependencies import Input, Output
from dateutil import parser as dateparser

from dojo.vis import variables
from dojo.vis.graphs import positions_graph, price_graph, reward_graph

ActionType = Enum("ActionType", ["Trade", "Quote"])


pio.templates.default = "plotly_dark"


def register_interactions(app: Dash):
    """Helper function."""

    @app.callback(
        Output("download-csv", "data"),
        Input("button-save", "n_clicks"),
        prevent_initial_call=True,
    )
    def save_data(clickData):
        return dict(
            content=jsons.dumps(
                {
                    "params": variables.params.__dict__,
                    "data": jsons.dump(variables.data),
                },
                indent=2,
            ),
            filename="dojo.json",
        )

    @app.callback(
        Output("file_upload_success_modal", "is_open", allow_duplicate=True),
        Input("button-load", "n_clicks"),
        prevent_initial_call=True,
    )
    def open_modal(n_clicks):
        return True

    @app.callback(
        Output("file_upload_success_modal", "is_open", allow_duplicate=True),
        Input("upload-data", "contents"),
        prevent_initial_call=True,
    )
    def update_output(contents):
        json_string = contents.split(",")[1]
        decoded_data = base64.b64decode(json_string)
        json_object = json.loads(decoded_data)
        variables.reset()
        for key in json_object["data"].keys():
            variables.data[key] = jsons.load(
                json_object["data"][key], variables.BlockData
            )
        variables.params.token0 = json_object["params"]["token0"]
        variables.params.token1 = json_object["params"]["token1"]
        variables.params.pool = json_object["params"]["pool"]
        variables.params.pool_fee = float(json_object["params"]["pool_fee"])
        variables.params.progress_value = float(json_object["params"]["progress_value"])
        variables.params.start_date = dateparser.parse(
            json_object["params"]["start_date"]
        )
        variables.params.end_date = dateparser.parse(json_object["params"]["end_date"])
        return False

    @app.callback(
        [Output("click-data", "children"), Output("inspector-modal", "is_open")],
        Input("live-update-graph", "clickData"),
    )
    def display_click_data(clickData):
        return json.dumps(clickData, indent=2), clickData is not None

    @app.callback(
        Output("interval-component", "n_intervals"),
        Input("button-reset", "n_clicks"),
    )
    def reset_dashboard(a):
        if variables.is_dev:
            variables.dummydata()
        else:
            variables.reset()
        return 0

    # Define the callback function to update the plot
    @app.callback(
        [
            Output("live-update-graph", "figure"),
            Output("graph-price", "figure"),
            Output("positions-graph", "figure"),
            Output("progress-bar", "value"),
            Output("info-start-date", "children"),
            Output("info-end-date", "children"),
            Output("info-pool", "href"),
            Output("info-tokens", "children"),
            Output("info-num-agents", "children"),
        ],
        [Input("interval-component", "n_intervals")],
        prevent_initial_call=True,
    )
    def update_graph(n):
        """Refresh the graph.

        :param n: Unused parameter.
        """
        fig_rewards = reward_graph()
        fig_price = price_graph()

        fig_liquidities = positions_graph()

        # data = copy.copy(variables.data)
        # table_data = []  # [
        #     {
        #         "block": block,
        #         "reward": block_data.rewards[1],
        #         "actions": "<br>".join(
        #             [f"{action.type}: {action.info}" for action in block_data.actions]
        #         ),
        #     }
        #     for block, block_data in data.items()
        # ]
        progress = variables.params.progress_value
        return (
            fig_rewards,
            fig_price,
            fig_liquidities,
            progress,
            f"{variables.params.start_date}",
            f"{variables.params.end_date}",
            f"https://info.uniswap.org/#/pools/{variables.params.pool}",
            f"{variables.params.token0} - {variables.params.token1} {variables.params.pool_fee*100}%",
            f"{variables.params.num_agents}",
        )

    return app
