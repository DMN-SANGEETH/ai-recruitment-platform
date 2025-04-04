from typing import Dict, Any, List
from app.db.mongodb.queries.jd_repository import JobDescriptionRepository
from app.core.matching.matcher import JobMatcher
from app.utils.logger import logger

class JobService:
    def __init__(self):
        """Initialize the Job Service"""
        self.repository = JobDescriptionRepository()
        self.matcher = JobMatcher()
        
    def get_job_by_id(self, job_id: str) -> Dict[str, Any]:
        """Get a job description by ID"""
        try:
            job = self.repository.find_by_id(job_id)
            if job:
                return job.model_dump()
            return None
        except Exception as e:
            logger.error(f"Error getting job by ID: {str(e)}")
            return None
    
    def get_jobs_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        """Get job descriptions by domain"""
        try:
            jobs = self.repository.find_by_domain(domain)
            return [job.model_dump() for job in jobs]
        except Exception as e:
            logger.error(f"Error getting jobs by domain: {str(e)}")
            return []
    
    def get_all_jobs(self, limit: int = 100, skip: int = 0) -> List[Dict[str, Any]]:
        """Get all job descriptions"""
        try:
            jobs = self.repository.find_many({}, limit=limit, skip=skip)
            return [job.model_dump() for job in jobs]
        except Exception as e:
            logger.error(f"Error getting all jobs: {str(e)}")
            return []
    
    def get_job_matches_for_resume(self, resume_data: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
        """Get job recommendations for a resume"""
        try:
            matches = self.matcher.match_resume_to_jobs(resume_data, limit)

            # Convert matches to a format suitable for the UI
            formatted_matches = []
            for match in matches:
                job = match['job']
                if hasattr(job, 'model_dump'):
                    job_data = job.model_dump()
                else:
                    job_data = job
                
                formatted_matches.append({
                    'job': job_data,
                    'score': match['score'],
                    'match_percentage': match['match_percentage'],
                    'explanation': match['explanation']
                })
            
            return formatted_matches
        except Exception as e:
            logger.error(f"Error getting job matches for resume: {str(e)}")
            return []
    
    def search_jobs_by_keyword(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for jobs by keyword in title or skills"""
        try:
            # Search in title field
            title_query = {"title": {"$regex": keyword, "$options": "i"}}
            title_results = self.repository.find_many(title_query, limit=limit//2)
            
            # Search in required_skills field
            skills_query = {"required_skills": {"$regex": keyword, "$options": "i"}}
            skills_results = self.repository.find_many(skills_query, limit=limit//2)
            
            # Combine results and remove duplicates
            combined_results = title_results + skills_results
            unique_jobs = {job.id: job for job in combined_results}
            
            return [job.model_dump() for job in unique_jobs.values()][:limit]
            
        except Exception as e:
            logger.error(f"Error searching jobs by keyword: {str(e)}")
            return []