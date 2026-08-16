# Kapitola 4: Orchestračná vrstva

---

S oboma protokolmi za sebou máme spodné poschodia stacku na mieste. LLM vie uvažovať. MCP vie siahnuť po nástrojoch a dátach. A2A vie siahnuť po iných agentoch. Ale niečo stále musí rozhodnúť, *čo agent skutočne robí*: ktorý nástroj zavolať ako prvý, čo robiť, keď zlyhá, kedy skončiť, kedy sa spýtať používateľa, kedy odovzdať prácu ďalej.

To je orchestračná vrstva. Tu býva mozog. A je to vrstva, na ktorej sa odohráva väčšina zaujímavých hádok o frameworkoch, lebo na rozdiel od protokolovej vrstvy (ustálenej okolo MCP) a modelovej vrstvy (hŕstka dominantných dodávateľov) je orchestračná vrstva stále naozaj sporná.

Kým v ďalších dvoch kapitolách zmapujeme frameworky, jedna základnejšia otázka: potrebujete framework vôbec?

## Základná úroveň: LLM v slučke

Najjednoduchšia možná architektúra agenta nemá framework. Je to slučka while, jazykový model s podporou volania funkcií a zoznam nástrojov:

1. Pošlite modelu požiadavku používateľa, katalóg nástrojov a doterajší rozhovor.
2. Model buď vráti konečnú odpoveď (stop), alebo volanie nástroja (pokračuj).
3. Ak je to volanie nástroja, vykonajte ho, pripojte výsledok do rozhovoru, choďte na 1.

To je všetko. Žiadny framework. Žiadny graf. Žiadne odovzdávanie. Pre prekvapivo veľkú triedu podnikových prípadov použitia to stačí. Zvládne väčšinu asistentov v štýle chatbota, väčšinu prípadov „agent nad konkrétnou sadou nástrojov“, väčšinu krátko bežiacich úloh s menej než tuctom nástrojov.

Na tomto záleží, lebo inštinkt odvetvia je siahnuť po frameworku okamžite, často skôr, než ho prípad použitia vyžaduje. Framework má skutočné náklady: krivku učenia, daň za abstrakciu, vrstvu nepriamosti medzi vami a modelom, produkčnú archeológiu, keď sa niečo pokazí. Ak tie náklady ešte nepotrebujete, neplaťte ich.

**Prvá poctivá otázka v každom agentnom projekte je, či ste naozaj vyskúšali LLM v slučke s dobrými promptmi a čistou sadou nástrojov. Ak nie, ešte neviete, či framework potrebujete.**

V cloudovej analógii je LLM v slučke obyčajná inštancia EC2 s vlastnými skriptmi. Nie sofistikovaná, nie pôsobivá pri revízii návrhu, často presne správny nástroj na danú prácu a nedostatočne využívaná, lebo nie je v móde.

## Keď základná úroveň prestane stačiť

Základná úroveň začne bolieť v predvídateľnej množine scenárov. Keď na ne narazíte, framework si zaslúži svoje miesto.

**Netriviálny riadiaci tok.** Model potrebuje plánovať, vykonať kroky paralelne a potom syntetizovať. Alebo politiku opakovania s odstupom pre jeden konkrétny nástroj. Alebo vetvenie, kde model rozhoduje medzi dvoma podpostupmi. Vyjadriť to čisto v slučke rýchlo zoškaredie.

**Stav a pamäť naprieč ťahmi.** Slučka s dlhým rozhovorom pchá všetko do promptu, kým kontextové okno nepretečie. Framework vie udržiavať explicitný stav, zhŕňať staršiu históriu, ukladať kontrolné body priebehu a pokračovať z uloženého stavu. Pre každého agenta, ktorý žije dlhšie než jedno sedenie, správa stavu nie je voliteľná.

**Koordinácia viacerých agentov.** Len čo máte viac než jedného agenta, základná úroveň sa stane nesprávnou. Frameworky ponúkajú štruktúrované vzory pre hierarchie nadriadený/pracovník, tímy špecialistov, delegovanie sprostredkované cez A2A. Postaviť to bez frameworku sa dá, ale málokedy je to dobré využitie úsilia.

**Mantinely a spätné volania.** Produkční agenti potrebujú háčiky. „Pred každým volaním nástroja skontroluj oprávnenia.“ „Po odpovedi modelu spusti filter na zaujatosť a osobné údaje.“ „Ak agent minie viac než päť eur, zastav sa a spýtaj sa.“ Frameworky vám dajú pomenované body životného cyklu. Slučka vás núti rozsypať tie isté kontroly po celom kóde, čo rýchlo zhnije.

**Trvanlivosť.** Tridsaťsekundový proces je v slučke v poriadku. Osemhodinový nie; ak sa server reštartuje, stratíte všetko. LangGraph ponúka trvanlivé vykonávanie: stav s kontrolnými bodmi, dlho bežiaci agenti sa pozastavia a pokračujú, pády sú obnoviteľné. Vážna inžinierska otázka pre agentov, ktorí robia skutočnú prácu vo veľkom.

**Pozorovateľnosť a vyhodnocovanie.** Produkční agenti potrebujú stopy, priraďovanie nákladov na tokeny, metriky kvality, možnosť prehratia. Frameworky to buď poskytujú, alebo sa integrujú s nástrojmi (LangSmith, Langfuse, Phoenix), ktoré to robia. Postaviť si to sami je poriadny projekt, ktorý má vlastnú kapitolu (kapitola 7).

Narazte na viacero z týchto naraz a framework prestane byť príjemným doplnkom a stane sa nevyhnutnou infraštruktúrou. Nenarazte na žiadny a je to väčšinou mŕtva váha.

## Dve rodiny

Ak framework potrebujete, prichádza kľúčové rozhodnutie tejto brožúry: ktorý?

K roku 2026 sa krajina vyjasnila do dvoch širokých rodín.

**Dodávateľské frameworky.** Google ADK, OpenAI Agents SDK, Claude Agent SDK, AWS Strands, Azure AI Foundry Agent Service. Každý postavil dodávateľ infraštruktúry alebo základných modelov, každý je optimalizovaný pre ekosystém svojho tvorcu. Ponuka: rýchlosť vývojára. Hrajú rolu, ktorú hrali AWS Elastic Beanstalk a Google App Engine: názorovo vyhranené, rýchle a zarovnané s dodávateľom.

**Nezávislé frameworky.** LangGraph, CrewAI a malý počet tichších uchádzačov. Nezávislé od modelu aj od cloudu. Ponuka: prenositeľnosť a kontrola. Hrajú rolu, ktorú hrali Kubernetes a Docker Compose: viac kontroly, viac práce, viac odolnosti voči budúcnosti.

Ani jedna rodina nie je „lepšia“. Riešia rôzne problémy. Dodávateľské frameworky sú pre tímy, ktoré chcú dodávať rýchlo a zmierili sa so záväzkom voči dodávateľovi. Nezávislé frameworky sú pre tímy, ktoré chcú dlhodobú prenositeľnosť a zaplatia za ňu daň za abstrakciu.

Ďalšie dve kapitoly pokrývajú každú rodinu po poradí: kapitola 5 mapuje dodávateľov; kapitola 6 pokrýva nezávislé frameworky a vyrovnáva sa s protiargumentom „modely sa stali príliš dobrými“, ktorý získava na váhe.

## Ešte jedna oprava mentálneho modelu

Je ľahké (najmä pre vývojárov prichádzajúcich z tradičného softvéru) myslieť si o orchestračnej vrstve, že „to je ten agent“. Nie je. Orchestračná vrstva je manažér. Skutočná inteligencia je vo vrstve LLM pod ňou. Skutočná schopnosť je v nástrojoch a dátach vystavených cez MCP. Skutočnú hodnotu produkujú systémy na dne. Dobrý framework je cenný tak, ako je cenný dobrý projektový manažér: dokáže, aby tím múdrych špecialistov dobre spolupracoval. A žiadny framework, akokoľvek vyleštený, nezachráni slabých špecialistov.

Dôsledok: keď agentné projekty zlyhávajú, inštinkt často velí vymeniť framework. To je takmer vždy nesprávne. Zlyhanie je zvyčajne v sade nástrojov, v návrhu promptov, v testovacom postroji alebo vo výbere modelu, nie v orchestrátorovi. Najprv diagnostikujte. **Ak je vaším prvým inštinktom, keď sa agent správa zle, siahnuť po inom frameworku, pravdepodobne liečite nesprávnu chorobu.**

---

*Ďalej: [Kapitola 5: Dodávateľské frameworky](05_vendor_frameworks.md)*
