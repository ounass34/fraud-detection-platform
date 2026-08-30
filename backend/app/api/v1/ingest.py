import json
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_db
from app.schemas.ingest import MeterReadingIngestRequest, CustomerSyncRequest

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

@router.post("/meter-readings", status_code=status.HTTP_202_ACCEPTED)
async def ingest_meter_readings(payload: MeterReadingIngestRequest, db: AsyncSession = Depends(get_db)):
    accepted, missing = 0, []
    for r in payload.readings:
        meter_id = (await db.execute(text("SELECT id FROM meters WHERE meter_number=:n"), {"n": r.meter_number})).scalar_one_or_none()
        if not meter_id:
            missing.append(r.meter_number)
            continue
        await db.execute(text('''
          INSERT INTO meter_readings(meter_id,reading_time,active_energy_kwh,reactive_energy_kvarh,voltage,current,load_profile,source)
          VALUES(:meter_id,:reading_time,:active,:reactive,:voltage,:current,CAST(:profile AS jsonb),:source)
        '''), {"meter_id":meter_id,"reading_time":r.reading_time,"active":r.active_energy_kwh,
               "reactive":r.reactive_energy_kvarh,"voltage":r.voltage,"current":r.current,
               "profile":json.dumps(r.load_profile or {}),"source":payload.source})
        accepted += 1
    await db.commit()
    return {"status":"accepted","accepted":accepted,"missing_meters":missing}

@router.post("/customers")
async def sync_customers(payload: CustomerSyncRequest, db: AsyncSession = Depends(get_db)):
    for c in payload.customers:
        await db.execute(text('''
          INSERT INTO customers(external_id,account_number,full_name,phone,address,voltage,phase,subscribed_power_kw,geom)
          VALUES(:external_id,:account_number,:full_name,:phone,:address,:voltage,:phase,:power,
          CASE WHEN :lat IS NULL OR :lon IS NULL THEN NULL ELSE ST_SetSRID(ST_MakePoint(:lon,:lat),4326)::geography END)
          ON CONFLICT(account_number) DO UPDATE SET full_name=EXCLUDED.full_name, phone=EXCLUDED.phone,
          address=EXCLUDED.address, voltage=EXCLUDED.voltage, phase=EXCLUDED.phase,
          subscribed_power_kw=EXCLUDED.subscribed_power_kw, geom=EXCLUDED.geom, updated_at=NOW()
        '''), {"external_id":c.external_id,"account_number":c.account_number,"full_name":c.full_name,
               "phone":c.phone,"address":c.address,"voltage":c.voltage,"phase":c.phase,
               "power":c.subscribed_power_kw,"lat":c.latitude,"lon":c.longitude})
    await db.commit()
    return {"status":"success","processed":len(payload.customers)}
