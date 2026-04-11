# Project Structure Guide

## Overview
This document describes the complete project structure for the Multi-Agent Trading Framework thesis research project.

## Root Level Files

### Project Documentation
- **README.md** - Main project overview and setup instructions
- **DEVELOPMENT.md** - Development workflow and guidelines
- **CLAUDE.md** - Claude Code configuration and context
- **PROJECT_STRUCTURE.md** - This file

### Configuration
- **.gitignore** - Git ignore patterns
- **.claudeignore** - Claude Code context ignore patterns
- **.env.example** - Environment variable template
- **Makefile** - Common development commands

### Python Project Files
- **pyproject.toml** - Python project configuration (dependencies, tools)
- **requirements.txt** - Python dependencies list

---

## Directory Structure

### `/src/` - Source Code

The main application code organized by functionality:

```
src/
├── __init__.py              # Package initialization
├── README.md               # Source code documentation
├── agents/                 # Multi-agent system
│   └── .gitkeep
├── models/                 # ML/LLM models
│   └── .gitkeep
├── data/                   # Data processing
│   └── .gitkeep
├── trading/                # Trading strategies
│   └── .gitkeep
├── evaluation/             # Model evaluation
│   └── .gitkeep
└── utils/                  # Utility functions
    └── .gitkeep
```

**Key modules to develop:**
- `agents/base.py`, `agents/trading_agent.py` - Agent implementations
- `models/llm.py`, `models/knowledge_graph.py` - Model interfaces
- `data/loader.py`, `data/processor.py` - Data pipelines
- `trading/strategy.py`, `trading/portfolio.py` - Trading logic
- `evaluation/metrics.py`, `evaluation/backtester.py` - Evaluation tools

### `/tests/` - Test Suite

Comprehensive testing structure:

```
tests/
├── __init__.py             # Test package
├── conftest.py             # Pytest configuration & fixtures
├── unit/                   # Unit tests (one per module)
│   └── .gitkeep
├── integration/            # Integration tests
│   └── .gitkeep
└── fixtures/               # Test data and mocks
    └── .gitkeep
```

**Test organization:**
- `tests/unit/test_agents.py`, `test_models.py`, etc.
- `tests/integration/test_agent_coordination.py`, etc.
- `tests/fixtures/` - Shared test data

### `/research/` - Research Materials

Documentation of research findings and literature:

```
research/
├── README.md               # Research guide
├── notes/                  # Research analysis
│   ├── .gitkeep
│   ├── 2026-04-11-llm-knowledge-graphs.md
│   └── 2026-04-11-multi-agent-systems.md
├── findings/               # Key discoveries
│   └── .gitkeep
└── papers/                 # Reference papers (duplicated from document/)
    └── .gitkeep
```

**Guidelines:**
- One file per research topic
- Include date, source, and key points
- Link to relevant code implementations
- Cross-reference with papers in `document/paper/`

### `/data/` - Data Management

Data handling with strict organization:

```
data/
├── raw/                    # Original data (never modify)
│   └── .gitkeep
├── processed/              # Cleaned and processed data
│   └── .gitkeep
└── external/               # External data sources
    └── .gitkeep
```

**Rules:**
- Never commit large data files (use .gitignore)
- Keep data pipelines reproducible
- Document data sources and transformations
- Use CSV/Parquet for structured data

### `/docs/` - Documentation

Technical documentation and architecture decisions:

```
docs/
├── README.md               # Documentation overview
├── decisions/              # Architecture Decision Records
│   ├── .gitkeep
│   ├── 0001-use-langchain.md
│   └── 0002-knowledge-graph-backend.md
├── architecture/           # System architecture
│   └── .gitkeep
└── api/                    # API documentation
    └── .gitkeep
```

**ADR Template (decisions/):**
```markdown
# ADR-001: [Decision Title]

## Status
Accepted

## Context
[Problem description]

## Decision
[Solution chosen]

## Consequences
[Tradeoffs and impacts]
```

### `/notebooks/` - Jupyter Notebooks

Exploratory and analysis notebooks:

```
notebooks/
├── .gitkeep
├── 01-eda.ipynb            # Exploratory data analysis
├── 02-model-experiments.ipynb
└── 03-strategy-backtest.ipynb
```

### `/config/` - Configuration Files

Application and experiment configurations:

```
config/
├── .gitkeep
├── config.example.yaml     # Example configuration
├── development.yaml        # Dev environment config
├── testing.yaml            # Test environment config
└── production.yaml         # Production config (don't commit secrets)
```

### `/logs/` - Application Logs

Runtime logs (never commit):

```
logs/
├── .gitkeep
├── app.log                 # Main application log
└── trading.log             # Trading system log
```

### `/document/` - Thesis Documents

Thesis-related materials:

```
document/
├── Luận_văn.pdf            # Thesis document
├── paper/                  # Reference papers
│   ├── 2412.20138v7.pdf
│   ├── NeurIPS-2020-RAG.pdf
│   └── PanEtAl2023-LLM-KG.pdf
└── slides/                 # Presentation materials
```

---

## File Organization Rules

### Python Modules

Each module should follow this structure:

```python
# module_name.py

"""
Module docstring explaining purpose and usage.

Example:
    How to use this module
"""

from typing import Type
import logging

logger = logging.getLogger(__name__)


class MyClass:
    """Class docstring."""
    
    def method(self, param: str) -> int:
        """Method docstring."""
        pass


def standalone_function(param: str) -> int:
    """Function docstring."""
    pass
```

### Test Files

```python
# tests/unit/test_module_name.py

import pytest
from src.module_name import MyClass, standalone_function


class TestMyClass:
    def setup_method(self):
        """Setup for each test."""
        self.obj = MyClass()
    
    def test_method_happy_path(self):
        """Test normal operation."""
        assert self.obj.method("input") == expected


class TestStandaloneFunction:
    def test_function_with_valid_input(self):
        """Test function with valid input."""
        assert standalone_function("input") == expected
```

### Documentation Files

Use Markdown with clear structure:

```markdown
# Title

## Section 1
Description and details

## Section 2
- Bullet point
- Another point

## References
- [Link](url)
```

---

## Development Workflow

### Before Starting

1. **Read documentation**: README.md, DEVELOPMENT.md, CLAUDE.md
2. **Setup environment**: `make dev-install`
3. **Run tests**: `make test` should pass

### When Adding Features

1. **Create feature branch**: `git checkout -b feature/description`
2. **Add tests first**: Write in `tests/unit/` or `tests/integration/`
3. **Implement feature**: Code in `src/`
4. **Document changes**: Update relevant README/docs
5. **Run all checks**: `make format && make lint && make test`
6. **Commit and push**: Clear commit messages

### When Adding Research

1. **Create research note**: `research/notes/YYYY-MM-DD-topic.md`
2. **Document findings**: Summary, key points, references
3. **Link to code**: Reference implementations in `src/`
4. **Update research README**: Add to navigation

### When Making Architecture Decisions

1. **Create ADR**: `docs/decisions/XXXX-decision.md`
2. **Document context**: Why this decision matters
3. **Explain choice**: Rationale and alternatives considered
4. **Record consequences**: Tradeoffs and impacts

---

## Important Notes

### What Goes Where

| Item | Location | Status |
|------|----------|--------|
| Source code | `src/` | Track |
| Unit tests | `tests/unit/` | Track |
| Data files | `data/raw/` | Don't track |
| Notebooks | `notebooks/` | Track |
| Research notes | `research/notes/` | Track |
| Configuration | `.env` | Don't track |
| Logs | `logs/` | Don't track |
| Secrets | Don't commit | Never |

### Naming Conventions

- **Directories**: `lowercase_with_underscores`
- **Python files**: `lowercase_with_underscores.py`
- **Classes**: `PascalCase`
- **Functions/variables**: `lowercase_with_underscores`
- **Constants**: `UPPERCASE_WITH_UNDERSCORES`
- **Git branches**: `feature/description` or `fix/description`
- **Commits**: `type: brief description`

### Helpful Commands

```bash
make help          # List all available commands
make install       # Install dependencies
make test          # Run tests with coverage
make format        # Auto-format code
make lint          # Check code style
make clean         # Clean generated files
```

---

## Checklist for New Developers

- [ ] Clone repository
- [ ] Read README.md
- [ ] Read DEVELOPMENT.md
- [ ] Read CLAUDE.md
- [ ] Run `make dev-install`
- [ ] Run `make test` (should pass)
- [ ] Create feature branch
- [ ] Understand this file (PROJECT_STRUCTURE.md)
- [ ] Ready to start development!

---

**Last Updated**: 2026-04-11
**Maintained by**: Nguyễn Thị Quý
