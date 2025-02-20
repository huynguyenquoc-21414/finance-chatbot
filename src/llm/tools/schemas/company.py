from pydantic import BaseModel, Field


class GetCompanyInfomation(BaseModel):
    symbol: str = Field(
        ...,
        description="Mã cố phiếu của công ty cần lấy thông tin.",
    )
