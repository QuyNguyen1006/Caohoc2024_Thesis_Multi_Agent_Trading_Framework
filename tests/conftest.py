"""
Pytest configuration and shared fixtures for tests
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_data():
    """Provide sample data for tests"""
    return {
        "prices": [100, 105, 103, 108, 110],
        "volumes": [1000, 1100, 950, 1200, 1150],
    }


@pytest.fixture
def temp_config(tmp_path):
    """Provide temporary config file"""
    config_file = tmp_path / "config.yaml"
    config_file.write_text("debug: false\nlog_level: info\n")
    return config_file
