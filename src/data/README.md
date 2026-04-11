# Data Processing Module

## Overview

Xử lý và quản lý dữ liệu cho Knowledge Graph và Trading Framework.

## Modules

### vn30_puller.py - Pull Data từ Vnstock

**Mục đích**: Lấy dữ liệu từ vnstock phục vụ xây dựng Financial Knowledge Graph.

**Yêu cầu**:
```bash
pip install vnstock pandas tqdm
```

**Sử dụng**:
```python
from src.data.vn30_puller import Puller

# Pull tất cả data
puller = Puller()
puller.run_all()

# Hoặc từng phần
puller.pull_prices()
puller.pull_financials()
puller.pull_company_info()
puller.pull_news()
puller.build_kg_staging()
```

**Hoặc từ command line**:
```bash
python src/data/vn30_puller.py
# hoặc
python -m src.data.vn30_puller
```

**Output Structure**:
```
data/
├── prices/                          # OHLCV daily data
│   ├── VCB.csv
│   ├── VNM.csv
│   └── ...
├── financials/
│   ├── income_statement.csv
│   ├── balance_sheet.csv
│   ├── cash_flow.csv
│   └── ratios.csv
├── company_info/
│   ├── overview.csv                 # Company info
│   ├── shareholders.csv             # Large shareholders
│   ├── officers.csv                 # Management
│   └── subsidiaries.csv             # Subsidiaries
├── news/
│   ├── news_VCB.csv
│   ├── news_VNM.csv
│   └── ...
└── kg_staging/                      # Ready for Neo4j LOAD CSV
    ├── nodes_company.csv
    ├── nodes_industry.csv
    ├── nodes_shareholder.csv
    ├── edges_belongs_to.csv
    ├── edges_owns.csv
    └── edges_subsidiary.csv
```

**Cấu hình**:
- `START_DATE` = "2023-01-01"
- `END_DATE` = "2025-12-31"
- `DATA_SOURCE` = "VCI" (hoặc "TCBS")
- `SLEEP_BETWEEN_CALLS` = 0.6s (rate limiting)
- `OUT_DIR` = `data/`

**Danh sách VN30 Tickers**:
VCB, VNM, FPT, TCB, BID, HPG, SHB, CTG, GAS, SSB, MBB, VPB, TPB, ACB, BVH, VHM, MWG, GVR, VIC, VJC, STB, POW, PLX, VRE, SSI, SAB, GVR, BCM, HDB, MSN

**Key Features**:
- ✓ Rate limiting thân thiện (0.6s giữa các calls)
- ✓ Error handling - lỗi không crash pipeline
- ✓ Pre-formatted files cho Neo4j import
- ✓ Progress bars với tqdm
- ✓ Logging toàn bộ quá trình

**Một số lưu ý**:
- VCI (Vietcap) ổn định hơn cho fundamental data
- TCBS có thể nhanh hơn nhưng đôi khi bị rate limit
- Tất cả columns sẽ được giữ từ API response
- Subsidiaries được lưu dưới dạng edges sẵn sàng import Neo4j

## Cấu trúc Folder

```
src/data/
├── __init__.py           # Package initialization
├── vn30_puller.py        # Data pulling logic
├── README.md             # Documentation
```

## Tiếp theo

1. **Xây dựng KG từ staging files**:
   - Dùng `data/kg_staging/*.csv`
   - Load vào Neo4j với Cypher LOAD CSV
   - Tạo relationships giữa entities

2. **Data Preprocessing**:
   - Normalize financial metrics
   - Handle missing values
   - Time series alignment

3. **Feature Engineering**:
   - Calculate derived metrics
   - Create feature vectors
   - Generate embeddings

## Troubleshooting

### ImportError: No module named 'vnstock'
```bash
pip install vnstock pandas tqdm
```

### API Rate Limit Errors
- Tăng `SLEEP_BETWEEN_CALLS` (hiện tại 0.6s)
- Giảm số tickers hoặc chạy phần nhỏ hơn

### Memory Issues (dữ liệu quá lớn)
- Process từng ticker một
- Lưu từng output ngay (đã implement sẵn)
- Xóa files cũ nếu không cần

### Missing Columns
- Vnstock API có thể thay đổi column names
- Check logs để xem exact error
- Update column mapping trong code

## References

- [Vnstock Documentation](https://docs.vnstock.site/)
- [Neo4j LOAD CSV](https://neo4j.com/docs/cypher-manual/current/clauses/load-csv/)
- [Pandas Documentation](https://pandas.pydata.org/)
