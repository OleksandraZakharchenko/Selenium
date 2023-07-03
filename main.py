from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from extract import *
import os
import requests
import subprocess

SECRET = os.getenv("SECRET")

app = FastAPI()

class PostalCode(BaseModel):
    postal_code: str

@app.get("/")
async def root():
    return {"message": "Hello!"}

@app.get("/sales-tax/")
async def get_sales_tax(postal_code: str):
    sales_tax = calculate_sales_tax(postal_code)
    
    if sales_tax is None:
        raise HTTPException(status_code=404, detail="Sales tax not found for the provided postal code")
    
    return {"sales_tax": sales_tax}

def calculate_sales_tax(postal_code: str) -> float:
    # Implement your logic here to calculate and retrieve the sales tax based on the postal code
    # You can use a database, external API, or any other data source to fetch the sales tax rates
    
    # Placeholder logic: Example sales tax rates based on postal code
    sales_tax_rates = {
        "10001": 0.085,  # Example sales tax rate for postal code 10001
        "20001": 0.06,   # Example sales tax rate for postal code 20001
        # Add more sales tax rates for other postal codes as needed
    }
    
    return sales_tax_rates.get(postal_code)
