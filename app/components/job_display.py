import streamlit as st
from typing import Dict, Any, List
import pandas as pd
from datetime import datetime

class JobDisplayComponent:
    def __init__(self):
        """Initialize the Job Display Component"""
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup custom CSS styles for job cards"""
        st.markdown("""
        <style>
            .job-card {
                border: 1px solid #e1e4e8;
                border-radius: 6px;
                padding: 16px;
                margin-bottom: 16px;
                background-color: #ffffff;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .job-card:hover {
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
            }
            .match-badge {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 12px;
                background-color: #4CAF50;
                color: white;
                font-size: 0.8em;
                font-weight: bold;
            }
            .job-title {
                color: #0366d6;
                margin-bottom: 4px;
            }
            .job-company {
                font-weight: 600;
                color: #24292e;
            }
            .job-meta {
                color: #586069;
                font-size: 0.9em;
                margin-bottom: 8px;
            }
            .job-section {
                margin-bottom: 12px;
            }
            .job-section-title {
                font-weight: 600;
                margin-bottom: 4px;
                color: #24292e;
            }
        </style>
        """, unsafe_allow_html=True)

    def render_job_card(self, job: Dict[str, Any], match_score: float = None, explanation: str = None):
        """
        Render a single job card with all details
        """
        with st.container():
            # Start job card with custom styling
            st.markdown('<div class="job-card">', unsafe_allow_html=True)

            # Header section with title and match percentage
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f'<div class="job-title">{job.get("title", "Job Title")}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="job-company">{job.get("company", "Company")}</div>', unsafe_allow_html=True)

            with col2:
                if match_score is not None:
                    st.markdown(f'<div class="match-badge">{match_score:.1f}% Match</div>', unsafe_allow_html=True)

            # Basic job metadata
            st.markdown(f"""
            <div class="job-meta">
                {job.get("location", "Location not specified")} |
                {job.get("employment_type", "Employment type not specified")} |
                {self._format_date(job.get("posted_date"))}
            </div>
            """, unsafe_allow_html=True)

            # Match explanation if available
            if explanation:
                with st.expander("Why this match?"):
                    st.info(explanation)

            # Tabs for different sections
            tab1, tab2, tab3 = st.tabs(["Description", "Requirements", "Details"])

            with tab1:
                self._render_job_description(job)

            with tab2:
                self._render_job_requirements(job)

            with tab3:
                self._render_job_details(job)

            # Apply button
            if job.get("apply_url"):
                st.markdown(f"""
                <a href="{job["apply_url"]}" target="_blank">
                    <button style="
                        background-color: #4CAF50;
                        color: white;
                        padding: 8px 16px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        cursor: pointer;
                        border: none;
                        border-radius: 4px;
                    ">
                        Apply Now
                    </button>
                </a>
                """, unsafe_allow_html=True)

            # End job card
            st.markdown('</div>', unsafe_allow_html=True)

    def _render_job_description(self, job: Dict[str, Any]):
        """Render job description section"""
        st.markdown('<div class="job-section">', unsafe_allow_html=True)
        st.markdown('<div class="job-section-title">Job Description</div>', unsafe_allow_html=True)

        description = job.get("description")
        if description:
            if isinstance(description, list):
                for item in description:
                    st.markdown(f"- {item}")
            else:
                st.markdown(description)
        else:
            st.markdown("No description provided")

        st.markdown('</div>', unsafe_allow_html=True)

    def _render_job_requirements(self, job: Dict[str, Any]):
        """Render job requirements section"""
        st.markdown('<div class="job-section">', unsafe_allow_html=True)
        st.markdown('<div class="job-section-title">Requirements</div>', unsafe_allow_html=True)

        requirements = job.get("requirements", [])
        if requirements:
            for req in requirements:
                st.markdown(f"- {req}")
        else:
            st.markdown("No requirements listed")

        st.markdown('</div>', unsafe_allow_html=True)

    def _render_job_details(self, job: Dict[str, Any]):
        """Render additional job details"""
        st.markdown('<div class="job-section">', unsafe_allow_html=True)
        st.markdown('<div class="job-section-title">Additional Details</div>', unsafe_allow_html=True)

        # Salary information
        salary = job.get("salary")
        if salary and isinstance(salary, dict):
            st.markdown(f"**Salary Range:** {salary.get('min', 'N/A')} - {salary.get('max', 'N/A')} {salary.get('currency', '')}")

        # Benefits
        benefits = job.get("benefits", [])
        if benefits:
            st.markdown("**Benefits:**")
            for benefit in benefits:
                st.markdown(f"- {benefit}")

        # Experience level
        experience = job.get("experience_level")
        if experience:
            st.markdown(f"**Experience Level:** {experience}")

        # Education requirements
        education = job.get("education")
        if education:
            st.markdown(f"**Education:** {education}")

        # Application deadline
        deadline = job.get("application_deadline")
        if deadline:
            st.markdown(f"**Application Deadline:** {self._format_date(deadline)}")

        st.markdown('</div>', unsafe_allow_html=True)

    def _format_date(self, date_str: str) -> str:
        """Format date string for display"""
        if not date_str:
            return "Date not specified"

        try:
            # Try parsing ISO format
            dt = datetime.fromisoformat(date_str)
            return dt.strftime("%b %d, %Y")
        except (ValueError, TypeError):
            return date_str

    def render_job_list(self, jobs: List[Dict[str, Any]], with_matches: bool = False):
        """
        Render a list of job cards
        """
        if not jobs:
            st.info("No jobs found matching your criteria")
            return

        st.subheader(f"Found {len(jobs)} matching jobs")

        for job_item in jobs:
            if with_matches and isinstance(job_item, dict) and 'job' in job_item:
                # This is a job match object with score and explanation
                self.render_job_card(
                    job=job_item['job'],
                    match_score=job_item.get('match_percentage'),
                    explanation=job_item.get('explanation')
                )
            else:
                # This is a regular job dictionary
                self.render_job_card(job=job_item)