# The World — Saturday 21 November 2026

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/0xyfann/makefun-news-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/0xyfann/makefun-news-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

A one-page newspaper front page summing up the world's news of
**Saturday 21 November 2026**, drawn from scratch in pure Python
(standard library only) for make.fun's
["Sum up 21 November's world news in one image"](https://make.fun/bounty/news-image-20261121)
bounty.

## The day in one page

- **Lead — the Gulf:** Iran strikes an industrial site in Bahrain, and
  tanker attacks near the Strait of Hormuz hit a wartime high; oil
  shipments through the strait are down 15 percent.
- **APEC, Shenzhen:** Trump, Xi and Putin at the APEC summit — the
  leaders of the three nuclear powers hold historic talks and agree a
  dialogue on nuclear risk.
- **Climate:** COP31 runs into overtime in Antalya as fossil-fuel
  wording stalls a deal.
- **Markets:** U.S. stocks fall into correction in an AI sell-off;
  Chinese AI shares shed $1.7 trillion.
- **Mexico:** cartel boss "El Chapo Isidro" (Fausto Isidro Meza Flores)
  captured in a Sinaloa raid; 11 killed.
- **Ukraine:** Russia hits Zelensky's hometown, Kryvyi Rih; Ukraine
  hits a Russia-bound ship at sea.
- **Peru:** a magnitude 6.7 quake shakes the Andes near Junin.
- **Brazil:** former president Bolsonaro in intensive care.
- **Science:** an Anthropic researcher says AI helped prove the
  Riemann hypothesis.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` draws the 1024x1024 front page with a hand-written 5x7
bitmap font and writes `out/entry.png`. Two runs write byte-identical
files. No network, no dependencies beyond Python 3.13's standard
library.

## License

MIT — see [LICENSE](LICENSE).
