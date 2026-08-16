# Kapitola 5: Dodávateľské frameworky

---

Každý veľký dodávateľ AI dnes dodáva framework na vývoj agentov. Google má ADK. OpenAI má Agents SDK. Anthropic má Claude Agent SDK. AWS má Strands. Microsoft má Azure AI Foundry Agent Service. V cloudových pojmoch je každý z nich niečo blízke platforme ako službe: názorovo vyhranené prostredie, v ktorom je stavanie agentov mimoriadne rýchle, pokiaľ ostanete v oplotenej záhrade dodávateľa.

Táto kapitola je prehliadka. Pri každom frameworku: filozofia návrhu, v čom je naozaj dobrý a aký gravitačný ťah vyvíja smerom k svojmu materskému dodávateľovi. Porovnania funkcia po funkcii zastarajú za týždne. Stabilné je to, *aký druh nástroja každý framework je* a *akú stávku robíte, keď si ho vyberiete*. Kapitola 8 rieši otázku nákladov na prechod priamo; tu sú frameworky opísané samy za seba.

## Google ADK

Hierarchické stromy agentov. Koreňový agent prijme požiadavku používateľa a deleguje ju podagentom, ktorí môžu delegovať ďalej. Vykonávanie riadia štrukturálne primitíva, ktoré ADK volá Sequential, Parallel a Loop agenti. Systém agentov je strom; framework ten strom spúšťa.

Tri skutočné silné stránky. **Vizuálne ladenie**: ADK sa dodáva s CLI a webovým rozhraním, kde sa so svojím agentom rozprávate, sledujete jeho vnútorné uvažovanie a krokujete vykonávanie. Pri zložitých multiagentných nasadeniach jedna z lepších vývojárskych skúseností na trhu. **Natívna podpora A2A**: ADK automaticky generuje karty agentov a stará sa o inštalatérčinu protokolu. Ak máte na cestovnej mape multiagentnú prácu naprieč hranicami, ADK vám dá najhladší nájazd. **Multimodálna schopnosť**: agenti v ADK natívne spracúvajú obrázky, zvuk a video cez multimodálne API Gemini, čo otvára prípady použitia ako vizuálna inšpekcia, hlasová zákaznícka podpora a porozumenie dokumentom.

Gravitačný ťah: Gemini, Vertex AI, BigQuery, Google Cloud. Technicky nezávislý od modelu, ale každý trecí bod v ekosystéme potichu ukazuje späť na Gemini. To nie je kritika; dodávateľské frameworky to majú robiť.

**Berte ADK vážne, ak** už ste na Google Cloud, uprednostňujete viacero agentov s komunikáciou naprieč hranicami, máte zmysluplne multimodálne prípady použitia alebo zistíte, že vizuálne ladenie vás zrýchľuje viac, než vás názory frameworku spomaľujú.

## OpenAI Agents SDK

Výslovne proti grafom. Kde LangGraph chce, aby ste nakreslili stavový automat, OpenAI chce, aby ste definovali malý počet agentov, každého s jasnou špecializáciou, a nechali ich podľa potreby odovzdávať si prácu. Mentálny model: tím špecialistov s recepčnou, ktorá smeruje hovory, nie vývojový diagram. Štyri primitíva: Agents, Tools, Handoffs, Guardrails. To je celý slovník.

Silné stránky. **Rýchlosť vývojára**: rýchlo sa učí, rýchlo sa číta, rýchlo sa udržiava. Pre tím, ktorý chce architektúru agenta, ktorá sa zmestí do jedného súboru, framework, ktorý najviac rešpektuje váš čas. **Hostované nástroje a sandboxing**: webové vyhľadávanie, vyhľadávanie v súboroch, interpret kódu bežia na infraštruktúre OpenAI bez nastavovania. Pre agentov, ktorí potrebujú písať a spúšťať kód, je spravovaný sandbox skutočný rozdiel. **Hlas a multimodalita**: Realtime API je prvotriedne, multimodalita GPT-4o je vystavená čisto.

Gravitačný ťah: modely OpenAI, hostovaná infraštruktúra, spoľahlivosť štruktúrovaného výstupu vyladená pre OpenAI. Vymeňte modely cez smerovacie knižnice a zachováte si sémantiku riadiaceho toku, ale stratíte väčšinu spravovanej infraštruktúry, ktorá robila framework príťažlivým.

**Berte ho vážne, ak** ste upísaní modelom OpenAI, záleží vám na hlase alebo vykonávaní kódu a chcete najrýchlejšiu možnú cestu od konceptu k bežiacemu agentovi bez architektonických ceremónií.

## Claude Agent SDK

Iný prístup. Postavený na predpoklade, že agent bude pôsobiť v prostredí podobnom počítaču: čítať súbory, spúšťať shellové príkazy, písať kód, prehľadávať web. Dodáva sa s ôsmimi zabudovanými nástrojmi hneď z krabice (Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch). Mentalita návrhu: dajte agentovi počítač a nechajte ho pracovať.

Model orchestrácie: **háčiky a podagenti**. Háčiky zachytávajú udalosti životného cyklu („pred volaním nástroja“, „po odpovedi modelu“), takže môžete vynucovať mantinely alebo sledovať správanie. Podagenti delegujú úlohy detským agentom s vlastnými sadami nástrojov a pokynmi. Kde OpenAI organizuje prácu odovzdávaním medzi rovnocennými, Claude ju organizuje delegovaním deťom.

Silné stránky. **Dlho bežiaca autonómna práca**: úlohy, ktoré trvajú hodiny alebo dni, nie sekundy. Kompakcia kontextu, kontrolné body stavu, asynchrónne vykonávanie sú zapečené dnu. Pre „prejdi túto kódovú základňu a vypracuj plán migrácie“ alebo „analyzuj tikety za posledný rok a navrhni päť najlepších kandidátov na automatizáciu“ je to framework, ktorý dlho bežiaci tvar zvláda najprirodzenejšie. **Zabudovaná sada nástrojov**: osem nástrojov znamená, že agenti začínajú so skutočnými schopnosťami, nie s prázdnymi registrami. Zmysluplný náskok pre prípady použitia typu vývojársky asistent. **Háčiky ako riadiaci povrch**: presná kontrola nad správaním agenta v bodoch životného cyklu, čo podniky oceňujú z dôvodov súladu a pozorovateľnosti. Novší prírastok, Agent Skills (priečinky s pokynmi, skriptmi a zdrojmi, ktoré si agent načíta na požiadanie), vyšiel začiatkom roka 2026 ako otvorený štandard a dáva SDK prenositeľný spôsob balenia procedurálnych znalostí.

Gravitačný ťah: toto je najhlbšia väzba v kategórii dodávateľských frameworkov. Claude bol špecificky trénovaný na úlohy ovládania počítača (súborové systémy, shellové príkazy, prehliadače). Iné modely nemajú rovnocenný tréning. Spustiť to isté SDK cez model iný než Claude dáva citeľne horšie výsledky. To je behaviorálna väzba na úrovni modelu, nie iba príslušnosť k ekosystému.

**Berte ho vážne, ak** staviate inžiniersky náročné záťaže (asistenti na programovanie, agenti na správu systémov), dlho bežiace autonómne úlohy a chcete framework so skutočnými názormi na bezpečnosť ovládania počítača.

## AWS Strands

Najmladší z piatich, hoci už nie experiment, ako ktorý sa spúšťal: Strands je dnes produkčné SDK v strede Amazon Bedrock AgentCore, spravovaného agentného behového prostredia AWS, kým špičkový výskum sa presunul do samostatnej organizácie Strands Labs. Návrhová stávka sa nezmenila. Silne sa oprieť o to, že LLM riadi, namiesto toho, aby sa obmedzoval. Kde vás LangGraph núti definovať hrany v grafe, Strands vás núti definovať ciele v prirodzenom jazyku a spolieha sa na to, že model rozhodne, ako ich dosiahnuť. Stávka, že modely sú dnes dosť schopné na to, aby zvládli orchestráciu autonómne, a úlohou frameworku je poskytnúť bezpečné vykonávanie + integráciu s AWS, nie vnucovať riadiaci tok.

Silné stránky. **Integrácia s AWS**: hlboké prepojenie na Bedrock (modely), Lambdu (nástroje), DynamoDB (stav). Ak je vaša infraštruktúra natívne v AWS, Strands odstráni veľa inštalatérčiny. **Flexibilita v rámci Bedrocku**: natívny prístup ku Claude, Llame, Mistralu a ďalším; väčšia flexibilita modelov než pri frameworkoch dodávateľov základných modelov, *v rámci obmedzenia, že na prístup k modelom používate Bedrock*. **Spravované behové prostredie**: AgentCore obaľuje agentov v Strands spravovanými sedeniami, pamäťou, identitou a pozorovateľnosťou, takže medzera medzi prototypom a produkciou je nezvyčajne krátka. Experimentálne primitíva („AI Functions“ a ich príbuzní) dnes žijú v Strands Labs, jasne oplotené od produkčného SDK.

Gravitačný ťah: infraštruktúra AWS, nie jediný model. Obrátený lock-in oproti frameworkom dodávateľov základných modelov.

**Berte ho vážne, ak** je ťažiskom vašej infraštruktúry AWS a flexibilita modelov sprostredkovaná Bedrockom je pre vás konkrétne užitočná.

## Microsoft Azure AI Foundry Agent Service

Agentný príbeh Microsoftu má dve vrstvy. Open-source vrstva je Microsoft Agent Framework, zjednotenie multiagentných výskumných vzorov z AutoGenu s podnikovou inštalatérčinou Semantic Kernelu (verziu 1.0 dosiahol v apríli 2026). Spravovaná vrstva je Azure AI Foundry Agent Service, ktorá tieto vzory spúšťa v produkcii a kladie dôraz na integráciu s podnikovým ekosystémom Microsoftu: agenti, ktorých spúšťajú udalosti v Azure, čítajú SharePoint, píšu do Teams, koordinujú sa s kopilotmi v Microsoft 365.

Silné stránky. **Šírka integrácie**: pre organizácie na Microsoft 365, Dynamics, SharePointe, Power Platform hĺbka, ktorej sa žiadny iný framework nevyrovná. **Postoj k identite a súladu**: natívne zdedené desaťročia podnikovej compliance infraštruktúry Microsoftu. SSO, podmienený prístup, audítorské stopy, rezidencia dát, podpora suverénneho cloudu, všetko od prvého dňa. **Prevzaté vzory z AutoGenu**: multiagentné konverzačné vzory (debata, konsenzus, hierarchická koordinácia) prenesené z open-source výskumu Microsoftu do Agent Frameworku a spravovanej služby nad ním.

Gravitačný ťah: ekosystém Microsoftu. Predvolený model je OpenAI cez partnerstvo, predvolené behové prostredie je Azure, predvolené integrácie sú Microsoft 365. Ak žijete v tom svete, framework vás zrýchli; ak nie, platíte za integrácie, ktoré nevyužijete.

**Berte ho vážne, ak** ste organizácia postavená na Microsofte, potrebujete jeho postoj k súladu alebo staviate agentov, ktorí intenzívne pracujú s dátami a pracovnými postupmi v Microsoft 365.

## Zhrnutie

| Framework | Ponuka v jednej vete |
|---|---|
| Google ADK | Špičkové multiagentné + A2A, najlepšie ladenie, hlboký ťah ku Gemini/GCP |
| OpenAI Agents SDK | Najrýchlejšia cesta od nuly k bežiacemu agentovi, ekosystém OpenAI, model odovzdávania |
| Claude Agent SDK | Najsilnejší príbeh ovládania počítača a dlho bežiacich úloh, najhlbšia väzba na model |
| AWS Strands | Natívne pre AWS, flexibilita modelov cez Bedrock, spravované prostredie AgentCore |
| Azure AI Foundry Agent Service | Najhlbšia integrácia s Microsoft 365, najsilnejší postoj k podnikovému súladu |

Každý je rozumná voľba pre organizáciu, pre ktorú bol postavený. Žiadny nie je rozumná voľba pre každú organizáciu.

> **Čo si z tejto kapitoly odniesť:** Dodávateľské frameworky sú PaaS agentnej éry: názorovo vyhranené, rýchle a hlboko zarovnané s dodávateľom, ktorý ich postavil. Každý má skutočnú silnú stránku a konkrétny gravitačný ťah. Správna voľba závisí od toho, v ktorom ekosystéme už žijete a koľko prenositeľnosti vymeníte za rýchlosť. Kapitola 8 rieši dôsledky lock-inu pre jednotlivých dodávateľov; táto kapitola ustanovila, čím každý framework je sám za seba.

---

*Ďalej: [Kapitola 6: Nezávislé frameworky](06_agnostic_frameworks.md)*
