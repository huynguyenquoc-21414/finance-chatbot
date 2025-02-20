from typing import Type
from pandas import DataFrame
from pydantic import BaseModel
from vnstock3.common.data.data_explorer import StockComponents
from vnstock3 import Vnstock

from llm.tools.schemas import CustomBaseTool
from llm.tools.schemas.quote import GetQuoteHistoryInfo


class GetQuoteHistory(CustomBaseTool):
    name: str = "GetQuoteHistory"
    description: str = "Lấy lịch sử giá cổ phiếu của công ty."
    args_schema: Type[BaseModel] = GetQuoteHistoryInfo
    return_direct: bool = True

    @property
    def args(self) -> dict:
        return self.get_input_schema().model_json_schema()

    def _run(self, symbol: str, start: str, end: str) -> DataFrame:
        stock: StockComponents = Vnstock().stock(symbol)
        quote_history: DataFrame = stock.quote.history(
            start=start,
            end=end,
        )
        if not quote_history.empty:
            quote_history.assign(symbol=symbol)

        return quote_history.to_markdown()
