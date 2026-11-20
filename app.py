import csv
import io
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import streamlit as st
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from src.claim_extractor import extract_claims
from src.pdf_utils import extract_pages
from src.search import web_search
from src.verifier import generate_queries, verify_claim


st.set_page_config(page_title="Truth Layer", page_icon="🔎", layout="wide")


def secret(name: str, fallback: str = "") -> str:
    try:
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    return os.getenv(name, fallback)


def current_model_name() -> str:
    configured = secret("GEMINI_MODEL", "gemini-3.5-flash-lite")
    if configured in ("gemini-3.8-flash", "gemini-2.5-flash", "gemini-2.5-flash-lite"):
        return "gemini-3.5-flash-lite"
    return configured


with st.sidebar:
    st.header("API setup")
    gemini_key = st.text_input(
        "Gemini API key",
        value=secret("GEMINI_API_KEY"),
        type="password",
    )
    tavily_key = st.text_input(
        "Tavily API key",
        value=secret("TAVILY_API_KEY"),
        type="password",
    )
    model = st.text_input("Model", value=current_model_name())
    max_claims = st.slider("Maximum claims", 5, 25, 5)

st.title("Truth Layer")
st.caption("Upload a PDF. We extract checkable claims and compare them with live web evidence.")

uploaded = st.file_uploader("Upload PDF", type=["pdf"])
sample = st.button("Analyze sample trap PDF")


@st.cache_data(show_spinner=False)
def cached_extract(pdf_bytes: bytes, key: str, model_name: str, limit: int):
    import io
    class InMemoryFile:
        def read(self):
            return pdf_bytes
    pages = extract_pages(InMemoryFile())
    if not any(text.strip() for _, text in pages):
        raise ValueError("No selectable text was found. This PDF may be scanned.")
    return extract_claims(pages, key, model_name, limit).model_dump()


def retryable_verification_error(exc):
    message = str(exc).upper()
    if any(code in message for code in ("429", "RESOURCE_EXHAUSTED", "QUOTA")):
        return False
    if any(code in message for code in ("401", "403", "INVALID_API_KEY")):
        return False
    return any(code in message for code in ("408", "500", "502", "503", "504", "TIMEOUT", "CONNECTION"))


@st.cache_data(show_spinner=False)
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception(retryable_verification_error),
    reraise=True,
)
def verify_one(claim, gemini_key, tavily_key, model_name):
    results = []
    for query in generate_queries(claim)[:2]:
        results.extend(cached_search(query, tavily_key))
    deduped = {r["url"]: r for r in results}
    verification = verify_claim(claim, list(deduped.values()), gemini_key, model_name)
    return claim, verification


@st.cache_data(show_spinner=False)
def cached_search(query: str, tavily_key: str):
    return web_search(query, tavily_key)


def run_analysis(pdf_bytes: bytes):
    if not gemini_key or not tavily_key:
        st.error("Add both API keys in the sidebar or Streamlit secrets.")
        return
    try:
        claim_data = cached_extract(pdf_bytes, gemini_key, model, max_claims)
    except Exception as exc:
        st.error(str(exc))
        return
    claims = [__import__("src.schemas", fromlist=["Claim"]).Claim.model_validate(c) for c in claim_data["claims"]]
    if not claims:
        st.warning("No specific, checkable claims were found.")
        return

    st.subheader("Verification progress")
    progress = st.progress(0)
    status = st.empty()
    rows = []
    with ThreadPoolExecutor(max_workers=1) as pool:
        futures = {
            pool.submit(verify_one, claim, gemini_key, tavily_key, model): claim
            for claim in claims
        }
        for index, future in enumerate(as_completed(futures), start=1):
            claim = futures[future]
            status.write(f"Checking claim {index}/{len(claims)}: {claim.claim_text[:100]}...")
            try:
                _, result = future.result()
                row = {"claim": claim, "result": result}
            except Exception as exc:
                error_text = str(exc)
                if any(code in error_text.upper() for code in ("429", "RESOURCE_EXHAUSTED", "QUOTA")):
                    reasoning = "API quota exhausted. Gemini's daily or per-minute quota was reached; wait for reset or use another key."
                elif "INVALID_TAVILY" in error_text.upper():
                    reasoning = "Tavily API key is invalid. Check Streamlit secrets or the sidebar key."
                else:
                    reasoning = f"Error - retry: {type(exc).__name__}: {error_text}"
                row = {
                    "claim": claim,
                    "result": __import__("src.schemas", fromlist=["Verification"]).Verification(
                        verdict="Error - retry",
                        confidence=0,
                        what_the_evidence_says="Verification request failed.",
                        corrected_fact=None,
                        source_urls=[],
                        reasoning=reasoning,
                    ),
                }
            rows.append(row)
            progress.progress(index / len(claims))
    status.write("Analysis complete.")

    counts = {"Verified": 0, "Inaccurate": 0, "False": 0, "Error - retry": 0}
    for row in rows:
        counts[row["result"].verdict] += 1
    trust = round(100 * counts["Verified"] / len(rows)) if rows else 0
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Verified", counts["Verified"])
    c2.metric("Inaccurate", counts["Inaccurate"])
    c3.metric("False", counts["False"])
    c4.metric("Trust score", f"{trust}%")

    verdict_filter = st.pills(
        "Filter verdict",
        ["All", "Verified", "Inaccurate", "False", "Error - retry"],
        default="All",
    )
    for row in rows:
        claim = row["claim"]
        result = row["result"]
        if verdict_filter != "All" and result.verdict != verdict_filter:
            continue
        color = {
            "Verified": "green",
            "Inaccurate": "orange",
            "False": "red",
            "Error - retry": "gray",
        }[result.verdict]
        st.markdown(f":{color}[**{result.verdict}**] · Page {claim.page_number} · Confidence {result.confidence:.0%}")
        st.markdown(f"**Original:** {claim.claim_text}")
        st.write(result.what_the_evidence_says)
        if result.corrected_fact:
            st.info(f"**Real fact:** {result.corrected_fact}")
        for url in result.source_urls:
            st.write(url)
        st.caption(result.reasoning)
        st.divider()

    export_rows = []
    for row in rows:
        claim, result = row["claim"], row["result"]
        export_rows.append({
            "claim_text": claim.claim_text,
            "category": claim.category,
            "page_number": claim.page_number,
            "exact_snippet": claim.exact_snippet,
            "verdict": result.verdict,
            "confidence": result.confidence,
            "what_the_evidence_says": result.what_the_evidence_says,
            "corrected_fact": result.corrected_fact or "",
            "source_urls": "; ".join(result.source_urls),
            "reasoning": result.reasoning,
        })
    json_bytes = __import__("json").dumps(export_rows, indent=2).encode()
    st.download_button("Download JSON", json_bytes, "truth-layer-results.json", "application/json")
    text = io.StringIO()
    if export_rows:
        writer = csv.DictWriter(text, fieldnames=export_rows[0].keys())
        writer.writeheader()
        writer.writerows(export_rows)
    st.download_button("Download CSV", text.getvalue(), "truth-layer-results.csv", "text/csv")


if sample:
    try:
        run_analysis(open("sample/trap_document.pdf", "rb").read())
    except FileNotFoundError:
        st.error("Bundled sample PDF is missing.")
elif uploaded:
    run_analysis(uploaded.getvalue())
