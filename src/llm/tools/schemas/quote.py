from pydantic import BaseModel, Field


class GetQuoteHistoryInfo(BaseModel):
    symbol: str = Field(
        ...,
        description="Mã cổ phiếu cần lấy thống kê lịch sử giá.",
    )
    start: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="Thời điểm bắt đầu (YYYY-MM-DD)",
    )
    end: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="Thời điểm kết thúc (YYYY-MM-DD)",
    )
