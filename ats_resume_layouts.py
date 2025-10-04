# app/services/ats_resume_layouts.py - Professional ATS Resume Layouts
from typing import Dict, List, Optional
from datetime import datetime
import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

class ATSResumeLayouts:
    """
    Professional ATS-friendly resume layouts matching industry standards
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_ats_styles()
        
        # Layout options
        self.layouts = {
            'modern_ats': self._generate_modern_ats,
            'classic_professional': self._generate_classic_professional,
            'tech_focused': self._generate_tech_focused,
            'executive_style': self._generate_executive_style,
            'clean_minimal': self._generate_clean_minimal
        }
    
    def _setup_ats_styles(self):
        """Setup ATS-optimized professional styles"""
        
        # Name header - clean and professional
        self.styles.add(ParagraphStyle(
            name='ATSName',
            parent=self.styles['Normal'],
            fontSize=18,
            fontName='Helvetica-Bold',
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        # Contact info - single line format
        self.styles.add(ParagraphStyle(
            name='ATSContact',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            spaceAfter=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#34495e')
        ))
        
        # Professional summary/objective
        self.styles.add(ParagraphStyle(
            name='ATSSummaryTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            fontName='Helvetica-Bold',
            spaceAfter=6,
            spaceBefore=12,
            textColor=colors.HexColor('#2c3e50'),
            alignment=TA_LEFT
        ))
        
        # Section headers
        self.styles.add(ParagraphStyle(
            name='ATSSectionHeader',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica-Bold',
            spaceAfter=8,
            spaceBefore=16,
            textColor=colors.HexColor('#2c3e50'),
            alignment=TA_LEFT,
            borderWidth=0.5,
            borderColor=colors.HexColor('#bdc3c7'),
            borderPadding=2
        ))
        
        # Experience company/title
        self.styles.add(ParagraphStyle(
            name='ATSCompanyTitle',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica-Bold',
            spaceAfter=2,
            spaceBefore=8,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        # Experience details (dates, location)
        self.styles.add(ParagraphStyle(
            name='ATSDetails',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            spaceAfter=4,
            textColor=colors.HexColor('#7f8c8d'),
            alignment=TA_LEFT
        ))
        
        # Bullet points
        self.styles.add(ParagraphStyle(
            name='ATSBullet',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            spaceAfter=3,
            leftIndent=15,
            bulletIndent=10,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        # Skills categories
        self.styles.add(ParagraphStyle(
            name='ATSSkillCategory',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            spaceAfter=3,
            textColor=colors.HexColor('#34495e')
        ))
        
        # Skills list
        self.styles.add(ParagraphStyle(
            name='ATSSkillList',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            spaceAfter=6,
            textColor=colors.HexColor('#2c3e50')
        ))
    
    def generate_ats_resume(self, resume_data: Dict, layout: str = 'modern_ats') -> Dict:
        """
        Generate professional ATS resume with selected layout
        """
        if layout not in self.layouts:
            layout = 'modern_ats'
        
        print(f"🎨 Generating ATS resume with {layout} layout...")
        
        # Process resume data
        processed_data = self._process_resume_data(resume_data)
        
        # Generate with selected layout
        return self.layouts[layout](processed_data)
    
    def _process_resume_data(self, raw_data: Dict) -> Dict:
        """Process and clean resume data for ATS formatting"""
        
        # Extract personal info
        personal_info = self._extract_personal_info(raw_data)
        
        # Extract and format experience
        experience = self._extract_experience(raw_data)
        
        # Extract skills by category
        skills = self._categorize_skills(raw_data)
        
        # Extract education
        education = self._extract_education(raw_data)
        
        return {
            'personal_info': personal_info,
            'professional_summary': self._generate_professional_summary(raw_data),
            'experience': experience,
            'skills': skills,
            'education': education,
            'additional_sections': self._extract_additional_sections(raw_data)
        }
    
    def _generate_modern_ats(self, data: Dict) -> Dict:
        """Generate Modern ATS layout - clean and professional"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"modern_ats_resume_{timestamp}.pdf"
        file_path = f"uploads/optimized/{filename}"
        
        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        personal_info = data['personal_info']
        
        # Header with name
        if personal_info.get('name'):
            story.append(Paragraph(personal_info['name'].upper(), self.styles['ATSName']))
        
        # Contact information - single line
        contact_parts = []
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('linkedin'):
            contact_parts.append(personal_info['linkedin'])
        if personal_info.get('github'):
            contact_parts.append(personal_info['github'])
        
        if contact_parts:
            contact_text = ' | '.join(contact_parts)
            story.append(Paragraph(contact_text, self.styles['ATSContact']))
        
        # Professional Summary/Objective
        if data.get('professional_summary'):
            story.append(Paragraph("PROFESSIONAL SUMMARY", self.styles['ATSSummaryTitle']))
            story.append(Paragraph(data['professional_summary'], self.styles['Normal']))
        
        # Technical Skills
        skills = data.get('skills', {})
        if skills:
            story.append(Paragraph("TECHNICAL SKILLS", self.styles['ATSSectionHeader']))
            
            if skills.get('programming'):
                story.append(Paragraph(f"• <b>Programming:</b> {', '.join(skills['programming'])}", self.styles['ATSSkillList']))
            
            if skills.get('frameworks'):
                story.append(Paragraph(f"• <b>Frameworks & Tools:</b> {', '.join(skills['frameworks'])}", self.styles['ATSSkillList']))
            
            if skills.get('databases'):
                story.append(Paragraph(f"• <b>Databases:</b> {', '.join(skills['databases'])}", self.styles['ATSSkillList']))
            
            if skills.get('cloud'):
                story.append(Paragraph(f"• <b>Cloud & DevOps:</b> {', '.join(skills['cloud'])}", self.styles['ATSSkillList']))
            
            if skills.get('other'):
                story.append(Paragraph(f"• <b>Data & Visualization:</b> {', '.join(skills['other'])}", self.styles['ATSSkillList']))
        
        # Professional Experience
        experience = data.get('experience', [])
        if experience:
            story.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles['ATSSectionHeader']))
            
            for exp in experience:
                # Company and position
                company_title = f"{exp.get('company', 'Company Name')}"
                if exp.get('location'):
                    company_title += f" | {exp['location']}"
                story.append(Paragraph(company_title, self.styles['ATSCompanyTitle']))
                
                # Position and dates
                position_line = f"{exp.get('position', 'Position Title')}"
                if exp.get('dates'):
                    position_line += f" | {exp['dates']}"
                story.append(Paragraph(position_line, self.styles['ATSDetails']))
                
                # Responsibilities/achievements
                for responsibility in exp.get('responsibilities', []):
                    story.append(Paragraph(f"• {responsibility}", self.styles['ATSBullet']))
                
                story.append(Spacer(1, 6))
        
        # Education
        education = data.get('education', [])
        if education:
            story.append(Paragraph("EDUCATION", self.styles['ATSSectionHeader']))
            
            for edu in education:
                # Institution
                institution = edu.get('institution', 'Institution Name')
                if edu.get('location'):
                    institution += f" | {edu['location']}"
                story.append(Paragraph(institution, self.styles['ATSCompanyTitle']))
                
                # Degree and year
                degree_line = f"{edu.get('degree', 'Degree')}"
                if edu.get('year'):
                    degree_line += f" | {edu['year']}"
                story.append(Paragraph(degree_line, self.styles['ATSDetails']))
                
                story.append(Spacer(1, 6))
        
        # Build PDF
        doc.build(story)
        
        return {
            'filename': filename,
            'pdf_path': file_path,
            'layout': 'modern_ats',
            'text_content': self._generate_text_version(data)
        }
    
    def _generate_tech_focused(self, data: Dict) -> Dict:
        """Generate Tech-Focused ATS layout"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tech_focused_resume_{timestamp}.pdf"
        file_path = f"uploads/optimized/{filename}"
        
        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        personal_info = data['personal_info']
        
        # Header
        if personal_info.get('name'):
            story.append(Paragraph(personal_info['name'], self.styles['ATSName']))
        
        # Contact info
        contact_parts = []
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('linkedin'):
            contact_parts.append(personal_info['linkedin'])
        if personal_info.get('github'):
            contact_parts.append(personal_info['github'])
        
        if contact_parts:
            story.append(Paragraph(' | '.join(contact_parts), self.styles['ATSContact']))
        
        # Tech specialization header
        story.append(Paragraph("SOFTWARE DEVELOPMENT & DATA ANALYTICS", self.styles['ATSSummaryTitle']))
        
        # Professional Summary
        if data.get('professional_summary'):
            story.append(Paragraph(data['professional_summary'], self.styles['Normal']))
        
        # Technical Skills - Detailed categories
        skills = data.get('skills', {})
        if skills:
            story.append(Paragraph("TECHNICAL SKILLS", self.styles['ATSSectionHeader']))
            
            # Create skills table for better ATS parsing
            skills_data = []
            
            if skills.get('programming'):
                skills_data.append(['Programming Languages:', ', '.join(skills['programming'])])
            
            if skills.get('frameworks'):
                skills_data.append(['Frameworks & Libraries:', ', '.join(skills['frameworks'])])
            
            if skills.get('databases'):
                skills_data.append(['Databases & Storage:', ', '.join(skills['databases'])])
            
            if skills.get('cloud'):
                skills_data.append(['Cloud & DevOps:', ', '.join(skills['cloud'])])
            
            if skills.get('other'):
                skills_data.append(['Data Science & ML:', ', '.join(skills['other'])])
            
            if skills_data:
                skills_table = Table(skills_data, colWidths=[1.5*inch, 5*inch])
                skills_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), 3),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ]))
                story.append(skills_table)
                story.append(Spacer(1, 12))
        
        # Professional Experience
        experience = data.get('experience', [])
        if experience:
            story.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles['ATSSectionHeader']))
            
            for exp in experience:
                # Company name
                story.append(Paragraph(exp.get('company', 'Company Name'), self.styles['ATSCompanyTitle']))
                
                # Position and dates on same line
                position_date = f"{exp.get('position', 'Position Title')}"
                if exp.get('dates'):
                    # Create a table for position and dates alignment
                    position_data = [[exp.get('position', 'Position Title'), exp['dates']]]
                    position_table = Table(position_data, colWidths=[4*inch, 2*inch])
                    position_table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                        ('FONTNAME', (1, 0), (1, 0), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, -1), 11),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('TOPPADDING', (0, 0), (-1, -1), 2),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                    ]))
                    story.append(position_table)
                else:
                    story.append(Paragraph(position_date, self.styles['ATSDetails']))
                
                # Location if available
                if exp.get('location'):
                    story.append(Paragraph(exp['location'], self.styles['ATSDetails']))
                
                # Achievements with tech focus
                for responsibility in exp.get('responsibilities', []):
                    story.append(Paragraph(f"• {responsibility}", self.styles['ATSBullet']))
                
                story.append(Spacer(1, 8))
        
        # Education
        education = data.get('education', [])
        if education:
            story.append(Paragraph("EDUCATION", self.styles['ATSSectionHeader']))
            
            for edu in education:
                # Create education table
                edu_data = []
                
                institution_line = edu.get('institution', 'Institution')
                if edu.get('location'):
                    institution_line += f", {edu['location']}"
                
                degree_year = edu.get('degree', 'Degree')
                if edu.get('year'):
                    degree_year += f" | {edu['year']}"
                
                edu_data.append([institution_line, degree_year])
                
                edu_table = Table(edu_data, colWidths=[4*inch, 2*inch])
                edu_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                story.append(edu_table)
                story.append(Spacer(1, 4))
        
        # Build PDF
        doc.build(story)
        
        return {
            'filename': filename,
            'pdf_path': file_path,
            'layout': 'tech_focused',
            'text_content': self._generate_text_version(data)
        }
    
    def _generate_classic_professional(self, data: Dict) -> Dict:
        """Generate Classic Professional layout"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"classic_professional_resume_{timestamp}.pdf"
        file_path = f"uploads/optimized/{filename}"
        
        doc = SimpleDocTemplate(file_path, pagesize=letter, rightMargin=inch, leftMargin=inch, topMargin=inch, bottomMargin=inch)
        
        story = []
        personal_info = data['personal_info']
        
        # Traditional header format
        if personal_info.get('name'):
            story.append(Paragraph(personal_info['name'].upper(), self.styles['ATSName']))
        
        # Address and contact (traditional format)
        contact_lines = []
        if personal_info.get('address'):
            contact_lines.append(personal_info['address'])
        
        phone_email = []
        if personal_info.get('phone'):
            phone_email.append(personal_info['phone'])
        if personal_info.get('email'):
            phone_email.append(personal_info['email'])
        
        if phone_email:
            contact_lines.append(' | '.join(phone_email))
        
        if personal_info.get('linkedin') or personal_info.get('github'):
            links = []
            if personal_info.get('linkedin'):
                links.append(personal_info['linkedin'])
            if personal_info.get('github'):
                links.append(personal_info['github'])
            contact_lines.append(' | '.join(links))
        
        for line in contact_lines:
            story.append(Paragraph(line, self.styles['ATSContact']))
        
        # Objective/Summary
        if data.get('professional_summary'):
            story.append(Paragraph("PROFESSIONAL SUMMARY", self.styles['ATSSectionHeader']))
            story.append(Paragraph(data['professional_summary'], self.styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Experience first (traditional format)
        experience = data.get('experience', [])
        if experience:
            story.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles['ATSSectionHeader']))
            
            for exp in experience:
                # Traditional format: Company, Position, Dates
                story.append(Paragraph(f"<b>{exp.get('company', 'Company Name')}</b>", self.styles['ATSCompanyTitle']))
                story.append(Paragraph(f"{exp.get('position', 'Position Title')} | {exp.get('dates', 'Dates')}", self.styles['ATSDetails']))
                
                if exp.get('location'):
                    story.append(Paragraph(exp['location'], self.styles['ATSDetails']))
                
                for responsibility in exp.get('responsibilities', []):
                    story.append(Paragraph(f"• {responsibility}", self.styles['ATSBullet']))
                
                story.append(Spacer(1, 8))
        
        # Education
        education = data.get('education', [])
        if education:
            story.append(Paragraph("EDUCATION", self.styles['ATSSectionHeader']))
            
            for edu in education:
                story.append(Paragraph(f"<b>{edu.get('institution', 'Institution')}</b>", self.styles['ATSCompanyTitle']))
                story.append(Paragraph(f"{edu.get('degree', 'Degree')} | {edu.get('year', 'Year')}", self.styles['ATSDetails']))
                if edu.get('location'):
                    story.append(Paragraph(edu['location'], self.styles['ATSDetails']))
                story.append(Spacer(1, 6))
        
        # Technical Skills
        skills = data.get('skills', {})
        if skills:
            story.append(Paragraph("TECHNICAL SKILLS", self.styles['ATSSectionHeader']))
            
            all_skills = []
            for category, skill_list in skills.items():
                all_skills.extend(skill_list)
            
            story.append(Paragraph(', '.join(all_skills), self.styles['ATSSkillList']))
        
        # Build PDF
        doc.build(story)
        
        return {
            'filename': filename,
            'pdf_path': file_path,
            'layout': 'classic_professional',
            'text_content': self._generate_text_version(data)
        }
    
    def _generate_executive_style(self, data: Dict) -> Dict:
        """Generate Executive Style layout"""
        # Implementation for executive layout
        return self._generate_modern_ats(data)  # Placeholder - will implement if needed
    
    def _generate_clean_minimal(self, data: Dict) -> Dict:
        """Generate Clean Minimal layout"""
        # Implementation for minimal layout  
        return self._generate_modern_ats(data)  # Placeholder - will implement if needed
    
    # Helper methods for data processing
    def _extract_personal_info(self, raw_data: Dict) -> Dict:
        """Extract and clean personal information"""
        
        # Get original resume text
        original_text = raw_data.get('original_resume_text', '')
        resume_analysis = raw_data.get('resume_analysis', {})
        
        # Extract name (first line typically)
        lines = [line.strip() for line in original_text.split('\n') if line.strip()]
        name = lines[0] if lines else "Your Name"
        
        # Clean name (remove email/phone if accidentally included)
        name = re.sub(r'[\+\d\s\-\(\)]{10,}', '', name)  # Remove phone numbers
        name = re.sub(r'\S+@\S+', '', name)  # Remove emails
        name = name.strip()
        
        # Extract contact info
        contact_info = resume_analysis.get('contact_info', {})
        
        # Extract phone from original text if not in analysis
        phone = contact_info.get('phone')
        if not phone:
            phone_match = re.search(r'(\+91[\s\-]?)?[6789]\d{9}', original_text)
            if phone_match:
                phone = phone_match.group(0)
        
        # Extract LinkedIn
        linkedin = None
        linkedin_match = re.search(r'linkedin\.com/in/([A-Za-z0-9\-]+)', original_text)
        if linkedin_match:
            linkedin = f"https://linkedin.com/in/{linkedin_match.group(1)}"
        
        # Extract GitHub
        github = None
        github_match = re.search(r'github\.com/([A-Za-z0-9\-]+)', original_text)
        if github_match:
            github = f"https://github.com/{github_match.group(1)}"
        
        return {
            'name': name,
            'email': contact_info.get('email'),
            'phone': phone,
            'linkedin': linkedin,
            'github': github,
            'address': None  # Extract if needed
        }
    
    def _extract_experience(self, raw_data: Dict) -> List[Dict]:
        """Extract and format professional experience"""
        
        original_text = raw_data.get('original_resume_text', '')
        lines = original_text.split('\n')
        
        experiences = []
        
        # Look for experience patterns in original text
        current_exp = None
        in_experience_section = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for experience section headers
            if re.match(r'(professional\s+)?experience|work\s+experience|employment', line.lower()):
                in_experience_section = True
                continue
            
            # Check for other section headers that end experience
            if re.match(r'education|skills|projects|certifications', line.lower()):
                in_experience_section = False
                continue
            
            if in_experience_section:
                # Look for company names (usually in caps or bold indicators)
                if line.isupper() or (len(line) < 50 and not line.startswith('•')):
                    if current_exp:
                        experiences.append(current_exp)
                    
                    current_exp = {
                        'company': line,
                        'position': '',
                        'dates': '',
                        'location': '',
                        'responsibilities': []
                    }
                
                # Look for position titles and dates
                elif current_exp and not current_exp['position']:
                    # Try to extract position and dates from line
                    date_pattern = r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|\d{4})'
                    if re.search(date_pattern, line.lower()):
                        # Line contains dates
                        current_exp['dates'] = line
                    else:
                        current_exp['position'] = line
                
                # Look for bullet points
                elif line.startswith('•') or line.startswith('-'):
                    if current_exp:
                        responsibility = line.lstrip('•- ').strip()
                        if responsibility:
                            current_exp['responsibilities'].append(responsibility)
        
        # Add last experience
        if current_exp:
            experiences.append(current_exp)
        
        # If no experiences found, create template
        if not experiences:
            job_analysis = raw_data.get('job_analysis', {})
            target_title = job_analysis.get('job_title', 'Target Position')
            
            experiences = [{
                'company': 'Company Name',
                'position': target_title,
                'dates': 'Start Date - End Date',
                'location': 'City, State',
                'responsibilities': [
                    'Developed and implemented solutions using relevant technologies',
                    'Collaborated with cross-functional teams to deliver high-quality results',
                    'Led initiatives that improved efficiency and system performance',
                    'Contributed to strategic planning and decision-making processes'
                ]
            }]
        
        return experiences
    
    def _categorize_skills(self, raw_data: Dict) -> Dict:
        """Categorize technical skills"""
        
        resume_analysis = raw_data.get('resume_analysis', {})
        job_analysis = raw_data.get('job_analysis', {})
        
        # Get all technical skills
        resume_skills = set(resume_analysis.get('technical_skills', []))
        job_skills = set(job_analysis.get('technical_skills', []))
        
        # Combine and categorize
        all_skills = resume_skills.union(job_skills)
        
        # Skill categories
        programming = []
        frameworks = []
        databases = []
        cloud = []
        other = []
        
        # Categorization logic
        programming_keywords = ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'sql', 'html', 'css']
        framework_keywords = ['react', 'angular', 'vue', 'nodejs', 'django', 'flask', 'spring', 'express', 'tailwind']
        database_keywords = ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle']
        cloud_keywords = ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'github']
        
        for skill in all_skills:
            skill_lower = skill.lower()
            if any(kw in skill_lower for kw in programming_keywords):
                programming.append(skill)
            elif any(kw in skill_lower for kw in framework_keywords):
                frameworks.append(skill)
            elif any(kw in skill_lower for kw in database_keywords):
                databases.append(skill)
            elif any(kw in skill_lower for kw in cloud_keywords):
                cloud.append(skill)
            else:
                other.append(skill)
        
        return {
            'programming': programming,
            'frameworks': frameworks,
            'databases': databases,
            'cloud': cloud,
            'other': other
        }
    
    def _extract_education(self, raw_data: Dict) -> List[Dict]:
        """Extract education information"""
        
        original_text = raw_data.get('original_resume_text', '')
        lines = original_text.split('\n')
        
        education = []
        in_education_section = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for education section
            if re.match(r'education|academic|qualifications', line.lower()):
                in_education_section = True
                continue
            
            # Check for other sections
            if re.match(r'experience|skills|projects', line.lower()):
                in_education_section = False
                continue
            
            if in_education_section:
                # Look for degree patterns
                degree_pattern = r'(b\.?tech|bachelor|master|m\.?tech|phd|diploma)'
                if re.search(degree_pattern, line.lower()):
                    education.append({
                        'institution': 'University Name',
                        'degree': line,
                        'year': 'Year',
                        'location': 'City, State'
                    })
        
        # Default education if none found
        if not education:
            education = [{
                'institution': 'University Name',
                'degree': 'Bachelor of Technology, Computer Science',
                'year': '2021 - 2025',
                'location': 'City, State'
            }]
        
        return education
    
    def _extract_additional_sections(self, raw_data: Dict) -> Dict:
        """Extract additional sections like certifications, projects"""
        return {
            'certifications': [],
            'projects': [],
            'languages': []
        }
    
    def _generate_professional_summary(self, raw_data: Dict) -> str:
        """Generate professional summary based on analysis"""
        
        resume_analysis = raw_data.get('resume_analysis', {})
        job_analysis = raw_data.get('job_analysis', {})
        
        experience_years = resume_analysis.get('experience_years', 3)
        job_title = job_analysis.get('job_title', 'Software Developer')
        
        # Get top skills
        technical_skills = resume_analysis.get('technical_skills', [])
        top_skills = ', '.join(technical_skills[:3]) if technical_skills else 'software development'
        
        summary = f"Results-driven professional with {experience_years}+ years of experience in {top_skills.lower()} and software development. "
        summary += f"Proven track record of delivering high-quality solutions and driving organizational success. "
        summary += f"Seeking to leverage technical expertise and problem-solving skills in a {job_title.lower()} role."
        
        return summary
    
    def _generate_text_version(self, data: Dict) -> str:
        """Generate plain text version of resume"""
        
        text_parts = []
        personal_info = data['personal_info']
        
        # Header
        if personal_info.get('name'):
            text_parts.append(personal_info['name'].upper())
            text_parts.append('=' * len(personal_info['name']))
        
        # Contact
        contact_parts = []
        for field in ['phone', 'email', 'linkedin', 'github']:
            if personal_info.get(field):
                contact_parts.append(personal_info[field])
        
        if contact_parts:
            text_parts.append(' | '.join(contact_parts))
            text_parts.append('')
        
        # Professional Summary
        if data.get('professional_summary'):
            text_parts.append('PROFESSIONAL SUMMARY')
            text_parts.append('-' * 20)
            text_parts.append(data['professional_summary'])
            text_parts.append('')
        
        # Technical Skills
        skills = data.get('skills', {})
        if skills:
            text_parts.append('TECHNICAL SKILLS')
            text_parts.append('-' * 15)
            for category, skill_list in skills.items():
                if skill_list:
                    text_parts.append(f"• {category.title()}: {', '.join(skill_list)}")
            text_parts.append('')
        
        # Experience
        experience = data.get('experience', [])
        if experience:
            text_parts.append('PROFESSIONAL EXPERIENCE')
            text_parts.append('-' * 24)
            for exp in experience:
                text_parts.append(f"{exp.get('company', 'Company')}")
                text_parts.append(f"{exp.get('position', 'Position')} | {exp.get('dates', 'Dates')}")
                if exp.get('location'):
                    text_parts.append(exp['location'])
                
                for resp in exp.get('responsibilities', []):
                    text_parts.append(f"• {resp}")
                text_parts.append('')
        
        # Education
        education = data.get('education', [])
        if education:
            text_parts.append('EDUCATION')
            text_parts.append('-' * 9)
            for edu in education:
                text_parts.append(f"{edu.get('institution', 'Institution')}")
                text_parts.append(f"{edu.get('degree', 'Degree')} | {edu.get('year', 'Year')}")
                text_parts.append('')
        
        return '\n'.join(text_parts)

def get_available_layouts() -> Dict[str, str]:
    """Get available resume layouts with descriptions"""
    return {
        'modern_ats': 'Modern ATS - Clean, professional layout optimized for ATS systems',
        'tech_focused': 'Tech Focused - Emphasizes technical skills and achievements', 
        'classic_professional': 'Classic Professional - Traditional corporate resume format'
    }
