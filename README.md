# Truth Layer — PDF Fact-Check Agent

Truth Layer extracts checkable claims from uploaded PDFs, searches the live web, and labels
each claim **Verified**, **Inaccurate**, or **False**. It includes evidence snippets, source URLs,
confidence, progress, filters, and JSON/CSV exports.

## Architecture

```mermaid
flowchart LR
  U[User uploads PDF] --> P[Page extraction: pypdf]
  P --> C[Gemini claim extraction]
  C --> W[Parallel claim workers]
  W --> T[Tavily advanced search]
  T --> V[Gemini evidence judge]
  V --> R[Streamlit report + exports]
```

## Pipeline

1. Extract selectable text page-by-page.
2. Chunk large PDFs and ask Gemini for atomic, specific claims.
3. For each claim, generate 1–2 entity/metric/year queries.
4. Search with Tavily and deduplicate results.
5. Ask Gemini to judge with today's date and only the actual search snippets.
6. Return a source-constrained JSON result and exportable report.

## Setup

```powers
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Create a Gemini API key and Tavily API key. You can enter them in the sidebar, or configure:

```text
GEMINI_API_KEY=...
TAVILY_API_KEY=...
GEMINI_MODEL=gemini-2.5-flash
```

Copy `.env.example` to `.env` locally. Streamlit supports these values in `st.secrets`.

## Streamlit Community Cloud

1. Push the repository to GitHub.
2. Open [share.streamlit.io](https://share.streamlit.io), choose **New app**, select the repository,
   branch, and set **Main file path** to `app.py`.
3. Open **Advanced settings → Secrets** and paste:

```toml
GEMINI_API_KEY = "..."
TAVILY_API_KEY = "..."
GEMINI_MODEL = "gemini-2.5-flash"
```

4. Deploy. The app also has a bring-your-own-key sidebar fallback.

## Tests and sample

```powers
python -m compileall -q app.py src
python -m pytest -q
python sample/generate_trap_document.py
```

The generated trap PDF is [sample/trap_document.pdf](sample/trap_document.pdf).
Expected classifications and caveats are in [sample/expected_results.md](sample/expected_results.md).

## Design decisions

- `pypdf` preserves page numbers and avoids external OCR dependencies.
- Gemini returns Pydantic-validated JSON with `temperature=0`.
- Tavily uses advanced depth and two targeted queries per claim.
- Threading limits latency while Tenacity retries transient failures.
- Cached extraction and search reduce repeated API calls.
- Source URLs are filtered against actual Tavily results before display.

## Limitations

- Scanned PDFs require OCR and return a clear selectable-text error.
- Search quality depends on Tavily coverage and source authority.
- Gemini/Tavily can disagree or fail; API failures are labeled `Error - retry`.
- "False" means no credible evidence or direct contradiction, not mathematical certainty.
- Historical and date-sensitive claims need explicit model-date awareness.

## Future work

- Add OCR through an OCR provider.
- Add source-authority scoring and page-level evidence highlights.
- Add organization-specific source allowlists.
- Persist jobs and user feedback in a database.
- Support claim verification callbacks and human review.
