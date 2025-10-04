from typing import Dict, List
from datetime import datetime
import os
import re
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

class ProfessionalResumeGenerator:
    """
    Professional ATS-optimized resume generator
    Creates industry-standard resume formats
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_professional_styles()
    
    def _setup_professional_styles(self):
        """Setup professional ATS-friendly styles"""
        
        # Name header style
        self.styles.add(ParagraphStyle(
            name='NameHeader',
            parent=self.styles['Title'],
            fontSize=20,
            fontName='Helvetica-Bold',
            spaceAfter=6,
            textColor=colors.HexColor('#2c3e50'),
            alignment=TA_CENTER
        ))
        
        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica',
            alignment=TA_CENTER,
            spaceAfter=12,
            textColor=colors.HexColor('#34495e')
        ))
        
        # Section header style (ATS-friendly)
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            fontName='Helvetica-Bold',
            spaceBefore=18,
            spaceAfter=6,
            textColor=colors.HexColor('#2c3e50'),
            borderWidth=1,
            borderColor=colors.HexColor('#3498db'),
            borderPadding=3
        ))
        
        # Professional summary style
        self.styles.add(ParagraphStyle(
            name='ProfessionalSummary',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica',
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        # Skills text style
        self.styles.add(ParagraphStyle(
            name='SkillsText',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            spaceAfter=6,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        # Job title style
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            fontName='Helvetica-Bold',
            spaceAfter=3,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        # Company info style
        self.styles.add(ParagraphStyle(
            name='CompanyInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Oblique',
            spaceAfter=6,
            textColor=colors.HexColor('#7f8c8d')
        ))
        
        # Bullet points style
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            spaceAfter=3,
            leftIndent=20,
            bulletIndent=10,
            textColor=colors.HexColor('#2c3e50')
        ))

    def generate_optimized_resume(self, original_resume_text: str, resume_analysis: Dict, 
                                job_analysis: Dict, match_analysis: Dict, suggestions: List[str]) -> Dict:
        """Generate a professional, ATS-optimized resume"""
        
        print("🎨 Generating professional ATS-optimized resume...")
        
        # Parse original resume
        parsed_resume = self._parse_resume_content(original_resume_text, resume_analysis)
        
        # Create optimized content
        optimized_content = self._create_optimized_content(
            parsed_resume, resume_analysis, job_analysis, match_analysis
        )
        
        # Generate professional PDF
        pdf_path = self._generate_professional_pdf(optimized_content, job_analysis)
        
        # Generate text version for preview
        text_content = self._generate_text_version(optimized_content)
        
        print(f"✅ Generated professional resume: {os.path.basename(pdf_path)}")
        
        return {
            'text_content': text_content,
            'pdf_path': pdf_path,
            'filename': os.path.basename(pdf_path)
        }
    
    def _parse_resume_content(self, original_text: str, resume_analysis: Dict) -> Dict:
        """Parse original resume into structured sections"""
        
        sections = {
            'personal_info': self._extract_personal_info(original_text, resume_analysis),
            'professional_summary': self._extract_summary(original_text),
            'work_experience': self._extract_work_experience(original_text),
            'education': self._extract_education(original_text),
            'skills': resume_analysis.get('technical_skills', []) + resume_analysis.get('soft_skills', []),
            'certifications': self._extract_certifications(original_text),
            'projects': self._extract_projects(original_text)
        }
        
        return sections
    
    def _extract_personal_info(self, text: str, resume_analysis: Dict) -> Dict:
        """Extract personal information"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Name is usually the first line
        name = lines[0] if lines else "Your Name"
        name = re.sub(r'(resume|cv)\s*', '', name, flags=re.IGNORECASE).strip()
        
        contact_info = resume_analysis.get('contact_info', {})
        
        # Extract additional info
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        phone = phones[0] if phones else contact_info.get('phone')
        
        # Extract location
        location_patterns = [
            r'([A-Za-z\s]+,\s*[A-Za-z]{2}\s*\d{5})',
            r'([A-Za-z\s]+,\s*[A-Za-z]{2})',
            r'([A-Za-z\s]+,\s*[A-Za-z\s]+)'
        ]
        
        location = None
        for pattern in location_patterns:
            matches = re.findall(pattern, text)
            if matches:
                location = matches[0]
                break
        
        return {
            'name': name,
            'email': contact_info.get('email'),
            'phone': phone,
            'location': location,
            'linkedin': self._extract_linkedin(text),
            'github': self._extract_github(text)
        }
    
    def _extract_summary(self, text: str) -> str:
        """Extract professional summary from original resume"""
        summary_patterns = [
            r'(?:professional\s+summary|summary|profile|objective)[\s:]*\n(.*?)(?=\n\s*\n|\n[A-Z])',
            r'(?:about\s+me|overview)[\s:]*\n(.*?)(?=\n\s*\n|\n[A-Z])'
        ]
        
        for pattern in summary_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            if matches:
                return matches[0].strip()
        
        return ""
    
    def _extract_work_experience(self, text: str) -> List[Dict]:
        """Extract work experience"""
        exp_pattern = r'(?:work\s+experience|experience|employment)[\s:]*\n(.*?)(?=\n\s*(?:education|skills|projects|\Z))'
        
        matches = re.findall(exp_pattern, text, re.IGNORECASE | re.DOTALL)
        if not matches:
            return []
        
        experience_text = matches[0]
        
        # Simple parsing - split by double newlines or patterns that look like job titles
        jobs = []
        sections = re.split(r'\n\s*\n', experience_text)
        
        for section in sections:
            if len(section.strip()) < 20:  # Too short to be a job
                continue
                
            lines = [line.strip() for line in section.split('\n') if line.strip()]
            if len(lines) < 2:
                continue
            
            # First line is usually job title
            title = lines[0]
            
            # Second line often contains company and dates
            company_info = lines[1] if len(lines) > 1 else ""
            
            # Rest are responsibilities
            responsibilities = lines[2:] if len(lines) > 2 else []
            
            jobs.append({
                'title': title,
                'company_info': company_info,
                'responsibilities': responsibilities
            })
        
        return jobs[:3]  # Limit to 3 most recent jobs
    
    def _extract_education(self, text: str) -> List[Dict]:
        """Extract education information"""
        edu_pattern = r'(?:education|academic)[\s:]*\n(.*?)(?=\n\s*(?:experience|skills|projects|\Z))'
        
        matches = re.findall(edu_pattern, text, re.IGNORECASE | re.DOTALL)
        if not matches:
            return []
        
        education_text = matches[0]
        education = []
        
        # Look for degree patterns
        degree_patterns = [
            r'(bachelor|master|phd|doctorate|associate).*?(?:in|of)\s+(.*?)(?:\n|$)',
            r'(b\.?s\.?|m\.?s\.?|b\.?a\.?|m\.?a\.?|phd).*?(?:in|of)?\s+(.*?)(?:\n|$)'
        ]
        
        for pattern in degree_patterns:
            matches = re.findall(pattern, education_text, re.IGNORECASE)
            for match in matches:
                education.append({
                    'degree': match[0],
                    'field': match[1],
                    'school': 'Your University',  # Default - could be enhanced
                    'year': 'Year'  # Default - could be enhanced
                })
        
        return education
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        cert_patterns = [
            r'aws\s+certified',
            r'google\s+cloud',
            r'azure\s+certified',
            r'pmp',
            r'scrum\s+master',
            r'cissp',
            r'comptia',
            r'cisco\s+ccna'
        ]
        
        certifications = []
        for pattern in cert_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                certifications.append(pattern.replace(r'\s+', ' ').title())
        
        return certifications
    
    def _extract_projects(self, text: str) -> List[Dict]:
        """Extract projects"""
        project_pattern = r'(?:projects?)[\s:]*\n(.*?)(?=\n\s*(?:education|experience|skills|\Z))'
        
        matches = re.findall(project_pattern, text, re.IGNORECASE | re.DOTALL)
        if not matches:
            return []
        
        # Simple project parsing
        projects = []
        lines = [line.strip() for line in matches[0].split('\n') if line.strip()]
        
        for line in lines[:3]:  # Limit to 3 projects
            if len(line) > 10:
                projects.append({
                    'name': line,
                    'description': 'Project description would go here'
                })
        
        return projects
    
    def _extract_linkedin(self, text: str) -> str:
        """Extract LinkedIn URL"""
        linkedin_pattern = r'linkedin\.com/(?:in/)?([A-Za-z0-9-]+)'
        matches = re.findall(linkedin_pattern, text)
        return f"linkedin.com/in/{matches[0]}" if matches else None
    
    def _extract_github(self, text: str) -> str:
        """Extract GitHub URL"""
        github_pattern = r'github\.com/([A-Za-z0-9-]+)'
        matches = re.findall(github_pattern, text)
        return f"github.com/{matches[0]}" if matches else None
    
    def _create_optimized_content(self, parsed_resume: Dict, resume_analysis: Dict, 
                                job_analysis: Dict, match_analysis: Dict) -> Dict:
        """Create optimized content based on analysis"""
        
        # Enhanced professional summary
        optimized_summary = self._create_optimized_summary(
            parsed_resume['professional_summary'], 
            resume_analysis, 
            job_analysis
        )
        
        # Enhanced skills section
        optimized_skills = self._create_optimized_skills(
            resume_analysis, 
            job_analysis, 
            match_analysis
        )
        
        # Enhanced work experience
        optimized_experience = self._enhance_work_experience(
            parsed_resume['work_experience'],
            job_analysis,
            match_analysis
        )
        
        return {
            'personal_info': parsed_resume['personal_info'],
            'professional_summary': optimized_summary,
            'skills': optimized_skills,
            'work_experience': optimized_experience,
            'education': parsed_resume['education'],
            'certifications': parsed_resume['certifications'],
            'projects': parsed_resume['projects']
        }
    
    def _create_optimized_summary(self, original_summary: str, resume_analysis: Dict, job_analysis: Dict) -> str:
        """Create an optimized professional summary"""
        
        experience_years = resume_analysis.get('experience_years', 3)
        job_level = job_analysis.get('job_level', 'Mid-level')
        required_skills = job_analysis.get('required_tech_skills', [])
        
        # Base opening
        if job_level == 'Senior':
            opening = f"Experienced professional with {experience_years}+ years of proven expertise"
        elif job_level == 'Junior' or experience_years < 2:
            opening = f"Motivated professional with {experience_years} years of hands-on experience"
        else:
            opening = f"Results-driven professional with {experience_years} years of progressive experience"
        
        # Add key skills
        if required_skills:
            top_skills = required_skills[:4]
            skills_phrase = ', '.join(top_skills[:-1]) + f", and {top_skills[-1]}" if len(top_skills) > 1 else top_skills[0]
            middle = f"in {skills_phrase}"
        else:
            middle = "in software development and technology solutions"
        
        # Add value proposition
        if job_level == 'Senior':
            ending = "with a strong track record of leading cross-functional teams, architecting scalable solutions, and driving organizational growth through innovative technology implementations."
        elif job_level == 'Junior':
            ending = "with strong analytical skills and a passion for learning new technologies. Eager to contribute to team success while continuing professional development."
        else:
            ending = "with demonstrated ability to deliver high-quality solutions, collaborate effectively with stakeholders, and adapt quickly to emerging technologies."
        
        return f"{opening} {middle} {ending}"
    
    def _create_optimized_skills(self, resume_analysis: Dict, job_analysis: Dict, match_analysis: Dict) -> Dict:
        """Create optimized skills sections"""
        
        # Get existing skills
        existing_tech = set(resume_analysis.get('technical_skills', []))
        existing_soft = set(resume_analysis.get('soft_skills', []))
        
        # Get required skills
        required_tech = set(job_analysis.get('required_tech_skills', []))
        required_soft = set(job_analysis.get('required_soft_skills', []))
        
        # Combine and prioritize
        all_tech_skills = list(required_tech.union(existing_tech))
        all_soft_skills = list(required_soft.union(existing_soft))
        
        # Categorize technical skills
        programming_langs = [s for s in all_tech_skills if s in ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin']]
        frameworks = [s for s in all_tech_skills if s in ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'laravel', 'express', 'nodejs']]
        databases = [s for s in all_tech_skills if s in ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql']]
        cloud_tools = [s for s in all_tech_skills if s in ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform', 'git']]
        other_tech = [s for s in all_tech_skills if s not in programming_langs + frameworks + databases + cloud_tools]
        
        return {
            'programming_languages': programming_langs,
            'frameworks_libraries': frameworks,
            'databases': databases,
            'cloud_devops': cloud_tools,
            'other_technical': other_tech,
            'soft_skills': all_soft_skills
        }
    
    def _enhance_work_experience(self, original_experience: List[Dict], job_analysis: Dict, match_analysis: Dict) -> List[Dict]:
        """Enhance work experience with job-relevant keywords"""
        
        if not original_experience:
            return [{
                'title': 'Your Job Title',
                'company_info': 'Company Name | Start Date - End Date',
                'responsibilities': [
                    'Add your key accomplishments and responsibilities here',
                    'Use action verbs like: Developed, Implemented, Led, Created, Managed',
                    'Quantify achievements with specific numbers and percentages',
                    'Include relevant technologies and skills from the job description'
                ]
            }]
        
        # Enhance existing experience
        enhanced_experience = []
        
        for job in original_experience:
            enhanced_job = job.copy()
            
            # Enhance responsibilities with keywords
            if 'responsibilities' in enhanced_job:
                enhanced_responsibilities = []
                for resp in enhanced_job['responsibilities']:
                    # Add relevant keywords naturally
                    enhanced_resp = self._enhance_responsibility_text(resp, job_analysis)
                    enhanced_responsibilities.append(enhanced_resp)
                
                enhanced_job['responsibilities'] = enhanced_responsibilities
            
            enhanced_experience.append(enhanced_job)
        
        return enhanced_experience
    
    def _enhance_responsibility_text(self, text: str, job_analysis: Dict) -> str:
        """Enhance responsibility text with relevant keywords"""
        required_skills = job_analysis.get('required_tech_skills', [])
        
        # Simple enhancement - add relevant skills contextually
        enhanced_text = text
        
        # Add specific skills if not already present
        for skill in required_skills[:2]:  # Add top 2 relevant skills
            if skill.lower() not in text.lower() and len(enhanced_text) < 150:
                if 'developed' in text.lower() or 'built' in text.lower():
                    enhanced_text = enhanced_text.replace(' using ', f' using {skill}, ')
                    break
        
        return enhanced_text
    
    def _generate_professional_pdf(self, content: Dict, job_analysis: Dict) -> str:
        """Generate professional ATS-optimized PDF"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"optimized_resume_{timestamp}.pdf"
        file_path = f"uploads/optimized/{filename}"
        
        # Create PDF with professional settings
        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Personal Information Header
        personal_info = content['personal_info']
        
        # Name
        if personal_info.get('name'):
            story.append(Paragraph(personal_info['name'], self.styles['NameHeader']))
        
        # Contact Information
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('location'):
            contact_parts.append(personal_info['location'])
        if personal_info.get('linkedin'):
            contact_parts.append(personal_info['linkedin'])
        
        if contact_parts:
            contact_text = ' | '.join(contact_parts)
            story.append(Paragraph(contact_text, self.styles['ContactInfo']))
        
        story.append(Spacer(1, 12))
        
        # Professional Summary
        if content.get('professional_summary'):
            story.append(Paragraph("PROFESSIONAL SUMMARY", self.styles['SectionHeader']))
            story.append(Paragraph(content['professional_summary'], self.styles['ProfessionalSummary']))
            story.append(Spacer(1, 6))
        
        # Technical Skills
        skills = content.get('skills', {})
        if any(skills.values()):
            story.append(Paragraph("TECHNICAL SKILLS", self.styles['SectionHeader']))
            
            # Create skills table for better formatting
            skills_data = []
            
            for category, skill_list in skills.items():
                if skill_list and category != 'soft_skills':
                    category_name = category.replace('_', ' ').title()
                    skills_text = ', '.join(skill_list)
                    skills_data.append([f"{category_name}:", skills_text])
            
            if skills_data:
                skills_table = Table(skills_data, colWidths=[1.5*inch, 5*inch])
                skills_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 3),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ]))
                story.append(skills_table)
                story.append(Spacer(1, 12))
        
        # Work Experience
        work_experience = content.get('work_experience', [])
        if work_experience:
            story.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles['SectionHeader']))
            
            for job in work_experience:
                if job.get('title'):
                    story.append(Paragraph(job['title'], self.styles['JobTitle']))
                
                if job.get('company_info'):
                    story.append(Paragraph(job['company_info'], self.styles['CompanyInfo']))
                
                if job.get('responsibilities'):
                    for resp in job['responsibilities']:
                        if resp.strip():
                            story.append(Paragraph(f"• {resp}", self.styles['BulletPoint']))
                
                story.append(Spacer(1, 12))
        
        # Education
        education = content.get('education', [])
        if education:
            story.append(Paragraph("EDUCATION", self.styles['SectionHeader']))
            
            for edu in education:
                edu_text = f"{edu.get('degree', '')} {edu.get('field', '')}"
                if edu.get('school'):
                    edu_text += f" - {edu['school']}"
                if edu.get('year'):
                    edu_text += f" ({edu['year']})"
                
                story.append(Paragraph(edu_text, self.styles['Normal']))
            
            story.append(Spacer(1, 12))
        
        # Core Competencies (Soft Skills)
        soft_skills = skills.get('soft_skills', [])
        if soft_skills:
            story.append(Paragraph("CORE COMPETENCIES", self.styles['SectionHeader']))
            soft_skills_text = ' • '.join(soft_skills)
            story.append(Paragraph(soft_skills_text, self.styles['SkillsText']))
        
        # Build PDF
        doc.build(story)
        
        return file_path
    
    def _generate_text_version(self, content: Dict) -> str:
        """Generate text version for preview"""
        
        text_parts = []
        personal_info = content['personal_info']
        
        # Header
        if personal_info.get('name'):
            text_parts.append(personal_info['name'])
            text_parts.append('=' * len(personal_info['name']))
        
        # Contact
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(f"Email: {personal_info['email']}")
        if personal_info.get('phone'):
            contact_parts.append(f"Phone: {personal_info['phone']}")
        if personal_info.get('location'):
            contact_parts.append(f"Location: {personal_info['location']}")
        
        if contact_parts:
            text_parts.extend(contact_parts)
            text_parts.append('')
        
        # Professional Summary
        if content.get('professional_summary'):
            text_parts.append('PROFESSIONAL SUMMARY')
            text_parts.append('-' * 20)
            text_parts.append(content['professional_summary'])
            text_parts.append('')
        
        # Skills
        skills = content.get('skills', {})
        if any(skills.values()):
            text_parts.append('TECHNICAL SKILLS')
            text_parts.append('-' * 15)
            
            for category, skill_list in skills.items():
                if skill_list and category != 'soft_skills':
                    category_name = category.replace('_', ' ').title()
                    text_parts.append(f"{category_name}: {', '.join(skill_list)}")
            
            text_parts.append('')
        
        # Experience
        work_experience = content.get('work_experience', [])
        if work_experience:
            text_parts.append('PROFESSIONAL EXPERIENCE')
            text_parts.append('-' * 22)
            
            for job in work_experience:
                if job.get('title'):
                    text_parts.append(job['title'])
                if job.get('company_info'):
                    text_parts.append(job['company_info'])
                
                if job.get('responsibilities'):
                    for resp in job['responsibilities']:
                        text_parts.append(f"• {resp}")
                
                text_parts.append('')
        
        return '\n'.join(text_parts)
