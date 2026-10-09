#!/usr/bin/env python3
"""Validate the public Readiness Index data files."""

import csv
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
COMPANIES = ROOT / "data" / "companies.csv"
SOURCES = ROOT / "data" / "sources.csv"

DIMENSIONS = (
    "model_configuration_comparison",
    "trace_production_evaluation",
    "action_tool_validation",
    "human_acceptance",
    "workflow_simulation",
    "business_outcome",
)

EVIDENCE_STATES = {"shown", "partial", "not_found_publicly"}
VERIFICATION_STATES = {
    "not_contacted",
    "fact_check_sent",
    "confirmed_by_company",
    "corrected_by_company",
    "not_reviewed_by_company",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    companies = read_csv(COMPANIES)
    sources = read_csv(SOURCES)

    assert len(companies) == 12, f"expected 12 companies, found {len(companies)}"

    names = [row["company"] for row in companies]
    assert names == sorted(names, key=str.casefold), "companies must remain alphabetical"
    assert len(names) == len(set(names)), "company names must be unique"

    for row in companies:
        for dimension in DIMENSIONS:
            assert row[dimension] in EVIDENCE_STATES, (
                f"{row['company']}: invalid {dimension} state {row[dimension]}"
            )
        assert row["verification_status"] in VERIFICATION_STATES, (
            f"{row['company']}: invalid verification status"
        )

    source_companies = {row["company"] for row in sources}
    assert set(names) == source_companies, "every company must have at least one source"

    for row in sources:
        parsed = urlparse(row["url"])
        assert parsed.scheme == "https" and parsed.netloc, (
            f"{row['company']}: invalid source URL {row['url']}"
        )
        listed_dimensions = set(row["dimensions"].split("|"))
        assert listed_dimensions <= set(DIMENSIONS), (
            f"{row['company']}: unknown source dimension"
        )

    print(f"Readiness Index valid: {len(companies)} companies, {len(sources)} sources")


if __name__ == "__main__":
    main()

