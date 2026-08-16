# Slovenské vydania publikácií — slovník a pravidlá registra

Ústava prekladov na publications.barcik.training. Nadväzuje na
`BOOK_autobiography/translation/GLOSSARY_SK.md` (Bod v čase) a preberá jeho zásady;
odchýlky sú vyznačené. Každé rozhodnutie zapísané tu platí vo všetkých slovenských
vydaniach; ak sa počas prekladu ukáže ako zlé, zmení sa TU a potom všade naraz.

Preklad píše výhradne Fable 5 (ten istý model, ktorý písal alebo spolupísal originály) –
žiadna próza od menších modelov. Kontroly konzistencie smú byť skriptované.

## Kto číta a kto hovorí

| Rozhodnutie | Voľba | Poznámka |
|---|---|---|
| Publikum | Robertovi študenti a firemní účastníci školení – ľudia z IT, produktu, compliance | rozumejú anglickému žargónu; preklad má znieť ako slovenský odborný text, nie ako učebnica pre laikov |
| Oslovenie čitateľa | **vykanie** („viete", „predstavte si", „váš agent") | rovnako ako v knihe |
| Hlas Clauda (Field Notes, Claude Code, poznámky spoluautora) | prvá osoba, **mužský gramatický rod** („napísal som") | ako v knihe – gramatika, nie tvrdenie o identite; priznať v poznámke k prekladu |
| Hlas Roberta (jeho brožúry, eseje) | prvá osoba, mužský rod – prirodzene | |
| Význam pred slovom | idiómy sa prekladajú významovo, nikdy kalkom | pri hre so slovami hľadať slovenskú hru, nie vysvetlenie |
| Poznámka k prekladu | krátky odsek na obálke / v autorskej poznámke: prekladal ten istý model, dátum, mužský rod, významovo | podpísaná; neprepisuje pôvodné podpisy a dátumy |
| Čo sa NEprekladá | názvy repozitárov, súborov, príkazy, skratky (MCP, RLHF), názvy modelov, názvy zručností v kurzíve (*wrap-up*, *drive-push*), URL | pri prvom výskyte podľa potreby glosa v zátvorke |
| Názvy publikácií v odkazoch | slovenský názov, ak SK vydanie existuje; inak pôvodný anglický názov + slovenský dovetok, ak je užitočný | krížové odkazy smerujú na SK vydanie, ak existuje, inak na EN |
| Úvodzovky | „…“ (U+201E … U+201C; vnútorné ‚…‘) | slovenská typografia, ako v knihe |
| Pomlčky | – (s medzerami) | Robertovo pravidlo „žiadne em-dash" platí aj v slovenčine: pomlčku používať striedmo, radšej dvojbodku alebo bodku |
| Čísla, dátumy | 39 000; desatinná čiarka; 12. júla 2026 | |

## Odchýlka od knižného slovníka: „AI", nie „UI"

Kniha používa skratku UI. V praktických publikáciách pre IT publikum používame **AI**
(„umelá inteligencia" rozpísaná pri prvom výskyte v texte, ďalej AI): skratka UI koliduje s
používateľským rozhraním a v slovenskej firemnej praxi sa dnes bežne hovorí AI. Rovnako
znie aj kolofón transparentnosti („Transparentnosť AI").

## Skloňovanie mien

| Meno | Vzor |
|---|---|
| Claude | Clauda, Claudovi, Claudom |
| Claude Code | Claude Code (nesklonné; oporne „nástroj Claude Code", „v Claude Code") |
| Fable / Opus / Sonnet | nesklonné pri modeloch („model Fable 5", „modelu Opus 4.8"); Sonnet sa smie skloňovať (Sonnetu), Opus a Fable nie |
| Anthropic | Anthropicu, Anthropicom |
| Robert Barcik | Roberta Barcika, Robertovi Barcikovi |
| Udemy, Skillmea, GitHub, AWS | nesklonné / prirodzene: „na Udemy", „na GitHube", „v AWS" |

## Technický slovník (drží sa vo všetkých vydaniach)

### Agenti, nástroje, prevádzka

| EN | SK | Poznámka |
|---|---|---|
| agent / agentic | agent / agentný („agentná práca", „agentné systémy") | nie „agentický" |
| AI colleague | AI kolega | titul: „váš AI kolega" |
| human in the loop / the loop | človek v slučke / slučka | prvý výskyt s glosou (human in the loop); „the other side of the loop" = „druhá strana slučky" |
| delegation / to delegate | delegovanie / delegovať | |
| brief | zadanie | „the brief travels invisibly" = „zadanie cestuje neviditeľne" |
| prompt | prompt (promptu, prompty) | |
| context window | kontextové okno | |
| token(s) | token, tokeny | |
| memory (persistent) | pamäť; „memory directory" = pamäťový adresár | |
| skill (Claude Code) | zručnosť (skill) | prvý výskyt s glosou; názvy zručností ostávajú anglicky v kurzíve |
| sub-agent | podagent | |
| workflow | pracovný postup | „workflow" ponechať len v názvoch |
| repository / repo | repozitár | „repo" hovorovo ponechať ako „repo" iba v priamej reči/skratke |
| commit (n./v.) | commit / commitnúť | IT úzus; skloňovať: commity, commitov |
| push / pull | push / pull (nesklonné, kurzíva netreba) | „push je podmienený schválením" |
| deploy / deployment | nasadiť / nasadenie | |
| build (n.) | zostavenie (build) | v kontexte kurzov: „výstavba kurzu" |
| render | vykresliť | „render it and look at it" = „vykresliť a pozrieť sa" |
| grep (v.) | mechanicky vyhľadať (grep) | prvý výskyt s glosou; potom „grepnúť" iba v hovorovom tóne |
| pipeline | pipeline (nesklonné) / reťazec spracovania | podľa registra |
| backlog | backlog | |
| shell command | shellový príkaz | |
| terminal | terminál | |
| ops room / operations | prevádzková miestnosť / prevádzka | „operations specialist" = prevádzkový špecialista |
| blast radius | polomer škôd (blast radius) | prvý výskyt s glosou |
| trust dial | regulátor dôvery | „Trust is a dial, not a door" = „Dôvera je regulátor, nie dvere" |
| guardrails | mantinely | |
| kill switch | vypínač (kill switch) | |
| review / review pass | revízia / revízny prechod | „review-gotchas file" = súbor s poučeniami z revízií |
| receipts (idiom) | doklady | „With Receipts" = „aj s dokladmi" |
| verification | overovanie | „verify artifacts, never assurances" = „overujte výstupy, nie uistenia" |
| artifact | výstup / artefakt | v bežnej vete „výstup", pri technickom rozlíšení „artefakt" |
| gotcha | úskalie / poučenie | |
| filing system | kartotéka | „gardening a filing system" = „starať sa o kartotéku" |
| freshness | čerstvosť | „freshness watch" = strážca čerstvosti |
| trigger log | denník spúšťačov | |
| open loop | otvorená úloha | |
| leash | vôdzka | „when the leash came off" = „keď sa pustila vôdzka" |

### Modely a technika

| EN | SK | Poznámka |
|---|---|---|
| large language model (LLM) | veľký jazykový model (LLM) | |
| frontier model / the frontier | frontier model / hranica možností | „the frontier" ako pojem: „frontier" ponechať pri prvom výskyte s glosou „(špička)"; ďalej „špička" alebo „frontier modely" |
| open-weight | s otvorenými váhami | |
| weights / parameters | váhy / parametre | |
| inference | inferencia | |
| fine-tuning | dolaďovanie | |
| RLHF | RLHF | |
| benchmark | benchmark | |
| hallucination / confabulation | halucinácia / konfabulácia | |
| chain of thought / reasoning | reťazec uvažovania / uvažovanie | |
| tool use / function calling | používanie nástrojov / volanie funkcií | |
| MCP (Model Context Protocol) | MCP | |
| capability | schopnosť; „capability became illegible" = „schopnosť sa stala nečitateľnou" | |
| long-horizon (work) | práca s dlhým horizontom | |
| compute | výpočtový výkon (compute) | |
| gated access | prístup za bránou / obmedzený prístup | „gated frontier" = špička za bránou |
| free tier | bezplatná úroveň | |
| chat window | chatové okno | |
| Full Disk Access | Full Disk Access (názov nastavenia macOS) | ponechať |

### Právo a organizácie

| EN | SK | Poznámka |
|---|---|---|
| EU AI Act | Akt EÚ o umelej inteligencii (AI Act) | prvý výskyt celé, ďalej „AI Act" |
| provider / deployer | poskytovateľ / nasadzujúci subjekt | úradná slovenská terminológia nariadenia |
| high-risk system | vysokorizikový systém | |
| conformity assessment | posudzovanie zhody | |
| Official Journal | Úradný vestník EÚ | |
| Digital Omnibus | Digital Omnibus | |
| standard (harmonised) | (harmonizovaná) norma | |
| oversight | dohľad | „human oversight" = ľudský dohľad |
| compliance | súlad (compliance) | |

## Watchlist (rozhodnutia z konkrétnych miest)

- Field Notes, Part 3 nadpis „Where I Fail, With Receipts" → „Kde zlyhávam, aj s dokladmi".
- Field Notes, Part 5 „act, then tell / build freely, ship on approval / prepare, never send" →
  „konať a potom povedať / stavať voľne, dodať po schválení / pripraviť, nikdy neodoslať".
- Field Notes, Part 6 „a committee of former colleagues, each of whom left after a single day" →
  „výbor bývalých kolegov, z ktorých každý odišiel po jedinom dni".
- „Put the brief in the furniture, not the prompt" → „Zadanie patrí do nábytku, nie do promptu"
  (metafora nábytku sa drží v celom texte: „constraint was waiting for me in the room").
- „This was mine." (záver Field Notes) → „Táto bola moja." (vzťahuje sa na otázku).
- Claude Code: „honesty box" → „schránka úprimnosti"; „bloopers" → „prešľapy".
- Invisible Curve: „gotchas" (people who collect gotchas) → „ľudia, ktorí zbierajú prešľapy" /
  „úlovky"; rozhodnuté pri preklade.
