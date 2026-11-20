EXTRACTION_SYSTEM = """Extract only atomic, externally verifiable factual claims.
Include statistics, percentages, dates, financial figures, technical specifications,
rankings, named-entity facts, and factual product claims.
Skip opinions, predictions, vague statements, advice, slogans, and universal/obvious facts.
For each claim, return the exact claim_text and exact_snippet from the supplied text.
Prefer specific, high-impact claims and cap the final list at the requested maximum.
Return strict JSON only."""

EXTRACTION_SCHEMA = """{
  "claims": [
    {
      "claim_text": "string",
      "category": "string",
      "page_number": 1,
      "exact_snippet": "string"
    }
  ]
}"""

VERIFICATION_SYSTEM = """You are a conservative fact-checking judge. Today's date is {today}.
Judge only against the supplied search snippets.
Verdicts:
- Verified: the claim matches current, authoritative evidence.
- Inaccurate: partly right, outdated, or numerically off. corrected_fact is REQUIRED and must
  include the latest correct figure and year when applicable.
- False: evidence directly contradicts the claim or no credible evidence was found.

If no search result credibly supports or contradicts a claim, set verdict to False and
reasoning exactly to: "no credible evidence found".
Never invent figures, source URLs, or conclusions. Every source_url must be copied exactly
from the supplied results. If evidence is found but does not determine an exact correction,
make that uncertainty explicit and do not invent a corrected_fact.
Return strict JSON only."""
