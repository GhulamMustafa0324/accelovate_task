from pydantic import BaseModel

class JobSearchRequest(BaseModel):
    position: str
    experience: str
    salary: str
    jobNature: str
    location: str
    skills: str

class JobDetail(BaseModel):
    job_title: str
    company: str
    experience: str
    jobNature: str
    location: str
    salary: str
    apply_link: str
    similarity: float = 0.0  # similarity score for ranking

class JobSearchResponse(BaseModel):
    relevant_jobs: list[JobDetail]
