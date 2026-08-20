from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EditorialRecord:
    anchor: str
    status: str
    rule: str | None
    description: str | None
    references: tuple[dict, ...]


def derive_editorial_records(references: list[dict], contexts: list[dict]) -> list[EditorialRecord]:
    """Derive safe garment records from contiguous, matched DOM image contexts.

    Splitting is allowed when every referenced image has persisted structural
    identity. Matched, ambiguous and unsupported groups keep their own status; the
    record boundary is a transition between contiguous structural groups. Image
    counts and filename/content semantics never participate in the decision.
    """
    ordered = list(references)
    if not ordered:
        return [EditorialRecord("page", "unsupported", None, None, ())]
    by_reference = {row.get("image_reference_id"): row for row in contexts}
    paired = [(ref, by_reference.get(ref.get("id"))) for ref in ordered]
    if any(context is None or (not context.get("structural_group_key") and (context.get("status") != "matched" or not context.get("context_text"))) for _, context in paired):
        status = "ambiguous" if any(context and context.get("status") == "ambiguous" for _, context in paired) else "unsupported"
        return [EditorialRecord("page", status, None, None, tuple(ordered))]
    unsafe = [context for _, context in paired if context.get("status") != "matched" or not context.get("context_text")]
    if unsafe:
        matched_signatures = {
            (context["structural_group_key"], " ".join(context["context_text"].split()).casefold())
            for _, context in paired
            if context.get("status") == "matched" and context.get("context_text") and context.get("structural_group_key")
        }
        unsafe_groups = {context.get("structural_group_key") for context in unsafe}
        descriptions = [description for _, description in matched_signatures]
        isolated_repeated_pair = (
            len(unsafe_groups) == 1
            and all(context.get("status") == "no_description" for context in unsafe)
            and len(matched_signatures) == 2
            and len(set(descriptions)) == 1
        )
        if not isolated_repeated_pair:
            status = "ambiguous" if any(context.get("status") == "ambiguous" for context in unsafe) else "unsupported"
            return [EditorialRecord("page", status, None, None, tuple(ordered))]
    groups: list[list[tuple[dict, dict]]] = []
    for ref, context in paired:
        signature = context.get("structural_group_key") or (context["extraction_rule"], context.get("container_type"), context["context_text"])
        previous = groups[-1][0][1] if groups else None
        previous_signature = None if previous is None else (previous.get("structural_group_key") or (previous["extraction_rule"], previous.get("container_type"), previous["context_text"]))
        if not groups or signature != previous_signature:
            groups.append([])
        groups[-1].append((ref, context))
    records = []
    if len(groups) == 1 and not groups[0][0][1].get("structural_group_key"):
        context = groups[0][0][1]
        return [EditorialRecord("page", "matched", context["extraction_rule"], context["context_text"], tuple(ref for ref, _ in groups[0]))]
    for group in groups:
        context = group[0][1]
        first_order = min(int(row[1]["dom_order"]) for row in group)
        anchor = context.get("structural_group_key") or f"{context['extraction_rule'].casefold()}:{context.get('container_type') or 'unknown'}:dom-{first_order}"
        raw_status = context.get("status")
        status = "matched" if raw_status == "matched" and context.get("context_text") else ("ambiguous" if raw_status == "ambiguous" else "unsupported")
        records.append(EditorialRecord(anchor, status, context.get("extraction_rule"), context.get("context_text"), tuple(ref for ref, _ in group)))
    return records


def audit_editorial_records(pages: list[dict], references: list[dict], contexts: list[dict]) -> dict:
    refs_by_page: dict[int, list[dict]] = {}
    contexts_by_page: dict[int, list[dict]] = {}
    for row in references:
        refs_by_page.setdefault(row["page_id"], []).append(row)
    for row in contexts:
        contexts_by_page.setdefault(row["html_page_id"], []).append(row)
    stats = {"pages": len(pages), "singleRecordPages": 0, "multipleRecordPages": 0, "safeRecords": 0, "ambiguousPages": 0, "unsupportedPages": 0, "potentiallyGroupedItems": 0, "examples": []}
    for page in pages:
        records = derive_editorial_records(refs_by_page.get(page["id"], []), contexts_by_page.get(page["id"], []))
        if len(records) > 1:
            stats["multipleRecordPages"] += 1
            stats["potentiallyGroupedItems"] += 1
            if len(stats["examples"]) < 10:
                stats["examples"].append({"page": page["relative_path"], "records": len(records), "descriptions": [x.description for x in records]})
        else:
            stats["singleRecordPages"] += 1
        stats["safeRecords"] += sum(x.status == "matched" for x in records)
        stats["ambiguousPages"] += int(any(x.status == "ambiguous" for x in records))
        stats["unsupportedPages"] += int(any(x.status == "unsupported" for x in records))
    return stats
