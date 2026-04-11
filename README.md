# Multi-Agent Trading Framework with LLMs and Knowledge Graphs

**Tiếng Việt**: Nghiên cứu mô hình ngôn ngữ lớn tăng cường đồ thị tri thức trong dự báo tài chính và lập luận đầu tư dựa trên ngữ cảnh

**English**: Research on Large Language Models enhanced with Knowledge Graphs for financial prediction and context-based investment reasoning

## Project Overview

This thesis research project develops a multi-agent trading framework that leverages:
- **Large Language Models (LLMs)** for reasoning and analysis
- **Knowledge Graphs (KGs)** for context-rich information representation
- **Multi-Agent Systems** for distributed decision-making in trading scenarios

## Directory Structure

```
.
├── src/                          # Source code
│   ├── agents/                   # Multi-agent system components
│   ├── models/                   # ML/LLM models and integrations
│   ├── data/                     # Data processing modules
│   ├── trading/                  # Trading logic and strategies
│   ├── evaluation/               # Performance evaluation tools
│   └── utils/                    # Utility functions
│
├── research/                     # Research materials
│   ├── notes/                    # Research notes and analysis
│   ├── findings/                 # Key findings
│   └── papers/                   # Reference papers
│
├── data/                         # Data directory
│   ├── raw/                      # Raw datasets
│   ├── processed/                # Processed data
│   └── external/                 # External data sources
│
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── fixtures/                 # Test data/fixtures
│
├── docs/                         # Documentation
│   ├── decisions/                # Architecture Decision Records
│   └── architecture/             # Architecture documentation
│
├── notebooks/                    # Jupyter notebooks for exploration
├── config/                       # Configuration files
├── document/                     # Thesis documents and papers
└── logs/                         # Application logs
```

## Quick Start

### Prerequisites
- Python 3.9+
- pip or conda

### Installation

1. Clone the repository
```bash
git clone <repo-url>
cd Caohoc2024_Thesis_Multi_Agent_Trading_Framework
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
pip install -e ".[dev]"  # Install development dependencies
```

4. Configure environment
```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

### Development

Run tests:
```bash
pytest
```

Format code:
```bash
black src/ tests/
```

Check code quality:
```bash
flake8 src/
```

## Project Structure Details

### `src/` - Source Code
- **agents/**: Multi-agent framework implementation
- **models/**: LLM and knowledge graph models
- **data/**: Data pipelines and processing
- **trading/**: Trading strategies and portfolio management
- **evaluation/**: Backtesting and performance metrics

See [src/README.md](src/README.md) for more details.

### `research/` - Research Materials
- **notes/**: Analysis and research findings
- **papers/**: Reference materials
- **findings/**: Key discoveries and insights

See [research/README.md](research/README.md) for more details.

### `tests/` - Testing
- Unit tests for individual components
- Integration tests for system interactions
- Test fixtures and mock data

### `docs/` - Documentation
- Architecture Decision Records (ADRs)
- System architecture diagrams
- API documentation

See [docs/README.md](docs/README.md) for more details.

## Configuration

### CLAUDE.md
Configuration file for Claude Code integration. Contains:
- Project context and goals
- Key directories and conventions
- Development workflow guidelines

### .claudeignore
Files and directories ignored by Claude Code during context selection.

### pyproject.toml
Python project configuration including:
- Dependencies
- Build system
- Tool configurations (pytest, mypy, black)

## Research Focus

This project investigates how to effectively combine:
1. **Large Language Models** for contextual reasoning about financial markets
2. **Knowledge Graphs** for structured representation of domain knowledge
3. **Multi-Agent Systems** for distributed trading decisions

Key areas of research:
- Agent communication and coordination
- Knowledge graph enrichment from LLM outputs
- Context-aware financial analysis
- Portfolio optimization with AI reasoning

## Contributing

1. Create a feature branch: `git checkout -b feature/description`
2. Make your changes and add tests
3. Run tests and linting: `pytest && black src/`
4. Commit with clear messages
5. Push to your branch and create a pull request
6. Update documentation as needed

## Documentation Standards

- Add research findings to `research/notes/`
- Document architectural decisions in `docs/decisions/` as ADRs
- Keep docstrings updated in source code
- Update this README when directory structure changes

## License

[Add license information]

## Contact

**Nguyễn Thị Quý** - Student ID: 24007795

---

**Last Updated**: 2026-04-11