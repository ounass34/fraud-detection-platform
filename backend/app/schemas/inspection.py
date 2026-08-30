from datetime import datetime
from pydantic import BaseModel

class AssignInspectionRequest(BaseModel):
    customer_id: str
    agent_id: str
    scheduled_at: datetime | None = None

class InspectionEvidence(BaseModel):
    evidence_type: str
    file_url: str | None = None
    sha256: str | None = None

class InspectionSubmitRequest(BaseModel):
    inspection_id: str
    fraud_confirmed: bool
    fraud_type: str
    notes: str | None = None
    latitude: float
    longitude: float
    gps_accuracy_m: float | None = None
    device_id: str
    completed_at: datetime
    evidence: list[InspectionEvidence] = []
