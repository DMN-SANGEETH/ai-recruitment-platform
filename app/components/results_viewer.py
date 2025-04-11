"""Result viewer"""
from typing import List, Dict, Any

import streamlit as st
import pandas as pd

class ResultsViewer:
    """Result view class"""
    def __init__(self):
        """Initialize the Results Viewer"""

    def render(self,
               matches: List[Dict[str, Any]]
               ):
        """Render the job matches results"""
        if not matches:
            st.warning("No matching jobs found")
            return

        st.subheader("Recommended Jobs")

        # Add download button for results
        self._add_download_button(matches)

        # Display each match
        for match in matches:
            self._render_match(match)

    def _render_match(self,
                      match: Dict[str, Any]
                      ):
        """Render a single job match"""
        job = match['job']
        score = match.get('match_percentage', 0)
        explanation = match.get('explanation', '')

        title_j = job.get('title', 'Job Title')
        with st.expander(f"{title_j} - {score:.1f}% Match", expanded=True):
            st.markdown(f"**Company:** {job.get('company', 'N/A')}")
            st.markdown(f"**Location:** {job.get('location', 'N/A')}")
            st.markdown(f"**Experience Level:** {job.get('experience_level', 'N/A')}")

            if explanation:
                st.markdown("**Why this match?**")
                st.info(explanation)

            # Tabs for different sections
            tab1, tab2, tab3 = st.tabs(["Description", "Requirements", "Details"])

            with tab1:
                st.subheader("Job Description")
                st.markdown(job.get('description', 'No description available'))

            with tab2:
                st.subheader("Requirements")
                # Benefits
                responsibilities = job.get('responsibilities', [])
                if responsibilities:
                    st.markdown("**Responsibilities:**")
                    for responsibility in responsibilities:
                        st.markdown(f"- {responsibility}")

                # Benefits
                required_skills = job.get('required_skills', [])
                if required_skills:
                    st.markdown("**Required Skills:**")
                    for required_skill in required_skills:
                        st.markdown(f"- {required_skill}")

                # Benefits
                education = job.get('education', [])
                if education:
                    st.markdown("**Education:**")
                    st.markdown(f"- {education}")

            with tab3:
                self._render_job_details(job)

    def _render_job_details(self,
                            job: Dict[str, Any]
                            ):
        """Render additional job details"""
        st.subheader("Additional Details")

        # Salary information
        salary = job.get('salary_range', {})
        if salary and isinstance(salary, dict):
            min_s = salary.get('min', 'N/A')
            max_s = salary.get('max', 'N/A')
            currency_s = salary.get('currency', '')
            st.markdown(f"**Salary Range:** {min_s} - {max_s} {currency_s}")

        # Application post date
        posted_date = job.get('posted_date')
        if posted_date:
            st.markdown(f"**Posted Date:** {posted_date}")

        # Application deadline
        deadline = job.get('application_deadline')
        if deadline:
            st.markdown(f"**Application Deadline:** {deadline}")

        # Application URL
        apply_url = job.get('apply_url')
        if apply_url:
            st.markdown(f"**Application LINK:** {apply_url}")

    def _add_download_button(self,
                             matches: List[Dict[str, Any]]
                             ):
        """Add button to download results as CSV"""
        if not matches:
            return

        # Prepare data for CSV
        csv_data = []
        for match in matches:
            job = match['job']
            csv_data.append({
                'Job Title': job.get('title', ''),
                'Company': job.get('company', ''),
                'Location': job.get('location', ''),
                'Match Score': f"{match.get('match_percentage', 0):.1f}%",
                'Key Skills': ', '.join(job.get('required_skills', [])),
                'Experience Level': job.get('experience_level', '')
            })

        df = pd.DataFrame(csv_data)

        st.download_button(
            label="Download Results as CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='job_matches.csv',
            mime='text/csv'
        )
