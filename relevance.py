import json
from logger import get_logger
from transformers import AutoTokenizer, pipeline
import torch

logger = get_logger(__name__)


from sentence_transformers import SentenceTransformer, util
import torch


class LLMRanker:
    def __init__(self):
        logger.info("Loading embedding model for ranking...")
        # Load a SentenceTransformer model for generating embeddings.
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("Embedding model loaded successfully.")

    def rank_jobs(self, jobs, search_keywords):
        # Build the query string from the search keywords.
        query_text = f"{search_keywords.get('position', '')} {search_keywords.get('skills', '')} {search_keywords.get('experience', '')} {search_keywords.get('location', '')}"
        logger.info(f"Ranking jobs using query: {query_text}")
        print(f"Ranking jobs using query: {query_text}")

        # Generate the embedding for the query.
        query_embedding = self.embedding_model.encode(
            query_text, convert_to_tensor=True
        )

        # Prepare a list to hold job descriptions.
        job_texts = []
        for job in jobs:
            job_text = (
                f"{job['job_title']} at {job['company']} in {job['location']}. "
                f"Experience required: {job['experience']}, Job Nature: {job['jobNature']}, Salary: {job['salary']}."
            )
            job_texts.append(job_text)

        # Generate embeddings for all job texts.
        job_embeddings = self.embedding_model.encode(job_texts, convert_to_tensor=True)

        # Compute cosine similarities between the query and each job.
        cosine_scores = util.cos_sim(query_embedding, job_embeddings)[0]

        # Assign similarity scores to each job (scaled between 0 and 100).
        for idx, job in enumerate(jobs):
            # Convert cosine similarity (range -1 to 1) to a positive scale.
            # Since our embeddings typically yield positive similarities, a simple scaling works.
            job["similarity"] = float(cosine_scores[idx].item() * 100)

        # Sort jobs by similarity in descending order.
        ranked_jobs = sorted(jobs, key=lambda x: x["similarity"], reverse=True)
        logger.info("Job ranking via embeddings completed.")
        print("Job ranking via embeddings completed.")
        return ranked_jobs
