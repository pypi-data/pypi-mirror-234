from typing import Any
import pandas as pd


class Data:
    mapper: dict[str, list[Any]] = {"indices": [],
                                    "acoes": [], "indicadores": [], "renda_fixa": [], "commodities": []}

    def __init__(self, name):
        self.name = name
        