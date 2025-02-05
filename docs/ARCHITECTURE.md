# Friday AI Assistant Architecture

## Overview

Friday is an advanced AI assistant designed for local operation on M3 Max MacBooks, focusing on privacy, performance, and personalization. The system uses Llama2 through Ollama for its core intelligence.

## Core Components

### 1. Intelligence Layer

- **Model**: Llama2:13b via Ollama
- **Context Engine**: Maintains awareness of:
  - Time and schedule context
  - System state and resources
  - User activity and patterns
  - Project and task context
  - Environmental factors

### 2. Data Management

- **Local Storage**
  - SQLite database for structured data
  - File-based storage for configurations
  - Encrypted personal data storage
  - Local embedding storage
- **Privacy**
  - All data stays local
  - Sensitive data encryption
  - Gitignored personal files
  - Secure config management

### 3. Core Features

#### System Monitoring (`system_monitor.py`)

- Real-time resource tracking
- Performance optimization
- Anomaly detection
- Predictive maintenance
- Battery optimization

#### Context Management (`context_manager.py`)

- Time-aware context building
- Pattern recognition
- Activity tracking
- User preference learning
- Environment awareness

#### Workflow Management (`workflow_manager.py`)

- Development environment setup
- Project tracking
- Task automation
- Layout management
- Focus mode control

#### Health Monitoring (`health_monitor.py`)

- Screen time tracking
- Break reminders
- Posture monitoring
- Eye strain prevention
- Work-life balance

#### Schedule Management (`schedule_manager.py`)

- Calendar integration
- Meeting preparation
- Time optimization
- Task scheduling
- Break planning

#### Project Management (`project_manager.py`)

- Git integration
- Development workflow
- Environment setup
- Code analysis
- Project tracking

#### Personality Engine (`personality.py`)

- Adaptive responses
- Context-aware tone
- Learning from interactions
- User preference adaptation
- Personality consistency

#### System Control (`system_controller.py`)

- Resource optimization
- Environment management
- Focus mode control
- Performance profiles
- Background task management

### 4. Database Structure

```sql
Core Tables:
- conversations: User interactions
- system_events: System activities
- command_history: Terminal commands
- app_usage: Application usage
- system_metrics: Performance data

Learning Tables:
- workflow_patterns: Usage patterns
- system_predictions: Performance predictions
- learning_events: Training data
- optimization_history: System improvements

User Tables:
- health_metrics: Wellness data
- project_activities: Development tracking
- schedule_events: Calendar data
- system_profiles: Environment configs
```

## Workflow Process

1. **Initialization**

   ```
   Load configurations
   → Initialize components
   → Connect to Ollama
   → Start monitoring systems
   → Begin context tracking
   ```

2. **Interaction Flow**

   ```
   User Input
   → Context Building
   → Pattern Recognition
   → Response Generation
   → Action Execution
   → Learning Update
   ```

3. **Background Processes**

   ```
   System Monitoring
   → Pattern Analysis
   → Optimization Checks
   → Health Tracking
   → Schedule Management
   ```

4. **Learning Loop**
   ```
   Collect Interaction Data
   → Update Patterns
   → Adjust Preferences
   → Optimize Responses
   → Enhance Context
   ```

## Configuration

- `config.json`: Core settings
- `user_prefs.json`: User preferences
- `.env`: Private credentials
- `memory.json`: Learning data

## Security Measures

1. Local-only operation
2. Encrypted storage
3. Secure configurations
4. Privacy-focused design
5. Data isolation

## Extension Points

1. Custom command handlers
2. New monitoring modules
3. Additional automations
4. Integration plugins
5. Workflow templates

## Best Practices

1. Keep personal data private
2. Regular backups
3. Monitor resource usage
4. Update configurations
5. Review learned patterns

## Performance Considerations

1. M3 Max optimization
2. Memory management
3. Battery efficiency
4. Storage optimization
5. Process prioritization
