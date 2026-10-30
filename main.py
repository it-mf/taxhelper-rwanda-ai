import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

APP_ORIGIN = os.getenv("ALLOWED_ORIGIN", "https://it-mf.github.io")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

app = FastAPI(title="TaxHelper Rwanda AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[APP_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
    language: str = Field(default="rw", pattern="^(rw|en)$")

class ChatResponse(BaseModel):
    answer: str

SYSTEM_INSTRUCTION = """
You are TaxHelper Rwanda, an educational assistant that explains general tax
concepts relevant to Rwanda in clear Kinyarwanda or English.

Rules:
- Reply in the language requested by the user.
- Give general educational information, not binding tax, legal, or accounting advice.
- Never invent current tax rates, deadlines, thresholds, forms, or legal requirements.
- If a detail may have changed or depends on the taxpayer's situation, say so and direct
  the user to the Rwanda Revenue Authority (RRA) at https://www.rra.gov.rw/ or an
  appropriately qualified tax professional.
- Do not claim to represent RRA or to submit/pay taxes for the user.
- Ask a brief clarifying question when necessary.
- Do not request passwords, PINs, tax account credentials, national ID numbers,
  bank details, or other sensitive personal information.
- Keep answers practical, respectful, and concise.
"""

@app.get("/")
def root():
    return {"service": "TaxHelper Rwanda AI API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="AI service is not configured yet. Please try again later."
        )

    prompt_language = "Kinyarwanda" if payload.language == "rw" else "English"
    prompt = (
        f"Respond in {prompt_language}.\n"
        f"User question: {payload.question.strip()}"
    )

    try:
        client = genai.Client(api_key=api_key)
        result = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.2,
                max_output_tokens=500,
            ),
        )
        answer = (result.text or "").strip()
        if not answer:
            raise HTTPException(status_code=502, detail="The AI returned an empty response.")
        return ChatResponse(answer=answer)
    except HTTPException:
        raise
    except Exception:
        # Do not expose provider errors, keys, or internal details to website visitors.
        raise HTTPException(
            status_code=502,
            detail="The AI service could not answer right now. Please try again later."
        )
