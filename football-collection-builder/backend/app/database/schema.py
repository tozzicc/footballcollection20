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
-- image contexts are stored separately to keep existing references compatible
CREATE TABLE IF NOT EXISTS html_image_contexts (
 id INTEGER PRIMARY KEY AUTOINCREMENT, html_page_id INTEGER NOT NULL, image_reference_id INTEGER NOT NULL,
 reference_original TEXT NOT NULL, resolved_relative_path TEXT, dom_order INTEGER NOT NULL,
 container_type TEXT, context_text TEXT, caption_text TEXT, extraction_rule TEXT NOT NULL,
 confidence TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL,
 FOREIGN KEY(html_page_id) REFERENCES html_pages(id) ON DELETE CASCADE,
 FOREIGN KEY(image_reference_id) REFERENCES html_image_references(id) ON DELETE CASCADE,
 UNIQUE(html_page_id,image_reference_id)
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
CREATE INDEX IF NOT EXISTS idx_html_contexts_page_status ON html_image_contexts(html_page_id,status);
CREATE INDEX IF NOT EXISTS idx_html_contexts_reference ON html_image_contexts(image_reference_id);
CREATE INDEX IF NOT EXISTS idx_html_links_inventory_item_id ON html_link_references(referenced_inventory_item_id);
CREATE INDEX IF NOT EXISTS idx_html_links_status ON html_link_references(status);
CREATE INDEX IF NOT EXISTS idx_html_errors_run_id ON html_parse_errors(run_id);

CREATE TABLE IF NOT EXISTS image_parse_runs (
 id INTEGER PRIMARY KEY AUTOINCREMENT, workspace_path TEXT NOT NULL, started_at TEXT NOT NULL,
 finished_at TEXT, duration_ms INTEGER NOT NULL DEFAULT 0, status TEXT NOT NULL,
 total_images INTEGER NOT NULL DEFAULT 0, valid_images INTEGER NOT NULL DEFAULT 0,
 invalid_images INTEGER NOT NULL DEFAULT 0, referenced_images INTEGER NOT NULL DEFAULT 0,
 orphan_images INTEGER NOT NULL DEFAULT 0, broken_references INTEGER NOT NULL DEFAULT 0,
 html_audit_available INTEGER NOT NULL DEFAULT 0, total_size INTEGER NOT NULL DEFAULT 0,
 average_width REAL, average_height REAL, max_width INTEGER, max_height INTEGER, message TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS image_metadata (
 id INTEGER PRIMARY KEY AUTOINCREMENT, run_id INTEGER NOT NULL, inventory_item_id TEXT NOT NULL,
 relative_path TEXT NOT NULL, absolute_path TEXT NOT NULL, filename TEXT NOT NULL, extension TEXT NOT NULL,
 format TEXT, file_size INTEGER NOT NULL, width INTEGER, height INTEGER, aspect_ratio REAL, mode TEXT,
 has_alpha INTEGER NOT NULL, animated INTEGER NOT NULL, frame_count INTEGER NOT NULL, dpi_x REAL, dpi_y REAL,
 created_at TEXT, modified_at TEXT, readable INTEGER NOT NULL, valid_image INTEGER NOT NULL,
 validation_status TEXT NOT NULL, validation_message TEXT NOT NULL, reference_count INTEGER NOT NULL DEFAULT 0,
 reference_status TEXT NOT NULL, FOREIGN KEY(run_id) REFERENCES image_parse_runs(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS image_parse_errors (
 id INTEGER PRIMARY KEY AUTOINCREMENT, run_id INTEGER NOT NULL, inventory_item_id TEXT,
 relative_path TEXT NOT NULL, error_type TEXT NOT NULL, message TEXT NOT NULL,
 FOREIGN KEY(run_id) REFERENCES image_parse_runs(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_image_metadata_run_id ON image_metadata(run_id);
CREATE INDEX IF NOT EXISTS idx_image_metadata_inventory_item_id ON image_metadata(inventory_item_id);
CREATE INDEX IF NOT EXISTS idx_image_metadata_relative_path ON image_metadata(relative_path);
CREATE INDEX IF NOT EXISTS idx_image_metadata_extension ON image_metadata(extension);
CREATE INDEX IF NOT EXISTS idx_image_metadata_format ON image_metadata(format);
CREATE INDEX IF NOT EXISTS idx_image_metadata_valid_image ON image_metadata(valid_image);
CREATE INDEX IF NOT EXISTS idx_image_metadata_validation_status ON image_metadata(validation_status);
CREATE INDEX IF NOT EXISTS idx_image_metadata_width ON image_metadata(width);
CREATE INDEX IF NOT EXISTS idx_image_metadata_height ON image_metadata(height);
CREATE INDEX IF NOT EXISTS idx_image_errors_run_id ON image_parse_errors(run_id);

CREATE TABLE IF NOT EXISTS catalog_build_runs (
 id INTEGER PRIMARY KEY AUTOINCREMENT, started_at TEXT NOT NULL, finished_at TEXT,
 duration_ms INTEGER NOT NULL DEFAULT 0, status TEXT NOT NULL, countries INTEGER NOT NULL DEFAULT 0,
 teams INTEGER NOT NULL DEFAULT 0, collections INTEGER NOT NULL DEFAULT 0, items INTEGER NOT NULL DEFAULT 0,
 image_relations INTEGER NOT NULL DEFAULT 0, issues INTEGER NOT NULL DEFAULT 0, message TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS catalog_countries (
 id INTEGER PRIMARY KEY AUTOINCREMENT, build_run_id INTEGER NOT NULL, original_name TEXT NOT NULL,
 normalized_name TEXT NOT NULL, slug TEXT NOT NULL, relative_path TEXT NOT NULL,
 confidence TEXT NOT NULL, source TEXT NOT NULL, FOREIGN KEY(build_run_id) REFERENCES catalog_build_runs(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS catalog_teams (
 id INTEGER PRIMARY KEY AUTOINCREMENT, build_run_id INTEGER NOT NULL, country_id INTEGER,
 original_name TEXT NOT NULL, normalized_name TEXT NOT NULL, slug TEXT NOT NULL,
 relative_path TEXT NOT NULL, confidence TEXT NOT NULL, source TEXT NOT NULL,
 FOREIGN KEY(build_run_id) REFERENCES catalog_build_runs(id) ON DELETE CASCADE,
 FOREIGN KEY(country_id) REFERENCES catalog_countries(id) ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS catalog_collections (
 id INTEGER PRIMARY KEY AUTOINCREMENT, build_run_id INTEGER NOT NULL, team_id INTEGER NOT NULL,
 original_name TEXT NOT NULL, normalized_name TEXT NOT NULL, relative_path TEXT NOT NULL,
 classification TEXT NOT NULL, inclusion_month INTEGER, inclusion_year INTEGER, inclusion_batch INTEGER,
 confidence TEXT NOT NULL, source TEXT NOT NULL,
 FOREIGN KEY(build_run_id) REFERENCES catalog_build_runs(id) ON DELETE CASCADE,
 FOREIGN KEY(team_id) REFERENCES catalog_teams(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS catalog_items (
 id INTEGER PRIMARY KEY AUTOINCREMENT, build_run_id INTEGER NOT NULL, team_id INTEGER NOT NULL,
 collection_id INTEGER, source_page_id INTEGER, original_title TEXT NOT NULL, title TEXT NOT NULL,
 relative_path TEXT NOT NULL, slug TEXT NOT NULL, item_type TEXT NOT NULL, confidence TEXT NOT NULL, source TEXT NOT NULL,
 FOREIGN KEY(build_run_id) REFERENCES catalog_build_runs(id) ON DELETE CASCADE,
 FOREIGN KEY(team_id) REFERENCES catalog_teams(id) ON DELETE CASCADE,
 FOREIGN KEY(collection_id) REFERENCES catalog_collections(id) ON DELETE SET NULL,
 FOREIGN KEY(source_page_id) REFERENCES html_pages(id) ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS catalog_item_images (
 id INTEGER PRIMARY KEY AUTOINCREMENT, build_run_id INTEGER NOT NULL, catalog_item_id INTEGER NOT NULL,
 image_metadata_id INTEGER NOT NULL, source_page_id INTEGER, reference_original TEXT NOT NULL,
 relative_path TEXT NOT NULL, display_order INTEGER, alt_text TEXT, is_primary_candidate INTEGER NOT NULL DEFAULT 0,
 FOREIGN KEY(build_run_id) REFERENCES catalog_build_runs(id) ON DELETE CASCADE,
 FOREIGN KEY(catalog_item_id) REFERENCES catalog_items(id) ON DELETE CASCADE,
 FOREIGN KEY(image_metadata_id) REFERENCES image_metadata(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS catalog_inferences (
 id INTEGER PRIMARY KEY AUTOINCREMENT, build_run_id INTEGER NOT NULL, entity_type TEXT NOT NULL,
 entity_id INTEGER NOT NULL, field TEXT NOT NULL, value TEXT NOT NULL, source TEXT NOT NULL,
 source_reference TEXT, confidence TEXT NOT NULL, reason TEXT NOT NULL,
 FOREIGN KEY(build_run_id) REFERENCES catalog_build_runs(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS catalog_issues (
 id INTEGER PRIMARY KEY AUTOINCREMENT, build_run_id INTEGER NOT NULL, issue_type TEXT NOT NULL,
 severity TEXT NOT NULL, entity_type TEXT NOT NULL, entity_id INTEGER, relative_path TEXT,
 message TEXT NOT NULL, created_at TEXT NOT NULL,
 FOREIGN KEY(build_run_id) REFERENCES catalog_build_runs(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_catalog_countries_normalized_name ON catalog_countries(normalized_name);
CREATE INDEX IF NOT EXISTS idx_catalog_countries_slug ON catalog_countries(slug);
CREATE INDEX IF NOT EXISTS idx_catalog_countries_relative_path ON catalog_countries(relative_path);
CREATE INDEX IF NOT EXISTS idx_catalog_teams_country_id ON catalog_teams(country_id);
CREATE INDEX IF NOT EXISTS idx_catalog_teams_normalized_name ON catalog_teams(normalized_name);
CREATE INDEX IF NOT EXISTS idx_catalog_teams_slug ON catalog_teams(slug);
CREATE INDEX IF NOT EXISTS idx_catalog_teams_relative_path ON catalog_teams(relative_path);
CREATE INDEX IF NOT EXISTS idx_catalog_teams_confidence ON catalog_teams(confidence);
CREATE INDEX IF NOT EXISTS idx_catalog_collections_team_id ON catalog_collections(team_id);
CREATE INDEX IF NOT EXISTS idx_catalog_collections_relative_path ON catalog_collections(relative_path);
CREATE INDEX IF NOT EXISTS idx_catalog_items_team_id ON catalog_items(team_id);
CREATE INDEX IF NOT EXISTS idx_catalog_items_collection_id ON catalog_items(collection_id);
CREATE INDEX IF NOT EXISTS idx_catalog_items_source_page_id ON catalog_items(source_page_id);
CREATE INDEX IF NOT EXISTS idx_catalog_items_relative_path ON catalog_items(relative_path);
CREATE INDEX IF NOT EXISTS idx_catalog_items_item_type ON catalog_items(item_type);
CREATE INDEX IF NOT EXISTS idx_catalog_items_confidence ON catalog_items(confidence);
CREATE INDEX IF NOT EXISTS idx_catalog_item_images_item_id ON catalog_item_images(catalog_item_id);
CREATE INDEX IF NOT EXISTS idx_catalog_item_images_source_page_id ON catalog_item_images(source_page_id);
CREATE INDEX IF NOT EXISTS idx_catalog_issues_type ON catalog_issues(issue_type);
CREATE INDEX IF NOT EXISTS idx_catalog_issues_severity ON catalog_issues(severity);

CREATE TABLE IF NOT EXISTS catalog_quality_runs (
 id INTEGER PRIMARY KEY AUTOINCREMENT, catalog_build_run_id INTEGER NOT NULL, started_at TEXT NOT NULL,
 finished_at TEXT, duration_ms INTEGER NOT NULL DEFAULT 0, status TEXT NOT NULL,
 total_issues INTEGER NOT NULL DEFAULT 0, auto_resolved INTEGER NOT NULL DEFAULT 0,
 review_required INTEGER NOT NULL DEFAULT 0, quality_score REAL NOT NULL DEFAULT 0, message TEXT NOT NULL,
 FOREIGN KEY(catalog_build_run_id) REFERENCES catalog_build_runs(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS catalog_issue_assessments (
 id INTEGER PRIMARY KEY AUTOINCREMENT, quality_run_id INTEGER NOT NULL, issue_id INTEGER NOT NULL,
 resolution_status TEXT NOT NULL, pattern TEXT NOT NULL, evidence TEXT NOT NULL, reason TEXT NOT NULL,
 FOREIGN KEY(quality_run_id) REFERENCES catalog_quality_runs(id) ON DELETE CASCADE,
 FOREIGN KEY(issue_id) REFERENCES catalog_issues(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS catalog_resolutions (
 id INTEGER PRIMARY KEY AUTOINCREMENT, quality_run_id INTEGER NOT NULL, issue_id INTEGER NOT NULL,
 resolution_type TEXT NOT NULL, rule_code TEXT NOT NULL, previous_value TEXT,
 resolved_value TEXT, confidence TEXT NOT NULL, evidence TEXT NOT NULL, reason TEXT NOT NULL,
 created_at TEXT NOT NULL, FOREIGN KEY(quality_run_id) REFERENCES catalog_quality_runs(id) ON DELETE CASCADE,
 FOREIGN KEY(issue_id) REFERENCES catalog_issues(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_catalog_quality_runs_build ON catalog_quality_runs(catalog_build_run_id);
CREATE INDEX IF NOT EXISTS idx_catalog_assessments_run ON catalog_issue_assessments(quality_run_id);
CREATE INDEX IF NOT EXISTS idx_catalog_assessments_issue ON catalog_issue_assessments(issue_id);
CREATE INDEX IF NOT EXISTS idx_catalog_assessments_status ON catalog_issue_assessments(resolution_status);
CREATE INDEX IF NOT EXISTS idx_catalog_resolutions_run ON catalog_resolutions(quality_run_id);
CREATE INDEX IF NOT EXISTS idx_catalog_resolutions_issue ON catalog_resolutions(issue_id);
CREATE INDEX IF NOT EXISTS idx_catalog_resolutions_rule ON catalog_resolutions(rule_code);
CREATE INDEX IF NOT EXISTS idx_catalog_resolutions_type ON catalog_resolutions(resolution_type);
CREATE INDEX IF NOT EXISTS idx_catalog_resolutions_confidence ON catalog_resolutions(confidence);

CREATE TABLE IF NOT EXISTS catalog_stable_keys (
 id INTEGER PRIMARY KEY AUTOINCREMENT, build_run_id INTEGER NOT NULL, entity_type TEXT NOT NULL,
 entity_id INTEGER NOT NULL, stable_key TEXT NOT NULL,
 FOREIGN KEY(build_run_id) REFERENCES catalog_build_runs(id) ON DELETE CASCADE,
 UNIQUE(build_run_id,entity_type,entity_id), UNIQUE(build_run_id,entity_type,stable_key)
);
CREATE INDEX IF NOT EXISTS idx_catalog_stable_key_lookup ON catalog_stable_keys(entity_type,stable_key);

CREATE TABLE IF NOT EXISTS catalog_manual_reviews (
 id INTEGER PRIMARY KEY AUTOINCREMENT, issue_stable_key TEXT NOT NULL, issue_id INTEGER,
 quality_run_id INTEGER NOT NULL, original_build_run_id INTEGER NOT NULL, current_build_run_id INTEGER NOT NULL,
 review_type TEXT NOT NULL, status TEXT NOT NULL, entity_type TEXT NOT NULL,
 original_entity_id INTEGER, current_entity_id INTEGER, entity_stable_key TEXT NOT NULL,
 field_name TEXT, previous_value TEXT, resolved_value TEXT, target_stable_key TEXT,
 resolution_code TEXT NOT NULL, reason TEXT NOT NULL, notes TEXT, source TEXT NOT NULL DEFAULT 'manual',
 author TEXT NOT NULL DEFAULT 'local_user', reviewed_at TEXT NOT NULL, created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL, reverted_at TEXT, reconciliation_status TEXT NOT NULL DEFAULT 'matched',
 reconciled_at TEXT, reconciliation_message TEXT NOT NULL DEFAULT '',
 FOREIGN KEY(issue_id) REFERENCES catalog_issues(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_manual_reviews_issue ON catalog_manual_reviews(issue_id);
CREATE INDEX IF NOT EXISTS idx_manual_reviews_issue_key ON catalog_manual_reviews(issue_stable_key);
CREATE INDEX IF NOT EXISTS idx_manual_reviews_quality_run ON catalog_manual_reviews(quality_run_id);
CREATE INDEX IF NOT EXISTS idx_manual_reviews_status ON catalog_manual_reviews(status);
CREATE INDEX IF NOT EXISTS idx_manual_reviews_type ON catalog_manual_reviews(review_type);
CREATE INDEX IF NOT EXISTS idx_manual_reviews_entity ON catalog_manual_reviews(entity_type,entity_stable_key);
CREATE INDEX IF NOT EXISTS idx_manual_reviews_reviewed ON catalog_manual_reviews(reviewed_at);
CREATE INDEX IF NOT EXISTS idx_manual_reviews_reconciliation ON catalog_manual_reviews(reconciliation_status);

CREATE TABLE IF NOT EXISTS catalog_normalization_runs (
 id INTEGER PRIMARY KEY AUTOINCREMENT, catalog_build_id INTEGER NOT NULL, quality_run_id INTEGER,
 started_at TEXT NOT NULL, completed_at TEXT, status TEXT NOT NULL, rules_version TEXT NOT NULL,
 countries_processed INTEGER NOT NULL DEFAULT 0, teams_processed INTEGER NOT NULL DEFAULT 0,
 collections_processed INTEGER NOT NULL DEFAULT 0, items_processed INTEGER NOT NULL DEFAULT 0,
 normalized_count INTEGER NOT NULL DEFAULT 0, unchanged_count INTEGER NOT NULL DEFAULT 0,
 review_required_count INTEGER NOT NULL DEFAULT 0, overridden_count INTEGER NOT NULL DEFAULT 0,
 duration_ms INTEGER NOT NULL DEFAULT 0, error_message TEXT,
 FOREIGN KEY(catalog_build_id) REFERENCES catalog_build_runs(id) ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS catalog_normalized_countries (
 id INTEGER PRIMARY KEY AUTOINCREMENT, normalization_run_id INTEGER NOT NULL, stable_key TEXT NOT NULL,
 source_entity_id INTEGER NOT NULL, original_name TEXT NOT NULL, original_path TEXT NOT NULL,
 normalized_name TEXT NOT NULL, display_name TEXT NOT NULL, slug TEXT NOT NULL,
 normalization_status TEXT NOT NULL, normalization_source TEXT NOT NULL, confidence TEXT NOT NULL,
 rule_codes TEXT NOT NULL DEFAULT '[]', created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
 FOREIGN KEY(normalization_run_id) REFERENCES catalog_normalization_runs(id) ON DELETE CASCADE,
 UNIQUE(normalization_run_id,stable_key)
);
CREATE TABLE IF NOT EXISTS catalog_normalized_teams (
 id INTEGER PRIMARY KEY AUTOINCREMENT, normalization_run_id INTEGER NOT NULL, stable_key TEXT NOT NULL,
 source_entity_id INTEGER NOT NULL, country_stable_key TEXT, original_name TEXT NOT NULL, original_path TEXT NOT NULL,
 normalized_name TEXT NOT NULL, display_name TEXT NOT NULL, slug TEXT NOT NULL,
 normalization_status TEXT NOT NULL, normalization_source TEXT NOT NULL, confidence TEXT NOT NULL,
 rule_codes TEXT NOT NULL DEFAULT '[]', created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
 FOREIGN KEY(normalization_run_id) REFERENCES catalog_normalization_runs(id) ON DELETE CASCADE,
 UNIQUE(normalization_run_id,stable_key)
);
CREATE TABLE IF NOT EXISTS catalog_normalized_collections (
 id INTEGER PRIMARY KEY AUTOINCREMENT, normalization_run_id INTEGER NOT NULL, stable_key TEXT NOT NULL,
 source_entity_id INTEGER NOT NULL, team_stable_key TEXT NOT NULL, country_stable_key TEXT,
 original_name TEXT NOT NULL, original_path TEXT NOT NULL, normalized_name TEXT NOT NULL,
 display_name TEXT NOT NULL, slug TEXT NOT NULL, collection_type TEXT NOT NULL,
 inclusion_period TEXT, inclusion_month INTEGER, inclusion_year INTEGER, inclusion_batch INTEGER,
 normalization_status TEXT NOT NULL, normalization_source TEXT NOT NULL, confidence TEXT NOT NULL,
 rule_codes TEXT NOT NULL DEFAULT '[]', created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
 FOREIGN KEY(normalization_run_id) REFERENCES catalog_normalization_runs(id) ON DELETE CASCADE,
 UNIQUE(normalization_run_id,stable_key)
);
CREATE TABLE IF NOT EXISTS catalog_normalized_items (
 id INTEGER PRIMARY KEY AUTOINCREMENT, normalization_run_id INTEGER NOT NULL, stable_key TEXT NOT NULL,
 source_entity_id INTEGER NOT NULL, team_stable_key TEXT NOT NULL, country_stable_key TEXT,
 collection_stable_key TEXT, original_title TEXT NOT NULL, original_path TEXT NOT NULL,
 normalized_title TEXT NOT NULL, display_title TEXT NOT NULL, slug TEXT NOT NULL, source_page TEXT NOT NULL,
 normalization_status TEXT NOT NULL, normalization_source TEXT NOT NULL, confidence TEXT NOT NULL,
 rule_codes TEXT NOT NULL DEFAULT '[]', created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
 FOREIGN KEY(normalization_run_id) REFERENCES catalog_normalization_runs(id) ON DELETE CASCADE,
 UNIQUE(normalization_run_id,stable_key)
);
CREATE TABLE IF NOT EXISTS catalog_normalization_events (
 id INTEGER PRIMARY KEY AUTOINCREMENT, normalization_run_id INTEGER NOT NULL, entity_type TEXT NOT NULL,
 entity_stable_key TEXT NOT NULL, rule_code TEXT NOT NULL, previous_value TEXT, resulting_value TEXT,
 status TEXT NOT NULL, source TEXT NOT NULL, confidence TEXT NOT NULL, message TEXT NOT NULL,
 created_at TEXT NOT NULL, FOREIGN KEY(normalization_run_id) REFERENCES catalog_normalization_runs(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_normalization_runs_latest ON catalog_normalization_runs(status,id DESC);
CREATE INDEX IF NOT EXISTS idx_normalized_countries_run_status ON catalog_normalized_countries(normalization_run_id,normalization_status);
CREATE INDEX IF NOT EXISTS idx_normalized_teams_run_country_status ON catalog_normalized_teams(normalization_run_id,country_stable_key,normalization_status);
CREATE INDEX IF NOT EXISTS idx_normalized_collections_run_team_status ON catalog_normalized_collections(normalization_run_id,team_stable_key,normalization_status);
CREATE INDEX IF NOT EXISTS idx_normalized_items_run_collection_status ON catalog_normalized_items(normalization_run_id,collection_stable_key,normalization_status);
CREATE INDEX IF NOT EXISTS idx_normalization_events_run_entity ON catalog_normalization_events(normalization_run_id,entity_type,entity_stable_key);
CREATE INDEX IF NOT EXISTS idx_normalization_events_rule ON catalog_normalization_events(rule_code);

CREATE TABLE IF NOT EXISTS catalog_view_runs (
 id INTEGER PRIMARY KEY AUTOINCREMENT, normalization_run_id INTEGER NOT NULL, started_at TEXT NOT NULL,
 completed_at TEXT, status TEXT NOT NULL, countries INTEGER NOT NULL DEFAULT 0,
 teams INTEGER NOT NULL DEFAULT 0, collections INTEGER NOT NULL DEFAULT 0, items INTEGER NOT NULL DEFAULT 0,
 media_relations INTEGER NOT NULL DEFAULT 0, ready INTEGER NOT NULL DEFAULT 0,
 review_required INTEGER NOT NULL DEFAULT 0, unavailable INTEGER NOT NULL DEFAULT 0,
 duration_ms INTEGER NOT NULL DEFAULT 0, schema_version TEXT NOT NULL, error_message TEXT,
 FOREIGN KEY(normalization_run_id) REFERENCES catalog_normalization_runs(id) ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS catalog_view_countries (
 id INTEGER PRIMARY KEY AUTOINCREMENT, view_run_id INTEGER NOT NULL, slug TEXT NOT NULL, name TEXT NOT NULL,
 original_name TEXT, teams_count INTEGER NOT NULL, collections_count INTEGER NOT NULL, items_count INTEGER NOT NULL,
 primary_media_key TEXT, public_status TEXT NOT NULL, FOREIGN KEY(view_run_id) REFERENCES catalog_view_runs(id) ON DELETE CASCADE,
 UNIQUE(view_run_id,slug)
);
CREATE TABLE IF NOT EXISTS catalog_view_teams (
 id INTEGER PRIMARY KEY AUTOINCREMENT, view_run_id INTEGER NOT NULL, slug TEXT NOT NULL, country_slug TEXT NOT NULL,
 name TEXT NOT NULL, original_name TEXT, collections_count INTEGER NOT NULL, items_count INTEGER NOT NULL,
 images_count INTEGER NOT NULL, primary_media_key TEXT, latest_inclusion_period TEXT,
 public_status TEXT NOT NULL, FOREIGN KEY(view_run_id) REFERENCES catalog_view_runs(id) ON DELETE CASCADE,
 UNIQUE(view_run_id,country_slug,slug)
);
CREATE TABLE IF NOT EXISTS catalog_view_collections (
 id INTEGER PRIMARY KEY AUTOINCREMENT, view_run_id INTEGER NOT NULL, slug TEXT NOT NULL,
 country_slug TEXT NOT NULL, team_slug TEXT NOT NULL, name TEXT NOT NULL, original_name TEXT,
 collection_type TEXT NOT NULL, inclusion_month INTEGER, inclusion_year INTEGER, inclusion_batch INTEGER,
 display_period TEXT, items_count INTEGER NOT NULL, images_count INTEGER NOT NULL,
 primary_media_key TEXT, public_status TEXT NOT NULL,
 FOREIGN KEY(view_run_id) REFERENCES catalog_view_runs(id) ON DELETE CASCADE,
 UNIQUE(view_run_id,country_slug,team_slug,slug)
);
CREATE TABLE IF NOT EXISTS catalog_view_items (
 id INTEGER PRIMARY KEY AUTOINCREMENT, view_run_id INTEGER NOT NULL, slug TEXT NOT NULL,
 country_slug TEXT NOT NULL, team_slug TEXT NOT NULL, collection_slug TEXT,
 title TEXT NOT NULL, original_title TEXT, item_type TEXT NOT NULL, source_page_reference TEXT,
 images_count INTEGER NOT NULL, primary_media_key TEXT, public_status TEXT NOT NULL,
 public_route TEXT NOT NULL, breadcrumbs_json TEXT NOT NULL, season_label TEXT,
 season_start_year INTEGER, season_end_year INTEGER, description TEXT, competition TEXT,
 FOREIGN KEY(view_run_id) REFERENCES catalog_view_runs(id) ON DELETE CASCADE,
 UNIQUE(view_run_id,public_route)
);
CREATE TABLE IF NOT EXISTS catalog_view_media (
 id INTEGER PRIMARY KEY AUTOINCREMENT, view_run_id INTEGER NOT NULL, item_public_route TEXT NOT NULL,
 public_media_key TEXT NOT NULL, inventory_reference TEXT, filename TEXT NOT NULL, extension TEXT NOT NULL,
 width INTEGER, height INTEGER, aspect_ratio REAL, format TEXT, alt_text TEXT,
 display_order INTEGER, is_primary_candidate INTEGER NOT NULL, media_source TEXT NOT NULL,
 availability_status TEXT NOT NULL, FOREIGN KEY(view_run_id) REFERENCES catalog_view_runs(id) ON DELETE CASCADE,
 UNIQUE(view_run_id,item_public_route,public_media_key)
);
CREATE INDEX IF NOT EXISTS idx_view_runs_latest ON catalog_view_runs(status,id DESC);
CREATE INDEX IF NOT EXISTS idx_view_countries_run_status ON catalog_view_countries(view_run_id,public_status);
CREATE INDEX IF NOT EXISTS idx_view_teams_run_country_slug ON catalog_view_teams(view_run_id,country_slug,slug);
CREATE INDEX IF NOT EXISTS idx_view_teams_status ON catalog_view_teams(view_run_id,public_status);
CREATE INDEX IF NOT EXISTS idx_view_collections_scope ON catalog_view_collections(view_run_id,country_slug,team_slug,slug);
CREATE INDEX IF NOT EXISTS idx_view_collections_period ON catalog_view_collections(view_run_id,inclusion_year DESC,inclusion_month DESC,inclusion_batch DESC);
CREATE INDEX IF NOT EXISTS idx_view_collections_status ON catalog_view_collections(view_run_id,public_status);
CREATE INDEX IF NOT EXISTS idx_view_items_scope ON catalog_view_items(view_run_id,country_slug,team_slug,collection_slug,slug);
CREATE INDEX IF NOT EXISTS idx_view_items_type_status ON catalog_view_items(view_run_id,item_type,public_status);
CREATE INDEX IF NOT EXISTS idx_view_media_item ON catalog_view_media(view_run_id,item_public_route,display_order);

CREATE TABLE IF NOT EXISTS media_build_runs (
 id INTEGER PRIMARY KEY AUTOINCREMENT, catalog_view_run_id INTEGER NOT NULL, started_at TEXT NOT NULL,
 completed_at TEXT, status TEXT NOT NULL, total_relations INTEGER NOT NULL DEFAULT 0,
 unique_assets INTEGER NOT NULL DEFAULT 0, available_assets INTEGER NOT NULL DEFAULT 0,
 unavailable_assets INTEGER NOT NULL DEFAULT 0, invalid_assets INTEGER NOT NULL DEFAULT 0,
 duration_ms INTEGER NOT NULL DEFAULT 0, schema_version TEXT NOT NULL, error_message TEXT,
 FOREIGN KEY(catalog_view_run_id) REFERENCES catalog_view_runs(id) ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS media_assets (
 id INTEGER PRIMARY KEY AUTOINCREMENT, media_run_id INTEGER NOT NULL, media_key TEXT NOT NULL,
 inventory_reference TEXT NOT NULL, relative_path TEXT NOT NULL, filename TEXT NOT NULL, extension TEXT NOT NULL,
 format TEXT, mime_type TEXT NOT NULL, file_size INTEGER NOT NULL, width INTEGER, height INTEGER,
 aspect_ratio REAL, valid INTEGER NOT NULL, available INTEGER NOT NULL, modified_at TEXT,
 created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
 FOREIGN KEY(media_run_id) REFERENCES media_build_runs(id) ON DELETE CASCADE,
 UNIQUE(media_run_id,media_key)
);
CREATE TABLE IF NOT EXISTS media_asset_relations (
 id INTEGER PRIMARY KEY AUTOINCREMENT, media_run_id INTEGER NOT NULL,
 view_public_media_key TEXT NOT NULL, media_key TEXT NOT NULL,
 FOREIGN KEY(media_run_id) REFERENCES media_build_runs(id) ON DELETE CASCADE,
 UNIQUE(media_run_id,view_public_media_key)
);
CREATE INDEX IF NOT EXISTS idx_media_runs_latest ON media_build_runs(status,id DESC);
CREATE INDEX IF NOT EXISTS idx_media_assets_key ON media_assets(media_key,media_run_id);
CREATE INDEX IF NOT EXISTS idx_media_assets_available ON media_assets(media_run_id,available,valid);
CREATE INDEX IF NOT EXISTS idx_media_assets_format ON media_assets(media_run_id,format);
CREATE INDEX IF NOT EXISTS idx_media_relations_view_key ON media_asset_relations(media_run_id,view_public_media_key);
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
    "html_link_references", "html_parse_errors", "html_image_contexts",
)

IMAGE_PARSER_TABLES = ("image_parse_runs", "image_metadata", "image_parse_errors")
