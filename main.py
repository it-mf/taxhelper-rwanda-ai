
import os
import re
import unicodedata

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

APP_ORIGIN = os.getenv(
    "ALLOWED_ORIGIN",
    "https://it-mf.github.io"
)
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

RRA_URL = "https://www.rra.gov.rw/"
RRA_PHONE = "3004"

app = FastAPI(
    title="TaxHelper Rwanda API",
    version="1.2.0"
)

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


# General educational guidance.
# Current tax rates and deadlines are deliberately not hard-coded.
FAQ = {
    "registration": {
        "rw": (
            "Kwandikisha ubucuruzi mu Rwanda bikorwa binyuze muri Rwanda "
            "Development Board (RDB). Nyuma yo kwandikisha ubucuruzi, "
            "ugomba kumenya inshingano z'imisoro bireba ibikorwa byawe. "
            "Ibisabwa bishobora guterwa n'ubwoko bw'ubucuruzi. "
            "Reba RDB kuri https://www.rdb.rw/ na RRA kuri "
            f"{RRA_URL} kugira ngo ubone amakuru agezweho."
        ),
        "en": (
            "Business registration in Rwanda is handled through the "
            "Rwanda Development Board (RDB). After registration, check "
            "which tax obligations apply to your business activity. "
            "Requirements may vary depending on the type of business. "
            f"Visit https://www.rdb.rw/ and {RRA_URL} "
            "for current official guidance."
        )
    },

    "tin": {
        "rw": (
            "TIN ni nimero iranga umusoreshwa (Taxpayer Identification "
            "Number). Ku bijyanye no kuyibona cyangwa kuyigenzura, "
            f"koresha serivisi za RRA cyangwa uhamagare {RRA_PHONE}. "
            "Ntugashyire TIN yawe cyangwa indangamuntu yawe muri iyi chat."
        ),
        "en": (
            "TIN means Taxpayer Identification Number. To obtain or "
            f"verify it, use official RRA services or call {RRA_PHONE}. "
            "Do not share your TIN or national ID in this chat."
        )
    },

    "vat": {
        "rw": (
            "VAT ni umusoro ku nyongeragaciro. Ujyanye n'ibicuruzwa "
            "na serivisi bisoreshwa. Ibisabwa kwiyandikisha, uko "
            "ubarwa n'igihe cyo kuwumenyekanisha biterwa n'amategeko "
            "agezweho n'ubwoko bw'ubucuruzi. Reba amakuru ya RRA kuri "
            f"{RRA_URL} cyangwa uhamagare {RRA_PHONE}."
        ),
        "en": (
            "VAT is a tax on the value added to taxable goods and "
            "services. Registration requirements, calculations and "
            "filing obligations depend on current law and the type "
            f"of business. Check {RRA_URL} or call {RRA_PHONE}."
        )
    },

    "ebm": {
        "rw": (
            "EBM ni uburyo bw'ikoranabuhanga bwo gutanga inyemezabuguzi "
            "zemewe ku bikorwa bisoreshwa. Kugira ngo umenye niba "
            "ubucuruzi bwawe bugomba gukoresha EBM n'uko ikoreshwa, "
            f"reba {RRA_URL} cyangwa uhamagare {RRA_PHONE}."
        ),
        "en": (
            "EBM is an electronic system used to issue compliant "
            "invoices for taxable transactions. To confirm whether "
            "your business must use EBM and how it works, visit "
            f"{RRA_URL} or call {RRA_PHONE}."
        )
    },

    "income": {
        "rw": (
            "Umusoro ku nyungu uterwa n'ubwoko bw'ubucuruzi, amafaranga "
            "winjiza n'icyiciro cy'umusoro urimo. Ibipimo bishobora "
            "guhinduka. TaxHelper ntitanga igipimo cyangwa umubare "
            "utagenzuwe. Reba amakuru agezweho kuri "
            f"{RRA_URL} cyangwa uhamagare {RRA_PHONE}."
        ),
        "en": (
            "Income tax depends on the type of business, income and "
            "applicable tax category. Rates may change. TaxHelper "
            "does not provide unverified tax rates or calculations. "
            f"Check {RRA_URL} or call {RRA_PHONE}."
        )
    },

    "payroll": {
        "rw": (
            "PAYE ni umusoro ku mushahara ukurikije amategeko agenga "
            "imisoro ku bakozi. Ibarura riterwa n'amafaranga umukozi "
            "ahembwa n'amabwiriza agezweho. Ku bipimo n'ibisabwa "
            f"by'ubu, reba {RRA_URL} cyangwa uhamagare {RRA_PHONE}."
        ),
        "en": (
            "PAYE is tax withheld from employment income under "
            "applicable payroll tax rules. Its calculation depends "
            "on employee earnings and current regulations. For "
            f"current rates and requirements, visit {RRA_URL} "
            f"or call {RRA_PHONE}."
        )
    },

    "deadlines": {
        "rw": (
            "Amatariki ntarengwa yo kumenyekanisha no kwishyura "
            "imisoro aterwa n'ubwoko bw'umusoro n'icyiciro cy'usora. "
            "Kugira ngo wirinde amakuru ashaje, genzura ingengabihe "
            f"ya RRA kuri {RRA_URL} cyangwa uhamagare {RRA_PHONE}."
        ),
        "en": (
            "Tax filing and payment deadlines depend on the tax "
            "type and taxpayer category. To avoid outdated information, "
            f"check the current RRA guidance at {RRA_URL} "
            f"or call {RRA_PHONE}."
        )
    },

    "help": {
        "rw": (
            f"Ushobora kubaza Rwanda Revenue Authority (RRA) kuri "
            f"{RRA_PHONE}. Ushobora no gusura urubuga rwabo: {RRA_URL}. "
            "Ntugashyire hano ijambo ry'ibanga, PIN, TIN, indangamuntu "
            "cyangwa amakuru ya banki."
        ),
        "en": (
            f"For official tax assistance, contact the Rwanda Revenue "
            f"Authority (RRA) on {RRA_PHONE} or visit {RRA_URL}. "
            "Never share passwords, PINs, TINs, national ID numbers "
            "or bank details in this chat."
        )
    }
}


def normalize_text(text: str) -> str:
    """Normalize text for more reliable keyword matching."""
    text = text.casefold().strip()
    text = unicodedata.normalize("NFKC", text)
    return re.sub(r"\s+", " ", text)


def contains_keyword(text: str, keyword: str) -> bool:
    """
    Match whole words or phrases.
    This prevents short terms such as 'tin' matching inside
    unrelated words.
    """
    pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"
    return re.search(pattern, text) is not None


def offline_answer(question: str, language: str) -> str:
    q = normalize_text(question)

    categories = [
        (
            "registration",
            [
                "kwandikisha",
                "kwandikisha ubucuruzi",
                "registration",
                "register",
                "business registration",
                "business"
            ]
        ),
        (
            "tin",
            [
                "tin",
                "nimero iranga",
                "nimero y'umusoro",
                "taxpayer identification",
                "tax identification number"
            ]
        ),
        (
            "vat",
            [
                "vat",
                "value added tax",
                "nyongeragaciro"
            ]
        ),
        (
            "ebm",
            [
                "ebm",
                "inyemezabuguzi",
                "invoice",
                "invoices",
                "electronic billing"
            ]
        ),
        (
            "payroll",
            [
                "paye",
                "umushahara",
                "imisoro ku mushahara",
                "salary",
                "payroll",
                "employment tax"
            ]
        ),
        (
            "deadlines",
            [
                "deadline",
                "deadlines",
                "itariki",
                "amatariki",
                "igihe cyo kwishyura",
                "igihe cyo kumenyekanisha",
                "when to file",
                "due date",
                "filing date"
            ]
        ),
        (
            "income",
            [
                "income tax",
                "umusoro ku nyungu",
                "umusoro w'inyungu",
                "profit tax",
                "turnover tax"
            ]
        ),
        (
            "help",
            [
                "rra",
                "ubufasha",
                "help",
                "contact",
                "telephone",
                "phone",
                "amakuru"
            ]
        )
    ]

    for category, keywords in categories:
        if any(contains_keyword(q, word) for word in keywords):
            return FAQ[category][language]

    if language == "rw":
        return (
            "Murakoze kubaza TaxHelper Rwanda!\n\n"
            "Ubu ndi gukoresha ububiko bw'ibisubizo by'ibanze. "
            "Mushobora kumbaza kuri:\n"
            "• Kwandikisha ubucuruzi\n"
            "• TIN\n"
            "• VAT\n"
            "• EBM\n"
            "• PAYE\n"
            "• Umusoro ku nyungu\n"
            "• Amatariki yo kumenyekanisha imisoro\n\n"
            "Ku makuru yemewe kandi agezweho, sura "
            f"{RRA_URL} cyangwa uhamagare {RRA_PHONE}."
        )

    return (
        "Thank you for contacting TaxHelper Rwanda!\n\n"
        "I am currently using a basic offline FAQ. You can ask "
        "about:\n"
        "• Business registration\n"
        "• TIN\n"
        "• VAT\n"
        "• EBM\n"
        "• PAYE\n"
        "• Income tax\n"
        "• Tax filing deadlines\n\n"
        "For current official information, visit "
        f"{RRA_URL} or call {RRA_PHONE}."
    )


@app.get("/")
def root():
    return {
        "service": "TaxHelper Rwanda API",
        "status": "running",
        "version": "1.2.0"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    question = payload.question.strip()

    api_key = os.getenv("GEMINI_API_KEY")

    # Free offline mode when no Gemini key is configured.
    if not api_key:
        return ChatResponse(
            answer=offline_answer(question, payload.language)
        )

    try:
        from google import genai
        from google.genai import types

        prompt_language = (
            "Kinyarwanda"
            if payload.language == "rw"
            else "English"
        )

        system_instruction = """
You are TaxHelper Rwanda, an educational assistant
that explains general Rwanda tax information.

Rules:
1. Respond clearly and simply in the requested language.
2. Never invent tax rates, deadlines, legal requirements
   or government policies.
3. If a question requires current official information,
   direct the user to https://www.rra.gov.rw/
   or RRA telephone number 3004.
4. Do not pretend to access live RRA or NISR databases.
5. Do not claim to represent RRA or another government institution.
6. Do not claim to submit tax returns or make tax payments.
7. Never request passwords, PINs, TINs, national ID numbers
   or bank account details.
8. If uncertain, say so clearly instead of guessing.
9. Give educational explanations, not definitive legal advice.
"""

        client = genai.Client(api_key=api_key)

        result = client.models.generate_content(
            model=MODEL,
            contents=(
                f"Respond in {prompt_language}.\n"
                f"User question: {question}"
            ),
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                max_output_tokens=500
            )
        )

        answer = (result.text or "").strip()

        if not answer:
            answer = offline_answer(question, payload.language)

        return ChatResponse(answer=answer)

    except Exception:
        # Keep the service working if the optional AI service fails.
        return ChatResponse(
            answer=offline_answer(question, payload.language)
        )
