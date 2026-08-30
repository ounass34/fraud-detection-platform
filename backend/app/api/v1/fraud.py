from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_db

router = APIRouter(prefix="/fraud", tags=["Fraud Detection"])

@router.get("/suspects")
async def suspects(min_score: float = Query(0, ge=0, le=100), voltage: str | None = None, db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(text('''
      SELECT DISTINCT ON(fs.customer_id) fs.customer_id::text,c.account_number,c.full_name,
      fs.risk_score::float,fs.estimated_loss_kwh::float,fs.estimated_loss_amount::float,
      ST_Y(c.geom::geometry) latitude,ST_X(c.geom::geometry) longitude
      FROM fraud_scores fs JOIN customers c ON c.id=fs.customer_id
      WHERE fs.risk_score>=:score AND (:voltage IS NULL OR c.voltage=:voltage)
      ORDER BY fs.customer_id,fs.calculated_at DESC
    '''), {"score":min_score,"voltage":voltage})).mappings().all()
    data=[]
    for row in rows:
        x=dict(row); s=x["risk_score"]
        x["risk_level"]="CRITICAL" if s>=80 else "HIGH" if s>=50 else "MEDIUM" if s>=30 else "LOW"
        data.append(x)
    return {"data":data}

@router.get("/suspects/{client_id}/explain")
async def explain(client_id: str, db: AsyncSession = Depends(get_db)):
    row=(await db.execute(text('''
      SELECT risk_score::float,explanation,anomaly_ratio::float,peer_deviation::float
      FROM fraud_scores WHERE customer_id=:id ORDER BY calculated_at DESC LIMIT 1
    '''),{"id":client_id})).mappings().first()
    if not row: return {"customer_id":client_id,"risk_score":0,"top_factors":[],"ratios":{}}
    return {"customer_id":client_id,"risk_score":row["risk_score"],
            "top_factors":(row["explanation"] or {}).get("top_factors",[]),
            "ratios":{"anomaly_ratio":row["anomaly_ratio"],"peer_deviation":row["peer_deviation"]}}
