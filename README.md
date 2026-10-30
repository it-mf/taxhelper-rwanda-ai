# TaxHelper Rwanda

TaxHelper Rwanda is a bilingual (Kinyarwanda and English) educational web application that helps users understand basic tax-related topics in Rwanda.

## Problem and purpose
Tax rules and procedures can be difficult to understand. This project provides simple, accessible explanations of common topics and directs users to the Rwanda Revenue Authority (RRA) for authoritative and up-to-date guidance.

## What the application covers
The current FAQ knowledge base includes explanations and guidance about:
- Taxpayer Identification Number (TIN)
- Value Added Tax (VAT)
- Electronic Billing Machine (EBM)
- PAYE and payroll-related tax
- Business registration and income tax
- Filing deadlines and where to seek further help

## Data and information sources
The current version does **not** connect to a live tax database, an NISR dataset, or a live RRA API. Its offline responses come from a small, curated FAQ knowledge base embedded in `main.py`. The FAQ is intended for basic education, not as a substitute for official tax advice.

For current requirements, rates, deadlines and procedures, users should verify information directly with:
- Rwanda Revenue Authority: https://www.rra.gov.rw/
- RRA taxpayer support: dial 3004 (verify availability and charges with the provider).

No personal taxpayer records are collected by the FAQ feature.

## How users interact with it
1. Open the deployed web application.
2. Select Kinyarwanda or English.
3. Enter a question about one of the supported tax topics.
4. Read the explanation and follow the RRA links or contact RRA when an official decision is needed.

The backend exposes a health endpoint at `/health` and a chat endpoint at `/api/chat`.

## Technology
- Frontend: HTML, CSS and JavaScript (`index.html`)
- Backend: Python and FastAPI (`main.py`)
- Deployment: GitHub Pages (frontend) and Render (backend)

## Run locally
Python 3.10+ is recommended.

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open the frontend locally or use the deployed frontend. Configure `APP_ORIGIN` on the backend if the frontend origin changes.

## Live application
- Frontend: https://it-mf.github.io/taxhelper-rwanda-ai/
- Backend: https://taxhelper-rwanda-ai.onrender.com
- Health check: https://taxhelper-rwanda-ai.onrender.com/health

## Limitations
- Responses are limited to the topics covered by the curated FAQ unless the optional Gemini integration is correctly configured.
- The application does not register businesses, file tax returns, make payments, or provide binding tax advice.
- Users should confirm time-sensitive information with RRA.

## Team and eligibility documents
This project is submitted by a team of two students. Add each member's student card or other accepted proof of eligibility in the `eligibility/` folder before submission. Do not publish documents containing unnecessary sensitive information.

## Demo video
Add a screen-recorded demonstration (maximum 3 minutes, as specified in the NISR hackathon guidance) to the repository, for example at `demo/taxhelper-demo.webm`. The video should show the interface, language selection, and real example questions and answers.

## Repository contents
- `index.html` — web interface
- `main.py` — FastAPI backend and FAQ logic
- `requirements.txt` — Python dependencies
- `render.yaml` — Render deployment configuration
- `README.md` — project documentation
- `demo/` — demo video (to be added)
- `data/` — documentation or files for any additional data actually used (to be added if applicable)
- `eligibility/` — team eligibility documents (to be added privately by the team before final submission)
