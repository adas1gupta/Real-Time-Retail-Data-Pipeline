from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoice_no = Column(Integer, index=True)
    stock_code = Column(String(20))
    description = Column(String(256))
    quantity = Column(Integer)
    invoice_date = Column(DateTime)
    unit_price = Column(Float)
    customer_id = Column(Integer, index=True)
    country = Column(String(64))
    total_price = Column(Float)