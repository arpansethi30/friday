CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    context TEXT,
    user_input TEXT,
    response TEXT,
    embedding BLOB
);

CREATE TABLE system_events (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    event_type TEXT,
    event_data TEXT,
    context TEXT
);

CREATE TABLE command_history (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    command TEXT,
    output TEXT,
    exit_code INTEGER,
    context TEXT
);

CREATE TABLE app_usage (
    id INTEGER PRIMARY KEY,
    app_name TEXT,
    start_time DATETIME,
    end_time DATETIME,
    duration INTEGER
);

CREATE TABLE system_metrics (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    cpu_usage REAL,
    memory_usage REAL,
    battery_level INTEGER,
    temperature REAL
);

CREATE TABLE workflow_patterns (
    id INTEGER PRIMARY KEY,
    pattern_type TEXT,
    pattern_data TEXT,
    confidence REAL,
    occurrence_count INTEGER,
    last_seen DATETIME,
    success_rate REAL
);

CREATE TABLE system_predictions (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    metric_type TEXT,
    predicted_value REAL,
    actual_value REAL,
    accuracy REAL
);

CREATE TABLE learning_events (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    event_type TEXT,
    context TEXT,
    outcome TEXT,
    confidence REAL
);

CREATE TABLE optimization_history (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    optimization_type TEXT,
    initial_state TEXT,
    final_state TEXT,
    improvement_metric REAL
);

CREATE TABLE health_metrics (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    screen_time INTEGER,
    break_duration INTEGER,
    posture_alerts INTEGER,
    eye_strain_level REAL
);

CREATE TABLE project_activities (
    id INTEGER PRIMARY KEY,
    project_path TEXT,
    git_status TEXT,
    last_commit TEXT,
    open_issues INTEGER,
    pending_prs INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE schedule_events (
    id INTEGER PRIMARY KEY,
    event_type TEXT,
    start_time DATETIME,
    end_time DATETIME,
    context TEXT,
    preparation_status TEXT,
    notes TEXT
);

CREATE TABLE system_profiles (
    id INTEGER PRIMARY KEY,
    profile_name TEXT,
    display_config TEXT,
    audio_config TEXT,
    network_config TEXT,
    focus_settings TEXT,
    performance_settings TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);