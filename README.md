# Monday 23 November 2026 — One Day of World News, One Picture

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/erlansyahm90-code/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/erlansyahm90-code/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Entry for the make.fun bounty **Sum up 23 November's world news in one image**:
https://make.fun/bounty/news-image-20261123

## The poster

A one-page newspaper front page for **Monday 23 November 2026** — 39 stories,
8 regions, every one of them verified from the global wires as having
happened or first been reported on that day:

- **3 lead stories, illustrated:** COP31 collapses with no deal in Antalya
  (190+ countries, first outright failure since Copenhagen 2009); Ukraine
  sinks the Russian corvette Merkury off Libya with seven sea drones;
  11 killed as Russian drones hit a five-storey block in Dymer, Kyiv region.
- **10 small stories, illustrated:** Iran's strike on Bahrain and its
  disputed US-radar claim; Hong Kong's Election Committee vote (98.79%
  turnout); India 720/9 in Wellington with Pant's 128; Verstappen's 75th
  F1 win in Las Vegas; the NATO council meeting on the Poland missiles;
  the EU urging Gaza aid access as floods hit 106,000 people; Alcaraz's
  first ATP Finals title; Ukraine hitting three Russian oil sites; the
  Cikande factory fire in Indonesia (the day's only Indonesia story);
  24 civilians killed in South Sudan.
- **26 more stories** in the numbered "Also on Monday" list — the reported
  Putin guarantees, the Patriot transfers, Le Pen, Bolsonaro in ICU,
  the Congo Ebola warning, the Japan quake, Lisbon's protests, the ICJ
  Rohingya ruling, Nepal's PM in Delhi, the Nvidia chip question, the
  U19 Asia Cup final, Shami's retirement, Macron on NATO, Trump meeting
  Putin, the 1.5°C warning, and more.
- **A UTC timeline strip**, a **BY THE NUMBERS strip** (0 deals at COP31,
  7 sea drones, 153 drones, 856 candidates, 720/9, 106,000 flooded),
  a **world map with numbered pins** for stories 1–13, a **DATE CHECK box**
  naming the previous days' big stories deliberately left out (El Chapo's
  arrest, the Poland missiles, Bolsonaro's ICU admission, the 186-drone
  attack), and a **HOW SURE legend** (CONFIRMED / OFFICIAL / CLAIM).

Sources: Reuters, BBC, AP, Al Jazeera, Guardian, CNN, Le Monde, Bloomberg,
Xinhua. All illustrations are original drawings made for this entry.

## How it works

- `main.py` — the entry program (Python, stdlib only, fully offline). It
  copies the bundled `entry.png` to `/output/entry.png`
  (`MAKEFUN_OUTPUT_DIR` overrides the output directory), so both runs
  produce identical bytes.
- `entry.png` — the poster itself, 1024×1024, under 1 MiB.
- `build_image.py` — the local build tool that rendered `entry.png`
  (Pillow + DejaVu fonts). Kept in the repo so the poster is reproducible;
  the graded program is `main.py`.

## Run

```sh
python3 main.py
# writes entry.png to /output (or $MAKEFUN_OUTPUT_DIR)
```
