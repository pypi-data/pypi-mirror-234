from typing import Optional
from pydantic import ConfigDict, BaseModel, EmailStr, Field
from unipoll_api.documents import ResourceID


# Schema for the response with basic member info
class Member(BaseModel):
    id: ResourceID
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "1a2b3c4d5e6f7g8h9i0j",
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
        }
    })


# Schema for the request to add a member to a workspace
class AddMembers(BaseModel):
    accounts: list[ResourceID] = Field(title="Accounts")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "accounts": [
                "1a2b3c4d5e6f7g8h9i0j",
                "2a3b4c5d6e7f8g9h0i1j",
                "3a4b5c6d7e8f9g0h1i2j"
            ]
        }
    })


# Schema for the response with a list of members and their info
class MemberList(BaseModel):
    members: list[Member]
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "members": [
                {
                    "email": "jdoe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "role": "admin"
                },
                {
                    "email": "jsmith@example.com",
                    "first_name": "Jack",
                    "last_name": "Smith",
                    "role": "user"
                }
            ]
        }
    })
