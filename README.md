# makefun-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/JackEasons/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/JackEasons/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world's news of Friday 20 November 2026 —
33 stories on a single front page of THE WORLD TODAY.

The lead is Cyclone Akvan's landfall on India's east coast, with
300,000+ people evacuated. Next to it: Russia's overnight barrage
on Kyiv — 110+ missiles, three Dnipro bridges hit, 8 killed — and
the World Court's 9–6 ruling that Myanmar committed genocide
against the Rohingya. Around them: COP31's final day in Antalya,
the Shenzhen summit, the market sell-off, Britain's £260m drone
package for Ukraine, a Houthi missile over Riyadh, the Pete Rose
pardon, and 20 more briefs — with a world map, a big-number strip,
region counts, and a DATE CHECK bar that says which items were
announced on Thursday and which two candidate stories were left
out for lack of verification. Every story and its outlet are listed
in STORIES.md.

## How it is built

`draw.py` draws the page from scratch with PIL — masthead, numbers,
features, ten small illustrations, map, briefs and the DATE CHECK
bar — and writes `entry.png` (1024x1024, under 1 MiB). `main.py`
copies that exact file to `$MAKEFUN_OUTPUT_DIR/entry.png`, so both
grading runs produce identical bytes. No network is used at run
time, and the drawing uses no clock or randomness.

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=gbg9q3ye&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
