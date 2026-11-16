"""Cliche catalogs: the stock words and phrases that mark the average pick.

English and Persian. These are the "first, most average pick" ingredients —
a name, a hook or a piece of copy built from them is what antialgorithm
calls the safe zone. The catalog is data, not a judgement: a word can be
fine in the right sentence, but three of them in one line is a tell.
"""

EN_CLICHES = [
    # stock openers
    "in today's fast-paced world",
    "in today's digital age",
    "in the modern world",
    "it's important to note",
    "it is important to note",
    "in conclusion",
    "furthermore",
    "moreover",
    "additionally",
    "delve",
    "dive into",
    "embark on",
    "nestled",
    "bustling",
    "vibrant",
    "tapestry",
    "landscape",
    "realm",
    "a testament to",
    "boasts",
    "leverage",
    "utilize",
    "harness",
    "supercharge",
    "unlock",
    "elevate",
    "empower",
    "foster",
    "pave the way",
    "seamless",
    "effortless",
    "cutting-edge",
    "cutting edge",
    "state-of-the-art",
    "state of the art",
    "world-class",
    "best-in-class",
    "best in class",
    "top-notch",
    "game-changing",
    "game changer",
    "groundbreaking",
    "revolutionary",
    "innovative",
    "next-gen",
    "next generation",
    "ai-powered",
    "one-stop",
    "all-in-one",
    "robust",
    "scalable",
    "holistic",
    "synergy",
    "streamline",
    "optimize",
    "take it to the next level",
    "to the next level",
    "the ultimate",
    "dream come true",
    "once in a lifetime",
    "crystal clear",
    "picture-perfect",
    "picture perfect",
    "spearhead",
    "unleash",
    "transform your",
    "elevate your",
    "unlock the power",
    "unlock your",
]

EN_NAME_FILLER = [
    # stock name ingredients: a name built only from these is the default
    "pro", "plus", "max", "ultra", "prime", "elite", "smart", "hub",
    "lab", "zone", "world", "center", "centre", "shop", "store", "360",
    "247", "24/7", "ai", "tech", "digital", "nova", "apex", "nexus",
    "zenith", "quantum", "turbo", "mega", "super", "top", "best", "one",
]

FA_CLICHES = [
    "در دنیای امروز",
    "در دنیای دیجیتال",
    "لازم به ذکر است",
    "به طور کلی",
    "به‌طور کلی",
    "به طور خلاصه",
    "در نهایت",
    "بی‌نظیر",
    "بینظیر",
    "فوق‌العاده",
    "فوق العاده",
    "شگفت‌انگیز",
    "شگفت انگیز",
    "جادویی",
    "رویایی",
    "منحصربه‌فرد",
    "منحصر به فرد",
    "پیشرفته‌ترین",
    "بهترین",
    "فوق پیشرفته",
    "حرفه‌ای‌ترین",
    "تضمینی",
    "بدون شک",
    "انقلابی",
    "دگرگون",
    "عصر جدید",
    "بی‌رقیب",
    "استثنایی",
    "کامل‌ترین",
    "جامع",
    "نوین",
    "مدرن‌ترین",
    "جدیدترین",
    "سریع‌ترین",
    "قدرتمندترین",
    "ایده‌آل",
    "طلایی",
    "خاص",
    "متنوع",
    "عالی",
    "حرفه‌ای",
    "هوشمند",
    "آسان",
]

FA_NAME_FILLER = [
    "پرو", "پلاس", "مکس", "اولترا", "پرایم", "هوشمند", "مرکز", "هاب",
    "تک", "دیجیتال", "نوین", "مدرن", "برتر", "طلایی", "ویژه", "۲۴", "360",
]


def detect_language(text):
    """Persian characters present -> 'fa', else 'en'."""
    for ch in text:
        if "\u0600" <= ch <= "\u06ff" or "\ufb50" <= ch <= "\ufdff":
            return "fa"
    return "en"


def find_cliches(text):
    """Return the list of catalog phrases found in text (case-insensitive).

    Longer phrases are reported before their substrings; a phrase that is
    fully inside an already-reported phrase is not reported twice.
    """
    lang = detect_language(text)
    catalog = EN_CLICHES if lang == "en" else FA_CLICHES
    lowered = text.lower()
    hits = []
    for phrase in sorted(catalog, key=len, reverse=True):
        needle = phrase.lower()
        if needle in lowered:
            if any(needle in h.lower() for h in hits):
                continue
            hits.append(phrase)
    return hits


def name_filler_hits(name):
    """Stock name ingredients found in a name (case-insensitive, whole words)."""
    lang = detect_language(name)
    filler = EN_NAME_FILLER if lang == "en" else FA_NAME_FILLER
    words = [w.strip(" -_") for w in name.lower().replace("_", " ").split()]
    return [f for f in filler if f in words]
