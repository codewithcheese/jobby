from typing import Optional, List

from pydantic import BaseModel, Field


# Metadata model
class Metadata(BaseModel):
    id: int
    name: str
    value: Optional[str]
    value_type: str


# Location model
class Location(BaseModel):
    name: str


# DataCompliance model
class DataCompliance(BaseModel):
    type: str
    requires_consent: bool
    requires_processing_consent: bool
    requires_retention_consent: bool
    retention_period: Optional[str]


# Job model
class Job(BaseModel):
    absolute_url: str
    data_compliance: List[DataCompliance]
    internal_job_id: int
    location: Location
    metadata: Optional[List[Metadata]] = None  # Updated to allow null values
    id: int
    updated_at: str
    requisition_id: str
    title: str


# Department model
class Department(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    child_ids: List[int] = Field(default_factory=list)
    jobs: List[Job]


# Main model
class GreenhouseDepartmentsResponse(BaseModel):
    departments: List[Department]
