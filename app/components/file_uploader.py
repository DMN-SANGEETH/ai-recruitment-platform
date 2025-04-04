import streamlit as st
import os
from datetime import datetime
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
                    file_bytes = uploaded_file.getvalue()
                    resume_data = self.resume_service.process_resume_bytes(
                        file_bytes=file_bytes,
                        filename=uploaded_file.name
                        )
                    
                    if resume_data:
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
                                    if isinstance(exp, dict):
                                        st.markdown(self._format_experience(exp))
                                        st.write("")  # Add space between entries
                                    else:
                                        st.write(f"- {exp}")
                            else:
                                st.write("No experience extracted")
                            
                            # Education section
                            st.write("---")
                            st.subheader("Education")
                            education = resume_data.get('education', [])
                            if education:
                                for edu in education:
                                    if isinstance(edu, dict):
                                        st.markdown(self._format_education(edu))
                                        st.write("")  # Add space between entries
                                    else:
                                        st.write(f"- {edu}")
                            
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
                        st.error("Failed to process the resume. Please try again.")