"""Sending data to the Dashboard."""
import concurrent.futures
import json

import jsons
import requests

from dojo.vis.variables import BlockData


class Plotter:
    """Sending data to the dashboard for plotting."""

    def __init__(self, num_agents=2, port: int = 8051):
        """Initialize a new plotter instance.

        :param port: The port on which the dashboard is running.
        """
        self.port = port
        self.address = "http://0.0.0.0"
        self.headers = {"Content-Type": "application/json"}

    def update_blockdata(self, block: int, blockdata: BlockData):
        """Update date for a particular simulation block."""
        URL = f"{self.address}:{self.port}/blockdata"
        payload = {"block": block, "data": jsons.dump(blockdata)}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.send_post, *["POST", URL, self.headers, payload])

    def send_post(self, method: str, url: str, headers: dict, payload: str):
        """Helper function."""
        requests.request(method, url, headers=headers, data=json.dumps(payload))

    def send_progress(self, progress: int):
        """Send progress to the dashboard."""
        URL = f"{self.address}:{self.port}/progress"
        payload = {"progress": progress}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.send_post, *["POST", URL, self.headers, payload])

    def send_info(self, info: dict):
        """Send info to the dashboard."""
        URL = f"{self.address}:{self.port}/info"
        payload = info
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.send_post, *["POST", URL, self.headers, payload])
