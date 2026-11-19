from pydantic import BaseModel
from fastapi_users import schemas
import uuid

# this basically inherit frombasemodel (special object) , use this as a type to recieve body data inside our functions
class PostCreate(BaseModel):
    title:str
    content:str

class PostResponse(BaseModel):
    title:str
    content:str

class UserRead(schemas.BaseUser):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass