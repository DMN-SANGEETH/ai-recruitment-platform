from typing import List, Dict, Any
from scipy.spatial.distance import cosine
from app.db.mongodb.queries.jd_repository import JobDescriptionRepository
from app.db.mongodb.queries.resume_repository import ResumeRepository
from app.core.rag.embeddings import EmbeddingGenerator
from app.utils.logger import logger
import google.generativeai as genai
from app.utils.config import MongoDBConfig


class JobMatcher:
    def __init__(self):
        """Initialize the Job Matcher with client-side vector search"""
        self.jd_repository = JobDescriptionRepository()
        self.resume_repository = ResumeRepository()
        self.embedding_generator = EmbeddingGenerator()

        # Initialize Gemini for explanations
        genai.configure(api_key=MongoDBConfig.get_gemini_api_key())
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def _cosine_similarity(self, vec_a: List[float],
                           vec_b: List[float]
                           ) -> float:
        """Calculate cosine similarity between two vectors"""
        return 1 - cosine(vec_a, vec_b)

    def match_resume_to_jobs(self, resume_data: Dict[str, Any],
                             limit: int = 5) -> List[Dict[str, Any]]:
        """Match a resume to job descriptions using client-side vector
        similarity"""
        try:
            # Ensure we have embeddings for the resume
            if "embedding" not in resume_data or not resume_data["embedding"]:
                resume_data["embedding"] = self.embedding_generator.create_resume_embedding(resume_data)
                if '_id' in resume_data:
                    self.resume_repository.update(
                        resume_data['_id'],
                        {'embedding': resume_data['embedding']}
                    )

            # Get all job descriptions with embeddings
            all_jobs = self.jd_repository.get_all_with_embeddings()

            # Calculate similarities
            results = []
            for job in all_jobs:
                if not job.get('embedding'):
                    continue

                similarity = self._cosine_similarity(resume_data["embedding"], job['embedding'])
                results.append({
                    "job": job,
                    "score": similarity
                })

            # Sort by score and get top results
            sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)[:limit]

            # Enhance results with match explanations
            enhanced_results = []
            for result in sorted_results:
                job = result["job"]
                score = result["score"]

                explanation = self._generate_match_explanation(resume_data, job)

                enhanced_results.append({
                    "job": job,
                    "score": score,
                    "match_percentage": round(score * 100, 2),
                    "explanation": explanation
                })

            return enhanced_results

        except Exception as e:
            logger.error(f"Error in matching resume to jobs: {str(e)}", exc_info=True)
            return []

    def _generate_match_explanation(self, resume: Dict, job: Dict) -> str:
        """Generate a natural language explanation of the match"""
        try:
            prompt = f"""
            Explain why this resume is a good match for the job position.

            Resume Summary:
            {resume.get('summary', 'No summary available')}

            Key Skills:
            {', '.join(resume.get('skills', []))}

            Job Title:
            {job.get('title', 'Unknown')}

            Job Requirements:
            {', '.join(job.get('required_skills', []))}

            Provide a concise 2-3 sentence explanation focusing on the most relevant matches between the resume and job requirements.
            """
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating match explanation: {str(e)}")
            return "Match explanation not available"