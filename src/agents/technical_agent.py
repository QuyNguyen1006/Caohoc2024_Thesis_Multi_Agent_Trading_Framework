"""Technical analyst agent for price and trend analysis."""

from .base import BaseAgent, AgentOpinion


class TechnicalAgent(BaseAgent):
    """Analyzes price trends, moving averages, and technical indicators."""

    def __init__(self):
        super().__init__("Technical Analyst")

    def reason(self, context: str) -> AgentOpinion:
        """Analyze technical indicators."""
        # Extract technical metrics
        current_price = self._extract_metric(context, "Current Price:", float)
        ma20 = self._extract_metric(context, "MA20:", float)
        ma50 = self._extract_metric(context, "MA50:", float)
        rsi = self._extract_metric(context, "RSI:", float)

        # Decision logic
        # Price above MAs = uptrend
        above_ma20 = current_price > ma20
        above_ma50 = current_price > ma50
        rsi_overbought = rsi > 70
        rsi_oversold = rsi < 30

        if above_ma20 and above_ma50 and 40 < rsi < 70:
            recommendation = "BUY"
            confidence = 0.72
            reasoning = f"Strong uptrend: Price above both MAs, RSI={rsi:.1f} (healthy bullish momentum)"
        elif not above_ma50 and rsi < 40:
            recommendation = "SELL"
            confidence = 0.68
            reasoning = f"Downtrend confirmed: Price below MA50, RSI={rsi:.1f} (weak momentum)"
        elif rsi_overbought:
            recommendation = "SELL"
            confidence = 0.6
            reasoning = f"Overbought condition: RSI={rsi:.1f} > 70, correction likely"
        elif rsi_oversold:
            recommendation = "BUY"
            confidence = 0.65
            reasoning = f"Oversold condition: RSI={rsi:.1f} < 30, bounce likely"
        else:
            recommendation = "HOLD"
            confidence = 0.58
            reasoning = f"Mixed signals: Price at MA20, RSI={rsi:.1f}, trend unclear"

        opinion = AgentOpinion(
            agent_type=self.agent_type,
            recommendation=recommendation,
            confidence=confidence,
            reasoning=reasoning,
            reasoning_path={
                "current_price": current_price,
                "ma20": ma20,
                "ma50": ma50,
                "rsi": rsi,
                "above_ma20": above_ma20,
                "above_ma50": above_ma50
            }
        )
        self.opinion_history.append(opinion)
        return opinion

    def refine(
        self,
        current_opinion: AgentOpinion,
        peer_opinions: list[AgentOpinion]
    ) -> AgentOpinion:
        """Refine technical analysis considering peer analysis."""
        # If risk manager or fundamental analyst warn, lower confidence on aggressive calls
        risk_warnings = sum(1 for o in peer_opinions if o.agent_type == "Risk Manager" and o.recommendation == "SELL")

        if current_opinion.recommendation == "BUY" and risk_warnings > 0:
            new_confidence = max(0.0, current_opinion.confidence - 0.15)
        elif current_opinion.recommendation == "SELL" and risk_warnings > 0:
            new_confidence = min(1.0, current_opinion.confidence + 0.1)
        else:
            new_confidence = current_opinion.confidence

        refined = AgentOpinion(
            agent_type=self.agent_type,
            recommendation=current_opinion.recommendation,
            confidence=new_confidence,
            reasoning=f"{current_opinion.reasoning}\n[Refined: Risk factor adjustment applied]",
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
                    parts = line.split(marker)
                    if len(parts) > 1:
                        value_str = parts[1].strip().split()[0].replace("%", "").replace(",", "")
                        return metric_type(value_str)
            return 0.0
        except (ValueError, IndexError):
            return 0.0
