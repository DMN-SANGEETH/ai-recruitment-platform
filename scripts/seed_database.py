import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from app.data.generators.jd_generator import JobDescriptionGenerator

def main():
    """Generate datasets"""
    generator = JobDescriptionGenerator()

    domains = [
        "Software Engineering",
        "Data Science",
        "DevOps",
        "Machine Learning",
        "Quality Assurance",
        "Project Management",
        "Business Analytics"
    ]
    count_per_domain = 15
    result = generator.generate_job_descriptions(domains, count_per_domain)
    print(result)

if __name__ == "__main__":
    main()
