# Horizont agentov

## Strategický sprievodca podnikovým stackom na vývoj agentov

---

**Apríl 2026 &middot; prvé čítanie indikátorov júl 2026 &middot; slovenské vydanie august 2026**

*Robert Barcik*

*LearningDoe s.r.o.*

*Kontakt: [robert@barcik.training](mailto:robert@barcik.training)*

---

### O tejto brožúre

Každých pár týždňov sa objaví nový framework na agentov. Oznámi sa nový protokol. Ďalšia dodávateľská sada nástrojov sľubuje, že všetko zjednoduší. Pre inžiniera alebo biznisového zadávateľa, ktorý plánuje cestovnú mapu na roky 2026 až 2028, je pomer signálu k šumu hrozný a v hre je veľa.

Táto brožúra je konceptuálna mapa, nie porovnanie funkcií. Jej cieľom je pomôcť vám vidieť, **čo v rodiacom sa agentnom stacku kde sedí**, **prečo každá vrstva existuje** a **ako sa jednotlivé kúsky s najväčšou pravdepodobnosťou vyvinú** v najbližších dvoch až troch rokoch. Kostrou je analógia, ktorú už poznáte: prechod do cloudu. Paralely nie sú dokonalé, ale namapovanie agentných primitív na známe cloudové pojmy vám dá mentálny model, ktorý prežije aj ďalšie kolo premenovávania.

Keď dočítate, mali by ste vedieť s istotou odpovedať na štyri otázky. Čo je MCP a prečo ho všetci berú ako uzavretú vec? Aký je skutočný rozdiel medzi Google ADK, OpenAI Agents SDK, Claude Agent SDK a LangGraphom? A kedy má ktorý zmysel? Kde býva lock-in a nakoľko by vás mal trápiť? A konkrétne pre európsky podnik: je rozumnejšie najprv sa zviezť na dodávateľskej vlne a prenositeľnosť riešiť neskôr, alebo investovať do nezávislej infraštruktúry už teraz?

Brožúra sa uzatvára rozpracovanou prípadovou štúdiou: regulovaná európska banka prekladá rámec piatich otázok do konkrétneho stacku (vrátane jediného rozhodnutia, kde rámec hovoril jedno a my sme urobili druhé, a prečo to bolo správne).

Žiadny hype. Žiadne zadýchané predpovede. Len mapa a jeden konkrétny príklad.

### Pre koho je táto brožúra

- **Podnikoví inžinieri**, ktorí hodnotia frameworky na agentov pre produkčné nasadenie
- **Architekti**, ktorí navrhujú multiagentné systémy, ktoré musia prežiť jedného dodávateľa
- **Technologickí lídri**, ktorí tvarujú cestovnú mapu na roky 2026 až 2028
- **Biznisoví zadávatelia**, ktorí sa snažia pochopiť, o čom sa ich inžinieri hádajú

Ak ste v rozhovore počuli pojmy *MCP*, *ADK*, *LangGraph* alebo *A2A*, prikyvovali ste a potichu premýšľali, čo z toho je protokol a čo framework, táto brožúra je pre vás.

### Ako ju čítať

Kapitoly 1 a 2 stavajú mentálny model. Prečítajte si ich ako prvé, aj keď ste v téme hlboko. Kapitola 3 pokrýva dva ustálené protokoly (MCP a A2A). Kapitola 4 predstavuje orchestračnú vrstvu; kapitoly 5 a 6 mapujú jej dve rodiny (dodávateľskú a nezávislú). Kapitola 7 sa venuje pozorovateľnosti. Kapitoly 8 až 10 pokrývajú stratégiu: lock-in, európsky uhol, časovú os. Kapitola 11 to všetko spája do rozhodovacieho rámca, rozpracovanej prípadovej štúdie banky a krátkeho epilógu.

Kapitola 10 urobila svoju predpoveď vyvrátiteľnou šiestimi pomenovanými indikátormi; toto vydanie pridáva ich datované prvé čítanie (júl 2026). Zvyšok textu ostáva aprílovou snímkou, s rovnakou disciplínou, akú naše brožúry o [plánovaní scenárov](/scenario-planning/) a [merkantilizme](/mercantilism-of-genai/) držia svojimi denníkmi spúšťačov.

*Poznámka k slovenskému vydaniu: preložil Claude (Fable 5), ktorý sa podieľal aj na júlovej revízii originálu, 16. augusta 2026; prekladané významovo, nie slovo za slovom. Názvy protokolov, frameworkov a produktov ostávajú v angličtine; pojmy ako stack, framework a lock-in nechávame tak, ako sa používajú v slovenskej IT praxi. Pri pochybnostiach platí [anglický originál](/agent-horizon/).*

---

### Obsah

1. Paralela s cloudom
2. Vrstvová torta
3. Protokolová vrstva: MCP a A2A
4. Orchestračná vrstva
5. Dodávateľské frameworky
6. Nezávislé frameworky
7. Pozorovateľnosť, vyhodnocovanie a náklady
8. Otázka lock-inu
9. Európsky uhol
10. Naozaj sa časová os stlačí?
11. Výber vášho stacku: s rozpracovaným prípadom
