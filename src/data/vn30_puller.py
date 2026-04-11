"""
Pull dữ liệu VN30 (2023-2025) từ vnstock phục vụ xây dựng Financial Knowledge Graph.

Yêu cầu:
    pip install vnstock pandas tqdm

Cấu trúc output:
    data/
    ├── prices/                  # OHLCV daily theo từng mã
    │   ├── VCB.csv
    │   ├── VNM.csv
    │   └── ...
    ├── financials/
    │   ├── income_statement.csv     # Hợp nhất tất cả mã
    │   ├── balance_sheet.csv
    │   ├── cash_flow.csv
    │   └── ratios.csv
    ├── company_info/
    │   ├── overview.csv             # Tên, ngành, sàn, vốn hóa
    │   ├── shareholders.csv         # Cổ đông lớn -> dùng cho edge OWNS
    │   ├── officers.csv             # Ban lãnh đạo
    │   └── subsidiaries.csv         # Công ty con -> edge SUBSIDIARY_OF
    ├── news/
    │   └── news_<TICKER>.csv        # Tin tức + sự kiện theo mã
    └── kg_staging/                  # Đã pre-format cho Neo4j
        ├── nodes_company.csv
        ├── nodes_industry.csv
        ├── nodes_shareholder.csv
        ├── edges_belongs_to.csv     # Company -[BELONGS_TO]-> Industry
        ├── edges_owns.csv           # Shareholder -[OWNS {pct}]-> Company
        └── edges_subsidiary.csv     # Company -[SUBSIDIARY_OF]-> Company
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from tqdm import tqdm
from vnstock import Vnstock

# ---------------------------------------------------------------------------
# Cấu hình
# ---------------------------------------------------------------------------
START_DATE = "2023-01-01"
END_DATE = "2025-12-31"
DATA_SOURCE = "VCI"          # 'VCI' (Vietcap) hoặc 'TCBS'. VCI ổn định hơn cho fundamentals.
SLEEP_BETWEEN_CALLS = 0.6     # rate limit thân thiện
OUT_DIR = Path("data")

# Danh sách VN30 (cập nhật cuối 2024). Có thể thay bằng API list_index nếu muốn dynamic.
VN30_TICKERS = [
    "ACB", "BCM", "BID", "BVH", "CTG", "FPT", "GAS", "GVR", "HDB", "HPG",
    "MBB", "MSN", "MWG", "PLX", "POW", "SAB", "SHB", "SSB", "SSI", "STB",
    "TCB", "TPB", "VCB", "VHM", "VIB", "VIC", "VJC", "VNM", "VPB", "VRE",
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger("vn30_puller")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
@dataclass
class Puller:
    """
    Pull VN30 data từ vnstock và tạo staging files cho Knowledge Graph.

    Attributes:
        source: Data source ('VCI' hoặc 'TCBS')
        out_dir: Output directory để lưu data
    """

    source: str = DATA_SOURCE
    out_dir: Path = OUT_DIR

    def __post_init__(self) -> None:
        """Tạo các thư mục output."""
        for sub in ("prices", "financials", "company_info", "news", "kg_staging"):
            (self.out_dir / sub).mkdir(parents=True, exist_ok=True)

    def _stock(self, symbol: str):
        """Tạo stock object từ vnstock."""
        # Vnstock 3.x: factory pattern
        return Vnstock().stock(symbol=symbol, source=self.source)

    @staticmethod
    def _safe(fn, default=None, ctx: str = ""):
        """Bọc mọi call vnstock — log lỗi, không crash toàn pipeline."""
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001
            log.warning("Skip %s -> %s", ctx, exc)
            return default

    # ------------------------- 1. PRICES (OHLCV) ----------------------------
    def pull_prices(self) -> None:
        """Pull OHLCV daily data cho tất cả VN30 tickers."""
        log.info("== [1/4] Pulling OHLCV daily ==")
        for tkr in tqdm(VN30_TICKERS, desc="prices"):
            stock = self._stock(tkr)
            df = self._safe(
                lambda: stock.quote.history(
                    start=START_DATE, end=END_DATE, interval="1D"
                ),
                ctx=f"prices/{tkr}",
            )
            if df is not None and not df.empty:
                df["ticker"] = tkr
                df.to_csv(self.out_dir / "prices" / f"{tkr}.csv", index=False)
            time.sleep(SLEEP_BETWEEN_CALLS)

    # ------------------------- 2. FINANCIALS --------------------------------
    def pull_financials(self) -> None:
        """Pull financial statements (income, balance, cash flow, ratios) yearly."""
        log.info("== [2/4] Pulling financial statements (yearly) ==")
        income, balance, cash, ratios = [], [], [], []

        for tkr in tqdm(VN30_TICKERS, desc="financials"):
            stock = self._stock(tkr)
            fin = stock.finance

            i = self._safe(lambda: fin.income_statement(period="year", lang="vi"),
                           ctx=f"income/{tkr}")
            b = self._safe(lambda: fin.balance_sheet(period="year", lang="vi"),
                           ctx=f"balance/{tkr}")
            c = self._safe(lambda: fin.cash_flow(period="year"),
                           ctx=f"cashflow/{tkr}")
            r = self._safe(lambda: fin.ratio(period="year", lang="vi"),
                           ctx=f"ratio/{tkr}")

            for df, bucket in ((i, income), (b, balance), (c, cash), (r, ratios)):
                if df is not None and not df.empty:
                    df = df.copy()
                    df["ticker"] = tkr
                    bucket.append(df)

            time.sleep(SLEEP_BETWEEN_CALLS)

        mapping = {
            "income_statement.csv": income,
            "balance_sheet.csv": balance,
            "cash_flow.csv": cash,
            "ratios.csv": ratios,
        }
        for name, frames in mapping.items():
            if frames:
                pd.concat(frames, ignore_index=True).to_csv(
                    self.out_dir / "financials" / name, index=False
                )
                log.info("  saved %s (%d rows)", name, sum(len(f) for f in frames))

    # ------------------------- 3. COMPANY INFO ------------------------------
    def pull_company_info(self) -> None:
        """Pull company profile, shareholders, officers, và subsidiaries."""
        log.info("== [3/4] Pulling company profile / shareholders / subsidiaries ==")
        overviews, shareholders, officers, subs = [], [], [], []

        for tkr in tqdm(VN30_TICKERS, desc="company"):
            stock = self._stock(tkr)
            co = stock.company

            ov = self._safe(lambda: co.overview(),       ctx=f"overview/{tkr}")
            sh = self._safe(lambda: co.shareholders(),   ctx=f"shareholders/{tkr}")
            of = self._safe(lambda: co.officers(),       ctx=f"officers/{tkr}")
            sb = self._safe(lambda: co.subsidiaries(),   ctx=f"subs/{tkr}")

            for df, bucket in ((ov, overviews), (sh, shareholders),
                               (of, officers), (sb, subs)):
                if df is not None and not df.empty:
                    df = df.copy()
                    df["ticker"] = tkr
                    bucket.append(df)

            time.sleep(SLEEP_BETWEEN_CALLS)

        mapping = {
            "overview.csv": overviews,
            "shareholders.csv": shareholders,
            "officers.csv": officers,
            "subsidiaries.csv": subs,
        }
        for name, frames in mapping.items():
            if frames:
                pd.concat(frames, ignore_index=True).to_csv(
                    self.out_dir / "company_info" / name, index=False
                )
                log.info("  saved %s (%d rows)", name, sum(len(f) for f in frames))

    # ------------------------- 4. NEWS / EVENTS -----------------------------
    def pull_news(self) -> None:
        """Pull news và events cho từng ticker."""
        log.info("== [4/4] Pulling news & events ==")
        for tkr in tqdm(VN30_TICKERS, desc="news"):
            stock = self._stock(tkr)
            co = stock.company

            news_df = self._safe(lambda: co.news(),   ctx=f"news/{tkr}")
            evt_df  = self._safe(lambda: co.events(), ctx=f"events/{tkr}")

            frames = []
            if news_df is not None and not news_df.empty:
                news_df = news_df.copy()
                news_df["kind"] = "news"
                frames.append(news_df)
            if evt_df is not None and not evt_df.empty:
                evt_df = evt_df.copy()
                evt_df["kind"] = "event"
                frames.append(evt_df)

            if frames:
                merged = pd.concat(frames, ignore_index=True)
                merged["ticker"] = tkr
                merged.to_csv(self.out_dir / "news" / f"news_{tkr}.csv", index=False)

            time.sleep(SLEEP_BETWEEN_CALLS)

    # ------------------------- 5. KG STAGING --------------------------------
    def build_kg_staging(self) -> None:
        """Tạo file CSV nodes/edges sẵn sàng LOAD CSV vào Neo4j."""
        log.info("== [5/5] Building KG staging files ==")
        ci = self.out_dir / "company_info"
        kg = self.out_dir / "kg_staging"

        # ---- nodes_company ----
        ov_path = ci / "overview.csv"
        if ov_path.exists():
            ov = pd.read_csv(ov_path)
            cols = {c.lower(): c for c in ov.columns}
            company_nodes = pd.DataFrame({
                "ticker:ID(Company)": ov["ticker"],
                "name": ov.get(cols.get("short_name", "ticker"), ov["ticker"]),
                "exchange": ov.get(cols.get("exchange"), ""),
                "industry": ov.get(cols.get("industry"), ""),
                ":LABEL": "Company",
            })
            company_nodes.to_csv(kg / "nodes_company.csv", index=False)

            # ---- nodes_industry + edges BELONGS_TO ----
            if "industry" in cols:
                inds = ov[cols["industry"]].dropna().unique()
                pd.DataFrame({
                    "name:ID(Industry)": inds,
                    ":LABEL": "Industry",
                }).to_csv(kg / "nodes_industry.csv", index=False)

                pd.DataFrame({
                    ":START_ID(Company)": ov["ticker"],
                    ":END_ID(Industry)": ov[cols["industry"]],
                    ":TYPE": "BELONGS_TO",
                }).dropna().to_csv(kg / "edges_belongs_to.csv", index=False)

        # ---- shareholders -> nodes + edges OWNS ----
        sh_path = ci / "shareholders.csv"
        if sh_path.exists():
            sh = pd.read_csv(sh_path)
            cols = {c.lower(): c for c in sh.columns}
            name_col = cols.get("share_holder") or cols.get("shareholder") \
                       or cols.get("name") or list(sh.columns)[0]
            pct_col = cols.get("share_own_percent") or cols.get("percentage") \
                      or cols.get("ownership")

            holders = sh[name_col].dropna().unique()
            pd.DataFrame({
                "name:ID(Shareholder)": holders,
                ":LABEL": "Shareholder",
            }).to_csv(kg / "nodes_shareholder.csv", index=False)

            edges = pd.DataFrame({
                ":START_ID(Shareholder)": sh[name_col],
                ":END_ID(Company)": sh["ticker"],
                "pct:float": sh[pct_col] if pct_col else 0.0,
                ":TYPE": "OWNS",
            }).dropna(subset=[":START_ID(Shareholder)"])
            edges.to_csv(kg / "edges_owns.csv", index=False)

        # ---- subsidiaries -> edges SUBSIDIARY_OF ----
        sub_path = ci / "subsidiaries.csv"
        if sub_path.exists():
            sb = pd.read_csv(sub_path)
            cols = {c.lower(): c for c in sb.columns}
            sub_col = cols.get("sub_company_name") or cols.get("company_name") \
                      or cols.get("name") or list(sb.columns)[0]
            pd.DataFrame({
                ":START_ID(Company)": sb["ticker"],
                "subsidiary_name": sb[sub_col],
                ":TYPE": "HAS_SUBSIDIARY",
            }).to_csv(kg / "edges_subsidiary.csv", index=False)

        log.info("KG staging files written to %s", kg)

    # ------------------------- ORCHESTRATION --------------------------------
    def run_all(self) -> None:
        """Chạy toàn bộ pipeline pulling data."""
        self.pull_prices()
        self.pull_financials()
        self.pull_company_info()
        self.pull_news()
        self.build_kg_staging()
        log.info("Done. All output in: %s", self.out_dir.resolve())


if __name__ == "__main__":
    Puller().run_all()
