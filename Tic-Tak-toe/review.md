# LLD Interview Review — Tic-Tac-Toe

**Reviewer stance:** Staff/Principal-level, calibrated to top-tier product bars (Google, Amazon, Microsoft, Uber, Stripe, Atlassian).

**Scope note:** `input()` in `Player` and `print()` in `Board` are treated as scaffolding per the candidate's clarification and excluded from the SRP/testability critique. The candidate is still held to the abstraction that scaffolding was standing in for (notably, the missing `Move` object). Correctness bugs are de-prioritized; this is a *design* review.

---

## 1. Requirement Coverage — 6/10

Core functional requirements are met:

- 3×3 board (`Board` with `BOARD_SIZE`)
- Exactly two players
- Alternating turns via `ChanceManager.nextChance`
- Game halts on win/draw (`GamePlayManager.playGame` loop guard)
- Three states modeled (`BoardStates`: ONGOING / WON / DRAW)
- Symbol-per-player
- "Start with O" — traced through `ChanceManager.sortPlayer`, seats CIRCLE first correctly

**Design-level gaps (not incidental):**

- **Reset (NFR #3) has no home in the design.** Not merely unimplemented — there is no `Move` history, no `reset()` on any class, and `Board`/`GamePlayManager` hold mutable state with no re-initialization path. A missing *capability*, not a missing line.
- **Symbol-uniqueness validation is absent**, despite the candidate's own comment flagging it in `Player`. Nothing prevents two X players; `ChanceManager.sortPlayer` would then be undefined.
- **"Who won" is not a first-class outcome.** `Rules.getBoardState` returns `WON` but not the winner; `GamePlayManager` infers it as the current player. The requirement is satisfied by inference rather than by design.

---

## 2. Object-Oriented Design — 6/10

**Responsibilities:** Correct carve-up — `Board` (state), `Player` (identity), `Rules` (evaluation), `ChanceManager` (turn order), `GamePlayManager` (orchestration). Right seam set; the strongest asset.

**Abstraction:** Undermined by hollow interfaces. `PlayerInterface(ABC): pass` and `ChanceManagerInterface(ABC): pass` declare no methods — labels, not contracts. Meanwhile `GamePlayManager`, the collaborator that most benefits from a contract, has none. Abstraction is present where it's empty and absent where it matters.

**Encapsulation:** Leaked. `Board.getBoard()` returns the internal list by reference, so `Rules` (or any caller) can mutate board state through a read accessor.

**Cohesion:** Mostly good. One violation: `ChanceManager.sortPlayer` mixes round-robin iteration with *starting-order policy* and reaches into `Symbol.CIRCLE` to enforce it. Two responsibilities, one class.

**Coupling:** `ChanceManager` is coupled to a specific symbol value; `GamePlayManager` is temporally coupled to turn order (must read winner *before* `nextChance`).

**Naming:** Clear and consistent (`addMark`, `getBoardState`, `nextChance`). Minor: `RulesSet1` is a weak name — name a strategy by behavior, not by ordinal.

---

## 3. SOLID Principles — 6/10

**SRP — partial.** Discounting I/O: `ChanceManager` still carries two reasons to change (cycling + starting policy). `GamePlayManager` owns orchestration *and* winner-derivation. *Impact:* changing "who starts" edits the turn iterator; changing win-attribution edits the loop. *Suggestion:* move starting-order upstream of the iterator; let the evaluation layer surface the winner.

**OCP — followed, and well.** `RulesInterface` + `RulesSet1` lets a new ruleset drop in without touching the engine. The principle that matters most here, and the seam is placed correctly. *Caveat:* the diagonal logic generalizes to N×N while the FR fixes 3×3 — a dimension opened that the requirements didn't ask for.

**LSP — vacuously "passed."** Empty base interfaces mean no behavioral contract to violate — an absence, not a strength.

**ISP — not really exercised.** Interfaces are empty or single-method; no fat interfaces, but no evidence of deliberate segregation. Neutral.

**DIP — followed, and a highlight.** `GamePlayManager` receives `board`, `players`, `rules`, `chanceManager` via constructor injection, wired at a composition root in `__main__`, depending on `RulesInterface` not `RulesSet1`. Genuine inversion. *One leak:* `ChanceManager.sortPlayer` references the module-global `players` instead of `self._players` — a concrete dependency on ambient state that breaks the otherwise-clean injection story.

---

## 4. Design Patterns — 6.5/10

**Correctly applied:** Strategy (`RulesInterface` / `RulesSet1`) — the single most appropriate pattern for this problem, at the right seam. Full credit.

**Genuinely applicable but absent:**

- **State pattern** for `BoardStates` transitions. Currently an enum with scattered `if` checks in `playGame`. For three states this is a *defensible* simplification — not forced — but the candidate should articulate choosing enum over State deliberately.
- **A `Move` / Command-style object.** Its absence is the root cause of reset/undo having nowhere to live. The one missing pattern worth pushing on, because it unlocks a stated requirement.

Correctly did **not** force Factory or Observer.

---

## 5. Extensibility — 6/10

Axis by axis:

| Axis of change | Open / Closed | Why |
|---|---|---|
| New ruleset | **Open** | Strategy seam at `RulesInterface`. Excellent. |
| New player type (AI/remote) | Partially closed | Move-acquisition seam scaffolded inside `Player`, not modeled. |
| New UI (GUI/web/API) | Closed | Presentation lives in `Board.printBoard` + domain. |
| Undo / reset | Closed | No `Move`, no history. |
| N players | Mostly open | `ChanceManager` cycles N via modulo, but `Symbol` + O-first rule assume two. |

Genuinely extensible on the rules axis, closed on the axes most interviews probe. The concern is not the closure — it's *advertising* "good extensibility" without scoping which axis. Naming the boundary honestly scores better than the blanket claim.

---

## 6. Maintainability — 6/10

- **Readability:** Good — small classes, clear names, linear flow.
- **Modularity:** Good seams.
- **Testability:** Improved once I/O is removed as intended, but still hampered by the absence of a `Move` value object — you can only assert on board-mutation side-effects, not on "the move that was made."
- **Dependency management:** Strong via constructor injection, marred by the `sortPlayer` global reference.
- **Separation of concerns:** Mostly clean except presentation-in-`Board` and policy-in-`ChanceManager`.

---

## 7. Performance — 7/10

`Rules` rescans the full board each turn — O(n²) per move. For a fixed 3×3 this is a non-issue and should **not** be optimized; O(1) counters here would be premature. The real note is a design trade-off (see Trade-offs below): a **stateless** `Rules` structurally precludes incremental O(1) detection, because that needs per-game state. Choosing the clean stateless interface *is* choosing the rescan. Minor redundancy: the diagonal is effectively evaluated twice.

---

## 8. Error Handling — 4.5/10

Weakest axis. `addMark` returns a boolean to signal an occupied cell — good intent — but no caller consumes it, so illegal moves aren't rejected at the design level; there's no validation seam and no notion of a rejected-move outcome. No bounds guarding on positions. No defensive copy on `getBoard`. The `sortPlayer` global reference is a latent failure under any non-`__main__` composition. Essentially no defensive-programming layer or error-signaling contract.

---

## 9. Interview Feedback

**Strengths**
- Requirements written down first.
- Correct decomposition.
- Strategy at the right seam.
- Real dependency injection via a composition root.
- Clean, readable naming.

**Weaknesses**
- Decorative empty interfaces.
- Missing `Move` / `GameResult` domain objects.
- Winner derived by inference.
- Starting-order policy fused into the turn iterator.
- Encapsulation leak via `getBoard`.
- Two stated requirements (reset, uniqueness) with no structural home.

**Would impress:** the DI / composition-root discipline and the Strategy seam — mid-to-senior signals.

**Would raise concern:** empty interfaces (patterns applied by ritual) and the absence of a `Move` object (domain model not fully mined). Both are things a strong candidate catches themselves.

---

## Scorecard

| Dimension | Score |
|---|---|
| Requirement Coverage | 6/10 |
| OOP Design | 6/10 |
| SOLID Principles | 6/10 |
| Design Patterns | 6.5/10 |
| Extensibility | 6/10 |
| Maintainability | 6/10 |
| Performance | 7/10 |
| Code Quality | 5/10 |
| Overall Design | 6/10 |
| **Overall** | **61/100** |

---

## Hiring Recommendation: **Lean Hire**

The decomposition is correct and the two decisions that most separate signal from noise — Strategy for `Rules` and constructor injection at a composition root — are present and genuine, not cargo-culted. That floor rules out a No-Hire.

What holds it below a clean Hire is a consistent pattern of abstractions that aren't load-bearing: empty `PlayerInterface` / `ChanceManagerInterface`, a winner that's inferred rather than modeled, no `Move` object (leaving reset — a stated NFR — with nowhere to live), and policy leaking into `ChanceManager.sortPlayer`. Individually minor; together they indicate the design was carved correctly but not *pressure-tested* by the candidate against its own claims.

The distance from Lean Hire to Hire is short and mostly subtractive/relocative: make the interfaces real or delete them, introduce `Move` / `GameResult`, lift starting-order out of the iterator. A candidate who did those *and* narrated the trade-offs below would be a solid **Hire**.

---

## The Three Trade-offs to Narrate in the Room

Each is a place where the design silently picked a side. The senior signal is naming the trade and the condition under which it flips — not picking the "right" side.

### 1. Stateless Strategy vs. O(1) win detection
`Rules` is stateless and rescans the board each call. Upside: a clean, swappable Strategy with no game state to carry — the reason the OCP seam is tidy. Cost: it structurally rules out incremental O(1) detection (per-row/column/diagonal counters), which *needs* per-game state. Choosing the stateless interface *is* choosing O(n²). Correct at 3×3; flip it only when board size makes the rescan hurt.

### 2. Enum-with-conditionals vs. the State pattern
`BoardStates` is an enum driven by scattered `if` checks in `playGame`. Upside: simplicity — three states don't justify three state classes; State here would be over-engineering. Cost: transition logic isn't localized, so a new state ("paused", "forfeited") means editing the orchestrator. Fine trade — just signal it was deliberate.

### 3. N×N generality vs. a fixed-3×3 spec
The win-check generalizes to arbitrary N×N, but FR #1 fixes 3×3. Upside: a more reusable evaluator. Cost: a dimension opened beyond the spec — more surface area, more edge cases, and where the diagonal logic got fragile. The one trade to *question* rather than credit: generalizing beyond spec can read as forward-thinking or as undefended scope. Justify why the generality earns its keep, or scope back to 3×3.

---

## Concept Reference (from the discussion)

### What "OCP seam" means
A **seam** (Michael Feathers) is a point where you can change behavior without editing the code on either side. An **OCP seam** is the specific boundary through which Open/Closed operates — the line you extend across while the other side stays closed.

In this design the seam is `RulesInterface`:

```
GamePlayManager  ──depends on──▶  RulesInterface  ◀──implements──  RulesSet1
   (closed side)                    (the seam)                    (open side)
```

Add a new ruleset by implementing `RulesInterface` and injecting it; `GamePlayManager` never changes. OCP is always relative to an *axis of change*, and the seam is where that axis lives. This design has a seam on the rules axis and **no seam** on the player-type or UI axes — which is precisely why it's open on the first and closed on the others.

### What "optimal detection" means
Win-detection is answering "did the last move complete a line?" after each move. **Optimal = O(1) per move** via incremental counters instead of an O(n²) rescan.

A move only affects its own row, column, and (at most) the two diagonals. Keep a signed counter per row/column/diagonal; one player is `+1`, the other `−1`. On a mark at `(r, c)`:

```
row[r]    += delta
col[c]    += delta
if r == c:        diag     += delta
if r + c == n-1:  antiDiag += delta

win  ⟺  abs(any touched counter) == n
```

Constant time, independent of board size. The catch: this requires the detector to hold state across moves — which is why it conflicts with the stateless `Rules` (Trade-off #1). Correct choice at 3×3 is the rescan; know the O(1) version so you can answer "what if the board were enormous?"

### Is a stateful `Rules` bad design?
No — not inherently. State is only a smell when it's *unnecessary, hidden, or shared*. Counter state is essential, owned by one object, and scoped to one game — same category as `Board`'s grid or `ChanceManager._currentChance`.

What genuinely changes if `Rules` becomes stateful:

1. **Lifecycle coupling** — the detector is bound to one game and must be fed *every* move *in order*; skip or replay a move and counters silently desync.
2. **Interface contract shifts** — from "given this board, what's the state?" to "given this move, what's the state now?" A more faithful domain model, but a heavier, less trivially swappable contract.
3. **Testability shifts both ways** — you lose isolated single-board tests but gain direct tests of incremental logic.

Verdict: a legitimate design *provided the state is contained* — fed through one path, unable to accept a raw board, ideally rebuildable from move history. What makes it *bad* is letting the counters desync from the board: a fast wrong answer is worse than a slow right one. The impressive framing: *"I'd make `Rules` stateful only when O(n²) hurts, accepting the lifecycle constraint that it must see every move in order. At 3×3 that trade isn't worth it; at scale it is."*