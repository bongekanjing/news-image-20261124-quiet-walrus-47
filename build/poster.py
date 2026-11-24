#!/usr/bin/env python3
"""Build build/poster.html: a one-page newspaper front page for
Tuesday 24 November 2026, laid out for a 1024x1024 canvas.

Every word on the page comes from the module constants below.  They are
validated before a single byte of HTML is written; a story with no body,
a headline longer than its slot, a figure or brief tagged with a region
that files no story, or a column that will not fit the page all abort the
build with a non-zero exit and a message on stderr.

Standard library only.  No clock, no network, no randomness.
"""

from __future__ import annotations

import html
import pathlib
import sys
from dataclasses import dataclass

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "poster.html"

# ------------------------------------------------------------------ page copy

DAY_LINE = "TUESDAY 24 NOVEMBER 2026"
DAY_WORDS = "Tuesday 24 November 2026"
PAPER = "THE WORLD LEDGER"
VOLUME = "VOL. I  ·  NO. 328"
STANDING = "WORLD EDITION  ·  ONE DAY, ONE PAGE  ·  ALL TIMES UTC"

EDITION_FMT = "{n} STORIES  ·  {r} REGIONS  ·  COMPILED IN UTC  ·  PRICE ONE READ"
FOOT_NOTE = "THIS PAGE COVERS ONE DAY: THE NEWS OF 24 NOVEMBER 2026, IN UTC"

# Sections, in the order they print. Nothing else may be used as a region.
REGIONS = ("AMERICAS", "EUROPE", "ASIA-PACIFIC", "MIDDLE EAST", "AFRICA", "WORLD")

# ---------------------------------------------------------------- type metrics
# Character widths measured on the serif face this page is set in, as a
# fraction of the font size: caps are wide, roman lowercase is narrow.
CAP_EM = 0.585
ROMAN_EM = 0.415

COL_TEXT_W = 187      # printed width of one story column, px
FEAT_HEAD_PX = 15.0
STD_HEAD_PX = 11.2
BODY_PX = 8.8
LEAD_HEAD_PX = 33.0
LEAD_HEAD_W = 976
LEAD_BODY_COLS = 3
LEAD_COL_W = 300

HEAD_LH = 12.6
FEAT_HEAD_LH = 16.4
BODY_LH = 10.6
KICKER_H = 11.0
STORY_GAP = 7.0
BODY_BOX_H = 452.0
MIN_COL_FILL = 0.72


def cpl(width: float, font_px: float, em: float) -> int:
    """Characters that fit on one printed line."""
    return int(width / (font_px * em))


COL_HEAD_CPL = cpl(COL_TEXT_W, STD_HEAD_PX, CAP_EM)
COL_FEAT_CPL = cpl(COL_TEXT_W, FEAT_HEAD_PX, CAP_EM)
COL_BODY_CPL = cpl(COL_TEXT_W, BODY_PX, ROMAN_EM)
LEAD_HEAD_CPL = cpl(LEAD_HEAD_W, LEAD_HEAD_PX, CAP_EM)
LEAD_BODY_CPL = cpl(LEAD_COL_W, 9.6, ROMAN_EM)

MIN_STORIES, MAX_STORIES = 18, 22
N_COLUMNS = 4


# ---------------------------------------------------------------- stories

@dataclass(frozen=True)
class Story:
    region: str
    headline: str
    body: str
    head_lines: int = 2
    body_lines: int = 3
    feature: bool = False
    lead: bool = False
    deck: str = ""


STORIES: tuple[Story, ...] = (
    # ---------------- AMERICAS
    Story(
        region="AMERICAS",
        headline="TRUMP: \u2018I PERSUADED THE BOARD\u2019 \u2014 HUANG BACK AT NVIDIA",
        deck=(
            "The board reversed itself eleven days after he stepped down. The shares jumped more "
            "than 30%, all three New York indices soared, and Washington is now arguing over what "
            "was promised to whom \u2014 and whether chips were part of the bargain."
        ),
        body=(
            "Nvidia's board reinstated Jensen Huang as chief executive eleven days after he "
            "stepped down, and the stock jumped more than 30% as all three main New York indices "
            "soared. President Trump said his intervention \u201cwas very important\u201d and that he had "
            "\u201cpersuaded the board\u201d. Democrats called it a security exemption and demanded a full "
            "investigation into chip exports to China. JD Vance had lobbied the board over the "
            "weekend."
        ),
        head_lines=2,
        body_lines=4,
        lead=True,
    ),
    Story(
        region="AMERICAS",
        headline="ARMY MOVES TO DETONATE FIVE TONNES OF CHEMICALS",
        body=(
            "The US Army moved to invoke emergency powers to detonate five tonnes of unstable, "
            "lead-bearing chemicals in Iowa, defying a court order. It says cold weather makes "
            "delay more dangerous."
        ),
        body_lines=4,
    ),
    Story(
        region="AMERICAS",
        headline="SAN FRANCISCO BRACES FOR HISTORIC FLOODING",
        body=(
            "San Francisco braced for possibly historic coastal flooding as unusually high tides "
            "met a storm in the holiday travel week. Low-lying districts were warned."
        ),
        body_lines=4,
    ),
    Story(
        region="AMERICAS",
        headline="BUKELE OPENS $1 MILLION FUND FOR THE FALLEN",
        body=(
            "President Bukele announced a $1 million fund for the families of Salvadoran soldiers "
            "killed fighting gangs in Haiti. Three more died."
        ),
        body_lines=3,
    ),
    # ---------------- EUROPE
    Story(
        region="EUROPE",
        headline="COP31 ENDS WITH NO DEAL, A FIRST IN 17 YEARS",
        body=(
            "COP31 in Antalya ended with no agreement after two weeks, the first failure of a UN "
            "climate summit in 17 years. Oil producers resisted; Antonio Guterres blamed "
            "\u201cpowerful fossil fuel interests\u201d."
        ),
        head_lines=3,
        body_lines=4,
        feature=True,
    ),
    Story(
        region="EUROPE",
        headline="BELGIAN STRIKE PARALYSES AIR TRAVEL",
        body=(
            "Belgium's general strike against austerity paralysed air travel as controllers "
            "joined the walkout. Workers marched again on the 23rd."
        ),
        body_lines=3,
    ),
    Story(
        region="EUROPE",
        headline="MERZ: BLOCKING KYIV'S 2008 NATO BID A MISTAKE",
        body=(
            "Chancellor Merz called blocking Ukraine's 2008 NATO bid a \u201cmistake\u201d. Membership "
            "guarantees are now the core issue in the peace talks."
        ),
        body_lines=3,
    ),
    Story(
        region="EUROPE",
        headline="KYIV REGION STRUCK; AT LEAST 14 MISSING",
        body=(
            "Russian drones and missiles struck Ukraine's Kyiv region and at least 14 people were "
            "missing, Zelenskyy said. Rescue teams worked through the damaged sites."
        ),
        body_lines=4,
    ),
    Story(
        region="EUROPE",
        headline="DENMARK TO BAN PHONES IN SCHOOLS TO GRADE 10",
        body=(
            "Denmark's education ministry will propose banning smartphones in schools up to the "
            "10th grade from 2027. Network filtering would follow."
        ),
        body_lines=3,
    ),
    Story(
        region="EUROPE",
        headline="BRUSSELS PROPOSES A 22ND SANCTIONS PACKAGE",
        body=(
            "The European Commission proposed a 22nd sanctions package against Russia, widening "
            "curbs on banks, crypto and sport. States must still approve it."
        ),
        body_lines=3,
    ),
    # ---------------- ASIA-PACIFIC
    Story(
        region="ASIA-PACIFIC",
        headline="34 MISSING AFTER FIRE AT INDONESIAN CANDY PLANT",
        body=(
            "A fire swept a candy factory in Banten, Indonesia. Teams recovered remains in 24 body "
            "bags while 34 workers were missing, with hotspots and collapsed sections hampering "
            "the search."
        ),
        head_lines=3,
        body_lines=4,
        feature=True,
    ),
    Story(
        region="ASIA-PACIFIC",
        headline="INDONESIA CHARGES EX-POLICE CHIEF WITH TREASON",
        body=(
            "Indonesia charged a former police chief and five others with treason. The probe "
            "found wiretapping of President Prabowo Subianto's phone."
        ),
        body_lines=3,
    ),
    Story(
        region="ASIA-PACIFIC",
        headline="CHINA SENTENCES AN OFFICIAL TO DEATH FOR SPYING",
        body=(
            "China sentenced an official to death for spying and leaking national secrets to a "
            "foreign country. The case was disclosed on Tuesday."
        ),
        body_lines=3,
    ),
    Story(
        region="ASIA-PACIFIC",
        headline="KIM: THE NORTH SEEKS SECURITY, NOT SUPREMACY",
        body=(
            "Kim Jong Un said North Korea seeks security rather than global supremacy. He spoke "
            "after snubbing Trump's latest attempt to arrange a meeting."
        ),
        body_lines=3,
    ),
    Story(
        region="ASIA-PACIFIC",
        headline="INDIA-CHINA BORDER TALKS; MODI'S NEPAL PACKAGE",
        body=(
            "India-China border talks and Modi's development package for Nepal led South Asian "
            "coverage. India's place in the Asia Power Index was also in focus."
        ),
        body_lines=3,
    ),
    # ---------------- MIDDLE EAST
    Story(
        region="MIDDLE EAST",
        headline="IRAN VOWS TO COUNTER THE US NAVAL BLOCKADE",
        body=(
            "Iran's foreign ministry said Tehran would use every means to counter the US naval "
            "blockade. Footage of an underground \u201cmissile city\u201d was released."
        ),
        body_lines=3,
    ),
    Story(
        region="MIDDLE EAST",
        headline="LIKUD AND YESH ATID OPEN A THIRD ROUND",
        body=(
            "Likud and Yesh Atid opened a third round of coalition talks. Yesh Atid's leader "
            "called action on Iran unnecessary before a government forms."
        ),
        body_lines=3,
    ),
    Story(
        region="MIDDLE EAST",
        headline="EISENKOT CONDEMNS WEST BANK ARSON ATTACKS",
        body=(
            "Opposition leader Gadi Eisenkot condemned arson attacks that settlers are suspected "
            "of carrying out in the occupied West Bank. He blamed Netanyahu's government."
        ),
        body_lines=4,
    ),
    # ---------------- AFRICA
    Story(
        region="AFRICA",
        headline="DR CONGO IMPOSES ANOTHER COBALT EXPORT BAN",
        body=(
            "The Democratic Republic of the Congo, the main cobalt producer, imposed a further "
            "export ban. Cobalt is central to vehicle batteries."
        ),
        body_lines=3,
    ),
    # ---------------- WORLD
    Story(
        region="WORLD",
        headline="FIFA AWARDS THE 2031 AND 2035 WORLD CUPS",
        body=(
            "FIFA approved the joint US-Mexico-Costa Rica-Jamaica bid for the 2031 Women's World "
            "Cup and confirmed England, Scotland, Wales and Northern Ireland for 2035. Both were "
            "unopposed."
        ),
        body_lines=4,
    ),
    Story(
        region="WORLD",
        headline="NATO WILL DEFEND AGAINST THREATS IN SPACE",
        body=(
            "NATO chief Mark Rutte said the alliance would defend against threats in space. German "
            "media reported Russia may be preparing a nuclear-armed satellite."
        ),
        body_lines=4,
    ),
)

# ---------------------------------------------------------------- figures

@dataclass(frozen=True)
class Figure:
    numeral: str
    gloss: str
    region: str


STATS: tuple[Figure, ...] = (
    Figure("+30%", "Nvidia's jump in a single session", "AMERICAS"),
    Figure("1,000", "Delta flights delayed by a software fault", "AMERICAS"),
    Figure("17", "years since a UN climate summit failed", "EUROPE"),
    Figure("34", "workers still missing at Banten", "ASIA-PACIFIC"),
    Figure("22", "sanctions packages proposed against Russia", "EUROPE"),
    Figure("2035", "Women's World Cup, to the home nations", "WORLD"),
)

# ---------------------------------------------------------------- clock

@dataclass(frozen=True)
class Beat:
    time: str
    event: str


CLOCK: tuple[Beat, ...] = (
    Beat("05:10", "Antalya: COP31 ends without a deal; recriminations begin."),
    Beat("07:30", "Brussels: controllers join the Belgian strike; flights halted."),
    Beat("09:15", "Kyiv region: strikes leave at least 14 people missing."),
    Beat("11:40", "Banten: 24 body bags recovered; 34 workers missing."),
    Beat("15:20", "San Francisco: high tide and storm raise flood warnings."),
    Beat("20:55", "New York: Nvidia closes more than 30% higher."),
)

# ---------------------------------------------------------------- briefs

BRIEFS: tuple[tuple[str, str], ...] = (
    ("AMERICAS", "Delta delays 1,000 flights as its aircraft-weighing system fails."),
    ("EUROPE", "Russian cargo ship burns in the Gulf of Finland; 16 crew evacuated."),
    ("EUROPE", "Moscow summons Estonia's charg\u00e9 d'affaires over the closed border."),
    ("EUROPE", "Finland warms to tank traps on its border with Russia in peacetime."),
    ("WORLD", "Ukrainian naval drones strike a new Russian warship in Libya."),
    ("ASIA-PACIFIC", "Myanmar calls an ASEAN decision unfair and imbalanced."),
)


class BuildError(Exception):
    pass


# ---------------------------------------------------------------- validation

def sentences(text: str) -> list[str]:
    """Split prose into sentences, leaving common abbreviations alone."""
    out, buf = [], ""
    for ch in text:
        buf += ch
        if ch in ".!?":
            stripped = buf.strip()
            if ch == "." and stripped.endswith(("Mr.", "Ms.", "Mrs.", "Dr.", "No.", "St.")):
                continue
            if stripped:
                out.append(stripped)
                buf = ""
    if buf.strip():
        out.append(buf.strip())
    return out


def fits(text: str, per_line: int, lines: int) -> bool:
    """Greedy word wrap: will `text` print inside `lines` lines of `per_line`?"""
    if len(text) > per_line * lines:
        return False
    used, col = 1, 0
    for word in text.split():
        need = len(word) + (1 if col else 0)
        if col + need <= per_line:
            col += need
        else:
            used += 1
            col = len(word)
            if used > lines:
                return False
    return used <= lines


def story_height(s: Story) -> float:
    if s.feature:
        head = s.head_lines * FEAT_HEAD_LH
    elif s.lead:
        head = s.head_lines * (LEAD_HEAD_PX * 1.1)
    else:
        head = s.head_lines * HEAD_LH
    return KICKER_H + head + 2.0 + s.body_lines * BODY_LH + STORY_GAP


def census_of(stories) -> dict[str, int]:
    out: dict[str, int] = {}
    for region in REGIONS:
        n = sum(1 for s in stories if s.region == region)
        if n:
            out[region] = n
    return out


def balance(stories) -> list[list[Story]]:
    """Split the stories into four contiguous columns, preserving reading
    order, choosing the split points that level the column heights best."""
    n = len(stories)
    if n < N_COLUMNS:
        return [[s] for s in stories] + [[] for _ in range(N_COLUMNS - n)]

    prefix = [0.0]
    for s in stories:
        prefix.append(prefix[-1] + story_height(s))

    def load(i, j):  # stories[i:j]
        return prefix[j] - prefix[i]

    best = None
    for a in range(1, n - 2):
        for b in range(a + 1, n - 1):
            for c in range(b + 1, n):
                loads = (load(0, a), load(a, b), load(b, c), load(c, n))
                score = (round(max(loads), 2), round(-min(loads), 2))
                if best is None or score < best[0]:
                    best = (score, (a, b, c))
    a, b, c = best[1]
    return [stories[0:a], stories[a:b], stories[b:c], stories[c:n]]


def validate():
    errs: list[str] = []

    if not (MIN_STORIES <= len(STORIES) <= MAX_STORIES):
        errs.append(f"story count {len(STORIES)} is outside {MIN_STORIES}-{MAX_STORIES}")

    leads = [s for s in STORIES if s.lead]
    if len(leads) != 1:
        errs.append(f"exactly one lead story is required, found {len(leads)}")

    seen_heads: set[str] = set()
    seen_bodies: set[str] = set()
    for i, s in enumerate(STORIES, 1):
        tag = f"story {i} [{s.region}] {s.headline[:30]!r}"
        if s.region not in REGIONS:
            errs.append(f"{tag}: region is not one of the six sections")
        if not s.headline.strip():
            errs.append(f"{tag}: empty headline")
        elif s.headline != s.headline.upper():
            errs.append(f"{tag}: headline is not set in caps")
        if not s.body.strip():
            errs.append(f"{tag}: no body text")
        if s.headline in seen_heads:
            errs.append(f"{tag}: duplicate headline")
        seen_heads.add(s.headline)
        if s.body in seen_bodies:
            errs.append(f"{tag}: body repeats another story's body")
        seen_bodies.add(s.body)

        n_sent = len(sentences(s.body))
        if not 2 <= n_sent <= 4:
            errs.append(f"{tag}: body has {n_sent} sentences, the slot takes 2-4")

        if s.lead:
            if not s.deck.strip():
                errs.append(f"{tag}: the lead needs a deck")
            elif len(sentences(s.deck)) > 3:
                errs.append(f"{tag}: the lead deck runs past three sentences")
            if not fits(s.headline, LEAD_HEAD_CPL, s.head_lines):
                errs.append(f"{tag}: headline will not fit {s.head_lines} lead lines")
            if len(s.body) > LEAD_BODY_CPL * 3 * LEAD_BODY_COLS:
                errs.append(f"{tag}: lead body will not fit {LEAD_BODY_COLS} columns")
            continue

        head_cpl = COL_FEAT_CPL if s.feature else COL_HEAD_CPL
        if not fits(s.headline, head_cpl, s.head_lines):
            errs.append(
                f"{tag}: headline {len(s.headline)} chars will not fit "
                f"{s.head_lines} line(s) of {head_cpl}"
            )
        if not fits(s.body, COL_BODY_CPL, s.body_lines):
            errs.append(
                f"{tag}: body {len(s.body)} chars will not fit "
                f"{s.body_lines} line(s) of {COL_BODY_CPL}"
            )

    # ---- the census must describe the stories actually printed
    census = census_of(STORIES)
    if sum(census.values()) != len(STORIES):
        errs.append("census total does not equal the number of stories")
    for region in REGIONS:
        if region not in census:
            errs.append(f"section {region} files no story")
        elif census[region] <= 0:
            errs.append(f"census lists {region} with no story")
    filed = set(census)

    # ---- everything else that names a region must have a story behind it
    if len(STATS) != 6:
        errs.append(f"six figures of the day are required, found {len(STATS)}")
    for f in STATS:
        if f.region not in filed:
            errs.append(f"figure {f.numeral!r} is tagged {f.region}, which files no story")
        if not f.numeral.strip():
            errs.append("a figure has an empty numeral")
        if len(f.gloss) > 42:
            errs.append(f"figure {f.numeral!r}: gloss {len(f.gloss)} chars, over 42")

    if len(CLOCK) != 6:
        errs.append(f"six clock entries are required, found {len(CLOCK)}")
    last = ""
    for b in CLOCK:
        hh, sep, mm = b.time.partition(":")
        if not (sep and len(hh) == 2 and len(mm) == 2 and hh.isdigit() and mm.isdigit()):
            errs.append(f"clock time {b.time!r} is not HH:MM")
        elif b.time <= last:
            errs.append(f"clock time {b.time} is not later than {last}")
        last = b.time
        if len(b.event) > 62:
            errs.append(f"clock entry at {b.time} is {len(b.event)} chars, over 62")
        if not b.event.strip():
            errs.append(f"clock entry at {b.time} has no event")

    if not BRIEFS:
        errs.append("the briefs block is empty")
    for region, text in BRIEFS:
        if region not in filed:
            errs.append(f"brief tagged {region}, which files no story")
        if len(text) > 78:
            errs.append(f"brief {len(text)} chars, over 78: {text[:40]!r}...")
        if not text.strip():
            errs.append("an empty brief")

    # ---- the four story columns must hold the body without overrunning
    body_stories = [s for s in STORIES if not s.lead]
    columns = balance(body_stories)
    loads = [sum(story_height(s) for s in col) for col in columns]
    if any(not col for col in columns):
        errs.append("a story column came out empty")
    for i, load in enumerate(loads, 1):
        if load > BODY_BOX_H:
            errs.append(
                f"column {i} needs {load:.0f}px of {BODY_BOX_H:.0f}px -- the page will not hold it"
            )
        elif load < BODY_BOX_H * MIN_COL_FILL:
            errs.append(
                f"column {i} fills only {load:.0f}px of {BODY_BOX_H:.0f}px -- ragged column"
            )

    if errs:
        raise BuildError("\n".join("  - " + e for e in errs))
    return census, columns, loads


# ---------------------------------------------------------------- render

def esc(text: str) -> str:
    return html.escape(text, quote=True)


def render(census, columns) -> str:
    e = esc
    lead = next(s for s in STORIES if s.lead)
    total = len(STORIES)
    n_regions = len(census)

    census_html = "".join(
        f'<span class="c-reg"><span class="c-name">{e(r)}</span>'
        f'<span class="c-n">{n}</span></span>'
        for r, n in census.items()
    )

    figs = "".join(
        f'<div class="fig"><div class="fig-num">{e(f.numeral)}</div>'
        f'<div class="fig-gloss">{e(f.gloss)}</div>'
        f'<div class="fig-reg">{e(f.region)}</div></div>'
        for f in STATS
    )

    beats = "".join(
        f'<li class="beat"><span class="b-time">{e(b.time)}</span>'
        f'<span class="b-text">{e(b.event)}</span></li>'
        for b in CLOCK
    )

    def story_html(s: Story) -> str:
        cls = "story feature" if s.feature else "story"
        return (
            f'<article class="{cls}">'
            f'<div class="kicker">{e(s.region)}</div>'
            f'<h3 class="sh">{e(s.headline)}</h3>'
            f'<p class="sb">{e(s.body)}</p>'
            f"</article>"
        )

    cols_html = "".join(
        '<div class="col">' + "".join(story_html(s) for s in col) + "</div>"
        for col in columns
    )

    briefs = "".join(
        f'<li class="brief"><span class="br-reg">{e(r)}</span>'
        f'<span class="br-text">{e(t)}</span></li>'
        for r, t in BRIEFS
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{e(PAPER)} \u2014 {e(DAY_WORDS)}</title>
<link rel="stylesheet" href="poster.css">
</head>
<body>
<div class="page">

  <header class="mast">
    <div class="standfirst"><span>{e(VOLUME)}</span><span>{e(STANDING)}</span></div>
    <div class="dateline">{e(DAY_LINE)}</div>
    <h1 class="nameplate">{e(PAPER)}</h1>
    <div class="edition">{e(EDITION_FMT.format(n=total, r=n_regions))}</div>
    <div class="rule-double" aria-hidden="true"></div>
  </header>

  <section class="lead">
    <div class="lead-kick"><span class="tag">LEAD STORY</span><span class="tag-reg">{e(lead.region)}</span><span class="tag-day">{e(DAY_LINE)}</span></div>
    <h2 class="lead-head">{e(lead.headline)}</h2>
    <p class="lead-deck">{e(lead.deck)}</p>
    <p class="lead-body">{e(lead.body)}</p>
  </section>

  <section class="figures">
    <div class="strip-head"><span>FIGURES OF THE DAY</span><span>six numbers, one from each section</span></div>
    <div class="fig-row">{figs}</div>
  </section>

  <div class="census">
    <span class="c-label">STORIES BY REGION</span>
    {census_html}
    <span class="c-total">{total} FILED</span>
  </div>

  <div class="body">
    <div class="stories">{cols_html}</div>
    <aside class="clock">
      <div class="clock-head">THE DAY IN UTC</div>
      <ol class="beats">{beats}</ol>
      <p class="clock-note">Times are when each item was reported, not when it happened.</p>
    </aside>
  </div>

  <section class="briefs">
    <div class="brief-head">ALSO REPORTED</div>
    <ul class="brief-list">{briefs}</ul>
  </section>

  <footer class="colophon">
    <div class="rule-heavy" aria-hidden="true"></div>
    <div class="foot-line">
      <span class="f-paper">{e(PAPER)}  ·  {e(DAY_LINE)}</span>
      <span class="f-note">{e(FOOT_NOTE)}</span>
      <span class="f-page">PAGE 1 OF 1</span>
    </div>
  </footer>

</div>
</body>
</html>
"""


def main() -> int:
    try:
        census, columns, loads = validate()
    except BuildError as exc:
        print("poster.py: refusing to write the page -- the data contradict themselves:",
              file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1

    page = render(census, columns)
    OUT.write_text(page, encoding="utf-8")
    print(f"poster.py: wrote {OUT.name} -- {len(STORIES)} stories, {len(census)} regions, "
          f"{len(STATS)} figures, {len(CLOCK)} clock beats, {len(BRIEFS)} briefs")
    print("poster.py: census " + "  ".join(f"{r}={n}" for r, n in census.items()))
    print("poster.py: column fill " + "  ".join(f"{x:.0f}/{BODY_BOX_H:.0f}px" for x in loads))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
