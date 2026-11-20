import json
import os
from google import genai
from google.genai import types
from .prompts import EXTRACTION_SYSTEM, EXTRACTION_SCHEMA
from .schemas import ClaimList


def _chunk_pages(pages: list[tuple[int, str]], max_chars: int = 18000):
    chunks, current, start = [], "", 1
    for number, text in pages:
        piece = f"\n[PAGE {number}]\n{text[:max_chars]}\n"
        if len(current) + len(piece) > max_chars and current:
            chunks.append((start, current))
            current = piece
            start = number
        else:
            current += piece
    if current:
        chunks.append((start, current))
    return chunks


def extract_claims(pages, api_key: str, model: str, max_claims: int) -> ClaimList:
    if not api_key:
        raise RuntimeError("Missing Gemini API key")
    client = genai.Client(api_key=api_key)
    all_claims = []
    for _, chunk in _chunk_pages(pages):
        prompt = (
            f"{EXTRACTION_SYSTEM}\n\nReturn exactly this JSON shape:\n{EXTRACTION_SCHEMA}\n"
            f"Maximum new claims for this chunk: {max_claims}\n\nDOCUMENT:\n{chunk}"
        )
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0,
            ),
        )
        try:
            data = json.loads(response.text)
            all_claims.extend(ClaimList.model_validate(data).claims)
        except Exception:
            continue
    unique = []
    seen = set()
    for claim in all_claims:
        key = claim.claim_text.lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(claim)
    return ClaimList(claims=unique[:max_claims])
