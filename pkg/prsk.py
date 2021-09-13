from datetime import datetime, timedelta

import pandas as pd
import requests as r
from pandas import DataFrame

YAML_PATH: str = "./config.yaml"


class PSEKAI:
    def __init__(self):
        self.TAR_RANK: list = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            20, 30, 40, 50, 100,
            200, 300, 400, 500, 1000,
            2000, 3000, 4000, 5000, 10000,
            20000, 30000, 40000, 50000, 100000
        ]
        self.BASE_URL: str = "https://api.sekai.best/event/{event_id}/" \
            "rankings/graph?rank={rank}"

    @staticmethod
    def get_event_name():
        res: dict = r.get("https://i18n-json.sekai.best/ja/event_name.json").json()
        table: list = []
        for eid, name in res.items():
            table.append({"eventId": int(eid), "eventName": name})
        return DataFrame(table)

    @staticmethod
    def fmt_the_date(dt_str: str) -> datetime:
        dt_str = dt_str.replace("T", " ")
        return datetime.fromisoformat(dt_str[:-5]) + timedelta(hours=9)

    def get_tar_rank(self, limit):
        return [n for n in self.TAR_RANK if n <= limit]

    def get_border(self, event_id, rank):
        edf: DataFrame = self.get_event_name()
        if event_id not in [str(n) for n in edf.eventId.to_list()]:
            return f'`{event_id}`は存在しないeventIdです。`.eventid`コマンドでIDをご確認ください。'
        if rank not in [str(n) for n in self.TAR_RANK]:
            return f'`TOP{rank}`の出力に対応していません。'
        res: dict = r.get(self.BASE_URL.format(event_id=event_id, rank=rank)).json()
        border_raw_list: list = res["data"]["eventRankings"]
        border_list: list = [
            {
                "datetime": self.fmt_the_date(rec["timestamp"]),
                "eventId": rec["eventId"],
                f"TOP{rank}": rec["score"],
                f"TOP{rank}_UID": rec["userId"],
                f"TOP{rank}_userName": rec["userName"],
            }
            for rec in border_raw_list
        ]
        cdf: DataFrame = DataFrame(border_list)
        return pd.merge(cdf, edf, on="eventId")
