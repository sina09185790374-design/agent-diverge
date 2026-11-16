"""Divergence moves: the ways out of the average pick.

Each move is a named operation with a question. The move does not invent
content — it points at the brief and asks for one concrete thing from it
(a detail, a constraint, a number, a moment). That is what keeps the
divergence grounded in the project instead of random.
"""

MOVES = [
    {
        "id": "opposite",
        "name": "Opposite",
        "question": "What is the exact opposite of the default pick — and what would it cost?",
    },
    {
        "id": "specific",
        "name": "One concrete detail",
        "question": "Replace the abstract claim with one real detail from the project.",
    },
    {
        "id": "constraint",
        "name": "Hard constraint",
        "question": "What if it had to fit in one word, one colour, one verb?",
    },
    {
        "id": "borrowed",
        "name": "Borrowed frame",
        "question": "Describe it as if it were a kitchen, a workshop, a sport, a street.",
    },
    {
        "id": "smaller",
        "name": "Smaller scale",
        "question": "Shrink it to one person, one moment, one object.",
    },
    {
        "id": "voice",
        "name": "Human voice",
        "question": "How would one person say this to another, out loud, in one breath?",
    },
    {
        "id": "not",
        "name": "Negative space",
        "question": "Say what it is NOT — the honest exclusion is often the identity.",
    },
    {
        "id": "number",
        "name": "A real number",
        "question": "Put a real number in it: a count, a time, a price, a limit.",
    },
    {
        "id": "time",
        "name": "Anchor in time",
        "question": "Pin it to a time: a morning, a deadline, a first try, a last chance.",
    },
    {
        "id": "tension",
        "name": "Name the trade-off",
        "question": "What does this give up? Name the trade-off instead of hiding it.",
    },
]

# Seed vocabularies, mirroring antialgorithm's seed.py: a starting point
# drawn from system randomness so two people with the same prompt start
# in different places. Deterministic when a seed is given.
VISUAL_METHODS = ["print", "paint", "stamp", "ink", "screen", "photo", "render", "collage"]
VISUAL_COLORS = ["ochre", "ink black", "paper white", "oxide red", "deep teal",
                 "mustard", "slate", "forest", "brick", "navy"]
VISUAL_LAYOUTS = ["one big block", "off-centre", "diagonal", "grid broken once",
                  "full-bleed image", "type only", "split in two"]
VISUAL_TYPES = ["heavy grotesque", "hand-drawn", "monospace", "condensed caps",
                "serif with bite", "single weight only"]
VISUAL_VERBS = ["stack", "cut", "fold", "pour", "stamp", "peel", "lean", "repeat"]
VISUAL_SCALES = ["postage stamp", "poster", "billboard", "phone screen", "book cover"]
VISUAL_SETTINGS = ["a night market", "a workshop at 2am", "a bus stop", "a kitchen table",
                   "a rooftop", "a repair shop", "a school yard"]
VISUAL_REGIONS = ["north", "south", "the coast", "the mountains", "the old town",
                  "the industrial edge"]
VISUAL_OBJECTS = ["a key", "a kettle", "a ladder", "a radio", "a ticket", "a spool of wire"]

TEXT_VOICES = ["plainspoken", "wry", "urgent", "tender", "blunt", "playful", "formal"]
TEXT_WAYS_IN = ["a confession", "a question", "a small scene", "a number",
                "a contradiction", "a memory"]
TEXT_REGISTERS = ["street", "workshop", "letter to a friend", "field note",
                  "instruction manual", "diary"]

IDEA_VERBS = ["hide", "carry", "trade", "wait", "break", "repair", "follow", "lose"]
IDEA_CONSTRAINTS = ["one room", "one hour", "one tool", "no words", "two people",
                    "one mistake allowed"]
IDEA_SCALES = ["a single street", "a lifetime", "a lunch break", "a season"]
IDEA_PRESSURES = ["a deadline", "a debt", "a promise", "a storm coming",
                  "someone watching", "running out"]
