# Kapitola 2: Vrstvová torta

---

## Najčastejšia chyba

Ak čítate technologickú tlač o vývoji agentov, narazíte na vety ako „mali by ste použiť ADK, alebo MCP?“ alebo „firmy si vyberajú medzi Claude Agent SDK a Model Context Protocolom“. Tieto vety sú nezmysel. Berú protokol a framework ako súperiace možnosti, ktorými nie sú. Žijú na rôznych vrstvách stacku a robia rôznu prácu.

Toto nie je pedantská výhrada. Je to jediné najnosnejšie ujasnenie v celej brožúre. Ak si z tejto kapitoly odnesiete jednu vec, nech je to táto: agentný stack má vrstvy a kúsky, o ktorých počujete debatovať v tlači, nie sú vždy na tej istej. Rozhodnutia o frameworku sa dejú na jednej vrstve, rozhodnutia o protokole na druhej, rozhodnutia o modeli na tretej. „Nevyberáte si medzi“ položkami z rôznych vrstiev. Vyberiete si po jednej z každej a skombinujete ich.

Cloudový ekvivalent by bola otázka „máme použiť AWS, alebo HTTP?“ AWS je poskytovateľ cloudu; HTTP je protokol. Používate oboje. Nie sú to súperiace rozhodnutia; sú to doplňujúce sa rozhodnutia na rôznych úrovniach stacku.

## Vrstvy

Čítajte tento obrázok zhora nadol, od toho, čo zažíva používateľ, po to, čo skutočne robí prácu.

```
┌─────────────────────────────────────────────────────┐
│  ORCHESTRAČNÁ VRSTVA                                │
│  „Kedy voláme čo, s akým stavom, pod akými          │
│   mantinelmi, naprieč koľkými agentmi?“             │
│                                                     │
│  ADK · LangGraph · CrewAI · OpenAI Agents SDK ·     │
│  Claude Agent SDK · AWS Strands · Azure AI Foundry  │
├─────────────────────────────────────────────────────┤
│  VRSTVA LLM                                         │
│  Uvažujúci motor, ktorý generuje volania nástrojov, │
│  plány a odpovede.                                  │
│                                                     │
│  Gemini · Claude · GPT · Mistral · Llama · ...      │
├─────────────────────────────────────────────────────┤
│  VRSTVA PRÍSTUPU K NÁSTROJOM/AGENTOM                │
│  Ako LLM siaha po nástrojoch, dátach a iných        │
│  agentoch.                                          │
│                                                     │
│  MCP (nástroje a dáta) · A2A (agent–agent) ·        │
│  natívne volanie funkcií · priame volania SDK       │
├─────────────────────────────────────────────────────┤
│  SKUTOČNÉ SYSTÉMY                                   │
│  Databázy, API, súbory, SaaS aplikácie, iní agenti  │
└─────────────────────────────────────────────────────┘
```

Štyri vrstvy. Každá má odlišnú úlohu. Z každej vrstvy si niečo vyberiete a potom to poskladáte.

**Orchestračná vrstva.** „Mozog“ agenta. Rozhoduje, ktorý nástroj zavolať, v akom poradí, čo robiť pri zlyhaní, ako odovzdávať stav z kroku na krok, kedy skončiť. V jednoduchom agentovi to môže byť slučka `while`, ktorá volá model, kým nepovie „hotovo“. V zložitom agentovi je to viackrokový stavový automat s vetveniami, opakovaniami, paralelným vykonávaním a odovzdávaním podagentom. Google ADK, LangGraph, CrewAI, OpenAI Agents SDK, Claude Agent SDK, AWS Strands, Azure AI Foundry Agent Service. Všetky žijú tu. Nezhodujú sa v tom, či je správnou abstrakciou graf, tím agentov s rolami, postupnosť odovzdaní alebo strom podagentov. Všetky riešia ten istý základný problém.

**Vrstva LLM.** Model, ktorý premýšľa. Gemini, Claude, GPT, Mistral, Llama. Framework rozhoduje, *kedy* model zavolať a *čo urobiť* s výsledkom; model rozhoduje, *čo povedať*, keď je zavolaný. Framework je projektový manažér; model je špecialista, ktorého sa pýtajú na názor.

**Vrstva prístupu k nástrojom a agentom.** Ako agent siaha po nástrojoch, dátach a iných agentoch. Záležia dva protokoly: **MCP** pre nástroje a dáta (ako sa môj agent rozpráva s databázou alebo API), **A2A** pre komunikáciu agent–agent (ako sa môj agent rozpráva s agentom niekoho iného). Oba žijú na tejto vrstve. Kapitola 3 ich pokrýva spolu.

**Skutočné systémy.** Databázy, API, SaaS aplikácie, interné nástroje. Vrstva, ktorú už poznáte. Agenti ju nenahrádzajú; zapájajú sa do nej.

## Prečo je „ADK verzus MCP“ kategoriálna chyba

S vrstvami pred očami sa otázka rozpustí.

ADK žije na orchestračnej vrstve. Rozhoduje, čo agent robí. MCP žije na prístupovej vrstve. Definuje, ako agent (postavený s ADK alebo s čímkoľvek iným) siahne po nástroji. Agent v ADK môže byť klientom MCP: keď ADK chce zavolať nástroj a ten nástroj je náhodou vystavený ako MCP server, ADK použije MCP, aby volanie vykonal. Keď je ten istý nástroj obyčajná funkcia v Pythone, ADK zavolá funkciu priamo. MCP je jeden z viacerých spôsobov, ako ADK siaha po nástrojoch, nie konkurent ADK.

Naopak, MCP je jedno, ktorý framework je na druhom konci. MCP server, ktorý dodá váš dátový tím, nevie, či agent, ktorý sa s ním rozpráva, bol postavený s ADK, LangGraphom, CrewAI alebo obyčajnou slučkou v Pythone. Vidí len klienta, ktorý hovorí MCP.

Rovnaká logika platí pre každú zdanlivú debatu „framework verzus protokol“: *Claude Agent SDK verzus MCP*, *LangGraph verzus A2A*, *OpenAI Agents SDK verzus MCP*. Všetky tri sú kategoriálne chyby. Framework robí orchestráciu; protokol robí prístup. Skladajú sa.

> **Opravený mentálny model v jednej vete:** Frameworky sedia na orchestračnej vrstve a rozhodujú, čo agent robí; protokoly sedia na prístupovej vrstve a rozhodujú, ako agent siaha do vonkajšieho sveta. Skladajú sa. Nesúperia.

Užitočná disciplína: keď čítate o novej agentnej technológii, spýtajte sa *na ktorej vrstve toto sedí?* skôr, než si utvoríte názor. Ak neviete odpovedať, ešte tomu nerozumiete dosť dobre. Väčšina zdanlivej zložitosti agentnej krajiny sa vyparí, len čo dokážete každý kúsok zasunúť do vrstvy, kam patrí.

> **Čo si z tejto kapitoly odniesť:** Agentný stack má štyri vrstvy: orchestráciu, LLM, prístup (MCP + A2A), skutočné systémy. Frameworky, modely a protokoly sa skladajú, nesúperia. Jediná najčastejšia chyba v diskusii o vývoji agentov je brať framework (ADK, LangGraph) tak, akoby súperil s protokolom (MCP). Nesúperí. Všetko v tejto brožúre je rozpracovaním tohto obrazu.

---

*Ďalej: [Kapitola 3: Protokolová vrstva](03_protocol_layer.md)*
