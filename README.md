# Friday AI Assistant

An advanced AI assistant powered by Llama2, designed for privacy-focused local operation on M3 Max MacBooks. Friday provides intelligent workspace management, development assistance, and system optimization.

## Features

### Core Intelligence

- Local LLM processing using Ollama
- Context-aware responses
- Pattern recognition
- Personalized learning
- Privacy-focused design

### Development Support

- Project environment setup
- Git repository management
- Code analysis and suggestions
- Workflow optimization
- Terminal command assistance

### System Management

- Resource monitoring
- Performance optimization
- Battery management
- Focus mode control
- Workspace organization

### Health & Productivity

- Work/break cycle management
- Screen time monitoring
- Posture reminders
- Meeting preparation
- Schedule optimization

## Prerequisites

- M3 Max MacBook (optimized for Apple Silicon)
- Python 3.9+
- Ollama with Llama2 model
- SQLite3
- Git

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/friday.git
cd friday
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install Ollama and download Llama2:

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull Llama2 model
ollama pull llama2:13b
```

5. Configure the assistant:

```bash
# Copy example configuration
cp config/config.example.json config/config.json

# Edit configuration with your preferences
vim config/config.json
```

## Quick Start

1. Ensure Prerequisites:

```bash
# Check Python version (3.9+ required)
python3 --version

# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull Llama2 model
ollama pull llama2:13b
```

2. Setup Environment:

```bash
# Clone repository
git clone https://github.com/yourusername/friday.git
cd friday

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Unix/macOS
.\venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

3. Configure Friday:

```bash
# Copy example configs
cp config/config.example.json config/config.json
cp config/workspace_config.example.json config/workspace_config.json

# Edit configurations with your preferences
vim config/config.json
```

4. Initialize Database:

```bash
# Create database
sqlite3 database/friday.db < database/schema.sql
sqlite3 database/friday.db < database/workspace_schema.sql
```

5. Run Friday:

```bash
# Start the assistant
python friday.py
```

## Configuration

### Essential Settings

```json
{
  "OLLAMA_API": "http://localhost:11434/api/generate",
  "MODEL": "llama2:13b",
  "WAKE_WORD": "friday",
  "USER_PREFERENCES": {
    "name": "Your Name",
    "work_hours": "9:00-17:00"
  }
}
```

### Privacy Protection

- All data stays local
- Sensitive information in .gitignored files
- Encrypted storage for personal data
- Secure configuration management

## Usage

1. Start Friday:

```bash
python friday.py
```

2. Voice Commands:

```bash
"Friday, how's the system doing?"
"Friday, start coding mode"
"Friday, optimize performance"
```

3. Development Workflows:

```bash
"Friday, start project environment"
"Friday, track git changes"
"Friday, prepare for coding"
```

## Usage Examples

1. Basic Commands:

```bash
"Friday, how's the system doing?"
"Friday, start coding mode"
"Friday, optimize system"
```

2. Workspace Management:

```bash
"Friday, start backend project"
"Friday, save current workspace"
"Friday, restore last session"
```

3. System Control:

```bash
"Friday, optimize for performance"
"Friday, enable focus mode"
"Friday, start break timer"
```

## Troubleshooting

1. Database Issues:

```bash
# Reset database
rm database/friday.db
sqlite3 database/friday.db < database/schema.sql
sqlite3 database/friday.db < database/workspace_schema.sql
```

2. Model Issues:

```bash
# Restart Ollama
sudo systemctl restart ollama

# Verify model
ollama list
```

3. Permission Issues:

```bash
# Fix permissions
chmod +x friday.py
chmod -R 755 src/
```

## Monitoring Logs

```bash
# View logs
tail -f friday.log

# Check system metrics
sqlite3 database/friday.db "SELECT * FROM system_metrics ORDER BY timestamp DESC LIMIT 10;"
```

## Customization

1. Add Custom Commands:

- Edit `config/config.json`
- Add patterns to `VOICE_COMMANDS`
- Implement handlers in `voice_handler.py`

2. Modify Workspace Profiles:

- Edit `config/workspace_config.json`
- Add new workspace profiles
- Customize resource allocations

3. Adjust Learning Parameters:

- Modify `LEARNING_PARAMETERS` in config
- Tune pattern recognition settings
- Adjust adaptation rates

## Project Structure

```
friday/
├── src/                # Source code
├── database/           # Database files
├── config/            # Configuration
└── docs/             # Documentation
```

## Development

### Adding New Features

1. Create feature module in `src/`
2. Update database schema if needed
3. Add configuration options
4. Integrate with context system

### Running Tests

```bash
pytest tests/
```

## Memory & Learning

Friday learns from:

- Command patterns
- Work habits
- System usage
- User preferences
- Error patterns

## Security Considerations

1. Local Processing

- All computation done locally
- No cloud dependencies
- Private data stays on device

2. Data Protection

- Encrypted storage
- Secure configurations
- Access controls
- Git-ignored sensitive files

## Best Practices

1. Regular Maintenance

- Update configurations
- Review learned patterns
- Clean temporary files
- Optimize database

2. Performance

- Monitor resource usage
- Review system logs
- Update patterns
- Check optimization settings

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Ollama team for local LLM support
- Llama2 model from Meta
- Python community for essential libraries

## Support

- Review documentation in `/docs`
- Check known issues
- Create new issue for bugs
- Join community discussions

## Roadmap

- [ ] Enhanced context awareness
- [ ] Advanced pattern recognition
- [ ] Improved code analysis
- [ ] Extended automation capabilities
- [ ] Advanced health monitoring
