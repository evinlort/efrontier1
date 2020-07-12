from typing import List, Optional


class Asset:
    def __init__(self, name: str, body: dict, timestamp: str):
        self.name = name.strip('asset')
        self.ask = None
        self.bid = None
        self.timestamp = timestamp
        self.parse_asset(body)

    def parse_asset(self, body: dict):
        self.ask = body["ask"]
        self.bid = body["bid"]


class Stream:
    def __init__(self, coefficient: int = 1):
        self.coeff = coefficient
        self.output_stream = []
        self.count = 0
        self.time = None
        self.trade = dict()
        self.assets: List[List[Asset]] = []  # list of 2 lists of dicts

    def set(self, timestamp: str, assets: dict) -> bool:
        self.time = timestamp
        to_list = list()
        for name in assets.keys():
            to_list.append(Asset(name, assets[name], timestamp))
        if len(self.assets) >= 3:
            self.assets.pop(0)
        self.assets.append(to_list)
        return len(self.assets) >= 3

    def calculate(self):
        a1 = self.assets[0]
        a2 = self.assets[1]
        a3 = self.assets[2]
        trade = {"time": self.time, "actions": list()}
        for i in range(len(a1)):
            ask_diff21 = a2[i].ask - a1[i].ask
            bid_diff21 = a2[i].bid - a1[i].bid
            ask_diff32 = a3[i].ask - a2[i].ask
            bid_diff32 = a3[i].bid - a2[i].bid

            if ask_diff32 > 0:
                ask_div = abs(ask_diff21 / ask_diff32)
            else:
                ask_div = self.coeff
            if bid_diff32 > 0:
                bid_div = (bid_diff21 / bid_diff32)
            else:
                bid_div = self.coeff

            if ask_div < self.coeff or bid_div < self.coeff:
                if ask_diff21 - ask_diff32 > bid_diff21 - bid_diff32:
                    trade["actions"].append(f"buy{a1[i].name.upper()}")
                else:
                    trade["actions"].append(f"sell{a1[i].name.upper()}")

        if len(trade["actions"]) == 0:
            self.trade = None
        else:
            self.trade = trade

    def get_trade(self) -> Optional[dict]:
        return self.trade or None
