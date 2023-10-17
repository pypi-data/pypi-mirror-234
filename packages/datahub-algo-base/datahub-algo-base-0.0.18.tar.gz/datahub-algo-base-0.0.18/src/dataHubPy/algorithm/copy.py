from typing import List

from dataHubPy.algorithm.algorithm import Algorithm
from dataHubPy.connector.connector import Connector


class Copy(Algorithm):
    def __init__(self, configuration: dict) -> None:
        super().__init__(configuration)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    def run(
            self,
            connector_in_list: List[Connector],
            connector_out_list: List[Connector],
            cache_list: List[Connector]
    ) -> dict:
        connector_in = connector_in_list[0]
        connector_out = connector_out_list[0]
        data = connector_in.read_as_data_frame(self._input_data_item)
        connector_out.write_data_frame(data, self._output_data_item)
        return {"info": "executed Copy Algorithm."}
