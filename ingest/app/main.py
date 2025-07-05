from fastapi import FastAPI, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel
from datetime import datetime
from kafka import KafkaProducer, producer

class InvoiceItem(BaseModel):
    InvoiceNo: int
    StockCode: str
    Description: str
    Quantity: int
    InvoiceDate: str
    UnitPrice: float
    CustomerID: int
    Country: str

app = FastAPI()

# base url
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Add a new invoice
@app.post("/invoiceitem")
async def post_invoice_item(item: InvoiceItem):
    print("Message received")
    try:
        date = datetime.strptime(item.InvoiceDate, "%d/%m/%Y %H:%M")
        item.InvoiceDate = date.strftime("%d-%m-%Y %H:%M:%S")
        
        json_of_item = jsonable_encoder(item)
        json_as_string = json.dumps(json_of_item)
        produce_kafka_string(json_as_string)

        return JSONResponse(content=json_of_item, status_code=201)
    
    except ValueError:
        return JSONResponse(content=jsonable_encoder(item), status_code=400)
        

def produce_kafka_string(json_as_string):
    producer = KafkaProducer(bootstrap_servers='kafka:9092',acks=1)
    producer.send('ingestion-topic', bytes(json_as_string, 'utf-8'))
    producer.flush() 