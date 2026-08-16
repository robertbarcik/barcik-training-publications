# Kapitola 3: Nákladová rovnica: ekonomika API, prenájmu a on-prem v každom rozsahu

> **V skratke**
>
> - Existujú tri spôsoby, ako prevádzkovať produkčnú AI záťaž (API za token, prenajaté GPU, vlastný hardvér), a ich ekonomika je naozaj rôzna. Každá tabuľka v tejto kapitole je označená svojím režimom.
> - Náklady na API sú lineárne: 5,40 $ (rozpočtová úroveň) až 180 $ (frontier úroveň) na používateľa mesačne, v akomkoľvek rozsahu. Náklady vlastného hostingu na používateľa s rozsahom strmo klesajú.
> - Vlastný hardvér poráža prenájom zhruba 3× na výpočtovej položke. Oproti cenám API strednej triedy sa vlastné nasadenie 20B pretína zhruba pri 250 – 350 používateľoch, ale len tam, kde je menší model pre záťaž naozaj dosť dobrý.
> - Pre klientov vyžadujúcich on-prem sa porovnanie úplne obracia: vaša spravovaná služba oproti klientovým nákladom urobiť si to sám 125 – 204 $ na používateľa mesačne. To je tradičná ekonomika spravovaných služieb pri maržiach 40 – 55 %.
>
> **Číslo, ktoré si zapamätať:** 5,40 $, náklady API rozpočtovej úrovne na používateľa mesačne. Každý biznisový prípad vlastného hostingu sa mu musí zodpovedať.

Toto je kapitola, kde prestávame hovoriť v abstrakciách a začíname hovoriť v peniazoch. Ak si z tejto brožúry odnesiete jednu vec, mali by to byť čísla na týchto stranách. Buď potvrdia váš strategický smer, alebo vás prinútia ho zmeniť.

Kým prepočítame čísla, musíme byť presní v tom, čo porovnávame. Existujú tri odlišné spôsoby prevádzky produkčnej AI záťaže a ekonomika každého je naozaj iná. Prejdeme úplné náklady každého režimu v štyroch rozsahoch (10, 100, 500 a 1 000 používateľov), porovnáme ich medzi sebou a s komerčnými API a, čo je kľúčové, ukážeme, že pre klientov vyžadujúcich on-prem je porovnanie, na ktorom záleží, znovu iné: vaša spravovaná služba oproti tomu, že si to klient urobí sám.

Poznámka k mene: ceny API, GPU hardvér a sadzby prenájmu sú v tejto kapitole uvádzané v USD, lebo tak ich uvádzajú dodávatelia. Platy, licenčné poplatky a rozpočty inde v brožúre sú v EUR, lebo tak ich uvádza trh EÚ. Konvencia v celom texte: každé číslo ostáva v mene, ktorú jeho trh naozaj používa.

---

## Tri režimy nasadenia

Každá AI záťaž beží v jednom z troch režimov. Ceny, kapitálová štruktúra a prevádzková záťaž sa medzi nimi podstatne líšia.

*Tabuľka 3.1 · Tri režimy nasadenia*

| Režim | Definícia v jednom riadku | Kto vlastní GPU | Kto prevádzkuje modelový stack |
|---|---|---|---|
| **Spotreba API** | Platíte za token komerčnému poskytovateľovi | Hyperškálová firma | Hyperškálová firma |
| **Prenajatá vyhradená inferencia** | Rezervujete GPU-hodiny od cloudového poskytovateľa a spúšťate na nich vlastný model | Cloudový poskytovateľ (AWS, GCP, Azure, Lambda, RunPod, CoreWeave) | Vy |
| **Vlastná on-prem inferencia** | Kúpite hardvér; nainštalujete do svojho racku alebo kolokácie | Vy | Vy |

**Spotreba API** je možnosť s najmenším trením: OpenAI, Anthropic, Google a Mistral vezmú váš prompt a účtujú vám za milión tokenov. Nepíšete žiadny infraštruktúrny kód.

**Prenajatá vyhradená inferencia** je to, čo väčšina tímov myslí, keď mimochodom povie „vlastný hosting“. Roztočíte inštanciu s pripojenými H100, nasadíte vLLM alebo TGI, načítate model s otvorenými váhami a obsluhujete ho. Fyzické GPU je kapitál niekoho iného; vy platíte mesačne (alebo hodinovo) za výhradný prístup.

**Vlastná on-prem inferencia** je tradičný IT model: objednávka, odpisový plán, priestor v racku, zmluva o napájaní, náhradné kusy v sklade. Nič neopúšťa váš perimeter. Kapitálové výdavky vopred, potom nižšie prevádzkové náklady mesačne.

Štvrtý režim, **lokálna inferencia na okraji**, kde model beží na notebooku zamestnanca, je témou kapitoly 7 a má vlastnú ekonomiku. Táto kapitola je o troch vyššie.

Keď v tejto kapitole čítate tabuľku, skontrolujte označenie. Každá nákladová tabuľka nižšie je označená jedným z tých troch režimov. Ich miešanie je spôsob, ako sa biznisové prípady pokazia.

---

## Ako modelujeme používanie

Každé číslo, ktoré nasleduje, závisí od predpokladu o používaní. Každý bod zlomu, každé tvrdenie „toto poráža tamto“, každý záver sa pohne, ak sa predpoklad zmení. Tak ho vyslovme výslovne.

Východiskom v celej kapitole je **jeden milión tokenov na používateľa denne**, rozdelených v pomere vstup : výstup 3 : 1. To je predpoklad ťažkého používania vhodný pre znalostného pracovníka, ktorý integroval AI do svojho denného pracovného postupu: vývojára používajúceho asistenta na programovanie celý deň, analytika spúšťajúceho vyhľadávanie nad veľkými sadami dokumentov, konzultanta s dlho bežiacim agentným postupom zhŕňajúcim stretnutia a píšucim návrhy výstupov.

Pre orientáciu: 1M tokenov je zhruba 750 strán anglického textu denne na používateľa, vstup a výstup spolu. Znie to veľa, kým nespočítate agentov používajúcich nástroje, ktorí si pri každom ťahu znovu čítajú vlastný kontext, vyhľadávacie systémy, ktoré napchajú 30 – 40K tokenov kontextu do každého volania, a realitu, že výstupné tokeny sú v agentnej záťaži len špička ľadovca.

**Kalibrujte to na svojich klientov.** Ak je vaša populácia ľahšia (občasný chat, príležitostné zhŕňanie, 100 – 300K tokenov na používateľa denne), všetky čísla na strane API v tejto kapitole úmerne klesnú, kým čísla prenájmu a vlastného hardvéru ostanú takmer nezmenené (fixné náklady na GPU sa s nižším využitím nezmenšia). Praktický účinok: pri 300K tokenov denne sa každý bod zlomu medzi vlastným hostingom a API posunie zhruba trikrát ďalej doprava. Vlastný hosting pre 300 používateľov pri ľahkom používaní sa ekonomicky podobá vlastnému hostingu pre 100 používateľov pri ťažkom používaní.

Vzorkujte vlastných klientov, kým sa zaviažete ku ktorejkoľvek z týchto tabuliek. Východisko 1M/deň je obhájiteľná horná hranica pre tímy znalostných pracovníkov, ktorí AI naozaj prijali; je to nadhodnotenie pre populácie stále v pilotnej fáze.

---

## Krajina cien API (apríl 2026)

Keďže každý režim sa nakoniec porovnáva s cenami API, ustanovíme ich ako prvé. Tu je, čo štyria veľkí poskytovatelia a hostované modely s otvorenými váhami účtujú za milión tokenov, vstup a výstup.

*Tabuľka 3.2 · Ceny API za milión tokenov, apríl 2026 (režim: API)*

| Poskytovateľ | Model | Vstup (za M tokenov) | Výstup (za M tokenov) |
|---|---|---|---|
| **OpenAI** | GPT-4.1 | 2,00 $ | 8,00 $ |
| | GPT-4o | 2,50 $ | 10,00 $ |
| | GPT-4o-mini | 0,15 $ | 0,60 $ |
| **Anthropic** | Claude Haiku 4.5 | 1,00 $ | 5,00 $ |
| | Claude Sonnet 4.6 | 3,00 $ | 15,00 $ |
| | Claude Opus 4.6 | 5,00 $ | 25,00 $ |
| **Google** | Gemini Flash-Lite | 0,10 $ | 0,40 $ |
| | Gemini Flash | 0,30 $ | 2,50 $ |
| | Gemini Pro | 1,25 $ | 10,00 $ |
| **Mistral** | Small | 0,20 $ | 0,60 $ |
| | Medium | 1,00 $ | 3,00 $ |
| | Large | 2,00 $ | 6,00 $ |
| **Llama (hostovaná)** | 8B | 0,05 $ | 0,08 $ |
| | Maverick | 0,15 $ | 0,60 $ |
| | 70B | 0,70 $ | 0,90 $ |

Z tejto tabuľky vyskakuje niekoľko vzorov.

Po prvé, **cenová podlaha stále klesá.** Flash-Lite od Googlu za 0,10 $/0,40 $ a Llama 8B za 0,05 $/0,08 $ sú pre väčšinu biznisových prípadov použitia takmer zadarmo. Pred rokom tieto cenové body pre modely porovnateľných schopností neexistovali.

Po druhé, **medzi najlacnejšími a najdrahšími modelmi je 50 – 100-násobný rozptyl.** Volanie Gemini Flash-Lite stojí zhruba 1/50 volania Claude Opus 4.6. Pre väčšinu rutinných podnikových úloh (zhŕňanie, klasifikácia, extrakcia, jednoduché otázky a odpovede) sú lacnejšie modely viac než primerané.

Po tretie, **výstupné tokeny sú u väčšiny poskytovateľov 3 – 5× drahšie než vstupné.** Na tom záleží pri modelovaní nákladov: chatbot, ktorý produkuje dlhé, podrobné odpovede, bude stáť podstatne viac než ten, ktorý dáva stručné.

Teraz premeňme tie ceny na mesačný účet. S naším východiskom 1M tokenov na používateľa denne generuje 100 používateľov zhruba 3 miliardy tokenov mesačne (1M tokenov × 100 používateľov × 30 dní). Pri pomere vstup : výstup 3 : 1 sa tri štvrtiny tých tokenov účtujú za vstupnú cenu a štvrtina za výstupnú, takže zmiešaná sadzba každého modelu je:

> **Zmiešaná sadzba za M tokenov ≈ 0,75 × vstupná cena + 0,25 × výstupná cena**

Raz rozpracované pre Gemini Flash-Lite: 0,75 × 0,10 $ plus 0,25 × 0,40 $ dáva 0,175 $, zaokrúhlene ~0,18 $ za milión tokenov. Vynásobte 3 000 (mesačné 3 miliardy tokenov počítané v miliónoch) a dostanete 540 $ mesačne, čiže 5,40 $ na používateľa. Každý riadok tabuľky nižšie je postavený presne rovnako, takže si ju môžete prestavať s objemami tokenov vlastného klienta a tabuľka sa stane vašou.

*Tabuľka 3.3 · Mesačné náklady API pri 100 používateľoch podľa úrovne modelu (režim: API)*

| Úroveň modelu | Zmiešaná sadzba (za M tokenov) | Mesačné náklady (3 mld. tokenov) | Na používateľa |
|---|---|---|---|
| Gemini Flash-Lite | ~0,18 $ | 540 $ | 5,40 $ |
| GPT-4o-mini | ~0,30 $ | 900 $ | 9,00 $ |
| Llama 70B (hostovaná) | ~0,75 $ | 2 250 $ | 22,50 $ |
| Mistral Medium | ~1,50 $ | 4 500 $ | 45,00 $ |
| Claude Haiku 4.5 | ~2,00 $ | 6 000 $ | 60,00 $ |
| GPT-4o | ~4,40 $ | 13 200 $ | 132,00 $ |
| Claude Sonnet 4.6 | ~6,00 $ | 18 000 $ | 180,00 $ |

Používanie rozpočtovej úrovne za 5,40 $ na používateľa mesačne je benchmark, ktorý každé vlastne hostované nasadenie bude mať problém poraziť iba na nákladoch. Držte to číslo; opakovane sa k nemu vraciame.

---

## Ceny prenájmu GPU (apríl 2026)

Toto sú sadzby, ktoré poháňajú matematiku režimu prenájmu nižšie. Ceny sa výrazne líšia podľa poskytovateľa, úrovne záväzku a dostupnosti.

*Tabuľka 3.4 · Sadzby prenájmu GPU, apríl 2026 (režim: prenájom)*

| GPU | Rozsah hodinovej sadzby | Mesačný odhad (730 h) |
|---|---|---|
| NVIDIA H100 (80 GB) | 1,49 – 6,98 $ | 1 088 – 5 095 $ |
| NVIDIA H200 (141 GB) | 2,29 – 10,60 $ | 1 672 – 7 738 $ |
| NVIDIA A100 (80 GB) | 0,78 – 2,50 $ | 569 – 1 825 $ |
| NVIDIA A6000 (48 GB) | 0,50 – 1,20 $ | 365 – 876 $ |
| NVIDIA L40S (48 GB) | 0,60 – 1,80 $ | 438 – 1 314 $ |

Spodný koniec týchto rozsahov odráža spotové ceny alebo dlhodobé rezervácie u menších GPU cloudových poskytovateľov (Lambda, RunPod, Vast.ai, CoreWeave). Horný koniec odráža ceny na požiadanie od veľkých hyperškálových firiem (AWS, Azure, GCP). Pre produkčné záťaže vyžadujúce spoľahlivosť a SLA rozpočtujte smerom k strednému až hornému rozsahu.

> **Kľúčové posolstvo:** Ceny prenájmu GPU klesli zhruba o 30 – 40 % medziročne, ako sa rozšírila ponuka, ale ostávajú podstatné. Jediné H100 pri stredných cenách (2 500 – 3 500 $/mesiac) stojí mesačne viac než mnohé tradičné serverové konfigurácie. Toto je GPU ako prémiová komodita, nie GPU ako utilita.

---

## Režim B: prenajatá vyhradená inferencia

Toto je režim, na ktorý mnohé tímy myslia ako prvé, keď si predstavia „spustiť si model sami“. Rezervujete GPU kapacitu od cloudového poskytovateľa, nasadíte model s otvorenými váhami a obsluhujete ho sami. Ekonomika je priama: mesačný prenájom GPU plus prevádzková réžia.

### Stručne: prečo hra so 120B frontier triedou nefunguje

Model so 120B parametrami v plnej presnosti (kvantizovaná Llama 3.1 405B, Mistral Large alebo podobný) vyžaduje na obsluhu 100 súbežných používateľov 3 – 4 uzly 8× H100, pričom samotný prenájom GPU beží na 30 000 – 50 000 $ mesačne a realistické celkové náklady sú 600 – 1 000 $ na používateľa mesačne, keď sa zahrnie prevádzka, pozorovateľnosť, sieť a personál. Podnikové AI licencie od hyperškálových firiem sa cenníkovo pohybujú na 20 – 30 $ na používateľa mesačne pri štandardných úrovniach a až 200 $ na prémiovom konci. Matematika nefunguje: potrebovali by ste hodnotovú ponuku tak presvedčivú, aby zákazníci platili 3 – 5× bežnú sadzbu. Pre drvivú väčšinu poskytovateľov IT služieb nie je vlastný hosting frontier triedy v režime prenájmu biznis. Nezdržiavame sa pri tom, lebo je to slepá ulička; čítajte ďalej k režimu, ktorý funguje.

### Realistická hra: model 20B

Realistickou hrou je menší, efektívnejší model, 20B parametrov alebo menej. Modely ako Mistral Small, Llama 3.1 8B/70B (kvantizovaná) alebo doménovo špecifické doladenia v rozsahu 7 – 20B dodávajú silný výkon pri sústredených podnikových úlohách a bežia na oveľa menšom hardvéri.

Aby ste videli, ako sa náklady prenajatého nasadenia naozaj skladajú, tu je úplná skladba v rozsahu 100 používateľov: zdieľané oddelenské nasadenie, najbežnejšia prvá vážna zákazka.

*Tabuľka 3.5 · Skladba nákladov prenájmu pri 100 používateľoch, model 20B (režim: prenájom)*

| Zložka | Mesačné náklady |
|---|---|
| 2× H100 (zvládajú súbežnosť a priepustnosť) | 5 000 – 8 000 $ |
| Prevádzková réžia (monitorovanie, podpora, záplatovanie, pohotovosť) | 5 000 – 8 000 $ |
| **Spolu** | **10 000 – 16 000 $** |
| **Na používateľa** | **100 – 160 $** |

Všimnite si, že v tomto rozsahu sa prevádzková réžia zhruba rovná výpočtovému výkonu. Potrebujete poriadne monitorovanie, nasadzovaciu pipeline, niekoho na pohotovosti a proces aktualizácií modelu a bezpečnostných záplat. GPU sa možno prevádzkuje samo, ale systém okolo neho nie. A 100 používateľov typicky predstavuje čerstvo spustené nasadenie vo validácii; prevádzka na používateľa je tu vyššia než pri väčších rozsahoch, lebo ho stále vodíte za ruku.

Teraz rovnaká konštrukcia vo všetkých štyroch rozsahoch. Toto je tabuľka, ktorá ukazuje, prečo rozsah mení všetko.

*Tabuľka 3.6 · Prenájom v štyroch rozsahoch, model 20B (režim: prenájom)*

| Rozsah | Prenájom GPU | Prevádzková réžia | Mesačne spolu | Na používateľa |
|---|---|---|---|---|
| 10 používateľov (vyhradené zariadenie pre zákazníka) | 2 000 – 3 000 $ | 500 – 1 000 $ | 2 500 – 4 000 $ | 250 – 400 $ |
| 100 používateľov (zdieľané oddelenské) | 5 000 – 8 000 $ | 5 000 – 8 000 $ | 10 000 – 16 000 $ | 100 – 160 $ |
| 500 používateľov (biznisová jednotka / stredný podnik) | 7 500 – 12 000 $ | 3 500 – 6 000 $ | 11 000 – 18 000 $ | 22 – 36 $ |
| 1 000 používateľov (veľký podnik / multi-tenant) | 11 000 – 18 000 $ | 7 000 – 9 000 $ | 18 000 – 27 000 $ | 18 – 27 $ |

*Poznámka k stĺpcu prevádzky, ktorý zámerne nie je monotónny: pri 100 používateľoch vodíte za ruku nasadenie stále vo validácii; pri 500 používateľoch sa platforma usadila do ustáleného stavu a rovnaké nástroje pokrývajú viac miest; pri 1 000 používateľoch multi-tenant zložitosť (izolácia klientov, reporting po klientoch, koordinované okná zmien) tlačí prevádzku späť hore.*

Čítajte stĺpec na používateľa zhora nadol: 250 – 400 $, potom 100 – 160 $, potom 22 – 36 $, potom 18 – 27 $. Príbeh vlastného hostingu je v tomto stĺpci. Pri 10 používateľoch (scenár „súkromného AI zariadenia“ s plnou izoláciou dát pre jediného zákazníka) sú náklady na používateľa bolestivé. Pri 500 používateľoch sa využitie dramaticky zlepší: toľko používateľov generuje dosť prevádzky, aby udržali GPU klastre počas pracovného dňa rozumne zaneprázdnené, a rovnaký monitoring, podpora a nástroje sa rozložia na viac miest. Pri 1 000 používateľoch sa ekonomika rozhodne nakloní: prenájom menšieho modelu začína podbiehať ceny API strednej triedy pri zachovaní plnej dátovej suverenity. To je sladký bod pre poskytovateľov, ktorí vedia agregovať dopyt naprieč viacerými klientmi.

### Protivietor využitia

Každé číslo vyššie predpokladá, že prenajaté GPU bežia 24/7. Bežia; platíte za 730 hodín mesačne, či sú vaši používatelia aktívni, alebo spia. Vyhradený klaster 2× H100 obsluhujúci 100 používateľov je počas pracovných hodín pravdepodobne na 30 – 40 % priemerného využitia a v noci a cez víkendy blízko nuly. Platíte za 100 % kapacity a používate 30 – 40 %.

API hyperškálových firiem túto krivku splošťujú naprieč miliónmi geograficky rozptýlených používateľov a prevádzkujú svoje flotily na 80 – 90 %+ využití. Štrukturálna nákladová výhoda, ktorú to vytvára, je jedným z dôvodov, prečo ceny API môžu sedieť pod tým, čo vyzerá ako rozumná podlaha. Kapitola 4 mechaniku podrobne skúma.

---

## Režim C: vlastná on-prem inferencia

Toto je režim, ktorý dostáva vo väčšine textov najkratšie spracovanie a tu potrebuje najviac pozornosti, lebo pre klientov z regulovaných odvetví v EÚ je často jedinou životaschopnou architektúrou.

V režime vlastníctva vy (alebo váš klient) GPU kúpite. Kapitálové výdavky vopred, potom elektrina, chladenie, sieť, kolokácia alebo priestor v dátovom centre a personál. Amortizovaná počas trojročnej účtovnej životnosti vyzerá výpočtová položka veľmi inak než prenájom.

### Realita capexu: čo hardvér naozaj stojí

Najprv cenovky. Z tabuľky hardvéru v kapitole 2, pri cenách z roku 2026:

*Tabuľka 3.7 · Nákupné ceny GPU, apríl 2026 (režim: vlastníctvo)*

| GPU | Nákupná cena | VRAM | Typické použitie |
|---|---|---|---|
| NVIDIA H100 80 GB (SXM) | 25 000 – 40 000 $ | 80 GB HBM3 | Produkčná inferencia, modely 20B – 70B |
| NVIDIA H200 141 GB | 30 000 – 45 000 $ | 141 GB HBM3e | Väčšie modely, vyššia priepustnosť |
| NVIDIA A100 80 GB | 15 000 – 17 000 $ | 80 GB HBM2e | Predchádzajúca generácia, dobrý pomer cena/výkon |
| NVIDIA L40S | 7 000 – 10 000 $ | 48 GB GDDR6X | Optimalizované na inferenciu, menšie modely |

Serverová skriňa, prepojenie NVLink/NVSwitch, sieť, zdroj a integrácia do racku pridávajú zhruba 20 – 30 % k cene GPU na uzol. Inferenčný uzol 2× H100 na kľúč pristáva okolo 75 000 – 95 000 $. Kolokácia (ak nemontujete do vlastného DC) beží na 500 – 1 500 $ mesačne za stopu jedného uzla vrátane napájania a chladenia.

### Vlastníctvo: rovnaká záťaž 20B, nacenená ako kapitál

Tu je rovnaké nasadenie pre 100 používateľov ako v tabuľke 3.5, ale s vlastným hardvérom amortizovaným počas 36 mesiacov namiesto prenájmu. Prevádzkové náklady sú nezmenené: to sú ľudia a nástroje, nie hardvér.

*Tabuľka 3.8 · Skladba nákladov vlastníctva pri 100 používateľoch, model 20B, 36-mesačná amortizácia (režim: vlastníctvo)*

| Zložka | Mesačné náklady |
|---|---|
| 2× H100 kúpené (amortizované 36 mes.) | 1 700 – 2 400 $ |
| Server, sieť, rack, rezerva náhradných dielov | 400 – 600 $ |
| Kolokácia / napájanie / chladenie | 800 – 1 500 $ |
| Prevádzková réžia | 5 000 – 8 000 $ |
| **Spolu** | **7 900 – 12 500 $** |
| **Na používateľa** | **79 – 125 $** |

Porovnajte výpočtovú položku s prenájmom: 1 700 – 2 400 $ vlastné oproti 5 000 – 8 000 $ prenajaté za tie isté dve H100. Výpočtový výkon samotný je pri vlastníctve zhruba 3× lacnejší. Celkový rozdiel je menší (zhruba 20 – 30 %), lebo dominuje prevádzka a tá je rovnaká tak či tak. Ale medzera je skutočná a vo veľkom sa úročí.

A úplný rebrík rozsahov, vlastníctvo:

*Tabuľka 3.9 · Vlastníctvo v štyroch rozsahoch, model 20B, 36-mesačná amortizácia (režim: vlastníctvo)*

| Rozsah | GPU (amortizované) | Infra + kolokácia | Prevádzka / podpora | Mesačne spolu | Na používateľa |
|---|---|---|---|---|---|
| 10 používateľov (hardvérové zariadenie, trieda L40S) | 280 – 420 $ | 300 – 600 $ | 500 – 1 000 $ | 1 100 – 2 000 $ | 110 – 200 $ |
| 100 používateľov (2× H100, zdieľané oddelenské) | 1 700 – 2 400 $ | 1 200 – 2 100 $ | 5 000 – 8 000 $ | 7 900 – 12 500 $ | 79 – 125 $ |
| 500 používateľov (3× H100, biznisová jednotka) | 2 500 – 3 600 $ | 1 800 – 3 100 $ | 3 500 – 6 000 $ | 7 800 – 12 700 $ | 16 – 25 $ |
| 1 000 používateľov (4× H100, veľký podnik) | 3 300 – 4 800 $ | 2 600 – 4 400 $ | 7 000 – 9 000 $ | 12 900 – 18 200 $ | 13 – 18 $ |

*Riadok pre 10 používateľov zahŕňa softvérovú licenciu a linku vzdialenej podpory namiesto plného prevádzkového personálu; hardvér zariadenia vopred je jednorazovo 10 000 – 15 000 $. Stĺpec prevádzky sleduje tie isté tri režimy ako prenájom: vodenie za ruku vo validačnej fáze pri 100 používateľoch, ustálený stav pri 500, multi-tenant zložitosť pri 1 000.*

Rovnaký príbeh na používateľa ako pri prenájme, ale lacnejší na každej priečke. Zariadenie pre 10 používateľov (kapitál vopred, potom nízke priebežné náklady) funguje najlepšie pre regulované odvetvia, kde dáta musia ostať on-prem: zdravotníctvo, právo, finančné služby. Pri 500 používateľoch vlastný hardvér začína podbiehať ceny API strednej triedy (60 $/používateľ pri sadzbách Haiku / Mistral Medium); tu sa prípad vlastného hardvéru stáva komerčne presvedčivým. Pri 1 000 používateľoch vlastný hardvér obsluhujúci model 20B pristáva na 13 – 18 $ na používateľa mesačne, konkurencieschopne s cenami API hostovanej Llamy 70B a pohodlne pod čímkoľvek zo strednej alebo frontier triedy.

> **Kľúčové posolstvo:** Vlastný on-prem je na výpočtovej položke systematicky lacnejší než prenájom (zhruba 3× pri dlhotrvajúcich nasadeniach), lebo prenájom na 36 mesiacov stojí toľko ako kúpa troch tých istých GPU. Úspory sa zúžia, keď sa zahrnie prevádzková réžia (prevádzka je rovnaká tak či tak), ale vlastníctvo je správna voľba vždy, keď máte istotu, že záťaž pretrvá počas amortizačného okna.

---

## Prenájom vs. vlastníctvo: 3-násobná medzera vo výpočtovom výkone

Priame porovnanie scenára 100 používateľov naprieč režimami robí medzeru viditeľnou.

*Tabuľka 3.10 · Prenájom vs. vlastníctvo pri 100 používateľoch, model 20B (režimy: prenájom vs. vlastníctvo)*

| Položka | Prenájom | Vlastníctvo (amortizované 36 mes.) | Pomer |
|---|---|---|---|
| Výpočtový výkon | 5 000 – 8 000 $/mes. | 1 700 – 2 400 $/mes. | ~3× |
| Infraštruktúra (sieť, kolokácia, napájanie) | v cene | 1 200 – 2 100 $/mes. | — |
| Prevádzková réžia | 5 000 – 8 000 $/mes. | 5 000 – 8 000 $/mes. | 1× |
| **Spolu** | **10 000 – 16 000 $** | **7 900 – 12 500 $** | **~1,3×** |

Tri otázky rozhodujú o tom, ktorý režim sedí danému klientovi:

1. **Ako dlho bude táto záťaž bežať?** Amortizovaný nákup je lacnejší len vtedy, ak hardvér používate aspoň 24 – 30 mesiacov. Pre piloty, overenia konceptu alebo záťaže s neistou životnosťou je prenájom správny aj za prémiové ceny.
2. **Kto nesie kapitálové riziko?** Vlastný hardvér je odpisované aktívum. Ak ceny GPU budúci rok klesnú o 30 % (tento rok klesli), váš klaster za 60 000 $ má na trhu s použitým hardvérom hodnotu 42 000 $. Prenájom nemá riziko zostatkovej hodnoty.
3. **Vyžaduje klient fyzickú kontrolu nad hardvérom?** Banky, obranní dodávatelia, utajované prostredia a niektoré nemocničné systémy majú politiky, ktoré úplne vylučujú zdieľanú cloudovú infraštruktúru, aj „vyhradený“ prenájom. Títo klienti sú v režime vlastníctva predvolene.

Pre všetko ostatné je rozhodnutie ekonomické: platiť každý mesiac o 30 % viac za flexibilitu vypnúť to, alebo zaviazať kapitál a zachytiť 3-násobnú úsporu na výpočtovom výkone.

---

## Životnosť hardvéru a ekonomika obnovy

Každý výpočet vlastného hardvéru v tejto kapitole používa 36-mesačnú amortizáciu. To je štandardná účtovná konvencia. V praxi je to aj neúplný obraz. Ak radíte klientovi pri nasadení AI na vlastnom hardvéri, dlhujete mu poctivejší pohľad na otázku životnosti hardvéru.

**Zverejnená servisná životnosť Nvidie** pre jej GPU do dátových centier je tri až päť rokov. Obe čísla sú správne podľa toho, čo tým myslíte. Tri roky sú bod, keď je GPU v typických firemných knihách odpísané na nulu a je spôsobilé na obnovu. Päť rokov je bod, keď hardvér sám typicky začína pod nepretržitou záťažou vykazovať poruchy: opotrebenie ventilátorov, degradácia teplovodivej pasty, chyby pamäte HBM stúpajúce nad prijateľné prahy.

**Inferencia je šetrnejšia než tréning.** Väčšina verejných dát o poruchách veľkých GPU flotíl pochádza z tréningových záťaží, kde GPU bežia týždne v kuse na trvalých 95 %+ využitia a boli verejne zdokumentované miery porúch niekoľkých percent na 10 000 GPU mesačne. Inferenčné záťaže sú nárazové a tepelne menej trestajúce. Skutočné miery porúch dobre chladenej inferenčnej flotily sú nižšie, ale nie nulové; rozpočtujte malú rezervu náhradných kusov (jedno GPU navyše na 8 – 10 produkčných) a proces RMA, ktorý nevyžaduje vypnutie služby.

**Účtovná životnosť, fyzická životnosť a užitočná životnosť sú tri rôzne čísla.**

- Účtovná životnosť (36 mesiacov) riadi odpisy v súvahe klienta.
- Fyzická životnosť (často 5+ rokov) riadi to, kedy hardvér naozaj zlyhá.
- Užitočná životnosť, tá, na ktorej záleží pre stratégiu, je typicky riadená technologickým zastarávaním, nie poruchami hardvéru. H100 vytláča H200, ktorú vytláča Blackwell. O 36 mesiacov budú dnešné H100 stále fungovať. Budú tiež súťažiť s hardvérom, ktorý je 2 – 3× rýchlejší pri rovnakom príkone a beží na modeloch efektívnejších na novších architektúrach. Váš klient pravdepodobne obnoví skôr, než hardvér zlyhá.

**Čo to znamená pre modelovanie TCO:**

1. **Rozpočtujte cyklus výmeny.** Nesľubujte klientovi „36 mesiacov a hardvér je zadarmo“. Sľúbte 36 mesiacov do plnej amortizácie s rozhodnutím o obnove v 30. mesiaci podľa toho, čo dovtedy dokáže novší kremík.
2. **Rezervujte náhradné kusy.** Jedno GPU navyše na rack je lacné poistenie proti lehotám RMA pri náhradách, ktoré sa pri žiadaných modeloch môžu natiahnuť na týždne.
3. **Zvážte trh s použitým hardvérom.** H100 z vyradených tréningových flotíl vstupujú od polovice roka 2025 na sekundárny trh v rastúcich objemoch, typicky za 40 – 60 % odporúčanej ceny. Pre klientov, ktorí potrebujú kapacitu, ale nie špičkový výkon, to môže znížiť capex na polovicu.
4. **Plánujte s postupnou kvantizáciou.** Ten istý GPU hardvér bude časom bežať s lepšie kvantizovanými verziami tých istých modelov, ako výskum kvantizácie postupuje. Model 20B, ktorý dnes pri INT8 potrebuje 40 GB VRAM, môže o 18 mesiacov bežať s porovnateľnou kvalitou na 20 GB pri INT4. Váš vlastný klaster rastie v efektívnej kapacite bez akejkoľvek zmeny hardvéru.

Analógia so spotrebiteľským hardvérom záleží pre kapitolu 7, kde sa rovnaká dynamika obnovy a odpisov vzťahuje na firemné notebooky s lokálnymi modelmi, ale ekonomika je stále priaznivá, lebo klient notebooky už vlastní.

---

## Zjednotené porovnanie

Teraz dáme všetko na jednu stranu: tú istú záťaž modelu 20B naprieč všetkými tromi režimami, vo všetkých štyroch rozsahoch, porovnanú s tromi úrovňami API. Toto je tabuľka, ktorú by mal mať každý poskytovateľ IT služieb na stene.

*Tabuľka 3.11 · Mesačné celkové náklady: tri režimy vs. tri úrovne API, v štyroch rozsahoch (všetky režimy)*

| Rozsah | API rozpočtová | API stredná | API frontier | Prenájom 20B | Vlastníctvo 20B |
|---|---|---|---|---|---|
| 10 používateľov | 54 $ | 600 $ | 1 800 $ | 2 500 – 4 000 $ | 1 100 – 2 000 $ |
| 100 používateľov | 540 $ | 6 000 $ | 18 000 $ | 10 000 – 16 000 $ | 7 900 – 12 500 $ |
| 500 používateľov | 2 700 $ | 30 000 $ | 90 000 $ | 11 000 – 18 000 $ | 7 800 – 12 700 $ |
| 1 000 používateľov | 5 400 $ | 60 000 $ | 180 000 $ | 18 000 – 27 000 $ | 12 900 – 18 200 $ |

*Rozpočtová úroveň: trieda Gemini Flash-Lite / GPT-4o-mini (~0,18 – 0,30 $/M zmiešane). Stredná úroveň: trieda Claude Haiku / Mistral Medium (~2,00 $/M zmiešane). Frontier: trieda Claude Sonnet / GPT-4o (~6,00 $/M zmiešane). Predpokladá 1M tokenov/používateľ/deň.*

Rovnaké dáta na používateľa. Toto je pohľad, ktorý robí štrukturálny rozdiel zjavným:

*Tabuľka 3.12 · Mesačné náklady na používateľa: tri režimy vs. tri úrovne API (všetky režimy)*

| Rozsah | API rozpočtová | API stredná | API frontier | Prenájom 20B | Vlastníctvo 20B |
|---|---|---|---|---|---|
| 10 používateľov | 5,40 $ | 60 $ | 180 $ | 250 – 400 $ | 110 – 200 $ |
| 100 používateľov | 5,40 $ | 60 $ | 180 $ | 100 – 160 $ | 79 – 125 $ |
| 500 používateľov | 5,40 $ | 60 $ | 180 $ | 22 – 36 $ | 16 – 25 $ |
| 1 000 používateľov | 5,40 $ | 60 $ | 180 $ | 18 – 27 $ | 13 – 18 $ |

Ceny API sú dokonale lineárne: náklady na používateľa sa s rozsahom nemenia. Náklady vlastného hostingu (prenájom aj vlastníctvo) s pridávaním používateľov dramaticky klesajú. Tam, kde klesajúca krivka vlastného hostingu pretína každú plochú čiaru API, je bod zlomu, a tie body zlomu sú strategickým srdcom tejto kapitoly.

*Tabuľka 3.13 · Body zlomu: kde vlastný hosting modelu 20B poráža každú úroveň API na cene (všetky režimy)*

| Porovnanie | Bod zlomu |
|---|---|
| Prenájom 20B vs rozpočtové API (Flash-Lite, 4o-mini) | **Nikdy** (prenájom je vždy drahší) |
| Vlastníctvo 20B vs rozpočtové API | **Nikdy** (podlaha prevádzkovej réžie prevyšuje rozpočtové API) |
| Prenájom 20B vs API strednej triedy (Haiku, Mistral Medium) | **~400 – 500 používateľov** |
| Vlastníctvo 20B vs API strednej triedy | **~250 – 350 používateľov** |
| Prenájom 20B vs frontier API (Sonnet, GPT-4o) | **~100 – 200 používateľov** |
| Vlastníctvo 20B vs frontier API | **~50 – 100 používateľov** |
| Prenájom 20B vs prémiové API (Opus, GPT-4.1 + ťažké používanie) | **~50 – 80 používateľov** |
| Vlastníctvo 20B vs prémiové API | **~30 – 50 používateľov** |

Vlastníctvo hardvéru posúva každý bod zlomu skôr faktorom zhruba 1,5 – 2× v porovnaní s prenájmom. Pre klienta zaviazaného k záťaži je to rozdiel medzi životaschopnosťou vlastného hostingu pri 150 používateľoch namiesto 300.

**Čítajte túto tabuľku s jednou kritickou výhradou: porovnáva ceny tokenov, nie schopnosti.** Riadky stavajúce vlastne hostovaný model 20B proti frontier a prémiovým úrovniam API neznamenajú, že model 20B s otvorenými váhami *je* Claude Sonnet alebo Opus; nie je, a vaši používatelia si to všimnú pri zložitom uvažovaní, analýze dlhých dokumentov a náročných úlohách programovania (bod o zhode modelu z kapitoly 2 a diskusia o medzere v kvalite z kapitoly 7 platia v plnom rozsahu). Bod zlomu má zmysel len tam, kde je menší model pre záťaž naozaj primeraný. Prvé dva riadky sú poctivé porovnanie rovnakého s rovnakým a tam vlastný hosting na cene nikdy nevyhráva. Každý ďalší riadok odpovedá na inú a praktickejšiu otázku: „ak model 20B túto prácu zvládne, pri akom rozsahu porazí jeho vlastná prevádzka platenie frontier cien?“

Pod každým riadkom sedí ešte jedna sila: cyklus capexu. Súčasné ceny API sú ceny na obsadenie trhu, financované najväčšou výstavbou infraštruktúry v histórii výpočtovej techniky (kapitola 4 vysvetľuje mechaniku). Z toho vyplývajú dve budúcnosti. Ak výstavba udrží tempo, dotované ceny API pretrvajú a body zlomu ostanú zhruba tam, kam ich kladie táto tabuľka. Ak sa zlomí, tak ako sa v roku 2001 zlomila predimenzovaná optika, trh zaplavia GPU z druhej ruky, sadzby prenájmu klesnú a každý bod zlomu sa posunie doľava, k vlastnému hostingu pri menších rozsahoch. Či vydrží, sa zvnútra tejto tabuľky nedá zistiť; [dekodér capexu](/scenario-planning-sk/#decoder) v sprievodnej brožúre Plánovanie scenárov je nástroj postavený presne na sledovanie tohto.

---

## Čo tieto čísla nezachytávajú

Kým vyvodíme z tabuliek vyššie strategické závery, výhrady.

**Faktory v prospech API:**

- Nulový čas nastavenia: môžete byť naživo za hodiny, nie týždne
- Automatické upgrady modelov: keď sa frontier model zlepší, dostanete ho zadarmo
- Elastické škálovanie: cez víkendy a sviatky neplatíte nič
- Žiadne riziko obstarávania GPU: nikdy nevlastníte odpisovaný hardvér
- Žiadna expozícia voči poruchám: hyperškálová firma vymieňa GPU transparentne

**Faktory v prospech prenájmu:**

- Plná kontrola nad stackom bez kapitálového záväzku
- Dátová suverenita v rozsahu, aký dovoľuje zmluva o spracovaní údajov poskytovateľa
- Možnosť spúšťať modely s otvorenými váhami alebo doladené modely, ktoré hyperškálové firmy neponúkajú
- Predvídateľné mesačné náklady, žiadne prekvapivé účty z prompt injection alebo utrhnutého agenta
- Nezávislosť od zastarania modelov alebo zmien podmienok API

**Faktory v prospech vlastného on-prem:**

- Skutočná dátová suverenita: tokeny nikdy neopustia váš perimeter
- Súlad s najprísnejšími regulačnými požiadavkami EÚ pre regulované odvetvia
- Plná kontrola nad hardvérom vrátane nasadení odpojených od siete
- Nižšie dlhodobé náklady na výpočtový výkon (3× na výpočtovej položke)
- Neobmedzené používanie za fixné náklady: žiadny tlak za token na prijatie
- Predvídateľný cyklus obnovy, ktorý riadite vy

Pre poskytovateľov IT služieb v EÚ sú argumenty dátovej suverenity a súladu často najsilnejším odôvodnením vlastného on-prem. Samotná nákladová matematika málokedy podporí prenájom pred API pre klientov otvorených cloudu, ale skombinujte náklady so skutočnou požiadavkou na súlad a vlastný on-prem začne vyzerať ako správna odpoveď pre zmysluplný podiel trhu.

Na túto stranu patrí aj jedna regulačná výhrada. Podľa AI Actu EÚ závisia povinnosti viazané na AI systém od vašej roly a vlastný hosting môže tú rolu posunúť. Klient, ktorý iba konzumuje komerčné API, je typicky nasadzujúci subjekt; klient (alebo poskytovateľ konajúci za neho), ktorý doladí alebo podstatne upraví model s otvorenými váhami, môže prekročiť do územia poskytovateľa, s oveľa ťažším bremenom dokumentácie a posudzovania zhody. Ten náklad sa nikdy neobjaví na faktúre za GPU. Kapitola 11 prechádza čiaru poskytovateľ/nasadzujúci subjekt podrobne; skontrolujte, na ktorú stranu vás vaša architektúra kladie, kým sa zaviažete k číslam vyššie.

> **Kľúčové posolstvo:** Nestavajte svoj biznisový prípad na úsporách nákladov z vlastného hostingu oproti API. Pre klientov otvorených cloudu ten argument prehráte. Stavajte prípad na dátovej suverenite, regulačnom súlade a prispôsobení. Použite tieto čísla na to, aby ste presne vedeli, akú prémiu klienta žiadate zaplatiť a prečo za to tá prémia stojí.

---

## Ekonomika on-prem: úplne iné porovnanie

Všetko vyššie porovnáva tri režimy medzi sebou a s cenami API. To je správne rámcovanie pre klientov, ktorí majú na výber. Pre významný segment podnikového trhu EÚ (bankovníctvo, zdravotníctvo, obrana, právo, verejný sektor a každá organizácia, ktorej tím pre súlad alebo právny tím vylúčil externé AI API) sú ceny API irelevantné, lebo to nie je možnosť, ktorú si môžu vybrať.

Pre týchto klientov je porovnanie, na ktorom záleží, iné:

- **Vaša spravovaná vlastná on-prem služba** vs. **klient, ktorý si ju postaví a prevádzkuje sám**
- **Vaša spravovaná vlastná on-prem služba** vs. **klient bez akejkoľvek AI**

To je tradičná ekonomika spravovaných IT služieb a čísla vyzerajú oveľa priaznivejšie.

### Čo klienta stojí urobiť si to sám

Zvážte stredne veľkú európsku banku, ktorá chce prevádzkovať model 20B on-prem pre 100 interných používateľov. Ak si banka infraštruktúru postaví a spravuje sama, tu je účet, ktorému čelí.

*Tabuľka 3.14 · Náklady klienta na vlastné riešenie: model 20B on-prem, 100 používateľov, ročne (režim: vlastníctvo, prevádzkuje klient)*

| Nákladová zložka | Ročné náklady |
|---|---|
| GPU hardvér (2× H100, amortizované na 3 roky) | 17 000 – 23 000 $ |
| Serverová infraštruktúra, sieť, chladenie | 8 000 – 12 000 $ |
| ML inžinier (1 FTE, trh EÚ) | 80 000 – 130 000 $ |
| DevOps/infraštruktúrny inžinier (0,5 FTE) | 30 000 – 50 000 $ |
| Softvérové licencie, monitorovanie, bezpečnostné nástroje | 10 000 – 20 000 $ |
| Školenia a zvyšovanie kvalifikácie | 5 000 – 10 000 $ |
| **Celkové ročné náklady (klient sám)** | **150 000 – 245 000 $** |
| **Mesačný ekvivalent** | **12 500 – 20 400 $** |
| **Na používateľa mesačne** | **125 – 204 $** |

Dominantným nákladom sú ľudia, nie hardvér. ML inžinier, ktorý vie nasadiť, optimalizovať a udržiavať inferenčnú infraštruktúru LLM, si na trhu EÚ pýta významný plat a klient potrebuje aspoň jedného na plný úväzok. Mnohí budú potrebovať viac, najmä počas fázy prvotného nastavenia.

Všimnite si medzeru oproti číslu 79 – 125 $ na používateľa z tabuľky 3.8. Rovnaký hardvér, rovnaký model, rovnaký rozsah, ale 79 – 125 $, keď to prevádzkujete vy (poskytovateľ IT služieb), a 125 – 204 $, keď to klient prevádzkuje sám. Tá medzera je vaša maržová príležitosť a je štrukturálna.

### Čo si môžete účtovať ako spravovanú službu

Ako poskytovateľ IT služieb máte výhody, ktoré jednotlivý klient nemá:

- **Zdieľaná odbornosť.** Váš ML inžinier obsluhuje viacerých klientov, nie jedného. Náklady sa rozložia na vašu zákaznícku základňu.
- **Znovupoužiteľné nástroje.** Vaše nasadzovacie pipeline, monitorovacie dashboardy a procesy aktualizácií sa postavia raz a použijú pre každého klienta.
- **Prevádzková zrelosť.** Infraštruktúru spravujete desaťročia. Klientom čerstvo najatý ML inžinier na to prichádza po prvý raz.
- **Vzťahy s dodávateľmi.** Vyjednávate obstarávanie GPU a cloudové ceny vo veľkom.

Tieto výhody vám dovolia dodať tú istú službu za nižšie náklady, než klient dosiahne sám: tá istá ekonomika, ktorá robila tradičné spravované IT služby ziskovými.

*Tabuľka 3.15 · Ceny spravovanej služby vs. náklady klienta na vlastné riešenie (režim: vlastníctvo/prenájom, prevádzkuje poskytovateľ)*

| Rozsah nasadenia | Vaše náklady | Účtujete | Náklady klienta sám | Vaša marža |
|---|---|---|---|---|
| 10 používateľov (vyhradené) | 2 500 – 4 000 $/mes. | 5 000 – 8 000 $/mes. | 7 000 – 12 000 $/mes. | 40 – 55 % |
| 100 používateľov (zdieľaná infra) | 10 000 – 16 000 $/mes. | 14 000 – 22 000 $/mes. | 12 500 – 20 400 $/mes. | 30 – 45 % |
| 500 používateľov (platforma) | 11 000 – 18 000 $/mes. | 22 000 – 35 000 $/mes. | 20 000 – 35 000 $/mes. | 45 – 55 % |

*Stĺpec „Vaše náklady“ používa ceny režimu prenájmu z tabuľky 3.6. Ak prevádzkujete vlastný hardvér, vaše náklady ďalej klesnú (tabuľka 3.9) a marže sa zodpovedajúco zlepšia.*

Pri 10 používateľoch je ekonomika obzvlášť presvedčivá. Malý klient nezdôvodní ML inžiniera na plný úväzok pre 10 používateľov, ale stále potrebuje niekoho, kto infraštruktúru spravuje. Váš model zdieľanej odbornosti mu dáva prevádzku AI podnikovej triedy za zlomok ceny toho, keby to robil sám.

Pri 100 používateľoch vaša cena sedí uprostred klientovho rozsahu na vlastné riešenie, niekedy mierne nad ním. To je v poriadku a mali by ste to otvorene obhajovať: klient, ktorý platí vám, sa vyhne riziku náboru v ML, dostane SLA namiesto jediného bodu zlyhania a je naživo za týždne namiesto kvartálov. To, čo kupuje, je odstránenie schopnosti, ktorú by mal problém vybudovať a udržať, nie lacnejší výpočtový výkon. Ak nákupný tím trvá na porovnaní riadok po riadku s číslom vlastného riešenia, ukotvite sa na trhu s náborom ML inžinierov, nie na hardvéri.

Pri 500+ používateľoch začína mať klient dosť rozsahu na zdôvodnenie vlastného tímu, ale aj vtedy môže váš platformový prístup (obsluha viacerých klientov na zdieľanej infraštruktúre s izolovanými dátami) ostať nákladovo konkurencieschopný.

> **Kľúčové posolstvo:** Pre klientov vyžadujúcich on-prem je vašou konkurenciou klientov interný IT tím, nie OpenAI alebo Google. A interné IT tímy porážate tak ako vždy: prevádzkovou špecializáciou, zdieľanými nákladmi naprieč viacerými klientmi a zrelými nástrojmi. Maržová štruktúra vyzerá ako tradičné spravované služby (40 – 55 % vo väčšine rozsahov), nie ako žiletkovo tenké marže z pokusu súťažiť s cenami API hyperškálových firiem.

### Otázka veľkosti trhu

Aký veľký je on-prem segment? Žiadne publikované dáta na to špecificky pre GenAI presne neodpovedajú, ale viaceré ukazovatele naznačujú, že na trhu EÚ je podstatný:

- **Bankovníctvo a finančné služby:** ECB a národní regulátori čoraz viac skúmajú riziko koncentrácie v cloude. Mnohé banky v EÚ udržiavajú prísne politiky vyžadujúce spracovanie citlivých dát on-prem alebo v súkromnom cloude.
- **Zdravotníctvo:** Dáta pacientov pod GDPR majú prísne požiadavky na spracovanie. Mnohé zdravotnícke systémy v EÚ majú výslovné politiky proti externým AI API pre klinické dáta.
- **Verejný sektor:** Vládne organizácie naprieč členskými štátmi EÚ často vyžadujú pre citlivé záťaže nasadenie on-prem alebo v suverénnom cloude.
- **Právo:** Advokátske tajomstvo a profesijná povinnosť mlčanlivosti vytvárajú silné motivácie pre on-prem AI.
- **Obrana a kritická infraštruktúra:** Tieto sektory z definície vyžadujú kontrolované prostredia.

Pre typického poskytovateľa IT služieb v EÚ, ktorého klientska základňa sa kloní k regulovaným odvetviam, môže on-prem segment predstavovať 30 – 60 % potenciálnych tržieb z AI služieb. Zďaleka nie nika, môže to byť jadro trhu.

### Spojený obraz

Realitou pre väčšinu poskytovateľov IT služieb v EÚ je, že budú obsluhovať oba segmenty súčasne.

*Tabuľka 3.16 · Spojený obraz: roly, modely tržieb a marže podľa segmentu klientov*

| Segment klientov | Vaša rola | Model tržieb | Marža |
|---|---|---|---|
| Vyžadujúci on-prem | Poskytovateľ spravovanej AI infraštruktúry | Mesačný paušál + poplatky za používateľa | 40 – 55 % |
| Otvorení cloudu | Integrátor AI riešení | Projektové poplatky + prefakturácia API + podpora | 25 – 40 % |
| Oba | Vrstva súladu a hodnotenia | Poplatky za posúdenie + paušál za monitorovanie | 50 – 65 % |

Najzdravší biznis kombinuje všetky tri: marže z infraštruktúry od on-prem klientov, tržby z integrácie a poradenstva od klientov otvorených cloudu a služby súladu navrstvené naprieč oboma. Nerobte chybu, že sa sústredíte výlučne na jeden segment, keď ten druhý môže byť rovnako alebo viac lukratívny.

---

## Praktické dôsledky pre vašu cenovú stratégiu

Tieto čísla vedú k štyrom okamžitým záverom o tom, ako by ste mali premýšľať o cenách:

**1. Nesnažte sa podbiehať poskytovateľov API na cene.** Prehráte. OpenAI, Google a Anthropic míňajú miliardy na vlastný kremík a infraštruktúru. Vaše náklady na token budú pri ekvivalentnej kvalite modelu vždy vyššie než ich.

**2. Pre on-prem klientov naceňujte oproti klientovým nákladom na vlastné riešenie, nie oproti cenám API.** Spravovaná AI infraštruktúrna služba za 180 $ na používateľa mesačne je drahá v porovnaní s volaním API za 5,40 $ na používateľa mesačne, ale je to výhodná kúpa v porovnaní so 125 – 204 $ na používateľa mesačne, ktoré by klienta stálo postaviť a obsadiť ju sám. Rámcujte svoje ceny voči správnemu benchmarku.

**3. Naceňujte podľa hodnoty, nie nákladov plus prirážky.** Ak vaša služba poskytuje dátovú suverenitu, uistenie o súlade alebo špecializované dolaďovanie, naceňte tie výsledky priamo. Služba za 180 $/používateľ/mesiac, ktorá udrží dáta pacientov on-prem, je iný produkt než volanie API za 5,40 $/používateľ/mesiac, ktoré posiela dáta na americké servery.

**4. Zvážte hybridné architektúry.** Smerujte citlivé dopyty cez vlastnú infraštruktúru a necitlivé cez lacné API. To drží využitie vašich GPU vysoké na práci, ktorá naozaj vyžaduje súkromie, a náklady nízke na všetkom ostatnom. Tento model podrobne skúmame v kapitole 6 a kapitola 7 rozširuje logiku ďalej na lokálnu inferenciu na zariadení, ktorá pri záťažiach, ktoré sa zmestia, produkuje výpočtové náklady doslova nulové.

Čísla rozprávajú dva príbehy. Pre klientov otvorených cloudu je stratégia o dodávaní odbornosti, integrácie a súladu nad ich API, nie o lacnejšej prevádzke modelov než hyperškálové firmy. Pre klientov vyžadujúcich on-prem ste stále v infraštruktúrnom biznise a ekonomika hrá vo váš prospech, pokiaľ naceňujete voči správnemu porovnaniu a zaviažete sa k amortizačnému oknu, ktoré robí vlastný hardvér životaschopným.

---

> **Strážca čerstvosti** · *overené apríl 2026 · odhadovaný polčas rozpadu: ~4 mesiace*
>
> Táto kapitola obsahuje časovo najcitlivejšie čísla brožúry. Tvrdenia, ktoré sa najpravdepodobnejšie posunú do 3 – 6 mesiacov:
>
> - **Tabuľka cien API**: každý uvedený poskytovateľ mení ceny aspoň raz za kvartál a celkový trend je klesajúci. Pred citovaním klientovi znovu overte ceny Gemini Flash-Lite, GPT-4o-mini, Claude Haiku a Llama 70B.
> - **Sadzby prenájmu GPU**: spotové trhy hyperškálových firiem a neocloudov sa hýbu mesačne. Ceny H100 konkrétne klesajú o 2 – 4 % mesačne.
> - **Pomenované verzie modelov** (GPT-4.1, Claude Sonnet 4.6, Gemini Flash-Lite, Llama 3.1 70B): nové vydania typicky vychádzajú každé 2 – 4 mesiace a môžu tieto položky premenovať, preceniť alebo nahradiť.
> - **Body zlomu** vyplývajú priamo z cenových tabuliek; hýbu sa vždy, keď sa pohne ktorákoľvek strana.
>
> Čo by malo vydržať dlhšie: rámcovanie tromi režimami, medzera prenájom vs. vlastníctvo (~3× na výpočtovom výkone), tvar krivky rozsahu (vlastníctvo poráža prenájom, ktorý poráža API pri rôznych počtoch používateľov) a ekonomika on-prem trhu. Ak toto čítate viac než šesť mesiacov po dátume vyššie, berte každé konkrétne číslo v dolároch ako smerové, ale štrukturálny argument by mal stále platiť.

---

*Kapitola 4 skúma, prečo strana API v porovnaní nie je lacnejšia iba dnes, ale štrukturálne, a čo to znamená pre akúkoľvek stratégiu postavenú na súťažení s hyperškálovými firmami na cene.*
