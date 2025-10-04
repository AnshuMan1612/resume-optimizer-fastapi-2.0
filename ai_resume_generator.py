# app/services/ai_resume_generator.py
from typing import Dict, List
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

class AIEnhancedResumeGenerator:
    """
    AI-enhanced resume generator using Perplexity-optimized content
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_professional_styles()
    
    def _setup_professional_styles(self):
        """Setup premium resume styles"""
        
        # Executive name style
        self.styles.add(ParagraphStyle(
            name='ExecutiveName',
            parent=self.styles['Title'],
            fontSize=22,
            fontName='Helvetica-Bold',
            spaceAfter=6,
            textColor=colors.HexColor('#1a365d'),
            alignment=TA_CENTER,
            borderWidth=2,
            borderColor=colors.HexColor('#3182ce'),
            borderPadding=8
        ))
        
        # Premium contact style
        self.styles.add(ParagraphStyle(
            name='PremiumContact',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica',
            alignment=TA_CENTER,
            spaceAfter=16,
            textColor=colors.HexColor('#2d3748')
        ))
        
        # Section header with accent
        self.styles.add(ParagraphStyle(
            name='AccentHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            fontName='Helvetica-Bold',
            spaceBefore=20,
            spaceAfter=8,
            textColor=colors.HexColor('#1a365d'),
            borderWidth=1,
            borderColor=colors.HexColor('#3182ce'),
            borderPadding=4,
            backColor=colors.HexColor('#ebf8ff')
        ))
        
        # AI-optimized summary style
        self.styles.add(ParagraphStyle(
            name='AISummary',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica',
            spaceAfter=14,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#2d3748'),
            borderWidth=1,
            borderColor=colors.HexColor('#e2e8f0'),
            borderPadding=8
        ))
        
        # Achievement bullet style
        self.styles.add(ParagraphStyle(
            name='Achievement',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            spaceAfter=4,
            leftIndent=20,
            bulletIndent=10,
            textColor=colors.HexColor('#2d3748')
        ))
    
    def generate_ai_optimized_resume(
        self, 
        original_resume_text: str, 
        resume_analysis: Dict,
        job_analysis: Dict, 
        perplexity_analysis: Dict,
        optimized_content: Dict
    ) -> Dict:
        """Generate premium AI-optimized resume"""
        
        print("🎨 Generating AI-enhanced premium resume...")
        
        # Extract personal info
        personal_info = self._extract_enhanced_personal_info(
            original_resume_text, 
            resume_analysis
        )
        
        # Create premium content structure
        premium_content = {
            'personal_info': personal_info,
            'ai_summary': optimized_content.get('professional_summary', ''),
            'key_achievements': optimized_content.get('key_achievements', []),
            'optimized_skills': self._create_premium_skills_section(
                resume_analysis, job_analysis
            ),
            'enhanced_experience': optimized_content.get('optimized_experience_bullets', []),
            'perplexity_insights': perplexity_analysis
        }
        
        # Generate premium PDF
        pdf_path = self._generate_premium_pdf(premium_content, job_analysis)
        
        # Generate enhanced text version
        text_content = self._generate_premium_text(premium_content)
        
        print(f"✅ AI-enhanced resume generated: {os.path.basename(pdf_path)}")
        
        return {
            'text_content': text_content,
            'pdf_path': pdf_path,
            'filename': os.path.basename(pdf_path),
            'enhancement_level': 'premium_ai',
            'perplexity_powered': True
        }
    
    def _extract_enhanced_personal_info(self, text: str, analysis: Dict) -> Dict:
        """Extract and enhance personal information"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        name = lines[0] if lines else "Professional Name"
        
        contact_info = analysis.get('contact_info', {})
        
        return {
            'name': name,
            'email': contact_info.get('email'),
            'phone': contact_info.get('phone'),
            'linkedin': self._extract_linkedin(text),
            'location': self._extract_location(text),
            'portfolio': self._extract_portfolio(text)
        }
    
    def _create_premium_skills_section(self, resume_analysis: Dict, job_analysis: Dict) -> Dict:
        """Create premium skills section with AI insights"""
        
        # Get skills with priority ranking
        resume_tech = set(resume_analysis.get('technical_skills', []))
        job_tech = set(job_analysis.get('technical_skills', []))
        
        # Prioritize matched skills
        matched_skills = list(resume_tech.intersection(job_tech))
        additional_resume_skills = list(resume_tech - job_tech)
        recommended_skills = list(job_tech - resume_tech)
        
        return {
            'priority_skills': matched_skills,
            'additional_skills': additional_resume_skills,
            'recommended_additions': recommended_skills[:5],
            'soft_skills': resume_analysis.get('soft_skills', [])
        }
    
    def _generate_premium_pdf(self, content: Dict, job_analysis: Dict) -> str:
        """Generate premium AI-optimized PDF"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_optimized_resume_{timestamp}.pdf"
        file_path = f"uploads/optimized/{filename}"
        
        # Create premium document
        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        personal_info = content['personal_info']
        
        # Executive header with name
        if personal_info.get('name'):
            story.append(Paragraph(personal_info['name'], self.styles['ExecutiveName']))
        
        # Premium contact information
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(f"📧 {personal_info['email']}")
        if personal_info.get('phone'):
            contact_parts.append(f"📱 {personal_info['phone']}")
        if personal_info.get('linkedin'):
            contact_parts.append(f"🔗 {personal_info['linkedin']}")
        if personal_info.get('location'):
            contact_parts.append(f"📍 {personal_info['location']}")
        
        if contact_parts:
            contact_text = ' | '.join(contact_parts)
            story.append(Paragraph(contact_text, self.styles['PremiumContact']))
        
        # AI-optimized professional summary
        if content.get('ai_summary'):
            story.append(Paragraph("EXECUTIVE SUMMARY", self.styles['AccentHeader']))
            story.append(Paragraph(content['ai_summary'], self.styles['AISummary']))
        
        # Key achievements section
        key_achievements = content.get('key_achievements', [])
        if key_achievements:
            story.append(Paragraph("KEY ACHIEVEMENTS", self.styles['AccentHeader']))
            for achievement in key_achievements:
                story.append(Paragraph(f"🏆 {achievement}", self.styles['Achievement']))
            story.append(Spacer(1, 12))
        
        # Premium technical skills
        skills = content.get('optimized_skills', {})
        if skills.get('priority_skills') or skills.get('additional_skills'):
            story.append(Paragraph("TECHNICAL EXPERTISE", self.styles['AccentHeader']))
            
            # Create premium skills table
            skills_data = []
            
            if skills.get('priority_skills'):
                skills_data.append(['Core Technologies:', ', '.join(skills['priority_skills'])])
            
            if skills.get('additional_skills'):
                skills_data.append(['Additional Skills:', ', '.join(skills['additional_skills'][:8])])
            
            if skills.get('soft_skills'):
                skills_data.append(['Professional Skills:', ', '.join(skills['soft_skills'][:6])])
            
            if skills_data:
                skills_table = Table(skills_data, colWidths=[1.5*inch, 5*inch])
                skills_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
                ]))
                story.append(skills_table)
                story.append(Spacer(1, 16))
        
        # Professional experience with AI enhancements
        enhanced_experience = content.get('enhanced_experience', [])
        if enhanced_experience:
            story.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles['AccentHeader']))
            
            # Add enhanced experience bullets
            for exp in enhanced_experience:
                story.append(Paragraph(f"• {exp}", self.styles['Achievement']))
            
            story.append(Spacer(1, 16))
        
        # AI insights footer
        if content.get('perplexity_insights'):
            story.append(Paragraph("OPTIMIZATION NOTES", self.styles['AccentHeader']))
            story.append(Paragraph(
                "This resume has been AI-optimized using advanced analysis for maximum ATS compatibility and recruiter appeal.",
                self.styles['Normal']
            ))
        
        # Build the premium PDF
        doc.build(story)
        return file_path
    
    def _generate_premium_text(self, content: Dict) -> str:
        """Generate premium text version"""
        
        text_parts = []
        personal_info = content['personal_info']
        
        # Header
        if personal_info.get('name'):
            name = personal_info['name']
            text_parts.append(name.upper())
            text_parts.append('=' * len(name))
        
        # Contact info
        contact_parts = []
        for field in ['email', 'phone', 'linkedin', 'location']:
            if personal_info.get(field):
                contact_parts.append(f"{field.title()}: {personal_info[field]}")
        
        if contact_parts:
            text_parts.extend(contact_parts)
            text_parts.append('')
        
        # AI-optimized summary
        if content.get('ai_summary'):
            text_parts.append('EXECUTIVE SUMMARY')
            text_parts.append('-' * 17)
            text_parts.append(content['ai_summary'])
            text_parts.append('')
        
        # Key achievements
        if content.get('key_achievements'):
            text_parts.append('KEY ACHIEVEMENTS')
            text_parts.append('-' * 16)
            for achievement in content['key_achievements']:
                text_parts.append(f"🏆 {achievement}")
            text_parts.append('')
        
        # Technical skills
        skills = content.get('optimized_skills', {})
        if skills:
            text_parts.append('TECHNICAL EXPERTISE')
            text_parts.append('-' * 19)
            
            if skills.get('priority_skills'):
                text_parts.append(f"Core Technologies: {', '.join(skills['priority_skills'])}")
            
            if skills.get('additional_skills'):
                text_parts.append(f"Additional Skills: {', '.join(skills['additional_skills'])}")
            
            text_parts.append('')
        
        # Enhanced experience
        if content.get('enhanced_experience'):
            text_parts.append('PROFESSIONAL EXPERIENCE (AI-ENHANCED)')
            text_parts.append('-' * 38)
            for exp in content['enhanced_experience']:
                text_parts.append(f"• {exp}")
            text_parts.append('')
        
        return '\n'.join(text_parts)
    
    def _extract_linkedin(self, text: str) -> str:
        """Extract LinkedIn profile"""
        import re
        linkedin_pattern = r'linkedin\.com/(?:in/)?([A-Za-z0-9-]+)'
        matches = re.findall(linkedin_pattern, text)
        return f"linkedin.com/in/{matches[0]}" if matches else None
    
    def _extract_location(self, text: str) -> str:
        """Extract location information"""
        import re
        location_patterns = [
            r'([A-Za-z\s]+,\s*[A-Za-z]{2})',
            r'([A-Za-z\s]+,\s*[A-Za-z\s]+)'
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        return None
    
    def _extract_portfolio(self, text: str) -> str:
        """Extract portfolio or website URL"""
        import re
        url_pattern = r'https?://(?:www\.)?([A-Za-z0-9.-]+\.[A-Za-z]{2,})'
        matches = re.findall(url_pattern, text)
        
        for match in matches:
            if 'linkedin' not in match and 'email' not in match:
                return f"https://{match}"
        return None
