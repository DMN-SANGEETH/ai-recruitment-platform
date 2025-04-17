"""Main module for the AI-Powered Recruitment Platform Streamlit app."""

import sys
from pathlib import Path
import streamlit as st
from .components.file_uploader import FileUploaderComponent
from .components.results_viewer import ResultsViewer
from .services.job_service import JobService
# Ensure app modules can be imported
sys.path.append(str(Path(__file__).parent.parent))


def main():
    """Main entry point of the Streamlit app."""
    st.set_page_config(
        page_title="AI Recruitment Platform",
        page_icon="💼",
        layout="wide"
    )

    st.title("AI-Powered Recruitment Platform")
    st.markdown("Upload your resume to find matching job opportunities")

    # Initialize services and components
    uploader = FileUploaderComponent()
    results_viewer = ResultsViewer()
    job_service = JobService()

    # File upload section
    uploader.render()

    # Process and display results if resume is processed
    if st.session_state.get('resume_processed', False):
        resume_data = st.session_state.get('resume_data')

        if resume_data:
            with st.spinner("Finding matching jobs..."):
                matches = job_service.get_job_matches_for_resume(resume_data)
                results_viewer.render(matches)


if __name__ == "__main__":
    main()
