🚀 ATS Resume Optimizer Pro
ATS Resume Optimizer Pro is an advanced, AI-powered web app built with Python (FastAPI) for creating, analyzing, and optimizing resumes specifically for Applicant Tracking Systems (ATS) and modern recruiting. It features deep job matching, smart keyword detection, multiple export formats, and customizable professional templates.

✨ Features
🤖 AI-Powered Resume & Job Analysis

Deep skill detection, industry insights, and Perplexity AI integration for job matching & ATS feedback.

Instant keyword, experience, and education analysis for maximum job compatibility.

📄 Smart Resume Generation

Create modern, classic, or tech-focused resumes.

Instant HTML/PDF/Text export with customizable layouts.

Bullet point optimization & quantified achievements.

🕵️ Smart Parsing & Extraction

Handles PDF or pasted resume/job posts, extracting all skills, qualifications, and experience.

🎨 Customizable Templates

Choose from “ATS Modern,” “Tech Focused,” or “Classic Professional” layouts.

🔗 Integrations

Perplexity AI job scraping & resume enhancement (optional, API key needed).

Modular code: every feature is independently upgradeable.

🛡️ Secure & Robust

Async uploads, PDF/text safety, and developer-friendly error handling.

🛠️ Installation
bash
git clone https://github.com/your-username/ats-resume-optimizer.git
cd ats-resume-optimizer
pip install -r requirements.txt
If using Perplexity AI features, add your API key to the environment or config file.

🚦 Usage
Run the server:

bash
uvicorn main:app --reload
Open the app:
Go to http://localhost:8000 in your browser.

Upload your resume & job description:
Analyze your resume against any job post for keyword and skill matching.

Optimize and export:
Download your new ATS-optimized resume as PDF, HTML, or TXT.

📁 Project Structure
text
main.py                 # FastAPI backend & routers
resume_generator.py     # Professional PDF generator
html_resume_generator.py# Modern HTML/CSS resume builder
ats_resume_layouts.py   # All resume templates
pdf_extractor.py        # PDF text extraction
job_scraper.py          # Job description fetching
enhanced_analyzer.py    # Advanced AI matching algorithms
simple_analyzer.py      # Simplified analysis (legacy support)
perplexity_analyzer.py  # Perplexity AI API features
ai_resume_generator.py  # Optional: AI resume writing
requirements.txt        # Dependencies
⚠️ Requirements
Python 3.8+

See requirements.txt for all must-have libraries.
