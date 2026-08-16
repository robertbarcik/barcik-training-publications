# Kapitola 3: Protokolová vrstva: MCP a A2A

---

Na prístupovej vrstve agentného stacku sedia dva protokoly. MCP obsluhuje premávku agent–nástroj a agent–dáta. A2A obsluhuje premávku agent–agent. Sú to rovnocenné štandardy a takmer každý podnikový architektonický rozhovor o agentoch sa nakoniec vráti k jednému alebo obom.

MCP je ustálené. A2A je tesne za ním, na okrajoch ešte tuhne. Táto kapitola pokrýva oba.

## MCP: HTTP agentnej éry

Väčšina technologických štandardov strávi roky v chaotickom medziobdobí, keď súperiace protokoly bojujú o prijatie. MCP ho malo nezvyčajne krátke. Oznámené Anthropicom na konci roka 2024, dostalo sa od „zaujímavého open-source návrhu“ k „faktickému štandardu odvetvia“ približne za osemnásť mesiacov.

Začiatkom roka 2026 sa s číslami ťažko háda: vyše 97 miliónov stiahnutí SDK mesačne naprieč implementáciami v Pythone a TypeScripte, vyše 10 000 verejne indexovaných MCP serverov, natívna podpora v Claude, ChatGPT, Cursore, v každom väčšom IDE s AI funkciou a v každom frameworku, ktorý táto brožúra pokrýva. V decembri 2025 Anthropic daroval MCP nadácii Linux Foundation, ktorá na jeho správu vytvorila Agentic AI Foundation, spoluzaloženú Anthropicom, Blockom a OpenAI, s ďalšou podporou od Googlu, Microsoftu, AWS, Cloudflare a Bloombergu. To nie je zostava sporného štandardu. To je zostava ustáleného.

Porovnanie, po ktorom siahajú všetci, je HTTP. Je to dobré porovnanie. HTTP tiež nie je niečo, čo si „vyberáte“; je to všadeprítomný protokol, ktorý dovolí akémukoľvek prehliadaču dosiahnuť akýkoľvek server. MCP sa tým stáva pre agentov: všadeprítomným protokolom, ktorý dovolí akémukoľvek agentovi dosiahnuť akýkoľvek nástroj alebo zdroj dát. Čoraz častejšie je *ne*podporovať ho drahšie než podporovať.

### Čo MCP v skutočnosti štandardizuje

Tri veci, nie jednu. Podniky, ktoré ho berú ako jednoduchú API bránu, prídu o väčšinu hodnoty.

**Nástroje**: spustiteľné funkcie, ktoré môže agent vyvolať. Nástroj má názov, krátky popis, vstupnú schému s popismi jednotlivých polí a štruktúrované chybové odpovede. Agent zavolá `tools/list`, aby videl katalóg, a potom `tools/call`, aby vyvolal konkrétny nástroj s argumentmi. Dôležité návrhové rozhodnutie je, že popisy nástrojov sú písané pre jazykový model, ktorý o nich uvažuje, nie pre človeka, ktorý číta dokumentáciu. Dobre navrhnutý MCP server má bližšie k promptovo vyladenému API než ku konvenčnému REST endpointu; jazyková kvalita popisov nástrojov je súčasťou správnosti servera.

**Zdroje**: dáta len na čítanie, ktoré server sprístupňuje. Dokumenty, riadky databázy, konfiguračné súbory, znalosti o politikách. Agent zdroj „nevolá“; načíta si ho a vloží obsah do vlastného kontextu. Pri podnikových nasadeniach na zdrojoch často záleží viac než na nástrojoch. Interný bot o firemných politikách chce strom zdrojov (`policies/hr/parental-leave.md`, `policies/security/acceptable-use.md`), ktorý môže agent prehliadať a čerpať z neho, nie nástroj `get_policy_document(id)`, pri ktorom musí hádať, ako ho vyvolať.

**Prompty**: znovupoužiteľné šablóny promptov, ktoré server ponúka klientom. Najmenej používaná z troch, ale dôvod jej existencie je principiálny: nástroje sú veci, ktoré sa robia, zdroje sú veci, ktoré sa čítajú, prompty sú veci, ktoré sa hovoria. Úplný MCP server môže ponúkať všetky tri.

### Podanie rúk

MCP je protokol klient–server nad malým slovníkom JSON-RPC. Prvotné pripojenie urobí jedno kolo vyjednávania (`initialize`): verzia protokolu, schopnosti, identita. Potom sú to už len volania metód: `tools/list`, `tools/call`, `resources/list`, `resources/read`, `prompts/list`, `prompts/get`. Slovník je malý zámerne. Väčšina zaujímavej návrhovej práce sa deje vnútri servera (ako modelujete svoju doménu, ako píšete popisy nástrojov, ako navrhujete strom zdrojov), nie v protokole samotnom.

### Ako MCP vyzerá v podniku

Tvar je takmer vždy rovnaký. Hŕstka interných MCP serverov sedí pred existujúcimi systémami: CRM, ticketovacia platforma, dátový sklad, interná znalostná báza, systém identít. Každý server udržiava tím, ktorý vlastní podkladový systém, lebo ten tím najlepšie rozumie sémantike domény. Ľubovoľný počet agentov (postavených na akomkoľvek frameworku, s akýmkoľvek modelom) sa pripája ako MCP klienti.

To dáva tri vlastnosti podnikovej triedy, ktoré vysvetľujú väčšinu krivky prijatia. Po prvé: znovupoužitie naprieč agentmi (jeden server, mnoho spotrebiteľov, dramaticky lepšie než svet pred MCP, kde každý agent integroval každý backend osobitne). Po druhé: znovupoužitie naprieč frameworkmi (prejdite budúci rok z LangGraphu na ADK a servery sa meniť nemusia). Po tretie: správa nadáciou (žiadny jednotlivý komerčný záujem nemôže rozbiť kompatibilitu ani zmeniť licencovanie).

### Cestovná mapa 2026: pripravenosť pre podniky

Cestovná mapa Agentic AI Foundation na rok 2026 uvádza štyri prioritné oblasti a prvou je výslovne pripravenosť pre podniky. Konkrétne: **integrácia identity a prístupu** (OAuth 2.1, podnikové SSO, tokeny s obmedzeným rozsahom), **správa a pozorovateľnosť** (správanie brán, audítorské stopy, administrátorské konzoly) a **prenositeľnosť transportu a konfigurácie** (streamovanie, rušenie, odolnosť v podmienkach podnikových sietí).

Podtext je, že MCP sa vedome pretvára z vývojárskeho protokolu na podnikový protokol. Je to ten istý prechod, akým prešlo HTTP v rokoch 1993 až 1999, stlačený približne do jedného roka.

### Čo MCP nerobí

MCP je zámerne hlúpe v mnohých veciach. Neorchestruje; nevie, ktorý nástroj zavolať, v akom poradí, ani čo robiť pri zlyhaní. To je práca orchestračnej vrstvy. Samo osebe neautentifikuje koncových používateľov; model autentifikácie je rozhodnutie podnikového nasadenia. Nerieši komunikáciu agent–agent; to je A2A, nižšie. A nenahrádza vaše existujúce API; sedí pred nimi.

Jedna predpoveď stojí za výslovné vyslovenie: o osemnásť mesiacov, ak máte netriviálnu internú platformu, budete pred ňou takmer určite mať MCP servery, napísané vaším vlastným tímom, udržiavané ako súčasť bežnej platformovej inžinierskej práce. Externí dodávatelia dodajú MCP servery pre svoje vlastné produkty (GitHub, Linear, Notion to už robia), ale vaše interné systémy sú na vás. Umenie podnikovej triedy písať dobré MCP servery (tesné rozhrania nástrojov, presné popisy, silná autentifikácia, čisté hierarchie zdrojov) je vznikajúce remeslo platformového inžinierstva, ktoré pred dvoma rokmi neexistovalo. Ak si chcete túto intuíciu vybudovať prakticky, existuje bezplatný spoločník: [github.com/robertbarcik/MCP-tutorial](https://github.com/robertbarcik/MCP-tutorial) prechádza pojmy tejto kapitoly v kóde.

> **Poznámka z júla 2026.** Cestovná mapa pripravenosti pre podniky vyššie prichádza načas. Revízia špecifikácie, ktorá pristáva 28. júla (už zverejnená ako kandidát na vydanie), je najväčšia od spustenia MCP: bezstavové jadro, ktoré škáluje nad obyčajným HTTP, spevnené zosúladenie s OAuth a OIDC pre podnikových poskytovateľov identity a dve oficiálne rozšírenia, MCP Apps pre používateľské rozhranie vykresľované serverom a Tasks pre dlho bežiacu prácu. Nič v tejto časti sa tým nemení; protokol robí to, čo ustálené protokoly robia, čiže nudnú inštalatérsku prácu.

## A2A: ten druhý protokol

Ak MCP odpovedá na otázku „ako sa môj agent rozpráva s nástrojom“, A2A odpovedá na otázku „ako sa môj agent rozpráva s iným agentom“. To sú dva smery premávky na prístupovej vrstve a zaslúžia si symetrickú pozornosť. Väčšina podnikových projektov sa najprv sústredí na nástroje a dáta, lebo tam žijú okamžité výhry. Komunikácia agent–agent znie ako problém budúcnosti, kým sa niekde okolo dvanásteho agenta, ktorého organizácia postaví, neprestane byť problémom budúcnosti a nestane sa naliehavou.

### Prečo sa stane naliehavou rýchlejšie, než tímy čakajú

Špecializácia: univerzálny agent podpory narazí na svoje limity a tím z neho vyčlení špecialistu na fakturáciu, technického špecialistu, špecialistu na súlad. Organizačné hranice: obchod postaví obchodného agenta, HR postaví HR agenta, financie postavia finančného agenta, a keď sa obchodník spýta na politiku provízií, tí traja musia spolupracovať. Externí partneri: agent dodávateľa vyjednáva s vaším nákupným agentom a jediný životaschopný spôsob, ako môžu spolupracovať, je otvorený protokol. Skladanie: vzor mikroslužieb sa prehráva znova na úrovni agentov a systémy agentov potrebujú protokol.

### Čo A2A robí

Tri veci. **Objavovanie schopností**: agent kompatibilný s A2A inzeruje „kartu agenta“, ktorá opisuje, čo vie robiť, aké vstupy očakáva, aké výstupy produkuje, ako sa autentifikovať. **Delegovanie úloh**: štruktúrovaný spôsob odovzdania úlohy, ktorý podporuje synchrónnu výmenu požiadavka–odpoveď aj dlhšie asynchrónne interakcie so streamovaným priebehom. **Autentifikácia a dôvera**: háčiky na prenášanie autentifikačného kontextu cez delegovanie, aby mohli nadväzujúci agenti robiť vlastné autorizačné rozhodnutia, namiesto slepého dôverovania tomu, kto je pred nimi. Tretí bod je ten, ktorý podniky podceňujú. Volania medzi agentmi môžu prekračovať organizačné, ba aj firemné hranice, a otázka, čia právomoc sa vykonáva na ktorom kroku, sa stáva zaujímavou.

### Kde A2A sedí v krajine

Chaotickejšie než pri MCP. **Google ADK má natívnu podporu A2A** a automaticky generuje karty agentov, čo je jeden z najsilnejších dôvodov, prečo brať ADK vážne pre multiagentné architektúry. **CrewAI tiež podporuje A2A**, čo odráža jeho dizajn zameraný v prvom rade na viac agentov. **LangGraph, OpenAI Agents SDK, Claude Agent SDK** majú čiastočnú alebo vznikajúcu podporu; všetky tri majú zverejnené položky v cestovnej mape.

Potenciálni rivali sa väčšinou pridali. Agent Communication Protocol od IBM sa v septembri 2025 zlúčil do A2A a Google daroval A2A nadácii Linux Foundation, kde teraz sedí pod tou istou strechou Agentic AI Foundation ako MCP. Na svoje prvé výročie v apríli 2026 protokol počítal vyše 150 členských organizácií, produkčné použitie v Microsofte, AWS, Salesforce, SAP a ServiceNow a vydanie 1.2 s kryptograficky podpísanými kartami agentov. Nad ním sa už formuje platobná vrstva: Agent Payments Protocol (AP2), podporovaný Googlom, Coinbase, Mastercardom a PayPalom, štandardizuje, ako agenti prevádzajú peniaze, s kryptografickými mandátmi dokazujúcimi, že nákup schválil človek.

Naše čítanie v apríli 2026: A2A je vedúci kandidát, ale ešte nie jednoznačný konsenzus, akým je MCP. Rozumná stávka pre väčšinu podnikov je navrhovať s A2A na mysli, brať protokoly medzi agentmi ako oblasť, kde môže byť v roku 2027 potrebné niečo prerobiť, a vyhnúť sa budovaniu vlastného proprietárneho variantu.

### Čo robiť s A2A dnes

Väčšina podnikov by do infraštruktúry A2A zatiaľ **nemala** nadmerne investovať. Ak staviate svojho prvého agenta, sústreďte sa na MCP, sústreďte sa na orchestračnú vrstvu a A2A berte ako niečo, čo prijmete, keď sa stane relevantným. Predčasné A2A zvyčajne znamená navrhovať multiagentný systém skôr, než má biznis preň prípad použitia.

**Nevylúčte A2A náhodou.** Keď si vyberáte framework, pozrite sa, ako je na tom s A2A. Framework bez dôveryhodnej cestovnej mapy pre A2A je tichá stávka, že na multiagentnej architektúre pre váš prípad použitia nezáleží. Obhájiteľné pre jednoúčelového agenta; riskantné pre platformu.

**Začnite písať karty agentov.** Aj bez formálneho A2A je zvyk zdokumentovať pre každého agenta, ktorého postavíte, čo robí, čo potrebuje a čo vracia, užitočná disciplína. Tú disciplínu je lacné neskôr formalizovať.

> **Čo si z tejto kapitoly odniesť:** MCP je ustálený protokol pre prístup agent–nástroj a agent–dáta. A2A je vznikajúci protokol pre komunikáciu agent–agent, menej ustálený, ale získavajúci konsenzus. Oba žijú na prístupovej vrstve stacku, pod orchestračnou vrstvou. Berte MCP ako všadeprítomnú infraštruktúru: konzumujte dodávateľské servery, stavajte vlastné pre interné systémy. Berte A2A ako architektonickú otázku, ktorú budete riešiť, keď sa multiagentné potreby stanú skutočnými, ale vyberajte si frameworky s dôveryhodnou cestovnou mapou pre A2A, aj keď ste dnes pri jednom agentovi.

---

*Ďalej: [Kapitola 4: Orchestračná vrstva](04_orchestration_layer.md)*
