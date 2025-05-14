
from fastapi import FastAPI
from typing import List, Optional
from pydantic import BaseModel
import uuid

app = FastAPI()

# Models
class Company(BaseModel):
    company_name: str
    country: str
    city: str
    address: str
    description: str
    website: Optional[str] = None

class WTSListing(BaseModel):
    company_id: str
    product_name: str
    quantity: int
    price: float
    currency: str
    description: Optional[str] = None

# In-memory "databases"
companies_db = []
wts_db = []

@app.get("/")
async def root():
    return {"message": "GSMAuth Server Running"}

@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi():
    from fastapi.openapi.utils import get_openapi
    return get_openapi(title="GSMAuth API", version="1.0.0", routes=app.routes)

@app.post("/insert_company")
async def insert_company(company: Company):
    company_id = str(uuid.uuid4())
    companies_db.append({"id": company_id, **company.dict()})
    return {"success": True, "company_id": company_id}

@app.post("/insert_bulk_companies")
async def insert_bulk_companies(companies: List[Company]):
    inserted = []
    for company in companies:
        company_id = str(uuid.uuid4())
        companies_db.append({"id": company_id, **company.dict()})
        inserted.append(company_id)
    return {"success": True, "company_ids": inserted}

@app.get("/search_companies")
async def search_companies(search_term: str):
    results = [c for c in companies_db if search_term.lower() in c["company_name"].lower()]
    return {"results": results}

@app.post("/insert_wts")
async def insert_wts(wts: WTSListing):
    wts_id = str(uuid.uuid4())
    wts_db.append({"id": wts_id, **wts.dict()})
    return {"success": True, "wts_id": wts_id}

@app.post("/insert_bulk_wts")
async def insert_bulk_wts(wts_list: List[WTSListing]):
    inserted = []
    for wts in wts_list:
        wts_id = str(uuid.uuid4())
        wts_db.append({"id": wts_id, **wts.dict()})
        inserted.append(wts_id)
    return {"success": True, "wts_ids": inserted}
