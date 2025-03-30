# import requests
# import time
# from bs4 import BeautifulSoup
# from logger import get_logger

# logger = get_logger(__name__)


# class JobScraper:
#     def __init__(self, search_criteria):
#         self.search_criteria = search_criteria

#     def fetch_indeed_jobs(self):
#         """Fetch job listings from Indeed based on search criteria."""
#         position = self.search_criteria.position.replace(" ", "+")
#         location = self.search_criteria.location.replace(" ", "+")
#         url = f"https://www.indeed.com/jobs?q={position}&l={location}"
#         headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

#         logger.info(
#             f"Fetching Indeed jobs for: Position='{position}', Location='{location}'"
#         )

#         try:
#             response = requests.get(url, headers=headers, timeout=10)
#             if response.status_code != 200:
#                 logger.error(
#                     f"Indeed responded with status code {response.status_code}"
#                 )
#                 return []

#             soup = BeautifulSoup(response.text, "html.parser")
#             jobs = []

#             # Find job cards based on Indeed’s current HTML structure
#             job_cards = soup.find_all(
#                 "div", class_="job_seen_beacon"
#             )  # Updated class name for Indeed job cards
#             logger.info(f"Found {len(job_cards)} job listings on Indeed.")

#             for card in job_cards:
#                 title_elem = card.find("h2")
#                 job_title = (
#                     title_elem.get_text(strip=True) if title_elem else "Unknown Title"
#                 )

#                 company_elem = card.find("span", class_="companyName")
#                 company = (
#                     company_elem.get_text(strip=True)
#                     if company_elem
#                     else "Unknown Company"
#                 )

#                 location_elem = card.find("div", class_="companyLocation")
#                 location_text = (
#                     location_elem.get_text(strip=True)
#                     if location_elem
#                     else "Unknown Location"
#                 )

#                 link_elem = card.find("a", href=True)
#                 apply_link = (
#                     f"https://www.indeed.com{link_elem['href']}"
#                     if link_elem
#                     else "No Link"
#                 )

#                 jobs.append(
#                     {
#                         "job_title": job_title,
#                         "company": company,
#                         "experience": self.search_criteria.experience,
#                         "jobNature": self.search_criteria.jobNature,
#                         "location": location_text,
#                         "salary": "Not Provided",
#                         "apply_link": apply_link,
#                     }
#                 )

#             time.sleep(1)  # Add delay to prevent getting blocked
#             return jobs

#         except requests.exceptions.RequestException as e:
#             logger.error(f"Failed to fetch Indeed jobs: {e}")
#             return []

#     def fetch_linkedin_jobs(self):
#         """LinkedIn restricts scraping. Use the API instead."""
#         logger.warning(
#             "LinkedIn scraping is not implemented. Consider using their API."
#         )
#         raise NotImplementedError(
#             "LinkedIn scraper not implemented. Use the official API."
#         )

#     def fetch_optional_jobs(self):
#         """Placeholder for other job sources like Glassdoor."""
#         logger.warning("Optional job scraper not implemented. Consider using an API.")
#         raise NotImplementedError(
#             "Optional job scraper not implemented. Use the official API or another method."
#         )


import os
from apify_client import ApifyClient
from fastapi import HTTPException
from logger import get_logger
from models import JobSearchRequest

logger = get_logger(__name__)

# Retrieve Apify token from environment or set it directly here.
APIFY_TOKEN = os.environ.get("APIFY_TOKEN", "<YOUR_API_TOKEN>")
client = ApifyClient(APIFY_TOKEN)


class JobScraper:
    def __init__(self, search_criteria: JobSearchRequest):
        self.search_criteria = search_criteria

    def fetch_indeed_jobs(self):
        """
        Use Apify actor to fetch job listings from Indeed.
        Expected input parameters for the actor are assumed to be:
          - searchQuery: job title or keywords.
          - location: job location.
          - proxy settings.
        The actor should output items with keys that can be mapped to:
          "job_title", "company", "location", "salary", and "apply_link".
        """
        run_input = {
            "searchQuery": self.search_criteria.position,
            "location": self.search_criteria.location,
            "proxy": {
                "useApifyProxy": True,
                "apifyProxyGroups": ["RESIDENTIAL"],
            },
        }
        logger.info(
            f"Fetching Indeed jobs for query='{self.search_criteria.position}', location='{self.search_criteria.location}'"
        )
        try:
            run = client.actor("apify/indeed-jobs-scraper").call(run_input=run_input)
            dataset_id = run["defaultDatasetId"]
            jobs = []
            for item in client.dataset(dataset_id).iterate_items():
                jobs.append(
                    {
                        "job_title": item.get("job_title", "Unknown Title"),
                        "company": item.get("company", "Unknown Company"),
                        "experience": self.search_criteria.experience,
                        "jobNature": self.search_criteria.jobNature,
                        "location": item.get("location", self.search_criteria.location),
                        "salary": item.get("salary", "Not Provided"),
                        "apply_link": item.get("apply_link", "No Link"),
                    }
                )
            logger.info(f"Fetched {len(jobs)} jobs from Indeed.")
            return jobs
        except Exception as e:
            logger.error(f"Error fetching Indeed jobs: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch Indeed jobs.")

    def fetch_linkedin_jobs(self):
        """
        Use Apify actor to fetch job listings from LinkedIn.
        Expected input parameters for the actor are assumed to be:
          - searchQuery: job title or keywords.
          - location: job location.
          - proxy settings.
        The actor should output items with keys that can be mapped to:
          "job_title", "company", "location", "salary", and "apply_link".
        """
        run_input = {
            "searchQuery": self.search_criteria.position,
            "location": self.search_criteria.location,
            "proxy": {
                "useApifyProxy": True,
                "apifyProxyGroups": ["RESIDENTIAL"],
            },
        }
        logger.info(
            f"Fetching LinkedIn jobs for query='{self.search_criteria.position}', location='{self.search_criteria.location}'"
        )
        try:
            run = client.actor("bebity/linkedin-jobs-scraper").call(run_input=run_input)
            dataset_id = run["defaultDatasetId"]
            jobs = []
            for item in client.dataset(dataset_id).iterate_items():
                jobs.append(
                    {
                        "job_title": item.get("job_title", "Unknown Title"),
                        "company": item.get("company", "Unknown Company"),
                        "experience": self.search_criteria.experience,
                        "jobNature": self.search_criteria.jobNature,
                        "location": item.get("location", self.search_criteria.location),
                        "salary": item.get("salary", "Not Provided"),
                        "apply_link": item.get("apply_link", "No Link"),
                    }
                )
            logger.info(f"Fetched {len(jobs)} jobs from LinkedIn.")
            return jobs
        except Exception as e:
            logger.error(f"Error fetching LinkedIn jobs: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to fetch LinkedIn jobs."
            )

    def fetch_optional_jobs(self):
        """
        Placeholder for any additional job sources.
        """
        logger.warning("Optional job scraper not implemented. Consider using an API.")
        raise NotImplementedError(
            "Optional job scraper not implemented. Use the official API or another method."
        )
