"""Fundamental analyst agent for financial analysis."""

from .base import BaseAgent, AgentOpinion


class FundamentalAgent(BaseAgent):
    """Analyzes company fundamentals (financials, valuation, growth)."""

    def __init__(self):
        super().__init__("Fundamental Analyst")

    def reason(self, context: str) -> AgentOpinion:
        """Analyze financial fundamentals."""
        # Simple mock analysis based on P/E ratio and ROE
        pe_ratio = self._extract_metric(context, "P/E Ratio:", float)
        roe = self._extract_metric(context, "ROE:", float)
        pb_ratio = self._extract_metric(context, "P/B Ratio:", float)
        revenue_growth = self._extract_metric(context, "Revenue Growth YoY:", float)

        # Decision logic
        if pe_ratio < 15 and roe > 15 and pb_ratio < 2:
            recommendation = "BUY"
            confidence = 0.75
            reasoning = f"Strong fundamentals: P/E={pe_ratio:.2f} (undervalued), ROE={roe:.1f}% (healthy), Growth={revenue_growth:.1f}%"
        elif pe_ratio > 25 or roe < 10:
            recommendation = "SELL"
            confidence = 0.65
            reasoning = f"Weak fundamentals: High P/E={pe_ratio:.2f} or low ROE={roe:.1f}%"
        else:
            recommendation = "HOLD"
            confidence = 0.55
            reasoning = f"Moderate fundamentals: P/E={pe_ratio:.2f}, ROE={roe:.1f}%, needs monitoring"

        opinion = AgentOpinion(
            agent_type=self.agent_type,
            recommendation=recommendation,
            confidence=confidence,
            reasoning=reasoning,
            reasoning_path={
                "pe_ratio": pe_ratio,
                "roe": roe,
                "pb_ratio": pb_ratio,
                "revenue_growth": revenue_growth
            }
        )
        self.opinion_history.append(opinion)
        return opinion

    def refine(
        self,
        current_opinion: AgentOpinion,
        peer_opinions: list[AgentOpinion]
    ) -> AgentOpinion:
        """Refine fundamental analysis based on peer opinions."""
        # Count peer recommendations
        buy_count = sum(1 for o in peer_opinions if o.recommendation == "BUY")
        sell_count = sum(1 for o in peer_opinions if o.recommendation == "SELL")

        # Adjust confidence based on consensus
        if (current_opinion.recommendation == "BUY" and buy_count >= 2):
            new_confidence = min(1.0, current_opinion.confidence + 0.1)
        elif (current_opinion.recommendation == "SELL" and sell_count >= 2):
            new_confidence = min(1.0, current_opinion.confidence + 0.1)
        else:
            new_confidence = max(0.0, current_opinion.confidence - 0.05)

        refined = AgentOpinion(
            agent_type=self.agent_type,
            recommendation=current_opinion.recommendation,
            confidence=new_confidence,
            reasoning=f"{current_opinion.reasoning}\n[Refined: {buy_count} peers agree BUY, {sell_count} agree SELL]",
            reasoning_path=current_opinion.reasoning_path
        )
        self.opinion_history.append(refined)
        return refined

    @staticmethod
    def _extract_metric(context: str, marker: str, metric_type: type = float) -> float:
        """Extract metric value from context string."""
        try:
            lines = context.split("\n")
            for line in lines:
                if marker in line:
                    # Extract value after the marker
                    parts = line.split(marker)
                    if len(parts) > 1:
                        value_str = parts[1].strip().split()[0].replace("%", "").replace(",", "")
                        return metric_type(value_str)
            return 0.0
        except (ValueError, IndexError):
            return 0.0
