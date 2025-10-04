# app/services/perplexity_analyzer.py - COMPLETE FIXED VERSION
import requests
import json
import re
from typing import Dict, List, Optional
from datetime import datetime

class PerplexityJobAnalyzer:
    """
    Enhanced job analysis using Perplexity AI API
    Provides superior content extraction and analysis
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def analyze_job_from_url(self, url: str) -> Dict:
        """
        Extract and analyze job posting from URL using Perplexity
        """
        try:
            print(f"🤖 Analyzing job posting with Perplexity AI: {url}")
            
            # Enhanced prompt for job extraction
            prompt = f"""
Please analyze this job posting URL and extract the following information in a structured format:

URL: {url}

Extract and provide:
1. Job Title
2. Company Name
3. Location (if specified)
4. Employment Type (Full-time, Part-time, Contract, etc.)
5. Experience Required (in years)
6. Education Requirements
7. Technical Skills Required (list all mentioned programming languages, frameworks, tools, technologies)
8. Soft Skills Required (leadership, communication, etc.)
9. Job Responsibilities (main duties and tasks)
10. Salary Range (if mentioned)
11. Benefits (if mentioned)
12. Company Description (brief)
13. Clean Job Description (remove promotional content, ads, navigation elements)

Focus only on the actual job posting content. Ignore:
- Website navigation menus
- Advertisements
- Promotional banners
- Footer content
- Related job suggestions
- Company promotional materials unrelated to this specific role

Provide the response in this exact JSON format:
{{
    "job_title": "...",
    "company_name": "...",
    "location": "...",
    "employment_type": "...",
    "experience_required": "...",
    "education_requirements": "...",
    "technical_skills": [...],
    "soft_skills": [...],
    "responsibilities": [...],
    "salary_range": "...",
    "benefits": [...],
    "company_description": "...",
    "clean_job_description": "...",
    "analysis_quality": "high/medium/low"
}}
"""

            # ✅ FIXED: Use correct current model name
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": "sonar",  # ✅ FIXED - Using current valid model
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert job market analyst and content extractor. Extract clean, accurate job posting information while filtering out promotional content and website noise."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    "max_tokens": 2000,
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "return_citations": True,
                    "return_images": False,
                    "return_related_questions": False
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"Perplexity API error: {response.status_code} - {response.text}")
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Extract JSON from the response
            job_data = self._extract_json_from_response(content)
            
            if job_data:
                job_data['success'] = True
                job_data['extraction_method'] = 'perplexity_ai'
                job_data['url'] = url
                job_data['analyzed_at'] = datetime.now().isoformat()
                
                print(f"✅ Perplexity analysis complete - Job: {job_data.get('job_title', 'Unknown')}")
                return job_data
            else:
                # Fallback response with basic info
                return {
                    'success': True,
                    'job_title': 'Job Position',
                    'company_name': 'Company',
                    'location': 'Not specified',
                    'clean_job_description': 'Please paste the job description manually for better analysis.',
                    'technical_skills': [],
                    'soft_skills': [],
                    'extraction_method': 'perplexity_ai_partial'
                }
                
        except Exception as e:
            print(f"❌ Perplexity analysis failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'extraction_method': 'perplexity_ai_failed'
            }
    
    def enhance_resume_analysis(self, resume_text: str, job_description: str) -> Dict:
        """
        Use Perplexity to provide enhanced resume optimization suggestions
        """
        try:
            print("🧠 Getting enhanced optimization suggestions from Perplexity...")
            
            prompt = f"""
As a professional resume optimization expert, analyze this resume against the job description and provide detailed, actionable optimization advice:

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:2000]}

Provide analysis in this JSON format:
{{
    "overall_assessment": "...",
    "strengths": [...],
    "improvement_areas": [...],
    "missing_keywords": [...],
    "suggested_additions": [...],
    "formatting_improvements": [...],
    "ats_optimization_tips": [...],
    "industry_specific_advice": [...],
    "experience_gap_analysis": "...",
    "skill_gap_analysis": "...",
    "recommended_action_items": [...]
}}

Focus on:
1. ATS compatibility
2. Keyword optimization
3. Industry-specific improvements
4. Quantifiable achievements
5. Skill gaps and how to address them
6. Professional formatting
7. Content structure optimization
"""

            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": "sonar",  # ✅ FIXED - Using current model
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a professional career counselor and resume optimization expert with 15+ years of experience in ATS systems and hiring practices."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": 1500,
                    "temperature": 0.2
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                analysis_data = self._extract_json_from_response(content)
                if analysis_data:
                    analysis_data['enhancement_method'] = 'perplexity_ai'
                    return analysis_data
            
            # Fallback response
            return {
                'recommended_action_items': [
                    'Add more quantified achievements with specific numbers',
                    'Include relevant technical keywords from the job description',
                    'Optimize for ATS compatibility with standard formatting',
                    'Highlight transferable skills and experiences',
                    'Use industry-specific terminology'
                ],
                'enhancement_method': 'fallback'
            }
            
        except Exception as e:
            print(f"❌ Enhanced analysis failed: {str(e)}")
            return {
                'recommended_action_items': [
                    'Add more quantified achievements',
                    'Include relevant keywords from job posting',
                    'Use ATS-friendly formatting',
                    'Highlight key accomplishments'
                ],
                'error': str(e)
            }
    
    def generate_optimized_content(self, resume_data: Dict, job_data: Dict) -> Dict:
        """
        Generate optimized resume content using Perplexity
        """
        try:
            print("✨ Generating optimized resume content with Perplexity...")
            
            # Extract key info with fallbacks
            experience_years = resume_data.get('experience_years', 3)
            job_title = job_data.get('job_title', 'Target Position')
            required_skills = job_data.get('technical_skills', [])
            skills_text = ', '.join(required_skills[:5]) if required_skills else 'relevant technologies'
            
            prompt = f"""
Create an optimized professional summary and experience descriptions for this resume based on the job requirements:

CURRENT RESUME DATA:
- Experience: {experience_years} years
- Target Job: {job_title}
- Required Skills: {skills_text}

Generate optimized content in JSON format:
{{
    "professional_summary": "...",
    "optimized_experience_bullets": [
        "...",
        "...",
        "..."
    ],
    "key_achievements": [
        "...",
        "..."
    ],
    "skills_summary": "...",
    "cover_letter_opener": "..."
}}

Requirements:
1. Use action verbs (Developed, Led, Implemented, Architected, etc.)
2. Include quantifiable metrics where possible
3. Incorporate job-relevant keywords naturally
4. Maintain ATS-friendly language
5. Focus on achievements, not just responsibilities
6. Align with the job's required experience level
"""

            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": "sonar",  # ✅ FIXED - Using current model
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a professional resume writer specializing in ATS optimization and career advancement. Create compelling, results-oriented content."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": 1200,
                    "temperature": 0.3
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                optimized_content = self._extract_json_from_response(content)
                if optimized_content:
                    optimized_content['generation_method'] = 'perplexity_ai'
                    return optimized_content
            
            # Fallback response
            return {
                'professional_summary': f"Results-driven professional with {experience_years}+ years of experience in {skills_text}. Proven track record of delivering high-quality solutions and driving organizational success.",
                'optimized_experience_bullets': [
                    f"Developed and implemented solutions using {skills_text}",
                    f"Led cross-functional teams to deliver projects on time and within budget",
                    f"Improved system efficiency and performance through strategic optimization"
                ],
                'key_achievements': [
                    "Successfully delivered multiple high-impact projects",
                    "Improved team productivity and system performance"
                ],
                'generation_method': 'fallback'
            }
            
        except Exception as e:
            print(f"❌ Content generation failed: {str(e)}")
            return {
                'professional_summary': f"Experienced professional with {resume_data.get('experience_years', 3)}+ years in the field.",
                'optimized_experience_bullets': [
                    "Delivered successful projects and initiatives",
                    "Collaborated effectively with cross-functional teams",
                    "Contributed to organizational goals and objectives"
                ],
                'error': str(e)
            }
    
    def _extract_json_from_response(self, content: str) -> Optional[Dict]:
        """Extract JSON object from Perplexity response"""
        try:
            # Try to find JSON block in the response
            json_match = re.search(r'``````', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            
            # Try to find JSON object directly
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            
            # If no JSON found, try to parse the entire content
            return json.loads(content)
            
        except json.JSONDecodeError:
            print("⚠️ Could not parse JSON from Perplexity response")
            return None
