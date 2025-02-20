from typing import Literal
from pydantic import BaseModel, Field


class GetIncomeStatementInfo(BaseModel):
    symbol: str = Field(
        ...,
        description="Mã cổ phiếu cần lấy thông tin báo cáo tài chính.",
    )
    source: Literal["VCI", "TCBS"] = Field(
        default="VCI",
        description="Nguồn dữ liệu tài chính: VCI hoặc TCBS.",
    )
