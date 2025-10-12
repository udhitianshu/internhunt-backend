from pydantic import BaseModel
from typing import List

class UserProfile(BaseModel):
    name: str
    email: str
    branch: str
    skills: List[str]
