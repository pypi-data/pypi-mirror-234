from typing import List

from dataHubPy.connector.connector import Connector


class Algorithm:
    _registry = {}

    def __init__(self, configuration: dict) -> None:
        super().__init__()
        self._input_data_item = configuration.get("input", {}).get("data", "")
        self._output_data_item = configuration.get("output", {}).get("data", "")

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[cls.__name__] = cls

    def run(
            self,
            connector_in_list: List[Connector],
            connector_out_list: List[Connector],
            connector_cache_list: List[Connector]
    ) -> dict:
        raise Exception("not implement")

    def list_registry(self):
        return self._registry
