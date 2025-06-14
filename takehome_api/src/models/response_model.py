from pydantic import BaseModel
from uuid import UUID


class AppointmentResponse(BaseModel):
    patient: str
    scheduled: bool
    appointment_id: UUID
    provider: str
    time: str


class ProviderResponse(BaseModel):
    first_name: str
    last_name: str
    title: str
    states: list[str]
    insurances: list[str]
    appointment_times: list[str]


class PatientResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    state: str
    insurance: str
    appointment_times: list[str]
