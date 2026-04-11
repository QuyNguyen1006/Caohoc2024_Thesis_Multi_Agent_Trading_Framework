# VN30 Data Puller Guide

Pull dữ liệu từ vnstock để xây dựng Financial Knowledge Graph.

## 📋 Quick Start

### 1. Install Dependencies

```bash
pip install vnstock pandas tqdm
# hoặc
pip install -r requirements.txt
```

### 2. Run Data Puller

**Mặc định (full pipeline)**:
```bash
python run_data_puller.py
```

**Chỉ pull giá (OHLCV)**:
```bash
python run_data_puller.py --prices-only
```

**Pull tất cả trừ giá**:
```bash
python run_data_puller.py --skip-prices
```

**Custom tickers**:
```bash
python run_data_puller.py --tickers VCB VNM FPT TCB
```

**Custom date range**:
```bash
python run_data_puller.py --start-date 2024-01-01 --end-date 2024-12-31
```

**Custom output folder**:
```bash
python run_data_puller.py --output ./my_data
```

### 3. Verify Output

```bash
ls data/
# prices/
# financials/
# company_info/
# news/
# kg_staging/
```

## 📖 Detailed Usage

### Python API

**Method 1: Using Default Config**
```python
from src.data.vn30_puller import Puller

puller = Puller()
puller.run_all()
```

**Method 2: Using Custom Config**
```python
from src.data.vn30_puller import Puller
from src.data.data_config import create_custom_config

config = create_custom_config(
    start_date="2024-01-01",
    end_date="2024-12-31",
    tickers=["VCB", "VNM", "FPT"],
    output_dir="my_data",
)

puller = Puller(source=config.data_source, out_dir=config.output_dir)
puller.run_all()
```

**Method 3: Pull Specific Components**
```python
from src.data.vn30_puller import Puller

puller = Puller()
puller.pull_prices()                # Chỉ giá
puller.pull_financials()            # Chỉ financials
puller.pull_company_info()          # Chỉ company info
puller.pull_news()                  # Chỉ news
puller.build_kg_staging()           # Build KG staging files
```

### Command Line

**View all options**:
```bash
python run_data_puller.py --help
```

**Common scenarios**:

```bash
# Full pipeline with verbose logging
python run_data_puller.py -v

# Just financials, verbose
python run_data_puller.py --financials-only -v

# Multiple tickers, custom period
python run_data_puller.py --tickers ACB BCM BID --start-date 2024-01-01 --end-date 2024-12-31

# Slower rate (avoid throttling)
python run_data_puller.py --sleep 1.0

# Different data source
python run_data_puller.py --source TCBS

# Build KG staging only (assuming raw data exists)
python run_data_puller.py --kg-staging-only
```

## 🔧 Configuration

### Default Settings (from `data_config.py`)

```python
start_date: "2023-01-01"
end_date: "2025-12-31"
data_source: "VCI"              # VCI = Vietcap, TCBS = VietStock
sleep_between_calls: 0.6        # seconds
tickers: VN30_TICKERS           # All 30 stocks
output_dir: Path("data")
```

### Change Defaults

Edit `src/data/data_config.py`:

```python
@dataclass
class DataConfig:
    start_date: str = "2024-01-01"  # Change here
    end_date: str = "2024-12-31"    # Change here
    # ... etc
```

## 📁 Output Structure

```
data/
├── prices/                          # OHLCV daily
│   ├── VCB.csv                     # Columns: date, open, high, low, close, volume
│   ├── VNM.csv
│   └── ... (30 files)
│
├── financials/                      # Yearly statements (consolidated)
│   ├── income_statement.csv        # Revenue, profit, etc.
│   ├── balance_sheet.csv           # Assets, liabilities, equity
│   ├── cash_flow.csv               # Operating, investing, financing CF
│   └── ratios.csv                  # Financial ratios
│
├── company_info/
│   ├── overview.csv                # Company name, sector, market cap
│   ├── shareholders.csv            # Major shareholders (for OWNS edges)
│   ├── officers.csv                # Management/board members
│   └── subsidiaries.csv            # Subsidiary companies
│
├── news/
│   ├── news_VCB.csv
│   ├── news_VNM.csv
│   └── ... (news + events per ticker)
│
└── kg_staging/                      # Ready for Neo4j LOAD CSV
    ├── nodes_company.csv
    ├── nodes_industry.csv
    ├── nodes_shareholder.csv
    ├── edges_belongs_to.csv        # Company -> Industry
    ├── edges_owns.csv              # Shareholder -> Company
    └── edges_subsidiary.csv        # Company -> Subsidiary
```

## ⚙️ Performance Tips

### Speed Up (if rate limiting is not a concern)
```bash
python run_data_puller.py --sleep 0.3
```

### Slow Down (if getting throttled)
```bash
python run_data_puller.py --sleep 1.5
```

### Smaller Scope (testing)
```bash
python run_data_puller.py --tickers VCB VNM FPT
```

### Check Memory Usage
```bash
# On Mac/Linux
# Terminal 1: python run_data_puller.py
# Terminal 2: 
watch -n 1 'ps aux | grep python'
```

## 🐛 Troubleshooting

### 1. ImportError: No module named 'vnstock'

**Solution**:
```bash
pip install vnstock pandas tqdm
```

### 2. Rate Limit / Throttling Errors

**Solution**:
```bash
# Increase sleep between calls
python run_data_puller.py --sleep 1.0
```

### 3. Missing Columns in Output

**Issue**: API response structure changed
**Solution**:
- Check logs: `ValueError: column 'X' not found`
- Update column mapping in `vn30_puller.py` in the `build_kg_staging()` method
- Report issue if it's API change

### 4. Memory Issues

**Solution**:
```bash
# Process by component
python run_data_puller.py --prices-only
python run_data_puller.py --financials-only
python run_data_puller.py --company-info-only
python run_data_puller.py --news-only
python run_data_puller.py --kg-staging-only
```

### 5. Network Timeout

**Solution**:
```bash
# Retry with longer sleep
python run_data_puller.py --sleep 2.0 -v
```

## 📊 Data Quality Notes

### Known Limitations

1. **news/**: Limited history (typically last 6-12 months)
2. **financials/**: Only yearly data, some companies may have incomplete history
3. **shareholders/**: Top shareholders, not all holders
4. **Data currency**: Updates daily, historical accuracy depends on API

### Validation

After pulling, check:
```bash
# Check data exists
wc -l data/prices/*.csv
wc -l data/financials/*.csv

# Spot check a file
head -5 data/prices/VCB.csv
```

## 🔄 Next Steps

### 1. Load into Neo4j

```cypher
// Load companies
LOAD CSV WITH HEADERS FROM "file:///kg_staging/nodes_company.csv" AS row
CREATE (c:Company {ticker: row.`ticker:ID(Company)`, name: row.name});

// Load industries
LOAD CSV WITH HEADERS FROM "file:///kg_staging/nodes_industry.csv" AS row
CREATE (i:Industry {name: row.`name:ID(Industry)`});

// And so on...
```

### 2. Build Financial Features

```python
# Use prices/ data to calculate technical indicators
# Use financials/ data to calculate financial ratios
# Create feature vectors for ML models
```

### 3. Knowledge Graph Enrichment

```python
# Add company relationships from shareholders/
# Add subsidiaries relationships
# Add news sentiment analysis
```

## 📚 References

- [Vnstock Docs](https://docs.vnstock.site/)
- [Neo4j LOAD CSV](https://neo4j.com/docs/cypher-manual/current/clauses/load-csv/)
- [VN30 Index](https://en.wikipedia.org/wiki/VN_Index)

## ❓ FAQ

**Q: Can I use TCBS instead of VCI?**
A: Yes, but VCI is more stable for fundamentals. Use `--source TCBS`

**Q: How often should I update data?**
A: Daily after market close (3:30 PM Vietnam time)

**Q: Can I modify the tickers list?**
A: Yes, edit `DEFAULT_CONFIG` in `src/data/data_config.py` or use `--tickers` flag

**Q: What if I only need recent data?**
A: Use `--start-date` and `--end-date` flags

**Q: How long does full pipeline take?**
A: ~15-30 minutes depending on network and sleep settings

---

**Last Updated**: 2026-04-11
