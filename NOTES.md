# NOTES — news-image-20261123

## Story list (39, numbered as on the poster)

Leads: 1 COP31 collapses — no deal (Antalya). 2 Ukraine sinks Russian
corvette Merkury off Libya. 3 Russian drone strike on Dymer — 11 dead.

Cards: 4 Iran strikes Bahrain, US radar claim disputed [CLAIM].
5 Hong Kong Election Committee vote, 98.79% turnout. 6 India 720/9,
Pant 128. 7 Verstappen wins Las Vegas GP, 75th win. 8 NATO council meets
on Poland missiles. 9 Gaza: EU urges aid access, floods hit 106,000.
10 Alcaraz wins first ATP Finals. 11 Ukraine hits three Russian oil
sites. 12 Cikande factory fire, Indonesia — 3 dead. 13 South Sudan:
SPLA-IO attack kills 24 civilians.

Also on Monday (14–39): Putin "said to agree" NATO-style guarantees
(WaPo, REPORTED); Zelenskiy asks US to release paid-for Patriots;
Le Pen turns down Kyiv invite; Bolsonaro still in ICU day 3; WHO Ebola
warning in Congo; M6.1 quake in northern Japan; Lisbon cost-of-living
protests; ICJ rules Myanmar genocide of Rohingya; Nepal PM Balen Shah
visits India; India–China border talks; US asks Nvidia about China chip
sales; India beat Pakistan by 1 wicket, U19 Asia Cup final; Pakistan A
beat India A by 48 runs; Mohammed Shami retires from Tests; India
hockey 1–0 over New Zealand; Macron on Ukraine NATO entry; Trump meets
Putin at APEC; Israel kills Hamas commander Samir Abu Younis; global
temperatures set to pass 1.5°C; Russia lost 2,471 troops in a day
(Ukraine claim); Saudi intercepts Houthi missiles, 2 tankers hit;
Israeli drone strike kills 2 in Gaza; Australia calls for Bowen to quit
after COP31; India's Yadav on COP31; Lakshya Sen loses Hong Kong Open
semi; Gukesh prepares to face Uzbekistan in world chess.

Region counts: Europe 10, Middle East 5, Asia-Pacific 7, Americas 2,
Africa 2, Oceania 1, Sport 9, World 3 = 39.

## Date checks applied

- El Chapo Isidro's arrest was Friday 20 Nov — left out.
- The missiles that fell in Poland were Friday 20 Nov — today is the
  NATO council meeting, not the strike.
- Bolsonaro entered ICU Friday 20 Nov (reported 21 Nov) — only a
  running-story mention (item 17).
- Russia's 186-drone attack was the night of 21–22 Nov — today is the
  153-drone attack and Dymer (item 3).
- COP31 collapsed Sunday afternoon in Antalya, first widely reported
  Monday 23 Nov — included per "happened or first reported" rule.
- The Merkury sinking happened the night of 21–22 Nov, announced by
  Zelenskiy Monday 23 Nov — included per the same rule.
- Verstappen won Saturday night in Las Vegas, first reported 23 Nov UTC
  — included per the same rule.
- Indonesia: only one story (Cikande fire). MSCI–Indonesia was
  deliberately excluded to keep the one-Indonesia rule.

## Verification

- `python3 build_image.py` renders entry.png (1024×1024, ~212 KB).
- Two consecutive runs produce identical sha256 hashes (deterministic).
- `python3 main.py` copies entry.png to /output/entry.png byte for byte.
- Hallmark audit (visual, 23 Nov): cream newspaper theme, dark text;
  masthead date dominates; 3-second read = COP31 / Merkury / Dymer;
  all 10 consensus stories present as leads or cards; DATE CHECK names
  the real date traps; no text overflows its box in the final render.
