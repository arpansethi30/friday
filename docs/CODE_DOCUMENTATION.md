# Friday AI Assistant - Code Documentation

## Project Structure

```
friday/
├── src/                      # Source code
│   ├── context_manager.py    # Context handling
│   ├── system_monitor.py     # System monitoring
│   ├── workflow_manager.py   # Workflow automation
│   ├── project_manager.py    # Project handling
│   ├── schedule_manager.py   # Schedule management
│   ├── health_monitor.py     # Health tracking
│   ├── personality.py        # Personality engine
│   ├── voice_handler.py      # Voice processing
│   └── system_controller.py  # System control
├── database/                 # Database files
│   └── schema.sql           # Database schema
├── config/                   # Configuration
│   ├── config.json          # Main configuration
│   └── user_prefs.json      # User preferences
└── docs/                     # Documentation
    ├── ARCHITECTURE.md      # System architecture
    └── WORKFLOW.txt         # Workflow processes
```

## Core Components Documentation

### 1. Context Manager (`context_manager.py`)

```python
class ContextManager:
    """
    Manages system-wide context awareness and pattern recognition.

    Key Methods:
    - get_current_context(): Returns current system context
    - build_advanced_context(): Builds comprehensive context
    - monitor_patterns(): Continuously monitors and updates patterns

    Usage:
    context = ContextManager(db_path)
    current_context = await context.build_advanced_context()
    """
```

### 2. System Monitor (`system_monitor.py`)

```python
class SystemMonitor:
    """
    Handles system resource monitoring and optimization.

    Key Methods:
    - track_command(): Records command execution
    - log_system_metrics(): Records system metrics
    - monitor_system_advanced(): Advanced monitoring with predictions

    Usage:
    monitor = SystemMonitor(db_path)
    await monitor.monitor_system_advanced()
    """
```

### 3. Workflow Manager (`workflow_manager.py`)

```python
class WorkflowManager:
    """
    Manages development workflows and environments.

    Key Methods:
    - start_coding_session(): Sets up coding environment
    - track_work_patterns(): Monitors work patterns

    Usage:
    workflow = WorkflowManager(config)
    await workflow.start_coding_session()
    """
```

### 4. Project Manager (`project_manager.py`)

```python
class ProjectManager:
    """
    Handles project-specific operations and Git integration.

    Key Methods:
    - track_project(): Monitors project activity
    - manage_dev_environment(): Manages development setup

    Usage:
    project = ProjectManager(config)
    await project.track_project(path)
    """
```

## Database Schema Usage

### Conversations Table

```sql
conversations
- Used for: Storing interaction history
- Key fields: user_input, response, context, timestamp
- Access pattern: Recent first, context-based queries
```

### System Metrics Table

```sql
system_metrics
- Used for: Performance monitoring
- Key fields: cpu_usage, memory_usage, battery_level
- Access pattern: Time-series analysis, anomaly detection
```

## Configuration Guide

### Main Configuration (config.json)

```json
{
  "PERSONALITY_TRAITS": {
    // Defines assistant's personality characteristics
    // Adjust these values to modify behavior
  },
  "ADVANCED_FEATURES": {
    // Controls system automation and intelligence
    // Configure thresholds and behaviors
  }
}
```

## API Integration

### Ollama Integration

```python
"""
Model Interaction:
1. Initialize connection to Ollama
2. Send context-aware prompts
3. Process responses with personality adjustments
4. Maintain conversation context
"""
```

## Privacy & Security

### Data Protection

```python
"""
Implementation Guidelines:
1. All sensitive data stored in .gitignored files
2. Database encryption for personal data
3. Local-only processing
4. Secure configuration handling
"""
```

## Error Handling

### Graceful Degradation

```python
"""
Error Handling Strategy:
1. Detect and log errors
2. Maintain core functionality
3. Auto-recovery procedures
4. User notification system
"""
```

## Performance Optimization

### Resource Management

```python
"""
Optimization Guidelines:
1. Async operations for I/O-bound tasks
2. Efficient database queries
3. Memory-conscious data structures
4. Background task scheduling
"""
```

## Extension Points

### Custom Commands

```python
"""
Adding New Commands:
1. Define command pattern
2. Implement handler function
3. Register in voice_handler.py
4. Add context awareness
"""
```

### New Features

```python
"""
Feature Integration:
1. Create new module in src/
2. Update database schema if needed
3. Add configuration options
4. Integrate with context system
"""
```

## Testing Guidelines

### Unit Tests

```python
"""
Test Coverage:
1. Core functionality
2. Error handling
3. Context building
4. Pattern recognition
"""
```

## Maintenance

### Regular Tasks

```python
"""
Maintenance Schedule:
1. Log rotation: Daily
2. Pattern updates: Weekly
3. Database optimization: Monthly
4. Configuration review: Monthly
"""
```

## Best Practices

### Code Style

```python
"""
Development Guidelines:
1. Use async/await for I/O operations
2. Implement proper error handling
3. Document all public methods
4. Follow privacy guidelines
"""
```

### Performance

```python
"""
Performance Guidelines:
1. Monitor memory usage
2. Optimize database queries
3. Use efficient data structures
4. Implement caching where appropriate
"""
```
