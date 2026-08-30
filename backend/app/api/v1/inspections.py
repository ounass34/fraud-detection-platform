import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_db
from app.schemas.inspection import AssignInspectionRequest, InspectionSubmitRequest

router=APIRouter(prefix="/inspections",tags=["Field Inspections"])

@router.post("/assign")
async def assign(payload:AssignInspectionRequest,db:AsyncSession=Depends(get_db)):
    iid=str(uuid.uuid4())
    await db.execute(text("INSERT INTO inspections(id,customer_id,agent_id,status,scheduled_at) VALUES(:id,:customer_id,:agent_id,'ASSIGNED',:scheduled_at)"),
                     {"id":iid,**payload.model_dump()})
    await db.commit()
    return {"id":iid,"status":"ASSIGNED"}

@router.post("/submit")
async def submit(payload:InspectionSubmitRequest,db:AsyncSession=Depends(get_db)):
    await db.execute(text('''
      UPDATE inspections SET status='COMPLETED',fraud_confirmed=:fraud_confirmed,fraud_type=:fraud_type,
      notes=:notes,completed_at=:completed_at,device_id=:device_id,
      inspection_geom=ST_SetSRID(ST_MakePoint(:longitude,:latitude),4326)::geography,
      updated_at=NOW(),sync_version=sync_version+1 WHERE id=:inspection_id
    '''),payload.model_dump(exclude={"evidence","gps_accuracy_m"}))
    for e in payload.evidence:
        await db.execute(text("INSERT INTO inspection_evidence(inspection_id,evidence_type,file_url,sha256) VALUES(:inspection_id,:evidence_type,:file_url,:sha256)"),
                         {"inspection_id":payload.inspection_id,**e.model_dump()})
    await db.commit()
    return {"status":"received","inspection_id":payload.inspection_id}

@router.get("/sync")
async def sync(last_sync:str|None=None,agent_id:str|None=None,db:AsyncSession=Depends(get_db)):
    rows=(await db.execute(text('''
      SELECT id::text,customer_id::text,agent_id::text,status,scheduled_at,sync_version,updated_at
      FROM inspections WHERE (:agent IS NULL OR agent_id::text=:agent)
      AND (:last IS NULL OR updated_at>CAST(:last AS timestamptz)) ORDER BY updated_at
    '''),{"last":last_sync,"agent":agent_id})).mappings().all()
    return {"server_time":datetime.now(timezone.utc).isoformat(),"inspections":[dict(x) for x in rows],"deleted_ids":[]}
