from pydantic import BaseModel, Field
from typing import List, Literal


Verdict = Literal["Verified", "Inaccurate", "False", "Error - retry"]


class Claim(BaseModel):
    claim_text: str
    category: str
    page_number: int
    exact_snippet: str


class ClaimList(BaseModel):
    claims: List[Claim] = Field(default_factory=list)


class Verification(BaseModel):
    verdict: Verdict
    confidence: float = Field(ge=0, le=1)
    what_the_evidence_says: str
    corrected_fact: str | None = None
    source_urls: List[str] = Field(default_factory=list)
    reasoning: str
