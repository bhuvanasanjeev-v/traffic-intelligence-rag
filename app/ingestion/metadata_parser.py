from pathlib import Path


def parse_metadata_from_filename(file_path):
    stem = Path(file_path).stem
    parts = [
        part
        for part in stem.split("_")
        if part
    ]

    year = _extract_year(parts)
    site = _extract_site(parts, year)
    document_type = _extract_document_type(parts, site, year)

    return {
        "document_type": document_type,
        "site": site,
        "year": year,
    }


def _extract_year(parts):
    for part in reversed(parts):
        if part.isdigit() and len(part) == 4:
            return int(part)

    return None


def _extract_site(parts, year):
    ignored_tokens = {"new", "report", "data"}
    site_index = len(parts) - 1

    if year is not None and parts and parts[-1] == str(year):
        site_index -= 1

    if site_index < 0:
        return None

    site = parts[site_index]

    if site.lower() in ignored_tokens:
        return None

    return site


def _extract_document_type(parts, site, year):
    metadata_tokens = []

    if year is not None:
        metadata_tokens.append(str(year))

    if site is not None:
        metadata_tokens.append(site)

    document_type_parts = [
        part
        for part in parts
        if part not in metadata_tokens
    ]

    if not document_type_parts:
        return "unknown"

    return "_".join(document_type_parts).lower()
