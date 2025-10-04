# app/services/simple_analyzer.py - Enhanced Compatibility Wrapper
"""
Simple analyzer that wraps the EnhancedResumeAnalyzer for backward compatibility
Provides simple method names while using advanced functionality under the hood
"""

from app.services.enhanced_analyzer import EnhancedResumeAnalyzer
from typing import Dict, List

class SimpleAnalyzer(EnhancedResumeAnalyzer):
    """
    Backward compatibility wrapper for EnhancedResumeAnalyzer
    Provides simple method names while using advanced 500+ skills functionality
    """
    
    def __init__(self):
        super().__init__()
        print("✅ Simple Analyzer initialized (using Enhanced backend)")
    
    def analyze_job(self, job_text: str) -> Dict:
        """
        Simple wrapper for analyze_job_description
        Maintains backward compatibility while using enhanced analysis
        """
        try:
            return self.analyze_job_description(job_text)
        except Exception as e:
            print(f"⚠️ Job analysis error: {e}")
            # Fallback basic analysis
            return {
                'technical_skills': [],
                'soft_skills': [],
                'keywords': [],
                'experience_required': 0,
                'job_level': 'Mid-level'
            }
    
    def calculate_match_score(self, resume_analysis: Dict, job_analysis: Dict) -> Dict:
        """
        Simple wrapper for calculate_advanced_match_score
        Returns enhanced scoring while maintaining simple interface
        """
        try:
            return self.calculate_advanced_match_score(resume_analysis, job_analysis)
        except Exception as e:
            print(f"⚠️ Match score calculation error: {e}")
            # Fallback basic scoring
            resume_tech = set(resume_analysis.get('technical_skills', []))
            job_tech = set(job_analysis.get('technical_skills', []))
            
            tech_score = (len(resume_tech.intersection(job_tech)) / len(job_tech) * 100) if job_tech else 100
            
            return {
                'overall_score': tech_score,
                'technical_score': tech_score,
                'soft_skills_score': 100,
                'matched_skills': list(resume_tech.intersection(job_tech)),
                'missing_technical_skills': list(job_tech - resume_tech),
                'missing_soft_skills': []
            }
    
    def generate_suggestions(self, match_analysis: Dict, resume_analysis: Dict, job_analysis: Dict) -> List[str]:
        """
        Simple wrapper for generate_advanced_suggestions
        Provides actionable recommendations using advanced logic
        """
        try:
            return self.generate_advanced_suggestions(match_analysis, resume_analysis, job_analysis)
        except Exception as e:
            print(f"⚠️ Suggestions generation error: {e}")
            # Fallback basic suggestions
            suggestions = []
            
            if match_analysis.get('overall_score', 0) < 60:
                suggestions.append("💡 Add more relevant technical skills from the job description")
            
            missing_tech = match_analysis.get('missing_technical_skills', [])
            if missing_tech:
                suggestions.append(f"🔧 Include these technical skills: {', '.join(missing_tech[:3])}")
            
            suggestions.extend([
                "📋 Use standard resume section headings (Experience, Education, Skills)",
                "🎯 Include both acronyms and full terms (e.g., AI/Artificial Intelligence)", 
                "📊 Add quantified achievements with specific numbers and percentages",
                "🤖 Ensure ATS-friendly formatting without tables or complex layouts"
            ])
            
            return suggestions
    
    # Additional convenience methods for compatibility
    def get_technical_skills_count(self, analysis: Dict) -> int:
        """Get count of technical skills found"""
        return len(analysis.get('technical_skills', []))
    
    def get_match_strength(self, score: float) -> str:
        """Categorize match strength based on score"""
        if score >= 85:
            return 'excellent'
        elif score >= 70:
            return 'good'
        elif score >= 50:
            return 'fair'
        else:
            return 'needs_improvement'
    
    def is_ats_friendly(self, resume_text: str) -> bool:
        """Basic ATS compatibility check"""
        try:
            analysis = self.analyze_resume(resume_text)
            ats_score = analysis.get('ats_compatibility_score', 0)
            return ats_score >= 70
        except:
            return False
