import json
import torch
from transformers import pipeline, AutoTokenizer
from models import JobSearchRequest
from logger import get_logger

logger = get_logger(__name__)


class LLMHelper:
    def __init__(self):
        logger.info("Loading Gemma 2 model for text generation...")
        print("Loading Gemma 2 model for text generation...")
        model_id = "google/gemma-2-2b-it"
        self.pipe = pipeline(
            "text-generation",
            model=model_id,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device="cuda" if torch.cuda.is_available() else "cpu",
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        logger.info("Gemma 2 model loaded successfully.")
        print("Gemma 2 model loaded successfully.")

    def format_search_keywords(self, search_request: JobSearchRequest):
        print(search_request)
        prompt = f"""
Extract and format the relevant keywords from the following job search request. Keep location but also add Country and City.
Return a JSON object with keys: "position", "experience", "location", "country", "city" and "skills".

Input:
Position: {search_request.position}
Experience: {search_request.experience}
Salary: {search_request.salary}
Job Nature: {search_request.jobNature}
Location: {search_request.location}
Skills: {search_request.skills}

NOTE: Only Provide JSON OUTPUT
"""
        logger.info("Generating formatted keywords using Gemma 2...")
        print("Generating formatted keywords using Gemma 2...")
        try:
            outputs = self.pipe(prompt, max_new_tokens=100)
            gen_text = outputs[0]["generated_text"][len(prompt) :]
            logger.info(f"Raw Gemma 2 output: {gen_text}")
            print(f"Raw Gemma 2 output: {gen_text}")
            # Try to extract the JSON part from the generated text
            start = gen_text.find("{")
            end = gen_text.rfind("}") + 1
            json_text = gen_text[start:end]
            keywords = json.loads(json_text)
            logger.info(f"Formatted Keywords: {keywords}")
            print(f"Formatted Keywords: {keywords}")
        except Exception as e:
            logger.warning(
                f"Failed to parse JSON response from Gemma 2, using fallback values: {e}"
            )
            print(
                f"Failed to parse JSON response from Gemma 2, using fallback values: {e}"
            )
            keywords = {
                "position": search_request.position,
                "experience": search_request.experience,
                "location": search_request.location,
                "skills": search_request.skills,
                "salary": search_request.salary,
                "jobNature": search_request.jobNature,
            }
        return keywords
