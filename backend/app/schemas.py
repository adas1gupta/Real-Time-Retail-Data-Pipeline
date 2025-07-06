from pydantic import BaseModel, Field
from datetime import datetime

class InvoiceIn(BaseModel):
    InvoiceNo: int
    StockCode: str
    Description: str
    Quantity: int
    InvoiceDate: datetime
    UnitPrice: float
    CustomerID: int
    Country: str