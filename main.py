from fastapi import FastAPI, HTTPException
from models import JobSearchRequest, JobSearchResponse, JobDetail
from llm_helper import LLMHelper
from llm_ranker import LLMRanker
from job_scraper import JobScraper
from pyngrok import ngrok
import nest_asyncio
import uvicorn
from config import NGROK_TOKEN
from logger import get_logger

logger = get_logger(__name__)

ngrok.set_auth_token(NGROK_TOKEN)

app = FastAPI(title="Job Finder API")


@app.post("/search", response_model=JobSearchResponse)
async def search_jobs(search_request: JobSearchRequest):
    try:
        logger.info("Received a job search request.")
        print("Received a job search request.")

        # Step 1: Format search keywords using the local LLM
        llm_helper = LLMHelper()
        formatted_keywords = llm_helper.format_search_keywords(search_request)

        logger.info(f"Formatted Keywords: {formatted_keywords}")
        print(f"Formatted Keywords: {formatted_keywords}")

        # Step 2: Fetch job listings using Apify API via the JobScraper
        scraper = JobScraper(formatted_keywords)

        # You can enable indeed_jobs if needed
        indeed_jobs = scraper.fetch_indeed_jobs()
        linkedin_jobs = scraper.fetch_linkedin_jobs()
        glassdoor_jobs = scraper.fetch_glassdoor_jobs()

        # For this example, we use only LinkedIn jobs
        all_jobs = linkedin_jobs + indeed_jobs + glassdoor_jobs
        logger.info(f"Total jobs fetched: {len(all_jobs)}")
        print(f"Total jobs fetched: {len(all_jobs)}")

        if not all_jobs:
            logger.warning("No job listings found.")
            print("No job listings found.")
            return {"relevant_jobs": []}

        # Step 3: Rank jobs based on relevance
        ranker = LLMRanker()
        ranked_jobs = ranker.rank_jobs(all_jobs, formatted_keywords)
        if ranked_jobs:
            logger.info(
                f"Ranking complete. Top job title: {ranked_jobs[0]['job_title']}"
            )
            print(f"Ranking complete. Top job title: {ranked_jobs[0]['job_title']}")
        else:
            logger.info("No relevant jobs found after ranking.")
            print("No relevant jobs found after ranking.")

        # Step 4: Return the top result
        top_jobs = ranked_jobs[:10]  # Return only the best match
        job_details = [JobDetail(**job) for job in top_jobs]

        logger.info(f"Returning {len(job_details)} best job(s).")
        print(f"Returning {len(job_details)} best job(s).")
        return {"relevant_jobs": job_details}

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------
# Main: Run FastAPI with Ngrok in Colab
# ----------------------------
if __name__ == "__main__":
    # Allow nested event loops (required in Colab)
    nest_asyncio.apply()

    # Set the port number for uvicorn
    port = 8000

    # Open an ngrok tunnel to the specified port
    public_url = ngrok.connect(port).public_url
    logger.info(f"Ngrok tunnel available at: {public_url}")
    print(f" * ngrok tunnel available at: {public_url}")

    # Run the FastAPI app with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
