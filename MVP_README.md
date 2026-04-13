# GraphRAG MVP - Investment Decision Framework

Complete implementation of the **multi-agent GraphRAG framework** for investment decisions as described in the thesis.

## 🎯 What This Demo Shows

This MVP demonstrates a complete flow from investment query to decision recommendation:

```
Query q: "Should I invest in VCB?"
    ↓
Knowledge Graph Retrieval: Gq = Retrieve(q, G, D)
    ↓
Initial Reasoning: o_i^(0) = Reason(Gq)  [4 agents analyze]
    ↓
Multi-Agent Debate: o_i^(k) = Refine(o_i^(k-1), peers)  [K=3 rounds]
    ↓
Final Aggregation: y = Aggregate({o_i^(K)})
    ↓
Result: BUY (Confidence: 86%)
```

## 🏗️ Architecture

### 1. Knowledge Graph Module (`src/kg/`)

**Purpose**: Retrieve financial data relevant to investment queries

```python
from src.kg.retriever import KGRetriever

retriever = KGRetriever()
context = retriever.retrieve("Should I invest in VCB?", "VCB")
```

**Data Retrieved**:
- Company information (name, industry, market cap)
- Financial metrics (P/E, ROE, debt ratios)
- Price data (current price, MAs, RSI, volatility)
- News & sentiment (recent headlines, sentiment score)

### 2. Agents Module (`src/agents/`)

**Purpose**: Specialized financial analysts with different perspectives

#### BaseAgent (Abstract)
```python
class BaseAgent(ABC):
    def reason(context) → AgentOpinion      # Initial analysis
    def refine(opinion, peers) → AgentOpinion  # Debate mechanism
```

#### Concrete Agents (4 types)

| Agent | Focus | Analyzes |
|-------|-------|----------|
| **Fundamental Analyst** | Valuations, growth, profitability | P/E, ROE, pb_ratio, revenue growth |
| **Sentiment Analyst** | Market mood, news signals | Sentiment score, recent headlines |
| **Technical Analyst** | Price trends, momentum | Moving averages, RSI, trends |
| **Risk Manager** | Volatility, leverage, liquidity | Volatility, debt/equity, current ratio |

### 3. Reasoning Module (`src/reasoning/`)

**Purpose**: Multi-agent debate mechanism for consensus

```python
from src.reasoning.debate import DebateEngine

debate = DebateEngine(agents=[fund, sent, tech, risk], num_rounds=3)
result = debate.run_debate(context, query="...", ticker="VCB")
```

**Debate Flow**:
1. **Round 0**: Initial reasoning by all agents
2. **Rounds 1-K**: Iterative refinement based on peer opinions
3. **Final**: Aggregation into single recommendation

**Aggregation Logic**:
- Majority voting (BUY/HOLD/SELL)
- Average confidence score
- Consensus reasoning from all perspectives

## 🚀 Running the Demo

### Quick Start

```bash
# Run complete demo
python demo_mvp.py
```

### Using in Your Code

```python
from src.kg.retriever import KGRetriever
from src.agents import FundamentalAgent, SentimentAgent, TechnicalAgent, RiskAgent
from src.reasoning.debate import DebateEngine

# 1. Retrieve context
retriever = KGRetriever()
context = retriever.retrieve("Should I buy VCB?", "VCB")
context_str = retriever.format_context(context)

# 2. Create agents
agents = [
    FundamentalAgent(),
    SentimentAgent(),
    TechnicalAgent(),
    RiskAgent(),
]

# 3. Run debate
debate = DebateEngine(agents, num_rounds=3)
result = debate.run_debate(context_str, "Should I buy VCB?", "VCB")

# 4. Get results
print(f"Recommendation: {result.final_recommendation}")
print(f"Confidence: {result.final_confidence:.2%}")
print(f"Reasoning: {result.consensus_reasoning}")
```

## 📊 Demo Output Example

The demo produces rich output showing:

### Stage 1: Query & Retrieval
```
Query: Should I invest in VCB stock?
Ticker: VCB

Company: Vietcombank (Finance sector)
Market Cap: $2.50T

Financial Metrics:
- P/E: 8.50 (undervalued)
- ROE: 28.0% (healthy)
- Revenue Growth: 12.5% YoY

Price Data:
- Current: 92,500 VND
- MA20: 91,200 | MA50: 89,800
- RSI: 65.0 (bullish momentum)
- Volatility: 1.8% (low)

Sentiment: 0.75/1.0 (positive)
```

### Stage 2: Initial Analysis
```
✓ Fundamental Analyst: BUY (0.75)
✓ Sentiment Analyst: BUY (0.70)
✓ Technical Analyst: BUY (0.72)
✓ Risk Manager: BUY (0.72)
```

### Stage 3: Debate Refinement
```
Round 1: Confidence increases as consensus builds
Round 2: Further refinement through peer influence
Round 3: Final convergence to high confidence
```

### Stage 4: Final Result
```
✅ RECOMMENDATION: BUY
   Confidence: 86%
   
Consensus: All 4 agents agree on BUY
- Fundamental: Strong valuation metrics
- Sentiment: Positive market mood
- Technical: Healthy uptrend
- Risk: Safe entry point
```

## 🔧 Extending the Framework

### Adding a New Agent

```python
from src.agents.base import BaseAgent, AgentOpinion

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__("Custom Agent")
    
    def reason(self, context: str) -> AgentOpinion:
        # Your analysis logic
        recommendation = "BUY"  # or HOLD/SELL
        confidence = 0.7
        reasoning = "My analysis says..."
        return AgentOpinion(
            agent_type=self.agent_type,
            recommendation=recommendation,
            confidence=confidence,
            reasoning=reasoning
        )
    
    def refine(self, opinion: AgentOpinion, peers: list) -> AgentOpinion:
        # How to adjust based on peers
        return opinion  # or modified version
```

### Adding Data to Knowledge Graph

Edit `src/kg/retriever.py` to add more companies or data sources:

```python
MOCK_DATA = {
    "YOUR_TICKER": {
        "company": CompanyNode(...),
        "financials": FinancialData(...),
        "prices": PriceData(...),
        "news": NewsData(...)
    }
}
```

### Integration with Real LLM

Replace mock reasoning with Claude API:

```python
from anthropic import Anthropic

class FundamentalAgentLLM(BaseAgent):
    def __init__(self):
        super().__init__("Fundamental Analyst")
        self.client = Anthropic()
    
    def reason(self, context: str) -> AgentOpinion:
        response = self.client.messages.create(
            model="claude-opus-4-6",
            messages=[{
                "role": "user",
                "content": f"Analyze fundamentals:\n{context}"
            }]
        )
        # Parse response and create AgentOpinion
        ...
```

## 📁 File Structure

```
src/
├── kg/
│   ├── __init__.py
│   └── retriever.py           # Knowledge graph retriever
│
├── agents/
│   ├── __init__.py
│   ├── base.py                # Base agent class
│   ├── fundamental_agent.py   # Valuation analysis
│   ├── sentiment_agent.py     # Sentiment analysis
│   ├── technical_agent.py     # Price trend analysis
│   └── risk_agent.py          # Risk assessment
│
├── reasoning/
│   ├── __init__.py
│   └── debate.py              # Multi-agent debate engine
│
└── ...

demo_mvp.py                     # Complete demo script
MVP_README.md                   # This file
```

## 🧪 Testing

```bash
# Run demo
python demo_mvp.py

# Test with different tickers
python -c "
from demo_mvp import demo_complete_flow
demo_complete_flow('Should I buy VNM?', 'VNM')
"
```

## 🎓 Thesis Framework Mapping

This implementation directly implements the thesis framework:

| Thesis Element | Implementation |
|---|---|
| Query q | Investment question to agents |
| Knowledge Graph G | Mock data in `KGRetriever.MOCK_DATA` |
| Context retrieval Gq = Retrieve(q,G,D) | `KGRetriever.retrieve()` |
| Initial reasoning o_i^(0) | `agent.reason(context)` |
| Debate mechanism o_i^(k) = Refine(...) | `agent.refine(opinion, peers)` |
| K rounds of refinement | `DebateEngine.num_rounds` |
| Final aggregation y = Aggregate({o_i^(K)}) | `DebateEngine._aggregate()` |
| Recommendation | `result.final_recommendation` |

## 🔮 Future Enhancements

1. **Real LLM Integration**: Replace mock reasoning with Claude/GPT API
2. **Live Data**: Connect to real vnstock API instead of mock data
3. **Neo4j Backend**: Store and query from actual knowledge graph
4. **Performance Metrics**: Backtest recommendations against historical data
5. **Portfolio Optimization**: Extend to portfolio-level decisions
6. **Reinforcement Learning**: Learn agent behaviors from feedback
7. **Explainability**: Generate detailed explanation reports
8. **A/B Testing**: Compare agent configurations

## 📚 References

- Thesis: "Enhancing Financial Forecasting with LLMs and Knowledge Graphs"
- Data Structure: See `DATA_STRUCTURE.md`
- Data Puller: See `DATA_PULLER_GUIDE.md`
- Project Overview: See `README.md`

## ❓ FAQ

**Q: Can I use real LLM predictions instead of mock?**
A: Yes! Replace the mock reasoning with actual API calls to Claude or OpenAI.

**Q: How do I add more data to the knowledge graph?**
A: Edit `src/kg/retriever.py` and add more entries to `MOCK_DATA` dictionary.

**Q: Can I use this with real stock data?**
A: Yes! Update the mock data with real data from `data/` folder created by data puller.

**Q: How to evaluate recommendation quality?**
A: Use backtesting against historical prices and compare Sharpe ratio, returns, drawdown.

**Q: Can agents have different debate strategies?**
A: Yes! Override `refine()` method with custom consensus logic in each agent.

---

**Created**: 2026-04-13  
**Thesis Project**: Multi-Agent Trading Framework with LLMs and Knowledge Graphs
