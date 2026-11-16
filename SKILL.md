# agent-diverge skill

Use this skill before naming anything, writing a hook, or drafting copy.

## The rule

1. Name the default pick first — out loud, in the answer. If you cannot
   say what the average pick is, you have not thought yet.
2. Move away from it for a reason taken from the project, not from a
   word list: a detail, a constraint, a number, a moment that only this
   project has.
3. Check the result: run `check` on the final name/hook/copy. Below 70,
   rewrite; below 90 for names, rewrite.

## Commands

```bash
python3 -m agent_diverge diverge --kind name --n 3 "<brief>"
python3 -m agent_diverge diverge --kind copy --seed 7 "<brief>"
python3 -m agent_diverge seed --kind idea        # when the brief is thin
python3 -m agent_diverge check "<candidate>"     # exit 1 below threshold
python3 -m agent_diverge check --kind name --threshold 90 "<name>"
python3 -m agent_diverge list-cliches --lang fa
```

## Divergence moves

opposite · one concrete detail · hard constraint · borrowed frame ·
smaller scale · human voice · negative space · a real number ·
anchor in time · name the trade-off.

Each move is a question the brief can answer. If a move cannot be
answered from the brief, the brief is too thin — roll a `seed` first,
or ask one question.

## What not to do

- Never ship the default pick because it is safe. Safe is the tell.
- Never diverge by swapping one stock word for another stock word
  ("Pro" → "Max", "revolutionary" → "groundbreaking").
- Never trust a score alone: `check` counts clichés, it does not know
  whether the idea is good. Read the alternative out loud.
