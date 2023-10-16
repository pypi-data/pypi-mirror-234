"""Dashboard to visualize simulation."""

import jsons
from flask import request
from flask.app import Flask

from dojo.vis import variables


def register_api(server: Flask) -> Flask:
    """Helper function."""

    @server.route("/info", methods=["POST"])
    def update_info():
        """API endpoint."""
        post_data = request.get_json()
        if "num_agents" in post_data:
            variables.params.num_agents = post_data["num_agents"]
        if "start_date" in post_data:
            variables.params.start_date = post_data["start_date"]
        if "end_date" in post_data:
            variables.params.end_date = post_data["end_date"]
        if "pool" in post_data:
            variables.params.pool = post_data["pool"]
        if "token0" in post_data:
            variables.params.token0 = post_data["token0"]
        if "token1" in post_data:
            variables.params.token1 = post_data["token1"]
        if "pool_fee" in post_data:
            variables.params.pool_fee = float(post_data["pool_fee"])
        if "num_agents" in post_data:
            variables.params.num_agents = int(post_data["num_agents"])

        return "Info updated successfully"

    @server.route("/progress", methods=["POST"])
    def update_progress():
        """API endpoint."""
        new_data = request.get_json()
        variables.params.progress_value = new_data["progress"]
        return "Progress updates successfully"

    @server.route("/blockdata", methods=["POST"])
    def update_blockdata():
        post_data = request.get_json()
        blockdata = jsons.load(post_data["data"], variables.BlockData)
        block = int(post_data["block"])

        variables.data[block] = blockdata

        return "Blockdata updated successfully"

    return server
