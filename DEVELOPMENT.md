# Development Guide

## Setup Development Environment

### 1. Clone and Setup
```bash
git clone <repo-url>
cd Caohoc2024_Thesis_Multi_Agent_Trading_Framework
make venv
source venv/bin/activate
make dev-install
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Verify Setup
```bash
make test
```

## Workflow

### Creating a New Feature

1. **Create a feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Develop with tests**
   - Write tests first in `tests/`
   - Implement feature in `src/`
   - Run tests: `make test`

3. **Code quality checks**
   ```bash
   make format    # Format code
   make lint      # Check style
   make typecheck # Check types (optional)
   ```

4. **Document your work**
   - Add docstrings to functions
   - Update relevant README files
   - Document any decisions in `docs/decisions/`

5. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: description of changes"
   git push origin feature/my-feature
   ```

6. **Create pull request**
   - Describe what changed and why
   - Reference any related issues
   - Ensure tests pass

### Adding Research Findings

1. Create a new file in `research/notes/`:
   ```bash
   touch research/notes/[date]-[topic].md
   ```

2. Use this template:
   ```markdown
   # [Research Topic]
   
   **Date**: 2026-04-11
   **Source**: [Paper/Article]
   **Author**: [Your Name]
   
   ## Summary
   [Brief summary of findings]
   
   ## Key Points
   - Point 1
   - Point 2
   
   ## Implementation Notes
   - Related code in `src/...`
   - Links to papers in `document/paper/`
   
   ## References
   - [Reference 1](link)
   ```

### Writing Tests

Tests should go in `tests/` and follow this structure:

```python
import pytest
from src.module import function_to_test

class TestMyFeature:
    def test_happy_path(self):
        """Test normal operation"""
        assert function_to_test(input) == expected_output
    
    def test_edge_case(self):
        """Test edge cases"""
        assert function_to_test(edge_input) == expected_output
    
    @pytest.mark.skip(reason="TODO: implement")
    def test_future_feature(self):
        pass
```

Run tests:
```bash
make test          # Full test with coverage
make test-fast     # Quick test without coverage
pytest tests/unit/ # Specific directory
```

## Code Standards

### Python Style
- Follow PEP 8
- Use type hints: `def function(param: Type) -> ReturnType:`
- Use meaningful variable names
- Maximum line length: 100 characters (see `pyproject.toml`)

### Documentation
- Add docstrings to all modules, classes, and functions
- Use Google-style docstrings:
  ```python
  def function(param: str) -> int:
      """Short description.
      
      Longer description if needed.
      
      Args:
          param: Description of parameter
          
      Returns:
          Description of return value
          
      Raises:
          ValueError: When validation fails
      """
  ```

### Commits
- Use meaningful commit messages
- Format: `type: description`
- Types: feat, fix, docs, test, refactor, style, chore
- Examples:
  - `feat: add multi-agent coordination system`
  - `fix: resolve knowledge graph connection issue`
  - `docs: update architecture documentation`

## Common Commands

```bash
# Development
make help          # Show all available commands
make install       # Install dependencies only
make dev-install   # Install with dev tools
make test          # Run tests with coverage
make test-fast     # Quick test run
make format        # Auto-format code
make lint          # Check code style
make clean         # Clean generated files

# Git workflow
git status         # Check changes
git diff           # See what changed
git log --oneline  # View recent commits
```

## Troubleshooting

### Import errors
- Ensure `src/` has `__init__.py`
- Check `PYTHONPATH` includes project root
- Try: `python -m pytest` instead of `pytest`

### Test failures
- Run with `-v` for verbose output: `pytest -v`
- Run specific test: `pytest tests/test_file.py::test_name`
- Check test fixtures in `tests/conftest.py`

### Code quality issues
- Auto-fix many issues: `make format`
- Check specific issues: `make lint`
- See detailed errors: `flake8 src/ --show-source`

## CI/CD

(To be added when setting up GitHub Actions or similar)

## Resources

- [PEP 8 Style Guide](https://pep8.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [Git Workflow](https://git-scm.com/book/en/v2)

---

For questions or issues, create a GitHub issue or contact the maintainer.
