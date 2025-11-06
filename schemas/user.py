from pydantic import BaseModel, EmailStr, Field, model_validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    first_name: Optional[str] = Field(None, description="User's first name")
    last_name: Optional[str] = Field(None, description="User's last name")
    email: Optional[EmailStr] = Field(None, description="User email address")

class UserInsert(UserBase):
    password: str = Field(..., description="Password required when creating a new user")

class UserUpdate(UserBase):
    id: int = Field(..., description="User ID to update")
    password: Optional[str] = Field(None, description="Optional password for update")

class UserFilter(UserBase):
    id: Optional[int] = Field(None, description="User ID filter")

class UserOut(UserBase):
    id: int = Field(..., description="Unique user identifier")
    password: Optional[str] = Field(None, description="Normally not returned for security reasons")
    created_at: datetime = Field(..., description="Timestamp when the user was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the user was last updated")

class ProfileUpdate(UserBase):
    password: Optional[str] = Field(None, description="Current password (required to change password)")
    new_password: Optional[str] = Field(None, description="New password")
    new_confirm_password: Optional[str] = Field(None, description="New password confirmation")

    @model_validator(mode='after')
    def check_password_match(self):
        if self.new_password or self.new_confirm_password:
            if not self.password:
                raise ValueError("Current password is required to update the password")

            if not self.new_password or not self.new_confirm_password:
                raise ValueError("Both new_password and new_confirm_password must be provided")

            if self.new_password != self.new_confirm_password:
                raise ValueError("New passwords do not match")
        return self
