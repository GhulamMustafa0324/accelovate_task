import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from logger import get_logger

logger = get_logger(__name__)


class LLMHelper:
    def __init__(self):
        logger.info("Loading LLM Model: SmolLM2-1.7B-Instruct...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            "HuggingFaceTB/SmolLM2-1.7B-Instruct"
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            "HuggingFaceTB/SmolLM2-1.7B-Instruct"
        )

        # Move model to GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        logger.info(f"LLM Model loaded successfully on {self.device.upper()}")

    def format_search_keywords(self, search_request):
        logger.info(
            f"Formatting search keywords for position: {search_request.position}"
        )

        prompt = f"""
        Extract and format the relevant keywords from the following job search request.
        Return a JSON object with keys: "position", "experience", "location", and "skills".
        
        Input:
        Position: {search_request.position}
        Experience: {search_request.experience}
        Salary: {search_request.salary}
        Job Nature: {search_request.jobNature}
        Location: {search_request.location}
        Skills: {search_request.skills}
        """

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        logger.info("Generating response from LLM...")

        outputs = self.model.generate(**inputs, max_new_tokens=100)
        output_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.info(f"Raw LLM Output: {output_text}")

        try:
            keywords = json.loads(output_text)
            logger.info(f"Formatted Keywords: {keywords}")
        except json.JSONDecodeError:
            logger.warning(
                "Failed to parse JSON response from LLM, using fallback values."
            )
            keywords = {
                "position": search_request.position,
                "experience": search_request.experience,
                "location": search_request.location,
                "skills": search_request.skills,
            }

        return keywords
