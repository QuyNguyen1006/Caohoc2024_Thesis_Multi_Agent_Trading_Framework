# VN30 Data Structure Guide

Tài liệu mô tả cấu trúc dữ liệu sau khi pull từ vnstock.

## 📊 Data Overview

Dữ liệu được tổ chức thành **5 thư mục chính**:

```
data/
├── prices/              # OHLCV daily data
├── financials/          # Yearly financial statements
├── company_info/        # Company profiles & relationships
├── news/                # News & events
└── kg_staging/          # Pre-formatted for Neo4j
```

---

## 1️⃣ PRICES (Daily OHLCV Data)

**Location**: `data/prices/`

**Files**: One CSV per ticker (e.g., `ACB.csv`, `VNM.csv`, ...)

### Structure

```csv
time,open,high,low,close,volume,ticker
2022-11-10,12.11,12.25,11.43,11.72,5466448,ACB
2022-11-11,12.13,12.43,11.99,12.19,4327549,ACB
2022-11-14,12.02,12.13,11.70,11.90,5259075,ACB
```

### Columns

| Column | Type | Description |
|--------|------|-------------|
| `time` | date | Trading date (YYYY-MM-DD) |
| `open` | float | Opening price |
| `high` | float | Daily high price |
| `low` | float | Daily low price |
| `close` | float | Closing price |
| `volume` | int | Trading volume |
| `ticker` | string | Stock ticker symbol |

### Usage

- **Technical Analysis**: Calculate RSI, MACD, Bollinger Bands
- **Trading Signals**: Identify entry/exit points
- **Backtesting**: Test trading strategies
- **Feature Engineering**: Create lag features, momentum indicators

### Time Range

- Start: 2022-11-10 (or earlier depending on availability)
- End: Latest date (updates daily)
- Frequency: Daily (1D)

---

## 2️⃣ FINANCIALS (Yearly Financial Statements)

**Location**: `data/financials/`

**Files**: 4 consolidated CSV files for all tickers

### Files & Structure

#### `income_statement.csv`

```csv
ticker,year,revenue,gross_profit,operating_profit,net_income,eps
ACB,2024,12500,5000,3500,2800,2.5
ACB,2023,11800,4800,3200,2600,2.3
```

**Metrics**:
- Revenue (Doanh thu)
- Gross Profit (Lợi nhuận gộp)
- Operating Profit (Lợi nhuận hoạt động)
- Net Income (Lợi nhuận ròng)
- EPS (Earnings Per Share)

#### `balance_sheet.csv`

```csv
ticker,year,total_assets,total_liabilities,total_equity,current_ratio
ACB,2024,250000,150000,100000,1.5
```

**Metrics**:
- Total Assets (Tổng tài sản)
- Total Liabilities (Tổng nợ)
- Total Equity (Vốn chủ sở hữu)
- Current Ratio (Tỷ lệ thanh toán hiện tại)

#### `cash_flow.csv`

```csv
ticker,year,operating_cash_flow,investing_cash_flow,financing_cash_flow
ACB,2024,8500,-2000,-6000
```

**Metrics**:
- Operating Cash Flow (Lưu tiền hoạt động)
- Investing Cash Flow (Lưu tiền đầu tư)
- Financing Cash Flow (Lưu tiền tài chính)

#### `ratios.csv`

```csv
ticker,year,pe_ratio,pb_ratio,roa,roe,debt_to_equity
ACB,2024,8.5,0.95,12.5,28.0,1.5
```

**Ratios**:
- PE Ratio (Price-to-Earnings)
- PB Ratio (Price-to-Book)
- ROA (Return on Assets)
- ROE (Return on Equity)
- Debt-to-Equity Ratio

### Usage

- **Valuation**: Compare PE, PB ratios across companies
- **Financial Health**: Analyze liquidity (current ratio), solvency (debt-to-equity)
- **Performance**: Track revenue growth, profitability (ROE, ROA)
- **Forecasting**: Use historical trends for earnings prediction

### Time Range

- Yearly data (annual reports)
- Typically 5+ years available

---

## 3️⃣ COMPANY INFO (Company Profiles & Relationships)

**Location**: `data/company_info/`

**Files**: 4 CSV files

### `overview.csv`

```csv
ticker,company_name,short_name,exchange,industry,market_cap
ACB,Ngân hàng Á Châu,ACB,HOSE,Finance,25000000000
VNM,Công ty Nông sản Sài Gòn,VNM,HOSE,Food & Beverage,185000000000
```

**Info**: Company name, industry classification, market cap

### `shareholders.csv`

```csv
ticker,shareholder_name,share_percentage
ACB,Nhà nước,15.5
ACB,Quỹ Đầu tư Nhân dân,8.2
VNM,Nhà nước,37.8
```

**Usage**: Build Knowledge Graph edges (OWNS relationships)

### `officers.csv`

```csv
ticker,officer_name,position,department
ACB,Trần Minh Bình,Chủ tịch HĐQT,Board
ACB,Phạm Quang Thái,Tổng Giám đốc,Management
```

**Info**: Management team, board members

### `subsidiaries.csv`

```csv
ticker,subsidiary_name,ownership_percentage
ACB,ACB Finance,100.0
VNM,Saigon Seeds,100.0
```

**Usage**: Build Knowledge Graph edges (HAS_SUBSIDIARY relationships)

---

## 4️⃣ NEWS (News & Events)

**Location**: `data/news/`

**Files**: One CSV per ticker (e.g., `news_ACB.csv`, `news_VNM.csv`)

### Structure

```csv
ticker,date,title,kind,url
ACB,2026-04-10,ACB công bố kết quả kinh doanh Q1 2026,news,https://...
ACB,2026-04-05,ACB tăng vốn điều lệ lên 25 tỷ VND,event,https://...
VNM,2026-04-08,VNM xuất khẩu cà phê lập kỷ lục mới,news,https://...
```

### Columns

| Column | Type | Description |
|--------|------|-------------|
| `ticker` | string | Stock ticker |
| `date` | date | Publication date |
| `title` | string | News headline |
| `kind` | string | Type: "news" or "event" |
| `url` | string | Link to original article |

### Usage

- **Sentiment Analysis**: Analyze impact of news on stock price
- **Event Detection**: Identify major events (earnings, corporate actions)
- **AI Reasoning**: Use news context for investment decisions
- **Correlation Analysis**: Link news events to price movements

### Time Range

- Typically last 6-12 months of news
- Updates as new articles are published

---

## 5️⃣ KG STAGING (Knowledge Graph Pre-formatted Files)

**Location**: `data/kg_staging/`

⭐ **These files are pre-formatted and ready to be loaded into Neo4j!**

### Format

Files follow Neo4j's **LOAD CSV** format:
- Header row with column names
- Special column name syntax for node/relationship IDs
- Consistent data types

### Files

#### `nodes_company.csv`

```csv
ticker:ID(Company),name,exchange,industry,:LABEL
ACB,Ngân hàng Á Châu,HOSE,Finance,Company
VNM,Công ty Nông sản Sài Gòn,HOSE,Food & Beverage,Company
```

**Neo4j Load**:
```cypher
LOAD CSV WITH HEADERS FROM "file:///kg_staging/nodes_company.csv" AS row
CREATE (c:Company {
  ticker: row.`ticker:ID(Company)`,
  name: row.name,
  exchange: row.exchange,
  industry: row.industry
})
```

#### `nodes_industry.csv`

```csv
name:ID(Industry),:LABEL
Finance,Industry
Food & Beverage,Industry
```

#### `nodes_shareholder.csv`

```csv
name:ID(Shareholder),:LABEL
Nhà nước,Shareholder
Vietcombank,Shareholder
```

#### `edges_belongs_to.csv` (Company → Industry)

```csv
:START_ID(Company),:END_ID(Industry),:TYPE
ACB,Finance,BELONGS_TO
VNM,Food & Beverage,BELONGS_TO
```

**Relationship**: `Company -[BELONGS_TO]-> Industry`

#### `edges_owns.csv` (Shareholder → Company)

```csv
:START_ID(Shareholder),:END_ID(Company),pct:float,:TYPE
Nhà nước,ACB,15.5,OWNS
Nhà nước,VNM,37.8,OWNS
```

**Relationship**: `Shareholder -[OWNS {percentage}]-> Company`

#### `edges_subsidiary.csv` (Company → Company)

```csv
:START_ID(Company),subsidiary_name,:TYPE
ACB,ACB Finance,HAS_SUBSIDIARY
VNM,Saigon Seeds,HAS_SUBSIDIARY
```

**Relationship**: `Company -[HAS_SUBSIDIARY]-> Company`

### Neo4j Loading Script

```cypher
// Load nodes
LOAD CSV WITH HEADERS FROM "file:///kg_staging/nodes_company.csv" AS row
CREATE (c:Company {ticker: row.`ticker:ID(Company)`, name: row.name});

LOAD CSV WITH HEADERS FROM "file:///kg_staging/nodes_industry.csv" AS row
CREATE (i:Industry {name: row.`name:ID(Industry)`});

LOAD CSV WITH HEADERS FROM "file:///kg_staging/nodes_shareholder.csv" AS row
CREATE (s:Shareholder {name: row.`name:ID(Shareholder)`});

// Load relationships
LOAD CSV WITH HEADERS FROM "file:///kg_staging/edges_belongs_to.csv" AS row
MATCH (c:Company {ticker: row.`START_ID(Company)`})
MATCH (i:Industry {name: row.`END_ID(Industry)`})
CREATE (c)-[:BELONGS_TO]->(i);

LOAD CSV WITH HEADERS FROM "file:///kg_staging/edges_owns.csv" AS row
MATCH (s:Shareholder {name: row.`START_ID(Shareholder)`})
MATCH (c:Company {ticker: row.`END_ID(Company)`})
CREATE (s)-[:OWNS {percentage: toFloat(row.`pct:float`)}]->(c);
```

---

## 📈 Data Flow

```
VN30 Stocks (30 companies)
    ↓
vnstock API (Data Fetching)
    ↓
vn30_puller.py (Processing)
    ↓
├─ prices/          (20,000+ daily records)
├─ financials/      (120+ yearly records)
├─ company_info/    (Multiple tables)
├─ news/            (1,000+ articles)
└─ kg_staging/      (Pre-formatted CSV)
    ↓
Neo4j Database (Knowledge Graph)
    ↓
ML Models (Feature Engineering)
    ↓
├─ Price Prediction
├─ Trading Strategies
├─ Portfolio Optimization
└─ Investment Reasoning
```

---

## 🎯 Common Use Cases

### Technical Analysis
```python
import pandas as pd
prices = pd.read_csv('data/prices/VCB.csv')
prices['MA_20'] = prices['close'].rolling(20).mean()
prices['RSI'] = calculate_rsi(prices['close'])
```

### Financial Ratio Analysis
```python
import pandas as pd
ratios = pd.read_csv('data/financials/ratios.csv')
top_companies = ratios.nlargest(5, 'roe')
```

### Knowledge Graph Query
```cypher
// Find major shareholders and their investments
MATCH (s:Shareholder)-[r:OWNS]->(c:Company)
WHERE r.percentage > 10
RETURN s.name, c.ticker, c.industry, r.percentage
ORDER BY r.percentage DESC
```

### News Sentiment Analysis
```python
import pandas as pd
news = pd.read_csv('data/news/news_ACB.csv')
news['sentiment'] = analyze_sentiment(news['title'])
```

---

## 📊 Data Quality Notes

- **Prices**: Generally reliable, daily updates
- **Financials**: Accurate yearly reports, may lag by 1-2 months
- **Company Info**: Mostly static, updates when corporate changes occur
- **News**: Comprehensive but with limited history (6-12 months typical)
- **KG Staging**: Formatted perfectly for Neo4j, no cleaning needed

---

## ⚠️ Known Limitations

1. **Rate Limiting**: Guest account limited to 20 requests/minute
   - Solution: Register free API key at https://vnstocks.com/login
   - This increases limit to 60 requests/minute

2. **Data Availability**: 
   - Some historical data may not be available for newer companies
   - Financial data typically lags by 1-2 months

3. **News**: Limited to recent articles (typically 6-12 months)

---

## 🚀 Getting Real Data

To pull actual data for all 30 VN30 stocks:

```bash
# Register API key
# https://vnstocks.com/login

# Set environment variable
export VNSTOCK_API_KEY="your-api-key"

# Run full pipeline
python run_data_puller.py --sleep 1.0

# Expected time: 30-40 minutes
# Result: ~20,000 price records + financials + company info
```

---

## 📝 Files Generated

Total files created per full run:
- Prices: 30 CSV files (one per stock)
- Financials: 4 CSV files (consolidated)
- Company Info: 4 CSV files
- News: ~30 CSV files (one per stock)
- KG Staging: 6 CSV files (pre-formatted for Neo4j)

**Total size**: ~50-100 MB depending on data completeness

---

For more information, see:
- `DATA_PULLER_GUIDE.md` - How to run the data puller
- `src/data/README.md` - Data module documentation
- `PROJECT_STRUCTURE.md` - Project organization
