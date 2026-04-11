# Source Code

## Directory Structure

### agents/
Multi-agent system components
- Agent base classes
- Specialized trading agents
- Agent communication protocols

### models/
ML and LLM models
- Knowledge graph models
- LLM integrations
- Model utilities

### data/
Data processing and handling
- Data loaders
- Data preprocessing
- Data validation

### trading/
Trading system logic
- Strategy implementations
- Portfolio management
- Risk assessment

### evaluation/
Model and strategy evaluation
- Metrics and benchmarks
- Backtesting tools
- Performance analysis

### utils/
Utility functions
- Logging
- Configuration
- Common helpers

## Code Standards

- Use type hints for all functions
- Document complex logic
- Write unit tests for new features
- Follow PEP 8 style guide

## Getting Started with Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Run tests
pytest

# Run with linting
black src/
flake8 src/
```
