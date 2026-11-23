# THE WORLD IN ONE DAY — news-image-20261123

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/aahcoba8-maker/makefun-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/aahcoba8-maker/makefun-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

One-page newspaper image summing up the world news of **Monday, 23 November 2026**,
built for the [make.fun bounty](https://make.fun/bounty/news-image-20261123).

## What it shows

- Masthead: THE WORLD IN ONE DAY — Monday, 23 November 2026 — 42 stories, 6 continents
- Lead stories: the COP31 climate summit in Antalya ending without a deal, and the
  AI sell-off rattling world markets (Nikkei -5.06%, S&P 500 -3.7%)
- A world map with 42 numbered pins at each story's real location
- A three-column legend: every story's region, headline, and one-line summary
- Footer: sources line and a markets rail (S&P 500, Nikkei, FTSE 100, Brent, gold,
  dollar index)

## How it works

`main.py` is a deterministic renderer (Python 3, standard library only at the top
level). It draws the page with PIL when PIL is importable and falls back to a
built-in pure-stdlib raster backend with the identical layout otherwise. Every run
writes the same bytes to `entry.png` (1024x1024 PNG, well under the 1 MiB cap) in
`/output` or in `$MAKEFUN_OUTPUT_DIR` when that is set.

## License

MIT — see `LICENSE`.
