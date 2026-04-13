"""Multi-agent debate mechanism for consensus reasoning."""

from dataclasses import dataclass, field
from typing import Optional
from src.agents.base import BaseAgent, AgentOpinion


@dataclass
class DebateRound:
    """Record of one debate round."""
    round_num: int
    opinions: dict[str, AgentOpinion]
    consensus: Optional[str] = None


@dataclass
class DebateResult:
    """Final result of debate."""
    query: str
    ticker: str
    initial_opinions: dict[str, AgentOpinion]
    debate_history: list[DebateRound]
    final_recommendation: str
    final_confidence: float
    consensus_reasoning: str


class DebateEngine:
    """
    Multi-agent debate mechanism for reaching investment consensus.

    Based on the thesis framework where agents iteratively refine opinions
    through multiple rounds of debate (K iterations).
    """

    def __init__(self, agents: list[BaseAgent], num_rounds: int = 3):
        """Initialize debate engine.

        Args:
            agents: List of specialized agents
            num_rounds: Number of debate rounds (K parameter in thesis)
        """
        self.agents = agents
        self.num_rounds = num_rounds
        self.agent_map = {agent.agent_type: agent for agent in agents}

    def run_debate(self, context: str, query: str, ticker: str) -> DebateResult:
        """
        Run multi-agent debate to reach investment consensus.

        Flow:
        1. Initial reasoning: o_i^(0) = Reason(context)
        2. Debate rounds: o_i^(k) = Refine(o_i^(k-1), {o_j^(k-1)}_{j≠i})
        3. Final aggregation: y = Aggregate({o_i^(K)})

        Args:
            context: Knowledge graph context (formatted string)
            query: Investment question
            ticker: Stock ticker

        Returns:
            DebateResult with full debate history and final recommendation
        """
        print(f"\n{'='*80}")
        print(f"DEBATE START: {query}")
        print(f"{'='*80}\n")

        # Stage 1: Initial reasoning by all agents
        print("📊 STAGE 1: Initial Analysis")
        print("-" * 80)
        initial_opinions: dict[str, AgentOpinion] = {}
        for agent in self.agents:
            opinion = agent.reason(context)
            initial_opinions[agent.agent_type] = opinion
            print(f"✓ {opinion.agent_type}")
            print(f"  Recommendation: {opinion.recommendation} (confidence: {opinion.confidence:.2f})")
            print(f"  Reasoning: {opinion.reasoning[:100]}...")
            print()

        # Store debate history
        debate_history: list[DebateRound] = []
        current_round = DebateRound(
            round_num=0,
            opinions=initial_opinions.copy()
        )
        debate_history.append(current_round)

        # Stage 2: Debate rounds (iterative refinement)
        print(f"💬 STAGE 2: {self.num_rounds} Debate Rounds")
        print("-" * 80)
        for round_num in range(1, self.num_rounds + 1):
            print(f"\n🔄 Round {round_num}/{self.num_rounds}")
            refined_opinions: dict[str, AgentOpinion] = {}

            for agent in self.agents:
                current_opinion = current_round.opinions[agent.agent_type]
                peer_opinions = [
                    current_round.opinions[other.agent_type]
                    for other in self.agents
                    if other.agent_type != agent.agent_type
                ]

                # Refine opinion based on peers
                refined = agent.refine(current_opinion, peer_opinions)
                refined_opinions[agent.agent_type] = refined

                # Print refinement
                old_conf = current_opinion.confidence
                new_conf = refined.confidence
                conf_change = new_conf - old_conf
                change_icon = "↑" if conf_change > 0 else "↓" if conf_change < 0 else "="
                print(f"  {agent.agent_type:20} {refined.recommendation:5} "
                      f"(conf: {new_conf:.2f} {change_icon} {abs(conf_change):+.2f})")

            # Create round record
            current_round = DebateRound(
                round_num=round_num,
                opinions=refined_opinions.copy()
            )
            debate_history.append(current_round)

        # Stage 3: Aggregation (final decision)
        print(f"\n🎯 STAGE 3: Final Aggregation")
        print("-" * 80)
        final_recommendation, final_confidence, consensus_reasoning = self._aggregate(
            debate_history[-1].opinions
        )

        print(f"\n✅ FINAL RECOMMENDATION: {final_recommendation}")
        print(f"   Confidence Score: {final_confidence:.2f}/1.0")
        print(f"   Consensus Reasoning:\n   {consensus_reasoning}")

        return DebateResult(
            query=query,
            ticker=ticker,
            initial_opinions=initial_opinions,
            debate_history=debate_history,
            final_recommendation=final_recommendation,
            final_confidence=final_confidence,
            consensus_reasoning=consensus_reasoning
        )

    def _aggregate(self, final_opinions: dict[str, AgentOpinion]) -> tuple[str, float, str]:
        """
        Aggregate final opinions into investment recommendation.

        y = Aggregate({o_i^(K)})

        Args:
            final_opinions: Final opinions from all agents

        Returns:
            Tuple of (recommendation, confidence_score, reasoning)
        """
        # Count votes
        buy_count = sum(1 for o in final_opinions.values() if o.recommendation == "BUY")
        sell_count = sum(1 for o in final_opinions.values() if o.recommendation == "SELL")
        hold_count = sum(1 for o in final_opinions.values() if o.recommendation == "HOLD")

        # Calculate average confidence
        avg_confidence = sum(o.confidence for o in final_opinions.values()) / len(final_opinions)

        # Majority voting
        if buy_count > hold_count and buy_count > sell_count:
            recommendation = "BUY"
        elif sell_count > hold_count and sell_count > buy_count:
            recommendation = "SELL"
        else:
            recommendation = "HOLD"

        # Generate consensus reasoning
        consensus_parts = [
            f"Consensus reached after {self.num_rounds} debate rounds.",
            f"Voting: {buy_count} BUY, {hold_count} HOLD, {sell_count} SELL",
            f"Average confidence: {avg_confidence:.2f}/1.0",
            f"\nKey agent perspectives:",
        ]

        for agent_type, opinion in final_opinions.items():
            consensus_parts.append(
                f"• {agent_type}: {opinion.recommendation} ({opinion.confidence:.2f}) - "
                f"{opinion.reasoning.split(chr(10))[0]}"
            )

        consensus_reasoning = "\n".join(consensus_parts)

        return recommendation, avg_confidence, consensus_reasoning
