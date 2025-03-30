# Job Scraper with LLM-Powered Ranking

## Overview
This project is a job scraper that fetches job listings from LinkedIn, Indeed, and Glassdoor using Apify Actors. It also leverages a large language model (LLM) for job relevance ranking to help users find the most suitable job listings based on their search criteria. The API is built using FastAPI for efficient request handling.

## Features
- **Scraping Job Listings**: Uses Apify Actors to fetch jobs from LinkedIn, Indeed, and Glassdoor.
- **Job Relevance Ranking**: Employs Google's Gemma 2 LLM to rank jobs based on similarity to user search queries.
- **FastAPI Integration**: Provides a RESTful API for querying jobs and receiving ranked results.
- **Logging & Debugging**: Implements structured logging for debugging and performance tracking.
- **Configurable & Extensible**: Uses environment variables for API tokens and other configurations.
- **Customizable Search Criteria**: Users can provide specific keywords, experience levels, and locations.

## Installation


### Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/GhulamMustafa0324/accelovate_task.git
   cd accelovate_task
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up the `.env` file with required API tokens:
   ```ini
   NGROK=<YOUR_NGROK_TOKEN>
   APIFY=<YOUR_APIFY_TOKEN>
   LINKEDIN=<YOUR_LINKEDIN_ACTOR_ID>
   INDEED=<YOUR_INDEED_ACTOR_ID>
   GLASSDOOR=<YOUR_GLASSDOOR_ACTOR_ID>
   ```

## Running the API
Start the FastAPI server using Uvicorn:
```sh
uvicorn main:app --reload
```
The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Testing the Endpoint
You can test the API using the interactive Swagger UI available at:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Use a JSON payload similar to:
```json
{
   "position": "Full Stack Engineer",
   "experience": "2 years",
   "salary": "70,000 PKR to 120,000 PKR",
   "jobNature": "onsite",
   "location": "Peshawar, Pakistan",
   "skills": "full stack, MERN, Node.js, Express.js, React.js, Next.js, Firebase,
   TailwindCSS, CSS Frameworks, Tokens handling"
}

```

## Project Structure
```
├── main.py            # Entry point for the FastAPI application
├── config.py          # Loads environment variables
├── logger.py          # Configures logging
├── models.py          # Defines data models
├── scrapers.py        # Handles job scraping from LinkedIn, Indeed, and Glassdoor
├── colab/accelovate.ipynb # A notebook which can be directly run from google colab
├── llm_helpers.py     # Uses LLM to generate formatted search queries
├── relevance.py       # Uses LLM to rank jobs based on relevance
├── utils.py           # Utility functions for mapping experience levels
├── requirements.txt   # Dependencies
├── .env               # API tokens (not included in repo for security)
└── README.md          # Project documentation
```

## LLM-Powered Ranking
The `relevance.py` module utilizes the `google/gemma-2-2b-it` model to assess job relevance based on the search criteria provided by the user. The model extracts job keywords and assigns similarity scores to rank listings.

## Logging
The project includes structured logging via `logger.py` to keep track of operations, making debugging easier.


## License
MIT License.

