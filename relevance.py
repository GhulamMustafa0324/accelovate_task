import json
from logger import get_logger
from transformers import AutoTokenizer, pipeline
import torch

logger = get_logger(__name__)


class LLMRanker:
    def __init__(self):
        logger.info("Loading Gemma 2 model for ranking...")
        print("Loading Gemma 2 model for ranking...")
        model_id = "google/gemma-2-2b-it"
        self.pipe = pipeline(
            "text-generation",
            model=model_id,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device="cuda" if torch.cuda.is_available() else "cpu",
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        logger.info("Gemma 2 model for ranking loaded successfully.")
        print("Gemma 2 model for ranking loaded successfully.")

    def rank_jobs(self, jobs, search_keywords):
        # Build a prompt that includes the query and the job details.
        print(search_keywords)
        query_text = f"{search_keywords.get('position', '')} {search_keywords.get('skills', '')} {search_keywords.get('experience', '')} {search_keywords.get('location', '')}"
        prompt = (
            "You are a helpful assitanct who will score the job listings against the searched job based on how similar they are and how close they match to, the scores must be in JSON and should be between 0 to 100 \n\n"
            "Example: {\"scores\": [100, 90, 80]}\n\n"
            f"Job Searched: {query_text}\n\n"
            "Job Listings:\n"
        )
        for idx, job in enumerate(jobs, 1):
            job_text = (
                f"Job {idx}: {job['job_title']} at {job['company']} in {job['location']}. "
                f"Experience required: {job['experience']}, Job Nature: {job['jobNature']}, Salary: {job['salary']}."
            )
            prompt += job_text + "\n"
        prompt += "\nONLY RETURN THE JSON OBJECT WITH SCORES VALUE."

        logger.info("Generating ranking scores using LLM with revised prompt...")
        print("Generating ranking scores using LLM with revised prompt...")
        try:
            outputs = self.pipe(prompt, max_new_tokens=1024)
            print(outputs)
            gen_text = outputs[0]["generated_text"][len(prompt) :]
            logger.info(f"Raw LLM ranking output: {gen_text}")
            print(f"Raw LLM ranking output: {gen_text}")

            # Extract the JSON block from the generated text.
            start = gen_text.find("{")
            end = gen_text.rfind("}") + 1
            json_text = gen_text[start:end]
            print("json", json_text)
            result = json.loads(json_text)
            # print("result",result)
            scores = result.get("scores", [])
        except Exception as e:
            logger.error(f"Failed to rank jobs using LLM: {e}")
            print(f"Failed to rank jobs using LLM: {e}")
            # Fallback: assign a default score of 50 for each job.
            scores = [50] * len(jobs)

        # Assign scores to each job.
        for i, job in enumerate(jobs):
            job["similarity"] = scores[i] if i < len(scores) else 50

        # Sort jobs by similarity score descending.
        ranked_jobs = sorted(jobs, key=lambda x: x["similarity"], reverse=True)
        logger.info("Job ranking via LLM completed.")
        print("Job ranking via LLM completed.")
        print(ranked_jobs)
        return ranked_jobs
