"""
Configuration settings cho data pulling module.

Dễ dàng tùy chỉnh cơ chế pulling mà không cần sửa code.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataConfig:
    """Configuration cho VN30 data pulling."""

    # Time range
    start_date: str = "2023-01-01"
    end_date: str = "2025-12-31"

    # Data source
    data_source: str = "VCI"  # 'VCI' (Vietcap) hoặc 'TCBS'

    # Rate limiting
    sleep_between_calls: float = 0.6  # seconds

    # Output directory
    output_dir: Path = Path("data")

    # VN30 tickers list
    tickers: list[str] = None

    def __post_init__(self):
        """Initialize tickers if not provided."""
        if self.tickers is None:
            self.tickers = [
                "ACB", "BCM", "BID", "BVH", "CTG", "FPT", "GAS", "GVR", "HDB", "HPG",
                "MBB", "MSN", "MWG", "PLX", "POW", "SAB", "SHB", "SSB", "SSI", "STB",
                "TCB", "TPB", "VCB", "VHM", "VIB", "VIC", "VJC", "VNM", "VPB", "VRE",
            ]


# Default configuration
DEFAULT_CONFIG = DataConfig()


def get_config() -> DataConfig:
    """Get default configuration."""
    return DEFAULT_CONFIG


def create_custom_config(
    start_date: str = "2023-01-01",
    end_date: str = "2025-12-31",
    tickers: list[str] = None,
    data_source: str = "VCI",
    sleep_between_calls: float = 0.6,
    output_dir: str = "data",
) -> DataConfig:
    """Tạo custom configuration.

    Args:
        start_date: Ngày bắt đầu (YYYY-MM-DD)
        end_date: Ngày kết thúc (YYYY-MM-DD)
        tickers: Danh sách tickers (default: VN30)
        data_source: 'VCI' hoặc 'TCBS'
        sleep_between_calls: Delay giữa API calls (seconds)
        output_dir: Thư mục output

    Returns:
        DataConfig instance
    """
    return DataConfig(
        start_date=start_date,
        end_date=end_date,
        tickers=tickers,
        data_source=data_source,
        sleep_between_calls=sleep_between_calls,
        output_dir=Path(output_dir),
    )
