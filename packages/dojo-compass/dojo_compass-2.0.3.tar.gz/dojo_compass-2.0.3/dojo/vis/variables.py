"""Global variables for the dashboard."""
import copy
import datetime
import random
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Union

from dojo.environments.uniswapV3 import UniV3ActionType


def random_continue(value):
    """TODO."""
    return value * 0.5 + value * (1.0 - (random.random() - 0.5)) * 0.5


@dataclass
class Action:
    """Holds information about taken actions."""

    type: UniV3ActionType
    info: str = None

    __annotations__ = {"type": UniV3ActionType, "info": str}


@dataclass
class Portfolio:
    """Holds information about an agents portfolio."""

    token0: float
    token1: float

    __annotations__ = {"token0": float, "token1": float}


@dataclass
class Liquidities:
    """Holds the wallet as well as the LP portfolio."""

    lp: Portfolio
    wallet: Portfolio

    __annotations__ = {"lp": Portfolio, "wallet": Portfolio}


@dataclass
class PoolData:
    """TODO."""

    price: Union[float, None]
    liquidity: Union[int, None]
    __annotations__ = {"price": Union[float, None], "liquidity": Union[int, None]}


@dataclass
class AgentData:
    """TODO."""

    reward: Union[float, None]
    actions: Union[List[Action], None]
    liquidities: Union[Liquidities, None]
    __annotations__ = {
        "reward": Union[float, None],
        "actions": Union[List[Action], None],
        "liquidities": Union[Liquidities, None],
    }


@dataclass
class BlockData:
    """Per block data."""

    pooldata: PoolData
    agentdata: List[AgentData]
    __annotations__ = {"pooldata": PoolData, "agentdata": List[AgentData]}


@dataclass
class Params:
    """Simulation params."""

    progress_value: Union[float, None]
    num_agents: Union[int, None]
    pool: Union[str, None]
    start_date: Union[datetime.datetime, None]
    end_date: Union[datetime.datetime, None]
    token0: Union[str, None]
    token1: Union[str, None]
    pool_fee: Union[float, None]

    __annotations__ = {
        "progress_value": Union[float, None],
        "num_agents": Union[int, None],
        "pool": Union[str, None],
        "start_date": Union[datetime.datetime, None],
        "end_date": Union[datetime.datetime, None],
        "token0": Union[str, None],
        "token1": Union[str, None],
        "pool_fee": Union[float, None],
    }


def _def_value_data():
    """Helper function."""
    pooldata = PoolData(price=None, liquidity=None)
    agentdata = AgentData(reward=None, actions=[], liquidities=None)
    return BlockData(pooldata=pooldata, agentdata=agentdata)


def _def_value_params():
    """Helper function."""
    return Params(
        progress_value=None,
        num_agents=0,
        pool=None,
        start_date=None,
        end_date=None,
        token0=None,
        token1=None,
        pool_fee=None,
    )


data = defaultdict(_def_value_data)
params = Params(
    progress_value=50,
    num_agents=2,
    pool=None,
    start_date=datetime.datetime(1900, 1, 1),
    end_date=datetime.datetime(1900, 1, 20),
    token0=None,
    token1=None,
    pool_fee=0.0,
)

is_dev = False


def reset():
    """Set back all variables to initial state."""
    global data, params
    data = defaultdict(_def_value_data)
    params = Params(
        progress_value=None,
        num_agents=0,
        pool=None,
        start_date=None,
        end_date=None,
        token0=None,
        token1=None,
        pool_fee=0.0,
    )


def dummydata():
    """TODO."""
    global data, params

    # action = UniV3Action(
    #     agent="0x0",
    #     type="trade",
    #     pool="0xpool",
    #     quantities=(Decimal("2000"), Decimal("1")),
    #     liquidity=10000,
    #     tick_range=(3000, 4000),
    #     owner="0x0",
    # )

    d0 = BlockData(
        pooldata=PoolData(price=2000, liquidity=10e6),
        agentdata=[
            AgentData(
                reward=10000,
                actions=[],
                liquidities=Liquidities(
                    lp=Portfolio(token0=2000.0, token1=1.0),
                    wallet=Portfolio(token0=2000.0, token1=1.0),
                ),
            ),
            AgentData(
                reward=10000,
                actions=[],
                liquidities=Liquidities(
                    lp=Portfolio(token0=2000.0, token1=1.0),
                    wallet=Portfolio(token0=2000.0, token1=1.0),
                ),
            ),
        ],
    )
    data = defaultdict(_def_value_data)
    START = 0
    data[START] = d0
    for i in range(START + 1, START + 100):
        dnew = copy.deepcopy(data[i - 1])
        dnew.pooldata.price = random_continue(dnew.pooldata.price)
        dnew.pooldata.liquidity = random_continue(dnew.pooldata.liquidity)
        dnew.agentdata[0].reward = random_continue(dnew.agentdata[0].reward)
        dnew.agentdata[1].reward = random_continue(dnew.agentdata[1].reward)

        dnew.agentdata[0].liquidities.lp.token0 = random_continue(
            dnew.agentdata[0].liquidities.lp.token0
        )
        dnew.agentdata[0].liquidities.lp.token1 = random_continue(
            dnew.agentdata[0].liquidities.lp.token1
        )
        dnew.agentdata[0].liquidities.wallet.token0 = random_continue(
            dnew.agentdata[0].liquidities.wallet.token0
        )
        dnew.agentdata[0].liquidities.wallet.token1 = random_continue(
            dnew.agentdata[0].liquidities.wallet.token1
        )

        dnew.agentdata[1].liquidities.lp.token0 = random_continue(
            dnew.agentdata[1].liquidities.lp.token0
        )
        dnew.agentdata[1].liquidities.lp.token1 = random_continue(
            dnew.agentdata[1].liquidities.lp.token1
        )
        dnew.agentdata[1].liquidities.wallet.token0 = random_continue(
            dnew.agentdata[1].liquidities.wallet.token0
        )
        dnew.agentdata[1].liquidities.wallet.token1 = random_continue(
            dnew.agentdata[1].liquidities.wallet.token1
        )

        data[i] = dnew
    params = Params(
        progress_value=50,
        num_agents=2,
        pools=["0xpoo1l", "0xpool2"],
        start_date=datetime.date(2023, 4, 1),
        end_date=datetime.date(2023, 4, 20),
        token0="USDC",
        token1="WETH",
        pool_fee=0.05,
    )
