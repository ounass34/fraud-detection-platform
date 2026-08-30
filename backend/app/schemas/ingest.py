from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field

class MeterReadingItem(BaseModel):
    meter_number: str
    reading_time: datetime
    active_energy_kwh: float | None = None
    reactive_energy_kvarh: float | None = None
    voltage: float | None = None
    current: float | None = None
    load_profile: dict[str, Any] | None = None

class MeterReadingIngestRequest(BaseModel):
    source: str = "API"
    readings: list[MeterReadingItem]

class CustomerSyncItem(BaseModel):
    external_id: str | None = None
    account_number: str
    full_name: str | None = None
    phone: str | None = None
    address: str | None = None
    voltage: str = Field(default="BT", pattern="^(BT|MT|HT)$")
    phase: str = Field(default="MONOPHASE", pattern="^(MONOPHASE|TRIPHASE)$")
    subscribed_power_kw: float | None = None
    latitude: float | None = None
    longitude: float | None = None

class CustomerSyncRequest(BaseModel):
    customers: list[CustomerSyncItem]
