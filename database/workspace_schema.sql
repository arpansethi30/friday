CREATE TABLE workspace_states (
    id INTEGER PRIMARY KEY,
    name TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    apps_state JSON,
    terminal_state JSON,
    window_layout JSON,
    project_context JSON,
    success_metric FLOAT,
    last_used DATETIME,
    use_count INTEGER DEFAULT 1
);

CREATE TABLE workspace_transitions (
    id INTEGER PRIMARY KEY,
    from_workspace_id INTEGER,
    to_workspace_id INTEGER,
    transition_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    success_rate FLOAT,
    FOREIGN KEY (from_workspace_id) REFERENCES workspace_states(id),
    FOREIGN KEY (to_workspace_id) REFERENCES workspace_states(id)
);

CREATE TABLE workspace_metrics (
    id INTEGER PRIMARY KEY,
    workspace_id INTEGER,
    metric_type TEXT,
    value FLOAT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    context JSON,
    FOREIGN KEY (workspace_id) REFERENCES workspace_states(id)
);

CREATE INDEX idx_workspace_name ON workspace_states(name);
CREATE INDEX idx_workspace_timestamp ON workspace_states(timestamp);
CREATE INDEX idx_workspace_success ON workspace_states(success_metric);
