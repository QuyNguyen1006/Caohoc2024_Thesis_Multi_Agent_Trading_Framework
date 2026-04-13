"""Risk manager agent for risk assessment."""

from .base import BaseAgent, AgentOpinion


class RiskAgent(BaseAgent):
    """Manages and assesses investment risks (volatility, debt, market risk)."""

    def __init__(self):
        super().__init__("Risk Manager")

    def reason(self, context: str) -> AgentOpinion:
        """Assess investment risks."""
        # Extract risk metrics
        volatility = self._extract_metric(context, "30-day Volatility:", float)
        debt_to_equity = self._extract_metric(context, "Debt-to-Equity:", float)
        current_ratio = self._extract_metric(context, "Current Ratio:", float)

        # Risk assessment logic
        high_volatility = volatility > 2.5
        high_debt = debt_to_equity > 0.8
        poor_liquidity = current_ratio < 1.2

        risk_score = 0
        if high_volatility:
            risk_score += 1
        if high_debt:
            risk_score += 1
        if poor_liquidity:
            risk_score += 1

        if risk_score >= 2:
            recommendation = "SELL"
            confidence = 0.7
            reasoning = f"High risk profile: Volatility={volatility:.1f}%, Debt/Equity={debt_to_equity:.2f}, Current Ratio={current_ratio:.2f}. Multiple risk factors detected."
        elif risk_score == 1:
            recommendation = "HOLD"
            confidence = 0.65
            reasoning = f"Moderate risk: One risk factor present. Requires careful monitoring. Volatility={volatility:.1f}%"
        else:
            recommendation = "BUY"
            confidence = 0.72
            reasoning = f"Low risk profile: Good fundamentals. Volatility={volatility:.1f}%, Debt/Equity={debt_to_equity:.2f}, Liquidity={current_ratio:.2f} healthy."

        opinion = AgentOpinion(
            agent_type=self.agent_type,
            recommendation=recommendation,
            confidence=confidence,
            reasoning=reasoning,
            reasoning_path={
                "volatility": volatility,
                "debt_to_equity": debt_to_equity,
                "current_ratio": current_ratio,
                "risk_score": risk_score
            }
        )
        self.opinion_history.append(opinion)
        return opinion

    def refine(
        self,
        current_opinion: AgentOpinion,
        peer_opinions: list[AgentOpinion]
    ) -> AgentOpinion:
        """Refine risk assessment based on peer consensus."""
        # Count aggressive recommendations
        aggressive_count = sum(
            1 for o in peer_opinions
            if o.recommendation == "BUY"
        )

        # If many peers say BUY, moderate the SELL recommendation
        if current_opinion.recommendation == "SELL" and aggressive_count >= 2:
            # Risk manager acknowledges peer optimism
            new_recommendation = "HOLD"
            new_confidence = 0.65
            reasoning_addendum = f"\n[Refined: Peers suggest {aggressive_count} BUY calls, moderating risk stance to HOLD]"
        elif current_opinion.recommendation == "BUY":
            new_recommendation = current_opinion.recommendation
            new_confidence = current_opinion.confidence
            reasoning_addendum = "\n[Refined: Risk analysis confirms safe entry point]"
        else:
            new_recommendation = current_opinion.recommendation
            new_confidence = current_opinion.confidence
            reasoning_addendum = ""

        refined = AgentOpinion(
            agent_type=self.agent_type,
            recommendation=new_recommendation,
            confidence=new_confidence,
            reasoning=current_opinion.reasoning + reasoning_addendum,
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
