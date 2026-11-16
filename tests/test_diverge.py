"""Tests for agent-diverge. Stdlib unittest only.

Run:  python3 -m unittest discover -s tests -v
"""

import json
import subprocess
import sys
import unittest

from agent_diverge.cliches import (
    detect_language, find_cliches, name_filler_hits,
)
from agent_diverge.engine import check_text, default_pick, diverge, score_text
from agent_diverge.seed import format_seed, roll_seed


class TestLanguageAndCliches(unittest.TestCase):
    def test_detect_english(self):
        self.assertEqual(detect_language("hello world"), "en")

    def test_detect_persian(self):
        self.assertEqual(detect_language("سلام دنیا"), "fa")

    def test_find_english_cliches(self):
        hits = find_cliches("In today's fast-paced world, we leverage synergy.")
        self.assertIn("in today's fast-paced world", hits)
        self.assertIn("leverage", hits)
        self.assertIn("synergy", hits)

    def test_find_persian_cliches(self):
        hits = find_cliches("در دنیای امروز، این محصول بی‌نظیر است.")
        self.assertIn("در دنیای امروز", hits)
        self.assertIn("بی‌نظیر", hits)

    def test_find_clean_text_has_no_hits(self):
        self.assertEqual(find_cliches("The kettle whistles at six."), [])

    def test_no_duplicate_hits(self):
        # "فوق‌العاده" is listed twice in the catalog; it must be hit once.
        hits = find_cliches("محصولی فوق‌العاده")
        self.assertEqual(hits.count("فوق‌العاده"), 1)

    def test_name_filler(self):
        self.assertIn("pro", name_filler_hits("Game Pro"))
        self.assertIn("hub", name_filler_hits("Coffee Hub"))
        self.assertEqual(name_filler_hits("Whisperwood"), [])


class TestScoring(unittest.TestCase):
    def test_clean_text_scores_100(self):
        self.assertEqual(score_text("The kettle whistles at six.")["score"], 100)

    def test_each_hit_costs_six(self):
        result = score_text("We leverage synergy.")
        self.assertEqual(result["score"], 100 - 6 * len(result["hits"]))
        self.assertGreater(len(result["hits"]), 0)

    def test_score_never_below_zero(self):
        text = " ".join(["leverage synergy"] * 20)
        self.assertEqual(score_text(text)["score"], 0)

    def test_name_kind_counts_filler(self):
        result = score_text("Game Pro Hub", kind="name")
        self.assertLess(result["score"], 100)
        self.assertTrue(any(h.startswith("name-filler:") for h in result["hits"]))

    def test_check_passes_clean_text(self):
        result = check_text("The kettle whistles at six.")
        self.assertTrue(result["pass"])
        self.assertEqual(result["threshold"], 70)

    def test_check_fails_cliched_text(self):
        text = ("In today's fast-paced world, our cutting-edge solution "
                "leverages synergy to unlock seamless results.")
        self.assertFalse(check_text(text)["pass"])

    def test_check_threshold_respected(self):
        text = "We leverage synergy."
        self.assertTrue(check_text(text, threshold=50)["pass"])
        self.assertFalse(check_text(text, threshold=100)["pass"])


class TestDefaultPick(unittest.TestCase):
    def test_name_default_uses_topic_word(self):
        pick, _ = default_pick("a cozy tea house in Arak", "name", "en")
        self.assertIn("Arak", pick)

    def test_copy_default_is_stock_opener(self):
        pick, _ = default_pick("anything", "copy", "en")
        self.assertIn("fast-paced world", pick)

    def test_persian_default(self):
        pick, _ = default_pick("یک چایخانه دنج در اراک", "copy", "fa")
        self.assertIn("دنیای امروز", pick)

    def test_brief_cliches_noted(self):
        _, why = default_pick("we leverage synergy for gamers", "idea", "en")
        self.assertIn("leverage", why)


class TestDiverge(unittest.TestCase):
    def test_returns_default_and_alternatives(self):
        result = diverge("a cozy tea house in Arak", kind="name", n=3, seed=7)
        self.assertIn("default", result)
        self.assertEqual(len(result["alternatives"]), 3)
        for alt in result["alternatives"]:
            self.assertIn("move", alt)
            self.assertIn("question", alt)
            self.assertIn("text", alt)
            self.assertIn("reason", alt)

    def test_deterministic_with_seed(self):
        a = diverge("a cozy tea house in Arak", kind="copy", n=3, seed=42)
        b = diverge("a cozy tea house in Arak", kind="copy", n=3, seed=42)
        self.assertEqual(a, b)

    def test_different_seed_usually_differs(self):
        a = diverge("a cozy tea house in Arak", kind="copy", n=3, seed=1)
        b = diverge("a cozy tea house in Arak", kind="copy", n=3, seed=2)
        self.assertNotEqual(
            [x["move"] for x in a["alternatives"]],
            [x["move"] for x in b["alternatives"]])

    def test_reason_grounded_in_brief(self):
        result = diverge("a cozy tea house in Arak", kind="name", n=2, seed=5)
        for alt in result["alternatives"]:
            self.assertIn("arak", alt["reason"].lower())

    def test_moves_are_distinct(self):
        result = diverge("a board game about tides", kind="idea", n=5, seed=9)
        moves = [a["move"] for a in result["alternatives"]]
        self.assertEqual(len(moves), len(set(moves)))

    def test_invalid_kind_raises(self):
        with self.assertRaises(ValueError):
            diverge("x", kind="poster")

    def test_invalid_n_raises(self):
        with self.assertRaises(ValueError):
            diverge("x", n=0)


class TestSeed(unittest.TestCase):
    def test_visual_seed_keys(self):
        seed = roll_seed("visual", seed=3)
        for key in ("method", "colors", "layout", "type", "verb", "scale"):
            self.assertIn(key, seed)

    def test_text_and_idea_seed_keys(self):
        self.assertEqual(set(roll_seed("text", seed=1)),
                         {"kind", "voice", "way_in", "register"})
        self.assertEqual(set(roll_seed("idea", seed=1)),
                         {"kind", "verb", "constraint", "scale", "pressure"})

    def test_deterministic_with_seed(self):
        self.assertEqual(roll_seed("visual", seed=11), roll_seed("visual", seed=11))

    def test_unknown_kind_raises(self):
        with self.assertRaises(ValueError):
            roll_seed("poster")

    def test_format_seed_readable(self):
        out = format_seed(roll_seed("text", seed=4))
        self.assertIn("seed (text):", out)
        self.assertIn("voice:", out)


class TestCLI(unittest.TestCase):
    def run_cli(self, *argv, input_text=None):
        return subprocess.run(
            [sys.executable, "-m", "agent_diverge", *argv],
            input=input_text, capture_output=True, text=True, timeout=30)

    def test_version(self):
        proc = self.run_cli("--version")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("agent-diverge", proc.stdout)

    def test_diverge_json(self):
        proc = self.run_cli("diverge", "--kind", "name", "--n", "2",
                            "--seed", "7", "--json", "a cozy tea house in Arak")
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertEqual(len(data["alternatives"]), 2)
        self.assertIn("default", data)

    def test_diverge_text_output_names_default(self):
        proc = self.run_cli("diverge", "--kind", "copy", "--seed", "7",
                            "a cozy tea house in Arak")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("The default pick", proc.stdout)
        self.assertIn("Divergent alternatives", proc.stdout)

    def test_check_pass_exit_zero(self):
        proc = self.run_cli("check", "The kettle whistles at six.")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("PASS", proc.stdout)

    def test_check_fail_exit_one(self):
        proc = self.run_cli(
            "check",
            "In today's fast-paced world, our cutting-edge solution "
            "leverages synergy to unlock seamless results.")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("FAIL", proc.stdout)

    def test_check_reads_stdin(self):
        proc = self.run_cli("check", input_text="The kettle whistles at six.")
        self.assertEqual(proc.returncode, 0)

    def test_seed_json_parses(self):
        proc = self.run_cli("seed", "--kind", "idea", "--seed", "5", "--json")
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertEqual(data["kind"], "idea")

    def test_list_cliches(self):
        proc = self.run_cli("list-cliches", "--lang", "fa")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("بی‌نظیر", proc.stdout)


if __name__ == "__main__":
    unittest.main()
