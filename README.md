# makefun-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/JackEasons/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/JackEasons/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world's news of Friday 20 November 2026.

Lead story: hours after the Shenzhen peace summit, Russia launches a massive overnight missile and drone attack on Kyiv, hitting three bridges over the Dnipro and killing at least five people in Kyiv and Lviv. Also: North Korea fires a ballistic missile toward the Sea of Japan; Anthropic closes up 17% on its stock-market debut near $97 after the $83 IPO, while Asian markets slide; the UK pledges £260 million and 1,000+ drones for Ukraine; Trump posthumously pardons Pete Rose and the US Senate rejects the Iran war-powers measure 51–48.

## Run it

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` copies `entry.png` (1024x1024 PNG, under 1 MiB) to `$MAKEFUN_OUTPUT_DIR/entry.png`, deterministically — both runs write the same bytes. No network is used at run time.

---

<sub>Entered on [make.fun](https://make.fun/?ref=gbg9q3ye&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
