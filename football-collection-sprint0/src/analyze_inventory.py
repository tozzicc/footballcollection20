from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
HTML_EXTENSIONS = {".htm", ".html", ".asp"}
IGNORED_NAMES = {"thumbs.db", "desktop.ini", "temp.tmp"}
TECHNICAL_ROOTS = {"aspnet_client", "cgi-bin", "webalizer", "logs", "br"}


@dataclass(frozen=True)
class InventoryItem:
    relative_path: str
    name: str
    extension: str
    size_bytes: int
    category: str
    root_section: str
    country: str | None
    team: str | None
    collection_folder: str | None
    ignored: bool
    ignore_reason: str | None


def normalize_path(value: str) -> str:
    return value.strip().replace("\\", "/").lstrip("./")


def normalize_extension(value: str | None, name: str) -> str:
    ext = (value or "").strip().lower()
    if not ext:
        ext = Path(name).suffix.lower()
    return ext


def classify(extension: str) -> str:
    if extension in IMAGE_EXTENSIONS:
        return "image"
    if extension in HTML_EXTENSIONS:
        return "page"
    if extension in {".css"}:
        return "style"
    if extension in {".js"}:
        return "script"
    if extension in {".xml", ".json", ".csv", ".txt", ".dat"}:
        return "data"
    return "other"


def extract_collection(parts: tuple[str, ...]) -> tuple[str | None, str | None, str | None]:
    # Estrutura observada: camisas/<pais>/<equipe ou selecao>/<pasta-da-colecao>/arquivo
    if len(parts) < 2 or parts[0].lower() != "camisas":
        return None, None, None

    country = parts[1] if len(parts) >= 2 else None
    team = parts[2] if len(parts) >= 3 else None
    collection_folder = parts[3] if len(parts) >= 4 else None
    return country, team, collection_folder


def ignored_reason(parts: tuple[str, ...], name: str) -> str | None:
    lower_parts = {part.lower() for part in parts}
    if name.lower() in IGNORED_NAMES:
        return "known-system-file"
    if parts and parts[0].lower() in TECHNICAL_ROOTS:
        return "technical-root"
    if "additional plug-ins" in lower_parts or "additional presets" in lower_parts:
        return "software-artifact"
    return None


def parse_int(value: str | None) -> int:
    if value is None:
        return 0
    text = str(value).strip().replace(".", "").replace(",", ".")
    try:
        return int(float(text))
    except ValueError:
        return 0


def load_inventory(csv_path: Path) -> list[InventoryItem]:
    items: list[InventoryItem] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"CaminhoRelativo", "Name", "Extension", "Length"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(sorted(missing))}")

        for row in reader:
            relative_path = normalize_path(row.get("CaminhoRelativo", ""))
            if not relative_path:
                continue
            path = PurePosixPath(relative_path)
            parts = path.parts
            name = (row.get("Name") or path.name).strip()
            extension = normalize_extension(row.get("Extension"), name)
            reason = ignored_reason(parts, name)
            country, team, collection_folder = extract_collection(parts)

            items.append(
                InventoryItem(
                    relative_path=relative_path,
                    name=name,
                    extension=extension,
                    size_bytes=parse_int(row.get("Length")),
                    category=classify(extension),
                    root_section=parts[0] if parts else "",
                    country=country,
                    team=team,
                    collection_folder=collection_folder,
                    ignored=reason is not None,
                    ignore_reason=reason,
                )
            )
    return items


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "sem-nome"


def build_catalog(items: Iterable[InventoryItem]) -> dict:
    hierarchy: dict[str, dict[str, list[InventoryItem]]] = defaultdict(lambda: defaultdict(list))
    for item in items:
        if item.ignored or item.category != "image" or not item.country:
            continue
        hierarchy[item.country][item.team or "sem-equipe"].append(item)

    countries = []
    for country_name in sorted(hierarchy, key=str.casefold):
        teams = []
        for team_name in sorted(hierarchy[country_name], key=str.casefold):
            images = sorted(hierarchy[country_name][team_name], key=lambda x: x.relative_path.casefold())
            folders = Counter(image.collection_folder or "raiz" for image in images)
            teams.append(
                {
                    "id": slugify(f"{country_name}-{team_name}"),
                    "name": team_name,
                    "imageCount": len(images),
                    "folders": [
                        {"name": folder, "imageCount": count}
                        for folder, count in sorted(folders.items(), key=lambda x: x[0].casefold())
                    ],
                    "images": [image.relative_path for image in images],
                }
            )
        countries.append(
            {
                "id": slugify(country_name),
                "name": country_name,
                "imageCount": sum(team["imageCount"] for team in teams),
                "teamCount": len(teams),
                "teams": teams,
            }
        )

    return {
        "schemaVersion": 1,
        "countryCount": len(countries),
        "teamCount": sum(country["teamCount"] for country in countries),
        "imageCount": sum(country["imageCount"] for country in countries),
        "countries": countries,
    }


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_reports(items: list[InventoryItem], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "totalFiles": len(items),
        "totalBytes": sum(item.size_bytes for item in items),
        "byCategory": Counter(item.category for item in items),
        "byExtension": Counter(item.extension or "[sem extensão]" for item in items),
        "byRootSection": Counter(item.root_section for item in items),
        "ignoredFiles": sum(item.ignored for item in items),
        "validCollectionImages": sum(
            not item.ignored and item.category == "image" and item.country is not None for item in items
        ),
    }
    summary = {
        **summary,
        "byCategory": dict(summary["byCategory"].most_common()),
        "byExtension": dict(summary["byExtension"].most_common()),
        "byRootSection": dict(summary["byRootSection"].most_common()),
    }

    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    catalog = build_catalog(items)
    (output_dir / "catalog.preview.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    ignored_rows = [
        {
            "CaminhoRelativo": item.relative_path,
            "Motivo": item.ignore_reason or "",
            "TamanhoBytes": item.size_bytes,
        }
        for item in items
        if item.ignored
    ]
    write_csv(
        output_dir / "ignored-files.csv",
        ignored_rows,
        ["CaminhoRelativo", "Motivo", "TamanhoBytes"],
    )

    candidate_rows = [
        {
            "Pais": item.country or "",
            "Equipe": item.team or "",
            "PastaColecao": item.collection_folder or "",
            "Arquivo": item.name,
            "CaminhoRelativo": item.relative_path,
            "Extensao": item.extension,
            "TamanhoBytes": item.size_bytes,
        }
        for item in items
        if not item.ignored and item.category == "image" and item.country
    ]
    write_csv(
        output_dir / "collection-images.csv",
        candidate_rows,
        ["Pais", "Equipe", "PastaColecao", "Arquivo", "CaminhoRelativo", "Extensao", "TamanhoBytes"],
    )

    all_rows = [asdict(item) for item in items]
    (output_dir / "inventory.normalized.json").write_text(
        json.dumps(all_rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Analisa o inventário do Football Collection sem alterar o acervo.")
    parser.add_argument("inventory_csv", type=Path, help="CSV gerado pelo PowerShell")
    parser.add_argument("--output", type=Path, default=Path("output"), help="Diretório dos relatórios")
    args = parser.parse_args()

    if not args.inventory_csv.is_file():
        parser.error(f"Arquivo não encontrado: {args.inventory_csv}")

    items = load_inventory(args.inventory_csv)
    generate_reports(items, args.output)
    print(f"Análise concluída: {len(items)} arquivos processados.")
    print(f"Relatórios gerados em: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
