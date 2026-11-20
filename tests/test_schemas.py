from src.schemas import Verification


def test_inaccurate_requires_corrected_fact():
    value = Verification(
        verdict="Inaccurate",
        confidence=0.9,
        what_the_evidence_says="The older number is outdated.",
        corrected_fact="The 2025 figure is 301.63 million.",
        source_urls=["https://example.com"],
        reasoning="The cited evidence gives a newer figure.",
    )
    assert value.corrected_fact
