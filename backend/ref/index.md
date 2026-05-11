# Reference Documentation Index

## Quick Navigation

### For New Users
1. **[../README.md](../README.md)** - Start here for project overview
2. **[../QUICKSTART.md](../QUICKSTART.md)** - Setup and first run
3. **[architecture.md](./architecture.md)** - Understand the system design

### For Developers
1. **[development.md](./development.md)** - Development setup and workflow
2. **[api-reference.md](./api-reference.md)** - Complete API documentation
3. **[agents.md](./agents.md)** - AI agents deep dive

### For Integrators
1. **[gamma-api.md](./gamma-api.md)** - Gamma API integration guide
2. **[api-reference.md](./api-reference.md)** - Web API endpoints
3. **[../GAMMA_EXPORT_UPDATE.md](../GAMMA_EXPORT_UPDATE.md)** - Export feature details

---

## Documentation Structure

### Main Documentation

#### [CLAUDE.md](../CLAUDE.md)
**Master reference document for AI assistants**
- Quick links to all resources
- System architecture overview
- Key concepts and patterns
- Troubleshooting guide
- Development workflow

#### [README.md](../README.md)
**Project introduction**
- What the system does
- Key features
- Quick start example
- Basic usage

#### [QUICKSTART.md](../QUICKSTART.md)
**Step-by-step setup guide**
- Prerequisites
- Installation steps
- Configuration
- First run
- Output verification

---

### Reference Guides (`/ref`)

#### [architecture.md](./architecture.md)
**System design and architecture**
- Architecture diagram
- Component descriptions
- Data flow
- State management
- Performance characteristics
- Deployment considerations

**When to read**: Understanding how the system works at a high level

#### [api-reference.md](./api-reference.md)
**Complete API documentation**
- Gamma API client methods
- Gemini API client methods
- Image server functions
- Workflow state definitions
- Configuration settings
- File handlers
- CLI commands

**When to read**: Implementing features or integrating with the system

#### [agents.md](./agents.md)
**AI agents reference**
- P1: Gamma PPT blueprint generator
- P2: Deep analysis generator
- P3: Technical article generator
- P4: Speech script generator
- Agent execution flow
- Customization guide
- Performance tips

**When to read**: Understanding or modifying agent behavior

#### [development.md](./development.md)
**Development guide**
- Setup instructions
- Project structure
- Running the system
- Development workflow
- Testing guide
- Code style
- Troubleshooting
- Contributing

**When to read**: Setting up development environment or contributing

#### [gamma-api.md](./gamma-api.md)
**Gamma API integration**
- API details and authentication
- Two-step workflow
- Request parameters
- Implementation examples
- Error handling
- Best practices
- Migration notes

**When to read**: Working with Gamma API or troubleshooting PPT generation

---

### Update Logs

#### [GAMMA_API_UPDATE.md](../GAMMA_API_UPDATE.md)
**Gamma API fixes (2025-11-20)**
- Corrected API endpoint
- Fixed authentication header
- Implemented two-step flow
- Added required parameters
- Improved error handling

**When to read**: Understanding recent Gamma API changes

#### [GAMMA_EXPORT_UPDATE.md](../GAMMA_EXPORT_UPDATE.md)
**Export feature (2025-11-20)**
- Auto export to PDF/PPTX
- Download functionality
- Configuration options
- Testing results
- API response examples

**When to read**: Understanding export feature or configuring export format

---

### Configuration Files

#### [.env.example](../.env.example)
**Environment configuration template**
- Required API keys
- Server configuration
- Output settings
- Logging configuration

**When to read**: Setting up environment variables

#### [pyproject.toml](../pyproject.toml)
**Poetry dependency management**
- Python dependencies
- Development dependencies
- Project metadata

**When to read**: Adding dependencies or understanding requirements

---

### Prompt Templates (`/docs`)

#### [Prompt-P1.md](../docs/Prompt-P1.md)
**P1 Agent: Gamma PPT blueprint**
- Task: Generate Gamma API-compatible markdown
- Input: Paper + images + metadata
- Output: Markdown with `---` separators
- Format: Gamma API specifications

#### [Prompt-P2.md](../docs/Prompt-P2.md)
**P2 Agent: Deep analysis**
- Task: Generate comprehensive technical analysis
- Input: P1 markdown + original paper
- Output: 20-250 KB detailed document

#### [Prompt-P3.md](../docs/Prompt-P3.md)
**P3 Agent: Technical article**
- Task: Generate accessible article
- Input: P1 markdown + original paper
- Output: 3-10 KB medium-style article

#### [Prompt-P4.md](../docs/Prompt-P4.md)
**P4 Agent: Speech script**
- Task: Generate presentation script
- Input: P1 markdown + original paper
- Output: 9-10 KB conference talk script

---

## Documentation by Topic

### Getting Started
- [README.md](../README.md) - Overview
- [QUICKSTART.md](../QUICKSTART.md) - Setup guide
- [.env.example](../.env.example) - Configuration template

### Architecture & Design
- [architecture.md](./architecture.md) - System design
- [CLAUDE.md](../CLAUDE.md) - Architecture decisions

### API Integration
- [gamma-api.md](./gamma-api.md) - Gamma API
- [api-reference.md](./api-reference.md) - All APIs
- [GAMMA_API_UPDATE.md](../GAMMA_API_UPDATE.md) - Recent updates

### AI Agents
- [agents.md](./agents.md) - Agent guide
- [Prompt-P1.md](../docs/Prompt-P1.md) - P1 template
- [Prompt-P2.md](../docs/Prompt-P2.md) - P2 template
- [Prompt-P3.md](../docs/Prompt-P3.md) - P3 template
- [Prompt-P4.md](../docs/Prompt-P4.md) - P4 template

### Development
- [development.md](./development.md) - Dev guide
- [api-reference.md](./api-reference.md) - API reference
- [pyproject.toml](../pyproject.toml) - Dependencies

### Features
- [GAMMA_EXPORT_UPDATE.md](../GAMMA_EXPORT_UPDATE.md) - Export feature
- [architecture.md](./architecture.md) - All features

---

## Common Use Cases

### "I'm new to this project"
1. Read [README.md](../README.md) for overview
2. Follow [QUICKSTART.md](../QUICKSTART.md) to get running
3. Review [architecture.md](./architecture.md) to understand design
4. Check [CLAUDE.md](../CLAUDE.md) for quick reference

### "I want to modify agent behavior"
1. Read [agents.md](./agents.md) for agent overview
2. Check [Prompt-P*.md](../docs/) for prompt templates
3. Review [api-reference.md](./api-reference.md) for agent APIs
4. Follow [development.md](./development.md) for testing

### "I'm getting Gamma API errors"
1. Check [gamma-api.md](./gamma-api.md) for troubleshooting
2. Review [GAMMA_API_UPDATE.md](../GAMMA_API_UPDATE.md) for recent fixes
3. Verify [.env](../.env) configuration
4. See [CLAUDE.md](../CLAUDE.md) troubleshooting section

### "I want to add a new feature"
1. Read [development.md](./development.md) for workflow
2. Review [architecture.md](./architecture.md) for design patterns
3. Check [api-reference.md](./api-reference.md) for existing APIs
4. Follow contribution guidelines in [development.md](./development.md)

### "I need to deploy this"
1. Read [development.md](./development.md) deployment section
2. Review [architecture.md](./architecture.md) for requirements
3. Check [.env.example](../.env.example) for configuration
4. See API mode in [api-reference.md](./api-reference.md)

---

## Documentation Maintenance

### Last Updated
- **CLAUDE.md**: 2025-11-20
- **All ref/ docs**: 2025-11-20
- **GAMMA_EXPORT_UPDATE.md**: 2025-11-20
- **GAMMA_API_UPDATE.md**: 2025-11-20

### Update Process
When making changes to the system:
1. Update relevant code files
2. Update corresponding documentation
3. Add entry to update logs if significant
4. Update CLAUDE.md with new patterns
5. Update this index if structure changes

---

## Quick Reference

### File Locations
```
Project Root
├── CLAUDE.md              # Main reference
├── README.md              # Overview
├── QUICKSTART.md          # Setup guide
├── .env.example           # Config template
├── pyproject.toml         # Dependencies
├── GAMMA_API_UPDATE.md    # API fixes
├── GAMMA_EXPORT_UPDATE.md # Export feature
├── docs/                  # Prompt templates
│   ├── Prompt-P1.md
│   ├── Prompt-P2.md
│   ├── Prompt-P3.md
│   └── Prompt-P4.md
├── ref/                   # Reference docs
│   ├── index.md          # This file
│   ├── architecture.md   # System design
│   ├── api-reference.md  # API docs
│   ├── agents.md         # Agents guide
│   ├── development.md    # Dev guide
│   └── gamma-api.md      # Gamma integration
└── src/                   # Source code
    ├── agents/           # AI agents
    ├── api/              # Web API
    ├── cli/              # CLI
    ├── core/             # Workflow
    ├── services/         # External APIs
    └── utils/            # Utilities
```

### Key Commands
```bash
# Setup
poetry install
cp .env.example .env

# Run CLI
poetry run python -m src.cli.main process examples/2410.05779v3

# Run API
poetry run python -m src.api.main

# Test
poetry run pytest
poetry run pytest --cov=src

# Format
poetry run black src/
poetry run isort src/
poetry run flake8 src/
```

### Configuration
```env
# Required
GOOGLE_API_KEY=xxx
GAMMA_API_KEY=sk-gamma-xxx

# Optional
GAMMA_EXPORT_FORMAT=pdf
IMAGE_SERVER_PORT=8001
OUTPUT_DIR=./outputs
LOG_LEVEL=INFO
```

### Troubleshooting
- **401 Gamma Error**: Check auth header is `X-API-KEY`, not `Bearer`
- **Concurrent Update**: Parallel nodes must return `Dict`, not full state
- **Timeout**: Increase `max_wait_time` in workflow
- **Port in Use**: Change `IMAGE_SERVER_PORT` in .env

---

*This index is automatically maintained. Last updated: 2025-11-20*
