"""
Data processing and management module.

Contains:
    - vn30_puller: Pull VN30 data từ vnstock
    - Utilities cho data loading, preprocessing, validation
"""

try:
    from src.data.vn30_puller import Puller, VN30_TICKERS
except ImportError:
    # vnstock có thể chưa được install
    Puller = None
    VN30_TICKERS = []

__all__ = ["Puller", "VN30_TICKERS"]
