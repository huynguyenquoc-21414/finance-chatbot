from typing import Type
from pydantic import BaseModel
from vnstock3.common.data.data_explorer import StockComponents
from vnstock3 import Vnstock
from pandas import DataFrame

from llm.tools.schemas import CustomBaseTool
from llm.tools.schemas.income_statement import GetIncomeStatementInfo


class GetIncomeStatement(CustomBaseTool):
    name: str = "GetIncomeStatement"
    description: str = "Lấy bảng cân đối kế toán của công ty, bao gồm doanh thu, lợi nhuận gộp, lợi nhuận ròng và các chỉ số tài chính khác."
    args_schema: Type[BaseModel] = GetIncomeStatementInfo
    return_direct: bool = True

    @property
    def args(self) -> dict:
        return self.get_input_schema().model_json_schema()

    def _run(self, symbol: str) -> DataFrame:
        stock: StockComponents = Vnstock().stock(symbol)
        income_statement: DataFrame = stock.finance.income_statement(
            period="year",
            lang="vi",
        )
        if not income_statement.empty:
            income_statement.assign(symbol=symbol)

        return income_statement.to_markdown()


class GetBalanceSheet(CustomBaseTool):
    name: str = "GetBalanceSheet"
    description: str = "Lấy bảng cân đối kế toán của công ty, bao gồm tài sản, nợ và vốn của công ty."
    args_schema: Type[BaseModel] = GetIncomeStatementInfo
    return_direct: bool = True

    @property
    def args(self) -> dict:
        return self.get_input_schema().model_json_schema()

    def _run(self, symbol: str) -> DataFrame:
        stock: StockComponents = Vnstock().stock(symbol)
        balance_sheet: DataFrame = stock.finance.balance_sheet(
            period="year",
            lang="vi",
        )
        if not balance_sheet.empty:
            balance_sheet.assign(symbol=symbol)

        return balance_sheet.to_markdown()


class GetCashFlow(CustomBaseTool):
    name: str = "GetCashFlow"
    description: str = "Lấy bảng cân đối kế toán của công ty, bao gồm tài sản, nợ và vốn của công ty."
    args_schema: Type[BaseModel] = GetIncomeStatementInfo
    return_direct: bool = True

    @property
    def args(self) -> dict:
        return self.get_input_schema().model_json_schema()

    def _run(self, symbol: str, source: str = "VCI") -> DataFrame:
        stock: StockComponents = Vnstock().stock(symbol, source)
        cash_flow: DataFrame = stock.finance.cash_flow(
            period="year",
            lang="vi",
        )
        if not cash_flow.empty:
            cash_flow.assign(symbol=symbol)

        return cash_flow.to_markdown()


class GetRatio(CustomBaseTool):
    name: str = "GetRatio"
    description: str = "Lấy các chỉ số tài chính của công ty, bao gồm ROE, ROA, EPS, P/E, P/B, P/S, EV/EBITDA và các chỉ số khác."
    args_schema: Type[BaseModel] = GetIncomeStatementInfo
    return_direct: bool = True

    @property
    def args(self) -> dict:
        return self.get_input_schema().model_json_schema()

    def _run(self, symbol: str, source: str = "VCI") -> DataFrame:
        stock: StockComponents = Vnstock().stock(symbol, source)
        ratio: DataFrame = stock.finance.ratio(
            symbol=symbol,
            period="year",
            lang="vi",
        )
        if not ratio.empty:
            ratio.assign(symbol=symbol)

        return ratio.to_markdown()
