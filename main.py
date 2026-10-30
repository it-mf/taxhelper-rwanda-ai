import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

APP_ORIGIN = os.getenv("ALLOWED_ORIGIN", "https://it-mf.github.io")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

app = FastAPI(title="TaxHelper Rwanda API", version="1.1.0")

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


# This no-key fallback intentionally gives general guidance only.
# It avoids hard-coding tax rates or deadlines that may change.
FAQ = {
    "registration": {
        "rw": "Kwandikisha ubucuruzi bikorwa binyuze muri Rwanda Development Board (RDB). Nyuma yo kwandikisha ubucuruzi, amakuru ajyanye na TIN n'inshingano z'imisoro aboneka binyuze muri RDB na Rwanda Revenue Authority (RRA). Ibisabwa bishobora guterwa n'ubwoko bw'ubucuruzi. Reba https://www.rdb.rw/ cyangwa https://www.rra.gov.rw/ kugira ngo ubone amakuru agezweho.",
        "en": "Business registration is handled through the Rwanda Development Board (RDB). After registration, check with RDB and the Rwanda Revenue Authority (RRA) about your TIN and applicable tax obligations. Requirements depend on the type of activity. See https://www.rdb.rw/ and https://www.rra.gov.rw/ for current guidance."
    },
    "tin": {
        "rw": "TIN ni nimero iranga usora. Ku bijyanye no kuyibona cyangwa kuyimenya, koresha serivisi zemewe za RRA cyangwa ubaze RRA kuri 3004. Ntugashyire TIN yawe cyangwa indangamuntu yawe hano muri chat.",
        "en": "A TIN is a taxpayer identification number. To obtain or verify it, use RRA's official services or contact RRA on 3004. Do not share your TIN or national ID in this chat."
    },
    "vat": {
        "rw": "VAT ni umusoro ku nyongeragaciro. Ibisabwa kwiyandikisha, ibicuruzwa cyangwa serivisi bisoreshwa, n'igihe cyo kumenyekanisha biterwa n'amategeko agezweho n'ubwoko bw'ubucuruzi. Reba ibisobanuro bya RRA kuri https://www.rra.gov.rw/ mbere yo gufata icyemezo.",
        "en": "VAT is a tax on the value added to taxable goods and services. Registration requirements, taxable supplies and filing dates depend on current law and the business situation. Check the latest RRA guidance at https://www.rra.gov.rw/ before acting."
    },
    "ebm": {
        "rw": "EBM ni uburyo bwemewe bwo gutanga inyemezabuguzi z'ibicuruzwa cyangwa serivisi bisoreshwa. Niba utazi niba ubucuruzi bwawe bugomba gukoresha EBM cyangwa uko wayikoresha, saba ubufasha bwa RRA kuri 3004 cyangwa urebe https://www.rra.gov.rw/.",
        "en": "EBM is the electronic invoicing system used for issuing compliant invoices for taxable transactions. To confirm whether your business must use it or how to use it, contact RRA on 3004 or visit https://www.rra.gov.rw/."
    },
    "income": {
        "rw": "Umusoro ku nyungu uterwa n'ubwoko bw'umusoro, amafaranga winjiza, n'uburyo ubucuruzi bwawe busoreshwamo. Ibipimo n'amatariki bishobora guhinduka, bityo TaxHelper ntitanga igipimo cyangwa umubare utagenzuwe. Reba amakuru agezweho kuri https://www.rra.gov.rw/ cyangwa ubaze RRA kuri 3004.",
        "en": "Income tax depends on the tax category, income and applicable tax regime. Rates and deadlines can change, so TaxHelper will not guess an unverified rate or amount. Check current guidance at https://www.rra.gov.rw/ or contact RRA on 3004."
    },
    "payroll": {
        "rw": "PAYE ni umusoro ukatwa ku mushahara hakurikijwe amategeko agenga imishahara. Ibarura riterwa n'amafaranga y'umukozi n'amabwiriza agezweho. Kugira ngo umenye igipimo n'igihe cyo kumenyekanisha by'ubu, reba https://www.rra.gov.rw/ cyangwa ubaze RRA kuri 3004.",
        "en": "PAYE is tax withheld from employment income under the applicable payroll tax rules. The calculation depends on the employee's pay and current rules. Check current rates and filing dates at https://www.rra.gov.rw/ or contact RRA on 3004."
    },
    "deadlines": {
        "rw": "Amatariki ntarengwa yo kumenyekanisha no kwishyura imisoro aterwa n'ubwoko bw'umusoro n'icyiciro cy'usora. Kugira ngo wirinde amakuru ashaje, genzura ingengabihe iri kuri https://www.rra.gov.rw/ cyangwa ubaze RRA kuri 3004.",
        "en": "Tax filing and payment deadlines depend on the tax type and taxpayer category. To avoid relying on outdated dates, check the current calendar at https://www.rra.gov.rw/ or contact RRA on 3004."
    },
    "help": {
        "rw": "Ushobora kubaza RRA ibibazo bijyanye n'imisoro kuri telefone itishyurwa 3004. Nanone reba urubuga rwabo: https://www.rra.gov.rw/. Ntugashyire hano ijambo ry'ibanga, PIN, TIN, nimero y'indangamuntu cyangwa amakuru ya banki.",
        "en": "For tax questions, contact the Rwanda Revenue Authority on toll-free number 3004 or visit https://www.rra.gov.rw/. Never share passwords, PINs, TINs, national ID numbers or bank details here."
    }
}


def offline_answer(question: str, language: str) -> str:
    q = question.casefold()

    categories = [
        ("registration", ["kwandikisha", "registration", "register", "business"]),
        ("tin", ["tin", "nimero iranga", "taxpayer identification"]),
        ("vat", ["vat", "value added", "nyongeragaciro"]),
        ("ebm", ["ebm", "inyemezabuguzi", "invoice", "invoices"]),
        ("payroll", ["paye", "umushahara", "salary", "payroll"]),
        ("deadlines", ["igihe", "itariki", "deadline", "when to file", "due date"]),
        ("income", ["income tax", "umusoro ku nyungu", "inyungu", "profit", "turnover"]),
        ("help", ["rra", "ubufasha", "help", "contact", "telephone", "phone"]),
    ]

    for category, keywords in categories:
        if any(word in q for word in keywords):
            return FAQ[category][language]

    if language == "rw":
        return (
            "Murakoze kubaza TaxHelper Rwanda. Ubu ndimo gukoresha ububiko bw'ibisubizo by'ibanze, "
            "bityo sinshobora gusuzuma ikibazo cyose nk'uko AI ibikora. Mushobora kubaza ku kwandikisha "
            "ubucuruzi, TIN, VAT, EBM, PAYE cyangwa igihe cyo kumenyekanisha imisoro. "
            "Ku bisobanuro byemewe kandi bigezweho, reba https://www.rra.gov.rw/ cyangwa uhamagare 3004."
        )
    return (
        "Thank you for contacting TaxHelper Rwanda. The assistant is currently using its basic "
        "offline FAQ, so it cannot analyse every question like the AI service. You can ask about "
        "business registration, TIN, VAT, EBM, PAYE or filing deadlines. For authoritative and "
        "up-to-date information, visit https://www.rra.gov.rw/ or call 3004."
    )


@app.get("/")
def root():
    return {"service": "TaxHelper Rwanda API", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return ChatResponse(answer=offline_answer(payload.question.strip(), payload.language))

    # Optional AI mode: imported only when a key is configured.
    try:
        from google import genai
        from google.genai import types

        prompt_language = "Kinyarwanda" if payload.language == "rw" else "English"
        system_instruction = (
            "You are TaxHelper Rwanda, an educational assistant. Explain general Rwanda tax "
            "concepts clearly. Do not invent current rates, deadlines or legal requirements. "
            "Refer users to https://www.rra.gov.rw/ or RRA 3004 for current official guidance. "
            "Do not request passwords, PINs, TINs, national ID numbers or bank details. "
            "Do not claim to represent RRA or to submit or pay taxes."
        )
        client = genai.Client(api_key=api_key)
        result = client.models.generate_content(
            model=MODEL,
            contents=f"Respond in {prompt_language}.\nUser question: {payload.question.strip()}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                max_output_tokens=500,
            ),
        )
        answer = (result.text or "").strip()
        if not answer:
            return ChatResponse(answer=offline_answer(payload.question.strip(), payload.language))
        return ChatResponse(answer=answer)
    except Exception:
        # Keep the public service useful if the optional AI provider is unavailable.
        return ChatResponse(answer=offline_answer(payload.question.strip(), payload.language))
