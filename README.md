# agent-diverge

Name the average pick, then diverge from it — stdlib only, no network, no keys. English + Persian.

**Pattern** (original code; pattern only, learned from today's radar): mankidev/antialgorithm makes the model say its first, most average pick out loud, then move away from it for a reason taken from the project — and ships deterministic helper scripts as the spine (`seed.py` rolls a random starting point, `check.py` renders and lists faults). This tool is that idea as a small local CLI for both languages we actually write in: a cliché catalog names the default pick, seeded divergence moves generate alternatives grounded in the brief's own words, and a `check` command scores cliché density as a CI gate. It is the sparring partner to `agent-humanizer`: one removes the AI tells, the other stops you from picking the average idea in the first place.

## How it works

1. **Name the default.** Given a brief (a name, a hook, a piece of copy, an idea), the tool builds the most average pick from the brief's own topic word plus the cliché catalog: "Arak Pro" for a tea house in Arak, "In today's fast-paced world, our cutting-edge solution…" for copy. If the brief itself already leans on clichés, the report says so.
2. **Diverge.** Each alternative applies one divergence move — opposite, one concrete detail, hard constraint, borrowed frame, smaller scale, human voice, negative space, a real number, anchor in time, name the trade-off — and names the reason, grounded in a distinctive word taken from the brief itself. Moves are picked by a seeded random draw, so `--seed` reproduces a run exactly.
3. **Seed.** `seed` rolls a starting point when the brief is thin: a visual seed (method, colours, layout, type, verb, scale, setting, region, half the time an object), a text seed (voice, way in, register), an idea seed (verb, constraint, scale, pressure). Two people with the same prompt start in different places.
4. **Check.** `check` scores any candidate 0–100: 100 minus 6 per cliché occurrence (names also count stock name ingredients like Pro/Hub/Max). Exit 0 at or above the threshold (default 70), exit 1 below — a CI gate for names, hooks and copy.

## Usage

```bash
python3 -m agent_diverge diverge --kind name --n 3 "a cozy tea house in Arak"
python3 -m agent_diverge diverge --kind copy --seed 7 "a cozy tea house in Arak"
python3 -m agent_diverge diverge --kind hook --json "a cozy tea house in Arak"

python3 -m agent_diverge seed --kind idea
python3 -m agent_diverge seed --kind visual --seed 5 --json

python3 -m agent_diverge check "The kettle whistles at six."
# Score: 100/100 (threshold 70) — PASS
python3 -m agent_diverge check "In today's fast-paced world, our cutting-edge solution leverages synergy."
# Score: 64/100 (threshold 70) — FAIL, exit 1

python3 -m agent_diverge check --kind name --threshold 90 "Game Pro Hub"
python3 -m agent_diverge list-cliches --lang fa
```

No file argument reads stdin. Language is detected from the script (Persian characters → FA); both catalogs apply, so mixed text works too. `--seed` makes `diverge` and `seed` reproducible; without it they draw from system randomness.

## Example

Brief: `a cozy tea house in Arak` (kind: name, seed 7):

> The default pick (the average answer):
>   Arak Pro
>   Why it is average: a topic word plus a stock name ingredient
>
> Divergent alternatives:
>   1. [Human voice] Say arak the way you would say it to a friend, in one breath.
>   2. [Hard constraint] One word, one colour: say arak in a five-word sentence.
>   3. [Negative space] Say what arak is NOT; the honest exclusion is the identity.

Full verified runs: `examples/before-after.md`.

## Scoring

`score = 100 − 6×cliché occurrences`, floored at 0. Occurrences, not unique phrases: a text that says "leverage" twenty times is twenty times as average as one that says it once. For `--kind name`, stock name ingredients (Pro, Hub, Max, Smart, …) count as hits too. Raise the threshold for strict gates (`--threshold 90` for names).

## Tests

```bash
python3 -m unittest discover -s tests
# Ran 38 tests — OK (cliché detection EN/FA, scoring incl. occurrence
# counting, default-pick naming, seeded divergence determinism, seed
# kinds, CLI exit codes incl. stdin)
```

The tests caught 3 real bugs before shipping: the anchor word picked the longest word ("house") instead of the proper noun ("Arak"), the score counted unique clichés instead of occurrences (a text repeating "leverage" twenty times scored 88), and a duplicated catalog entry.

## Why diverge, not just check

A checker tells you the copy is average after you wrote it. Naming the default *first* changes the next move: once "Arak Pro" is on the table and labelled average, nobody ships it. The moves are the point — each one asks a question the brief can answer, so the alternative comes from the project, not from a random word list.

---

# agent-diverge (فارسی)

اول متوسط‌ترین انتخاب را نام ببر، بعد از آن فاصله بگیر — فقط استاندارد لایبرری پایتون، بدون اینترنت و بدون کلید. انگلیسی + فارسی.

**الگو** (کد کاملاً اورجینال؛ فقط الگو از رادار امروز): mankidev/antialgorithm مدل را وادار می‌کند اول متوسط‌ترین انتخابش را با صدای بلند بگوید، بعد به دلیلی که از خود پروژه گرفته از آن فاصله بگیرد — و اسکریپت‌های قطعی را ستون کار می‌کند (`seed.py` نقطهٔ شروع تصادفی می‌دهد، `check.py` خطاها را فهرست می‌کند). این ابزار همان ایده است به شکل یک CLI کوچک برای هر دو زبانی که واقعاً با آن می‌نویسیم: فهرست کلیشه‌ها انتخاب پیش‌فرض را نام می‌برد، حرکت‌های واگرایی با بذر مشخص جایگزین‌هایی می‌سازند که ریشه در کلمه‌های خود بریف دارند، و دستور `check` تراکم کلیشه را به‌عنوان گیت CI امتیاز می‌دهد. شریک تمرینی `agent-humanizer` است: آن یکی نشانه‌های هوش مصنوعی را حذف می‌کند، این یکی جلوی انتخاب ایدهٔ متوسط را از اول می‌گیرد.

## روش کار

۱. **نام‌بردن پیش‌فرض.** با گرفتن یک بریف (نام، هوک، متن، ایده)، ابزار متوسط‌ترین انتخاب را از کلمهٔ موضوع بریف به‌علاوهٔ فهرست کلیشه‌ها می‌سازد: برای چایخانه‌ای در اراک «Arak Pro»، برای متن «In today's fast-paced world, our cutting-edge solution…». اگر خود بریف به کلیشه‌ها تکیه کرده باشد، گزارش همان را می‌گوید.
۲. **واگرایی.** هر جایگزین یک حرکت واگرایی اعمال می‌کند — برعکس، یک جزئیات واقعی، محدودیت سخت، قاب قرضی، مقیاس کوچک‌تر، صدای انسانی، فضای منفی، یک عدد واقعی، لنگر در زمان، نام‌بردن مصالحه — و دلیلش را با تکیه بر یک کلمهٔ شاخص از خود بریف می‌گوید. حرکت‌ها با قرعهٔ تصادفیِ بذردار انتخاب می‌شوند، پس `--seed` یک اجرا را دقیقاً تکرار می‌کند.
۳. **بذر.** `seed` وقتی بریف نازک است نقطهٔ شروع می‌دهد: بذر تصویری (روش، رنگ‌ها، چیدمان، تایپ، فعل، مقیاس، صحنه، منطقه، نیمی از وقت‌ها یک شیء)، بذر متنی (صدا، راه ورود، رجیستر)، بذر ایده (فعل، محدودیت، مقیاس، فشار). دو نفر با یک پرامپت از جاهای متفاوتی شروع می‌کنند.
۴. **سنجش.** `check` به هر نامزد امتیاز ۰ تا ۱۰۰ می‌دهد: ۱۰۰ منهای ۶ به‌ازای هر رخداد کلیشه (برای نام‌ها، اجزای کلیشه‌ای نام مثل Pro و Hub هم حساب می‌شوند). خروج ۰ در یا بالای آستانه (پیش‌فرض ۷۰)، خروج ۱ پایین‌تر — یک گیت CI برای نام‌ها، هوک‌ها و متن‌ها.

## استفاده

```bash
python3 -m agent_diverge diverge --kind name --n 3 "a cozy tea house in Arak"
python3 -m agent_diverge diverge --kind copy --seed 7 "a cozy tea house in Arak"

python3 -m agent_diverge seed --kind idea
python3 -m agent_diverge seed --kind visual --seed 5 --json

python3 -m agent_diverge check "The kettle whistles at six."
# Score: 100/100 (threshold 70) — PASS
python3 -m agent_diverge check "In today's fast-paced world, our cutting-edge solution leverages synergy."
# Score: 64/100 (threshold 70) — FAIL, خروج ۱

python3 -m agent_diverge check --kind name --threshold 90 "Game Pro Hub"
python3 -m agent_diverge list-cliches --lang fa
```

بدون آرگومان متنی، از stdin می‌خواند. زبان از روی خط متن تشخیص داده می‌شود (حروف فارسی → فارسی). `--seed` خروجی `diverge` و `seed` را تکرارپذیر می‌کند؛ بدون آن، از تصادف سیستم استفاده می‌شود.

## تست‌ها

```bash
python3 -m unittest discover -s tests
# Ran 38 tests — OK
```

تست‌ها پیش از انتشار ۳ باگ واقعی گرفتند: کلمهٔ لنگر طولانی‌ترین کلمه («house») را انتخاب می‌کرد نه اسم خاص («Arak»)، امتیاز کلیشه‌های یکتا را می‌شمرد نه رخدادها (متنی که بیست بار «leverage» می‌گفت امتیاز ۸۸ می‌گرفت)، و یک ورودی تکراری در فهرست فارسی بود.
