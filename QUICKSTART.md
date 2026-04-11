# Quick Start Guide

Get started with development in 5 minutes.

## 1. Initial Setup (Run Once)

```bash
# Clone and navigate
git clone <repo-url>
cd Caohoc2024_Thesis_Multi_Agent_Trading_Framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Setup environment
cp .env.example .env
# Edit .env with your API keys if needed
```

## 2. Verify Setup

```bash
# Run tests to verify everything works
make test
```

## 3. Common Commands

```bash
# Run tests
make test-fast         # Quick test run
make test              # Full test with coverage

# Code quality
make format            # Auto-format code
make lint              # Check code style

# Cleaning
make clean             # Remove generated files

# Help
make help              # Show all available commands
```

## 4. Create Your First Feature

```bash
# Create a feature branch
git checkout -b feature/my-feature

# Create a test file
touch tests/unit/test_my_feature.py

# Write test first
# Then implement feature in src/

# Run tests
make test

# Format and check
make format && make lint

# Commit
git add .
git commit -m "feat: add my new feature"
```

## 5. Add Research Notes

```bash
# Create research note with today's date
touch research/notes/2026-04-11-my-research-topic.md

# Edit the file with your findings
# Include: source, summary, key points, implementation notes

# Commit
git add research/
git commit -m "research: document findings on my-research-topic"
```

## Key Files to Know

| File | Purpose |
|------|---------|
| README.md | Project overview |
| DEVELOPMENT.md | Detailed development guide |
| CLAUDE.md | Claude Code configuration |
| PROJECT_STRUCTURE.md | Complete directory guide |
| Makefile | Quick commands (make help) |
| pyproject.toml | Python dependencies |

## Directory Quick Reference

```
src/           → Write your code here
tests/         → Write tests here
research/      → Document findings here
data/          → Store datasets here (don't commit large files)
docs/          → Technical documentation
notebooks/     → Jupyter exploratory notebooks
config/        → Configuration files
```

## Development Cycle

1. **Plan**: Read related docs, create feature branch
2. **Test First**: Write test in `tests/`
3. **Implement**: Write code in `src/`
4. **Verify**: `make test` must pass
5. **Polish**: `make format && make lint`
6. **Commit**: Clear commit message
7. **Document**: Update docs if needed

## Useful Patterns

### Run Specific Test
```bash
pytest tests/unit/test_file.py::TestClass::test_method -v
```

### Debug Failing Test
```bash
pytest tests/unit/test_file.py::TestClass::test_method -v -s
```

### View Test Coverage
```bash
make test
# Open htmlcov/index.html in browser
```

### Format Specific File
```bash
black src/my_module.py
flake8 src/my_module.py
```

## Troubleshooting

### Tests fail with import error
```bash
# Make sure src/ has __init__.py
ls -la src/__init__.py

# Run with module flag
python -m pytest tests/
```

### Code style issues
```bash
# Auto-fix many issues
make format

# See detailed issues
make lint
```

### Virtual environment not working
```bash
# Deactivate and reactivate
deactivate
source venv/bin/activate

# Or recreate it
rm -rf venv
make venv
source venv/bin/activate
```

## Next Steps

1. ✅ Run `make dev-install`
2. ✅ Run `make test`
3. ✅ Read DEVELOPMENT.md for detailed guidance
4. ✅ Read PROJECT_STRUCTURE.md for file organization
5. ✅ Create your first feature branch
6. ✅ Start development!

## Getting Help

- **Claude Code help**: `/help`
- **Command help**: `make help`
- **Git issues**: See git documentation
- **Python errors**: Check error messages and search for solutions

---

**Ready to start?** Create a branch: `git checkout -b feature/my-feature`
