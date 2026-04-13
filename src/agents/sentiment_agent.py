"""Sentiment analyst agent for market sentiment analysis."""

from .base import BaseAgent, AgentOpinion


class SentimentAgent(BaseAgent):
    """Analyzes market sentiment from news and social signals."""

    def __init__(self):
        super().__init__("Sentiment Analyst")

    def reason(self, context: str) -> AgentOpinion:
        """Analyze sentiment from news and market signals."""
        # Extract sentiment score from context
        sentiment_score = self._extract_sentiment(context)

        # Decision logic based on sentiment
        if sentiment_score > 0.6:
            recommendation = "BUY"
            confidence = 0.7
            reasoning = f"Positive sentiment: {sentiment_score:.2f}/1.0. Market buzz and recent news are bullish. Strong positive indicators."
        elif sentiment_score < 0.3:
            recommendation = "SELL"
            confidence = 0.65
            reasoning = f"Negative sentiment: {sentiment_score:.2f}/1.0. Recent news and market mood are bearish. Caution advised."
        else:
            recommendation = "HOLD"
            confidence = 0.6
            reasoning = f"Neutral sentiment: {sentiment_score:.2f}/1.0. Mixed signals from market. Wait for clarity."

        opinion = AgentOpinion(
            agent_type=self.agent_type,
            recommendation=recommendation,
            confidence=confidence,
            reasoning=reasoning,
            reasoning_path={
                "sentiment_score": sentiment_score
            }
        )
        self.opinion_history.append(opinion)
        return opinion

    def refine(
        self,
        current_opinion: AgentOpinion,
        peer_opinions: list[AgentOpinion]
    ) -> AgentOpinion:
        """Refine sentiment analysis based on peer perspectives."""
        # If fundamental and technical agents agree, boost confidence
        agreement_count = sum(
            1 for o in peer_opinions
            if o.recommendation == current_opinion.recommendation
        )

        if agreement_count >= 2:
            new_confidence = min(1.0, current_opinion.confidence + 0.12)
        else:
            new_confidence = max(0.0, current_opinion.confidence - 0.08)

        refined = AgentOpinion(
            agent_type=self.agent_type,
            recommendation=current_opinion.recommendation,
            confidence=new_confidence,
            reasoning=f"{current_opinion.reasoning}\n[Refined: {agreement_count} agents align with {current_opinion.recommendation}]",
            reasoning_path=current_opinion.reasoning_path
        )
        self.opinion_history.append(refined)
        return refined

    @staticmethod
    def _extract_sentiment(context: str) -> float:
        """Extract sentiment score from context."""
        try:
            lines = context.split("\n")
            for line in lines:
                if "Sentiment Score:" in line:
                    parts = line.split("Sentiment Score:")
                    if len(parts) > 1:
                        value_str = parts[1].split("/")[0].strip()
                        return float(value_str)
            return 0.5  # Default neutral
        except (ValueError, IndexError):
            return 0.5
