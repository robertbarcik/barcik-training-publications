# Kapitola 6: Nezávislé frameworky

---

Existuje menší, hlučnejší kút krajiny frameworkov, kde je definujúcou črtou *ne*byť zarovnaný s dodávateľom modelov. To sú nezávislé (agnostické) frameworky. Predpokladajú, že budete chcieť vymieňať modely, cloudy a sady nástrojov, a optimalizujú pre túto flexibilitu aj za cenu rýchlosti vývojára.

Dominujú dva: **LangGraph** a **CrewAI**. Oba sú staršie než väčšina dodávateľských SDK, oba majú väčšie komunity než ktorýkoľvek jednotlivý dodávateľský framework a oba sa dnes stavajú do pozície neutrálnej strednej vrstvy (Švajčiarska), ktorú budú veľké podniky nakoniec chcieť mať medzi sebou a dodávateľmi základných modelov.

Cloudová analógia tu drží pevne. Ak sú dodávateľské frameworky PaaS, **LangGraph je Kubernetes** a **CrewAI je Docker Compose**.

## LangGraph ako Kubernetes

Agentné pracovné postupy ako stavové automaty. Uzly (kroky). Hrany (prechody). Stav tečie grafom. Framework je explicitný ohľadom perzistencie: v každom kroku sa stav uloží do kontrolného bodu, takže ak server spadne alebo sa agent pozastaví na ľudské schválenie, pracovný postup pokračuje presne tam, kde skončil. Jeho trvanie na štrukturálnej explicitnosti je to, čo mu dáva silu, a to, čo generuje väčšinu sťažností.

Silné stránky.

**Trvanlivé vykonávanie.** Definujúca schopnosť LangGraphu. Dlho bežiaci agenti sa môžu pozastaviť na hodiny alebo dni, čakať na ľudský vstup, prežiť reštarty servera a pokračovať bez straty stavu. Pre regulačné schvaľovania, viackrokové pracovné postupy s krokmi s človekom v slučke, agentov, ktorí bežia cez noc; často jediné zvládnuteľné riešenie.

**Pozorovateľnosť a audit.** LangGraph sa prirodzene páruje s LangSmithom, ktorý poskytuje hlboké stopy, testovacie postroje a záznamy audítorskej kvality o každom volaní modelu, vyvolaní nástroja a prechode stavu. Pre regulované podniky môže byť táto papierová stopa rozdielom medzi nasaditeľným agentom a zablokovaným.

**Nezávislosť od modelu.** LangGraphu je jedno, či je podkladový model Claude, GPT, Gemini, Mistral alebo lokálna Llama. Primitíva frameworku sú modelovo neutrálne. Môžete vymeniť vrstvu modelu bez prepisovania pracovného postupu, čo je celá pointa.

**Produkčný rozsah.** Najzrelší produkčný príbeh zo všetkých agentných frameworkov. Vyše 400 verejne zdokumentovaných produkčných nasadení vrátane prípadov vo veľkom rozsahu (agent zákazníckej podpory Klarny s 85 miliónmi používateľov, 80-percentné skrátenie času riešenia). Nudné funkcie spoľahlivosti (združovanie spojení, sémantika opakovania, odstupy, obmedzovanie rýchlosti), na ktorých v produkcii záleží viac než v demách.

Jedna poctivá hviezdička pri tom vlajkovom čísle. Klarna je zároveň varovný príbeh odvetvia: jej skorší asistent podpory postavený na OpenAI bol tvárou stratégie „AI na prvom mieste“, ktorá zoškrtala zhruba 700 pozícií v podpore, zhoršila kvalitu služieb a do polovice roka 2025 mala firma verejne znova naberať ľudí do hybridného modelu. Nasadenie na LangGraphe je iný, neskorší systém a to číslo o rozsahu je skutočné. Ale keď sa to isté logo objaví v prípadovej štúdii dodávateľa aj v korporátnom cúvaní, čítajte prípadovú štúdiu ako marketing, nie ako dôkaz.

Cenou je skutočná krivka učenia. Vývojárom prichádzajúcim z prístupu „proste napíš kód agenta“ pripadá grafový formalizmus LangGraphu pre jednoduché prípady upovedaný. Kritici ho volajú „veľmi vyumelkovaný if-else“ a pre trojkrokového lineárneho agenta majú kus pravdy. Hodnota LangGraphu sa ukáže vo veľkom, v produkcii, v hraničných podmienkach, nie v demách.

**Berte LangGraph vážne, ak** ste v regulovanom odvetví, prevádzkujete dlhých agentov alebo agentov s človekom v slučke, robíte smerovanie medzi viacerými modelmi, čelíte mandátom proti lock-inu z úrovne predstavenstva alebo ste dosť veľkí na to, aby ste krivku učenia vstrebali.

## CrewAI ako Docker Compose

Práca organizovaná tak, ako to robí ľudský tím. Vytvoríte agentov, každému dáte rolu („senior dátový analytik“), cieľ („nájdi trendy v dátach o predaji za 2. kvartál“) a príbeh. Zložíte ich do „posádky“ a posádke dáte úlohu. CrewAI tím orchestruje. Biznisoví zadávatelia si vedia prečítať definíciu agenta v CrewAI a pochopiť, čo sa deje, a táto prívetivosť je zároveň najväčšou silou aj najväčšou slabosťou.

Silné stránky.

**Rýchlosť prototypovania.** Nič v žiadnej z oboch kategórií frameworkov nerozbehne multiagentný prototyp tak rýchlo. Pre workshopy, overenia konceptu, demá často najrýchlejšia cesta.

**Uvažovanie založené na rolách.** Pre úlohy, kde je prirodzený rozklad „tím špecialistov“ (výskumné pipeline, tvorba obsahu, analytické pracovné postupy), je abstrakcia založená na rolách elegantná. Sadne na tvar.

**Podpora protokolov.** Natívna podpora MCP a A2A, skôr než vo väčšine frameworkov. Dizajn s viacerými agentmi na prvom mieste.

**Hybnosť komunity.** Vyše 44 000 hviezdičiek na GitHube, aktívny Discord, rastúci komerčný ekosystém. Množstvo príkladov, ktoré si môžete požičať.

Cena: abstrakcie optimalizované na prototypovanie, nie na produkciu. Tenšia správa stavu, obmedzené kontrolné body. Pre dlho bežiaceho agenta kritického pre prevádzku vás CrewAI núti riešiť podnikové starosti mimo frameworku, a v tom bode ste jeho hlavnú hodnotu (rýchle prototypovanie) už prerástli.

**Berte CrewAI vážne, ak** robíte rýchle overenia konceptu, workshopy alebo multiagentné pracovné postupy, kde rozklad podľa rol sedí prirodzene a na čase do dema záleží viac než na čase do piatich deviatok.

## „Ale modely sa stali príliš dobrými“: protiargument

Kým si ktokoľvek osvojí nezávislý framework, mal by rozumieť najsilnejšiemu argumentu proti tomu.

Nezávislé frameworky existujú sčasti preto, že rané LLM boli slabé. Kontextové okná boli malé, tak frameworky pridali zhŕňanie a správu pamäte. Uvažovanie bolo nespoľahlivé, tak frameworky pridali štruktúrovaný riadiaci tok. Volanie funkcií bolo hrubé, tak frameworky pridali lešenie na validáciu nástrojov. Halucinácie boli časté, tak frameworky pridali vrstvy opakovania a validácie. Významná časť toho, čo LangGraph robí, vznikla ako záplata na obmedzenia modelov.

V roku 2026 sú podkladové modely dramaticky lepšie. Kontextové okná v miliónoch tokenov, nie v tisícoch. Uvažovanie dosť spoľahlivé na to, aby jediné dobre promptované volanie modelu zvládlo úlohy, ktoré pred osemnástimi mesiacmi vyžadovali viackrokový graf. Volanie funkcií presné. Štruktúrovaný výstup natívny. Pre zmysluplný výsek prípadov použitia dnes otázka „potrebujem framework, aby to orchestroval?“ znie „pravdepodobne nie, ak je model dosť dobrý“.

Tento argument má skutočnú váhu. Vývojár, ktorý v roku 2026 stavia agenta, má aspoň tri možnosti, ktoré v roku 2024 neexistovali: obyčajné LLM v slučke (funguje vo viacerých prípadoch než kedysi), dodávateľské SDK s agresívnymi hostovanými funkciami (odstráni väčšinu integračnej inštalatérčiny) a AI asistenta na programovanie, ktorý vygeneruje lešenie agenta na mieru za desať minút. Všetky tri stláčajú priestor, kde je nezávislý framework správnou odpoveďou.

Daň za abstrakciu je tiež skutočná. LangGraph pridáva vrstvy medzi vývojára a model. Keď niečo zlyhá, musíte sa cez tie vrstvy prehrabať k promptu, ktorý zlý výstup naozaj vyprodukoval, „produkčná archeológia“. Pre jednoduchých agentov tá cena prevyšuje prínos prenositeľnosti.

Poctivá verzia argumentu za nezávislé frameworky je v roku 2026 **užšia než pred osemnástimi mesiacmi**. Nezávislé frameworky stále rozhodne vyhrávajú, keď máte: potreby trvanlivosti, ktoré dodávateľské SDK neponúkajú, smerovanie medzi viacerými modelmi vynútené súladom alebo nákladmi, hlboké audítorské potreby regulovaného odvetvia alebo vážny organizačný mandát proti lock-inu. Mimo toho je dôvod platiť daň za abstrakciu slabší než kedysi.

## Kedy je argument za nezávislosť najsilnejší

**Regulované odvetvia**, kde je vymeniteľnosť otázkou súladu. Keď sa regulátor spýta „viete preukázať, že tento systém nezávisí od pokračujúceho dobrého správania jediného dodávateľa?“, chcete framework, ktorý vám dovolí odpovedať áno.

**Smerovanie medzi viacerými modelmi.** Keď jeden pracovný postup vyžaduje lokálny model s otvorenými váhami z dôvodov súladu a iný ťaží z frontier API, framework navrhnutý na smerovanie je oveľa jednoduchší než taký, ktorý predpokladá jediný model.

**Dlho bežiace, vysoko rizikové, s človekom v slučke.** Agenti, ktorí sa pozastavujú na dni alebo týždne, potrebujú nepriestrelnú obnoviteľnosť a nesú stav audítorskej kvality cez zložité schvaľovacie toky. Trvanlivé vykonávanie LangGraphu je ťažké zreplikovať od nuly.

**Mandáty proti lock-inu z úrovne predstavenstva.** V niektorých podnikoch je požiadavka „musí byť nezávislé od modelu“ direktívou z najvyššieho vedenia s právnou a obchodnou váhou. Debata o tom, či je dodávateľské SDK „technicky dosť dobré“, je bezpredmetná.

**Veľké inžinierske organizácie** s kapacitou vstrebať krivku učenia. Daň za abstrakciu sa znáša ľahšie s desiatimi inžiniermi prispievajúcimi do platformy než s dvoma, ktorí sa snažia dodať pred koncom kvartálu.

Pre typický podnik v roku 2026 znie poctivá odpoveď: pravdepodobne dodávateľské SDK dnes, s realistickou možnosťou migrovať na nezávislý framework v roku 2027, ak si to vyžiada rozsah, regulačné prostredie alebo vzťah s dodávateľom. Pre *regulovaný* podnik (najmä v Európe, kde hryzú obavy o súlad z kapitoly 9) sa odpoveď silnejšie prikláňa k nezávislému táboru už od začiatku.

**Poistky niečo stoja. Vyplatia sa v konkrétnych scenároch. Či za to stoja, závisí od toho, koľko rizika nesiete a nakoľko veríte, že tie scenáre nastanú.** To je argument za nezávislosť, poctivo vyslovený.

---

*Ďalej: [Kapitola 7: Pozorovateľnosť, vyhodnocovanie a náklady](07_observability_cost_governance.md)*
