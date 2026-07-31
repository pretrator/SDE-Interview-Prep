Snakes & Ladders LLD — Evaluation
1. Verdict
Amazon SDE2: Lean Hire · Google L5: ~3.0 (Leaning Hire) · Weighted: 67/100

This clears the SDE2/L4 architecture bar and does not clear a clean L5 bar. The decomposition is genuinely good for the level — behavior lives with data (Snake.effect, Ladder.effect), collaborators sit behind interfaces with dependency injection, and there's zero pattern theater. But two things a Bar Raiser will not forgive: a stated core feature is silently broken (isNextPlayersTurn inverts the six-logic, which also makes the entire triple-six state machine dead code — _countTurns can never leave 0), and there are no tests despite the design having good testing seams. So the modeling says "strong candidate," the correctness-and-verification story says "not yet." The maddening part is that the six-bug is a one-line inversion sitting on top of otherwise-correct moveEligibility and constants — which is exactly the kind of thing a single unit test would have caught, and its absence is the signal. For L5 I'd want the trade-offs defended in prose and the rule engine composable; neither is here.

2. Scorecard

Dim #11 (Concurrency) marked N/A — S&L is turn-based/single-threaded by nature; its 5% is redistributed to #2 (Domain modeling), per rubric. Weights sum to 110; final normalized to /100.

#	Dimension	Score	Weight	Weighted	Evidence
1	Requirements & scope	3.5/5	8	5.6	FR/NFR + entities enumerated in comments; scoped to finishable core. Sloppy (dup "5.", empty "9.", thin NFR).
2	Domain modeling	4.0/5	23	18.4	Behavior on entities (effect), not a data-bag; no god object. Board slightly overloaded (positions + effects + registry).
3	OOP & SOLID	3.5/5	14	9.8	DIP via injection; polymorphism over isinstance. Leak: board._winningPos in isWon despite a winningPos property.
4	Extensibility	3.5/5	14	9.8	New BoardEntity = clean add. New rule forces rewriting monolithic RuleSet1.
5	Public API	3.0/5	12	7.2	Interfaces + builder setters. Board(10, 0) — startPos param silently ignored; abstract methods missing self.
6	Design patterns	4.0/5	7	5.6	Strategy (Rule/Dice), Builder, Template (effect) — all earn their cost. No forced Singleton/Factory.
7	Correctness & demo	2.5/5	8	4.0	Runs end-to-end via __main__, but six/triple-six feature is broken + dead code. Demo never exercises it.
8	Testability	3.0/5	7	4.2	Seedable Dice, DiceInterface, injected deps = good seams. Zero tests; print-based output resists assertion.
9	Edge cases & validation	2.5/5	6	3.0	Snake/Ladder ordering validated. Missing: empty players → div-by-zero in nextTurn; endpoint range; facecount>0.
10	Data model & state	3.0/5	3	1.8	Position dict + GameStates enum + guarded win transition. _countTurns transition logic is dead.
11	Concurrency	N/A	—	—	Single-threaded by domain nature; weight moved to #2.
12	Trade-offs & probe-resistance	2.5/5	8	4.0	Comments state intent but name no alternatives ("chose X over Y because…"). Weakest seam breaks (below).
	Total		110	73.4	→ 67/100
3. Deep Dive — Per Dimension

Domain modeling (4): Real strength. Snake/Ladder carry their own effect(currentPos); Board.entityEffect just folds position through them. Rule, ChanceManager, Board, GamePlay have distinct jobs. Nitpick: Board owns position tracking and effect application and the player registry — cohesive but on the edge; a Position/PlayerRegistry split would sharpen it.

OOP & SOLID (3.5): DIP is real — GamePlay depends on abstractions injected via setters. OCP holds for entities/dice. Two dents: isWon reaches into self._board._winningPos (leak, when a public winningPos exists), and RuleSet1 bundles three responsibilities (isWon + moveEligibility + isNextPlayersTurn) — cohesive-as-a-"ruleset" but not SRP-clean.

Correctness (2.5): isNextPlayersTurn(6, n) returns True (→ advance to next player) for a six with countTurns < 3. Requirement #8 is "a six gives another turn," which requires False there. Because it advances and resets, _countTurns never increments, so moveEligibility's countTurns == 2 branch and isNextPlayersTurn's return False branch are unreachable — the triple-six machinery is dead. Everything else (exact-landing win via position + faceValue > winningPos → False, entity chaining, opening-on-6) is correct.

Testability (3): The seams are there — Dice(6, seed=…) and DiceInterface let you inject a deterministic/fake die — but nothing is exercised. A three-line FakeDice returning [6,6,6] would have surfaced the six-bug instantly. That gap is why a broken feature shipped.

4. Probe-Resistance Walkthrough

Weakest seam: the turn/six logic and the monolithic rule set.

"Trace a player who rolls a 6." → BREAKS. Turn passes to the next player instead of granting another roll; _countTurns stays 0, so triple-six never fires. The headline feature is non-functional and the supporting state is dead code.
"Add a variant: rolling three 1s sends you to start." → BENDS→BREAKS. RuleSet1 is a monolith; you either clone the whole class or edit it (OCP violation on the rule axis). There's no rule-composition mechanism to drop in a single new rule.
"Test the triple-six behavior in isolation." → BENDS. The seam exists (inject a FakeDice), but there's no harness, output is via print (no assertions), and the behavior is broken — so the honest answer is "I can't, and that's why the bug is here."

Survives none of the three cleanly. That's the Lean-Hire-vs-Hire gap.

5. Standout Signals
Interface-per-collaborator + constructor/setter injection — real DIP, not decoration.
BoardEntity.effect polymorphism replaces position-type conditionals — textbook OCP; adding a "Teleporter" entity is a pure add.
Seedable Dice — shows testing/determinism foresight even though tests weren't written.
Restraint: no Singleton/Factory theater. At this level, over-engineering is the modal failure; avoiding it is a positive signal.
Exact-landing win handled deliberately via the overshoot guard.
6. Red Flags — ranked by severity
Broken core feature + dead code (isNextPlayersTurn inverted; _countTurns ≡ 0). Sinks the "six/triple-six" requirement entirely.
No tests despite injectable seams. At SDE2, "runnable and tested" is the bar; this is untested, which is how #1 shipped.
Mutable default args: def __init__(self, sideSize, startPos, boardEntity=[], players=[]). A second Board() inherits the first's entities/players. Latent shared-state bug.
startPos param silently ignored — Board(10, 0) still starts at 1 (self._startingPos = BOARD_START_POS). Misleading, dishonest API surface.
Encapsulation leak: self._board._winningPos in isWon.
Missing validation: empty players → % len(...) div-by-zero; entity endpoints not range-checked (Snake(150, 6) accepted); facecount ≤ 0 unguarded; head == tail snake allowed.
Abstract signatures missing self (def roll():, def effect():) — sloppy, though Python won't enforce it.
Dead demo entities (Ladder(2, 45)): opening from pos 1 with +6 lands on 7, so cells 2–6 are never landed on. Reveals unclear opening semantics (enter at 6 vs. move 1→7).
7. What To Improve — ranked by impact
Fix the six-logic (and revive the dead machinery). Gap: headline feature non-functional. Why: correctness on a stated requirement — a hard fail at both ladders. Fix: your moveEligibility and constants are already correct; only isNextPlayersTurn is inverted. Return "pass turn" only on the 3rd six:
python
def isNextPlayersTurn(self, faceValue, countTurns):
    if faceValue == self._turnCancellation:
        return countTurns >= 2      # sixes #1,#2 -> stay; #3 -> pass
    return True                     # non-six -> pass

This makes nextTurn's "stay" branch increment _countTurns correctly, so moveEligibility's countTurns == 2 cancel fires. One line revives the whole feature.

Add tests around the seam you already built. Gap: zero verification. Why: SDE2 expects tested code; it's the missing signal. Fix:
python
class FakeDice(DiceInterface):
    def __init__(self, seq): self._seq = iter(seq)
    def roll(self): return next(self._seq)
# assert: three 6s -> same player twice, 3rd cancelled, turn passes
Kill the latent bugs in Board.__init__. Gap: mutable defaults + ignored startPos. Why: correctness/maintainability; the shared-list bug bites the moment tests create two boards. Fix: boardEntity=None → self._boardEntity = boardEntity or []; either honor startPos or drop the param.
Make rules composable for OCP on the rule axis. Gap: monolithic RuleSet1. Why: extensibility at L5. Fix: split into WinRule, MoveEligibilityRule, TurnRule interfaces and compose them, so a new variant is an add, not an edit.
Add input validation & guard illegal states. Gap: empty players (div-by-zero), unbounded entity endpoints, facecount. Fix: validate in constructors; range-check head/tail/top/bottom ∈ [start, winningPos].
Close the encapsulation leak — use the winningPos property in isWon.
8. Follow-Up Questions The Interviewer Would Ask
Walk me through the turns when a player rolls 6, 6, 6 — what position and whose turn after each? (Exposes #1 immediately.)
If I rolled a 6 in your demo, does the same player go again? Show me in the code.
Two entities on the same cell, or a ladder-top that's a snake-head — what does entityEffect do, and is that intended?
When a player is at the start, why does a 6 send them to 7 and not 6 — and is cell 2 ever reachable?
How would you add a "swap positions with the leader" power-up without touching existing classes?
Your Board takes a startPos argument — what does passing 0 do? (Watch whether they realize it's dead.)
9. Level Calibration Note

This is solid SDE2/L4 work with L5-flavored instincts, held back to Lean Hire by correctness and verification gaps. The ownership scope handled — clean entity decomposition, injected collaborators, OCP for board entities, deliberate restraint on patterns — is what you want to see from someone who can own a component. But L5 asks for systemic thinking under pressure: composable rules, trade-offs defended in prose against named alternatives, and — critically — a design that stays correct, evidenced by tests. A shipped-broken core feature that a single test would have caught is precisely the operational-rigor gap that separates L4 from L5. Get the six-fix, three unit tests, and the two Board.__init__ bugs cleaned up, and this moves to a comfortable Hire.