import sys
import os

# # Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# # No need for path modifications
from app.data.generators.jd_generator import JobDescriptionGenerator
# print("Project root:", project_root)
# print("work")

# print("work")

def main():
    generator = JobDescriptionGenerator()

    # Define domains and count per domain
    domains = [
        "Software Engineering",
        "Data Science", 
        "DevOps",
        "Machine Learning",
        "Quality Assurance",
        "Project Management",
        "Business Analytics"
    ]
    count_per_domain = 2
    result = generator.generate_job_descriptions(domains, count_per_domain)
    print(result)

if __name__ == "__main__":
    main()