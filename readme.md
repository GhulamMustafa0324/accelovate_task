# Job Finder API

This project is a Job Finder API that accepts job search criteria from the user, fetches job listings from online sources, and returns the best match based on semantic relevance. The API is built using FastAPI and leverages open-source models for natural language processing.

## Project Structure

```
job_finder/
 ├── main.py
 ├── models.py
 ├── scrapers.py
 ├── llm_helpers.py
 ├── relevance.py
 ├── .gitignore
 ├── requirements.txt
 └── README.md
```

- **main.py**: The entry point of the FastAPI application.
- **models.py**: Defines Pydantic models for request and response data.
- **scrapers.py**: Contains scraper classes for fetching job listings (Indeed is implemented; others can be added).
- **llm_helpers.py**: Uses Hugging Face’s SmolLM2-1.7B-Instruct model to format user input into search keywords.
- **relevance.py**: Ranks job posts based on semantic similarity using Sentence Transformers.
- **.gitignore**: Specifies files and directories to ignore in Git.
- **requirements.txt**: Lists project dependencies.
- **README.md**: This file.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://your-repo-url.git
   cd job_finder
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     venv\Scripts\activate
     ```

4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Running the API

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Testing the Endpoint

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
  "skills": "full stack, MERN, Node.js, Express.js, React.js, Next.js, Firebase, TailwindCSS, CSS Frameworks, Tokens handling"
}
```

## Notes

- **Scrapers:** The Indeed scraper is implemented as an example. For platforms like LinkedIn, it is recommended to use the official API or approved methods.
- **LLM & Embeddings:** The project uses Hugging Face’s SmolLM2-1.7B-Instruct model for keyword formatting and Sentence Transformers for semantic similarity ranking.
- **Extensibility:** The project is structured using object-oriented principles to make it easy to add more sources or improve the relevance ranking logic.

## License

This project is open-source. Feel free to modify and extend it as needed.
