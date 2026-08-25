"""A dependency-free local vector-store adapter for reviewed knowledge records."""

import hashlib
import json
import math
import re

from pathlib import Path

from .domain import SourceReference


ROOT = Path(__file__).resolve().parents[2] / "knowledge"
DOCUMENTS = ROOT / "documents"
INDEX = ROOT / "processed" / "index.json"

DIMENSIONS = 128


def embedding(text: str):
    vector = [0.0] * DIMENSIONS

    for term in re.findall(r"[a-z]{3,}", text.lower()):
        index = int(
            hashlib.sha256(term.encode()).hexdigest(),
            16,
        ) % DIMENSIONS

        vector[index] += 1

    length = math.sqrt(sum(item * item for item in vector)) or 1

    return [
        item / length
        for item in vector
    ]


def _parse(path: Path):
    """
    Parse a reviewed knowledge markdown file.

    Expected format:

    ---
    document_id: ...
    title: ...
    url: ...
    section: ...
    ---

    Content...
    """

    raw = path.read_text(encoding="utf-8").strip()

    # Split using the metadata delimiters.
    parts = re.split(
        r"^---\s*$",
        raw,
        maxsplit=2,
        flags=re.MULTILINE,
    )

    if len(parts) < 3:
        raise ValueError(
            f"Invalid knowledge document format: {path.name}"
        )

    metadata_text = parts[1].strip()
    excerpt = parts[2].strip()

    meta = {}

    for line in metadata_text.splitlines():
        line = line.strip()

        if not line:
            continue

        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        meta[key.strip()] = value.strip()

    required_fields = [
        "document_id",
        "title",
        "url",
        "section",
    ]

    missing = [
        field
        for field in required_fields
        if not meta.get(field)
    ]

    if missing:
        raise ValueError(
            f"Missing {', '.join(missing)} "
            f"in knowledge document: {path.name}"
        )

    return {
        **meta,
        "excerpt": excerpt,
    }


def build_index():
    """
    Build a local vector index from all reviewed knowledge documents.
    """

    records = []

    for path in DOCUMENTS.glob("*.md"):
        record = _parse(path)

        searchable_text = (
            record["document_id"]
            + " "
            + record["title"]
            + " "
            + record["section"]
            + " "
            + record["excerpt"]
        )

        record["embedding"] = embedding(searchable_text)

        records.append(record)

    INDEX.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    INDEX.write_text(
        json.dumps(
            records,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return records


def retrieve(
    query: str,
    limit: int = 2,
) -> list[SourceReference]:
    """
    Retrieve the most relevant reviewed knowledge records.
    """

    if INDEX.exists():
        try:
            records = json.loads(
                INDEX.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:
            records = build_index()

    else:
        records = build_index()

    # Rebuild if the existing index contains old or invalid records.
    required_fields = {
        "document_id",
        "title",
        "url",
        "section",
        "excerpt",
        "embedding",
    }

    if any(
        not required_fields.issubset(record.keys())
        for record in records
    ):
        records = build_index()

    query_vector = embedding(query)

    query_terms = set(
        re.findall(
            r"[a-z]{3,}",
            query.lower(),
        )
    )

    ranked = []

    for record in records:
        searchable_text = (
            record["document_id"]
            + " "
            + record["title"]
            + " "
            + record["section"]
            + " "
            + record["excerpt"]
        )

        record_terms = set(
            re.findall(
                r"[a-z]{3,}",
                searchable_text.lower(),
            )
        )

        # Require at least one overlapping term.
        if not query_terms.intersection(record_terms):
            continue

        score = sum(
            a * b
            for a, b in zip(
                query_vector,
                record["embedding"],
            )
        )

        if score > 0.02:
            ranked.append(
                (score, record)
            )

    ranked.sort(
        reverse=True,
        key=lambda pair: pair[0],
    )

    return [
        SourceReference(
            document_id=item["document_id"],
            title=item["title"],
            url=item["url"],
            section=item["section"],
            excerpt=item["excerpt"],
        )
        for _, item in ranked[:limit]
    ]