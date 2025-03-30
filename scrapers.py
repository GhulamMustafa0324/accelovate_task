from fastapi import HTTPException
from utils import map_experience_level, map_experience_level_indeed
from models import JobSearchRequest
from config import LINKEDIN_ACTOR_ID, INDEED_ACTOR_ID, GLASSDOOR_ACTOR_ID, APIFY_TOKEN
from logger import get_logger
from apify_client import ApifyClient


logger = get_logger(__name__)

client = ApifyClient(APIFY_TOKEN)
logger.info("Apify Client initialized.")

class JobScraper:
    def __init__(self, search_criteria: dict):
        self.search_criteria = search_criteria

    def fetch_linkedin_jobs(self):
        """
        Use the Apify Actor with dynamic inputs from the search_request to fetch LinkedIn jobs.
        Now includes jobNature and experienceLevel in the run_input.
        """
        print(self.search_criteria)
        # Extract the first number from the experience string and convert to string.
        experience_level = map_experience_level(
            self.search_criteria.get("experience", "1")
        )
        logger.info("Extracted experience level: %s", experience_level)
        print("Extracted experience level:", experience_level)

        # Build the dynamic input using values from the search request.
        run_input = {
            "title": self.search_criteria.get("position", ""),
            "location": self.search_criteria.get("location", ""),
            "companyName": self.search_criteria.get("companyName", []),
            "companyId": self.search_criteria.get("companyId", []),
            "jobNature": self.search_criteria.get("jobNature", ""),
            "experienceLevel": experience_level,
            "rows": 10,
            "proxy": {
                "useApifyProxy": True,
                "apifyProxyGroups": ["RESIDENTIAL"],
            },
        }
        logger.info(
            "Fetching LinkedIn jobs using Apify Actor with input: %s", run_input
        )
        print("Fetching LinkedIn jobs using Apify Actor with input:", run_input)
        try:
            run = client.actor(LINKEDIN_ACTOR_ID).call(run_input=run_input)
            dataset_id = run["defaultDatasetId"]
            jobs = []
            for item in client.dataset(dataset_id).iterate_items():
                job = {
                    "job_title": item.get("title", "Unknown Title"),
                    "company": item.get("companyName", "Unknown Company"),
                    "experience": self.search_criteria.get(
                        "experience", "Not Provided"
                    ),
                    "jobNature": self.search_criteria.get("jobNature", "Not Provided"),
                    "location": item.get(
                        "location", self.search_criteria.get("location", "")
                    ),
                    "salary": item.get("salary", "Not Provided"),
                    "apply_link": item.get("jobUrl", "No Link"),
                }
                jobs.append(job)
            logger.info("Fetched %d jobs from LinkedIn.", len(jobs))
            print("Fetched %d jobs from LinkedIn." % len(jobs))
            return jobs
        except Exception as e:
            logger.error("Error fetching LinkedIn jobs: %s", e)
            print("Error fetching LinkedIn jobs:", e)
            raise HTTPException(
                status_code=500, detail="Failed to fetch LinkedIn jobs."
            )

    def fetch_indeed_jobs(self):
        """
        Use the Apify Actor with dynamic inputs from the search_request to fetch Indeed jobs.
        The run_input is built dynamically using values from the search criteria.
        """
        experience_level = map_experience_level_indeed(
            self.search_criteria.get("experience", "1")
        )

        # Build the dynamic run input for Indeed.
        run_input = {
            "job": self.search_criteria.get("position", ""),
            "country": self.search_criteria.get("country", "united states"),
            "experienceLevel": experience_level,
            "sortType": self.search_criteria.get("jobNature", None),
            "city": self.search_criteria.get("city", ""),
            "numberOfResults": 5,
            "proxy": {"useApifyProxy": True},
        }
        logger.info("Fetching Indeed jobs using Apify Actor with input: %s", run_input)
        print("Fetching Indeed jobs using Apify Actor with input:", run_input)
        try:
            run = client.actor(INDEED_ACTOR_ID).call(run_input=run_input)
            dataset_id = run["defaultDatasetId"]
            jobs = []
            for item in client.dataset(dataset_id).iterate_items():
                job = {
                    "job_title": item.get("title", "Unknown Title"),
                    "company": item.get("companyName", "Unknown Company"),
                    "experience": item.get("experience", "Not Provided"),
                    "jobNature": item.get("jobNature", "Not Provided"),
                    "location": item.get(
                        "location", self.search_criteria.get("location", "")
                    ),
                    "salary": item.get("salary", "Not Provided"),
                    "apply_link": item.get("jobMetadata", {}).get("href", "No Link"),
                }
                jobs.append(job)
            logger.info("Fetched %d jobs from Indeed.", len(jobs))
            print("Fetched %d jobs from Indeed." % len(jobs))
            return jobs
        except Exception as e:
            logger.error("Error fetching Indeed jobs: %s", e)
            print("Error fetching Indeed jobs:", e)
            return []

    def fetch_glassdoor_jobs(self):
        """
        Use the Apify Actor with dynamic inputs from the search_request to fetch Glassdoor jobs.
        The run_input is built dynamically based on the search criteria.
        """
        try:
            salary_value = float(self.search_criteria.get("salary", 0))
        except Exception:
            salary_value = None

        run_input = {
            "keyword": f"{self.search_criteria.get('position', '')} {self.search_criteria.get('skills', '')}".strip(),
            "maxItems": 5,
            "location": self.search_criteria.get("location", ""),
            "includeNoSalaryJob": True,
            "minSalary": salary_value,
            "maxSalary": salary_value,
            "fromAge": 30,
            "jobType": self.search_criteria.get("jobNature", ""),
            "radius": 50,
            "proxy": {"useApifyProxy": True},
        }
        logger.info(
            "Fetching Glassdoor jobs using Apify Actor with input: %s", run_input
        )
        print("Fetching Glassdoor jobs using Apify Actor with input:", run_input)
        try:
            run = client.actor(GLASSDOOR_ACTOR_ID).call(run_input=run_input)
            dataset_id = run["defaultDatasetId"]
            jobs = []
            for item in client.dataset(dataset_id).iterate_items():
                job = {
                    "job_title": item.get("job_title", "Unknown Title"),
                    "company": item.get("company_name", "Unknown Company"),
                    "experience": self.search_criteria.get(
                        "experience", "Not Provided"
                    ),
                    "jobNature": (
                        ", ".join(item.get("job_job_types", []))
                        if item.get("job_job_types")
                        else "Not Provided"
                    ),
                    "location": item.get("job_location", {}).get(
                        "unknown", self.search_criteria.get("location", "")
                    ),
                    "salary": (
                        (
                            f"{item.get('job_salary', {}).get('currency_symbol', '$')}"
                            f"{item.get('job_salary', {}).get('min', 'Not Provided')}"
                        )
                        if item.get("job_salary")
                        else "Not Provided"
                    ),
                    "apply_link": item.get("job_apply_url", "No Link"),
                }
                jobs.append(job)
            logger.info("Fetched %d jobs from Glassdoor.", len(jobs))
            print("Fetched %d jobs from Glassdoor." % len(jobs))
            return jobs
        except Exception as e:
            logger.error("Error fetching Glassdoor jobs: %s", e)
            print("Error fetching Glassdoor jobs:", e)
            return []
