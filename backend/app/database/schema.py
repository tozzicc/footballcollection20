SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS inventory_metadata (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    generated_at TEXT NOT NULL,
    scanner_version TEXT NOT NULL,
    workspace_path TEXT NOT NULL,
    duration_ms INTEGER NOT NULL,
    saved_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory_statistics (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    total_files INTEGER NOT NULL,
    total_directories INTEGER NOT NULL,
    total_size INTEGER NOT NULL,
    total_images INTEGER NOT NULL,
    total_pages INTEGER NOT NULL,
    total_videos INTEGER NOT NULL,
    total_documents INTEGER NOT NULL,
    total_archives INTEGER NOT NULL,
    total_data INTEGER NOT NULL,
    total_other INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory_folders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    name TEXT NOT NULL,
    parent TEXT,
    depth INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory_items (
    id TEXT PRIMARY KEY,
    relative_path TEXT NOT NULL,
    absolute_path TEXT NOT NULL,
    directory TEXT NOT NULL,
    filename TEXT NOT NULL,
    extension TEXT NOT NULL,
    category TEXT NOT NULL,
    size INTEGER NOT NULL,
    created_at TEXT,
    modified_at TEXT,
    is_directory INTEGER NOT NULL,
    readable INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory_extensions (
    extension TEXT PRIMARY KEY,
    count INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory_categories (
    category TEXT PRIMARY KEY,
    count INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_inventory_folders_relative_path ON inventory_folders(relative_path);
CREATE INDEX IF NOT EXISTS idx_inventory_items_relative_path ON inventory_items(relative_path);
CREATE INDEX IF NOT EXISTS idx_inventory_items_extension ON inventory_items(extension);
CREATE INDEX IF NOT EXISTS idx_inventory_items_category ON inventory_items(category);
CREATE INDEX IF NOT EXISTS idx_inventory_items_directory ON inventory_items(directory);

CREATE TABLE IF NOT EXISTS html_parse_runs (
 id INTEGER PRIMARY KEY AUTOINCREMENT, workspace_path TEXT NOT NULL, started_at TEXT NOT NULL,
 finished_at TEXT, duration_ms INTEGER NOT NULL DEFAULT 0, status TEXT NOT NULL,
 total_pages INTEGER NOT NULL DEFAULT 0, parsed_pages INTEGER NOT NULL DEFAULT 0,
 failed_pages INTEGER NOT NULL DEFAULT 0, image_references INTEGER NOT NULL DEFAULT 0,
 internal_links INTEGER NOT NULL DEFAULT 0, external_links INTEGER NOT NULL DEFAULT 0,
 missing_references INTEGER NOT NULL DEFAULT 0, message TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS html_pages (
 id INTEGER PRIMARY KEY AUTOINCREMENT, run_id INTEGER NOT NULL, inventory_item_id TEXT NOT NULL,
 relative_path TEXT NOT NULL, absolute_path TEXT NOT NULL, filename TEXT NOT NULL,
 extension TEXT NOT NULL, file_size INTEGER NOT NULL, created_at TEXT, modified_at TEXT,
 encoding_used TEXT, title TEXT NOT NULL, document_language TEXT, charset_declared TEXT,
 meta_description TEXT, text_preview TEXT NOT NULL, parse_status TEXT NOT NULL,
 parse_message TEXT NOT NULL, FOREIGN KEY(run_id) REFERENCES html_parse_runs(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS html_headings (
 id INTEGER PRIMARY KEY AUTOINCREMENT, page_id INTEGER NOT NULL, level INTEGER NOT NULL,
 position INTEGER NOT NULL, text TEXT NOT NULL,
 FOREIGN KEY(page_id) REFERENCES html_pages(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS html_image_references (
 id INTEGER PRIMARY KEY AUTOINCREMENT, page_id INTEGER NOT NULL, src_original TEXT NOT NULL,
 src_normalized TEXT NOT NULL, alt_text TEXT, title_text TEXT, width_declared TEXT,
 height_declared TEXT, is_external INTEGER NOT NULL, resolved_relative_path TEXT,
 resolved_absolute_path TEXT, exists_in_inventory INTEGER NOT NULL,
 referenced_inventory_item_id TEXT, status TEXT NOT NULL,
 FOREIGN KEY(page_id) REFERENCES html_pages(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS html_link_references (
 id INTEGER PRIMARY KEY AUTOINCREMENT, page_id INTEGER NOT NULL, href_original TEXT NOT NULL,
 href_normalized TEXT NOT NULL, visible_text TEXT, title_text TEXT, is_external INTEGER NOT NULL,
 is_anchor INTEGER NOT NULL, is_mailto INTEGER NOT NULL, is_javascript INTEGER NOT NULL,
 resolved_relative_path TEXT, exists_in_inventory INTEGER NOT NULL,
 referenced_inventory_item_id TEXT, status TEXT NOT NULL,
 FOREIGN KEY(page_id) REFERENCES html_pages(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS html_parse_errors (
 id INTEGER PRIMARY KEY AUTOINCREMENT, run_id INTEGER NOT NULL, inventory_item_id TEXT,
 relative_path TEXT NOT NULL, error_type TEXT NOT NULL, message TEXT NOT NULL,
 FOREIGN KEY(run_id) REFERENCES html_parse_runs(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_html_pages_run_id ON html_pages(run_id);
CREATE INDEX IF NOT EXISTS idx_html_pages_inventory_item_id ON html_pages(inventory_item_id);
CREATE INDEX IF NOT EXISTS idx_html_pages_relative_path ON html_pages(relative_path);
CREATE INDEX IF NOT EXISTS idx_html_pages_parse_status ON html_pages(parse_status);
CREATE INDEX IF NOT EXISTS idx_html_headings_page_id ON html_headings(page_id);
CREATE INDEX IF NOT EXISTS idx_html_images_page_id ON html_image_references(page_id);
CREATE INDEX IF NOT EXISTS idx_html_images_inventory_item_id ON html_image_references(referenced_inventory_item_id);
CREATE INDEX IF NOT EXISTS idx_html_images_status ON html_image_references(status);
CREATE INDEX IF NOT EXISTS idx_html_links_page_id ON html_link_references(page_id);
CREATE INDEX IF NOT EXISTS idx_html_links_inventory_item_id ON html_link_references(referenced_inventory_item_id);
CREATE INDEX IF NOT EXISTS idx_html_links_status ON html_link_references(status);
CREATE INDEX IF NOT EXISTS idx_html_errors_run_id ON html_parse_errors(run_id);
"""

TABLES = (
    "inventory_metadata",
    "inventory_statistics",
    "inventory_folders",
    "inventory_items",
    "inventory_extensions",
    "inventory_categories",
)

HTML_PARSER_TABLES = (
    "html_parse_runs", "html_pages", "html_headings", "html_image_references",
    "html_link_references", "html_parse_errors",
)
