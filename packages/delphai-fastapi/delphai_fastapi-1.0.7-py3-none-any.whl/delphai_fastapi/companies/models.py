from typing import Any, Dict, List, Optional

from fastapi_camelcase import CamelModel
from pydantic import Field

from ..types import ObjectId
from ..models import Location, Source


class EmployeeCount(CamelModel):
    min: Optional[int] = Field(
        description="Bottom range of the employee count interval", example=11
    )
    max: Optional[int] = Field(
        description="Top range of the employee count interval", example=50
    )
    exact: Optional[int] = Field(description="Exact number for employees", example=30)
    range: Optional[str] = Field(
        description="Employee count interval displayed in delphai", example="11-50"
    )


class CompanyDescription(CamelModel):
    long: Optional[str] = Field(
        description="Company's default description",
        example=(
            "delphai is an AI and big data analytics software platform that informs "
            "business decisions and validates strategies"
        ),
    )
    short: Optional[str] = Field(
        description="Truncated version of company's default description",
        example="delphai is an AI and big data analytics software platform",
    )


class CompanyRevenue(CamelModel):
    currency: Optional[str] = Field(
        description="Currency of revenue number", example="EUR"
    )
    annual: Optional[int] = Field(
        description="Annual revenue number for specified year", example=5000000
    )
    year: Optional[int] = Field(description="Year of revenue number", example=2022)
    source: Source


CompanyIdentifierCategory = str
CompanyIdentifierSubcategory = str
CompanyIdentifier = Dict[CompanyIdentifierSubcategory, str]


class Company(CamelModel):
    id: ObjectId = Field(..., description="Internal company ID")
    name: Optional[str] = Field(description="Name of the company", example="delphai")
    url: str = Field(..., description="Webpage of the company", example="delphai.com")
    descriptions: Optional[Dict[str, CompanyDescription]]
    founding_year: Optional[int] = Field(description="Founding year", example=2020)
    headquarters: Optional[Location] = Field(description="Company address")
    employee_count: Optional[EmployeeCount] = Field(description="Number of employees")
    additional_urls: Optional[Dict[str, str]] = Field(
        example={"linkedin": "https://www.linkedin.com/company/delphai"}
    )
    revenue: Optional[Dict[str, CompanyRevenue]] = Field(
        description="Company revenue with currency"
    )
    products: Optional[List[str]] = Field(
        description="List of company products", example=["Software"]
    )
    identifiers: Optional[Dict[CompanyIdentifierCategory, CompanyIdentifier]] = Field(
        description="Object of company identifiers"
    )
    custom_attributes: Optional[Dict[str, Any]] = Field(
        description="Company custom attributes",
        example={"crmId": 84831, "labels": ["Partner", "Supplier"]},
    )
    industries: Optional[List[str]] = Field(
        example=["Software & internet services", "Hardware & IT equipment"]
    )


class CompaniesSearchResult(CamelModel):
    company: Company
    score: float = Field(default=0, description="Search score", example="202.35745")
    snippets: List[str] = Field(
        default=[],
        description="Snippets containing query keywords",
        example=[
            "delphai is an AI and big data analytics software platform that informs "
            "business decisions and validates strategies"
        ],
    )


class CompaniesSearchResults(CamelModel):
    results: List[CompaniesSearchResult]
    total: int = Field(..., description="Number of results", example=1337)


class CompanyPeer(CamelModel):
    company: Company
    score: float = Field(default=0, description="Search score", example="202.35745")


class CompanyPeers(CamelModel):
    results: List[CompanyPeer]
    total: int = Field(..., description="Number of results", example=5)


class CompanyCustomAttribute(CamelModel):
    type: str = Field(description="Attribute type", example="singleSelect")
    choices: Optional[List[Any]] = Field(description="Valid values")
    value: Any = Field(description="Attribute value")


class CompanyCustomAttributes(CamelModel):
    custom_attributes: Dict[str, CompanyCustomAttribute] = Field(
        description="Company custom attributes",
        example={
            "crmId": {"type": "singleSelect", "value": 84831},
            "labels": {
                "type": "multipleSelect",
                "choices": ["Partner", "Peer", "Provider", "Supplier"],
                "value": ["Partner", "Supplier"],
            },
        },
    )


class CompanyCustomAttributeUpdate(CamelModel):
    value: Any = Field(description="Attribute value")
    delete: bool = Field(False, description="Unset attribute")


class CompanyCustomAttributesUpdate(CamelModel):
    custom_attributes: Dict[str, CompanyCustomAttributeUpdate] = Field(
        description="Company custom attributes",
        example={
            "crmId": {"value": 84831},
            "labels": {"value": ["Partner", "Supplier"]},
            "notes": {"delete": True},
        },
    )
