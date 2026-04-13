#!/usr/bin/env python3
"""
Demo MVP: Complete GraphRAG Flow for Investment Decision Making

This demo shows a complete flow from query to result following the thesis framework:

1. Input: Query q (investment decision question)
   └─ Example: "Should I invest in VCB stock?"

2. Knowledge Graph Retrieval: Gq = Retrieve(q, G, D)
   └─ Retrieves company data, financials, prices, news

3. Multi-Agent Reasoning: o_i^(k) = Agent_i(Gq)
   └─ 4 specialized agents analyze from different perspectives

4. Debate Mechanism: o_i^(k) = Refine(o_i^(k-1), {o_j^(k-1)}_{j≠i})
   └─ K rounds of iterative refinement based on peer opinions

5. Final Aggregation: y = Aggregate({o_i^(K)})
   └─ Consensus investment recommendation with confidence score
"""

import json
from typing import Optional

from src.kg.retriever import KGRetriever
from src.agents import FundamentalAgent, SentimentAgent, TechnicalAgent, RiskAgent
from src.reasoning.debate import DebateEngine


def print_header(title: str, level: int = 1) -> None:
    """Print formatted section header."""
    if level == 1:
        print("\n" + "=" * 100)
        print(f"  {title}")
        print("=" * 100 + "\n")
    elif level == 2:
        print(f"\n{'─' * 100}")
        print(f"  {title}")
        print(f"{'─' * 100}\n")
    else:
        print(f"\n  → {title}\n")


def demo_complete_flow(query: str, ticker: str) -> None:
    """
    Run complete MVP flow: query → retrieval → reasoning → result.

    Args:
        query: Investment decision question
        ticker: Stock ticker (VCB, VNM, ACB, etc.)
    """
    print_header("GRAPHRAG INVESTMENT DECISION FRAMEWORK - MVP DEMO", level=1)

    # ========================================================================
    # STAGE 1: QUERY & KNOWLEDGE GRAPH RETRIEVAL
    # ========================================================================
    print_header("STAGE 1: Query & Knowledge Graph Retrieval", level=2)
    print(f"📝 Query: {query}")
    print(f"📊 Ticker: {ticker}\n")

    # Initialize retriever and fetch context
    print("🔍 Retrieving context from Knowledge Graph...")
    retriever = KGRetriever()
    context = retriever.retrieve(query, ticker)

    # Display retrieved context
    print(retriever.format_context(context))

    # ========================================================================
    # STAGE 2: INITIALIZE AGENTS
    # ========================================================================
    print_header("STAGE 2: Initialize Specialized Agents", level=2)
    print("Creating 4 specialized financial analysts:\n")

    agents = [
        FundamentalAgent(),
        SentimentAgent(),
        TechnicalAgent(),
        RiskAgent(),
    ]

    for agent in agents:
        print(f"  ✓ {agent.agent_type:20} - Analyzes {get_agent_focus(agent.agent_type)}")

    # ========================================================================
    # STAGE 3: MULTI-AGENT DEBATE & REASONING
    # ========================================================================
    print_header("STAGE 3: Multi-Agent Debate & Reasoning", level=2)
    print(f"Running GraphRAG debate mechanism with {len(agents)} agents...")
    print(f"Debate rounds (K): 3\n")

    # Format context as string for agents
    context_str = retriever.format_context(context)

    # Run debate engine
    debate_engine = DebateEngine(agents, num_rounds=3)
    result = debate_engine.run_debate(context_str, query, ticker)

    # ========================================================================
    # STAGE 4: FINAL RESULT & ANALYSIS
    # ========================================================================
    print_header("STAGE 4: Final Result & Investment Decision", level=2)

    print("📈 INVESTMENT RECOMMENDATION")
    print("─" * 100)
    print(f"\nRecommendation: {result.final_recommendation}")
    print(f"Confidence Score: {result.final_confidence:.2%}")
    print(f"\nConsensus Reasoning:\n{result.consensus_reasoning}")

    # ========================================================================
    # BONUS: DETAILED ANALYSIS
    # ========================================================================
    print_header("BONUS: Detailed Analysis by Agent", level=2)

    final_opinions = result.debate_history[-1].opinions
    for agent_type, opinion in final_opinions.items():
        print(f"\n🤖 {agent_type}")
        print(f"   Recommendation: {opinion.recommendation}")
        print(f"   Confidence: {opinion.confidence:.2f}")
        print(f"   Reasoning: {opinion.reasoning}")
        if opinion.reasoning_path:
            print(f"   Path Details: {json.dumps(opinion.reasoning_path, indent=6)}")

    # ========================================================================
    # BONUS: DEBATE HISTORY
    # ========================================================================
    print_header("BONUS: Debate History (Round-by-Round Evolution)", level=2)

    for round_data in result.debate_history:
        if round_data.round_num == 0:
            print(f"\n🔵 Initial Analysis (Round 0)")
        else:
            print(f"\n🔵 After Debate Round {round_data.round_num}")

        for agent_type, opinion in round_data.opinions.items():
            print(f"   {agent_type:20} → {opinion.recommendation:5} "
                  f"({opinion.confidence:.2f} confidence)")

    # ========================================================================
    # METHODOLOGY NOTES
    # ========================================================================
    print_header("Methodology Notes", level=2)
    print("""
This MVP demonstrates the GraphRAG framework described in the thesis:

1. **Knowledge Graph Retrieval (Gq = Retrieve(q, G, D))**
   - Fetches relevant company data, financials, prices, news
   - Context includes: company info, financial ratios, technical indicators, sentiment

2. **Multi-Agent Reasoning**
   - Fundamental Analyst: Evaluates P/E, ROE, growth metrics
   - Sentiment Analyst: Analyzes market mood from news signals
   - Technical Analyst: Examines price trends and RSI indicators
   - Risk Manager: Assesses volatility, debt levels, liquidity

3. **Debate Mechanism**
   - Iterative refinement over K rounds (K=3 in this demo)
   - Agents adjust confidence based on peer consensus
   - o_i^(k) = Refine(o_i^(k-1), {o_j^(k-1)}_{j≠i})

4. **Final Aggregation**
   - Majority voting on recommendation
   - Average confidence across agents
   - y = Aggregate({o_i^(K)})

The framework enables more robust investment decisions through:
- Multiple analytical perspectives
- Iterative consensus building
- Explainable reasoning paths
- Risk-aware recommendations
    """)

    print_header("End of Demo", level=1)


def get_agent_focus(agent_type: str) -> str:
    """Get focus area for agent type."""
    focus_map = {
        "Fundamental Analyst": "valuations, growth, profitability",
        "Sentiment Analyst": "market mood, news sentiment, signals",
        "Technical Analyst": "price trends, moving averages, RSI",
        "Risk Manager": "volatility, debt, liquidity risks",
    }
    return focus_map.get(agent_type, "financial metrics")


def main() -> None:
    """Run demo with sample queries."""
    print("\n")
    print("█" * 100)
    print("█" + " " * 98 + "█")
    print("█" + "  GraphRAG: Multi-Agent Investment Decision Framework - MVP Demo".center(98) + "█")
    print("█" + "  Thesis: Enhancing Financial Forecasting with LLMs and Knowledge Graphs".center(98) + "█")
    print("█" + " " * 98 + "█")
    print("█" * 100)

    # Demo scenarios
    demo_cases = [
        ("Should I invest in VCB stock?", "VCB"),
        ("Is VNM a good long-term investment?", "VNM"),
        ("Should I buy ACB stock?", "ACB"),
    ]

    print("\n\nAvailable demo cases:")
    for i, (query, ticker) in enumerate(demo_cases, 1):
        print(f"  {i}. {query} (Ticker: {ticker})")

    # Run first demo case
    query, ticker = demo_cases[0]
    print(f"\n✓ Running demo with: {query}\n")

    demo_complete_flow(query, ticker)


if __name__ == "__main__":
    main()
