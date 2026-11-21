# makefun-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/JackEasons/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/JackEasons/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world's news of Friday 20 November 2026 —
33 stories on a single front page of THE WORLD TODAY. The lead is
Cyclone Akvan's landfall at Gopalpur (440,461 evacuated, no deaths),
next to Russia's biggest air strike of the month on Kyiv (111 missiles,
404 drones, three Dnipro bridges hit) and COP31 closing with fossil
fuels cut from the draft text — plus a big-number strip, ten more
illustrated stories, 20 briefs, a world map with numbered dots, a
markets box, and a DATE CHECK bar. Every story and its outlet are
listed in STORIES.md.

## Run it

```sh
python3 press.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`press.py` draws the page with PIL and writes `entry.png`; `main.py`
only copies that pre-rendered image into the output directory, so it
runs with no network and writes nothing into the repository.

---

<sub>Entered on [make.fun](https://make.fun/?ref=gbg9q3ye&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
