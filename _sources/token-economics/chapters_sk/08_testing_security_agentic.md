# Kapitola 8: Biznis model: testovanie, bezpečnosť a agentná infraštruktúra

> **V skratke**
>
> - Tri línie služieb okolo modelu, nie v ňom: testovanie a validácia (najvyššia marža, najvzácnejšie talenty), bezpečnosť GenAI (rozširuje vašu bezpečnostnú prax) a agentná infraštruktúra (najrýchlejšia cesta k tržbám).
> - AI Act EÚ robí z dopytu po testovaní povinnosť: posudzovanie zhody za 20 – 50 tis. $ na systém plus 3 – 10 tis. $ mesačne za monitorovanie, opakovane zo zákona.
> - Model je len volanie API. MCP servery, RAG pipeline, integrácie nástrojov a mantinely sú integračná práca, ktorú robíte desaťročia, v novom protokole.
> - Na poradí záleží: začnite agentnou infraštruktúrou, súbežne budujte odbornosť v testovaní a bezpečnosti, správu viacerých modelov nechajte vzísť zo skúseností.
>
> **Číslo, ktoré si zapamätať:** 3 – 6 mesiacov, kým vaši existujúci integrační inžinieri dosiahnu prvú platenú agentnú zákazku.

Predchádzajúce dve kapitoly skúmali biznis modely postavené okolo jednej jadrovej schopnosti: proxy pre súkromie v kapitole 6, lokálne nasadenie modelov v kapitole 7. Táto kapitola pokrýva tri súvisiace príležitosti, ktoré zdieľajú dôležitú charakteristiku: vynárajú sa ako samostatné kategórie služieb, ktoré podniky budú potrebovať, ale nedokážu si ich ľahko postaviť interne.

Testovanie a validácia, bezpečnosť špecifická pre GenAI a agentná infraštruktúra predstavujú každá vysokomaržovú prácu pre poskytovateľov, ktorí včas investujú do správnych zručností. Pokrývajú široké rozpätie náročnosti, času k tržbám a súladu s existujúcimi schopnosťami IT služieb. Spoločnou niťou je, že žiadna nie je o prevádzkovaní modelov, ale o všetkom, čo model obklopuje: o hodnotení, ochrane a inštalatérčine, vďaka ktorej AI systémy fungujú v produkcii.

---

## Testovanie a validácia

AI Act EÚ nadobudol účinnosť v auguste 2024, povinnosti nabiehajú postupne do roku 2027. Pre poskytovateľov IT služieb je komerčne najvýznamnejšou požiadavkou posudzovanie zhody vysokorizikových AI systémov a priebežné monitorovanie, ktoré po ňom nasleduje.

### Čo regulácia vyžaduje

Vysokorizikové AI systémy musia pred nasadením prejsť posudzovaním zhody, ktoré hodnotí presnosť, robustnosť, kybernetickú bezpečnosť, transparentnosť, ľudský dohľad a nediskrimináciu. Nejde o jednorazové udalosti. Akt vyžaduje priebežné monitorovanie: detekciu driftu, identifikáciu vynárajúcich sa zaujatostí a dokumentovanie všetkého.

Nie je to cvičenie na odškrtnutie. Testovanie distribučnej zaujatosti naprieč chránenými charakteristikami, hodnotenie robustnosti voči adverzariálnym vstupom a meranie kalibrácie v reálnych podmienkach ide ďaleko za to, čo väčšina podnikov dokáže personálne pokryť interne.

### Ekonomika

| Služba | Cenové rozpätie | Frekvencia |
|---|---|---|
| Úvodné posúdenie zhody | 20 000 – 50 000 $ na systém | Jednorazovo (na nasadenie) |
| Priebežné monitorovanie a hodnotenie | 3 000 – 10 000 $/mesiac na systém | Priebežne |

Poskytovateľ s 20 klientmi, z ktorých každý prevádzkuje dva až tri vysokorizikové AI systémy, generuje 120 000 až 300 000 $ na úvodných posúdeniach a 1,4 až 7,2 milióna $ ročne na priebežnom monitorovaní. Marže sú vysoké: primárnym nákladom je kvalifikovaná práca, nie infraštruktúra.

### Problém s talentmi

Toto nie je tradičná práca IT prevádzky. Poriadne testovanie AI vyžaduje ľudí, ktorí rozumejú metodike hodnotenia ML, nielen „spustiť testovaciu sadu“, ale štatistickému uvažovaniu, prečo sú niektoré prístupy platné a iné zavádzajúce. Potrebujete ľudí, ktorí vedia navrhnúť adverzariálne testovacie prípady, určiť, či 2 % rozdiel v presnosti medzi demografickými skupinami je šum alebo systematická zaujatosť, a zorientovať sa v tom, že rôzne definície férovosti sa často navzájom vylučujú.

To sú výskumné a inžinierske talenty. Títo ľudia sú vzácni, drahí a momentálne zamestnaní v AI laboratóriách, na univerzitách a v hŕstke firiem s vyhradenými tímami pre bezpečnosť AI. Ich nábor vyžaduje presvedčivú ponuku: zaujímavú prácu, konkurencieschopné odmeňovanie a skutočný záväzok budovať prax.

> **Kľúčová ekonomika:** Testovanie a validácia ponúkajú najvyššie marže a najvyššie bariéry z troch príležitostí v tejto kapitole. Rozpočtujte 12 – 18 mesiacov od úvodnej investície po zmysluplné tržby. Regulačný dopyt je istý; AI Act EÚ je zákon. Otázka je, či dokážete tím vybudovať dosť rýchlo, aby ste ho zachytili.

---

## Bezpečnosť špecifická pre GenAI

Ak dnes prevádzkujete bezpečnostnú prax, máte náskok, ale menší, než by ste si mysleli. Bezpečnosť GenAI je samostatná disciplína. Plocha hrozieb je iná, vektory útokov sú nové a obranné nástroje ešte dozrievajú.

### Krajina hrozieb

Systémy GenAI sú zraniteľné voči tradičným bezpečnostným hrozbám plus sade, ktorá nemá priamu obdobu v konvenčnom IT:

**Prompt injection**: útočník vytvorí vstup, ktorý spôsobí, že model ignoruje svoje inštrukcie a nasleduje útočníkove. To je štrukturálna vlastnosť toho, ako jazykové modely spracúvajú inštrukcie a dáta v tom istom kanáli. Obrany existujú, ale žiadna nie je úplná.

**Únik dát cez výstupy**: model neúmyselne odhalí tréningové dáta, kontext RAG alebo systémové prompty vo svojich odpovediach. Starostlivo skonštruované dopyty môžu model prinútiť vytiahnuť interné dokumenty, dôverné inštrukcie alebo vzory z dát na dolaďovanie.

**Otrávenie modelu cez dolaďovanie**: dáta na dolaďovanie zavedú škodlivé správanie. Otrávený model sa môže na väčšine vstupov správať normálne, ale v scenároch zvolených útočníkom produkovať jemne nesprávne výstupy. Detekcia vyžaduje hodnotenie nad rámec štandardných metrík presnosti.

**Riziká dodávateľského reťazca pri open-source váhach**: AI ekvivalent zraniteľností závislostí. Keď stiahnete model z Hugging Face, dôverujete, že s váhami nikto nemanipuloval a tréningové dáta neboli otrávené. Open-source AI ekosystému chýba zrelosť nástrojov ako npm audit alebo Dependabot.

**Jailbreaking**: obchádzanie bezpečnostných mantinelov na produkovanie škodlivých výstupov alebo výstupov porušujúcich politiky. Nové techniky sa objavujú rýchlejšie, než ich poskytovatelia stíhajú plátať.

### Bezpečnostné audity a red-teaming

Bezpečnostný audit nasadenia GenAI pokrýva odolnosť voči prompt injection, testovanie úniku dát, riadenie prístupu, primeranosť logovania a súlad s politikami. Audit strednej zložitosti stojí 15 000 až 40 000 $.

Red-teaming je intenzívnejší: vyhradený tím trávi dni alebo týždne pokusmi systém prelomiť cez adverzariálne vstupy, extrakčné útoky a zneužitie schopností používania nástrojov. Red-teamingové zákazky stoja 30 000 až 80 000 $ a v regulovaných odvetviach sa čoraz viac očakávajú.

### Prenos zručností

Vaši existujúci bezpečnostní inžinieri rozumejú modelovaniu hrozieb, plochám útokov a obrane do hĺbky. Ten základ sa prenáša. Neprenáša sa špecifická znalosť toho, ako jazykové modely zlyhávajú: mechanika prompt injection, štatistické metódy detekcie úniku dát, hodnotiace rámce pre robustnosť modelov.

Očakávajte nábeh šesť až dvanásť mesiacov. Je to rýchlejšie než budovať testovanie od nuly, lebo bezpečnostné myslenie (myslieť ako útočník, predpokladať zraniteľnosť, overovať namiesto dôvery) je už prítomné. Doménová znalosť sa navrství naň.

> **Kľúčové posolstvo:** Bezpečnosť GenAI je prirodzeným rozšírením existujúcich bezpečnostných praxí, ale vyžaduje značné nové technické znalosti. Plocha hrozieb je skutočne iná a nástroje sú stále nezrelé. Poskytovatelia, ktorí teraz investujú do zvyšovania kvalifikácie svojich bezpečnostných tímov, budú vlastniť trh, od ktorého bude musieť nakupovať každý podnik nasadzujúci AI.

---

## Agentná infraštruktúra ako služba

Z troch príležitostí je agentná infraštruktúra pre poskytovateľov IT služieb najprístupnejšia a s najväčšou pravdepodobnosťou vygeneruje tržby už v prvom roku.

### Posun k agentnej AI

Podniková GenAI sa posúva za jednoduché interakcie prompt – odpoveď smerom k používaniu nástrojov, viackrokovým pracovným postupom, autonómnym agentom a orchestračným vrstvám. Samotný model (Claude, GPT-4.1, Gemini alebo open-source) je len jedna zložka. Čoraz viac je najmenej diferencovanou zložkou.

Hodnota je vo všetkom okolo modelu:

**MCP servery** (Model Context Protocol) poskytujú štandardizované rozhrania medzi AI modelmi a externými zdrojmi dát, nástrojmi a službami. Stavba a údržba MCP serverov pre podnikové prostredia (pripojenie modelov k databázam, úložiskám dokumentov, ticketovacím systémom, CRM platformám) je integračná práca, ktorú poskytovatelia IT služieb robia desaťročia, v novom protokole.

**RAG pipeline** vyžadujú ingestovanie dokumentov, stratégie delenia na kúsky, výber embedding modelu, správu vektorovej databázy a priebežné hodnotenie kvality vyhľadávania. RAG pipeline, ktorá funguje v deme, a taká, ktorá spoľahlivo funguje v produkcii s miliónmi dokumentov, sú úplne odlišné inžinierske výzvy.

**Integrácie nástrojov** dávajú agentom schopnosť konať: vytvárať tickety, dopytovať databázy, aktualizovať záznamy, spúšťať pracovné postupy. Každá integrácia vyžaduje autentifikáciu, správu chýb, obmedzovanie rýchlosti, auditné logovanie a mantinely brániace neoprávneným akciám.

**Orchestrácia pracovných postupov** koordinuje viacero agentov, nástrojov a zdrojov dát do viackrokových procesov. Agent zákazníckeho servisu, ktorý vyhľadá objednávku, skontroluje sklad, iniciuje vrátenie, aktualizuje CRM a pošle potvrdenie, je choreografovaná sekvencia použití nástrojov, podmienenej logiky a kontrolných bodov s človekom v slučke.

**Mantinely** (filtrovanie vstupov a výstupov, obsahové politiky, limity používania a bezpečnostné hranice) sú základná infraštruktúra, ktorú potrebuje každé podnikové nasadenie.

### Prečo sa to mapuje na existujúce zručnosti

MCP servery sú API integrácie. RAG pipeline sú dátové inžinierstvo. Integrácie nástrojov sú systémová integrácia. Orchestrácia pracovných postupov je automatizácia biznis procesov. Mantinely sú vynucovanie politík. Konkrétne technológie sú nové (embedding modely a vektorové databázy namiesto ETL a relačných databáz), ale podkladové disciplíny sú tie isté. Váš tím, ktorý prepája Salesforce so SAP, sa môže naučiť prepojiť Claude s úložiskom dokumentov vášho klienta.

Model je len volanie API. Vaša hodnota je inštalatérčina.

### Ekonomika

| Fáza | Tržby | Trvanie |
|---|---|---|
| Discovery a architektúra | 15 000 – 40 000 $ | 2 – 4 týždne |
| Stavba a nasadenie | 50 000 – 200 000 $ | 2 – 4 mesiace |
| Priebežná správa a optimalizácia | 5 000 – 20 000 $/mesiac | Priebežne |

Priebežná správa je tam, kde žijú opakované tržby. RAG pipeline potrebujú ladenie, ako sa menia korpusy dokumentov. Integrácie nástrojov potrebujú údržbu, ako sa vyvíjajú API. Mantinely potrebujú aktualizácie, ako sa objavujú nové hrozby. Toto je práca spravovaných služieb pri vyšších maržiach než tradičné monitorovanie infraštruktúry, lebo zručnosti sú špecializovanejšie.

> **Kľúčové posolstvo:** Agentná infraštruktúra je pre poskytovateľov IT služieb najprirodzenejším prechodom. Model je len volanie API; vaša hodnota je v MCP serveroch, RAG pipeline, integráciách nástrojov, orchestrácii pracovných postupov a mantineloch, ktoré ho robia užitočným. To sa priamo mapuje na integračné a automatizačné zručnosti, ktoré už máte.

---

## Prevádzka agentov: dohľad ako služba

Postaviť agentnú inštalatérčinu je projekt. Prevádzkovať agentov je služba a je to časť, o ktorej väčšina klientov nepremýšľala, kým ich prvý agent neurobil niečo drahé.

Agenti konajú. Vytvárajú tickety, aktualizujú záznamy, posielajú správy, spúšťajú pracovné postupy. Každá z tých akcií potrebuje ľudskú odpoveď na tri otázky: kto schvaľuje tie rizikové pred vykonaním, komu zazvoní telefón, keď agent vybočí zo scenára, a kto potom preskúma audítorskú stopu. Pri vysokorizikových systémoch to nie je voliteľná hygiena: článok 14 AI Actu EÚ vyžaduje účinný ľudský dohľad kvalifikovaným personálom a línia služieb 5 v kapitole 11 pokrýva návrh týchto mechanizmov. Niekto ich musí aj personálne obsadiť.

Väčšina klientov nemôže. Stredne veľký podnik prevádzkujúci tucet agentných pracovných postupov potrebuje funkciu dohľadu, ktorá sleduje schvaľovacie fronty, rieši eskalácie do minút a denne kontroluje logy zásahov, nonstop, ak agenti bežia nonstop. To nie je popis práce, na ktorý sa dá nabrať; je to pult. A pult s pokrytím 24/7, eskalačnými procedúrami a disciplínou zmien je presne to, čo už prevádzkujete. AgentOps pult je prevádzkový sval NOC namierený na flotily agentov namiesto infraštruktúrnych alertov: rovnaké rozpisy, rovnaké runbooky, nové režimy zlyhania.

Služba má prirodzený tvar paušálu: mesačný poplatok za pracovný postup alebo za flotilu agentov, pokrývajúci personál pre schvaľovaciu frontu, reakciu na eskalácie, týždenné revízie zásahov a dokumentáciu dohľadu, ktorú tím klienta pre súlad zakladá. Správny návrh odovzdávania medzi človekom a AI je rovnako dôležitý ako jeho personálne obsadenie; vzorce (čo agenti eskalujú, kedy ľudia zasahujú, ako schválenia plynú bez toho, aby sa stali gumovými pečiatkami) sú predmetom sprievodnej brožúry [Vzory interakcie LLM a človeka pre prevádzku](/llm-human-interaction-patterns-sk/), ktorá sa s touto líniou služieb priamo páruje.

Strategická príťažlivosť: toto je najlepkavejšia ponuka v kapitole. Testovacie zákazky končia, audity končia, ale dohľad beží tak dlho ako agenti. Poskytovateľ, ktorý personálne obsadzuje klientov pult dohľadu, drží rovnakú pozíciu, akú v starom svete držal poskytovateľ NOC, tentoraz s regulačnou požiadavkou pod sebou.

---

## Správa viacerých modelov

Žiadny seriózny podnik nebude prevádzkovať jediný model pre všetky prípady použitia. Vynárajúci sa vzorec:

- **Frontier API modely** (Claude, GPT-4.1, Gemini) pre zložité uvažovanie a interakcie so zákazníkmi
- **Menšie API modely** (Claude Haiku, GPT-4o mini) pre vysokoobjemové, menej zložité úlohy
- **Lokálne nasadené open-source modely** pre citlivé dáta, ktoré nemôžu opustiť organizáciu
- **Doladené modely** pre doménovo špecifické úlohy: medicínska terminológia, právna analýza, odvetvová klasifikácia

Každý model má iné schopnosti, náklady, latenciu, záruky zaobchádzania s dátami a cykly aktualizácií. Spravovať túto zložitosť naprieč desiatkami aplikácií poháňaných AI je významná prevádzková výzva.

### Analógia s multi-cloudom

Je to štrukturálne podobné správe multi-cloudu, trhu, ktorý živí životaschopné biznisy vyše desaťročia. Služby zahŕňajú:

**Správu životného cyklu modelov**: sledovanie nasadení, správu aktualizácií verzií, koordináciu migrácií, keď poskytovatelia ukončia podporu modelov.

**Hodnotenie a testovanie**: keď poskytovateľ vydá novú verziu modelu, niekto musí vyhodnotiť, či na konkrétnych prípadoch použitia organizácie funguje lepšie alebo horšie. To vyžaduje systematické A/B testovanie, regresné hodnotenie a benchmarkovanie voči skutočným záťažiam.

**Optimalizáciu nákladov**: smerovanie požiadaviek na nákladovo najefektívnejší model, ktorý spĺňa požiadavky na kvalitu. Inteligentné smerovanie môže znížiť náklady o 30 – 50 % bez degradácie kvality.

**Zjednotenú pozorovateľnosť**: konzistentné logovanie, monitorovanie a alertovanie naprieč všetkými modelmi. Keď model produkuje degradované výstupy, potrebujete to detegovať bez ohľadu na poskytovateľa.

Správa viacerých modelov je spojivové tkanivo, ktoré viaže dokopy agentnú infraštruktúru, testovanie a bezpečnosť. Ako správa multi-cloudu, aj toto je daň zo zložitosti, ktorú podniky niekomu zaplatia za spravovanie.

---

## Realita talentov

Tieto príležitosti pokrývajú široké rozpätie požiadaviek na talenty a poctivosť je pre plánovanie kľúčová.

**Testovanie a validácia** vyžadujú najvzácnejšie talenty: odbornosť v hodnotení ML, štatistickú prísnosť a výskumné myslenie. Ťažko sa hľadajú, draho najímajú, najdlhšie trvá, kým sú produktívni. Rozpočtujte 12 – 18 mesiacov.

**Bezpečnosť GenAI** vyžaduje tradičnú bezpečnostnú odbornosť plus znalosti špecifické pre AI. Bezpečnostné myslenie sa prenáša; znalosti AI sú skutočne nové. Rozpočtujte 6 – 12 mesiacov na zvýšenie kvalifikácie.

**Agentná infraštruktúra** je najprístupnejšia. API integrácia, dátové inžinierstvo, automatizácia pracovných postupov: tieto zručnosti už existujú. Nové znalosti (MCP, embeddingy, vektorové databázy, prompt engineering) sa dajú naučiť za tri až šesť mesiacov. Rozpočtujte 3 – 6 mesiacov do prvých zákaziek.

**Správa viacerých modelov** stavia na všetkých troch a vzniká prirodzene so skúsenosťami.

| Príležitosť | Kľúčové talenty | Čas nábehu | Marža | Bariéra |
|---|---|---|---|---|
| Testovanie a validácia | Hodnotenie ML, štatistika, adverzariálne testovanie | 12 – 18 mesiacov | Najvyššia | Najvyššia |
| Bezpečnosť GenAI | Bezpečnosť + znalosti špecifické pre AI | 6 – 12 mesiacov | Vysoká | Vysoká |
| Agentná infraštruktúra | Integrácia, dátové inžinierstvo, automatizácia | 3 – 6 mesiacov | Stredná až vysoká | Stredná |
| Správa viacerých modelov | Prevádzková + AI šírka | Buduje sa časom | Vysoká | Stredná až vysoká |

---

## Odporúčanie

Začnite agentnou infraštruktúrou. Nie preto, že je najcennejšia (testovanie a validácia dlhodobo prinášajú vyššie marže), ale preto, že je prirodzeným prechodom od toho, čo už robíte. Vaši integrační inžinieri môžu začať stavať MCP servery a RAG pipeline do niekoľkých mesiacov. Tržby prídu rýchlejšie, lebo medzera v zručnostiach je najmenšia.

Využite zákazky na agentnú infraštruktúru na budovanie dôveryhodnosti a vzťahov s klientmi. Ako budete AI systémy nasadzovať a udržiavať, prirodzene narazíte na výzvy testovania, bezpečnosti a správy viacerých modelov, z ktorých každá je príležitosťou na rozšírenie.

Súbežne investujte do testovania a bezpečnosti:

- **Mesiace 1 – 6:** Dodajte prvé zákazky na agentnú infraštruktúru. Určte jedného až dvoch ľudí na budovanie odbornosti v testovaní a bezpečnosti. Pošlite bezpečnostný personál na školenia špecifické pre AI.
- **Mesiace 6 – 12:** Ponúkajte základné bezpečnostné audity AI popri nasadeniach infraštruktúry. Pilotujte testovacie služby u existujúcich klientov.
- **Mesiace 12 – 18:** Spustite formálnu prax testovania a validácie. Ponúkajte posudzovanie zhody podľa AI Actu EÚ. Pozicionujte správu viacerých modelov ako rozšírenie spravovaných služieb.
- **Mesiace 18 – 24:** Všetky štyri schopnosti fungujú ako integrovaná prax. Agentná infraštruktúra generuje vzťahy s klientmi. Testovanie a bezpečnosť generujú najvyššie marže. Správa viacerých modelov generuje najlepkavejšie opakované tržby.

> **Čo si z tejto kapitoly odniesť:** Tri súvisiace príležitosti (testovanie, bezpečnosť a agentná infraštruktúra) plus správa viacerých modelov ponúkajú vysokomaržové služby, ktoré si podniky nedokážu ľahko postaviť interne. Začnite agentnou infraštruktúrou, lebo sa najbližšie mapuje na existujúce zručnosti a najrýchlejšie generuje tržby. Súbežne investujte do testovania a bezpečnosti: regulačný dopyt je istý a marže najvyššie, ale požiadavky na talenty sú strmšie a čas k tržbám dlhší. Model je len volanie API. Všetko okolo neho je váš biznis.

---

> **Strážca čerstvosti** · *overené apríl 2026 · odhadovaný polčas rozpadu: ~9 mesiacov*
>
> Tri kategórie služieb sú trvanlivé; špecifiká toho, ako ich dodávate, sa budú vyvíjať.
>
> - **Dátumy vymáhania AI Actu EÚ** (august 2026 pre vysokorizikové systémy, august 2027 pre bezpečnostné komponenty v sektorovo regulovaných produktoch) sú pevne dané zákonom, ale vykonávacie usmernenia a postupy posudzovania zhody sa stále publikujú a budú sa vyvíjať počas rokov 2026 – 2027.
> - **Ceny služieb** (posúdenie 20 – 50 tis. $, monitorovanie 3 – 10 tis. $/mesiac, red-teaming 30 – 80 tis. $) odrážajú súčasné trhové sadzby. Očakávajte ich stlačenie, ako trh dozreje a vstúpi viac poskytovateľov: okno 12 – 24 mesiacov, kým sa toto viac skomoditizuje.
> - **Krajina MCP, RAG nástrojov a vektorových databáz**: konkrétne produkty a štandardy citované tu sa menia každých 6 – 12 mesiacov. Podkladové disciplíny (API integrácia, dátové inžinierstvo) sú trvalé.
> - **Krajina hrozieb**: prompt injection, otrávenie modelov, jailbreakové techniky sa neustále vyvíjajú. Akýkoľvek konkrétny útok opísaný v tejto kapitole môže byť v čase čítania zmiernený; kategórie ostávajú relevantné.

---

*Kapitola 9 skúma, ako tá istá AI, ktorú sa učíte predávať klientom, súčasne mení spôsob, akým dodávate svoje existujúce služby, a prečo táto vnútorná disrupcia môže byť najdôležitejšou strategickou výzvou, ktorej čelíte.*
