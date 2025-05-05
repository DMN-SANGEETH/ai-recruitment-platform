JD_GENERATION_TEMPLATE = """
            Generate {count} realistic job description for the {domain} domain name.
            This is important: Ensure the output is valid JSON. Each job description should be a JSON object with the following keys:
            - Job title (use field name 'title', "title" (string))
            - {domain} need to include
            - Job description (Detailed job "description" matching {domain} and title requirements)
            - Company ("company" name posting this job)
            - Technology requirement (some service providers required for specific {domain}, "technology" (array of strings))
            - Location (mix of remote and in-person, on-site, hybrid,"location" (string))
            - 5-7 Key responsibilities (use field name 'responsibilities',"responsibilities" (array of strings))
            - 5-10 required skills (use field name 'required_skills',"required_skills" (array of strings))
            - Experience level requirement (use field name 'experience_level',"experience_level" (string))
            - Education requirement (use field name 'education',"education" (string))
            - Salary range (as min and max values, use field name 'salary_range', e.g. {{"min": 80000, "max": 120000}})
            - Posted Date (use field name 'posted_date', format "YYYY/MM/DD", e.g. "2025/04/05")
            - Application deadline (use field name 'application_deadline', format "YYYY/MM/DD", e.g. "2025/05/05")
            - Apply URL (use field name 'apply_url', e.g. "https://company.com/careers/job-123")

            Format as a JSON array with each job as an object. *Do not include any Markdown or formatting outside of the JSON.*
            Ensure all field names are consistent and match exactly as specified above.
            """

RESUME_PROCESSOR_TEMPLATE = """
            Extract structured information from the following resume text.
            Return the result as a valid JSON object with the following fields:
            - name (string): Full name of the candidate
            - email (string): Email address
            - phone (string): Phone number
            - summary (string): Professional summary or objective
            - skills (array of strings): Technical and soft skills
            - experience (array of objects): Work history with the following fields for each entry:
                - title (string): Job title
                - company (string): Company name
                - duration (string): Employment period
                - description (string): Job responsibilities and achievements
            - education (array of objects): Educational background with the following fields for each entry:
                - degree (string): Degree or certification name
                - institution (string): School or university name
                - year (string): Graduation year
            - certifications (array of strings): Professional certifications
            - projects (array of objects): Notable projects with the following fields for each:
                - name (string): Project name
                - description (string): Project details
            - is_valid_resume (boolean): True if document contains resume data, False if not a resume

            Resume text:
            {resume_text}
            Format as a JSON object. Ensure all field names are lowercase. Do not include any explanations, just return the JSON.
            Set is_valid_resume=False for:
            - Non-resume documents
            - Extremely poor quality resumes
            - 'Documents with' <30% 'resume content'
        """

RESUME_VALIDATION_TEMPLATE = """
            You are a resume validation expert. Your task is to determine whether the provided
            text is a resume or any other type of content include or not a cv or resume.

            Text to validate:
            ```
            {text}
            ```

            Examine whether this text has the structure and content typically found in a resume, such as:
            - Personal information (name, contact details)
            - Professional experience or work history(optional)
            - Education details
            - Skills section
            - Optional sections like projects, certifications, or objective statement

            Provide your analysis in JSON format with these fields:
            - is_valid_resume: boolean (true if it's a valid resume, false otherwise)
            - reason: string (brief explanation of your decision)
            if include un-match data that is not a resume

            Response format:
            ```json
            {{
            "is_valid_resume": true/false,
            "reason": "Your explanation here"
            }}
            ```
            """

LINKEDIN_VALIDATION_TEMPLATE = """
            You are a professional profile validation expert analyzing LinkedIn profile data. Evaluate the following content:

            {text}

            Analysis Criteria:
            1. REQUIRED FIELDS (at least 2 must be present):
            - Name fields (first_name/last_name/full_name)
            - Professional headline or position
            - Work experiences or education

            2. OPTIONAL FIELDS (nice to have but not required):
            - About/summary
            - Location
            - Skills
            - Contact info
            - Profile URL

            3. ACCEPTABLE FORMATS:
            - Raw database records with professional info
            - JSON-like structures
            - Machine-readable formats
            - Null/empty fields are acceptable

            Validation Rules:
            - Consider it valid if it contains professional information, even if not human-readable
            - Missing optional fields should not invalidate the profile
            - Empty arrays (like education=[]) are acceptable

            Response Format (STRICT JSON):
            {{
                "is_valid_profile": boolean,
                "reason": "Brief explanation",
                "missing_critical_fields": ["field1", "field2"]  // only if profile is invalid
            }}

            Example Valid Responses:
            {{
                "is_valid_profile": true,
                "reason": "Profile contains name, headline, and work experience",
                "missing_critical_fields": []
            }}

            {{
                "is_valid_profile": false,
                "reason": "Missing both name and professional information",
                "missing_critical_fields": ["name", "professional_info"]
            }}
            """
