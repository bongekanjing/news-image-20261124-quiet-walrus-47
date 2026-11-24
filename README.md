# news-image-20261124-quiet-walrus-47

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/bongekanjing/news-image-20261124-quiet-walrus-47/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/bongekanjing/news-image-20261124-quiet-walrus-47/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

The world's news of Tuesday 24 November 2026 on one page: a broadsheet front
page of 21 stories across six regions, with the day's six figures, a UTC
timeline and a region census.

Entered in [make.fun's daily news-image bounty](https://make.fun/bounty/news-image-20261124).

## The day it sums up

The lead is Nvidia's board reinstating Jensen Huang as chief executive eleven
days after he stepped down, sending the shares up more than 30% and all three
New York indices with them, while Washington argued over what was promised and
whether chips were part of the bargain. Around it: COP31 closing in Antalya with
no agreement, the first failure of a UN climate summit in 17 years; a fire at an
Indonesian candy factory with 34 workers missing; Kyiv region struck again;
Belgium's general strike grounding air travel; Denmark moving to ban phones in
schools; Iran vowing to counter the US naval blockade; and FIFA awarding the 2031
and 2035 Women's World Cups.

## What is here

- `entry.png` — the page, 1024x1024.
- `main.ts` — the program the grader runs: it checks the PNG header and copies
  the image to the output directory.
- `build/poster.py` — the data and the page. The day's reporting lives in
  `STORIES`, `STATS`, `CLOCK` and `BRIEFS`; the build refuses to write a page
  whose parts disagree (a region in the census with no story, a headline over its
  slot, a body that will not fit its lines, a column past the page).
- `build/poster.css` — the page's own styles.
- `build/render.sh` — renders `build/poster.html` to `entry.png` in headless
  Chrome and refuses a page that is not exactly 1024x1024 or that spilled past
  its frame.

## Build

```sh
bash build/render.sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
