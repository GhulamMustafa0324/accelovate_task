# from fastapi import FastAPI, HTTPException
# from models import JobSearchRequest, JobSearchResponse, JobDetail
# from scrapers import JobScraper
# from llm_helpers import LLMHelper
# from relevance import RelevanceRanker
# from logger import get_logger

# app = FastAPI(title="Job Finder API")
# logger = get_logger(__name__)


# @app.post("/search", response_model=JobSearchResponse)
# async def search_jobs(search_request: JobSearchRequest):
#     try:
#         logger.info("Received a job search request.")

#         # Step 1: Format search keywords via the local LLM
#         logger.info("Formatting search keywords using LLM.")
#         llm_helper = LLMHelper()
#         formatted_keywords = llm_helper.format_search_keywords(search_request)
#         logger.info(f"Formatted Keywords: {formatted_keywords}")

#         # Step 2: Fetch job listings from available sources
#         scraper = JobScraper(search_request)

#         logger.info("Fetching job listings from Indeed...")
#         indeed_jobs = scraper.fetch_indeed_jobs()
#         logger.info(f"Fetched {len(indeed_jobs)} jobs from Indeed.")

#         linkedin_jobs = []
#         try:
#             logger.info("Fetching job listings from LinkedIn...")
#             linkedin_jobs = scraper.fetch_linkedin_jobs()
#             logger.info(f"Fetched {len(linkedin_jobs)} jobs from LinkedIn.")
#         except NotImplementedError:
#             logger.warning("LinkedIn integration is pending.")

#         optional_jobs = []
#         try:
#             logger.info("Fetching job listings from an optional source...")
#             optional_jobs = scraper.fetch_optional_jobs()
#             logger.info(f"Fetched {len(optional_jobs)} jobs from optional source.")
#         except NotImplementedError:
#             logger.warning("Optional job source integration is pending.")

#         # Combine all jobs
#         all_jobs = indeed_jobs + linkedin_jobs + optional_jobs
#         logger.info(f"Total jobs fetched: {len(all_jobs)}")

#         if not all_jobs:
#             logger.warning("No job listings found.")
#             return {"relevant_jobs": []}

#         # Step 3: Rank jobs based on relevance
#         logger.info("Ranking jobs based on relevance.")
#         ranker = RelevanceRanker()
#         ranked_jobs = ranker.rank_jobs(all_jobs, formatted_keywords)
#         logger.info(
#             f"Ranking complete. Top job title: {ranked_jobs[0]['job_title']}"
#             if ranked_jobs
#             else "No relevant jobs found."
#         )

#         # Step 4: Return the top result
#         top_jobs = ranked_jobs[:1]  # Return only the best match
#         job_details = [JobDetail(**job) for job in top_jobs]

#         logger.info(f"Returning {len(job_details)} best job(s).")
#         return {"relevant_jobs": job_details}

#     except Exception as e:
#         logger.error(f"Error occurred: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=500, detail=str(e))


# if __name__ == "__main__":
#     import uvicorn

#     logger.info("Starting Job Finder API server...")
#     uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI, HTTPException
from models import JobSearchRequest, JobSearchResponse, JobDetail
from scrapers import JobScraper
from llm_helpers import LLMHelper
from relevance import RelevanceRanker
from logger import get_logger

app = FastAPI(title="Job Finder API")

logger = get_logger(__name__)

@app.post("/search", response_model=JobSearchResponse)
async def search_jobs(search_request: JobSearchRequest):
    try:
        logger.info("Received a job search request.")

        # Step 1: Format search keywords using the local LLM
        llm_helper = LLMHelper()
        formatted_keywords = llm_helper.format_search_keywords(search_request)
        logger.info(f"Formatted Keywords: {formatted_keywords}")

        # Step 2: Fetch job listings using Apify API via the JobScraper
        scraper = JobScraper(search_request)

        indeed_jobs = scraper.fetch_indeed_jobs()
        linkedin_jobs = scraper.fetch_linkedin_jobs()

        # Uncomment and implement if you wish to add another source.
        # optional_jobs = scraper.fetch_optional_jobs()

        all_jobs = indeed_jobs + linkedin_jobs
        logger.info(f"Total jobs fetched: {len(all_jobs)}")

        if not all_jobs:
            logger.warning("No job listings found.")
            return {"relevant_jobs": []}

        # Step 3: Rank jobs based on relevance
        ranker = RelevanceRanker()
        ranked_jobs = ranker.rank_jobs(all_jobs, formatted_keywords)
        logger.info(
            f"Ranking complete. Top job title: {ranked_jobs[0]['job_title']}"
            if ranked_jobs
            else "No relevant jobs found."
        )

        # Step 4: Return the top result
        top_jobs = ranked_jobs[:1]  # Return only the best match
        job_details = [JobDetail(**job) for job in top_jobs]

        logger.info(f"Returning {len(job_details)} best job(s).")
        return {"relevant_jobs": job_details}

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Job Finder API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
