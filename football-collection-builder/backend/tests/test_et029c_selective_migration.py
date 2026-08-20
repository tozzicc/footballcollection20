import csv
import importlib.util
import sqlite3
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[2] / "scripts/migrations/et_029c_selective_collection_reassociation.py"
SPEC = importlib.util.spec_from_file_location("et029c", SCRIPT)
et029c = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = et029c
SPEC.loader.exec_module(et029c)


def make_fixture(tmp_path, *, bad_target_team=False):
    db_path = tmp_path / "candidate.db"
    db = sqlite3.connect(db_path)
    db.executescript("""
      PRAGMA foreign_keys=ON;
      CREATE TABLE catalog_build_runs(id INTEGER PRIMARY KEY,status TEXT);
      CREATE TABLE catalog_teams(id INTEGER PRIMARY KEY,build_run_id INTEGER,relative_path TEXT);
      CREATE TABLE catalog_collections(id INTEGER PRIMARY KEY,build_run_id INTEGER,team_id INTEGER REFERENCES catalog_teams(id),relative_path TEXT);
      CREATE TABLE catalog_items(id INTEGER PRIMARY KEY,build_run_id INTEGER,team_id INTEGER REFERENCES catalog_teams(id),collection_id INTEGER REFERENCES catalog_collections(id),relative_path TEXT,slug TEXT);
      CREATE TABLE catalog_stable_keys(id INTEGER PRIMARY KEY,build_run_id INTEGER,entity_type TEXT,entity_id INTEGER,stable_key TEXT);
      CREATE TABLE catalog_item_images(id INTEGER PRIMARY KEY,catalog_item_id INTEGER REFERENCES catalog_items(id));
      INSERT INTO catalog_build_runs VALUES(10,'completed');
      INSERT INTO catalog_teams VALUES(1,10,'paises/brasil/teste');
      INSERT INTO catalog_teams VALUES(2,10,'paises/italia/outro');
      INSERT INTO catalog_collections VALUES(10,10,1,'camisas/brasil/teste/old');
      INSERT INTO catalog_collections VALUES(11,10,1,'camisas/brasil/teste/new');
      INSERT INTO catalog_items VALUES(100,10,1,10,'paises/brasil/teste/a.htm#x','a');
      INSERT INTO catalog_stable_keys VALUES(1,10,'item',100,'item:key');
    """)
    if bad_target_team:
        db.execute("UPDATE catalog_collections SET team_id=2 WHERE id=11")
    db.commit(); db.close()
    csv_path = tmp_path / "authorized.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["item_id", "identity", "team_path", "collection_before", "collection_target", "stable_key", "item_slug"])
        writer.writeheader(); writer.writerow({"item_id":100,"identity":"paises/brasil/teste/a.htm#x","team_path":"paises/brasil/teste","collection_before":"camisas/brasil/teste/old","collection_target":"camisas/brasil/teste/new","stable_key":"item:key","item_slug":"a"})
    return db_path, csv_path


@pytest.fixture(autouse=True)
def compact_baseline(monkeypatch):
    monkeypatch.setattr(et029c, "EXPECTED_ITEMS", 1)


def collection_id(path):
    db = sqlite3.connect(path); value = db.execute("SELECT collection_id FROM catalog_items WHERE id=100").fetchone()[0]; db.close(); return value


def test_dry_run_rolls_back(tmp_path):
    db, rows = make_fixture(tmp_path)
    result = et029c.migrate(db, rows, expected_count=1)
    assert result["changed"] == 1 and collection_id(db) == 10


def test_apply_and_idempotency_preserve_identity(tmp_path):
    db, rows = make_fixture(tmp_path)
    assert et029c.migrate(db, rows, apply=True, expected_count=1)["changed"] == 1
    assert collection_id(db) == 11
    result = et029c.migrate(db, rows, apply=True, expected_count=1)
    assert result["already_applied"] == 1
    con = sqlite3.connect(db)
    assert con.execute("SELECT id,team_id,relative_path,slug FROM catalog_items").fetchone() == (100,1,"paises/brasil/teste/a.htm#x","a")
    assert con.execute("PRAGMA foreign_key_check").fetchall() == []


@pytest.mark.parametrize("field,value", [("stable_key","wrong"),("team_path","paises/brasil/wrong"),("identity","wrong")])
def test_divergence_rolls_back(tmp_path, field, value):
    db, rows = make_fixture(tmp_path)
    data = list(csv.DictReader(rows.open(encoding="utf-8"))); data[0][field] = value
    with rows.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=data[0].keys()); w.writeheader(); w.writerows(data)
    with pytest.raises(et029c.MigrationError): et029c.migrate(db, rows, apply=True, expected_count=1)
    assert collection_id(db) == 10


def test_missing_collection_and_team_mismatch_are_rejected(tmp_path):
    db, rows = make_fixture(tmp_path, bad_target_team=True)
    with pytest.raises(et029c.MigrationError): et029c.migrate(db, rows, expected_count=1)


def test_unauthorized_fot_gio_cannot_be_changed(tmp_path):
    db, rows = make_fixture(tmp_path)
    con=sqlite3.connect(db); con.execute("UPDATE catalog_collections SET relative_path='camisas/italia/torino/fot_gio' WHERE id=10"); con.commit(); con.close()
    data=list(csv.DictReader(rows.open(encoding="utf-8"))); data[0]["collection_before"]='camisas/italia/torino/fot_gio'
    with rows.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=data[0].keys()); w.writeheader(); w.writerows(data)
    with pytest.raises(et029c.MigrationError): et029c.migrate(db, rows, expected_count=1)


def test_authorized_count_and_duplicates_are_enforced(tmp_path):
    db, rows = make_fixture(tmp_path)
    with pytest.raises(et029c.MigrationError): et029c.migrate(db, rows, expected_count=2)


def test_explicit_safe_subset_cardinality_is_accepted(tmp_path):
    db, rows = make_fixture(tmp_path)
    result = et029c.migrate(db, rows, expected_count=1)
    assert result["authorized"] == 1


def test_official_database_is_always_rejected(tmp_path, monkeypatch):
    db, rows = make_fixture(tmp_path)
    monkeypatch.setattr(et029c, "OFFICIAL_DB", db.resolve())
    with pytest.raises(et029c.MigrationError): et029c.migrate(db, rows, expected_count=1)


def test_approved_candidate_stable_key_is_updated_with_reassociation(tmp_path):
    db, rows = make_fixture(tmp_path)
    data = list(csv.DictReader(rows.open(encoding="utf-8")))
    data[0]["candidate_stable_key"] = "item:candidate"
    with rows.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    result = et029c.migrate(db, rows, apply=True, expected_count=1, update_stable_keys=True)
    con = sqlite3.connect(db)
    assert result["stable_keys_changed"] == 1
    assert con.execute("SELECT stable_key FROM catalog_stable_keys").fetchone()[0] == "item:candidate"
    con.close()
