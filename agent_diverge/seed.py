"""Seed rolling: a random starting point for a thin brief.

A visual seed gives a making method, colours, layout, type, a verb and a
scale, plus a setting, a region and, half the time, an object. A text seed
gives a voice, a way in and a register. An idea seed gives a verb, a
constraint, a scale and a pressure. Draws from a random.Random instance,
so a fixed seed reproduces the same seed — tests and demos stay stable.
"""

import random

from .moves import (
    IDEA_CONSTRAINTS, IDEA_PRESSURES, IDEA_SCALES, IDEA_VERBS,
    TEXT_REGISTERS, TEXT_VOICES, TEXT_WAYS_IN,
    VISUAL_COLORS, VISUAL_LAYOUTS, VISUAL_METHODS, VISUAL_OBJECTS,
    VISUAL_REGIONS, VISUAL_SCALES, VISUAL_SETTINGS, VISUAL_TYPES,
    VISUAL_VERBS,
)


def _rng(seed):
    return random.Random(seed) if seed is not None else random.Random()


def roll_visual(rng):
    seed = {
        "kind": "visual",
        "method": rng.choice(VISUAL_METHODS),
        "colors": rng.sample(VISUAL_COLORS, 2),
        "layout": rng.choice(VISUAL_LAYOUTS),
        "type": rng.choice(VISUAL_TYPES),
        "verb": rng.choice(VISUAL_VERBS),
        "scale": rng.choice(VISUAL_SCALES),
        "setting": rng.choice(VISUAL_SETTINGS),
        "region": rng.choice(VISUAL_REGIONS),
    }
    if rng.random() < 0.5:
        seed["object"] = rng.choice(VISUAL_OBJECTS)
    return seed


def roll_text(rng):
    return {
        "kind": "text",
        "voice": rng.choice(TEXT_VOICES),
        "way_in": rng.choice(TEXT_WAYS_IN),
        "register": rng.choice(TEXT_REGISTERS),
    }


def roll_idea(rng):
    return {
        "kind": "idea",
        "verb": rng.choice(IDEA_VERBS),
        "constraint": rng.choice(IDEA_CONSTRAINTS),
        "scale": rng.choice(IDEA_SCALES),
        "pressure": rng.choice(IDEA_PRESSURES),
    }


ROLLERS = {"visual": roll_visual, "text": roll_text, "idea": roll_idea}


def roll_seed(kind="visual", seed=None):
    """Roll one seed of the given kind. Raises ValueError on unknown kind."""
    if kind not in ROLLERS:
        raise ValueError("unknown seed kind: %r (visual, text, idea)" % kind)
    return ROLLERS[kind](_rng(seed))


def format_seed(seed):
    """One readable line per seed field."""
    lines = ["seed (%s):" % seed["kind"]]
    for key, value in seed.items():
        if key == "kind":
            continue
        if isinstance(value, list):
            value = ", ".join(value)
        lines.append("  %s: %s" % (key, value))
    return "\n".join(lines)
