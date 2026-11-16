# Verified runs

All output below is from real CLI runs (2026-11-16).

## diverge — name

```
$ python3 -m agent_diverge diverge --kind name --n 3 --seed 7 "a cozy tea house in Arak"
Brief: a cozy tea house in Arak
Kind: name (en)

The default pick (the average answer):
  Arak Pro
  Why it is average: a topic word plus a stock name ingredient

Divergent alternatives:
  1. [Human voice] Say arak the way you would say it to a friend, in one breath.
     Ask: How would one person say this to another, out loud, in one breath?
     grounded in the brief's word 'arak'
  2. [Hard constraint] One word, one colour: say arak in a five-word sentence. — seed: wait
     Ask: What if it had to fit in one word, one colour, one verb?
     grounded in the brief's word 'arak'
  3. [Negative space] Say what arak is NOT; the honest exclusion is the identity. — seed: cut
     Ask: Say what it is NOT — the honest exclusion is often the identity.
     grounded in the brief's word 'arak'
```

## check — clichéd copy fails, clean copy passes

```
$ python3 -m agent_diverge check "In today's fast-paced world, our cutting-edge solution leverages synergy to unlock seamless results."
Score: 64/100 (threshold 70) — FAIL
Cliche hits (6):
  - in today's fast-paced world
  - cutting-edge
  - leverage
  - seamless
  - synergy
  - unlock
(exit 1)

$ python3 -m agent_diverge check "The kettle whistles at six."
Score: 100/100 (threshold 70) — PASS
No cliche hits.
(exit 0)
```

## check — a stock name is flagged

```
$ python3 -m agent_diverge check --kind name "Game Pro Hub"
Score: 88/100 (threshold 70) — PASS
Cliche hits (2):
  - name-filler:pro
  - name-filler:hub
```

Two filler ingredients still pass the default threshold — raise it for
names (`--threshold 90`) when the name must carry no stock parts.

## seed — idea

```
$ python3 -m agent_diverge seed --kind idea --seed 5
seed (idea):
  verb: break
  constraint: one mistake allowed
  scale: a lunch break
  pressure: running out
```
