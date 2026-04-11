#!/usr/bin/env python
"""
Helper script để chạy VN30 data puller.

Cách sử dụng:
    python run_data_puller.py                    # Chạy với cấu hình mặc định
    python run_data_puller.py --help             # Xem tùy chọn
    python run_data_puller.py --prices-only      # Chỉ pull giá
    python run_data_puller.py --output custom    # Output folder khác
"""

import argparse
import logging
import sys
from pathlib import Path

# Setup path để import từ src
sys.path.insert(0, str(Path(__file__).parent))

from src.data.vn30_puller import Puller
from src.data.data_config import create_custom_config


def setup_logging(verbose: bool = False) -> None:
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    )


def main() -> int:
    """Parse arguments và chạy puller."""
    parser = argparse.ArgumentParser(
        description="Pull VN30 data từ vnstock phục vụ xây dựng Knowledge Graph",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  python run_data_puller.py                    # Full pipeline
  python run_data_puller.py --prices-only      # Chỉ OHLCV
  python run_data_puller.py --skip-prices      # Skip OHLCV
  python run_data_puller.py --output ./custom  # Custom folder
  python run_data_puller.py -v                 # Verbose logging
        """,
    )

    parser.add_argument(
        "--start-date",
        default="2023-01-01",
        help="Ngày bắt đầu (YYYY-MM-DD). Default: 2023-01-01",
    )

    parser.add_argument(
        "--end-date",
        default="2025-12-31",
        help="Ngày kết thúc (YYYY-MM-DD). Default: 2025-12-31",
    )

    parser.add_argument(
        "--tickers",
        nargs="+",
        help="Danh sách tickers (space-separated). Default: VN30",
    )

    parser.add_argument(
        "--output",
        default="data",
        help="Thư mục output. Default: data/",
    )

    parser.add_argument(
        "--source",
        choices=["VCI", "TCBS"],
        default="VCI",
        help="Data source. Default: VCI",
    )

    parser.add_argument(
        "--sleep",
        type=float,
        default=0.6,
        help="Delay giữa API calls (seconds). Default: 0.6",
    )

    # Component-specific flags
    parser.add_argument(
        "--prices-only",
        action="store_true",
        help="Chỉ pull OHLCV prices",
    )

    parser.add_argument(
        "--financials-only",
        action="store_true",
        help="Chỉ pull financial statements",
    )

    parser.add_argument(
        "--company-info-only",
        action="store_true",
        help="Chỉ pull company info",
    )

    parser.add_argument(
        "--news-only",
        action="store_true",
        help="Chỉ pull news & events",
    )

    parser.add_argument(
        "--kg-staging-only",
        action="store_true",
        help="Chỉ build KG staging files",
    )

    parser.add_argument(
        "--skip-prices",
        action="store_true",
        help="Skip OHLCV prices",
    )

    parser.add_argument(
        "--skip-financials",
        action="store_true",
        help="Skip financial statements",
    )

    parser.add_argument(
        "--skip-company-info",
        action="store_true",
        help="Skip company info",
    )

    parser.add_argument(
        "--skip-news",
        action="store_true",
        help="Skip news & events",
    )

    parser.add_argument(
        "--skip-kg-staging",
        action="store_true",
        help="Skip KG staging files",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose logging",
    )

    args = parser.parse_args()
    setup_logging(args.verbose)
    log = logging.getLogger("run_data_puller")

    # Create config
    config = create_custom_config(
        start_date=args.start_date,
        end_date=args.end_date,
        tickers=args.tickers,
        data_source=args.source,
        sleep_between_calls=args.sleep,
        output_dir=args.output,
    )

    log.info(f"Configuration: {config}")

    # Create puller
    puller = Puller(source=config.data_source, out_dir=config.output_dir)

    # Determine what to run
    only_flags = [
        args.prices_only,
        args.financials_only,
        args.company_info_only,
        args.news_only,
        args.kg_staging_only,
    ]
    only_mode = any(only_flags)

    if only_mode:
        # Run only specified components
        if args.prices_only or not (only_mode and not args.prices_only):
            puller.pull_prices()
        if args.financials_only or not (only_mode and not args.financials_only):
            puller.pull_financials()
        if args.company_info_only or not (only_mode and not args.company_info_only):
            puller.pull_company_info()
        if args.news_only or not (only_mode and not args.news_only):
            puller.pull_news()
        if args.kg_staging_only or not (only_mode and not args.kg_staging_only):
            puller.build_kg_staging()
    else:
        # Run all, but skip if requested
        if not args.skip_prices:
            puller.pull_prices()
        if not args.skip_financials:
            puller.pull_financials()
        if not args.skip_company_info:
            puller.pull_company_info()
        if not args.skip_news:
            puller.pull_news()
        if not args.skip_kg_staging:
            puller.build_kg_staging()

    log.info(f"Done. Data saved to: {config.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
