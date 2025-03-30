from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

NGROK_TOKEN = os.getenv("ngrok")
APIFY_TOKEN = os.getenv("apify")
LINKEDIN_ACTOR_ID = os.getenv("linkedin")
INDEED_ACTOR_ID = os.getenv("indeed")
GLASSDOOR_ACTOR_ID = os.getenv("glassdoor")