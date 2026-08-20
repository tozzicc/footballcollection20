"""ET-029C selective reassociation prototype.

Dry-run is the default. The command refuses the official database and changes only
``catalog_items.collection_id`` for rows explicitly present in the authorized CSV.
"""

from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path


EXPECTED_BUILD = 10
EXPECTED_ITEMS = 4465
EXPECTED_AUTHORIZED = 703
OFFICIAL_DB = (Path(__file__).resolve().parents[2] / "database" / "football_collection.db").resolve()


class MigrationError(RuntimeError):
    pass


def restore_catalog_image_relations(database: Path, *, build_id: int = EXPECTED_BUILD,
                                    apply: bool = False,
                                    allow_official_apply: bool = False) -> dict[str, object]:
    """Recompute parser-backed relations and attach them to existing Catalog IDs.

    No item, collection, media file, or image metadata is created. The Catalog
    builder is executed through a capture-only repository and therefore cannot
    persist a new Catalog run.
    """
    database = database.resolve()
    if database == OFFICIAL_DB and not (apply and allow_official_apply):
        raise MigrationError("refusing to operate on the official database")
    backend = Path(__file__).resolve().parents[2] / "backend"
    if str(backend) not in sys.path:
        sys.path.insert(0, str(backend))
    from app.repositories.catalog_repository import CatalogRepository
    from app.services.catalog_builder_service import CatalogBuilderService

    delegate = CatalogRepository(database)

    class CaptureRepository:
        def __init__(self):
            self.items = None
            self.relations = None

        def prerequisites(self): return delegate.prerequisites()
        def source_data(self): return delegate.source_data()
        def last_build(self): return delegate.last_build()
        def save_build(self, run, countries, teams, collections, items, relations,
                       inferences, issues, replace_previous=True):
            self.items, self.relations = items, relations
            return build_id

    capture = CaptureRepository()
    CatalogBuilderService(capture).build(replace_previous=False)
    if capture.items is None or capture.relations is None:
        raise MigrationError("Catalog preview did not produce relations")
    db = sqlite3.connect(database)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    try:
        current = {row["relative_path"]: row["id"] for row in db.execute(
            "SELECT id,relative_path FROM catalog_items WHERE build_run_id=?", (build_id,))}
        prepared = {value[5]: key for key, value in capture.items.items()}
        if set(current) != set(prepared):
            raise MigrationError("Catalog/parser item identity set diverged")
        image_run = db.execute("SELECT MAX(id) FROM image_parse_runs WHERE status IN ('completed','completed_with_errors')").fetchone()[0]
        valid_images = {row[0] for row in db.execute("SELECT id FROM image_metadata WHERE run_id=?", (image_run,))}
        rows = []
        seen = set()
        for relation in capture.relations:
            item_key, image_id, source_page_id, reference, relative_path, order, alt, primary = relation
            item_path = capture.items[item_key][5]
            if image_id not in valid_images:
                raise MigrationError(f"relation references stale image metadata {image_id}")
            signature = (current[item_path], image_id, source_page_id, order)
            if signature in seen:
                raise MigrationError("duplicate Catalog image relation produced")
            seen.add(signature)
            rows.append((build_id, current[item_path], image_id, source_page_id, reference,
                         relative_path, order, alt, primary))
        before = db.execute("SELECT COUNT(*) FROM catalog_item_images WHERE build_run_id=?", (build_id,)).fetchone()[0]
        db.execute("BEGIN IMMEDIATE")
        db.execute("DELETE FROM catalog_item_images WHERE build_run_id=?", (build_id,))
        db.executemany("""INSERT INTO catalog_item_images(
            build_run_id,catalog_item_id,image_metadata_id,source_page_id,reference_original,
            relative_path,display_order,alt_text,is_primary_candidate)
            VALUES(?,?,?,?,?,?,?,?,?)""", rows)
        fk = db.execute("PRAGMA foreign_key_check").fetchall()
        if fk:
            raise MigrationError(f"foreign key errors after media restoration: {len(fk)}")
        result = {"mode": "apply" if apply else "dry-run", "before": before,
                  "after": len(rows), "items_with_relations": len({r[1] for r in rows}),
                  "image_run": image_run, "foreign_key_errors": 0}
        if apply: db.commit()
        else: db.rollback()
        return result
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@dataclass(frozen=True)
class AuthorizedMove:
    item_id: int
    identity: str
    team_path: str
    collection_before: str
    collection_target: str
    stable_key: str
    item_slug: str
    candidate_stable_key: str | None = None


def load_authorized(path: Path, expected_count: int = EXPECTED_AUTHORIZED) -> list[AuthorizedMove]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != expected_count:
        raise MigrationError(f"authorized list must contain {expected_count} rows; found {len(rows)}")
    moves = [AuthorizedMove(
        item_id=int(row["item_id"]), identity=row["identity"], team_path=row["team_path"],
        collection_before=row["collection_before"], collection_target=row["collection_target"],
        stable_key=row["stable_key"], item_slug=row["item_slug"],
        candidate_stable_key=row.get("candidate_stable_key") or None,
    ) for row in rows]
    if len({m.item_id for m in moves}) != len(moves):
        raise MigrationError("authorized list contains duplicate item IDs")
    return moves


def _scalar(db: sqlite3.Connection, sql: str, params: tuple = ()):
    return db.execute(sql, params).fetchone()[0]


def migrate(database: Path, authorized_csv: Path, *, apply: bool = False,
            expected_count: int = EXPECTED_AUTHORIZED,
            allow_protected_fot_gio: bool = False,
            update_stable_keys: bool = False,
            allow_official_apply: bool = False) -> dict[str, object]:
    database = database.resolve()
    if database == OFFICIAL_DB and not (apply and allow_official_apply and expected_count == 698):
        raise MigrationError("refusing to operate on the official database")
    moves = load_authorized(authorized_csv, expected_count)
    db = sqlite3.connect(database)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    try:
        build_id = _scalar(db, "SELECT MAX(id) FROM catalog_build_runs WHERE status='completed'")
        if build_id != EXPECTED_BUILD:
            raise MigrationError(f"baseline divergence: expected Catalog build {EXPECTED_BUILD}, found {build_id}")
        if _scalar(db, "SELECT COUNT(*) FROM catalog_items WHERE build_run_id=?", (build_id,)) != EXPECTED_ITEMS:
            raise MigrationError("baseline divergence: active Catalog item count is not 4465")
        images_before = _scalar(db, "SELECT COUNT(*) FROM catalog_item_images")
        identity_before = {m.item_id: tuple(db.execute(
            "SELECT id, team_id, relative_path, slug FROM catalog_items WHERE id=? AND build_run_id=?",
            (m.item_id, build_id)).fetchone() or ()) for m in moves}
        db.execute("BEGIN IMMEDIATE")
        changed = already_applied = stable_keys_changed = 0
        for move in moves:
            item = db.execute("""
                SELECT i.*, t.relative_path AS team_path, c.relative_path AS current_collection,
                       sk.stable_key
                FROM catalog_items i
                JOIN catalog_teams t ON t.id=i.team_id
                LEFT JOIN catalog_collections c ON c.id=i.collection_id
                JOIN catalog_stable_keys sk ON sk.build_run_id=i.build_run_id
                  AND sk.entity_type='item' AND sk.entity_id=i.id
                WHERE i.id=? AND i.build_run_id=?
            """, (move.item_id, build_id)).fetchone()
            if not item:
                raise MigrationError(f"missing authorized item {move.item_id}")
            checks = {
                "identity": (item["relative_path"], move.identity), "team": (item["team_path"], move.team_path),
                "stable key": (item["stable_key"], move.stable_key), "slug": (item["slug"], move.item_slug),
            }
            for label, (actual, expected) in checks.items():
                if actual != expected:
                    raise MigrationError(f"{label} mismatch for item {move.item_id}")
            target = db.execute("""
                SELECT c.id, t.relative_path AS team_path FROM catalog_collections c
                JOIN catalog_teams t ON t.id=c.team_id
                WHERE c.build_run_id=? AND c.relative_path=?
            """, (build_id, move.collection_target)).fetchone()
            if not target or target["team_path"] != move.team_path:
                raise MigrationError(f"missing/cross-team target for item {move.item_id}")
            touches_fot_gio = any("/torino/fot_gio" in value.lower() for value in
                                  (move.collection_before, move.collection_target))
            if touches_fot_gio and not allow_protected_fot_gio:
                raise MigrationError(f"protected fot-gio change requires separate authorization: item {move.item_id}")
            if item["current_collection"] == move.collection_target:
                already_applied += 1
                continue
            if item["current_collection"] != move.collection_before:
                raise MigrationError(f"source collection mismatch for item {move.item_id}")
            db.execute("UPDATE catalog_items SET collection_id=? WHERE id=?", (target["id"], move.item_id))
            changed += 1
            if update_stable_keys:
                if not move.candidate_stable_key:
                    raise MigrationError(f"missing approved candidate stable key for item {move.item_id}")
                db.execute("""UPDATE catalog_stable_keys SET stable_key=?
                              WHERE build_run_id=? AND entity_type='item' AND entity_id=?""",
                           (move.candidate_stable_key, build_id, move.item_id))
                if db.total_changes < 1:
                    raise MigrationError(f"stable key row missing for item {move.item_id}")
                stable_keys_changed += 1
        if _scalar(db, "SELECT COUNT(*) FROM catalog_items WHERE build_run_id=?", (build_id,)) != EXPECTED_ITEMS:
            raise MigrationError("item count changed")
        if _scalar(db, "SELECT COUNT(*) FROM catalog_item_images") != images_before:
            raise MigrationError("catalog_item_images changed")
        identity_after = {m.item_id: tuple(db.execute(
            "SELECT id, team_id, relative_path, slug FROM catalog_items WHERE id=?", (m.item_id,)).fetchone()) for m in moves}
        if identity_after != identity_before:
            raise MigrationError("item identity changed")
        duplicate_stable_keys = _scalar(db, """SELECT COUNT(*) FROM (
            SELECT stable_key FROM catalog_stable_keys WHERE build_run_id=?
            GROUP BY stable_key HAVING COUNT(*)>1)""", (build_id,))
        if duplicate_stable_keys:
            raise MigrationError(f"stable key collisions after reassociation: {duplicate_stable_keys}")
        fk_errors = db.execute("PRAGMA foreign_key_check").fetchall()
        integrity = _scalar(db, "PRAGMA integrity_check")
        if fk_errors or integrity != "ok":
            raise MigrationError(f"database integrity failed: {integrity}; FK errors={len(fk_errors)}")
        result = {"mode": "apply" if apply else "dry-run", "authorized": len(moves),
                  "changed": changed, "already_applied": already_applied,
                  "stable_keys_changed": stable_keys_changed,
                  "integrity_check": integrity, "foreign_key_errors": len(fk_errors)}
        if apply:
            db.commit()
        else:
            db.rollback()
        return result
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", required=True, type=Path)
    parser.add_argument("--authorized-csv", required=True, type=Path)
    parser.add_argument("--expected-count", type=int, default=EXPECTED_AUTHORIZED,
                        help="exact whitelist cardinality (698 for the ET-029D safe subset)")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--allow-protected-fot-gio", action="store_true",
                        help="prototype-only override for the protected Torino/fot_gio case")
    parser.add_argument("--restore-catalog-media", action="store_true",
                        help="recompute parser-backed Catalog image relations after reassociation")
    args = parser.parse_args()
    result = migrate(args.database, args.authorized_csv, apply=args.apply,
                     expected_count=args.expected_count,
                     allow_protected_fot_gio=args.allow_protected_fot_gio)
    if args.restore_catalog_media:
        result["catalog_media"] = restore_catalog_image_relations(args.database, apply=args.apply)
    print(result)


if __name__ == "__main__":
    main()
