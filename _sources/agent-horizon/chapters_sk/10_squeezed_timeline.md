# Kapitola 10: Naozaj sa časová os stlačí?

---

Všetko doteraz predpokladalo, že agentný prechod sa bude hýbať rýchlejšie než cloudový a že najmä európske podniky budú mať dôvod skočiť rovno k zrelej architektúre namiesto prežívania fázy lock-inu. Tento predpoklad je zapečený v radách, ktoré táto brožúra dáva. Je aj skutočne sporný. Táto kapitola dlhuje čitateľovi predpoveď: nie esej „na jednej strane, na druhej strane“, ale jasný verdikt o tom, kam ukazujú dôkazy a čo by sa muselo stať, aby bol verdikt nesprávny.

## Dva scenáre

**Scenár Preskok.** Podniky, najmä v Európe, sa rýchlo posunú za lock-in u dodávateľa a do rokov 2027 až 2028 sa usadia na hybridných, nezávislých architektúrach s intenzívnym smerovaním. Protokoly v štýle MCP ovládnu prístupovú vrstvu. Nezávislé frameworky v štýle LangGraphu sa stanú referenčnou orchestračnou vrstvou pre regulované odvetvia. Dodávateľské SDK pretrvajú ako akceleračné nástroje pre menej regulované vertikály, ale nestanú sa dominantným podnikovým štandardom. Nástroje na pozorovateľnosť a audit sa stanú samostatnou kategóriou podnikového softvéru analogickou k APM. Cyklus, ktorý cloudovému odvetviu trval dvanásť rokov, sa uzavrie za päť.

**Scenár Očistec pilotov.** Väčšina podnikov uviazne v tej istej pasci, ktorá už chytá 95 % AI pilotov: technológia funguje, piloty sú zaujímavé, škálovanie nikdy nenastane. Modely sa ďalej zlepšujú, čo paradoxne robí frameworky menej potrebnými, čo drží architektúry malé a neformálne. Dodávateľské SDK vyhrajú automaticky, lebo sú cestou najmenšieho odporu. Nezávislé frameworky ostanú špeciálnou starosťou úzkeho výseku regulovaných podnikov. Cyklus lock-inu pripomína cloudový cyklus, dlhú chaotickú prechodnú fázu trvajúcu väčšinu desaťročia.

## Verdikt

Najpravdepodobnejší výsledok je **rozdvojený, naklonený k Preskoku pre regulovanú EÚ a k Očistcu pilotov pre všetkých ostatných**. Regulované európske podniky (bankovníctvo, poisťovníctvo, verejný sektor, zdravotníctvo, obrana) Preskočia, lebo AI Act je priama vynucovacia sila a architektúry, ktoré potrebujú na splnenie súladu, vyzerajú ako zrelý konečný stav. Všetci ostatní strávia čas v Očistci pilotov, nie preto, že technológia zlyhá, ale preto, že organizačná mašinéria (kvalita dát, sponzorstvo vedenia, disciplína vyhodnocovania) nie je pripravená. Dodávateľské SDK urobia väčšinu tichej ťažkej práce pri pilotoch, ktoré uspejú. Nezávislé frameworky plus pozorovateľnosť ovládnu dlhodobú architektúru pre záťaže, na ktorých záleží najviac.

V cloudovej paralele: Preskok vyzerá ako európsky podnik v roku 2012, ktorý preskočil monokultúru AWS a išiel rovno do hybridného cloudu s Kubernetesom. Očistec pilotov vyzerá ako americký stredne veľký podnik v roku 2015, ktorý stále prevádzkuje paralelné systémy v troch cloudoch a snaží sa prísť na súvislú stratégiu. Oba existovali; oba boli racionálnou odpoveďou na konkrétne podmienky.

## Prečo sa to stále môže mýliť: pomenované predstihové indikátory

Predpoveď má byť vyvrátiteľná. Tu je šesť konkrétnych indikátorov na roky 2026 až 2027. Ak sa budú vyvíjať, ako je uvedené, Preskok pre regulovanú EÚ platí. Ak nie, mýlim sa.

**1. MCP dosiahne 200 miliónov mesačných stiahnutí SDK do 4. kvartálu 2026.** Dnes ~97 miliónov. Pokračujúce zdvojnásobovanie potvrdí, že protokolová vrstva je naozaj ustálená. Sploštenie pod 150 miliónov do 4. kvartálu znamená, že prijímanie protokolu stagnuje a téza slabne.

**2. AI Act prinesie aspoň jeden verejne oznámený vynucovací krok pri vysokorizikovom systéme do 2. kvartálu 2027.** Nie varovný list, skutočnú pokutu alebo príkaz. Bez toho je premisa vynucovacej sily slabšia, než som tvrdil.

**3. LangSmith prekročí 1 000 platených podnikových licencií do 3. kvartálu 2026.** Konkrétne, sledovateľné (LangChain zverejňuje míľniky). Ak sa kategória pozorovateľnosti nemonetizuje, predpoveď „stane sa vlastnou softvérovou kategóriou ako APM“ neplatí.

**4. Mistral, Aleph Alpha alebo podobne postavené európske laboratórium dodá do polovice roka 2027 model do 10 % od špičky (na pomenovanom benchmarku, povedzme GPQA alebo SWE-Bench).** Ak sa medzera namiesto toho rozšíri, smerovací vzor sa pre záťaže náročné na uvažovanie zrúti a európske podniky budú nútené voliť medzi prístupom k špičke a suverenitou. Šance Očistca pilotov podstatne stúpnu.

**5. Aspoň jeden z OpenAI, Googlu alebo Anthropicu dodá do konca roka 2026 pre zákazníkov v EÚ záruku rezidencie dát v suverénnom cloude (zmluvne záväznú, nielen regionálnu dostupnosť).** Ak áno, dodávateľské SDK ostanú v hre pre európske regulované záťaže a argument za nezávislosť zoslabne. Ak nie, dodávateľské SDK sú fakticky diskvalifikované z kusa regulovaného trhu EÚ.

**6. A2A (alebo jeho priamy nástupca) dosiahne do konca roka 2027 vyše 10 000 verejných kariet agentov v objaviteľnom registri.** To je indikátor toho, že interoperabilita medzi agentmi sa stáva všadeprítomnou, nie teoretickou. Ak premávka A2A ostane interná v rámci jednotlivých podnikov, premisa „multiagentná architektúra sa stane hlavným prúdom“ sa odloží a načasovanie Preskoku sa posunie.

**Toto nie sú obvyklé indikátory. Nikto iný ich nesleduje ako súvislú množinu.** Ak sa tri zo šiestich pohnú, ako je opísané, predpoveď platí. Ak sa tri alebo viac nepohnú, mýlim sa v načasovaní alebo v tvare, pravdepodobne v oboch.

## Prvé čítanie: júl 2026

Tri mesiace je skoro na skórovanie predpovede, ale táto brožúra sľúbila vyvrátiteľnosť, tak tu je prvé čítanie tabule.

**Indikátor 1 (MCP na 200 miliónoch mesačných stiahnutí do 4. kvartálu 2026): hýbe sa podľa predpovede.** Oficiálne citované číslo je stále ~97 miliónov, ale práca na protokole ukazuje správnym smerom: revízia špecifikácie, ktorá pristáva 28. júla (bezstavové jadro, spevnenie podnikovej identity, rozšírenia Apps a Tasks), je presne ten míľnik pripravenosti pre podniky, ktorý kapitola 3 kázala sledovať. Rozhodne číslo za 4. kvartál.

**Indikátor 2 (prvý vynucovací krok podľa AI Actu pri vysokorizikovom systéme do 2. kvartálu 2027): otvorený.** Zatiaľ nič verejné a okno beží ešte rok. Augustové termíny 2026 prichádzajú budúci mesiac; hodiny sa naozaj rozbehnú až vtedy.

**Indikátor 3 (LangSmith na 1 000 platených podnikových licenciách do 3. kvartálu 2026): neoverené, ale smerovo podporené.** LangChain počet licencií nezverejnil. Čo sa stalo: LangGraph aj LangChain dosiahli verziu 1.0 a LangSmith sa rozdelil na samostatné produktové línie pre pozorovateľnosť, vyhodnocovanie a nasadzovanie. Kategórie sa takto neproduktizujú, pokiaľ niekto neplatí.

**Indikátor 4 (európske laboratórium do 10 % od špičky do polovice roka 2027): zakalený udalosťami.** Júlové znovuvydanie najschopnejších amerických modelov za bránami (preverené firmy na najvyššej úrovni, pod ňou nákladné moderované API) sťažuje samotné meranie: ktokoľvek mimo prevereného kruhu má dnes problém sa voči špičke čo i len benchmarkovať. Otázka medzery sa mení na otázku prístupu.

**Indikátor 5 (zmluvne záväzná záruka suverénneho cloudu od OpenAI, Googlu alebo Anthropicu do konca roka 2026): skôr proti, z dôvodu, ktorý predpoveď nepomenovala.** To isté zavedenie brán tlačilo opačným smerom než záruka rezidencie; živou otázkou v júli 2026 nie je, kde model beží, ale kto ho vôbec smie spustiť. Ak to vydrží, indikátor sa vyrieši ako „nie“ a argument za nezávislosť sa posilní ostrejšie, než pôvodná predpoveď predpokladala. Mechanika je zmapovaná v [Merkantilizme generatívnej AI](/mercantilism-of-genai/#m-bloc); rámec scenárov, ktorý to živí, je [Scenario Planning for Generative AI](/scenario-planning/).

**Indikátor 6 (vyše 10 000 verejných kariet agentov do konca roka 2027): hýbe sa podľa predpovede, skoro.** A2A pohltilo svojho hlavného rivala (ACP od IBM), prekročilo 150 členských organizácií a vo vydaní 1.2 dodalo kryptograficky podpísané karty agentov. Otázka rozsahu registra ostáva otvorená.

Stali sa dve veci, ktoré zoznam indikátorov nepredvídal. Gartner dnes predpovedá, že 40 % projektov agentnej AI bude do roku 2027 zrušených, čo je Očistec pilotov, ktorý získal citáciu. A OpenAI jedenásť mesiacov po spustení ukončilo svoj no-code Agent Builder, pripomienka, že dodávateľská vrstva sa stále vrtí, kým protokolová vrstva tvrdne.

Čisté čítanie: dva indikátory sa hýbu podľa predpovede, dva sú otvorené, jeden zakalený, jeden sa nakláňa proti spôsobom, ktorý jadro rád tejto brožúry posilňuje, nie oslabuje. Rozdvojený verdikt platí. Ďalšie čítanie príde s číslami za 4. kvartál.

> **Naša predpoveď v jednej vete:** Regulované európske podniky Preskočia zhruba do roku 2028; väčšina ostatných podnikov prežije stlačenú, ale skutočnú verziu cyklu lock-inu z cloudovej éry; dodávateľské SDK vyhrajú krátkodobo a nezávislé frameworky plus ich ekosystém pozorovateľnosti vyhrajú dlhodobo pre záťaže, na ktorých záleží najviac, pokiaľ sa tri zo šiestich pomenovaných indikátorov vyššie nepohnú, ako je opísané, a v takom prípade som cyklus prečítal zle.

---

*Ďalej: [Kapitola 11: Výber vášho stacku](11_picking_your_stack.md)*
