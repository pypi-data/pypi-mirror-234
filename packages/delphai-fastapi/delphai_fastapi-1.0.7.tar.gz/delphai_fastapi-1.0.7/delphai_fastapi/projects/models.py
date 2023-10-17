from typing import List, Optional
from ..companies.models import Company
from fastapi_camelcase import CamelModel
from pydantic import Field
from datetime import datetime
from ..types import ObjectId


class Project(CamelModel):
    id: ObjectId = Field(..., description="Internal project ID")
    name: str = Field(
        ..., description="Name of the project", example="Healthcare | Startups"
    )
    total: Optional[int] = Field(
        description="Total number of companies in this project", example=35
    )
    created: Optional[datetime] = Field(description="When the project was created")
    created_by: Optional[str] = Field(
        description="ID of the user who created the project"
    )
    client: Optional[str] = Field(description="ID of the client who owns the project")
    last_modified: Optional[datetime] = Field(
        description="When the project was last edited or updated"
    )
    parent_project: Optional[ObjectId] = Field(
        description="Internal project ID of parent project"
    )


class Projects(CamelModel):
    results: List[Project]
    total: int = Field(..., description="Number of results")


class ProjectsCompany(CamelModel):
    company: Company
    custom_labels: Optional[List[str]] = Field(
        description="Custom labels assigned by user"
    )
    assigned_by: str = Field(description="By whom the company was added to the project")


class ProjectsCompanies(CamelModel):
    results: List[ProjectsCompany]
    total: int = Field(..., description="Number of companies in project", example=54)
