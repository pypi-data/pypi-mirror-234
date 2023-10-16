"""Plotly graphs for the dashboard."""
import copy
from enum import Enum

import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots

from dojo.vis import variables

pio.templates["myname"] = go.layout.Template(
    layout=go.Layout(colorway=["#6BD6E3", "#BE97D2", "#FF929C"])
)
pio.templates.default = "myname"


ActionType = Enum("ActionType", ["Trade", "Quote"])

COLORS = ["#BE97D2", "#6BD6E3", "#FEE26C", "#FF929C"]
GLOW_WIDTH = 5
GLOW_COLOR = "rgba(255,255,255,0.1)"


def positions_graph():
    """Plots the current positions of the agent."""
    keys = copy.copy(list(variables.data.keys()))

    # Create figure with secondary y-axis
    subplot_titles = ("wallet agent 1", "LP agent 1", " wallet agent 2", "LP agent 2")

    if not variables.params.num_agents or variables.params.num_agents == 0:
        # return go.Figure()
        variables.params.num_agents = 2

    num_rows = variables.params.num_agents

    fig = make_subplots(
        rows=num_rows,
        cols=2,
        subplot_titles=subplot_titles,
        shared_xaxes=True,
        vertical_spacing=0.1,
        specs=[[{"secondary_y": True}, {"secondary_y": True}]] * num_rows,
    )

    for iagent in range(variables.params.num_agents):
        blocks = [
            i
            for i in keys
            if variables.data[i].agentdata[iagent].liquidities is not None
        ]
        trace_lp_token0 = [
            variables.data[block].agentdata[iagent].liquidities.lp.token0
            for block in blocks
        ]
        trace_lp_token1 = [
            variables.data[block].agentdata[iagent].liquidities.lp.token1
            for block in blocks
        ]
        trace_wallet_token0 = [
            variables.data[block].agentdata[iagent].liquidities.wallet.token0
            for block in blocks
        ]
        trace_wallet_token1 = [
            variables.data[block].agentdata[iagent].liquidities.wallet.token1
            for block in blocks
        ]
        wallet_token0 = go.Scatter(
            x=blocks,
            y=trace_wallet_token0,
            hoverinfo="x+y",
            mode="lines",
            name="wallet token 0",
            line=dict(color=COLORS[0], width=1),
            showlegend=False,
        )
        glow_wallet_token0 = go.Scatter(
            x=blocks,
            y=trace_wallet_token0,
            hoverinfo="skip",
            mode="lines",
            line=dict(color=GLOW_COLOR, width=GLOW_WIDTH),
            showlegend=False,
        )
        lp_token0 = go.Scatter(
            x=blocks,
            y=trace_lp_token0,
            hoverinfo="x+y",
            mode="lines",
            name="lp token 0",
            line=dict(color=COLORS[0], width=1),
            showlegend=False,
        )
        glow_lp_token0 = go.Scatter(
            x=blocks,
            y=trace_lp_token0,
            hoverinfo="skip",
            mode="lines",
            line=dict(color=GLOW_COLOR, width=GLOW_WIDTH),
            showlegend=False,
        )
        wallet_token1 = go.Scatter(
            x=blocks,
            y=trace_wallet_token1,
            hoverinfo="x+y",
            mode="lines",
            name="wallet token 1",
            line=dict(color=COLORS[1], width=1),
            showlegend=False,
        )
        glow_wallet_token1 = go.Scatter(
            x=blocks,
            y=trace_wallet_token1,
            hoverinfo="skip",
            mode="lines",
            line=dict(color=GLOW_COLOR, width=GLOW_WIDTH),
            showlegend=False,
        )
        lp_token1 = go.Scatter(
            x=blocks,
            y=trace_lp_token1,
            hoverinfo="x+y",
            mode="lines",
            name="lp token 1",
            line=dict(color=COLORS[1], width=1),
            showlegend=False,
        )
        glow_lp_token1 = go.Scatter(
            x=blocks,
            y=trace_lp_token1,
            hoverinfo="skip",
            mode="lines",
            line=dict(color=GLOW_COLOR, width=GLOW_WIDTH),
            showlegend=False,
        )

        fig.add_trace(wallet_token0, row=iagent + 1, col=1)
        fig.add_trace(glow_wallet_token0, row=iagent + 1, col=1)

        fig.add_trace(wallet_token1, row=iagent + 1, col=1, secondary_y=True)
        fig.add_trace(glow_wallet_token1, row=iagent + 1, col=1, secondary_y=True)

        fig.add_trace(lp_token0, row=iagent + 1, col=2)
        fig.add_trace(glow_lp_token0, row=iagent + 1, col=2)

        fig.add_trace(lp_token1, row=iagent + 1, col=2, secondary_y=True)
        fig.add_trace(glow_lp_token1, row=iagent + 1, col=2, secondary_y=True)
        fig.update_yaxes(
            row=iagent + 1,
            col=1,
            secondary_y=False,
            title=f"{variables.params.token0}",
            title_font_color=COLORS[0],
        )
        fig.update_yaxes(
            row=iagent + 1,
            col=1,
            secondary_y=True,
            title=f"{variables.params.token1}",
            title_font_color=COLORS[1],
        )
        fig.update_yaxes(
            row=iagent + 1,
            col=2,
            secondary_y=False,
            title=f"{variables.params.token0}",
            title_font_color=COLORS[0],
        )
        fig.update_yaxes(
            row=iagent + 1,
            col=2,
            secondary_y=True,
            title=f"{variables.params.token1}",
            title_font_color=COLORS[1],
        )

        fig.update_yaxes(row=iagent + 1, col=1, spikemode="across")
        fig.update_yaxes(row=iagent + 1, col=2, spikemode="across")

        fig.update_xaxes(row=variables.params.num_agents, col=1, title="block")
        fig.update_xaxes(row=variables.params.num_agents, col=2, title="block")

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=400 * variables.params.num_agents,
        hovermode="x",
    )
    fig.update_layout(font_family="Quicksand")
    return fig


def reward_graph():
    """Plot reward graph."""

    def actions2string(block, actions):
        result = f"BLOCK: {block}<br>"
        result += "ACTIONS:<br>"
        for action in actions:
            result += f" {action.type}: {action.info}"
        return result

    blocks = sorted(list(variables.data.keys()))

    num_rows = variables.params.num_agents if variables.params.num_agents > 0 else 1

    fig = make_subplots(
        rows=num_rows,
        cols=1,
        subplot_titles=[f"agent {i+1}" for i in range(num_rows)],
        shared_xaxes=True,
        vertical_spacing=0.1,
        specs=[[{"secondary_y": True}]] * num_rows,
    )

    prices = [variables.data[block].pooldata.price for block in blocks]
    trace_price = go.Scatter(
        x=blocks,
        y=prices,
        name="price",
        hoverinfo="text",
        hovertext=[f"Price: {price}" for price in prices],
        mode="lines",
        line=dict(color=COLORS[1], dash="dot", width=1),
    )

    for iagent in range(variables.params.num_agents):
        y0 = [variables.data[block].agentdata[iagent].reward for block in blocks]

        trace = go.Scatter(
            x=blocks,
            y=y0,
            hoverinfo="skip",
            showlegend=False,
            mode="lines",
            line=dict(color=GLOW_COLOR, width=GLOW_WIDTH),
        )
        fig.add_trace(trace, row=iagent + 1, col=1)

        trace = go.Scatter(
            x=blocks,
            y=y0,
            name="reward",
            hoverinfo="text",
            showlegend=True,
            hovertext=[
                f"BLOCK {block}<br>REWARD {round(variables.data[block].agentdata[iagent].reward,3)}"
                for block in blocks
            ],
            mode="lines",
            line=dict(color=COLORS[0], width=1),
        )
        fig.add_trace(trace, row=iagent + 1, col=1)
        blocks_with_actions = [
            block
            for block in blocks
            if len(variables.data[block].agentdata[iagent].actions) > 0
        ]
        trace_actions = go.Scatter(
            x=blocks_with_actions,
            y=[
                variables.data[block].agentdata[iagent].reward
                for block in blocks_with_actions
            ],
            mode="markers",
            hoverinfo="text",
            marker=dict(
                size=8,
                color=COLORS[0],
                line=dict(width=2, color="rgba(255,255,255,0.2)"),
            ),
            name="actions",
            hovertext=[
                actions2string(block, variables.data[block].agentdata[iagent].actions)
                for block in blocks_with_actions
            ],
            showlegend=False,
        )
        fig.add_trace(trace_actions, row=iagent + 1, col=1)
        fig.add_trace(trace_price, row=iagent + 1, col=1, secondary_y=True)

    names = set()
    fig.for_each_trace(
        lambda trace: trace.update(showlegend=False)
        if (trace.name in names)
        else names.add(trace.name)
    )

    # for itrace, trace in enumerate(traces):
    #     fig.add_trace(trace, row=itrace + 1, col=1)
    # fig = go.Figure(data=traces, layout=layout)
    fig.update_layout(
        yaxis=dict(title="reward"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=400 * num_rows,  # TODO
    )

    fig.update_xaxes(
        title_text="block number",
        row=variables.params.num_agents,
        col=1,
    )

    for i in range(num_rows):
        fig.update_xaxes(row=i + 1, col=1, matches="x2")
        fig.update_yaxes(row=i + 1, col=1, title="price", secondary_y=True)
    fig.update_layout(hovermode="x")
    fig.update_layout(font_family="Quicksand")
    return fig


def price_graph():
    """Plot price graph."""
    blocks = sorted(list(variables.data.keys()))
    prices = [variables.data[block].pooldata.price for block in blocks]
    liquidities = [variables.data[block].pooldata.liquidity for block in blocks]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    trace1 = go.Scatter(
        x=blocks,
        y=prices,
        name="price",
        hoverinfo="text",
        hovertext=[f"Price: {price}" for price in prices],
        mode="lines",
        line=dict(color=COLORS[0], width=1),
    )
    glow_trace1 = go.Scatter(
        x=blocks,
        y=prices,
        hoverinfo="skip",
        mode="lines",
        line=dict(color=GLOW_COLOR, width=GLOW_WIDTH),
        showlegend=False,
    )
    trace2 = go.Scatter(
        x=blocks,
        y=liquidities,
        name="total liquidity",
        hoverinfo="text",
        hovertext=[f"Liquidity: {liquidity}" for liquidity in liquidities],
        mode="lines",
        line=dict(color=COLORS[1], width=1),
    )
    glow_trace2 = go.Scatter(
        x=blocks,
        y=liquidities,
        hoverinfo="skip",
        mode="lines",
        line=dict(color=GLOW_COLOR, width=GLOW_WIDTH),
        showlegend=False,
    )
    fig.add_trace(trace1, secondary_y=False)
    fig.add_trace(trace2, secondary_y=True)
    fig.add_trace(glow_trace1, secondary_y=False)
    fig.add_trace(glow_trace2, secondary_y=True)
    fig.update_layout(
        xaxis=dict(title="block"),
        yaxis=dict(
            title=f"price {variables.params.token1} in {variables.params.token0}"
        ),
        yaxis2=dict(title="total pool liquidity"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(font_family="Quicksand")
    return fig
