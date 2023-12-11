from pydantic import BaseModel
import datetime

class UserSchema(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    created_at: datetime.datetime | None = None
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
    
class ListUsers(BaseModel):
    status: int
    count: int
    users: list[UserSchema]