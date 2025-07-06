from fastapi import FastAPI, Depends, HTTPException
from kafka import KafkaProducer
from sqlalchemy.orm import Session
import json, os
from .database import SessionLocal, Base, engine
from .schemas import InvoiceIn
from .models import Invoice

Base.metadata.create_all(bind=engine)

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS","kafka:9092"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def health():
    return {"status": "ok"}

@app.post("/invoices", status_code=201)
async def ingest(invoice: InvoiceIn):
    producer.send("ingestion-topic", invoice.model_dump())
    return {"message": "queued"}

@app.get("/sales")
async def sales_summary(db: Session = Depends(get_db)):
    rows = db.execute(
        """SELECT country, SUM(total_price) as revenue
           FROM invoices GROUP BY country ORDER BY revenue DESC LIMIT 10"""
    ).fetchall()
    return [dict(r) for r in rows]