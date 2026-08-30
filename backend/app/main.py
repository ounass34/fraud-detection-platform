from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, ingest, fraud, inspections

app=FastAPI(title="PNT Fraud Detection Platform",version="1.0.0",
            openapi_url="/api/v1/openapi.json",docs_url="/api/v1/docs",redoc_url="/api/v1/redoc")
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.CORS_ORIGINS.split(",")],
                   allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
for r in [auth.router,ingest.router,fraud.router,inspections.router]:
    app.include_router(r,prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status":"healthy","service":"pnt-fraud-api"}
