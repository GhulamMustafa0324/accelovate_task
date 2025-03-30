from typing import List, Optional
from pydantic import BaseModel

class JobSearchRequest(BaseModel):
    position: str
    experience: str
    salary: str
    jobNature: str
    location: str
    Country: Optional[str] = ""
    City: Optional[str] = ""
    skills: str
    companyName: Optional[List[str]] = []  # Optional dynamic input
    companyId: Optional[List[str]] = []  # Optional dynamic input
    publishedAt: Optional[str] = ""  # Optional dynamic input


# The rest of your models remain unchanged.
class JobDetail(BaseModel):
    job_title: str
    company: str
    experience: str
    jobNature: str
    location: str
    salary: str
    apply_link: str
    similarity: float = 0.0


class JobSearchResponse(BaseModel):
    relevant_jobs: List[JobDetail]
