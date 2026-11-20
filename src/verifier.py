import json
import re
from datetime import date
from google import genai
from google.genai import types
from .prompts import VERIFICATION_SYSTEM
from .schemas import Claim, Verification


def generate_queries(claim: Claim) -> list[str]:
    text = claim.claim_text.strip()
    year_matches = re.findall(r"\b(?:19|20)\d{2}\b", text)
    year = year_matches[-1] if year_matches else str(date.today().year)
    return [
        f"{text} official source {year}",
        f"{text} latest data source",
    ]


def verify_claim(
    claim: Claim,
    search_results: list[dict],
    api_key: str,
    model: str,
) -> Verification:
    if not api_key:
        raise RuntimeError("Missing Gemini API key")
    if not search_results:
        return Verification(
            verdict="False",
            confidence=0.95,
            what_the_evidence_says="No credible search results were available.",
            corrected_fact=None,
            source_urls=[],
            reasoning="no credible evidence found",
        )
    snippets = "\n\n".join(
        f"TITLE: {r.get('title','')}\nURL: {r.get('url','')}\nSNIPPET: {r.get('content','')}"
        for r in search_results
    )
    prompt = (
        VERIFICATION_SYSTEM.format(today=date.today().isoformat())
        + "\n\nCLAIM:\n"
        + claim.claim_text
        + "\n\nSEARCH RESULTS (URLs are the only permitted citations):\n"
        + snippets
        + "\n\nReturn strict JSON with fields: verdict, confidence, what_the_evidence_says, "
        "corrected_fact, source_urls, reasoning."
    )
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0,
        ),
    )
    data = json.loads(response.text)
    result = Verification.model_validate(data)
    allowed = {r["url"] for r in search_results}
    result.source_urls = [url for url in result.source_urls if url in allowed]
    if result.verdict == "Inaccurate" and not result.corrected_fact:
        raise ValueError("Inaccurate verdict requires corrected_fact")
    if result.verdict == "False" and result.reasoning.strip().lower() == "no credible evidence found":
        result.source_urls = []
    return result
