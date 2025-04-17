import streamlit as st
from app.utils.file_handling import FileHandler
from app.services.resume_service import ResumeService

class FileUploaderComponent:
    def __init__(self):
        """Initialize the File Uploader Component"""
        self.resume_service = ResumeService()

    def _format_experience(self, experience: dict) -> str:
        """Format experience dictionary into a clean string"""
        return f"""
        **{experience.get('title', 'Position')}** at *{experience.get('company', 'Company')}*
        *{experience.get('duration', 'Period')}*
        {experience.get('description', 'No description available')}
        """

    def _format_education(self, education: dict) -> str:
        """Format education dictionary into a clean string"""
        return f"""
        **{education.get('degree', 'Degree')}**
        *{education.get('institution', 'Institution')}*
        {education.get('year', 'Year')}
        """

    def render(self):
        """Render the file uploader component"""
        st.subheader("Upload Your Resume")

        uploaded_file = st.file_uploader(
            "Upload your resume (PDF, DOCX, DOC, TXT)",
            type=list(FileHandler.ALLOWED_EXTENSIONS)
        )

        if uploaded_file is not None:
            if st.button("Process Resume"):
                with st.spinner("Processing your resume..."):
                    # Create a unique filename
                    # file_extension = uploaded_file.name.split('.')[-1]
                    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    # filename = f"resume_{timestamp}.{file_extension}"
                    # Process the file
                    resume_data = self.resume_service.process_resume_bytes(
                        file_bytes=uploaded_file.getvalue(),
                        filename=uploaded_file.name
                    )

                    if resume_data:
                        if resume_data.get('is_valid_resume'):
                            st.success(f"Successfully processed resume for {resume_data.get('name', 'candidate')}")

                            # Store the processed resume data in session state
                            st.session_state.resume_data = resume_data
                            st.session_state.resume_processed = True

                            # Display a summary of extracted information
                            with st.expander("Resume Information", expanded=True):
                                st.write(f"**Name:** {resume_data.get('name', '')}")
                                st.write(f"**Email:** {resume_data.get('email', '')}")
                                st.write(f"**Phone:** {resume_data.get('phone', '')}")

                                # Skills section
                                st.write("---")
                                st.subheader("Skills")
                                skills = resume_data.get('skills', [])
                                if skills:
                                    cols = st.columns(4)
                                    for i, skill in enumerate(skills):
                                        cols[i % 4].write(f"• {skill}")
                                else:
                                    st.write("No skills extracted")

                               # Experience section
                                st.write("---")
                                st.subheader("Professional Experience")
                                experience = resume_data.get('experience', [])
                                if experience:
                                    for exp in experience:
                                        # Access attributes directly
                                        title = exp.title if hasattr(exp, 'title') else 'No title available'
                                        company = exp.company if hasattr(exp, 'company') else 'No company available'
                                        duration = exp.duration if hasattr(exp, 'duration') else 'No duration available'
                                        description = exp.description if hasattr(exp, 'description') else 'No description available'

                                        # Display with formatting
                                        st.markdown(
                                            f'<span style="color: #ff0000; text-decoration: underline; font-style: italic;">{title}</span>',
                                            unsafe_allow_html=True
                                        )
                                        st.markdown(f'<span style="color: #1e88e5">{company}</span>   -   <span style="color: #43a047">{duration}</span>',
                                                unsafe_allow_html=True)

                                        # Process description (split by newlines and add bullet points)
                                        if description:
                                            desc_lines = description.split('\n')
                                            for line in desc_lines:
                                                if line.strip():  # Only process non-empty lines
                                                    st.markdown(f"{line.strip()}")
                                        else:
                                            st.write("No description available")

                                        st.write("")
                                else:
                                    st.write("No experience extracted")

                                # Education section
                                st.write("---")
                                st.subheader("Education")
                                education = resume_data.get('education', [])
                                if education:
                                    for edu in education:
                                        degree = edu.degree if hasattr(edu, 'degree') else 'No title available'
                                        institution = edu.institution if hasattr(edu, 'institution') else 'No company available'
                                        year = edu.year if hasattr(edu, 'year') else 'No duration available'

                                         # Display with formatting
                                        st.markdown(
                                            f'<span style="color: #ff0000; text-decoration: underline; font-style: italic;">{degree}</span>',
                                            unsafe_allow_html=True
                                        )
                                        st.markdown(f'<span>{institution}</span>   -   <span style="color: #43a047">{year}</span>',
                                                unsafe_allow_html=True)
                                        st.write("")
                                else:
                                    st.write("No Education extracted")


                                # Certifications section
                                st.write("---")
                                st.subheader("Certifications")
                                certifications = resume_data.get('certifications', [])
                                if certifications:
                                    for cert in certifications:
                                        st.write(f"• {cert}")
                                else:
                                    st.write("No certifications listed")

                                # Projects section
                                st.write("---")
                                st.subheader("Projects")
                                projects = resume_data.get('projects', [])
                                if projects:
                                    for proj in projects:
                                        if isinstance(proj, dict):
                                            st.write(f"**{proj.get('name', 'Project')}**")
                                            st.write(proj.get('description', 'No description available'))
                                            st.write("")  # Add space between entries
                                        else:
                                            st.write(f"- {proj}")
                        else:
                            st.error(f"Invalid resume detected: {resume_data.get('validation_reason', 'Not a valid resume')}")
                            st.warning("Please upload a proper resume document with professional experience, education details, and skills.")
                    else:
                        st.error("Failed to process the resume. Please try again.")