from typing import Type
from pandas import DataFrame
from pydantic import BaseModel
from vnstock3 import Company

from llm.tools.schemas import CustomBaseTool
from llm.tools.schemas.company import GetCompanyInfomation


class GetCompanyProfile(CustomBaseTool):
    name: str = "GetCompanyProfile"
    description: str = "Lấy thông tin hồ sơ chi tiết của công ty, bao gồm lịch sử, ngành nghề, địa chỉ và các thông tin cơ bản khác."
    args_schema: Type[BaseModel] = GetCompanyInfomation
    return_direct: bool = True

    @property
    def args(self) -> dict:
        return self.get_input_schema().model_json_schema()

    def _run(self, symbol: str) -> DataFrame:
        company = Company(symbol)
        profile: DataFrame = company.profile()
        if not profile.empty:
            profile.assign(symbol=symbol)

        return profile.to_markdown()


class GetCompanyOverview(CustomBaseTool):
    name: str = "GetCompanyOverview"
    description: str = "Lấy tổng quan về công ty, bao gồm vốn hóa thị trường, giá cổ phiếu, doanh thu, lợi nhuận và các chỉ số tài chính quan trọng."
    args_schema: Type[BaseModel] = GetCompanyInfomation
    return_direct: bool = True

    @property
    def args(self) -> dict:
        return self.get_input_schema().model_json_schema()

    def _run(self, symbol: str) -> DataFrame:
        company = Company(symbol)
        overview: DataFrame = company.overview()
        if not overview.empty:
            overview.assign(symbol=symbol)

        return overview.to_markdown()


class GetCompanyShareholders(CustomBaseTool):
    name: str = "GetCompanyShareholders"
    description: str = "Lấy danh sách cổ đông lớn của công ty, bao gồm tỷ lệ sở hữu của từng cổ đông."
    args_schema: Type[BaseModel] = GetCompanyInfomation
    return_direct: bool = True

    @property
    def args(self) -> dict:
        return self.get_input_schema().model_json_schema()

    def _run(self, symbol: str) -> DataFrame:
        company = Company(symbol)
        shareholders: DataFrame = company.shareholders()
        if not shareholders.empty:
            shareholders.assign(symbol=symbol)

        return shareholders.to_markdown()


class GetCompanyOfficers(CustomBaseTool):
    name: str = "GetCompanyOfficers"
    description: str = "Lấy danh sách ban lãnh đạo của công ty, bao gồm tên, chức vụ và thông tin cơ bản của từng người."
    args_schema: Type[BaseModel] = GetCompanyInfomation
    return_direct: bool = True

    @property
    def args(self) -> dict:
        return self.get_input_schema().model_json_schema()

    def _run(self, symbol: str) -> DataFrame:
        company = Company(symbol)
        officers: DataFrame = company.officers()
        if not officers.empty:
            officers.assign(symbol=symbol)

        return officers.to_markdown()


class GetCompanySubsidiaries(CustomBaseTool):
    name: str = "GetCompanySubsidiaries"
    description: str = "Lấy danh sách công ty con hoặc công ty liên kết của công ty mẹ."
    args_schema: Type[BaseModel] = GetCompanyInfomation
    return_direct: bool = True

    @property
    def args(self) -> dict:
        return self.get_input_schema().model_json_schema()

    def _run(self, symbol: str) -> DataFrame:
        company = Company(symbol)
        subsidiaries: DataFrame = company.subsidiaries()
        if not subsidiaries.empty:
            subsidiaries.assign(symbol=symbol)

        return subsidiaries.to_markdown()


class GetCompanyNews(CustomBaseTool):
    name: str = "GetCompanyNews"
    description: str = "Lấy tin tức mới nhất liên quan đến công ty, bao gồm tin tức thị trường và các thông báo quan trọng."
    args_schema: Type[BaseModel] = GetCompanyInfomation
    return_direct: bool = True

    @property
    def args(self) -> dict:
        return self.get_input_schema().model_json_schema()

    def _run(self, symbol: str) -> DataFrame:
        company = Company(symbol)
        news: DataFrame = company.news()
        if not news.empty:
            news.assign(symbol=symbol)

        return news.to_markdown()


class GetCompanyDividends(CustomBaseTool):
    name: str = "GetCompanyDividends"
    description: str = "Lấy thông tin về cổ tức của công ty, bao gồm ngày chia cổ tức, tỷ lệ chi trả và lịch sử chi trả cổ tức."
    args_schema: Type[BaseModel] = GetCompanyInfomation
    return_direct: bool = True

    @property
    def args(self) -> dict:
        return self.get_input_schema().model_json_schema()

    def _run(self, symbol: str) -> DataFrame:
        company = Company(symbol)
        dividends: DataFrame = company.dividends()
        if not dividends.empty:
            dividends.assign(symbol=symbol)

        return dividends.to_markdown()


class GetCompanyInsiderDeals(CustomBaseTool):
    name: str = "GetCompanyInsiderDeals"
    description: str = "Lấy danh sách giao dịch nội bộ của công ty, bao gồm thông tin mua bán cổ phiếu của lãnh đạo và cổ đông lớn."
    args_schema: Type[BaseModel] = GetCompanyInfomation
    return_direct: bool = True

    @property
    def args(self) -> dict:
        return self.get_input_schema().model_json_schema()

    def _run(self, symbol: str) -> DataFrame:
        company = Company(symbol)
        insider_deals: DataFrame = company.insider_deals()
        if not insider_deals.empty:
            insider_deals.assign(symbol=symbol)

        return insider_deals.to_markdown()


class GetCompanyEvents(CustomBaseTool):
    name: str = "GetCompanyEvents"
    description: str = (
        "Lấy danh sách các sự kiện quan trọng của công ty, bao gồm hội nghị cổ đông, phát hành cổ phiếu, và các thay đổi quan trọng khác."
    )
    args_schema: Type[BaseModel] = GetCompanyInfomation
    return_direct: bool = True

    @property
    def args(self) -> dict:
        return self.get_input_schema().model_json_schema()

    def _run(self, symbol: str) -> DataFrame:
        company = Company(symbol)
        events: DataFrame = company.events()
        if not events.empty:
            events.assign(symbol=symbol)

        return events.to_markdown()
