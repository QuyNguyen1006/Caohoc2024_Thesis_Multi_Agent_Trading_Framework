# Luận Văn Tổng Hợp: GraphRAG + Multi-Agent Reasoning cho Dự Báo Tài Chính

## 📋 Thông Tin Cơ Bản

| Thông Tin | Chi Tiết |
|-----------|----------|
| **Tên Luận Văn** | Nghiên cứu mô hình ngôn ngữ lớn tăng cường đồ thị tri thức trong dự báo tài chính và lập luận đầu tư dựa trên ngữ cảnh |
| **Học Viên** | Nguyễn Thị Quý (24007795) |
| **Giảng Viên Hướng Dẫn** | TS. Nguyễn Thị Hồng Khánh |
| **Trường** | Trường Đại học Khoa học Tự nhiên, ĐHQGHN |
| **Ngày Hoàn Thành** | 7 tháng 4 năm 2026 |
| **Công Nghệ Chính** | GraphRAG + Multi-Agent Reasoning |

---

## 🎯 1. Giới Thiệu (Introduction)

### 1.1 Động Lực Nghiên Cứu

**Vấn đề chính**: Dự báo tài chính là một bài toán có độ phức tạp cao, chịu ảnh hưởng bởi nhiều yếu tố:
- Các yếu tố kinh tế vĩ mô (macro factors)
- Mối quan hệ giữa các doanh nghiệp (entity relationships)
- Tâm lý thị trường (market sentiment)

**Yêu cầu**: 
- Độ chính xác cao trong dự báo
- Khả năng giải thích (explainability)

### 1.2 Hạn Chế của Các Phương Pháp Hiện Tại

| Phương Pháp | Ưu Điểm | Hạn Chế |
|-------------|---------|---------|
| **LSTM / GRU** | Dự đoán chuỗi thời gian tốt | Thiếu biểu diễn quan hệ thực thể |
| **LLM (GPT-4)** | Khả năng tạo sinh mạnh mẽ | Ảo giác, thiếu cấu trúc, không giải thích được |
| **Đồ Thị Tri Thức** | Biểu diễn quan hệ rõ ràng | Thiếu khả năng sinh và lý luận |

### 1.3 Nhu Cầu Nghiên Cứu

**Đề xuất**: Khung **GraphRAG** tích hợp:
- **FKG** (Financial Knowledge Graph): Biểu diễn cấu trúc quan hệ tài chính
- **LLM**: Khả năng lý luận và sinh
- **Multi-Agent**: Lập luận hợp tác từ nhiều góc nhìn

**Mục tiêu**:
- ✅ Giảm thiểu ảo giác
- ✅ Cải thiện tính ổn định
- ✅ Cung cấp khả năng giải thích

---

## 🔬 2. Kiến Thức Nền Tảng

### 2.1 Đồ Thị Tri Thức (Knowledge Graph - KG)

**Định nghĩa**: 
```
G = {(h, r, t) | h, t ∈ E, r ∈ R}
```

**Các thành phần**:
- **Thực thể (E)**: Công ty, ngành, chỉ số vĩ mô, sự kiện tài chính
- **Quan hệ (R)**: Sở hữu, ảnh hưởng, nhân quả
- **Hỗ trợ lập luận đa bước** (multi-hop reasoning)

### 2.2 Mô Hình Ngôn Ngữ Lớn (LLM)

**Công thức**:
```
P(w₁, ..., wₙ) = Πᵢ₌₁ⁿ P(wᵢ | w<ᵢ)
```

**Đặc điểm**:
- ✅ Khả năng hiểu và tạo ngôn ngữ tự nhiên mạnh mẽ
- ❌ Thiếu gắn kết với tri thức có cấu trúc
- ❌ Có thể tạo đầu ra ảo giác

### 2.3 RAG (Retrieval-Augmented Generation)

**RAG Truyền Thống**:
```
y = LLM(q, Dq)
```
- Truy xuất văn bản phi cấu trúc

**GraphRAG (Đề Xuất)**:
```
Gq ⊆ G
```
- Truy xuất có cấu trúc từ đồ thị
- Giảm thiểu ảo giác
- Cải thiện lập luận

---

## 💡 3. Phương Pháp Đề Xuất

### 3.1 Tổng Quan Khung Đề Xuất

**Luồng Xử Lý**:
```
Truy vấn q → Truy xuất KG → LLM (Multi-Agent) → Quyết định + Trích xuất giải thích
```

**4 Bước Chi Tiết**:

1. **Truy vấn q**: Nhận câu hỏi tài chính từ người dùng
   - Ví dụ: "Nên mua VCB tuần tới không?"

2. **Truy xuất KG**: Trích xuất đồ thị con Gq liên quan từ FKG
   - Tương đồng ngữ nghĩa
   - Lọc theo cấu trúc

3. **LLM (Multi-Agent)**: Mã hóa h = LLM(q, Gq) và lý luận qua các tác nhân chuyên biệt:
   - Af (Cơ bản): Phân tích báo cáo tài chính
   - As (Tâm lý): Phân tích tâm lý thị trường
   - At (Kỹ thuật): Phân tích chỉ báo kỹ thuật
   - Ar (Rủi ro): Đánh giá và quản trị rủi ro

4. **Quyết định + Trích xuất giải thích**: 
   - Tổng hợp y = Aggregate({o_i^(K)})
   - Đường lý luận P ⊆ Gq (giải thích)

### 3.2 Xây Dựng Đồ Thị Tri Thức Tài Chính (FKG)

```
G = (E, R)
```

**Nút (Nodes)**:
- Công ty
- Ngành
- Chỉ số kinh tế vĩ mô
- Sự kiện tài chính

**Cạnh (Edges)**:
- Sở hữu (OWNS)
- Chuỗi cung ứng (SUPPLY_CHAIN)
- Tương tác nhân quả (CAUSALITY)

**Thuộc tính (Attributes)**:
- Tỷ lệ tài chính
- Xu hướng giá

**Thời gian (Temporal)**:
- Tích hợp để nắm bắt động lực thị trường

### 3.3 Truy Xuất Đồ Thị & Mã Hóa LLM

**Truy xuất đồ thị**:
```
Gq = Retrieve(q, G, D)
```
- Tương đồng ngữ nghĩa
- Lọc theo cấu trúc

**Mã hóa LLM**:
```
h = LLM(q, Gq)
```
- Tiêm tri thức đồ thị vào LLM
- Cải thiện tính nhất quán thực tế

### 3.4 Cơ Chế Tranh Luận (Multi-Agent Debate)

**Tinh chỉnh lặp**:
```
o_i^(k) = Refine(o_i^(k-1), {o_j^(k-1)}_{j≠i})
```

**Đặc điểm**:
- Các tác nhân tinh chỉnh đầu ra dựa trên phản hồi của nhau
- Xác thực chéo giảm thiểu thiên kiến cá nhân

**Dự đoán cuối cùng**:
```
y = Aggregate({o_i^(K)})
```

### 3.5 Giải Thích Qua Đồ Thị

```
P = {p₁, p₂, ..., pₘ}, pᵢ ⊆ Gq
```

**Đặc điểm**:
- Trích xuất đường lý luận từ đồ thị tri thức
- Quyết định minh bạch, có thể truy vết

### 3.6 Hàm Mục Tiêu

```
L = L_pred(ŷ, y) + λL_cons({o_i^(K)}, Gq)
```

- **L_pred**: Độ chính xác dự đoán
- **L_cons**: Nhất quán với cấu trúc đồ thị
- **λ**: Cân bằng giữa hai mục tiêu

### 3.7 Phân Tích Độ Phức Tạp

```
O(K(|Gq| + L² + |A|²))
```

| Thành Phần | Độ Phức Tạp | Mô Tả |
|-----------|-----------|-------|
| **Truy xuất đồ thị** | O(\|Gq\|) | Duyệt đồ thị + tương đồng ngữ nghĩa |
| **Mã hóa LLM** | O(L²) | Transformer self-attention |
| **Đa tác nhân** | O(K\|A\|²) | K vòng tranh luận, \|A\| tác nhân |

---

## 🧪 4. Thí Nghiệm

### 4.1 Tập Dữ Liệu

**Cổ phiếu**: VN30 (30 cổ phiếu lớn nhất Việt Nam)

**Thời gian**: 2023–2025

**Dữ liệu**:
- 📊 Dữ liệu giá (OHLCV)
- 📈 Báo cáo tài chính
- 📰 Bài báo tin tức

### 4.2 Mô Hình So Sánh (Baselines)

1. **LSTM**: Dự đoán dựa trên chuỗi thời gian
2. **LLM độc lập (GPT)**: LLM không sử dụng KG
3. **Buy-and-Hold**: Chiến lược mua và giữ đơn giản

### 4.3 Chỉ Số Đánh Giá

- **Tỷ lệ Sharpe**: Lợi nhuận điều chỉnh theo rủi ro
- **Maximum Drawdown**: Mức sụt giảm tối đa
- **Annual Return**: Lợi nhuận hàng năm

---

## 📊 5. Kết Quả Dự Kiến

### 5.1 Hiệu Suất Dự Báo

- ✅ **Tỷ lệ Sharpe cao hơn** so với các baseline
- ✅ **Mức sụt giảm thấp hơn** (Lower Maximum Drawdown)
- ✅ **Dự đoán ổn định hơn** (More Stable Predictions)

### 5.2 Khả Năng Giải Thích

- Đường lý luận có thể truy vết từ đồ thị
- Quyết định minh bạch và có căn cứ
- Giảm ảo giác so với LLM độc lập

---

## 🚀 6. Đóng Góp Chính (Main Contributions)

1. **Đồ Thị Tri Thức Tài Chính (FKG)** cho thị trường chứng khoán Việt Nam
2. **Khung GraphRAG** tích hợp KG và LLM cho lý luận tài chính
3. **Cơ Chế Tranh Luận Đa Tác Nhân** cho ra quyết định
4. **Đường Lý Luận Có Khả Năng Giải Thích** trên đồ thị
5. **Cải Thiệu Hiệu Suất Tài Chính** so với các baseline

---

## 🔮 7. Hướng Phát Triển (Future Directions)

1. **Cập Nhật Đồ Thị Tri Thức Động** (Dynamic KG)
   - Cập nhật KG theo thời gian thực
   - Thêm mối quan hệ mới dựa trên dữ liệu mới

2. **Tác Nhân Học Tăng Cường** (Reinforcement Learning)
   - Huấn luyện tác nhân để tối ưu hóa dự đoán
   - Tăng cường cơ chế tranh luận

3. **Triển Khai Thời Gian Thực** (Real-time Deployment)
   - Hệ thống phục vụ thời gian thực
   - Cập nhật dự đoán liên tục

---

## 📈 8. Bài Toán Nghiên Cứu

### 8.1 Định Nghĩa Chính Thức

**Đầu Vào**:
- Truy vấn tài chính q
  - Ví dụ: "Nên mua VCB tuần tới không?"
- Đồ thị tri thức tài chính G
- Dữ liệu lịch sử D (giá, báo cáo tài chính, tin tức)

**Đầu Ra**:
- Dự đoán y: xu hướng giá hoặc hành động đầu tư (Mua/Bán/Giữ)
- Tập đường lý luận P ⊆ Gq: giải thích cho quyết định

**Công Thức**:
```
f(q, G, D) → (y, P)
```

---

## 💼 9. Ứng Dụng Thực Tế

### 9.1 Lợi Ích Chính

1. **Dự Báo Chính Xác**: Kết hợp dữ liệu và lý luận từ nhiều nguồn
2. **Giải Thích**: Nhà đầu tư có thể hiểu lý do đằng sau quyết định
3. **Ổn Định**: Giảm ảo giác và lỗi dự báo
4. **Linh Hoạt**: Dễ dàng mở rộng với các tác nhân hoặc nguồn dữ liệu mới

### 9.2 Trường Hợp Sử Dụng

- 🏦 **Công Ty Quản Lý Quỹ**: Tối ưu hóa danh mục đầu tư
- 📊 **Nhà Giao Dịch**: Quyết định mua/bán dựa trên lý luận AI
- 📈 **Phân Tích Tài Chính**: Hỗ trợ phân tích và dự báo
- 🎯 **Quản Lý Rủi Ro**: Đánh giá rủi ro dựa trên dữ liệu toàn bộ

---

## 📚 10. Tài Liệu Tham Khảo (References)

Các bài báo chính được sử dụng:
1. **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** (NeurIPS 2020)
2. **Unifying Large Language Models and Knowledge Graphs: A Roadmap** (Pan et al., 2023)
3. **Recent Advances in Knowledge Graph** (arXiv 2412.20138)

---

## 🎓 11. Kết Luận

### 11.1 Tóm Tắt

Luận văn đề xuất **GraphRAG**, một khung kết hợp Đồ Thị Tri Thức Tài Chính, Mô Hình Ngôn Ngữ Lớn, và Lý Luận Đa Tác Nhân để:
- ✅ Dự báo tài chính chính xác
- ✅ Giảm ảo giác
- ✅ Cung cấp giải thích minh bạch

### 11.2 Ý Nghĩa

- **Học Thuật**: Chứng minh hiệu quả của GraphRAG trong lĩnh vực tài chính
- **Thực Tiễn**: Cung cấp công cụ hỗ trợ quyết định đầu tư
- **Công Nghệ**: Kết hợp các công nghệ mới (LLM, KG, Multi-Agent)

---

## 📞 Thông Tin Liên Hệ

| Thông Tin | Chi Tiết |
|-----------|----------|
| **Tên** | Nguyễn Thị Quý |
| **Email** | 24007795@hus.edu.vn |
| **Trường** | Trường Đại học Khoa học Tự nhiên, ĐHQGHN |
| **Giảng Viên Hướng Dẫn** | TS. Nguyễn Thị Hồng Khánh |

---

## 📎 Phụ Lục: Danh Sách Công Thức Toán Học

1. **Đồ Thị Tri Thức**: `G = {(h, r, t) | h, t ∈ E, r ∈ R}`
2. **LLM**: `P(w₁, ..., wₙ) = Πᵢ₌₁ⁿ P(wᵢ | w<ᵢ)`
3. **Truy Xuất Đồ Thị**: `Gq = Retrieve(q, G, D)`
4. **Mã Hóa LLM**: `h = LLM(q, Gq)`
5. **Tinh Chỉnh Lặp**: `o_i^(k) = Refine(o_i^(k-1), {o_j^(k-1)}_{j≠i})`
6. **Dự Đoán Cuối Cùng**: `y = Aggregate({o_i^(K)})`
7. **Giải Thích**: `P = {p₁, p₂, ..., pₘ}, pᵢ ⊆ Gq`
8. **Hàm Mục Tiêu**: `L = L_pred(ŷ, y) + λL_cons({o_i^(K)}, Gq)`
9. **Độ Phức Tạp**: `O(K(|Gq| + L² + |A|²))`
10. **Bài Toán**: `f(q, G, D) → (y, P)`

---

**Generated**: 12/04/2026  
**Status**: ✅ Tài Liệu Tóm Tắt Hoàn Chỉnh
