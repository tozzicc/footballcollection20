from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.services.historical_collections_service import HistoricalCollectionsService
from app.services.media_service import media_key


class FakeRepository:
    def __init__(self, workspace: Path, lookup: dict):
        self._workspace = workspace
        self._lookup = lookup
        self.saved = []

    def create_schema(self): pass
    def workspace(self): return str(self._workspace)
    def image_lookup(self): return self._lookup
    def persist(self, run, sections, items):
        self.saved.append((run, sections, items))
        return len(self.saved)


def source_html(src: str, caption: str, section: str) -> str:
    image = f'<table><tr><td><img src="{src}"></td></tr></table>'
    text = f'<table><tr><td>{caption}</td></tr></table>'
    if section == 'pennants':
        return f'<table><tr><td><img src="{src}"></td></tr><tr><td>{caption}</td></tr></table>'
    return text + image if section == 'flags' else image + text


def make_workspace(tmp_path: Path):
    definitions = [
        ('pennants/brasil.htm', 'brasil/a.jpg', 'BRASIL', 'pennants'),
        ('pennants/italy.htm', 'italy/a.jpg', 'ITALY', 'pennants'),
        ('pennants/other.htm', 'other/a.jpg', 'OTHER', 'pennants'),
        ('flags/flags.htm', 'a.jpg', 'JUVENTUS', 'flags'),
        ('memorabilia/memorabilia.htm', 'a.jpg', 'GUANTI - TACCONI', 'memorabilia'),
    ]
    lookup = {}
    for source, src, caption, section in definitions:
        page = tmp_path / source
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(source_html(src, caption, section), encoding='iso-8859-1')
        relative = (Path(source).parent / src).as_posix()
        lookup[relative.casefold()] = {'inventory_item_id': f'inv:{relative}', 'relative_path': relative, 'valid_image': 1, 'readable': 1}
    (tmp_path / 'pennants/pennants.htm').write_text('<html></html>', encoding='iso-8859-1')
    return lookup


def test_parses_three_domains_and_is_deterministic(tmp_path):
    repository = FakeRepository(tmp_path, make_workspace(tmp_path))
    service = HistoricalCollectionsService(repository)
    first, second = service.build(), service.build()
    assert first['total_items'] == second['total_items'] == 5
    assert [x['items_count'] for x in first['sections']] == [3, 1, 1]
    first_items, second_items = repository.saved[0][2], repository.saved[1][2]
    assert [x['stable_key'] for x in first_items] == [x['stable_key'] for x in second_items]
    assert [x['slug'] for x in first_items] == [x['slug'] for x in second_items]
    assert first_items[-1]['category'] == 'luvas'
    assert len({x['slug'] for x in first_items}) == 5


def test_missing_caption_is_review_required(tmp_path):
    lookup = make_workspace(tmp_path)
    (tmp_path / 'memorabilia/memorabilia.htm').write_text('<table><tr><td><img src="a.jpg"></td></tr></table>', encoding='iso-8859-1')
    repository = FakeRepository(tmp_path, lookup)
    HistoricalCollectionsService(repository).build()
    assert repository.saved[0][2][-1]['status'] == 'review_required'


def test_media_key_is_shared_deterministically():
    assert media_key('FLAGS/JUVENTUS.JPG') == media_key('flags/juventus.jpg')


def test_public_api_paginates_and_hides_internal_fields():
    client = TestClient(app)
    response = client.get('/api/public/collections/sections/pennants/items?group=italy&limit=2')
    assert response.status_code == 200
    payload = response.json()
    assert len(payload['items']) == 2 and payload['total'] == 88 and payload['hasNext']
    forbidden = ('sourceHtml', 'stableKey', 'inventory', 'workspace', 'runId', 'C:\\')
    serialized = response.text
    assert all(value not in serialized for value in forbidden)


def test_public_routes_are_unique():
    client = TestClient(app)
    page = client.get('/api/public/collections/sections/flags/items?limit=9').json()
    assert len({item['route'] for item in page['items']}) == 9
