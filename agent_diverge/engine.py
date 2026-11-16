"""Core logic: name the default pick, diverge from it, score a candidate.

The default pick is built from the brief's own words plus the cliche
catalog — it is the answer the model (or a tired human) reaches first.
The alternatives are not random text: each one applies a divergence move
to the brief and names the reason, grounded in a concrete word taken
from the brief itself.
"""

import random
import re

from .cliches import (
    EN_CLICHES, EN_NAME_FILLER, FA_CLICHES, FA_NAME_FILLER,
    detect_language, find_cliches, name_filler_hits,
)
from .moves import MOVES
from .seed import roll_seed

EN_STOPWORDS = {
    "a", "an", "the", "for", "of", "and", "or", "to", "in", "on", "with",
    "my", "our", "your", "is", "are", "it", "this", "that", "we", "i",
    "about", "make", "made", "new", "app", "website", "site",
}
FA_STOPWORDS = {
    "و", "در", "به", "از", "که", "را", "با", "برای", "یک", "این", "آن",
    "ما", "من", "است", "های", "ها", "می", "تا", "یا", "روی", "چون",
}

DEFAULT_NAME_FILLER_EN = ["Pro", "Hub", "Max", "Smart"]
DEFAULT_NAME_FILLER_FA = ["پرو", "هاب", "پلاس", "هوشمند"]

DEFAULT_COPY_EN = (
    "In today's fast-paced world, our cutting-edge solution unlocks "
    "seamless, world-class results for everyone."
)
DEFAULT_COPY_FA = (
    "در دنیای امروز، راهکار بی‌نظیر و فوق‌العاده ما تجربه‌ای جادویی و "
    "رویایی برای شما رقم می‌زند."
)
DEFAULT_HOOK_EN = "The ultimate game-changing secret nobody tells you!"
DEFAULT_HOOK_FA = "راز بی‌نظیر و فوق‌العاده‌ای که هیچ‌کس به شما نمی‌گوید!"

SCORE_PER_HIT = 6


def topic_words(brief, lang):
    """Distinctive words from the brief: capitalised words first, then longest.

    A capitalised word is usually a proper noun — the most distinctive
    thing in the brief — so it outranks merely long generic words.
    """
    stop = EN_STOPWORDS if lang == "en" else FA_STOPWORDS
    words = re.findall(r"[\w\u0600-\u06ff]+", brief, flags=re.UNICODE)
    caps = {w.lower() for w in words if w[:1].isupper()}
    seen = []
    for word in words:
        low = word.lower()
        if low in stop or low in seen:
            continue
        seen.append(low)
    # distinctive = capitalised first, then longest; stable order otherwise
    return sorted(seen, key=lambda w: (w in caps, len(w)), reverse=True)


def anchor_word(brief, lang):
    """The single most distinctive word of the brief, for the reason line."""
    words = topic_words(brief, lang)
    return words[0] if words else ("thing" if lang == "en" else "چیز")


def default_pick(brief, kind, lang):
    """Name the most average pick for this brief and kind.

    Returns (pick, explanation). If the brief itself already contains
    cliches, the pick quotes them — the default is visible in the brief.
    Otherwise the pick is assembled from the catalog + the brief's topic.
    """
    hits = find_cliches(brief)
    topic = anchor_word(brief, lang)
    if kind == "name":
        filler = DEFAULT_NAME_FILLER_EN if lang == "en" else DEFAULT_NAME_FILLER_FA
        pick = "%s %s" % (topic.title() if lang == "en" else topic, filler[0])
        why = "a topic word plus a stock name ingredient"
    elif kind == "copy":
        pick = DEFAULT_COPY_EN if lang == "en" else DEFAULT_COPY_FA
        why = "the stock opener plus stock superlatives"
    elif kind == "hook":
        pick = DEFAULT_HOOK_EN if lang == "en" else DEFAULT_HOOK_FA
        why = "the stock superlative plus a stock secret"
    else:  # idea
        pick = ("An AI-powered app that leverages cutting-edge tech to "
                "revolutionize %s." % topic) if lang == "en" else \
            ("اپلیکیشنی هوشمند که با فناوری نوین، %s را دگرگون می‌کند." % topic)
        why = "the stock tech claim plus the topic"
    if hits:
        why += "; the brief itself already leans on: %s" % ", ".join(hits[:3])
    return pick, why


def _alternative_text(move, brief, kind, lang, seed, anchor):
    """One concrete alternative: the move applied to the brief."""
    if lang == "fa":
        templates = {
            "opposite": "برعکس پیش‌فرض: %s را کوچک و آرام بگو، نه بزرگ و پر سر و صدا.",
            "specific": "به‌جای ادعای کلی، یک جزئیات واقعی از «%s» بگو: کدام لحظه، کدام عدد؟",
            "constraint": "فقط با یک کلمه و یک رنگ: «%s» را در یک جمله‌ی پنج‌کلمه‌ای بگو.",
            "borrowed": "«%s» را مثل یک کارگاه توصیف کن: ابزار چیست، صدای کار چیست؟",
            "smaller": "فقط یک نفر، یک لحظه از «%s»: همان لحظه‌ای که همه‌چیز عوض شد.",
            "voice": "«%s» را مثل حرفی که به یک دوست می‌زنی بگو، در یک نفس.",
            "not": "بگو «%s» چه چیزی نیست؛ حذف صادقانه، هویت است.",
            "number": "یک عدد واقعی در «%s» بگذار: چند، چقدر، چه زمانی؟",
            "time": "«%s» را به یک زمان بچسبان: یک صبح، یک مهلت، یک اولین بار.",
            "tension": "مصالحه‌ی «%s» را نام ببر: چه چیزی را فدا می‌کند؟",
        }
    else:
        templates = {
            "opposite": "The opposite of the default: say %s small and quiet, not big and loud.",
            "specific": "Instead of the grand claim, one real detail from %s: which moment, which number?",
            "constraint": "One word, one colour: say %s in a five-word sentence.",
            "borrowed": "Describe %s as a workshop: what is the tool, what does the work sound like?",
            "smaller": "One person, one moment of %s: the moment everything changed.",
            "voice": "Say %s the way you would say it to a friend, in one breath.",
            "not": "Say what %s is NOT; the honest exclusion is the identity.",
            "number": "Put a real number in %s: how many, how much, by when?",
            "time": "Pin %s to a time: a morning, a deadline, a first try.",
            "tension": "Name what %s gives up; the trade-off, not the slogan.",
        }
    text = templates[move["id"]] % anchor
    if seed is not None:
        extra = seed.get("verb") or seed.get("voice") or seed.get("method")
        if extra:
            tail = (" — seed: %s" % extra) if lang == "en" else (" — بذر: %s" % extra)
            text += tail
    return text


def diverge(brief, kind="name", n=3, seed=None):
    """Name the default pick, then generate n divergent alternatives.

    Returns a dict: {brief, kind, lang, default, default_why, alternatives}.
    Deterministic when seed is given.
    """
    if kind not in ("name", "copy", "hook", "idea"):
        raise ValueError("unknown kind: %r (name, copy, hook, idea)" % kind)
    if n < 1:
        raise ValueError("n must be >= 1")
    lang = detect_language(brief)
    pick, why = default_pick(brief, kind, lang)
    anchor = anchor_word(brief, lang)
    rng = random.Random(seed) if seed is not None else random.Random()
    moves = rng.sample(MOVES, min(n, len(MOVES)))
    alternatives = []
    for move in moves:
        seed_roll = roll_seed(rng.choice(["visual", "text", "idea"]),
                              seed=rng.randrange(10 ** 9)) \
            if rng.random() < 0.5 else None
        alternatives.append({
            "move": move["id"],
            "move_name": move["name"],
            "question": move["question"],
            "text": _alternative_text(move, brief, kind, lang, seed_roll, anchor),
            "reason": ("grounded in the brief's word %r" % anchor)
                      if lang == "en" else
                      ("ریشه در کلمه‌ی «%s» از خود بریف دارد" % anchor),
        })
    return {
        "brief": brief,
        "kind": kind,
        "lang": lang,
        "default": pick,
        "default_why": why,
        "alternatives": alternatives,
    }


def score_text(text, kind="copy"):
    """Score 0-100: 100 minus 6 per cliche occurrence (names: filler counts too).

    Occurrences, not unique phrases: a text that says "leverage" twenty
    times is twenty times as average as one that says it once.
    """
    hits = find_cliches(text)
    lowered = text.lower()
    total = sum(lowered.count(h.lower()) for h in hits)
    extra = []
    if kind == "name":
        extra = ["name-filler:%s" % f for f in name_filler_hits(text)]
        total += len(extra)
    score = max(0, 100 - SCORE_PER_HIT * total)
    return {"score": score, "hits": hits + extra, "lang": detect_language(text)}


def check_text(text, kind="copy", threshold=70):
    """Score a candidate; pass when score >= threshold (CI gate)."""
    result = score_text(text, kind)
    result["threshold"] = threshold
    result["pass"] = result["score"] >= threshold
    return result
