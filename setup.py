from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ai_recruitment_platform",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,  # Auto-read from requirements.txt
    python_requires=">=3.8",       # Specify Python version
)