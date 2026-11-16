"""CLI: diverge / seed / check / list-cliches.

Exit codes: 0 ok, 1 check failed or bad usage, 2 invalid arguments.
`check` exits 1 when the score is below the threshold — use it as a CI gate.
"""

import argparse
import json
import sys

from . import __version__
from .cliches import EN_CLICHES, FA_CLICHES, detect_language
from .engine import check_text, diverge
from .seed import format_seed, roll_seed


def _read_text(args):
    if args.text:
        return " ".join(args.text)
    data = sys.stdin.read()
    if not data.strip():
        raise SystemExit("error: give text as arguments or pipe it on stdin")
    return data.strip()


def _print(obj, as_json):
    if as_json:
        print(json.dumps(obj, ensure_ascii=False, indent=2))
    else:
        print(obj)


def cmd_diverge(args):
    brief = _read_text(args)
    result = diverge(brief, kind=args.kind, n=args.n, seed=args.seed)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    print("Brief: %s" % result["brief"])
    print("Kind: %s (%s)" % (result["kind"], result["lang"]))
    print()
    print("The default pick (the average answer):")
    print("  %s" % result["default"])
    print("  Why it is average: %s" % result["default_why"])
    print()
    print("Divergent alternatives:")
    for i, alt in enumerate(result["alternatives"], 1):
        print("  %d. [%s] %s" % (i, alt["move_name"], alt["text"]))
        print("     Ask: %s" % alt["question"])
        print("     %s" % alt["reason"])
    return 0


def cmd_seed(args):
    seed = roll_seed(args.kind, seed=args.seed)
    if args.json:
        print(json.dumps(seed, ensure_ascii=False, indent=2))
    else:
        print(format_seed(seed))
    return 0


def cmd_check(args):
    text = _read_text(args)
    result = check_text(text, kind=args.kind, threshold=args.threshold)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Score: %d/100 (threshold %d) — %s"
              % (result["score"], result["threshold"],
                 "PASS" if result["pass"] else "FAIL"))
        if result["hits"]:
            print("Cliche hits (%d):" % len(result["hits"]))
            for hit in result["hits"]:
                print("  - %s" % hit)
        else:
            print("No cliche hits.")
    return 0 if result["pass"] else 1


def cmd_list_cliches(args):
    lang = args.lang or "en"
    catalog = EN_CLICHES if lang == "en" else FA_CLICHES
    if args.json:
        print(json.dumps(catalog, ensure_ascii=False, indent=2))
    else:
        for phrase in catalog:
            print(phrase)
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="agent-diverge",
        description="Name the average pick, then diverge from it. Stdlib only.")
    parser.add_argument("--version", action="version",
                        version="agent-diverge %s" % __version__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("diverge", help="name the default pick, offer alternatives")
    p.add_argument("text", nargs="*", help="the brief (or pipe it on stdin)")
    p.add_argument("--kind", default="name",
                   choices=["name", "copy", "hook", "idea"])
    p.add_argument("--n", type=int, default=3, help="alternatives (default 3)")
    p.add_argument("--seed", type=int, default=None,
                   help="fixed seed for reproducible output")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_diverge)

    p = sub.add_parser("seed", help="roll a random starting point")
    p.add_argument("--kind", default="visual",
                   choices=["visual", "text", "idea"])
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_seed)

    p = sub.add_parser("check", help="score a candidate for cliche density")
    p.add_argument("text", nargs="*", help="the candidate (or pipe it on stdin)")
    p.add_argument("--kind", default="copy", choices=["name", "copy", "hook", "idea"])
    p.add_argument("--threshold", type=int, default=70,
                   help="pass at or above this score (default 70)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("list-cliches", help="print the cliche catalog")
    p.add_argument("--lang", default="en", choices=["en", "fa"])
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_list_cliches)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
