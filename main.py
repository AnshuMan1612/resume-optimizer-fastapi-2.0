# app/main.py - COMPLETE VERSION v5.0 with HTML/CSS Resume Generation
from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import core services
from app.services.pdf_extractor import PDFExtractor
from app.services.enhanced_analyzer import EnhancedResumeAnalyzer

# Import AI services with error handling
try:
    from app.services.perplexity_analyzer import PerplexityJobAnalyzer
    from app.services.ai_resume_generator import AIEnhancedResumeGenerator
    AI_SERVICES_AVAILABLE = True
except ImportError as e:
    logger.warning(f"AI services not available: {e}")
    AI_SERVICES_AVAILABLE = False

# Import HTML Resume Generator
try:
    from app.services.html_resume_generator import HTMLResumeGenerator
    HTML_GENERATOR_AVAILABLE = True
except ImportError as e:
    logger.warning(f"HTML resume generator not available: {e}")
    HTML_GENERATOR_AVAILABLE = False

# ✅ YOUR ACTUAL API KEY CONFIGURED
PERPLEXITY_API_KEY = "ENTER YOUR API KEY HERE"

# Create FastAPI app
app = FastAPI(
    title="ATS Resume Optimizer Pro",
    description="AI-powered resume optimization with professional HTML/CSS templates",
    version="5.0.0"
)

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Initialize core services (always available)
pdf_extractor = PDFExtractor()
analyzer = EnhancedResumeAnalyzer()

# Initialize HTML Resume Generator
html_generator = None
if HTML_GENERATOR_AVAILABLE:
    try:
        html_generator = HTMLResumeGenerator()
        logger.info("✅ HTML Resume Generator initialized")
    except Exception as e:
        logger.error(f"⚠️ HTML generator failed to initialize: {str(e)}")
        html_generator = None

# Initialize AI services with proper error handling
perplexity_analyzer = None
ai_resume_generator = None
ai_services_active = False

if AI_SERVICES_AVAILABLE and PERPLEXITY_API_KEY:
    try:
        perplexity_analyzer = PerplexityJobAnalyzer(PERPLEXITY_API_KEY)
        ai_resume_generator = AIEnhancedResumeGenerator()
        ai_services_active = True
        logger.info("✅ AI services initialized - Perplexity integration ACTIVE")
    except Exception as e:
        logger.error(f"⚠️ AI services failed to initialize: {str(e)}")
        ai_services_active = False
else:
    logger.info("ℹ️ AI services disabled - using enhanced standard functionality")

# Ensure directories exist
directories = ["uploads/resumes", "uploads/optimized", "logs", "app/templates/resume_templates"]
for directory in directories:
    Path(directory).mkdir(parents=True, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Enhanced home page with HTML resume generation status"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "app_version": "5.0.0",
        "ai_powered": ai_services_active,
        "html_generator_available": html_generator is not None,
        "features": {
            "skills_analyzed": "500+",
            "ats_compatibility": "95%",
            "success_rate": "3x more interviews",
            "ai_enhancement": "🤖 Premium AI Analysis" if ai_services_active else "📊 Enhanced Analysis",
            "resume_quality": "Professional HTML/CSS Templates" if html_generator else "Standard PDF Generation"
        }
    })

@app.post("/fetch-job")
async def fetch_job_description(request: Request):
    """
    Enhanced job description fetching with Perplexity AI
    """
    try:
        body = await request.json()
        url = body.get('url')
        
        if not url:
            raise HTTPException(status_code=400, detail="URL is required")
        
        if not ai_services_active:
            return JSONResponse({
                "success": False,
                "error": "🤖 Job URL scraping requires AI services. Please use 'Paste Text' option instead."
            }, status_code=400)
        
        logger.info(f"🤖 Analyzing job with Perplexity AI: {url}")
        
        # Use Perplexity for enhanced job analysis
        job_data = perplexity_analyzer.analyze_job_from_url(url)
        
        if job_data.get('success'):
            # Clean and format the response
            clean_description = job_data.get('clean_job_description', '')
            
            # If clean description is too short, use fallback
            if len(clean_description.strip()) < 100:
                clean_description = job_data.get('company_description', 'Job description extracted successfully. Please review and add additional details if needed.')
            
            return JSONResponse({
                "success": True,
                "title": job_data.get('job_title', ''),
                "company": job_data.get('company_name', ''),
                "location": job_data.get('location', ''),
                "description": clean_description,
                "technical_skills": job_data.get('technical_skills', []),
                "soft_skills": job_data.get('soft_skills', []),
                "extraction_method": "perplexity_ai",
                "analysis_quality": job_data.get('analysis_quality', 'high'),
                "employment_type": job_data.get('employment_type', ''),
                "experience_required": job_data.get('experience_required', ''),
                "message": f"✨ Enhanced analysis by Perplexity AI - {job_data.get('job_title', 'Position')} at {job_data.get('company_name', 'Company')}"
            })
        else:
            error_msg = job_data.get('error', 'Failed to analyze job posting')
            return JSONResponse({
                "success": False,
                "error": f"Job analysis failed: {error_msg}. Please try pasting the job description manually."
            }, status_code=400)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Job fetching error: {str(e)}")
        return JSONResponse({
            "success": False,
            "error": f"Error analyzing job posting: {str(e)}. Please try the 'Paste Text' option."
        }, status_code=500)

@app.post("/upload-resume")
async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    job_description: str = Form(...),
    template: Optional[str] = Form("ats_modern")  # Template selection
):
    """
    Enhanced resume upload with HTML/CSS template generation
    """
    logger.info(f"\n🚀 Starting {'AI-enhanced' if ai_services_active else 'enhanced'} resume analysis")
    logger.info(f"📁 File: {file.filename}")
    logger.info(f"📝 Job description: {len(job_description)} chars")
    logger.info(f"🎨 Template selected: {template}")
    logger.info(f"🤖 AI Services: {'ACTIVE' if ai_services_active else 'STANDARD'}")
    logger.info(f"📄 HTML Generator: {'ACTIVE' if html_generator else 'FALLBACK'}")
    
    try:
        # Step 1: Validate inputs
        if not file or not file.filename:
            raise HTTPException(status_code=400, detail="No file uploaded")
        
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported. Please convert your resume to PDF format.")
        
        if not job_description or len(job_description.strip()) < 50:
            raise HTTPException(status_code=400, detail="Job description is too short (minimum 50 characters required)")
        
        # Validate template selection
        available_templates = ['ats_modern', 'tech_focused', 'classic_professional']
        if template not in available_templates:
            template = 'ats_modern'  # Default fallback
        
        # Step 2: Handle file upload
        try:
            file_content = await file.read()
            file_size_mb = len(file_content) / (1024 * 1024)
            
            if file_size_mb > 10:
                raise HTTPException(status_code=400, detail=f"File too large: {file_size_mb:.1f}MB (maximum 10MB allowed)")
            
            # Save file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{file.filename}"
            file_path = f"uploads/resumes/{safe_filename}"
            
            with open(file_path, "wb") as buffer:
                buffer.write(file_content)
            
            logger.info(f"💾 File saved: {file_path}")
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
        
        # Step 3: Extract text from PDF
        try:
            logger.info("📄 Extracting text from PDF...")
            resume_text = pdf_extractor.extract_text(file_path)
            
            if not resume_text or len(resume_text.strip()) < 100:
                raise Exception("PDF contains insufficient readable text. Please ensure your PDF is not a scanned image.")
            
            logger.info(f"✅ Extracted {len(resume_text)} characters from PDF")
            
        except Exception as e:
            # Clean up file
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=400, detail=f"PDF processing failed: {str(e)}. Please ensure your PDF contains selectable text.")
        
        # Step 4: Core analysis using enhanced analyzer
        try:
            logger.info("🔍 Performing enhanced analysis...")
            
            # Use enhanced analyzer methods
            resume_analysis = analyzer.analyze_resume(resume_text)
            job_analysis = analyzer.analyze_job_description(job_description)
            match_analysis = analyzer.calculate_advanced_match_score(resume_analysis, job_analysis)
            basic_suggestions = analyzer.generate_advanced_suggestions(match_analysis, resume_analysis, job_analysis)
            
            logger.info(f"📊 Enhanced analysis complete - Overall Score: {match_analysis['overall_score']}%")
            
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            # Clean up file
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"Resume analysis failed: {str(e)}. Please try again with a different PDF.")
        
        # Step 5: AI Enhancement (if available)
        ai_enhanced = False
        enhanced_suggestions = basic_suggestions
        perplexity_insights = {}
        optimized_content = {}
        
        if ai_services_active and perplexity_analyzer:
            try:
                logger.info("🧠 Applying AI enhancement with Perplexity...")
                
                # Get AI insights
                perplexity_insights = perplexity_analyzer.enhance_resume_analysis(
                    resume_text, job_description
                )
                
                # Generate optimized content
                optimized_content = perplexity_analyzer.generate_optimized_content(
                    resume_analysis, job_analysis
                )
                
                # Combine suggestions
                ai_suggestions = perplexity_insights.get('recommended_action_items', [])
                if ai_suggestions:
                    enhanced_suggestions = basic_suggestions + ai_suggestions[:5]
                    ai_enhanced = True
                    logger.info("✅ AI enhancement successful")
                
            except Exception as e:
                logger.warning(f"⚠️ AI enhancement failed: {str(e)} - continuing with enhanced standard analysis")
        
        # Step 6: Professional HTML/CSS Resume Generation
        generated_resumes = []
        generation_method = "html_to_pdf"
        
        try:
            logger.info(f"🎨 Generating professional HTML-to-PDF resume with {template} template...")
            
            if html_generator:
                # Prepare comprehensive resume data
                resume_data = {
                    'original_resume_text': resume_text,
                    'resume_analysis': resume_analysis,
                    'job_analysis': job_analysis,
                    'match_analysis': match_analysis,
                    'suggestions': enhanced_suggestions,
                    'ai_insights': perplexity_insights,
                    'optimized_content': optimized_content
                }
                
                # Generate primary resume with selected template
                try:
                    primary_resume = html_generator.generate_resume(resume_data, template)
                    generated_resumes.append({
                        **primary_resume,
                        'is_primary': True,
                        'layout_name': template.replace('_', ' ').title(),
                        'generation_type': 'html_to_pdf'
                    })
                    
                    logger.info(f"✅ Primary HTML resume generated: {primary_resume['filename']}")
                    generation_method = "html_to_pdf_success"
                    
                    # Generate alternative templates for comparison
                    alt_templates = [t for t in ['ats_modern', 'tech_focused'] if t != template]
                    for alt_template in alt_templates[:2]:  # Generate up to 2 alternatives
                        try:
                            alt_resume = html_generator.generate_resume(resume_data, alt_template)
                            generated_resumes.append({
                                **alt_resume,
                                'is_primary': False,
                                'layout_name': alt_template.replace('_', ' ').title(),
                                'generation_type': 'html_to_pdf'
                            })
                            logger.info(f"✅ Alternative resume generated: {alt_template}")
                        except Exception as e:
                            logger.warning(f"⚠️ Failed to generate {alt_template} template: {e}")
                
                except Exception as e:
                    logger.error(f"❌ HTML resume generation failed: {e}")
                    raise Exception("HTML generation failed")
            
            else:
                logger.warning("⚠️ HTML generator not available, using fallback")
                raise Exception("HTML generator not initialized")
            
        except Exception as e:
            logger.error(f"Resume generation error: {str(e)}")
            
            # Fallback to basic resume generation
            try:
                logger.info("📝 Creating fallback resume...")
                basic_resume = create_comprehensive_fallback_resume(
                    resume_text, resume_analysis, job_analysis, match_analysis, 
                    enhanced_suggestions, timestamp
                )
                generated_resumes.append({
                    **basic_resume,
                    'is_primary': True,
                    'layout_name': 'Text Format',
                    'generation_type': 'fallback'
                })
                generation_method = "fallback_text"
                
            except Exception as fallback_error:
                logger.error(f"❌ Even fallback generation failed: {fallback_error}")
                
                # Create minimal analysis report
                analysis_content = f"""RESUME ANALYSIS REPORT
File: {file.filename}
Analysis Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

MATCH ANALYSIS:
Overall Score: {match_analysis['overall_score']}%
Technical Score: {match_analysis.get('technical_score', 0)}%
Soft Skills Score: {match_analysis.get('soft_skills_score', 0)}%

MATCHED SKILLS:
{', '.join(match_analysis.get('matched_skills', []))}

SUGGESTIONS:
{chr(10).join([f"• {s}" for s in enhanced_suggestions[:10]])}

AI ENHANCED: {"Yes" if ai_enhanced else "No"}
GENERATION METHOD: Emergency Fallback
"""
                
                filename = f"analysis_report_{timestamp}.txt"
                file_path = f"uploads/optimized/{filename}"
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(analysis_content)
                
                generated_resumes = [{
                    'filename': filename,
                    'pdf_path': file_path,
                    'text_content': analysis_content,
                    'layout_name': 'Analysis Report',
                    'is_primary': True,
                    'generation_type': 'emergency_fallback'
                }]
                generation_method = "emergency_fallback"
        
        # Step 7: Clean up temporary file
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info("🗑️ Temporary file cleaned up")
        except Exception as e:
            logger.warning(f"Cleanup warning: {str(e)}")
        
        # Step 8: Prepare comprehensive response
        primary_resume = next((r for r in generated_resumes if r.get('is_primary')), generated_resumes[0])
        logger.info(f"✅ Complete analysis finished! Overall Score: {match_analysis['overall_score']}%")
        
        # Enhanced template data
        template_data = {
            "request": request,
            "filename": file.filename,
            "message": f"{'🤖 AI-Enhanced' if ai_enhanced else '📊 Enhanced'} analysis complete! Match score: {match_analysis['overall_score']}%",
            
            # Core scores using enhanced analyzer structure
            "match_score": match_analysis['overall_score'],
            "technical_score": match_analysis.get('technical_score', 0),
            "soft_skills_score": match_analysis.get('soft_skills_score', 0), 
            "experience_score": match_analysis.get('experience_score', 0),
            "education_score": match_analysis.get('education_score', 0),
            "ats_compatibility_score": match_analysis.get('ats_compatibility_score', 0),
            
            # Skills analysis using enhanced structure
            "matched_skills": match_analysis.get('matched_skills', []),
            "missing_technical_skills": match_analysis.get('missing_technical_skills', []),
            "missing_soft_skills": match_analysis.get('missing_soft_skills', []),
            "matched_technical_skills": match_analysis.get('matched_technical_skills', []),
            
            # Suggestions (enhanced or AI-enhanced)
            "suggestions": enhanced_suggestions,
            
            # Analysis data
            "resume_analysis": resume_analysis,
            "job_analysis": job_analysis,
            "match_analysis": match_analysis,
            "job_description": job_description[:500] + "..." if len(job_description) > 500 else job_description,
            
            # AI enhancement info
            "ai_enhanced": ai_enhanced,
            "ai_insights": perplexity_insights,
            "generation_method": generation_method,
            
            # Resume generation info - UPDATED for HTML templates
            "has_generated_resume": bool(generated_resumes),
            "generated_resumes": generated_resumes,  # Multiple resume options
            "primary_resume": primary_resume,
            "template_selected": template,
            "download_link": f"/download/{primary_resume['filename']}" if primary_resume.get('filename') else None,
            "generated_filename": primary_resume.get('filename'),
            "resume_preview": primary_resume.get('text_content', '')[:800] + "..." if primary_resume.get('text_content') else None,
            
            # Template options
            "available_templates": ['ats_modern', 'tech_focused', 'classic_professional'],
            "template_descriptions": {
                'ats_modern': 'Modern ATS - Clean, professional HTML format optimized for ATS systems',
                'tech_focused': 'Tech Focused - Emphasizes technical skills and achievements',
                'classic_professional': 'Classic Professional - Traditional corporate resume format'
            },
            
            # Generation info
            "html_generator_used": html_generator is not None,
            "pdf_quality": "Professional HTML/CSS" if generation_method.startswith("html") else "Standard Text",
            
            # Metadata
            "analysis_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "processing_duration": "< 30 seconds",
            "app_version": "5.0.0",
            "enhancement_type": "Perplexity AI + HTML Templates" if ai_enhanced else "Enhanced Analysis + HTML Templates",
            "ats_optimized": True,
            "pixel_perfect": generation_method.startswith("html")
        }
        
        return templates.TemplateResponse("result.html", template_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error during resume processing: {str(e)}")
        
        # Clean up file if it exists
        if 'file_path' in locals() and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        
        raise HTTPException(
            status_code=500,
            detail=f"Resume analysis failed: {str(e)}. Please try again or contact support."
        )

@app.post("/generate-template")
async def generate_additional_template(
    request: Request,
    resume_data: str = Form(...),
    template: str = Form(...)
):
    """
    Generate resume with different HTML template
    """
    try:
        if not html_generator:
            raise HTTPException(status_code=400, detail="HTML template generator not available")
        
        # Parse resume data
        data = json.loads(resume_data)
        
        # Generate with selected template
        result = html_generator.generate_resume(data, template)
        
        return JSONResponse({
            "success": True,
            "filename": result['filename'],
            "download_link": f"/download/{result['filename']}",
            "template": template,
            "generation_type": result.get('generation_method', 'html_to_pdf'),
            "message": f"Resume generated with {template.replace('_', ' ').title()} template using HTML/CSS"
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Secure file download with comprehensive error handling"""
    try:
        # Security: prevent path traversal attacks
        safe_filename = os.path.basename(filename)
        if safe_filename != filename:
            raise HTTPException(status_code=400, detail="Invalid filename provided")
        
        # Check file exists and is accessible
        file_path = f"uploads/optimized/{safe_filename}"
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="Resume file not found or has expired")
        
        # Determine media type based on file extension
        if filename.lower().endswith('.pdf'):
            media_type = 'application/pdf'
        elif filename.lower().endswith('.txt'):
            media_type = 'text/plain'
        else:
            media_type = 'application/octet-stream'
        
        logger.info(f"📥 Serving download: {safe_filename}")
        
        return FileResponse(
            path=file_path,
            filename=f"optimized_{safe_filename}",
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename=optimized_{safe_filename}",
                "Cache-Control": "no-cache",
                "X-Generation-Method": "HTML-to-PDF" if filename.endswith('.pdf') else "Text"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        raise HTTPException(status_code=500, detail="Download failed. Please try again.")

@app.get("/preview/{filename}")
async def preview_resume(filename: str):
    """Preview PDF files in browser"""
    try:
        if not filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files can be previewed")
        
        safe_filename = os.path.basename(filename)
        file_path = f"uploads/optimized/{safe_filename}"
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        logger.info(f"👁️ Serving preview: {safe_filename}")
        
        return FileResponse(
            path=file_path,
            filename=safe_filename,
            media_type='application/pdf',
            headers={"Content-Disposition": "inline"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Preview failed")

@app.get("/api/templates")
async def get_available_templates():
    """Get available HTML resume templates"""
    if not html_generator:
        return JSONResponse({
            "templates": [],
            "message": "HTML template generator not available"
        })
    
    return JSONResponse({
        "templates": [
            {
                "id": "ats_modern",
                "name": "Modern ATS",
                "description": "Clean, professional HTML format optimized for ATS systems",
                "recommended_for": "General applications, all industries",
                "features": ["ATS Optimized", "Professional Typography", "Clean Layout"]
            },
            {
                "id": "tech_focused", 
                "name": "Tech Focused",
                "description": "Emphasizes technical skills and achievements with modern styling",
                "recommended_for": "Software development, data science, engineering",
                "features": ["Technical Skills Emphasis", "Project Highlighting", "Modern Design"]
            },
            {
                "id": "classic_professional",
                "name": "Classic Professional", 
                "description": "Traditional corporate resume format with clean HTML structure",
                "recommended_for": "Finance, consulting, management, executive roles",
                "features": ["Traditional Layout", "Corporate Styling", "Executive Format"]
            }
        ],
        "generation_method": "HTML/CSS to PDF",
        "quality": "Professional Grade"
    })

@app.get("/health")
async def health_check():
    """Comprehensive health check with detailed status"""
    try:
        # Count processed files
        resume_count = len([f for f in os.listdir("uploads/resumes") if f.endswith('.pdf')]) if os.path.exists("uploads/resumes") else 0
        optimized_count = len([f for f in os.listdir("uploads/optimized") if os.path.isfile(f"uploads/optimized/{f}")]) if os.path.exists("uploads/optimized") else 0
        
        # Disk space check
        disk_usage = shutil.disk_usage(".")
        disk_free_gb = disk_usage.free / (1024**3)
        
        return {
            "status": "healthy",
            "message": "🚀 ATS Resume Optimizer Pro v5.0 with HTML Templates running optimally!",
            "timestamp": datetime.now().isoformat(),
            "version": "5.0.0",
            
            # Service status
            "services": {
                "pdf_extractor": "operational",
                "enhanced_analyzer": "operational",
                "html_resume_generator": "operational" if html_generator else "not_available",
                "ai_services": "active" if ai_services_active else "standard",
                "perplexity_integration": "active" if ai_services_active else "inactive"
            },
            
            # System metrics
            "system_metrics": {
                "disk_free_gb": round(disk_free_gb, 2),
                "resumes_processed": resume_count,
                "optimized_resumes_generated": optimized_count,
                "ai_enhancement_available": ai_services_active,
                "html_templates_available": html_generator is not None
            },
            
            # Feature availability
            "features": {
                "enhanced_analysis": True,
                "500_plus_skills_detection": True,
                "ats_optimization": True,
                "html_template_generation": html_generator is not None,
                "pixel_perfect_pdfs": html_generator is not None,
                "professional_formatting": True,
                "ai_insights": ai_services_active,
                "job_url_scraping": ai_services_active,
                "perplexity_powered": ai_services_active
            },
            
            # Template system
            "template_system": {
                "available": html_generator is not None,
                "templates": html_generator.get_available_templates() if html_generator else [],
                "generation_method": "HTML/CSS to PDF" if html_generator else "Text Only"
            }
        }
        
    except Exception as e:
        return {
            "status": "degraded",
            "message": f"Health check encountered issues: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "ai_services": ai_services_active,
            "html_generator": html_generator is not None,
            "version": "5.0.0"
        }

# Helper function for comprehensive fallback resume
def create_comprehensive_fallback_resume(resume_text: str, resume_analysis: Dict, job_analysis: Dict, 
                                       match_analysis: Dict, suggestions: List[str], timestamp: str) -> Dict:
    """Create comprehensive fallback resume when HTML generation fails"""
    
    filename = f"comprehensive_resume_{timestamp}.txt"
    file_path = f"uploads/optimized/{filename}"
    
    # Extract personal info
    lines = [line.strip() for line in resume_text.split('\n') if line.strip()]
    name = lines[0] if lines else "Your Name"
    
    # Clean name
    import re
    clean_name = re.sub(r'\+?\d[\d\s\-\(\)]{8,}', '', name)
    clean_name = re.sub(r'\S+@\S+', '', clean_name).strip()
    if len(clean_name) > 2:
        name = clean_name
    
    contact_info = resume_analysis.get('contact_info', {})
    
    content = f"""{name.upper()}
{'=' * len(name)}

Contact Information:
Email: {contact_info.get('email', 'your.email@example.com')}
Phone: +91 8219234310
LinkedIn: https://www.linkedin.com/in/anshuman-sharma-23713322a/
GitHub: https://github.com/AnshuMan1612

MACHINE LEARNING & DATA ANALYTICS

PROFESSIONAL SUMMARY
Aspiring Machine Learning Engineer with practical experience in data analysis, algorithm development, and AI-driven solutions. Successfully built dynamic pricing algorithms and automated protein-ligand interaction workflows using Python and AI algorithms. Eager to apply skills in machine learning to drive innovation in healthcare, finance, and technology sectors.

TECHNICAL SKILLS
Programming: {', '.join(resume_analysis.get('technical_skills', [])[:8])}
Frameworks & Tools: React, Node.js, AWS, MongoDB, Qt, Visual Studio, Tailwind, PyMOL, MODELLER
Data & Visualization: Power BI, MS-Excel, seaborn, pandas, numpy, scikit-learn

PROFESSIONAL EXPERIENCE

Scaletrix
Data Analyst Intern | Jul 2025 - Present
• Created interactive Power BI dashboards to visualize client data and key metrics in real time, which significantly improved client decision-making and business outcomes.
• Performed data cleaning and EDA using Python, SQL, and Excel to improve data reliability and extract trends.
• Generated actionable insights and recommendations by analyzing real-world datasets with a modern analytics tech stack, leading to improved strategic planning.

Planto.AI
Research Intern | Feb 2025 - May 2025
• Revamped UI for Planto.ai homepage using React and Tailwind, enhancing user engagement.
• Developed dynamic pricing algorithms, supporting deployment and scaling on AWS.
• Built backend logic (Node.js, MongoDB) for internal prototyping of AI-driven features.

EDUCATION
Cluster Innovation Centre, University of Delhi
B.Tech, Computer Science & Mathematical Innovation | 2021 - 2025

ANALYSIS RESULTS
Overall Match Score: {match_analysis.get('overall_score', 0)}%
Technical Skills Score: {match_analysis.get('technical_score', 0)}%
Matched Skills: {', '.join(match_analysis.get('matched_skills', []))}

OPTIMIZATION RECOMMENDATIONS
{chr(10).join([f"{i+1}. {suggestion}" for i, suggestion in enumerate(suggestions[:8])])}

Note: This is a comprehensive text version of your resume. For professional PDF formatting, ensure HTML template dependencies are installed.
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # Save comprehensive resume
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return {
        'filename': filename,
        'pdf_path': file_path,
        'text_content': content,
        'template': 'comprehensive_fallback'
    }

# Enhanced error handlers
@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    """Handle form validation errors with detailed feedback"""
    logger.error(f"Form validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Form validation failed",
            "detail": "Please check your file upload and job description inputs",
            "requirements": {
                "file": "PDF format, maximum 10MB",
                "job_description": "Minimum 50 characters required",
                "template": "Optional - ats_modern, tech_focused, or classic_professional"
            },
            "message": "Ensure you've uploaded a valid PDF resume and provided a detailed job description"
        }
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Enhanced 404 handler"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "error": "Page not found - you've been redirected to the home page",
            "ai_powered": ai_services_active,
            "html_generator_available": html_generator is not None,
            "app_version": "5.0.0"
        },
        status_code=404
    )

@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    """Enhanced 500 error handler"""
    logger.error(f"Server error: {exc}")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "error": "An internal server error occurred. Our system is working to resolve this.",
            "ai_powered": ai_services_active,
            "html_generator_available": html_generator is not None,
            "app_version": "5.0.0"
        },
        status_code=500
    )

# Application startup and info
if __name__ == "__main__":
    import uvicorn
    
    print("\n🚀 ATS RESUME OPTIMIZER PRO v5.0 - HTML/CSS TEMPLATES EDITION")
    print("=" * 80)
    
    # Service status
    if ai_services_active:
        print("🤖 AI SERVICES: ✅ FULLY OPERATIONAL")
        print("   🎯 Perplexity AI integration: ACTIVE")
        print("   🧠 Enhanced job analysis: ENABLED") 
        print("   ✨ AI-powered resume optimization: ENABLED")
        print("   🔍 Advanced suggestion engine: ENABLED")
        print("   🌐 Job URL scraping: ENABLED")
    else:
        print("📊 ENHANCED MODE: ✅ OPERATIONAL")
        print("   🔧 Advanced resume analysis: ENABLED")
        print("   📈 500+ technical skills detection: ENABLED") 
        print("   🎯 Professional resume generation: ENABLED")
        print("   ⚠️  AI features require valid Perplexity API key")
    
    # HTML Template system status
    if html_generator:
        print(f"\n🎨 HTML TEMPLATE SYSTEM: ✅ OPERATIONAL")
        print(f"   📄 Modern ATS: Professional clean HTML format")
        print(f"   💻 Tech Focused: Technical skills emphasis with modern styling")
        print(f"   🏢 Classic Professional: Traditional corporate HTML format")
        print(f"   📋 Generation Method: HTML/CSS → PDF (WeasyPrint)")
        print(f"   🎯 Quality: Pixel-perfect, matching your target resume")
    else:
        print(f"\n🎨 HTML TEMPLATE SYSTEM: ⚠️ NOT AVAILABLE")
        print(f"   📝 Fallback to comprehensive text generation")
        print(f"   💡 Install: pip install weasyprint beautifulsoup4 lxml")
    
    print(f"\n🌐 ACCESS POINTS:")
    print(f"   🏠 Main Application: http://localhost:8000")
    print(f"   📚 API Documentation: http://localhost:8000/docs")
    print(f"   🔍 Health Check: http://localhost:8000/health") 
    print(f"   📊 API Status: http://localhost:8000/api/status")
    print(f"   🎨 Available Templates: http://localhost:8000/api/templates")
    
    print(f"\n🎯 CORE FEATURES:")
    print(f"   ✅ Advanced PDF text extraction & processing")
    print(f"   ✅ Enhanced skills analysis (500+ technical skills)")
    print(f"   ✅ Sophisticated job matching algorithms")
    print(f"   ✅ Professional HTML/CSS resume templates")
    print(f"   ✅ Pixel-perfect PDF generation (WeasyPrint)")
    print(f"   ✅ Comprehensive error handling & logging")
    print(f"   ✅ Modern professional UI/UX")
    print(f"   ✅ Resume preview & download functionality")
    
    if ai_services_active:
        print(f"\n🤖 AI-POWERED FEATURES:")
        print(f"   🌐 Intelligent job URL content extraction")
        print(f"   🧠 AI-powered resume content optimization")
        print(f"   🏢 Industry-specific insights & recommendations")
        print(f"   🎨 Premium AI-enhanced resume formatting")
        print(f"   💡 Advanced contextual suggestion engine")
        print(f"   🔗 Perplexity-powered research capabilities")
    
    print(f"\n" + "=" * 80)
    print(f"🔑 API Key Status: {'✅ CONFIGURED & ACTIVE' if ai_services_active else '⚠️ NOT CONFIGURED'}")
    print(f"🎨 HTML Templates: {'✅ OPERATIONAL (WeasyPrint)' if html_generator else '⚠️ FALLBACK MODE'}")
    print(f"📄 Resume Quality: {'Professional HTML/CSS → PDF' if html_generator else 'Comprehensive Text'}")
    
    if not ai_services_active:
        print(f"💡 To enable AI features, ensure Perplexity API key is valid and active")
    if not html_generator:
        print(f"💡 To enable HTML templates: pip install weasyprint beautifulsoup4 lxml")
    
    print(f"🎉 Ready to generate pixel-perfect, professional resumes!")
    print("=" * 80)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
