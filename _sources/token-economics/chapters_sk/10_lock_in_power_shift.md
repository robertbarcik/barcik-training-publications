# Kapitola 10: Posun moci pri lock-ine

> **V skratke**
>
> - Lock-in kedysi prial vám: prostredie klienta bolo zložité a vy ste boli tí, čo ho poznali. S GenAI lock-in migruje k dodávateľom modelov: prompty, schémy nástrojov, hodnotiace pipeline, doladenia.
> - Vaša obrana je architektonická: vlastnite abstrakčnú vrstvu, integračnú vrstvu a dátovú vrstvu, z návrhu nezávislé od modelu.
> - Schopnosť prepnúť je nová hodnotová ponuka: ak viete za pár dní vymeniť Claude za GPT-4.1 za Gemini, držíte vyjednávaciu silu, ktorú váš klient potrebuje.
> - Cieľ sa posúva od pasívnej nenahraditeľnosti (odísť od vás je bolestivé) k aktívnej nenahraditeľnosti (váš prínos je viditeľný a meraný).
>
> **Číslo, ktoré si zapamätať:** jedno popoludnie, toľko potrebuje kompetentný vývojár na integráciu LLM API. Všetko, čo účtujete, musí túto latku prekonať.

Každý poskytovateľ IT služieb rozumie lock-inu. Možno to tak na stretnutiach s klientmi nenazývate (hovoríte „hlboké partnerstvo“ alebo „inštitucionálne znalosti“), ale mechanizmus je ten istý. Čím viac sa vaše systémy prepletú s prevádzkou klienta, tým ťažšie sa mu odchádza. Čím ťažšie sa mu odchádza, tým predvídateľnejšie sú vaše tržby.

Táto kapitola je o tom, čo sa stane, keď ten lock-in migruje preč od vás k dodávateľom modelov. Je to posun, s ktorým sa mnohí poskytovatelia ešte plne nevyrovnali, lebo denná práca pôsobí známo, hoci mocenská dynamika pod ňou sa potichu preskupuje.

---

## Starý svet: lock-in prial poskytovateľovi IT

Buďme úprimní v tom, ako tradičný model IT služieb naozaj fungoval.

Stredne veľká európska firma si vás najme na správu infraštruktúry. Počas prvého roka spoznáte jej prostredie: legacy ERP systém, ktorý vyžaduje konkrétnu verziu JDK, konfiguráciu VPN, ktorú nastavil kontraktor, čo odišiel v roku 2019, harmonogram záloh, ktorý počíta s dávkovou úlohou bežiacou každý štvrtok o 3:00 ráno. Niečo z toho zdokumentujete. Veľa z toho žije v hlavách vášho prevádzkového tímu.

V druhom roku je klient od vás hlboko závislý. Nie preto, že vaša technológia je lepšia, ale preto, že náklady na zmenu sú obrovské. Konkurenčný poskytovateľ by potreboval mesiace na pochopenie prostredia. Riziko migrácie je skutočné. Vaše rozhovory o obnove zmluvy sú pohodlné, lebo obe strany vedia, že alternatíva je bolestivá.

To bola biznisová priekopa. Čím zložitejšie prostredie klienta, tým lepkavejší vzťah. Poskytovatelia, ktorí nahromadili inštitucionálne znalosti o systémoch svojich klientov, vybudovali trvanlivé biznisy s vysokou mierou udržania a zdravými maržami. Lock-in bol prirodzeným dôsledkom zložitosti infraštruktúry, nie zlomyseľnosti. Klient nebol uzamknutý, lebo ste ho oklamali. Bol uzamknutý, lebo práca bola ťažká a vy ste boli tí, čo ju vedeli robiť.

> **Stará rovnica lock-inu**: Zložitosť prostredia klienta vynásobená vašimi nahromadenými znalosťami o ňom sa rovnala nákladom na zmenu. Vysoké náklady na zmenu sa rovnali lepkavým tržbám. To bol samotný biznis model, nie jeho vedľajší efekt.

---

## Nový svet: lock-in beží k dodávateľom modelov

Teraz zvážte, čo sa stane, keď najdôležitejšou technologickou interakciou klienta nie je spravovaná flotila serverov, ale volanie API veľkého jazykového modelu.

Európska logistická firma chce GenAI na automatizáciu zákazníckej podpory a spracovanie dokumentov. Vývojár napíše integračný kód s formátom volania funkcií OpenAI, definuje schémy nástrojov v JSON štruktúre OpenAI a postaví pracovné postupy okolo Assistants API. Prompty sú vyladené na silné stránky GPT-4o. Hodnotiace metriky sú kalibrované voči vzorom výstupov GPT-4o.

Lock-in migroval. Logistická firma je teraz hlboko závislá od OpenAI: od jeho definícií nástrojov, jeho API schémy, výstredností správania jeho modelu. Ale poskytovateľ IT služieb, ktorý to pomohol nastaviť? Oveľa ľahšie nahraditeľný. Iný poskytovateľ by si mohol prečítať dokumentáciu API a prevziať to za pár týždňov. Zložitosť, ktorá vytvárala náklady na zmenu, bola dodávateľom modelu abstrahovaná preč.

Platforma zachytila lock-in, ktorý kedysi patril prostredníkovi.

Tento posun je štrukturálny. V tradičnom IT sedela abstrakčná vrstva nízko, blízko hardvéru. Jej správa vyžadovala hlbokú prevádzkovú odbornosť, čo je presne to, čo poskytovatelia IT služieb predávali. S GenAI API je abstrakcia oveľa vyššie. Kompetentný vývojár integruje OpenAI API za popoludnie. Ponuka „spravujeme to za vás“ stráca silu, keď spravovanou vecou je volanie REST API, nie viacserverové nasadenie s failoverom a obnovou po havárii.

---

## Kde teraz lock-in žije

Aby ste porozumeli novej konkurenčnej krajine, zmapujte, kam lock-in migroval. Teraz žije vo voľbách špecifických pre model, ktoré sa hromadia, ako organizácie budujú pracovné postupy poháňané AI.

**Prompt engineering špecifický pre model.** Prompty, ktoré fungujú dobre s Claudom, nemusia fungovať dobre s GPT-4o. Organizácie, ktoré mesiace investujú do vylaďovania systémových promptov, few-shot príkladov a šablón reťazenia myšlienok pre konkrétny model, vytvorili aktíva, ktoré sú čiastočne neprenosné.

**Formáty volania nástrojov a funkcií.** To je jeden z najkonkrétnejších vektorov lock-inu. Schéma volania funkcií OpenAI sa líši od formátu používania nástrojov Anthropicu, ktorý sa líši od deklarácií funkcií Googlu. Ak klient postavil 50 definícií nástrojov vo formáte OpenAI, migrácia na Claude vyžaduje viac než konverziu formátu; vyžaduje pretestovanie každej interakcie s nástrojom, lebo rôzne modely interpretujú popisy nástrojov rôzne.

**Stratégie kontextového okna.** Aplikácia navrhnutá okolo 200K kontextového okna Claudu funguje inak než tá navrhnutá okolo 128K okna GPT-4o. Prechod na model s menším efektívnym oknom znamená prearchitektovanie pipeline (stratégie delenia, augmentácia vyhľadávaním, sumarizačné vrstvy).

**Hodnotiace pipeline.** Možno najsubtílnejšia forma lock-inu. Organizácie, ktoré stavajú seriózne AI aplikácie, vyvíjajú testovacie sady a benchmarky kvality kalibrované na vzory výstupov konkrétneho modelu. Zmena modelu znamená prekalibrovať, ako vyzerá „dobré“: drahé, časovo náročné a zdroj skutočného organizačného odporu.

**Investície do dolaďovania.** Ak klient investoval do doladenia modelu (kurátorstvo tréningových dát, spúšťanie tréningových úloh, hodnotenie iterácií), tá investícia je úplne uzamknutá na platforme poskytovateľa. Doladený GPT-4o sa nedá preniesť na Claude. Tréningové dáta môžu byť prenosné, ale tréningová investícia nie.

> **Kde lock-in žije teraz**: V knižniciach promptov, schémach nástrojov, architektúrach kontextového okna, hodnotiacich pipeline a investíciách do dolaďovania. Čím viac staviate okolo jedného modelu, tým ťažšie sa prepína. A žiadny z týchto vektorov lock-inu neprospieva poskytovateľovi IT služieb uprostred; všetky prospievajú dodávateľovi modelu.

---

## Obranné stratégie pre poskytovateľov IT služieb

Pochopiť posun moci je krok jeden. Krok dva je vybudovať napriek nemu obhájiteľnú pozíciu. Nová krajina lock-inu vytvára konkrétne príležitosti pre poskytovateľov, ktorí myslia architektonicky, nie prevádzkovo.

**Abstrahujte vrstvu modelu.** Toto je jediné najdôležitejšie architektonické rozhodnutie, ktoré môžete v mene svojich klientov urobiť. Postavte abstrakčnú vrstvu medzi aplikačnou logikou klienta a API poskytovateľa modelu. Definície nástrojov uložené vo formáte neutrálnom voči poskytovateľovi, prekladané na integračnej vrstve. Prompty šablónované s variantmi špecifickými pre model. Žiadne natvrdo zapísané odkazy na `api.openai.com`. Keď ovládate abstrakčnú vrstvu, ovládate schopnosť prepnúť a schopnosť prepnúť je vyjednávacia sila.

**Vlastnite integračnú vrstvu.** Vaša hodnota nie je v modeli, ale v jeho prepojení s biznisovými systémami klienta: jeho ERP, CRM, správou dokumentov, pracovnými postupmi súladu. Táto integračná práca je skutočne zložitá, hlboko špecifická pre klienta a pre konkurenta ťažko rýchlo zopakovateľná. Vytvára zdravý lock-in, ktorý praje vám, nie dodávateľovi modelu.

**Postavte schopnosť prepnúť ako službu.** Ak viete vymeniť Claude za GPT-4o za Gemini za dni namiesto mesiacov, máte niečo cenné. Klient získa odolnosť voči zvyšovaniu cien, ukončeniu podpory modelu alebo regresiám kvality. Vy získate obhájiteľnú pozíciu poskytovateľa, ktorý zabezpečuje nezávislosť od dodávateľa. Stará hodnotová ponuka preformulovaná: riadenie zložitosti, ale teraz abstrakcia dodávateľov namiesto správy serverov.

**Vlastnite dátovú vrstvu.** RAG pipeline, znalostné bázy, vektorové databázy, datasety na dolaďovanie: tie robia AI funkčnou v konkrétnom biznisovom kontexte. Navrhnite ich nezávislé od modelu a stanú sa prenosnými aktívami, ktoré spravujete. Klient závisí od vašich znalostí jeho dátovej architektúry a embedding stratégií. To sú nové inštitucionálne znalosti, GenAI ekvivalent vedomosti, kde žije legacy konfigurácia VPN.

**Postavte hodnotiace rámce.** Ak viete objektívne porovnať výkon modelov pre konkrétny prípad použitia klienta (merať kvalitu, latenciu a náklady naprieč poskytovateľmi), stanete sa dôveryhodným poradcom. To je obhájiteľný, opakujúci sa poradenský vzťah, ktorý žiadny dodávateľ modelu nezopakuje, lebo dodávateľ modelu má v porovnaní inherentný konflikt záujmov.

---

## Nepríjemná pravda

Neprikrášľujme to. Obranné stratégie sú skutočné a cenné, ale nemenia základnú matematiku pre každého poskytovateľa.

Niektorí poskytovatelia IT služieb budú mať menej klientov, ktorí ich potrebujú, bez ohľadu na to, ako dobre to zvládnu. Keď sólo vývojár integruje LLM API za popoludnie, bazén klientov, ktorí potrebujú poskytovateľa spravovaných služieb, sa zmenšuje. Nie na nulu, ale zmysluplne.

Ponuka „spravujeme to za vás“ vyžaduje predefinovať, čo „to“ znamená. Ak „to“ je integrácia API a prompt engineering, ponuka je slabá. Ak „to“ je orchestrácia viacerých modelov, architektúra súladu, hodnotiace rámce a priebežná optimalizácia naprieč portfóliom AI aplikácií, to je úplne iný návrh. Ale vyžaduje schopnosti, ktoré väčšina tradičných poskytovateľov IT služieb momentálne nemá.

Hodnota sa musí posunúť od „prevádzkujeme vaše veci“ k „robíme AI funkčnou vo vašom konkrétnom kontexte“. To implikuje porozumenie biznisovej doméne klienta, nielen jeho infraštruktúre. Implikuje poradenskú schopnosť, nielen prevádzkovú. A implikuje ochotu byť meraný podľa výsledkov, nie podľa dostupnosti.

> **Nepríjemná pravda**: Štrukturálne zjednodušenie AI infraštruktúry znamená, že niektorí klienti poskytovateľa IT služieb nebudú potrebovať vôbec. Poskytovatelia, ktorí prosperujú, budú tí, ktorých hodnota jasne prevyšuje to, čo klient zvládne s API kľúčom a popoludním čítania dokumentácie.

---

## Príležitosť v abstrakcii

Byť vrstvou medzi organizáciami a dodávateľmi modelov je skutočný, obhájiteľný biznis, ale nevyzerá ani trochu ako tradičná správa infraštruktúry.

**Orchestrácia viacerých modelov ako služba.** Smerujte rôzne typy požiadaviek na rôzne modely podľa zložitosti, nákladov a požiadaviek na kvalitu. Chatbot zákazníckej podpory riešiaci rutinné otázky používa rýchly, lacný model. Ten istý systém pri eskalácii na zložité uvažovanie dynamicky smeruje na schopnejší model. Stavba a prevádzka tejto smerovacej vrstvy (s monitorovaním kvality, sledovaním nákladov a priebežnou optimalizáciou) je skutočná, opakujúca sa práca.

**Správa dodávateľov a optimalizácia nákladov.** Keď klient používa troch poskytovateľov modelov naprieč tuctom aplikácií, niekto musí sledovať výdavky, vyjednávať podnikové zmluvy, monitorovať limity rýchlosti a detegovať, keď zmena ceny alebo aktualizácia modelu u poskytovateľa rozbije pracovný postup. To je nákupná a prevádzková odbornosť aplikovaná na novú doménu.

**Hodnotenie a výber modelov.** Krajina modelov sa mení kvartálne. Poskytovateľ, ktorý udržiava aktuálne benchmarky naprieč modelmi pre bežné podnikové prípady použitia a vie klientom poradiť, kedy prepnúť, kedy ostať a kedy sa zaistiť, poskytuje priebežnú strategickú hodnotu.

Tieto služby zdieľajú charakteristiku: sú tým cennejšie, čím viac poskytovateľov modelov existuje a čím rýchlejšie sa trh hýbe. Vo svete s piatimi či šiestimi konkurencieschopnými poskytovateľmi vydávajúcimi nové modely každý kvartál (čo je svet, v ktorom sme) je zložitosť navigácie v krajine sama osebe zdrojom hodnoty.

> **Príležitosť**: Tá istá fragmentácia trhu, ktorá ohrozuje váš starý biznis model, vytvára dopyt po vašom novom. Zložitosť viacerých modelov je nová zložitosť infraštruktúry. Ak ju viete spravovať, máte biznis.

---

## Od pasívnej k aktívnej nenahraditeľnosti

V starom modeli ste boli nenahraditeľní, lebo odísť od vás bolo bolestivé: pasívny lock-in. V novom modeli musíte byť nenahraditeľní, lebo alternatíva je horšia, klient spravujúci orchestráciu viacerých modelov, hodnotenie, súlad a optimalizáciu sám. To je aktívna nenahraditeľnosť: klient ostáva, lebo váš prínos je viditeľný a merateľný, nie preto, že prepnutie je ťažké.

Aktívna nenahraditeľnosť sa buduje ťažšie, ale je trvanlivejšia. Závisí od odbornosti, ktorú klient vidí a cení si, nie od informačnej asymetrie. Poskytovatelia, ktorí si to osvoja najskôr, budú mať významný náskok, nie preto, že práca je nemožne zložitá, ale preto, že transformácia z prevádzkovateľov infraštruktúry na poradcov v inteligencii trvá. Okno je otvorené teraz.

> **Poznámka z júla 2026.** Táto kapitola berie lock-in ako komerčný problém: schémy, prompty, hodnotiace pipeline. Pre klientov v EÚ je nad tým teraz aj jurisdikčná vrstva. Od júlového opätovného vydania najschopnejších amerických modelov za bránami (iba preverené firmy na najvyššej úrovni, drahé moderované API pod ňou) je vaša voľba dodávateľa modelu aj expozíciou voči rozhodnutiam inej jurisdikcie o prístupe. Obranné stratégie vyššie (abstrahovať vrstvu modelu, držať schopnosť prepnúť zahriatu) sa ukazujú ako zaistenie aj proti geopolitickému riziku, nielen cenovému, čo ich robí cennejšími, nie menej. Ako funguje prístup odstupňovaný podľa blokov, je zmapované v brožúre [Merkantilizmus generatívnej AI](/mercantilism-of-genai-sk/#m-bloc).

---

> **Strážca čerstvosti** · *overené apríl 2026 · odhadovaný polčas rozpadu: ~4 – 6 mesiacov*
>
> Štrukturálne tvrdenie (lock-in migroval z infraštruktúry do volieb špecifických pre model) je trvanlivé. Konkrétne technické detaily sa hýbu rýchlejšie:
>
> - **Veľkosti kontextových okien** (200K Claudu vs 128K GPT-4o) sa menia približne každých 6 – 9 mesiacov, ako vychádzajú nové verzie modelov. Medzera medzi poskytovateľmi sa zužuje.
> - **Nekompatibilita schém volania nástrojov/funkcií** medzi formátmi OpenAI, Anthropicu a Googlu je dnes skutočný vektor lock-inu. Štandardizačné snahy (špecifikácie funkcií v štýle OpenAPI, MCP) to môžu do roku 2027 čiastočne riešiť.
> - **Pomenované funkcie** (OpenAI Assistants API, konkrétne formáty nástrojov poskytovateľov) môžu byť ukončené alebo premenované; pred písaním architektonických dokumentov pre klientov overte aktuálne názvy.
>
> Obranné stratégie (abstrahovať vrstvu modelu, vlastniť integráciu, postaviť schopnosť prepnúť ako službu) sú s vývojom podkladovej krajiny API *cennejšie*, nie menej.

---

*Ďalej: [Kapitola 11, AI Act EÚ: vaša príležitosť v súlade](11_eu_ai_act.md)*
