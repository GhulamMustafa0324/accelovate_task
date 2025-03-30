import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from logger import get_logger

logger = get_logger(__name__)


class RelevanceRanker:
    def __init__(self):
        logger.info("Loading Sentence Transformer model...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device=self.device)
        logger.info(f"Model loaded on {self.device.upper()}")

    def get_embedding(self, text):
        """Generate embeddings for a given text."""
        if not text.strip():
            return np.zeros((384,))  # Return a zero vector if text is empty
        logger.info(
            f"Generating embedding for text: {text[:50]}..."
        )  # Log first 50 chars
        return self.model.encode(text, convert_to_numpy=True)

    def cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors."""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def rank_jobs(self, jobs, search_keywords):
        """Rank job listings based on similarity with user search criteria."""
        if not jobs:
            logger.warning("No job listings found to rank.")
            return []

        # Build a query string from formatted search keywords
        query_text = (
            f"{search_keywords.get('position', '')} {search_keywords.get('skills', '')}"
        )
        logger.info(f"Ranking jobs based on query: {query_text}")

        query_embedding = self.get_embedding(query_text)

        ranked_jobs = []
        for job in jobs:
            job_text = f"{job['job_title']} {job['company']} {job['location']} {job['experience']} {job['jobNature']}"
            job_embedding = self.get_embedding(job_text)
            similarity = self.cosine_similarity(query_embedding, job_embedding)
            job["similarity"] = similarity
            ranked_jobs.append(job)
            logger.info(f"Job: {job['job_title']} | Similarity: {similarity:.4f}")

        # Sort jobs in descending order of similarity
        ranked_jobs.sort(key=lambda x: x["similarity"], reverse=True)
        logger.info("Job ranking completed.")
        return ranked_jobs
