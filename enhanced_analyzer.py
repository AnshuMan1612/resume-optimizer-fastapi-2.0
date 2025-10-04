# app/services/enhanced_analyzer.py
import re
from typing import List, Dict, Set, Tuple
from collections import Counter
import json

class EnhancedResumeAnalyzer:
    """
    Advanced resume and job analysis with enhanced skill detection,
    industry-specific insights, and detailed matching algorithms
    """
    
    def __init__(self):
        self._initialize_skill_databases()
        self._initialize_analysis_patterns()
    
    def _initialize_skill_databases(self):
        """Initialize comprehensive skill databases by category"""
        
        # Programming Languages (expanded)
        self.programming_languages = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 
            'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash', 
            'powershell', 'sql', 'html', 'css', 'sass', 'less', 'dart', 'elixir', 'haskell',
            'clojure', 'f#', 'vb.net', 'cobol', 'fortran', 'assembly', 'lua', 'groovy'
        ]
        
        # Frameworks and Libraries
        self.frameworks_libraries = [
            'react', 'angular', 'vue', 'svelte', 'ember', 'backbone', 'jquery', 'nodejs', 
            'express', 'koa', 'fastify', 'django', 'flask', 'fastapi', 'pyramid', 'tornado',
            'spring', 'spring boot', 'hibernate', 'struts', 'laravel', 'symfony', 'codeigniter',
            'rails', 'sinatra', 'asp.net', 'mvc', 'blazor', 'xamarin', 'unity', 'unreal',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib',
            'seaborn', 'plotly', 'opencv', 'nltk', 'spacy', 'hugging face', 'transformers'
        ]
        
        # Databases
        self.databases = [
            'mysql', 'postgresql', 'sqlite', 'oracle', 'sql server', 'mongodb', 'cassandra',
            'redis', 'elasticsearch', 'solr', 'neo4j', 'dynamodb', 'couchdb', 'influxdb',
            'firebase', 'mariadb', 'cockroachdb', 'amazon rds', 'azure sql', 'google cloud sql'
        ]
        
        # Cloud Platforms and DevOps
        self.cloud_devops = [
            'aws', 'azure', 'gcp', 'google cloud platform', 'digital ocean', 'linode',
            'docker', 'kubernetes', 'openshift', 'helm', 'istio', 'jenkins', 'github actions',
            'gitlab ci', 'circle ci', 'travis ci', 'azure devops', 'terraform', 'ansible',
            'chef', 'puppet', 'vagrant', 'packer', 'consul', 'vault', 'nomad', 'prometheus',
            'grafana', 'elk stack', 'datadog', 'new relic', 'splunk', 'nagios', 'zabbix'
        ]
        
        # Tools and Technologies
        self.tools_technologies = [
            'git', 'github', 'gitlab', 'bitbucket', 'svn', 'mercurial', 'jira', 'confluence',
            'slack', 'microsoft teams', 'zoom', 'figma', 'sketch', 'adobe xd', 'photoshop',
            'illustrator', 'after effects', 'premiere pro', 'blender', 'autocad', 'solidworks',
            'excel', 'powerbi', 'tableau', 'qlik', 'looker', 'apache spark', 'hadoop',
            'kafka', 'rabbitmq', 'celery', 'airflow', 'luigi', 'prefect', 'dbt'
        ]
        
        # Soft Skills (enhanced)
        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'collaboration', 'problem solving',
            'analytical thinking', 'critical thinking', 'creative thinking', 'innovation',
            'adaptability', 'flexibility', 'resilience', 'time management', 'organization',
            'project management', 'stakeholder management', 'client relations', 'customer service',
            'presentation skills', 'public speaking', 'negotiation', 'conflict resolution',
            'mentoring', 'coaching', 'training', 'strategic planning', 'decision making',
            'attention to detail', 'quality assurance', 'continuous improvement', 'agile mindset',
            'emotional intelligence', 'cultural awareness', 'remote work', 'cross-functional collaboration'
        ]
        
        # Methodologies and Practices
        self.methodologies = [
            'agile', 'scrum', 'kanban', 'lean', 'six sigma', 'devops', 'ci/cd', 'tdd', 'bdd',
            'pair programming', 'code review', 'microservices', 'monolith', 'serverless',
            'event-driven architecture', 'domain-driven design', 'clean architecture',
            'solid principles', 'design patterns', 'rest api', 'graphql', 'grpc',
            'oauth', 'jwt', 'saml', 'ldap', 'sso', 'encryption', 'ssl/tls', 'penetration testing',
            'vulnerability assessment', 'compliance', 'gdpr', 'hipaa', 'sox', 'pci dss'
        ]
        
        # Industry-specific skills
        self.industry_skills = {
            'fintech': ['blockchain', 'cryptocurrency', 'defi', 'trading algorithms', 'risk management', 'compliance', 'kyc', 'aml'],
            'healthcare': ['hipaa', 'hl7', 'fhir', 'medical devices', 'clinical trials', 'telemedicine', 'ehr', 'emr'],
            'ecommerce': ['payment processing', 'inventory management', 'supply chain', 'logistics', 'crm', 'shopify', 'magento', 'woocommerce'],
            'gaming': ['game engines', 'unity', 'unreal engine', 'c#', 'c++', 'graphics programming', 'shader programming', 'multiplayer networking'],
            'iot': ['embedded systems', 'sensors', 'actuators', 'edge computing', 'mqtt', 'lorawan', 'zigbee', 'bluetooth'],
            'ai_ml': ['machine learning', 'deep learning', 'neural networks', 'computer vision', 'nlp', 'reinforcement learning', 'mlops', 'model deployment']
        }
        
        # Combine all technical skills
        self.all_technical_skills = (
            self.programming_languages + self.frameworks_libraries + self.databases + 
            self.cloud_devops + self.tools_technologies + self.methodologies
        )
        
        # Add industry-specific skills
        for industry_skills in self.industry_skills.values():
            self.all_technical_skills.extend(industry_skills)
        
        # Remove duplicates while preserving order
        self.all_technical_skills = list(dict.fromkeys(self.all_technical_skills))
    
    def _initialize_analysis_patterns(self):
        """Initialize regex patterns for various analysis tasks"""
        
        # Experience extraction patterns
        self.experience_patterns = [
            r'(\d+)[\+]?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)[\+]?\s*(?:year|yr)\s*(?:experience|exp)',
            r'experience[:\s]*(\d+)[\+]?\s*(?:years?|yrs?)',
            r'(\d+)[\+]?\s*(?:years?|yrs?)\s*(?:in|with|of)',
            r'over\s*(\d+)\s*(?:years?|yrs?)',
            r'more than\s*(\d+)\s*(?:years?|yrs?)'
        ]
        
        # Education patterns
        self.education_patterns = {
            'phd': [r'\bphd\b', r'\bph\.d\b', r'\bdoctorate\b', r'\bdoctoral\b'],
            'masters': [r'\bmaster[\'s]?\b', r'\bmba\b', r'\bms\b', r'\bm\.s\b', r'\bma\b', r'\bm\.a\b', r'\bmsc\b', r'\bm\.sc\b'],
            'bachelors': [r'\bbachelor[\'s]?\b', r'\bbs\b', r'\bb\.s\b', r'\bba\b', r'\bb\.a\b', r'\bbsc\b', r'\bb\.sc\b', r'\bbtech\b', r'\bb\.tech\b'],
            'associates': [r'\bassociate[\'s]?\b', r'\bas\b', r'\ba\.s\b', r'\bdiploma\b']
        }
        
        # Contact information patterns
        self.contact_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(\+\d{1,3}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            'linkedin': r'linkedin\.com/(?:in/)?([A-Za-z0-9-]+)',
            'github': r'github\.com/([A-Za-z0-9-]+)'
        }
        
        # Job level indicators
        self.job_level_patterns = {
            'senior': ['senior', 'lead', 'principal', 'staff', 'architect', 'manager', 'director', 'head of', 'vp', 'cto', 'cio'],
            'mid': ['mid-level', 'intermediate', 'experienced', 'specialist', 'analyst', 'developer', 'engineer'],
            'junior': ['junior', 'entry', 'entry-level', 'associate', 'intern', 'trainee', 'graduate', 'assistant']
        }
    
    def analyze_resume(self, resume_text: str) -> Dict:
        """
        Comprehensive resume analysis with enhanced insights
        """
        if not resume_text or len(resume_text.strip()) < 50:
            raise ValueError("Resume text is too short or empty for meaningful analysis")
        
        resume_lower = resume_text.lower()
        
        print("🔍 Performing comprehensive resume analysis...")
        
        # Basic analysis
        basic_analysis = {
            'word_count': len(resume_text.split()),
            'character_count': len(resume_text),
            'line_count': len([line for line in resume_text.split('\n') if line.strip()]),
            'paragraph_count': len([p for p in resume_text.split('\n\n') if p.strip()])
        }
        
        # Skills analysis
        skills_analysis = self._analyze_skills(resume_lower)
        
        # Experience analysis
        experience_analysis = self._analyze_experience(resume_lower)
        
        # Education analysis
        education_analysis = self._analyze_education(resume_lower)
        
        # Contact information
        contact_analysis = self._analyze_contact_info(resume_text)
        
        # Content quality analysis
        quality_analysis = self._analyze_content_quality(resume_text)
        
        # Keywords extraction
        keywords = self._extract_advanced_keywords(resume_text)
        
        # Industry detection
        industry = self._detect_industry(resume_lower)
        
        # Combine all analysis results
        analysis_result = {
            **basic_analysis,
            **skills_analysis,
            **experience_analysis,
            **education_analysis,
            'contact_info': contact_analysis,
            'quality_metrics': quality_analysis,
            'keywords': keywords,
            'detected_industry': industry,
            'ats_compatibility_score': self._calculate_ats_compatibility(resume_text)
        }
        
        print(f"✅ Resume analysis complete - {len(skills_analysis['technical_skills'])} technical skills found")
        
        return analysis_result
    
    def analyze_job_description(self, job_text: str) -> Dict:
        """
        Enhanced job description analysis
        """
        if not job_text or len(job_text.strip()) < 50:
            raise ValueError("Job description is too short for meaningful analysis")
        
        job_lower = job_text.lower()
        
        print("💼 Analyzing job description requirements...")
        
        # Skills analysis
        skills_analysis = self._analyze_skills(job_lower)
        
        # Requirements analysis
        requirements_analysis = self._analyze_job_requirements(job_lower)
        
        # Company analysis
        company_analysis = self._analyze_company_info(job_text)
        
        # Urgency and priority analysis
        urgency_analysis = self._analyze_job_urgency(job_lower)
        
        # Keywords extraction
        keywords = self._extract_advanced_keywords(job_text)
        
        # Industry detection
        industry = self._detect_industry(job_lower)
        
        analysis_result = {
            **skills_analysis,
            **requirements_analysis,
            **company_analysis,
            **urgency_analysis,
            'keywords': keywords,
            'industry': industry,
            'job_complexity_score': self._calculate_job_complexity(job_text)
        }
        
        print(f"✅ Job analysis complete - {analysis_result['job_level']} position requiring {len(skills_analysis['technical_skills'])} technical skills")
        
        return analysis_result
    
    def calculate_advanced_match_score(self, resume_analysis: Dict, job_analysis: Dict) -> Dict:
        """
        Advanced matching algorithm with weighted scoring
        """
        print("🎯 Calculating advanced compatibility scores...")
        
        # Get skill sets
        resume_tech = set(resume_analysis.get('technical_skills', []))
        job_tech = set(job_analysis.get('technical_skills', []))
        
        resume_soft = set(resume_analysis.get('soft_skills', []))
        job_soft = set(job_analysis.get('soft_skills', []))
        
        # Technical skills matching
        tech_matches = resume_tech.intersection(job_tech)
        tech_score = (len(tech_matches) / len(job_tech) * 100) if job_tech else 100
        
        # Soft skills matching
        soft_matches = resume_soft.intersection(job_soft)
        soft_score = (len(soft_matches) / len(job_soft) * 100) if job_soft else 100
        
        # Experience level matching
        resume_exp = resume_analysis.get('experience_years', 0)
        required_exp = job_analysis.get('experience_required', 0)
        exp_score = self._calculate_experience_score(resume_exp, required_exp)
        
        # Education level matching
        education_score = self._calculate_education_score(
            resume_analysis.get('education_level'),
            job_analysis.get('education_required')
        )
        
        # Industry alignment
        industry_score = self._calculate_industry_alignment(
            resume_analysis.get('detected_industry'),
            job_analysis.get('industry')
        )
        
        # Keywords overlap
        resume_keywords = set(resume_analysis.get('keywords', []))
        job_keywords = set(job_analysis.get('keywords', []))
        keyword_matches = resume_keywords.intersection(job_keywords)
        keyword_score = (len(keyword_matches) / len(job_keywords) * 100) if job_keywords else 0
        
        # ATS compatibility factor
        ats_factor = resume_analysis.get('ats_compatibility_score', 0) / 100
        
        # Weighted overall score
        weights = {
            'technical': 0.35,
            'soft_skills': 0.15,
            'experience': 0.20,
            'education': 0.10,
            'industry': 0.10,
            'keywords': 0.10
        }
        
        weighted_score = (
            tech_score * weights['technical'] +
            soft_score * weights['soft_skills'] +
            exp_score * weights['experience'] +
            education_score * weights['education'] +
            industry_score * weights['industry'] +
            keyword_score * weights['keywords']
        )
        
        # Apply ATS compatibility factor
        final_score = weighted_score * (0.7 + 0.3 * ats_factor)
        
        # Detailed breakdown
        match_result = {
            'overall_score': round(final_score, 1),
            'technical_score': round(tech_score, 1),
            'soft_skills_score': round(soft_score, 1),
            'experience_score': round(exp_score, 1),
            'education_score': round(education_score, 1),
            'industry_score': round(industry_score, 1),
            'keyword_score': round(keyword_score, 1),
            'ats_compatibility_score': round(resume_analysis.get('ats_compatibility_score', 0), 1),
            
            # Detailed matches and gaps
            'matched_technical_skills': list(tech_matches),
            'missing_technical_skills': list(job_tech - resume_tech),
            'matched_soft_skills': list(soft_matches),
            'missing_soft_skills': list(job_soft - resume_soft),
            'matched_keywords': list(keyword_matches),
            
            # Combined matched skills for display
            'matched_skills': list(tech_matches.union(soft_matches)),
            
            # Experience gap analysis
            'experience_gap': max(0, required_exp - resume_exp),
            'experience_surplus': max(0, resume_exp - required_exp),
            
            # Match strength indicators
            'match_strength': self._categorize_match_strength(final_score),
            'top_skill_gaps': self._identify_top_skill_gaps(job_tech - resume_tech, job_analysis),
            
            # Scoring weights used
            'scoring_weights': weights
        }
        
        print(f"✅ Match analysis complete - Overall score: {match_result['overall_score']}%")
        
        return match_result
    
    def generate_advanced_suggestions(self, match_analysis: Dict, resume_analysis: Dict, job_analysis: Dict) -> List[str]:
        """
        Generate prioritized, actionable optimization suggestions
        """
        suggestions = []
        overall_score = match_analysis['overall_score']
        match_strength = match_analysis['match_strength']
        
        # Priority 1: Critical issues (always show first)
        if overall_score < 40:
            suggestions.append("🚨 CRITICAL: Your resume requires major optimization. Consider professional resume writing services or significant restructuring.")
        
        # Priority 2: Technical skills gaps
        missing_tech = match_analysis['missing_technical_skills']
        if missing_tech:
            top_missing = match_analysis.get('top_skill_gaps', missing_tech[:5])
            if len(top_missing) > 3:
                suggestions.append(f"🔧 HIGH PRIORITY: Add these critical technical skills: {', '.join(top_missing[:3])}. Consider online courses or certifications.")
            else:
                suggestions.append(f"🔧 TECHNICAL SKILLS: Include experience with {', '.join(top_missing)} in your resume.")
        
        # Priority 3: Experience level issues
        exp_gap = match_analysis.get('experience_gap', 0)
        if exp_gap > 2:
            suggestions.append(f"📈 EXPERIENCE GAP: You need {exp_gap} more years of experience. Highlight relevant projects, internships, and volunteer work to bridge this gap.")
        elif exp_gap > 0:
            suggestions.append(f"📊 Emphasize transferable skills and relevant projects to compensate for the {exp_gap}-year experience gap.")
        
        exp_surplus = match_analysis.get('experience_surplus', 0)
        if exp_surplus > 5:
            suggestions.append("💼 You're significantly overqualified. Consider applying for senior positions or highlighting leadership and mentoring experience.")
        
        # Priority 4: Soft skills
        missing_soft = match_analysis['missing_soft_skills']
        if missing_soft and len(missing_soft) > 2:
            suggestions.append(f"🤝 SOFT SKILLS: Demonstrate these competencies: {', '.join(missing_soft[:3])}. Use specific examples in your experience section.")
        
        # Priority 5: ATS Optimization
        ats_score = match_analysis.get('ats_compatibility_score', 0)
        if ats_score < 70:
            suggestions.append("🤖 ATS COMPATIBILITY: Improve formatting - use standard fonts, avoid tables/images, and include standard section headings ('Experience', 'Education', 'Skills').")
        
        # Priority 6: Content optimization
        quality_score = resume_analysis.get('quality_metrics', {}).get('overall_quality', 0)
        if quality_score < 70:
            suggestions.append("✍️ CONTENT QUALITY: Add more quantified achievements (e.g., 'Increased efficiency by 25%', 'Led team of 8 developers').")
        
        # Priority 7: Keywords optimization
        keyword_score = match_analysis.get('keyword_score', 0)
        if keyword_score < 60:
            suggestions.append("🎯 KEYWORDS: Incorporate more job-specific terms naturally throughout your resume. Use both acronyms and full terms (e.g., 'AI/Artificial Intelligence').")
        
        # Priority 8: Industry alignment
        industry_score = match_analysis.get('industry_score', 0)
        if industry_score < 70:
            detected_industry = resume_analysis.get('detected_industry')
            job_industry = job_analysis.get('industry')
            if detected_industry and job_industry and detected_industry != job_industry:
                suggestions.append(f"🏢 INDUSTRY FOCUS: Tailor your experience to emphasize {job_industry} industry knowledge and terminology.")
        
        # Priority 9: Education recommendations
        education_score = match_analysis.get('education_score', 0)
        if education_score < 80:
            required_edu = job_analysis.get('education_required')
            if required_edu:
                suggestions.append(f"🎓 EDUCATION: Ensure your {required_edu} degree is prominently displayed. Include relevant coursework if applicable.")
        
        # Priority 10: General optimization based on match strength
        if match_strength == 'poor':
            suggestions.append("📋 STRATEGY: Consider significant resume restructuring. Focus on the top 3-5 missing skills and create specific examples of how you've used similar technologies.")
        elif match_strength == 'fair':
            suggestions.append("📝 OPTIMIZATION: You're close to a good match. Focus on incorporating the missing technical skills and quantifying your achievements.")
        elif match_strength == 'good':
            suggestions.append("🔧 FINE-TUNING: Minor adjustments needed. Add the missing skills and ensure your resume is ATS-optimized.")
        else:  # excellent
            suggestions.append("⭐ EXCELLENT MATCH: Your resume aligns well with this position. Consider customizing your summary to mention specific company needs.")
        
        # Priority 11: Universal best practices (always include 2-3)
        universal_suggestions = [
            "📊 Use specific metrics and numbers to demonstrate impact (e.g., 'Reduced processing time by 40%', 'Managed $2M budget')",
            "💪 Start bullet points with strong action verbs: Architected, Optimized, Spearheaded, Streamlined, Pioneered",
            "🎯 Customize your Professional Summary to directly address the job requirements and company needs",
            "📱 Ensure your resume is mobile-friendly and prints correctly in both PDF and text formats",
            "🔄 Use consistent formatting, bullet styles, and date formats throughout your resume"
        ]
        
        # Add 2-3 universal suggestions based on current gaps
        suggestions.extend(universal_suggestions[:3])
        
        # Limit to top 10 suggestions to avoid overwhelming the user
        return suggestions[:10]
    
    # Helper methods for analysis
    def _analyze_skills(self, text: str) -> Dict:
        """Analyze and categorize skills found in text"""
        found_technical = []
        found_soft = []
        
        # Technical skills detection with context awareness
        for skill in self.all_technical_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text):
                found_technical.append(skill)
        
        # Soft skills detection
        for skill in self.soft_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text):
                found_soft.append(skill)
        
        return {
            'technical_skills': found_technical,
            'soft_skills': found_soft
        }
    
    def _analyze_experience(self, text: str) -> Dict:
        """Extract and analyze experience information"""
        years = []
        
        for pattern in self.experience_patterns:
            matches = re.findall(pattern, text)
            years.extend([int(match) for match in matches if match.isdigit()])
        
        experience_years = max(years) if years else 0
        
        return {
            'experience_years': experience_years,
            'experience_level': self._categorize_experience_level(experience_years)
        }
    
    def _analyze_education(self, text: str) -> Dict:
        """Analyze education level and details"""
        education_level = None
        education_score = 0
        
        # Check for education levels in priority order
        for level, patterns in self.education_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    education_level = level
                    education_score = {'phd': 100, 'masters': 85, 'bachelors': 70, 'associates': 50}.get(level, 0)
                    break
            if education_level:
                break
        
        return {
            'education_level': education_level,
            'education_score': education_score
        }
    
    def _analyze_contact_info(self, text: str) -> Dict:
        """Extract contact information"""
        contact_info = {}
        
        for contact_type, pattern in self.contact_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                contact_info[contact_type] = matches[0] if isinstance(matches[0], str) else matches[0]
        
        return contact_info
    
    def _analyze_content_quality(self, text: str) -> Dict:
        """Analyze resume content quality"""
        
        # Quantification analysis
        numbers = re.findall(r'\d+(?:\.\d+)?(?:%|k|m|b|\$|€|£)', text.lower())
        quantification_score = min(100, len(numbers) * 10)
        
        # Action verbs analysis
        action_verbs = [
            'achieved', 'administered', 'analyzed', 'architected', 'automated', 'built', 'collaborated',
            'created', 'delivered', 'designed', 'developed', 'directed', 'enhanced', 'established',
            'executed', 'implemented', 'improved', 'increased', 'led', 'managed', 'optimized',
            'organized', 'pioneered', 'reduced', 'resolved', 'spearheaded', 'streamlined'
        ]
        
        action_verb_count = sum(1 for verb in action_verbs if verb in text.lower())
        action_verb_score = min(100, action_verb_count * 5)
        
        # Overall quality score
        overall_quality = (quantification_score * 0.6 + action_verb_score * 0.4)
        
        return {
            'quantification_score': quantification_score,
            'action_verb_score': action_verb_score,
            'overall_quality': round(overall_quality, 1),
            'numbers_found': len(numbers),
            'action_verbs_found': action_verb_count
        }
    
    def _extract_advanced_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords with frequency analysis"""
        # Tokenize and clean
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter stop words
        stop_words = {
            'the', 'and', 'for', 'are', 'with', 'this', 'that', 'have', 'from', 'they', 'been',
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall'
        }
        
        filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Count frequencies
        word_freq = Counter(filtered_words)
        
        # Return top keywords
        return [word for word, freq in word_freq.most_common(20)]
    
    def _detect_industry(self, text: str) -> str:
        """Detect industry based on keywords"""
        industry_scores = {}
        
        for industry, keywords in self.industry_skills.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                industry_scores[industry] = score
        
        if industry_scores:
            return max(industry_scores, key=industry_scores.get)
        
        # Fallback industry detection
        if any(word in text for word in ['software', 'developer', 'engineer', 'programming']):
            return 'technology'
        elif any(word in text for word in ['finance', 'banking', 'investment']):
            return 'finance'
        elif any(word in text for word in ['healthcare', 'medical', 'hospital']):
            return 'healthcare'
        else:
            return 'general'
    
    def _calculate_ats_compatibility(self, text: str) -> float:
        """Calculate ATS compatibility score"""
        score = 100.0
        
        # Penalize for problematic elements
        if re.search(r'[^\x00-\x7F]', text):  # Non-ASCII characters
            score -= 10
        
        # Check for standard section headers
        standard_sections = ['experience', 'education', 'skills', 'summary']
        found_sections = sum(1 for section in standard_sections if section in text.lower())
        section_score = (found_sections / len(standard_sections)) * 20
        
        # Length check
        word_count = len(text.split())
        if word_count < 300:
            score -= 15
        elif word_count > 800:
            score -= 5
        
        return max(0, score - (20 - section_score))
    
    def _analyze_job_requirements(self, text: str) -> Dict:
        """Analyze job requirements and preferences"""
        
        # Experience requirements
        required_experience = self._extract_required_experience(text)
        
        # Job level determination
        job_level = self._determine_job_level(text)
        
        # Education requirements
        education_required = self._extract_education_requirements(text)
        
        # Remote work options
        remote_friendly = any(term in text for term in ['remote', 'work from home', 'distributed', 'telecommute'])
        
        return {
            'experience_required': required_experience,
            'job_level': job_level,
            'education_required': education_required,
            'remote_friendly': remote_friendly
        }
    
    def _extract_required_experience(self, text: str) -> int:
        """Extract required years of experience"""
        patterns = [
            r'(\d+)[\+]?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'minimum\s*(\d+)\s*(?:years?|yrs?)',
            r'at least\s*(\d+)\s*(?:years?|yrs?)',
            r'(\d+)[\+]?\s*(?:to|\-)\s*(\d+)\s*(?:years?|yrs?)'
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    years.extend([int(m) for m in match if m.isdigit()])
                elif match.isdigit():
                    years.append(int(match))
        
        return min(years) if years else 0
    
    def _determine_job_level(self, text: str) -> str:
        """Determine job level from description"""
        
        for level, indicators in self.job_level_patterns.items():
            if any(indicator in text for indicator in indicators):
                return level.title()
        
        return 'Mid-level'
    
    def _extract_education_requirements(self, text: str) -> str:
        """Extract education requirements"""
        
        if re.search(r'phd.*required|doctorate.*required', text):
            return 'phd'
        elif re.search(r'master.*required|mba.*required', text):
            return 'masters'
        elif re.search(r'bachelor.*required|degree.*required', text):
            return 'bachelors'
        
        return None
    
    def _analyze_company_info(self, text: str) -> Dict:
        """Analyze company information from job posting"""
        
        # Company size indicators
        size_indicators = {
            'startup': ['startup', 'early stage', 'seed', 'series a'],
            'small': ['small', 'growing', '10-50', '50-100'],
            'medium': ['medium', '100-500', '500-1000'],
            'large': ['large', 'enterprise', '1000+', 'fortune']
        }
        
        company_size = 'unknown'
        for size, indicators in size_indicators.items():
            if any(indicator in text.lower() for indicator in indicators):
                company_size = size
                break
        
        return {
            'company_size': company_size,
            'is_remote_friendly': 'remote' in text.lower()
        }
    
    def _analyze_job_urgency(self, text: str) -> Dict:
        """Analyze job posting urgency and priority"""
        
        urgent_indicators = ['urgent', 'immediate', 'asap', 'immediately', 'right away']
        urgent = any(indicator in text for indicator in urgent_indicators)
        
        competitive_indicators = ['competitive', 'multiple candidates', 'fast-paced', 'dynamic']
        competitive = any(indicator in text for indicator in competitive_indicators)
        
        return {
            'urgent_hire': urgent,
            'competitive_position': competitive
        }
    
    def _calculate_job_complexity(self, text: str) -> float:
        """Calculate job complexity score"""
        
        complexity_factors = [
            len(re.findall(r'\b(?:required|must have|essential)\b', text.lower())),
            len(re.findall(r'\b(?:preferred|nice to have|bonus)\b', text.lower())),
            len(re.findall(r'\b(?:years?|yrs?)\b', text.lower())),
            len(text.split()) / 50  # Length factor
        ]
        
        return min(100, sum(complexity_factors) * 10)
    
    # Additional helper methods
    def _calculate_experience_score(self, resume_exp: int, required_exp: int) -> float:
        """Calculate experience matching score"""
        if required_exp == 0:
            return 100
        
        if resume_exp >= required_exp:
            # Slight bonus for meeting requirements, penalty for being overqualified
            if resume_exp <= required_exp * 1.5:
                return 100
            else:
                return max(70, 100 - (resume_exp - required_exp * 1.5) * 5)
        else:
            # Penalty for not meeting requirements
            gap = required_exp - resume_exp
            return max(0, 100 - gap * 20)
    
    def _calculate_education_score(self, resume_edu: str, required_edu: str) -> float:
        """Calculate education matching score"""
        if not required_edu:
            return 100
        
        education_levels = {'associates': 1, 'bachelors': 2, 'masters': 3, 'phd': 4}
        
        resume_level = education_levels.get(resume_edu, 0)
        required_level = education_levels.get(required_edu, 0)
        
        if resume_level >= required_level:
            return 100
        elif resume_level == required_level - 1:
            return 75
        elif resume_level == required_level - 2:
            return 50
        else:
            return 25
    
    def _calculate_industry_alignment(self, resume_industry: str, job_industry: str) -> float:
        """Calculate industry alignment score"""
        if not job_industry or not resume_industry:
            return 70  # Neutral score
        
        if resume_industry == job_industry:
            return 100
        
        # Related industries get partial credit
        related_industries = {
            'technology': ['fintech', 'ai_ml', 'iot'],
            'healthcare': ['fintech'],  # Some overlap in regulatory compliance
            'finance': ['fintech']
        }
        
        if job_industry in related_industries.get(resume_industry, []):
            return 80
        
        return 50  # Different industries
    
    def _categorize_match_strength(self, score: float) -> str:
        """Categorize match strength based on score"""
        if score >= 85:
            return 'excellent'
        elif score >= 70:
            return 'good'
        elif score >= 50:
            return 'fair'
        else:
            return 'poor'
    
    def _categorize_experience_level(self, years: int) -> str:
        """Categorize experience level"""
        if years >= 8:
            return 'senior'
        elif years >= 3:
            return 'mid-level'
        elif years >= 1:
            return 'junior'
        else:
            return 'entry-level'
    
    def _identify_top_skill_gaps(self, missing_skills: Set[str], job_analysis: Dict) -> List[str]:
        """Identify the most important missing skills"""
        if not missing_skills:
            return []
        
        # Prioritize based on frequency in job posting and skill importance
        skill_importance = {
            # High importance skills
            'python': 10, 'java': 10, 'javascript': 10, 'react': 9, 'aws': 9,
            'sql': 9, 'git': 8, 'docker': 8, 'kubernetes': 8, 'node.js': 8,
            # Medium importance skills
            'angular': 7, 'vue': 7, 'django': 7, 'flask': 7, 'spring': 7,
            # Lower importance but still relevant
            'html': 5, 'css': 5, 'bootstrap': 4
        }
        
        # Sort missing skills by importance
        sorted_skills = sorted(
            missing_skills,
            key=lambda skill: skill_importance.get(skill, 3),
            reverse=True
        )
        
        return sorted_skills[:5]
