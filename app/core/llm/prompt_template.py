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
            - first name (string): First name of the candidate
            - last name (string): Last name of the candidate
            - name (string): Full name of the candidate
            - email (string): Email address
            - linkedin_url (string): LinkedIn url of the candidate(it should be start and arrange like this format https://www.linkedin.com/in/..)
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

# RESUME_LINKEDIN_PROCESSOR_TEMPLATE = """
#             Input Data:
#             LinkedIn: {linkedin_profile}
#             Process resume and LinkedIn data to create a merged profile with these REQUIRED FEATURES:

#             1. PROFILE MERGING LOGIC (CORE OUTPUT STRUCTURE):
            
            
#             {"merged_profile": {
#                 "personal_info": {
#                 "final_name": {"value": str, "source": "resume/linkedin/combined", "confidence": float},
#                 "final_contact": {
#                     "email": {"value": str, "source": "resume/linkedin", "valid": bool},
#                     "phone": {"value": str, "source": "resume/linkedin", "formatted": bool}
#                 }
#                 },
#                 "employment": [{
#                 "merged_record": {
#                     "title": {"value": str, "source": "resume/linkedin/combined", "resolution_method": str},
#                     "company": {"value": str, "normalized_name": str, "source": "resume/linkedin"},
#                     "duration": {"value": str, "source": "resume/linkedin/combined"},
#                     "is_current": bool
#                 },
#                 "conflict_resolution": {
#                     "type": "title_discrepancy/date_gap/company_variation",
#                     "resolution_strategy": "used_resume/used_linkedin/combined/flagged",
#                     "confidence_score": float
#                 }
#                 }]
#             },

#             # EXPLICIT CONFLICT RESOLUTION SECTION
#             "conflict_analysis": {
#                 "total_conflicts": int,
#                 "resolved_conflicts": [
#                 {
#                     "field": str,
#                     "resume_value": str,
#                     "linkedin_value": str,
#                     "resolution": str,
#                     "auto_resolved": bool
#                 }
#                 ],
#                 "unresolved_conflicts": [
#                 {
#                     "field": str,
#                     "resume_value": str,
#                     "linkedin_value": str,
#                     "required_manual_review": bool
#                 }
#                 ]
#             },

#             # EXPLICIT DATA VALIDATION SECTION
#             "data_validation": {
#                 "valid_fields": {
#                 "resume": [{"field": str, "validation_passed": bool}],
#                 "linkedin": [{"field": str, "validation_passed": bool}]
#                 },
#                 "invalid_fields": {
#                 "resume": [{"field": str, "issue": str}],
#                 "linkedin": [{"field": str, "issue": str}]
#                 },
#                 "completeness_scores": {
#                 "resume": float,
#                 "linkedin": float
#                 }
#             },

#             # EXPLICIT QUALITY ANALYSIS SECTION
#             "quality_analysis": {
#                 "profile_consistency": {
#                 "score": float,
#                 "inconsistencies": [str]
#                 },
#                 "ats_compatibility": {
#                 "score": float,
#                 "missing_keywords": [str]
#                 },
#                 "improvement_recommendations": [
#                 {
#                     "area": "summary/experience/skills",
#                     "suggestion": str,
#                     "priority": "high/medium/low"
#                 }
#                 ]
#             }
#             }

#             2. PROCESSING RULES:
#             - MERGING: Prefer resume for names/education dates, LinkedIn for current positions
#             - CONFLICTS: Auto-resolve minor differences (<30 present dissimilarity), flag major ones
#             - VALIDATION: Verify emails, phone formats, date sequences, institution names
#             - QUALITY: Check for skills gaps, employment gaps, ATS keywords

#             3. REQUIRED OUTPUTS:
#             - Must include all four sections: merged_profile, conflict_analysis, data_validation, quality_analysis
#             - Every field must indicate its data source
#             - All conflicts must be documented with resolution method
#             - All validations must include pass/fail status

#             Return ONLY this complete JSON structure.
#             """
            
RESUME_LINKEDIN_PROCESSOR_TEMPLATE = """
            Analyze the provided resume and LinkedIn profile separately, then create a merged profile with conflict resolution.

            Processing Instructions:

            1. First extract these fields SEPARATELY for both resume and LinkedIn:

            BASIC INFORMATION:
            - Full name
            - Email address
            - Phone number
            - LinkedIn URL
            - Location
            - Professional summary

            PROFESSIONAL DETAILS:
            - Skills (list)
            - Work experience (list with: job title, company, dates, description)
            - Education (list with: degree, institution, year)
            - Certifications
            - Projects
            - Languages

            2. Then create a MERGED PROFILE showing:
            - Combined data where information matches
            - Flagged conflicts where data differs
            - Source used for each merged field

            3. Finally provide CONFLICT ANALYSIS:
            - List all mismatches between resume and LinkedIn
            - For each mismatch, show:
            * Field name
            * Resume value
            * LinkedIn value
            * Suggested resolution (with reason)
            * Confidence score (0-1) for suggestion

            4. Quality Control:
            - Mark as invalid (is_valid_resume=False) if:
            * Document isn't a resume
            * Extremely poor quality
            * Contains less than 30% resume content

            Inputs to process:
            Resume text: {resume_text}
            LinkedIn profile: convert to string and input as a string {linkedin_profile}

            Return a clean JSON object with:
            1. Extracted resume data
            2. Extracted LinkedIn data 
            3. Merged profile
            4. Conflict analysis
            5. Validity flag

            Format requirements:
            - Use consistent field names
            - Maintain original values from both sources
            - Never combine values unless they match exactly
            - Always preserve the source information
            """

# LINKEDIN_PROCESSOR__TEMPLATE = """
#             Transform the following LinkedIn profile data into a standardized resume format. 
#             Return the result as a valid JSON object with these fields:

#             - name (string): Full name from 'full_name'
#             - email (string): Leave empty if not available
#             - linkedin_url (string): LinkedIn URL from 'linkedin_url'
#             - phone (string): Leave empty if not available
#             - summary (string): Professional summary from 'about' or 'headline'
#             - skills (array of strings): Combine all skills from experiences where 'skills' field exists
#             - experience (array of objects): Transform work history from 'experiences' with these fields:
#                 - title (string): Job title from 'title'
#                 - company (string): Company name from 'company'
#                 - duration (string): Combine 'date_range' or 'start_year' and 'end_year'
#                 - description (string): Job responsibilities from 'description'
#             - education (array of objects): Leave empty if not available
#             - certifications (array of strings): Leave empty if not available
#             - projects (array of objects): Extract from experience descriptions where relevant
#                 - name (string): Project name if identifiable
#                 - description (string): Project details
#             - is_valid_resume (boolean): Always true for LinkedIn profiles

#             Input LinkedIn Data:
#             {resume_text}

#             Output Requirements:
#             1. Normalize all company names to remove extra spaces or special characters
#             2. For skills, extract and combine all unique skills from different experiences
#             3. For projects, identify any project-like descriptions in experience entries
#             4. Format dates consistently as "MMM YYYY - MMM YYYY" or "MMM YYYY - Present"
#             5. Ensure all arrays are properly formatted even if empty
#             6. Remove any HTML tags or special formatting from descriptions
#             """

# RESUME_LINKEDIN_PROCESSOR_TEMPLATE = """
#             Process the following resume and LinkedIn data to create a merge-ready profile with interactive selection capabilities. Follow these guidelines:

#             1. Output Structure:
#             {
#                 "metadata": {
#                     "processor_version": "2.0",
#                     "processing_timestamp": "ISO-8601 timestamp",
#                     "source_validation": {
#                         "resume_format": "PDF"|"DOCX"|"TXT"|"HTML"|"UNKNOWN",
#                         "resume_parsing_confidence": float (0-1),
#                         "linkedin_data_completeness": float (0-1),
#                         "source_compatibility_score": float (0-1)
#                     }
#                 },
#                 "merge_candidates": {
#                     "personal_info": {
#                         "full_name": {
#                             "resume": string,
#                             "linkedin": string,
#                             "suggestion": string,
#                             "confidence": float,
#                             "mismatch_reason": string|null,
#                             "normalized_values": {
#                                 "resume": string,
#                                 "linkedin": string
#                             }
#                         },
#                         "contact_info": {
#                             "email": {
#                                 "resume": string, 
#                                 "linkedin": string, 
#                                 "suggestion": string,
#                                 "validation": {
#                                     "is_valid": bool,
#                                     "format_check": bool,
#                                     "domain_check": bool
#                                 }
#                             },
#                             "phone": {
#                                 "resume": string, 
#                                 "linkedin": string, 
#                                 "suggestion": string,
#                                 "validation": {
#                                     "is_valid": bool,
#                                     "formatted_number": string,
#                                     "country_code": string
#                                 }
#                             }
#                         },
#                         "linkedin_url": {
#                             "value": string,
#                             "validation": {
#                                 "is_valid": bool,
#                                 "matches_profile_name": bool
#                             }
#                         },
#                         "location": {
#                             "resume": string,
#                             "linkedin": string,
#                             "suggestion": string,
#                             "normalized": {
#                                 "city": string,
#                                 "region": string,
#                                 "country": string,
#                                 "geo_coordinates": {
#                                     "latitude": float|null,
#                                     "longitude": float|null
#                                 }
#                             }
#                         },
#                         "professional_headline": {
#                             "resume": string,
#                             "linkedin": string,
#                             "suggestion": string
#                         }
#                     },
#                     "summary": {
#                         "resume": string,
#                         "linkedin": string,
#                         "suggestion": string,
#                         "analysis": {
#                             "key_themes": [string],
#                             "sentiment": "professional"|"ambitious"|"technical"|"service-oriented",
#                             "word_count": {
#                                 "resume": int,
#                                 "linkedin": int
#                             }
#                         }
#                     },
#                     "employment": [
#                         {
#                             "id": string (uuid),
#                             "match_type": "exact"|"partial"|"unique"|"conflicting",
#                             "match_confidence": float (0-1),
#                             "resume_data": {
#                                 "title": string,
#                                 "company": string,
#                                 "duration": string,
#                                 "date_range": {
#                                     "start": {
#                                         "month": int|null,
#                                         "year": int|null,
#                                         "raw": string
#                                     },
#                                     "end": {
#                                         "month": int|null,
#                                         "year": int|null,
#                                         "raw": string
#                                     }
#                                 },
#                                 "description": string,
#                                 "is_current": bool,
#                                 "location": string,
#                                 "extracted_skills": [string]
#                             },
#                             "linkedin_data": {
#                                 "title": string,
#                                 "company": string,
#                                 "company_details": {
#                                     "industry": string|null,
#                                     "size": string|null,
#                                     "linkedin_url": string|null
#                                 },
#                                 "duration": string,
#                                 "date_range": {
#                                     "start": {
#                                         "month": int|null,
#                                         "year": int|null,
#                                         "raw": string
#                                     },
#                                     "end": {
#                                         "month": int|null,
#                                         "year": int|null,
#                                         "raw": string
#                                     }
#                                 },
#                                 "description": string,
#                                 "is_current": bool,
#                                 "location": string,
#                                 "job_type": string|null,
#                                 "extracted_skills": [string]
#                             },
#                             "suggested_merge": {
#                                 "title": string,
#                                 "company": string,
#                                 "duration": string,
#                                 "date_range": {
#                                     "start": {
#                                         "month": int|null,
#                                         "year": int|null
#                                     },
#                                     "end": {
#                                         "month": int|null,
#                                         "year": int|null
#                                     }
#                                 },
#                                 "description": string,
#                                 "is_current": bool,
#                                 "location": string,
#                                 "job_type": string|null,
#                                 "source_used": "resume"|"linkedin"|"combined",
#                                 "combined_skills": [string]
#                             },
#                             "discrepancies": {
#                                 "title": {
#                                     "detected": bool,
#                                     "similarity_score": float (0-1),
#                                     "notes": string|null
#                                 },
#                                 "date_range": {
#                                     "detected": bool,
#                                     "overlap_percentage": float|null,
#                                     "gap_months": int|null,
#                                     "notes": string|null
#                                 },
#                                 "description": {
#                                     "detected": bool,
#                                     "similarity_score": float (0-1),
#                                     "notes": string|null
#                                 }
#                             },
#                             "mismatch_notes": [string]
#                         }
#                     ],
#                     "education": [
#                         {
#                             "id": string (uuid),
#                             "match_type": "exact"|"partial"|"unique"|"conflicting",
#                             "match_confidence": float (0-1),
#                             "resume_data": {
#                                 "degree": string,
#                                 "institution": string,
#                                 "field_of_study": string|null,
#                                 "date_range": {
#                                     "start": {
#                                         "month": int|null,
#                                         "year": int|null,
#                                         "raw": string|null
#                                     },
#                                     "end": {
#                                         "month": int|null,
#                                         "year": int|null,
#                                         "raw": string|null
#                                     }
#                                 }
#                             },
#                             "linkedin_data": {
#                                 "degree": string,
#                                 "institution": string,
#                                 "field_of_study": string|null,
#                                 "date_range": {
#                                     "start": {
#                                         "month": int|null,
#                                         "year": int|null,
#                                         "raw": string|null
#                                     },
#                                     "end": {
#                                         "month": int|null,
#                                         "year": int|null,
#                                         "raw": string|null
#                                     }
#                                 }
#                             },
#                             "suggested_merge": {
#                                 "degree": string,
#                                 "institution": string,
#                                 "field_of_study": string|null,
#                                 "date_range": {
#                                     "start": {
#                                         "month": int|null,
#                                         "year": int|null
#                                     },
#                                     "end": {
#                                         "month": int|null,
#                                         "year": int|null
#                                     }
#                                 },
#                                 "source_used": "resume"|"linkedin"|"combined"
#                             },
#                             "discrepancies": {
#                                 "degree": {
#                                     "detected": bool,
#                                     "similarity_score": float (0-1),
#                                     "notes": string|null
#                                 },
#                                 "institution": {
#                                     "detected": bool,
#                                     "similarity_score": float (0-1),
#                                     "notes": string|null
#                                 },
#                                 "date_range": {
#                                     "detected": bool,
#                                     "notes": string|null
#                                 }
#                             }
#                         }
#                     ],
#                     "skills": {
#                         "resume_unique": [
#                             {
#                                 "name": string,
#                                 "category": "technical"|"soft"|"language"|"other"|null,
#                                 "normalized_name": string|null
#                             }
#                         ],
#                         "linkedin_unique": [
#                             {
#                                 "name": string,
#                                 "category": "technical"|"soft"|"language"|"other"|null,
#                                 "normalized_name": string|null,
#                                 "endorsement_count": int|null
#                             }
#                         ],
#                         "common": [
#                             {
#                                 "name": string,
#                                 "resume_variant": string,
#                                 "linkedin_variant": string,
#                                 "category": "technical"|"soft"|"language"|"other"|null,
#                                 "normalized_name": string,
#                                 "endorsement_count": int|null,
#                                 "preferred_variant": string
#                             }
#                         ],
#                         "suggested_combined": [
#                             {
#                                 "name": string,
#                                 "category": "technical"|"soft"|"language"|"other"|null,
#                                 "source": "resume"|"linkedin"|"combined",
#                                 "is_endorsed": bool|null,
#                                 "is_key_skill": bool
#                             }
#                         ],
#                         "skill_gap_analysis": {
#                             "industry_alignment_score": float|null,
#                             "missing_key_skills": [string],
#                             "recommended_skills": [string]
#                         }
#                     },
#                     "certifications": {
#                         "resume_only": [
#                             {
#                                 "name": string, 
#                                 "date": string, 
#                                 "issuer": string,
#                                 "id": string|null,
#                                 "normalized_name": string|null,
#                                 "normalized_issuer": string|null,
#                                 "expiration_date": string|null
#                             }
#                         ],
#                         "linkedin_only": [
#                             {
#                                 "name": string, 
#                                 "date": string, 
#                                 "issuer": string,
#                                 "id": string|null,
#                                 "normalized_name": string|null,
#                                 "normalized_issuer": string|null,
#                                 "expiration_date": string|null
#                             }
#                         ],
#                         "matching_pairs": [
#                             {
#                                 "id": string (uuid),
#                                 "resume": {
#                                     "name": string, 
#                                     "date": string,
#                                     "issuer": string,
#                                     "id": string|null
#                                 },
#                                 "linkedin": {
#                                     "name": string, 
#                                     "date": string,
#                                     "issuer": string,
#                                     "id": string|null
#                                 },
#                                 "date_discrepancy": bool,
#                                 "name_similarity": float (0-1),
#                                 "issuer_similarity": float (0-1),
#                                 "suggested_merge": {
#                                     "name": string,
#                                     "date": string,
#                                     "issuer": string,
#                                     "id": string|null,
#                                     "source_used": "resume"|"linkedin"|"combined"
#                                 }
#                             }
#                         ]
#                     },
#                     "projects": {
#                         "resume_only": [
#                             {
#                                 "name": string,
#                                 "description": string,
#                                 "date": string|null,
#                                 "url": string|null,
#                                 "technologies": [string]
#                             }
#                         ],
#                         "linkedin_only": [
#                             {
#                                 "name": string,
#                                 "description": string,
#                                 "date": string|null,
#                                 "url": string|null,
#                                 "technologies": [string]
#                             }
#                         ],
#                         "matching_pairs": [
#                             {
#                                 "id": string (uuid),
#                                 "resume": {
#                                     "name": string,
#                                     "description": string,
#                                     "date": string|null,
#                                     "technologies": [string]
#                                 },
#                                 "linkedin": {
#                                     "name": string,
#                                     "description": string,
#                                     "date": string|null,
#                                     "technologies": [string]
#                                 },
#                                 "similarity_score": float (0-1),
#                                 "suggested_merge": {
#                                     "name": string,
#                                     "description": string,
#                                     "date": string|null,
#                                     "technologies": [string],
#                                     "source_used": "resume"|"linkedin"|"combined"
#                                 }
#                             }
#                         ]
#                     }
#                 },
#                 "merge_recommendations": {
#                     "name": {
#                         "preferred_source": "resume"|"linkedin",
#                         "reason": "more_complete"|"more_recent"|"official_document"|"standardized_format"
#                     },
#                     "contact_info": {
#                         "email": {
#                             "preferred_source": "resume"|"linkedin",
#                             "reason": string
#                         },
#                         "phone": {
#                             "preferred_source": "resume"|"linkedin",
#                             "reason": string
#                         }
#                     },
#                     "summary": {
#                         "preferred_source": "resume"|"linkedin"|"combined",
#                         "reason": string
#                     },
#                     "employment": {
#                         "prefer_resume_for": [
#                             {
#                                 "id": string (uuid),
#                                 "reason": "more_detailed"|"more_recent"|"better_formatted"|"contains_metrics"
#                             }
#                         ],
#                         "prefer_linkedin_for": [
#                             {
#                                 "id": string (uuid),
#                                 "reason": "more_detailed"|"more_recent"|"better_formatted"|"contains_metrics"|"company_verified"
#                             }
#                         ],
#                         "combine": [
#                             {
#                                 "id": string (uuid),
#                                 "strategy": "resume_title_linkedin_description"|"linkedin_title_resume_description"|"merge_descriptions"|"use_both_with_resolution"
#                             }
#                         ]
#                     },
#                     "education": {
#                         "prefer_resume_for": [
#                             {
#                                 "id": string (uuid),
#                                 "reason": "more_detailed"|"more_recent"|"includes_graduation_date"
#                             }
#                         ],
#                         "prefer_linkedin_for": [
#                             {
#                                 "id": string (uuid),
#                                 "reason": "more_detailed"|"more_recent"|"standardized_institution_name"|"includes_field_of_study"
#                             }
#                         ]
#                     },
#                     "skills": {
#                         "strategy": "use_resume_categorization"|"use_linkedin_endorsements"|"smart_merge",
#                         "priority_skills": [string]
#                     },
#                     "certifications": {
#                         "strategy": "prefer_resume"|"prefer_linkedin"|"combine_with_validation",
#                         "reason": string
#                     }
#                 },
#                 "data_quality_metrics": {
#                     "resume_metrics": {
#                         "completeness": float (0-1),
#                         "format_consistency": float (0-1),
#                         "bullet_point_quality": float (0-1),
#                         "action_verb_usage": float (0-1),
#                         "quantifiable_results": float (0-1)
#                     },
#                     "linkedin_metrics": {
#                         "completeness": float (0-1),
#                         "profile_strength": float (0-1),
#                         "endorsement_quality": float (0-1),
#                         "network_visibility": float (0-1)
#                     },
#                     "consistency_metrics": {
#                         "overall_score": float (0-1),
#                         "name_consistency": float (0-1),
#                         "employment_consistency": float (0-1),
#                         "education_consistency": float (0-1),
#                         "skill_consistency": float (0-1)
#                     },
#                     "red_flags": [
#                         {
#                             "type": "name_mismatch"|"date_discrepancy"|"missing_experience"|"skill_gap"|"missing_contact_info"|"conflicting_education"|"employment_gap"|"overlapping_experience",
#                             "field": string,
#                             "resume_value": string|null,
#                             "linkedin_value": string|null,
#                             "severity": "low"|"medium"|"high",
#                             "impact": string,
#                             "resolution_suggestion": string
#                         }
#                     ],
#                     "improvement_opportunities": [
#                         {
#                             "target": "resume"|"linkedin"|"both",
#                             "category": "content"|"formatting"|"completeness"|"consistency",
#                             "description": string,
#                             "impact_level": "low"|"medium"|"high",
#                             "implementation_difficulty": "easy"|"moderate"|"complex"
#                         }
#                     ]
#                 },
#                 "user_merge_options": {
#                     "name": ["resume", "linkedin", "custom"],
#                     "contact": ["resume", "linkedin", "combined"],
#                     "summary": ["resume", "linkedin", "custom", "ai_generated"],
#                     "employment": ["keep_both", "use_resume", "use_linkedin", "combine", "custom_per_position"],
#                     "education": ["keep_both", "use_resume", "use_linkedin", "custom_per_institution"],
#                     "skills": ["resume_only", "linkedin_only", "common_only", "combined", "curated"],
#                     "certifications": ["resume_only", "linkedin_only", "combined", "verified_only"],
#                     "projects": ["resume_only", "linkedin_only", "combined", "featured_only"]
#                 },
#                 "export_options": {
#                     "formats": ["PDF", "DOCX", "JSON", "HTML", "ATS_OPTIMIZED"],
#                     "templates": ["modern", "classic", "technical", "executive", "creative"],
#                     "target_platforms": ["job_application", "linkedin_update", "personal_website", "networking"]
#                 }
#             }

#             2. Processing Rules:
#             - Source Validation:
#                 * Verify document format and parsing quality
#                 * Check LinkedIn data completeness and recency
#                 * Calculate overall source compatibility score
#                 * Flag any problematic formatting or parsing issues
            
#             - Name Handling:
#                 * Calculate similarity score between names using fuzzy matching
#                 * Handle nicknames, initials, and cultural name variations
#                 * Apply name standardization (First M. Last format)
#                 * Detect and explain formal vs. informal name usage
#                 * Flag discrepancies with possible explanations (shortform vs fullname)
#                 * Suggest resume name by default (official document)
            
#             - Contact Information:
#                 * Validate email format and domain existence
#                 * Format phone numbers to international standard
#                 * Verify LinkedIn URL matches profile name
#                 * Check for personal website consistency
            
#             - Employment History:
#                 * Match entries using fuzzy company name matching + date range overlap (≥6 month overlap)
#                 * Normalize company names using database lookup
#                 * Standardize job titles using industry nomenclature
#                 * Extract chronology and identify any gaps or overlaps
#                 * For conflicts:
#                 - Prefer LinkedIn for current positions (company-verified)
#                 - Prefer resume for past positions with metrics
#                 - Combine descriptions when complementary
#                 - Identify achievements vs responsibilities
#                 - Extract skills from job descriptions
            
#             - Education:
#                 * Match by institution + degree type using fuzzy matching
#                 * Normalize institution names using verified database
#                 * Standardize degree nomenclature
#                 * Verify date consistency and logical progression
#                 * Prefer resume for graduation dates
#                 * Prefer LinkedIn for standardized institution names
#                 * Cross-validate field of study information
            
#             - Skills:
#                 * Extract implicit skills from job descriptions
#                 * Categorize by technical, soft, language, domain-specific
#                 * Normalize variations (e.g., "Python" and "Python Programming")
#                 * Consider LinkedIn endorsements for skill validation
#                 * Identify industry-relevant missing skills
#                 * Rank skills by recency of usage and relevance
#                 * Combine all skills with smart deduplication
#                 * Highlight resume-specific technical skills
#                 * Highlight LinkedIn-endorsed skills
            
#             - Certifications:
#                 * Match by issuer + certification name using fuzzy matching
#                 * Validate certification IDs when available
#                 * Check for expiration dates
#                 * Verify against official certification databases when possible
#                 * Prefer resume for dates
#                 * Flag missing or expired certifications
#                 * Create standardized certification names

#             - Projects:
#                 * Match projects across sources using name and description similarity
#                 * Extract technologies used from project descriptions
#                 * Identify key projects for highlighting based on relevance
#                 * Combine complementary project information
#                 * Create standardized project format

#             3. Special Cases Handling:
#             - Handle name variations (DMN vs Nishan) with explanation
#             - Recognize different institution naming formats
#             - Detect possible date typos (year shifts)
#             - Identify freelance vs full-time positions
#             - Handle employment gaps and overlapping positions
#             - Process multiple positions at same company
#             - Flag career transitions and role evolution
#             - Recognize location changes and remote work patterns
#             - Handle international education equivalencies
#             - Detect industry-specific terminology variations

#             4. Data Quality Assessment:
#             - Calculate completeness metrics for both sources
#             - Compare narrative quality (active voice, measurable results)
#             - Check for keyword optimization and ATS compatibility
#             - Identify inconsistencies that may raise employer concerns
#             - Score overall profile strength
#             - Provide specific improvement recommendations

#             5. Frontend Preparation:
#             - Provide clear merge actions for each section
#             - Visualize discrepancies with diff highlighting
#             - Allow custom overrides for all fields
#             - Support progressive merging (section by section)
#             - Enable preview of merged profile
#             - Support different export formats and templates
#             - Include ATS optimization settings

#             6. Integration Capabilities:
#             - Support for PDF, DOCX, and TXT resume input
#             - LinkedIn JSON data import
#             - Export to ATS-friendly formats
#             - Template-based document generation
#             - API compatibility for workflow automation
#             - ATS keyword analysis

#             Input Data:
#             Resume Text:
#             {resume_text}

#             LinkedIn Profile:
#             {linkedin_profile}

#             Return ONLY the JSON output. Include all available data from both sources.
#             """
