"""Knowledge Graph Retriever for financial data."""

from dataclasses import dataclass
from typing import Optional
import json


@dataclass
class CompanyNode:
    """Company node in knowledge graph."""
    ticker: str
    name: str
    industry: str
    market_cap: float


@dataclass
class FinancialData:
    """Financial metrics for a company."""
    ticker: str
    pe_ratio: float
    pb_ratio: float
    roe: float
    roa: float
    debt_to_equity: float
    revenue_growth: float  # YoY growth %
    net_income: float
    current_ratio: float


@dataclass
class PriceData:
    """Price and technical data."""
    ticker: str
    current_price: float
    ma_20: float  # 20-day moving average
    ma_50: float  # 50-day moving average
    rsi: float  # Relative Strength Index
    volatility: float  # 30-day volatility %


@dataclass
class NewsData:
    """News and sentiment data."""
    ticker: str
    recent_news: list[str]
    sentiment_score: float  # -1 to 1, negative to positive


@dataclass
class RetrievedContext:
    """Context retrieved for a query."""
    query: str
    ticker: str
    company: CompanyNode
    financials: FinancialData
    prices: PriceData
    news: NewsData


class KGRetriever:
    """Mock Knowledge Graph Retriever for demo purposes."""

    # Mock data for VN30 stocks
    MOCK_DATA = {
        "VCB": {
            "company": CompanyNode(
                ticker="VCB",
                name="Vietcombank",
                industry="Finance",
                market_cap=2.5e12
            ),
            "financials": FinancialData(
                ticker="VCB",
                pe_ratio=8.5,
                pb_ratio=0.95,
                roe=28.0,
                roa=2.1,
                debt_to_equity=0.12,
                revenue_growth=12.5,
                net_income=8.5e11,
                current_ratio=1.8
            ),
            "prices": PriceData(
                ticker="VCB",
                current_price=92500,
                ma_20=91200,
                ma_50=89800,
                rsi=65.0,
                volatility=1.8
            ),
            "news": NewsData(
                ticker="VCB",
                recent_news=[
                    "VCB tăng vốn điều lệ lên 15 tỷ USD",
                    "Lợi nhuận Q1 2026 tăng 18% YoY",
                    "Tỷ lệ nợ xấu giảm xuống 0.5%"
                ],
                sentiment_score=0.75
            )
        },
        "VNM": {
            "company": CompanyNode(
                ticker="VNM",
                name="Vinamilk",
                industry="Food & Beverage",
                market_cap=1.85e12
            ),
            "financials": FinancialData(
                ticker="VNM",
                pe_ratio=22.5,
                pb_ratio=3.2,
                roe=18.5,
                roa=1.8,
                debt_to_equity=0.45,
                revenue_growth=8.2,
                net_income=2.1e11,
                current_ratio=1.5
            ),
            "prices": PriceData(
                ticker="VNM",
                current_price=85000,
                ma_20=84500,
                ma_50=83200,
                rsi=55.0,
                volatility=2.1
            ),
            "news": NewsData(
                ticker="VNM",
                recent_news=[
                    "VNM xuất khẩu sữa tăng mạnh vào thị trường Trung Quốc",
                    "Triển khai dự án nhà máy mới tại Long An",
                    "Đối tác chiến lược với tập đoàn Nhật Bản"
                ],
                sentiment_score=0.55
            )
        },
        "ACB": {
            "company": CompanyNode(
                ticker="ACB",
                name="Asia Commercial Bank",
                industry="Finance",
                market_cap=2.0e12
            ),
            "financials": FinancialData(
                ticker="ACB",
                pe_ratio=9.2,
                pb_ratio=1.1,
                roe=25.0,
                roa=1.9,
                debt_to_equity=0.15,
                revenue_growth=15.3,
                net_income=6.5e11,
                current_ratio=1.7
            ),
            "prices": PriceData(
                ticker="ACB",
                current_price=28500,
                ma_20=27800,
                ma_50=27200,
                rsi=68.0,
                volatility=1.9
            ),
            "news": NewsData(
                ticker="ACB",
                recent_news=[
                    "ACB kỷ lục lợi nhuận ròng năm 2025",
                    "Mở rộng mạng lưới chi nhánh tại Đông Nam Á",
                    "Phê duyệt chương trình mua lại cổ phiếu"
                ],
                sentiment_score=0.8
            )
        }
    }

    def retrieve(self, query: str, ticker: str) -> RetrievedContext:
        """
        Retrieve context from knowledge graph for a given query and ticker.

        Args:
            query: Investment decision query (e.g., "Should I invest in VCB?")
            ticker: Stock ticker symbol

        Returns:
            RetrievedContext with all relevant data
        """
        if ticker not in self.MOCK_DATA:
            # Return default data for unknown ticker
            return self._create_default_context(query, ticker)

        data = self.MOCK_DATA[ticker]
        return RetrievedContext(
            query=query,
            ticker=ticker,
            company=data["company"],
            financials=data["financials"],
            prices=data["prices"],
            news=data["news"]
        )

    def _create_default_context(self, query: str, ticker: str) -> RetrievedContext:
        """Create default context for unknown ticker."""
        return RetrievedContext(
            query=query,
            ticker=ticker,
            company=CompanyNode(
                ticker=ticker,
                name=f"Company {ticker}",
                industry="Unknown",
                market_cap=0.0
            ),
            financials=FinancialData(
                ticker=ticker,
                pe_ratio=0.0,
                pb_ratio=0.0,
                roe=0.0,
                roa=0.0,
                debt_to_equity=0.0,
                revenue_growth=0.0,
                net_income=0.0,
                current_ratio=0.0
            ),
            prices=PriceData(
                ticker=ticker,
                current_price=0.0,
                ma_20=0.0,
                ma_50=0.0,
                rsi=0.0,
                volatility=0.0
            ),
            news=NewsData(
                ticker=ticker,
                recent_news=[],
                sentiment_score=0.0
            )
        )

    def format_context(self, context: RetrievedContext) -> str:
        """Format context as readable string for agents."""
        return f"""
=== Knowledge Graph Context for {context.ticker} ({context.company.name}) ===

Company Info:
- Industry: {context.company.industry}
- Market Cap: ${context.company.market_cap / 1e12:.2f}T

Financial Metrics:
- P/E Ratio: {context.financials.pe_ratio:.2f}
- P/B Ratio: {context.financials.pb_ratio:.2f}
- ROE: {context.financials.roe:.1f}%
- ROA: {context.financials.roa:.1f}%
- Debt-to-Equity: {context.financials.debt_to_equity:.2f}
- Revenue Growth YoY: {context.financials.revenue_growth:.1f}%
- Current Ratio: {context.financials.current_ratio:.2f}

Price & Technical:
- Current Price: {context.prices.current_price:,.0f} VND
- MA20: {context.prices.ma_20:,.0f} VND
- MA50: {context.prices.ma_50:,.0f} VND
- RSI: {context.prices.rsi:.1f}
- 30-day Volatility: {context.prices.volatility:.1f}%

Recent News & Sentiment:
- Sentiment Score: {context.news.sentiment_score:.2f}/1.0
- Headlines:
  - {chr(10).join(['  - ' + news for news in context.news.recent_news])}
"""
