# Kapitola 8: Otázka lock-inu

---

Dodávatelia frameworkov hovoria, že modely môžete vymieňať. Nezávislé frameworky hovoria, že nemôžete, alebo presnejšie, že teoreticky áno, ale v praxi nie bez rozbitých funkcií a zhoršeného správania. Kto má pravdu?

Táto kapitola berie otázku vážne, jedného dodávateľa po druhom. Pri každom veľkom dodávateľskom SDK: ak na ňom dnes staviate s predvoleným modelom a zajtra sa rozhodnete model vymeniť, koľko z vášho agenta stále funguje? A čo sa rozbije ako prvé?

Odpoveď je premenlivejšia, než naznačuje abstraktná debata o lock-ine. Niektoré dodávateľské SDK sú takmer naozaj nezávislé od modelu. Niektoré sa ako nezávislé predávajú, ale majú hlboké skryté väzby. Jedno je výslovne natrénované do správania modelu a nemalo by sa nezávislým ani volať. Na nuansách záleží, lebo určujú skutočné inžinierske náklady migrácie, nie teoretické.

**Test poctivosti lock-inu:** ak v tomto frameworku vymením podkladový model, ktoré z hlavných schopností frameworku stále fungujú? Poctivá odpoveď sa pohybuje od „väčšina“ po „takmer žiadna“.

## Google ADK: stredný lock-in (ekosystém, nie model)

Nominálne nezávislý od modelu, a v základnom prípade aj je. Ale tri hlavné schopnosti sa pri výmene zhoršia.

*Multimodalita*: hlboko integrovaná do ADK cez API Gemini. Vymeňte za textový model a stratíte celú triedu prípadov použitia. Vymeňte za multimodálny model od iného dodávateľa a zaplatíte za integračnú prácu na mieru, aby ste dosiahli paritu.

*Generovanie kariet agentov*: ADK automaticky generuje karty A2A na základe správania Gemini pri volaní funkcií. Iné modely produkujú menej predvídateľné výstupy volaní funkcií, čím sú automaticky generované karty menej spoľahlivé. Dá sa to opraviť, ale z automatického sa stane manuálne.

*Integrácie s Vertexom*: najplynulejšie integrácie ADK sú s Vertex AI na nasadenie, BigQuery na dáta, Google Cloud na výpočty. Pri výmene modelu nezmiznú, ale stanú sa menej prirodzenými, ak sa zároveň sťahujete z Google Cloud.

Štruktúra orchestrácie (hierarchický strom agentov, primitíva Sequential/Parallel/Loop, vizuálny debugger) na iných modeloch ďalej funguje, len s viac manuálnej práce na okrajoch.

**Verdikt**: stredný lock-in. Framework samotný je stredne prenositeľný; ekosystém okolo neho nie.

## OpenAI Agents SDK: vysoký lock-in (hostované funkcie)

Čiastočne nezávislý. SDK sa dá namieriť na modely mimo OpenAI cez smerovacie proxy ako LiteLLM. Mechanizmus existuje. Čo sa pri výmene rozbije:

*Hostované nástroje*: webové vyhľadávanie, vyhľadávanie v súboroch, interpret kódu sú hostované u OpenAI. Zmiznú v okamihu, keď vymeníte poskytovateľa.

*Vykonávanie v sandboxe*: spravovaný sandbox na vykonávanie kódu beží na infraštruktúre OpenAI. Vymeňte poskytovateľa a buď sandbox stratíte, alebo si ho za netriviálne náklady postavíte sami.

*Spoľahlivosť odovzdávania*: mechanizmus odovzdávania sa spolieha na spoľahlivosť štruktúrovaného výstupu a volania funkcií u OpenAI. Iné modely štruktúrovaný výstup zvládajú, ale nie vždy s rovnakým profilom spoľahlivosti. Jemné zmeny môžu predtým fungujúce odovzdávania urobiť nestálymi.

*Hlas a Realtime API*: špecifické pre OpenAI. Hlasové prípady použitia sú fakticky iba pre OpenAI.

Základné primitíva agentov a odovzdávania na iných modeloch ďalej fungujú. Jednoduchí textoví agenti s vlastnými nástrojmi bežia na modeloch mimo OpenAI s miernym trením.

**Verdikt**: vysoký lock-in, ale skôr o *hostovaných funkciách* než o *správaní modelu*. Ak nepoužívate hostované nástroje, sandbox ani hlas, SDK je prenositeľnejšie než jeho povesť. Ak áno (a väčšina presvedčivých prípadov použitia OpenAI SDK *áno*), náklady na migráciu sú podstatné.

## Claude Agent SDK: veľmi vysoký lock-in (správanie modelu)

Nie je nezávislý a Anthropic nepredstiera opak. SDK sa volá podľa Clauda, je postavené okolo tréningu Clauda, predpokladá Clauda pod sebou.

*Vernosť ovládania počítača*: Claude bol špecificky trénovaný na úlohy ovládania počítača (čítanie obrazoviek, spúšťanie príkazov, navigácia v súborových systémoch). Iné modely rovnocenný tréning nemali. Spustenie pracovných postupov Claude Agent SDK cez model iný než Claude produkuje nepredvídateľný výstup: halucinované súradnice na obrazovke, nepochopenú sémantiku Bashu, zlyhanú manipuláciu so súbormi.

*Zabudované nástroje*: osem nástrojov (Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch) je navrhnutých okolo vzorov promptov, na ktoré Claude dobre reaguje. S inými modelmi fungujú, ale presnosť a bezpečnosť sa citeľne zhoršia.

*Správanie v dlhých sedeniach*: kompakcia kontextu Clauda je natrénovaná do modelu. Iné modely zvládajú dlhé kontexty inak, niekedy horšie.

*Háčiky a podagenti*: tieto štrukturálne primitíva fungujú s akýmkoľvek modelom, ale prínos závisí od spoľahlivosti modelu pri dodržiavaní kontraktov háčikov, čo je tréning špecifický pre Clauda.

**Verdikt**: najhlbší lock-in zo všetkých frameworkov v tejto kapitole, a úprimne, je to zámer. Nie generický agentný framework, ktorý náhodou pochádza z Anthropicu. Framework postavený špecificky na využitie tréningu Clauda. Vyberiete si ho a vyberáte si Clauda. To je rozumná stávka, ak ste to rozhodnutie už urobili; je to zlá stávka, ak potrebujete prenositeľnosť.

## AWS Strands: cloudový lock-in, flexibilita modelov

Obrátene. Používa Bedrock na prístup k modelom, čo znamená natívnu podporu Clauda, Llamy, Mistralu a ďalších modelov hostovaných v Bedrocku.

*Výmena v rámci Bedrocku je relatívne bezbolestná*: jedna z najsilnejších návrhových vlastností Strands. Chcete pustiť toho istého agenta dnes na Claude a zajtra na Llame? Strands to podporuje elegantnejšie než ktorékoľvek SDK dodávateľa základných modelov.

*Výmena mimo Bedrocku framework rozbije.* Cena je na cloudovej vrstve, nie na modelovej. Strands predpokladá Bedrock na modely, Lambdu na nástroje, DynamoDB na stav. Odíďte z AWS a prepisujete nasadenie od nuly.

**Verdikt**: obrátený lock-in oproti frameworkom dodávateľov základných modelov. Flexibilný na modeli (v rámci Bedrocku), uzamknutý na cloude (AWS). Pre podniky natívne v AWS často najlepšia voľba v kategórii dodávateľských frameworkov. Pre podniky prenositeľné medzi cloudmi najhoršia.

## Azure AI Foundry Agent Service: lock-in do ekosystému Microsoftu

Čiastočne nezávislý od modelu. Opiera sa o modely OpenAI cez partnerstvo s Microsoftom, ale existujú aj možnosti mimo OpenAI.

*Integrácie s Microsoft 365*: SharePoint, Teams, Outlook, celý povrch M365. Hlavný dôvod, prečo ste si službu vybrali. Nezávisia od konkrétneho modelu, ale mimo ekosystému Microsoftu sú nanič.

*Súlad a identita*: podniková compliance infraštruktúra Microsoftu je vlastnosťou služby. Pri výmene modelu ju nestratíte, stratíte ju úplne pri odchode z Azure.

*Spravované behové prostredie*: beží na Azure. Spravovaná služba sa neprenesie.

**Verdikt**: lock-in do ekosystému, nie do modelu. Cenný do tej miery, do akej ste upísaní podnikovému ekosystému Microsoftu. Ak ste, je to vlastnosť. Ak sa snažíte ostať neutrálni, je to pasca.

## Zhrnutie

| Framework | Nominálne | Skutočná hĺbka | Čo sa pri výmene modelu rozbije prvé |
|---|---|---|---|
| Google ADK | Áno | Stredná (ekosystém) | Multimodalita, automatické karty A2A, integrácie s Vertexom |
| OpenAI Agents SDK | Čiastočne | Vysoká (hostované funkcie) | Hostované nástroje, sandbox, hlas, spoľahlivosť odovzdávania |
| Claude Agent SDK | Nie | Veľmi vysoká (správanie modelu) | Ovládanie počítača, zabudované nástroje, správanie v dlhých sedeniach |
| AWS Strands | Áno v rámci Bedrocku | Cloudový lock-in | Odíde z AWS a neprežije nič |
| Azure AI Foundry Agent Service | Čiastočne | Ekosystém Microsoftu | Integrácie s M365, behové prostredie Azure |
| LangGraph | Áno | Nízka | Minimálne, to je cieľ návrhu |
| CrewAI | Áno | Nízka | Minimálne, to je cieľ návrhu |

## Lock-in nie je vždy problém

Kým vyhlásime všetky dodávateľské frameworky za diskvalifikované, symetrický bod. Lock-in nie je automaticky zlý. Je to obchod.

Podniky, ktoré sa v roku 2010 uzamkli do AWS, mali v roku 2018 drahšiu migráciu než podniky, ktoré od prvého dňa používali Kubernetes. Zároveň dodávali rýchlejšie v rokoch 2010, 2011, 2012, 2013, 2014 a počas tých rokov zachytili biznisovú hodnotu, o ktorej prenositeľnejšie podniky ešte stále písali architektonické dokumenty. V mnohých prípadoch sa výhoda rýchlosti úročila rýchlejšie, než sa hromadili náklady lock-inu.

Rovnaká logika platí dnes. Podnik, ktorý si v roku 2026 vyberie OpenAI Agents SDK a do 2. kvartálu 2027 dodá troch agentov pre zákazníkov, zachytil hodnotu, ktorú podnik stále sa hádajúci o LangGraph verzus CrewAI nezachytil. Ak bude prípadná migrácia z OpenAI drahá (a môže byť), je to budúci náklad, ktorý treba vážiť oproti súčasnému prínosu.

**Otázka lock-inu, poctivo položená, neznie „bude to niečo stáť?“ Odpoveď je áno. Otázka znie „ako sa náklady tejto budúcej migrácie porovnávajú s hodnotou, ktorú medzitým zachytím?“** Pre mnohé podniky matematika vychádza priaznivo. Pre iné (najmä regulované, kde budúca migrácia môže byť nedobrovoľná a naliehavá) vychádza nepriaznivo a mali by investovať do prenositeľnosti od prvého dňa.

## Kedy sa lock-in stáva štrukturálnym

Štyri podmienky prevážia matematiku v prospech toho, že prenositeľnosť stojí za svoje náklady.

**Regulačné riziko vynútenej migrácie.** Nová regulácia by vás vierohodne mohla prinútiť odísť od konkrétneho dodávateľa. Prenositeľnosť potrebujete *pred* reguláciou, nie po nej.

**Cenová sila dodávateľa.** Vaša záťaž sa stane závislou od jediného dodávateľa a ten môže jednostranne zdvihnúť ceny. Odovzdali ste svoju maržu. Prenositeľnosť je páka.

**Strategický význam záťaže.** Nasadenie, na ktorom stojí firma, má vyššie migračné riziko než automatizácia oddelenia. Čím vyššie na spektre kritickosti pre biznis, tým viac stojí poistka prenositeľnosti za to.

**Dátová suverenita.** Vaše regulačné prostredie môže vyžadovať suverénnu infraštruktúru. Dodávateľské frameworky, ktoré pod sebou predpokladajú vlastnú infraštruktúru, sa stanú záťažou.

Mimo týchto podmienok je lock-in u dodávateľa skutočný, ale zvládnuteľný náklad. Vnútri nich sú náklady strategické, nie prevádzkové, a strategické náklady sú tie, ktoré posadia generálnych riaditeľov na nepríjemné zasadnutia predstavenstva.

> **Čo si z tejto kapitoly odniesť:** „Nezávislý od modelu“ v marketingu dodávateľských frameworkov zvyčajne znamená „model technicky môžete vymeniť“, nie „hlavné schopnosti frameworku výmenu prežijú“. Lock-in sa pohybuje od nízkeho (LangGraph, CrewAI) cez stredný (ADK) a vysoký (OpenAI Agents SDK) po veľmi vysoký (Claude Agent SDK). AWS a Azure vzor obracajú: flexibilné na modeli, uzamknuté na cloude. Pre väčšinu podnikov je lock-in u dodávateľa cena, ktorú stojí za to zaplatiť za rýchlosť, kým nie, a podmienky, za ktorých nie, sú regulačné riziko, cenová sila dodávateľa, kritickosť záťaže a dátová suverenita. Vedzte, ktoré z nich sa vás týkajú, kým sa zaviažete.

---

*Ďalej: [Kapitola 9: Európsky uhol](09_eu_angle.md)*
