"""
Adaptive best-response agent for the Iterated Prisoner's Dilemma.

The agent combines four ideas that are evaluated in a fixed order every round:

1. Mirror detection. A deterministic strategy playing against a copy of itself produces
   identical move histories on both sides. That invariant identifies a twin at zero cost and
   locks the pair into permanent mutual cooperation, which is the single most valuable
   matchup in the tournament because self-play contributes two scoring rows to the same agent.
2. Online opponent identification. A library of deterministic opponent models is filtered
   every round against the observed history; any model that fails to reproduce the opponent's
   actual moves is discarded permanently.
3. Best-response planning. A library of candidate policies is simulated against every
   surviving model over the remaining horizon, and the policy with the highest expected
   payoff is played. When no model survives, a memory-one Markov model of the opponent is
   estimated and solved by value iteration.
4. Adaptive probing. Purely cooperative opponents are indistinguishable until provoked, so
   the agent spends exactly one defection to classify them, repairs the relationship
   immediately afterwards, and uses the measured outcome of past probes to decide whether
   probing is still profitable against the current field.
"""

from typing import Callable, Dict, List, Optional, Tuple

from utils.game_core import Agent, COOPERATE, DEFECT

C = COOPERATE
D = DEFECT

try:
    from utils.game_core.payoff import get_config as _get_payoff_config

    _CFG = _get_payoff_config()
    PAYOFF: Dict[Tuple[str, str], int] = {
        (C, C): _CFG.both_cooperate,
        (C, D): _CFG.betrayed_cooperator,
        (D, C): _CFG.betrayer_reward,
        (D, D): _CFG.both_defect,
    }
    REWARD_MUTUAL = _CFG.both_cooperate
except Exception:  # pragma: no cover - fallback if the config cannot be read
    PAYOFF = {(C, C): 3, (C, D): 0, (D, C): 5, (D, D): 1}
    REWARD_MUTUAL = 3


# ---------------------------------------------------------------------------
# Opponent models
#
# Every model is a pure function with the signature
# f(model_moves, my_moves, num_rounds) -> next move of the modelled opponent.
# They must not be Agent subclasses: the tournament loader picks the first class in the
# file that inherits from Agent, so any auxiliary class would shadow the real strategy.
# ---------------------------------------------------------------------------


def m_always_cooperate(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of an unconditional cooperator."""
    return C


def m_always_defect(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of an unconditional defector."""
    return D


def m_tit_for_tat(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of tit-for-tat."""
    return C if not mine else mine[-1]


def m_tit_for_tat_endgame(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of tit-for-tat that defects on the final round."""
    if n and len(theirs) == n - 1:
        return D
    return C if not mine else mine[-1]


def m_grim_trigger(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of an unforgiving strategy that defects forever after one defection."""
    return D if D in mine else C


def m_tit_for_two_tats(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of a strategy that retaliates only after two consecutive defections."""
    return D if len(mine) >= 2 and mine[-1] == D and mine[-2] == D else C


def m_win_stay_lose_shift(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of win-stay lose-shift (Pavlov)."""
    if not mine:
        return C
    if mine[-1] == C:
        return theirs[-1]
    return C if theirs[-1] == D else D


def m_pavlov_endgame(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of win-stay lose-shift that defects on the final round."""
    if n and len(theirs) == n - 1:
        return D
    return m_win_stay_lose_shift(theirs, mine, n)


def m_alternate_from_c(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of a blind alternator that opens with cooperation."""
    return C if len(theirs) % 2 == 0 else D


def m_alternate_from_d(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of a blind alternator that opens with defection."""
    return D if len(theirs) % 2 == 0 else C


def m_flip_own_last(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of an alternator that flips its own previous move, opening with cooperation."""
    if not theirs:
        return C
    return C if theirs[-1] == D else D


def m_flip_own_last_d(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of an alternator that flips its own previous move, opening with defection."""
    if not theirs:
        return D
    return C if theirs[-1] == D else D


def m_majority(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of a strategy that copies the opponent's most frequent move."""
    return D if mine.count(D) > mine.count(C) else C


def m_window_five(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of a strategy that defects after three defections in the last five rounds."""
    return D if len(mine) >= 5 and mine[-5:].count(D) >= 3 else C


def m_second_chance(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of a strategy that retaliates once every two observed defections."""
    counter = 0
    for move in mine:
        if move == D:
            counter += 1
        if counter >= 2:
            counter = 0
    return D if counter >= 2 else C


def m_trust_breaker(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of a strategy that defects as soon as it observes two consecutive cooperations."""
    return D if len(mine) >= 2 and mine[-1] == C and mine[-2] == C else C


def m_earn_trust(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of a strategy that opens with defection and cooperates after any cooperation."""
    if not mine:
        return D
    return C if C in mine else D


def m_suspicious_tit_for_tat(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of tit-for-tat that opens with defection."""
    return D if not mine else mine[-1]


def m_prober(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of a strategy that opens with a fixed probe and then plays tit-for-tat."""
    opening = [D, C, C]
    if len(theirs) < len(opening):
        return opening[len(theirs)]
    return C if not mine else mine[-1]


def m_hard_tit_for_tat(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of a strategy that defects if the opponent defected in either of the last two rounds."""
    return D if mine and D in mine[-2:] else C


def m_cooperate_then_defect(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of a strategy that cooperates once and then defects forever."""
    return C if not theirs else D


def m_conditional_prober(theirs: List[str], mine: List[str], n: Optional[int]) -> str:
    """Model of a tit-for-tat variant that occasionally probes and hardens after two defections."""
    round_number = len(theirs) + 1
    if n and round_number == n:
        return D
    if round_number == 1:
        return C
    if round_number == 2:
        return D if mine[-1] == D else C
    if mine.count(D) > 1:
        return D
    if mine[-1] == D and theirs[-2] == C:
        return D
    if mine[-1] == D and theirs[-2] == D:
        return C
    if mine.count(D) == 1 and theirs.count(D) == 1:
        return C
    if mine.count(D) == 0 and theirs[-1] == C:
        return D
    return C


OPPONENT_MODELS: List[Tuple[str, Callable[[List[str], List[str], Optional[int]], str]]] = [
    ("always_cooperate", m_always_cooperate),
    ("always_defect", m_always_defect),
    ("tit_for_tat", m_tit_for_tat),
    ("tit_for_tat_endgame", m_tit_for_tat_endgame),
    ("grim_trigger", m_grim_trigger),
    ("tit_for_two_tats", m_tit_for_two_tats),
    ("win_stay_lose_shift", m_win_stay_lose_shift),
    ("pavlov_endgame", m_pavlov_endgame),
    ("alternate_from_c", m_alternate_from_c),
    ("alternate_from_d", m_alternate_from_d),
    ("flip_own_last", m_flip_own_last),
    ("flip_own_last_d", m_flip_own_last_d),
    ("majority", m_majority),
    ("window_five", m_window_five),
    ("second_chance", m_second_chance),
    ("trust_breaker", m_trust_breaker),
    ("earn_trust", m_earn_trust),
    ("suspicious_tit_for_tat", m_suspicious_tit_for_tat),
    ("prober", m_prober),
    ("hard_tit_for_tat", m_hard_tit_for_tat),
    ("cooperate_then_defect", m_cooperate_then_defect),
    ("conditional_prober", m_conditional_prober),
]


# ---------------------------------------------------------------------------
# Candidate policies
#
# Every policy is a pure function policy(my_moves, their_moves, round_index) -> move.
# Periodic defection patterns are what exploit opponents that reason about defection
# density or about which move the opponent has played most often.
# ---------------------------------------------------------------------------


def p_always_cooperate(mine: List[str], theirs: List[str], r: int) -> str:
    """Policy that always cooperates."""
    return C


def p_always_defect(mine: List[str], theirs: List[str], r: int) -> str:
    """Policy that always defects."""
    return D


def p_tit_for_tat(mine: List[str], theirs: List[str], r: int) -> str:
    """Policy that mirrors the opponent's previous move."""
    return C if not theirs else theirs[-1]


def p_cooperate_then_defect(mine: List[str], theirs: List[str], r: int) -> str:
    """Policy that cooperates on the first round and defects afterwards."""
    return C if r == 0 else D


def _periodic(pattern: List[str]) -> Callable[[List[str], List[str], int], str]:
    """
    Build a policy that repeats a fixed pattern of moves.

    Parameters:
        pattern: Sequence of moves to repeat.

    Returns:
        A policy function that indexes the pattern by round number.
    """

    def policy(mine: List[str], theirs: List[str], r: int) -> str:
        """Return the pattern move for the current round."""
        return pattern[r % len(pattern)]

    return policy


CANDIDATE_POLICIES: List[Tuple[str, Callable[[List[str], List[str], int], str]]] = [
    ("always_cooperate", p_always_cooperate),
    ("always_defect", p_always_defect),
    ("tit_for_tat", p_tit_for_tat),
    ("cooperate_then_defect", p_cooperate_then_defect),
    ("d1c1", _periodic([D, C])),
    ("c1d1", _periodic([C, D])),
    ("d1c2", _periodic([D, C, C])),
    ("d1c3", _periodic([D, C, C, C])),
    ("d1c4", _periodic([D, C, C, C, C])),
    ("d2c2", _periodic([D, D, C, C])),
    ("d2c3", _periodic([D, D, C, C, C])),
    ("d2c4", _periodic([D, D, C, C, C, C])),
    ("d3c4", _periodic([D, D, D, C, C, C, C])),
]


class DanielAgent(Agent):
    """
    Adaptive agent that identifies the opponent online and plays a best response.

    The strategy is nice by default, provokes each purely cooperative opponent exactly once
    to classify it, repairs the relationship immediately, exploits opponents that tolerate
    defection, protects itself against unforgiving ones, and never defects against a mirror
    image of itself.
    """

    # Probing schedule.
    ADAPTIVE_PROBE = True
    PROBE_ROUND = 6
    LATE_PROBE_FRACTION = 0.75
    WARMUP_MATCHES = 2
    ESCALATE_THRESHOLD = 0.0
    ABANDON_THRESHOLD = -0.25
    OPPONENT_DAMAGE_WEIGHT = 0.0
    REWARD_WINDOW = 15
    REPAIR_LENGTH = 2

    # Planning.
    PLAN_HORIZON = 25
    REPLAN_EVERY = 4
    ENDGAME_ROUNDS = 1

    # Generic memory-one core.
    UNRESPONSIVE_EPSILON = 0.25
    MIN_SAMPLES = 6
    DISCOUNT = 0.98

    # Cross-match memory. Instances are recreated for every pairing but the class object is
    # loaded once per tournament, so this list accumulates the measured value of past probes.
    _probe_rewards: List[float] = []

    def __init__(self, num_rounds: Optional[int] = None):
        """
        Initialise per-match state and choose this match's probing schedule.

        Parameters:
            num_rounds: Number of rounds if the horizon is known, otherwise None.
        """
        super().__init__(num_rounds)
        self.horizon = num_rounds
        self.live_models = [name for name, _ in OPPONENT_MODELS]
        self.plan: Optional[Callable[[List[str], List[str], int], str]] = None
        self.plan_round = -1
        self.is_mirror: Optional[bool] = None
        self.probe_round = self._select_probe_round()
        self.probe_played_at: Optional[int] = None
        self.repair_until = -1
        self.opponent_is_unforgiving = False
        self.reward_slot: Optional[int] = None

    def _select_probe_round(self) -> Optional[int]:
        """
        Decide when, if at all, to spend one defection to classify the opponent.

        The schedule starts optimistic and is downgraded only when past probes have actually
        proved unprofitable against this field.

        Returns:
            The round index of the probe, or None to skip probing in this match.
        """
        rounds = self.horizon or 100
        late = max(2, int(rounds * self.LATE_PROBE_FRACTION))
        if not self.ADAPTIVE_PROBE:
            return self.PROBE_ROUND
        rewards = type(self)._probe_rewards
        if len(rewards) < self.WARMUP_MATCHES:
            return self.PROBE_ROUND
        average = sum(rewards) / len(rewards)
        if average >= self.ESCALATE_THRESHOLD:
            return self.PROBE_ROUND
        if average >= self.ABANDON_THRESHOLD:
            return late
        return None

    def _filter_models(self, mine: List[str], theirs: List[str]) -> List[str]:
        """
        Discard every opponent model that fails to reproduce the observed history.

        Parameters:
            mine: This agent's moves so far.
            theirs: The opponent's moves so far.

        Returns:
            Names of the models still consistent with what the opponent has played.
        """
        survivors = []
        for name, model in OPPONENT_MODELS:
            if name not in self.live_models:
                continue
            consistent = True
            for t in range(len(theirs)):
                try:
                    predicted = model(theirs[:t], mine[:t], self.horizon)
                except Exception:
                    consistent = False
                    break
                if predicted != theirs[t]:
                    consistent = False
                    break
            if consistent:
                survivors.append(name)
        return survivors

    def _simulate(
        self,
        policy: Callable[[List[str], List[str], int], str],
        model: Callable[[List[str], List[str], Optional[int]], str],
        mine: List[str],
        theirs: List[str],
        horizon: int,
    ) -> int:
        """
        Roll a policy forward against a model and accumulate this agent's payoff.

        Parameters:
            policy: Candidate policy for this agent.
            model: Candidate model of the opponent.
            mine: This agent's moves so far.
            theirs: The opponent's moves so far.
            horizon: Number of rounds to simulate.

        Returns:
            Total payoff obtained by this agent over the simulated rounds.
        """
        my_moves, their_moves = list(mine), list(theirs)
        total = 0
        base = len(my_moves)
        for k in range(horizon):
            try:
                mine_next = policy(my_moves, their_moves, base + k)
            except Exception:
                mine_next = C
            try:
                theirs_next = model(their_moves, my_moves, self.horizon)
            except Exception:
                theirs_next = C
            total += PAYOFF[(mine_next, theirs_next)]
            my_moves.append(mine_next)
            their_moves.append(theirs_next)
        return total

    def _plan_best_policy(
        self, mine: List[str], theirs: List[str]
    ) -> Callable[[List[str], List[str], int], str]:
        """
        Choose the policy with the best average payoff across all surviving models.

        Averaging over the surviving set is an implicit hedge: while the opponent's identity
        remains ambiguous, the agent plays what works across every remaining possibility.

        Parameters:
            mine: This agent's moves so far.
            theirs: The opponent's moves so far.

        Returns:
            The selected policy function.
        """
        remaining = (self.horizon - len(mine)) if self.horizon else self.PLAN_HORIZON
        horizon = max(1, min(self.PLAN_HORIZON, remaining))
        models = [model for name, model in OPPONENT_MODELS if name in self.live_models]
        best_policy, best_value = p_tit_for_tat, float("-inf")
        for _, policy in CANDIDATE_POLICIES:
            value = sum(self._simulate(policy, m, mine, theirs, horizon) for m in models)
            value /= len(models)
            if value > best_value:
                best_value, best_policy = value, policy
        return best_policy

    def _memory_one_response(self, mine: List[str], theirs: List[str]) -> str:
        """
        Play the optimal response to a memory-one estimate of the opponent.

        The opponent's conditional cooperation probabilities are estimated with Laplace
        smoothing. If they do not depend on this agent's last move the opponent is
        unresponsive, and defection dominates in every round. Otherwise the two-state Markov
        decision process is solved by value iteration.

        Parameters:
            mine: This agent's moves so far.
            theirs: The opponent's moves so far.

        Returns:
            "C" or "D".
        """
        after_c = after_c_total = after_d = after_d_total = 0
        for i in range(1, len(theirs)):
            if mine[i - 1] == C:
                after_c_total += 1
                after_c += theirs[i] == C
            else:
                after_d_total += 1
                after_d += theirs[i] == C
        p_after_c = (after_c + 1.0) / (after_c_total + 2.0)
        p_after_d = (after_d + 1.0) / (after_d_total + 2.0)

        responsive_samples = after_c_total >= self.MIN_SAMPLES and after_d_total >= self.MIN_SAMPLES
        if responsive_samples and abs(p_after_c - p_after_d) < self.UNRESPONSIVE_EPSILON:
            return D

        values = {C: 0.0, D: 0.0}
        for _ in range(200):
            updated = {}
            for state in (C, D):
                p = p_after_c if state == C else p_after_d
                q_c = p * PAYOFF[(C, C)] + (1 - p) * PAYOFF[(C, D)] + self.DISCOUNT * values[C]
                q_d = p * PAYOFF[(D, C)] + (1 - p) * PAYOFF[(D, D)] + self.DISCOUNT * values[D]
                updated[state] = max(q_c, q_d)
            values = updated

        state = mine[-1] if mine else C
        p = p_after_c if state == C else p_after_d
        q_c = p * PAYOFF[(C, C)] + (1 - p) * PAYOFF[(C, D)] + self.DISCOUNT * values[C]
        q_d = p * PAYOFF[(D, C)] + (1 - p) * PAYOFF[(D, D)] + self.DISCOUNT * values[D]
        return C if q_c >= q_d else D

    def _record_probe_outcome(self, mine: List[str], theirs: List[str]) -> None:
        """
        Update the running estimate of how profitable probing is against this field.

        Parameters:
            mine: This agent's moves so far.
            theirs: The opponent's moves so far.
        """
        if self.reward_slot is None or self.probe_played_at is None:
            return
        start = self.probe_played_at + 1
        window = theirs[start:start + self.REWARD_WINDOW]
        if not window:
            return
        my_average = sum(PAYOFF[(mine[start + i], window[i])] for i in range(len(window)))
        my_average /= len(window)
        their_average = sum(PAYOFF[(window[i], mine[start + i])] for i in range(len(window)))
        their_average /= len(window)
        reward = (my_average - REWARD_MUTUAL)
        reward += self.OPPONENT_DAMAGE_WEIGHT * (REWARD_MUTUAL - their_average)
        type(self)._probe_rewards[self.reward_slot] = reward

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Decide this round's move.

        Parameters:
            own_history: This agent's moves in all previous rounds.
            opponent_history: The opponent's moves in all previous rounds.

        Returns:
            "C" (cooperate) or "D" (defect). Never raises: any internal failure degrades to
            cooperation so that a defect in this agent can never abort the tournament.
        """
        try:
            return self._decide(list(own_history), list(opponent_history))
        except Exception:
            return COOPERATE

    def _decide(self, mine: List[str], theirs: List[str]) -> str:
        """
        Evaluate the decision layers in order and return the chosen move.

        Parameters:
            mine: This agent's moves in all previous rounds.
            theirs: The opponent's moves in all previous rounds.

        Returns:
            "C" or "D".
        """
        r = len(mine)

        # Layer 1: mirror detection. A perfect mirror is a copy of this agent; the status is
        # revocable so that an opponent imitating the signature cannot farm free cooperation.
        if r >= 1 and mine != theirs:
            self.is_mirror = False
        elif self.is_mirror is None and r >= (self.probe_round or 0) + 2:
            self.is_mirror = True
        if self.is_mirror:
            return COOPERATE

        self.live_models = self._filter_models(mine, theirs)

        # Layer 2: endgame. Defecting on the final round is weakly dominant, but never against
        # a mirror, because self-play contributes two scoring rows to this agent.
        if self.horizon and r >= self.horizon - self.ENDGAME_ROUNDS:
            if self.is_mirror is None and mine == theirs:
                return COOPERATE
            return DEFECT

        self._record_probe_outcome(mine, theirs)

        # Layer 3: single classification probe, only against an opponent that has cooperated
        # every round so far. Any opponent that has already defected is informative for free.
        if (
            self.probe_round is not None
            and self.probe_played_at is None
            and r == self.probe_round
            and theirs.count(DEFECT) == 0
        ):
            type(self)._probe_rewards.append(0.0)
            self.reward_slot = len(type(self)._probe_rewards) - 1
            self.probe_played_at = r
            self.repair_until = r + 1 + self.REPAIR_LENGTH
            return DEFECT

        # Layer 4: repair. Unconditional cooperation after the probe restores mutual
        # cooperation with retaliatory opponents and separates them from unforgiving ones.
        if self.probe_played_at is not None and r < self.repair_until:
            return COOPERATE

        if self.probe_played_at is not None and r == self.repair_until:
            after_probe = theirs[self.probe_played_at + 1:]
            if after_probe and all(move == DEFECT for move in after_probe):
                self.opponent_is_unforgiving = True
        if self.opponent_is_unforgiving:
            return DEFECT

        # Layer 5: best-response planning over the surviving models.
        if self.live_models:
            if self.plan is None or r - self.plan_round >= self.REPLAN_EVERY:
                self.plan = self._plan_best_policy(mine, theirs)
                self.plan_round = r
            return self.plan(mine, theirs, r)

        # Layer 6: generic memory-one core for opponents outside the model library.
        self.plan = None
        return self._memory_one_response(mine, theirs)
