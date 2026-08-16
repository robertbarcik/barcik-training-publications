# Kapitola 11: AI Act EÚ: vaša príležitosť v súlade

> **V skratke**
>
> - Súlad s AI Actom EÚ je zhruba na 20 % právna interpretácia a na 80 % technická implementácia. Právnici definujú povinnosti; niekto musí postaviť systémy, a ten niekto ste vy.
> - Väčšina vašich podnikových klientov sú „nasadzujúce subjekty“ vysokorizikových AI systémov: potrebujú fungujúci ľudský dohľad, logovanie, monitorovanie a hlásenie incidentov, nie politiky na papieri.
> - Osem línií služieb, od inventarizácie a klasifikácie AI (prirodzený vstupný bod) po monitorovanie po uvedení na trh (prirodzený paušál).
> - Nikdy nepredávajte „súlad“; predávajte nasadenie AI, ktoré je v súlade od prvého dňa. Zabalený súlad je hodnota; nezabalený súlad je náklad, ktorý treba minimalizovať.
>
> **Číslo, ktoré si zapamätať:** august 2026, keď sa povinnosti pre vysokorizikové systémy stanú vymáhateľnými. Váš najlepší obchodný nástroj, s pripojeným odpočítavaním.

Každá technologická regulácia vytvára dve skupiny: tých, ktorí ju vidia ako náklad na minimalizovanie, a tých, ktorí ju vidia ako službu na predaj. AI Act EÚ je najvýznamnejší kus AI regulácie na svete a pre poskytovateľov IT služieb so sídlom v EÚ patrí pevne do druhej kategórie.

Táto kapitola je praktický sprievodca, nie právny úvod; na to si môžete najať právnika. Pokrýva konkrétnu implementačnú prácu, ktorú Akt vyžaduje, prečo je tá práca technická a nie právna, a ako pozicionovať vašu firmu ako tú, ktorá ju robí.

---

## Práve dosť kontextu: čo Akt naozaj vyžaduje

AI Act EÚ nadobudol účinnosť 1. augusta 2024. Sleduje fázový harmonogram vymáhania:

- **Február 2025:** Nadobúdajú účinnosť zákazy AI systémov s neprijateľným rizikom (sociálne bodovanie, biometrická identifikácia v reálnom čase na verejných priestranstvách s úzkymi výnimkami, manipulácia zraniteľných skupín).
- **August 2025:** Nabiehajú povinnosti pre poskytovateľov modelov všeobecnej AI (GPAI): transparentnosť, dokumentácia, súlad s autorským právom a pri modeloch so systémovým rizikom dodatočné bezpečnostné hodnotenia.
- **August 2026:** Ten veľký. Povinnosti pre vysokorizikové AI systémy sa stávajú vymáhateľnými. Tu žije väčšina implementačnej práce a tu sa začína väčšina povinností vašich klientov.
- **August 2027:** Predĺžený termín pre vysokorizikové AI systémy, ktoré sú bezpečnostnými komponentmi produktov už regulovaných existujúcou sektorovou legislatívou EÚ (zdravotnícke pomôcky, strojové zariadenia, letectvo, vozidlá).

Akt klasifikuje AI systémy do štyroch úrovní rizika:

**Neprijateľné riziko:** priamo zakázané. Sociálne bodovanie, manipulatívna AI cieliaca na zraniteľné skupiny, necielené databázy rozpoznávania tvárí, rozpoznávanie emócií na pracoviskách a v školách. Vaši klienti by tieto nemali stavať. Ak áno, rozhovor je s právnym oddelením, nie s vami.

**Vysoké riziko:** silno regulované. Tu sú peniaze. Vysokorizikové systémy zahŕňajú AI používanú pri nábore a prijímaní, kreditnom bodovaní a finančných posúdeniach, presadzovaní práva a kontrole hraníc, správe kritickej infraštruktúry (energetika, voda, doprava), vzdelávaní (hodnotenie skúšok, posudzovanie študentov), prístupe k základným službám a spracovaní migrácie/azylu. Patrí sem aj každý AI systém používaný ako bezpečnostný komponent v produktoch pokrytých existujúcou legislatívou EÚ o bezpečnosti výrobkov.

**Obmedzené riziko:** povinnosti transparentnosti. Chatboty musia zverejniť, že sú AI. Deepfaky musia byť označené. Systémy rozpoznávania emócií musia informovať používateľov. To sú ľahšie požiadavky, ale stále potrebujú implementáciu.

**Minimálne riziko:** žiadne špecifické povinnosti. Spamové filtre, AI vo videohrách, väčšina interných nástrojov produktivity. Drvivá väčšina AI systémov patrí sem.

### Poskytovatelia vs nasadzujúce subjekty: rozlíšenie, na ktorom záleží

Akt kreslí kritickú čiaru medzi **poskytovateľmi** (tými, ktorí AI systémy vyvíjajú alebo uvádzajú na trh) a **nasadzujúcimi subjektmi** (tými, ktorí AI systémy používajú v profesionálnej kapacite). Väčšina vašich podnikových klientov budú nasadzujúce subjekty. Niektorí sa môžu stať aj poskytovateľmi, ak AI systém doladia alebo podstatne upravia.

Nasadzujúce subjekty vysokorizikových AI systémov musia:

- Používať systém v súlade s pokynmi poskytovateľa
- Zabezpečiť ľudský dohľad kvalifikovaným personálom
- Monitorovať prevádzku systému a hlásiť závažné incidenty
- Vykonať posúdenie vplyvu na základné práva (pri určitých kategóriách)
- Uchovávať logy generované systémom aspoň šesť mesiacov
- Informovať zamestnancov a ich zástupcov, že podliehajú AI systémom
- Zabezpečiť, že vstupné dáta sú relevantné a reprezentatívne

To nie sú abstraktné požiadavky politík, ale prevádzkové povinnosti, ktoré na splnenie potrebujú technické systémy, procesy a infraštruktúru. Niekto tie systémy musí postaviť. Ten niekto by ste mali byť vy.

> **Kľúčové posolstvo:** Väčšina vašich podnikových klientov budú podľa AI Actu EÚ „nasadzujúce subjekty“. Do augusta 2026 potrebujú fungujúci ľudský dohľad, monitorovanie, logovanie, hlásenie incidentov a procesy posudzovania vplyvu: nielen politiky na papieri, ale fungujúce technické implementácie.

## Prečo je to implementačná, nie právna práca

Tu je kľúčový vhľad, ktorý mnohým poskytovateľom uniká: súlad s AI Actom EÚ je zhruba na 20 % právna interpretácia a na 80 % technická implementácia. Právnici povedia vašim klientom, čo musia urobiť. Vy postavíte systémy, ktoré to naozaj urobia.

Zvážte, čo nasadzujúci subjekt vysokorizikového AI systému (povedzme banka používajúca AI na kreditné bodovanie) naozaj potrebuje:

**Systém riadenia rizík.** Nie dokument s názvom „Politika riadenia rizík“. Skutočný systém, ktorý priebežne identifikuje, hodnotí a zmierňuje riziká počas celého životného cyklu AI systému. To znamená monitorovacie pipeline, alertovaciu infraštruktúru, dashboardy rizikového bodovania a integráciu s existujúcimi rámcami riadenia rizík banky. To je inžinierska práca.

**Správu dát.** Tréningové a validačné dáta použité pri akomkoľvek dolaďovaní alebo prispôsobovaní potrebujú dokumentáciu: pôvod, kroky predspracovania, analýzu zaujatosti, posúdenie reprezentatívnosti. Ak váš klient dolaďuje modely na vlastných dátach, potrebuje pipeline správy dát: verzovanie, kontroly kvality, testovanie zaujatosti, sledovanie pôvodu. To je dátovo-inžinierska práca.

**Technickú dokumentáciu a technický spis.** Vysokorizikové systémy vyžadujú podrobnú dokumentáciu účelu systému, návrhu, vývojového procesu, testovacej metodiky a výkonnostných metrík. Pre nasadzujúci subjekt, ktorý AI systém prispôsobil alebo integroval, to znamená zdokumentovať celú integračnú architektúru, rozhodnutia prompt engineeringu, výsledky hodnotenia, režimy zlyhania. To je technické písanie podložené inžinierskou analýzou.

**Mechanizmy ľudského dohľadu.** Akt vyžaduje, aby vysokorizikové AI systémy mohli byť účinne dozerané fyzickými osobami. V praxi to znamená stavať rozhrania a pracovné postupy, kde ľudskí posudzovatelia môžu kontrolovať rozhodnutia AI, v prípade potreby ich prepísať a pri určitých prípadoch použitia zasiahnuť v reálnom čase. To je práca UX dizajnu a systémovej integrácie.

**Infraštruktúru logovania a monitorovania.** Systémy musia generovať logy umožňujúce sledovateľnosť počas celého životného cyklu AI systému. Pre produkčné AI systémy to znamená štruktúrované logovanie vstupov, výstupov, verzií modelov, skóre istoty a rozhodnutí o ľudskom prepísaní, bezpečne uložené, uchovávané požadovaný čas a prístupné pre audit. To je infraštruktúrne inžinierstvo.

**Hlásenie incidentov.** Závažné incidenty sa musia hlásiť orgánom dohľadu nad trhom. To vyžaduje detekčné mechanizmy (ako viete, že sa niečo pokazilo?), klasifikačnú logiku (je to závažné?) a hlásiace pracovné postupy integrované s existujúcou správou incidentov klienta. To je DevOps a procesné inžinierstvo.

Právna kancelária nič z toho nepostaví. Manažérska konzultačná firma vie napísať politiky, ale nevie implementovať systémy. Práca sedí priamo v doméne poskytovateľov technických služieb, ktorí rozumejú AI systémom aj podnikovej infraštruktúre, čo ste presne vy.

> **Kľúčové posolstvo:** Súlad s AI Actom EÚ je primárne technická implementačná výzva, nie právna. Právnici definujú povinnosti; vy staviate systémy, ktoré ich spĺňajú. Pipeline riadenia rizík, logovacia infraštruktúra, rozhrania ľudského dohľadu, rámce testovania zaujatosti, detekcia incidentov. To je vaša doména.

## Osem línií služieb, ktoré môžete postaviť už dnes

Tu sú konkrétne príležitosti služieb, zoradené zhruba podľa toho, ako rýchlo ich viete dostať na trh:

### 1. Inventarizácia a klasifikácia AI systémov

Kým klient môže byť v súlade, musí vedieť, aké AI systémy naozaj používa. Mnohé podniky nemajú komplexný inventár. Tieňová AI (oddelenia kupujúce prístup k API alebo používajúce AI nástroje bez vedomia IT) je rozšírená. Prvá zákazka je často discovery cvičenie: aké AI systémy existujú, kto ich používa, na aký účel a do ktorej kategórie rizika patria.

To je nízkonákladová, vysokohodnotná práca. Nevyžaduje hlbokú AI odbornosť, len zručnosti systematického posudzovania a znalosť klasifikačných kritérií Aktu. A je to prirodzený vstupný bod pre každú ďalšiu službu na tomto zozname.

### 2. Implementácia systému riadenia rizík

Stavba infraštruktúry priebežného posudzovania rizík pre vysokorizikové nasadenia AI. Zahŕňa definovanie rizikových metrík, stavbu monitorovacích dashboardov, nastavenie alertovacích pipeline a integráciu s existujúcimi rámcami rizík a súladu klienta. Ak máte skúsenosti s ISO 27001 alebo podobnými systémami riadenia, štruktúra je známa; iný je len obsah.

### 3. Testovanie zaujatosti a hodnotenie férovosti

Vysokorizikové AI systémy sa musia testovať na zaujatosť naprieč chránenými charakteristikami. To je opakujúca sa služba, nie jednorazová zákazka. Modely driftujú. Rozdelenia dát sa posúvajú. Vynárajú sa nové hraničné prípady. Kvartálny alebo mesačný audit zaujatosti so zdokumentovanou metodikou a výsledkami je presne ten druh paušálnej služby, ktorá buduje opakované tržby.

Technická práca zahŕňa stavbu hodnotiacich datasetov, spúšťanie štruktúrovaných testov naprieč demografickými skupinami, štatistickú analýzu výsledkov a jasný reporting. Ak má váš tím dátovovedecké schopnosti, je to prirodzené.

### 4. Infraštruktúra monitorovania a logovania

Produkčné AI systémy potrebujú štruktúrované, auditovateľné logovanie, ktoré zachytáva vstupy, výstupy, verzie modelov, latenciu, skóre istoty a udalosti ľudského zásahu. To je klasická infraštruktúrna práca, taká, akú váš prevádzkový tím už vie stavať, aplikovaná na novú doménu.

Kľúčový rozdiel oproti tradičnému aplikačnému logovaniu: logy AI systémov musia podporovať sledovateľnosť jednotlivých rozhodnutí, nielen metriky zdravia systému. To znamená bohatšie zachytávanie dát, dlhšie uchovávanie a dopytovacie schopnosti podporujúce dodatočnú analýzu konkrétnych výstupov.

### 5. Návrh mechanizmov ľudského dohľadu

Stavba rozhraní a pracovných postupov, ktoré umožňujú zmysluplný ľudský dohľad. Pri náborovej AI to môže znamenať kontrolný dashboard, kde recruiteri vidia uvažovanie AI, prepíšu rozhodnutia a označia obavy. Pri systéme kreditného bodovania to môže znamenať eskalačný pracovný postup, ktorý smeruje hraničné prípady k ľudským analytikom.

To je práca UX a systémovej integrácie. Je aj hlboko špecifická pre doménu a procesy každého klienta, čo ju robí ťažko komoditizovateľnou a ťažko ponúknuteľnou hyperškálovou firmou ako generickú službu. Tá špecifickosť je vaša výhoda.

### 6. Technická dokumentácia a príprava na posudzovanie zhody

Vysokorizikové AI systémy potrebujú technický spis, pri ktorom by sa regulátor zdravotníckych pomôcok cítil ako doma. Architektúra systému, návrhové rozhodnutia, dokumentácia tréningových dát, testovacia metodika, výkonnostné benchmarky, známe obmedzenia, špecifikácie nasadenia. Pre poskytovateľov to zahŕňa aj posudzovanie zhody: buď vlastné posúdenie, alebo posúdenie treťou stranou podľa prípadu použitia.

Väčšina klientov bude s prípravou týchto materiálov potrebovať pomoc. Práca kombinuje technickú hĺbku (systému musíte rozumieť, aby ste ho zdokumentovali) s regulačným povedomím (musíte vedieť, čo dokumentácia musí pokrývať). To je poradenstvo za prémiové sadzby.

### 7. Správa dát pre trénovanie a dolaďovanie

Ak váš klient dolaďuje alebo prispôsobuje AI modely na vlastných dátach, potrebuje rámce správy pokrývajúce pôvod dát, posúdenie kvality, analýzu zaujatosti, správu súhlasov (kde ide o osobné údaje) a riadenie verzií. To sa silno pretína s existujúcou správou dát podľa GDPR, ďalšou oblasťou, kde je vaša prítomnosť v EÚ výhodou.

### 8. Monitorovanie po uvedení na trh a hlásenie incidentov

Keď je vysokorizikový AI systém v produkcii, povinnosti sa nekončia. Nasadzujúce subjekty musia monitorovať výkon, detegovať degradáciu alebo drift, identifikovať závažné incidenty a hlásiť ich orgánom. Stavba systémov, ktoré to robia (automatizované sledovanie výkonu, detekcia anomálií, klasifikácia incidentov a hlásiace pracovné postupy), je priebežná infraštruktúrna práca s prirodzeným paušálnym modelom.

> **Kľúčové posolstvo:** AI Act EÚ vytvára aspoň osem samostatných technických línií služieb, od úvodnej inventarizácie a klasifikácie až po monitorovanie po uvedení na trh. Väčšina z nich sú opakujúce sa zákazky, nie jednorazové projekty. Začnite inventarizáciou AI systémov: má najnižšiu bariéru vstupu a je prirodzenou bránou ku všetkému ostatnému.

## Dátová suverenita ako prémiová služba

V kapitole 6 sme rozoberali model proxy pre súkromie a jeho ekonomiku. AI Act EÚ pridáva regulačný rozmer, ktorý v konkrétnych segmentoch posilňuje argument pre AI služby hostované v EÚ.

Niektorí klienti nielen preferujú držať dáta v EÚ. Sú k tomu právne povinní. Kombinácia obmedzení prenosu dát podľa GDPR, sektorových regulácií a požiadaviek AI Actu EÚ na správu dát a monitorovanie systémov vytvára scenáre, kde posielanie dát poskytovateľom AI so sídlom v USA skutočne nie je možnosťou:

- **Bankovníctvo a finančné služby** pod dohľadom ECB a národných orgánov dohľadu, kde outsourcing k spracovateľom mimo EÚ spúšťa dodatočné regulačné požiadavky, ktoré môžu prevýšiť úspory nákladov.
- **Zdravotníctvo** v jurisdikciách s prísnymi požiadavkami na lokalizáciu dát pacientov; nemecké regulácie infraštruktúry zdravotných dát sú ukážkovým príkladom.
- **Obrana a národná bezpečnosť**, kde pravidlá klasifikácie dát externé spracovanie úplne zakazujú.
- **Verejný sektor** v konkrétnych členských štátoch s mandátmi dátovej suverenity: francúzska kvalifikácia SecNumCloud, nemecké požiadavky IT-Grundschutz a podobné rámce.

Pre týchto klientov je ekonomika, ktorú sme načrtli v kapitolách 3 a 4, kde je vlastný hosting 5 – 15× drahší než prístup cez API, irelevantná. Relevantné porovnanie nie je „vlastný hosting vs API“, ale „vlastný hosting vs nepoužívať AI vôbec“. A oproti tejto alternatíve sa prémia za vlastný hosting obhajuje ľahko.

To je ten jeden scenár, kde sa infraštruktúrny biznis model zo starého sveta čisto prenáša do GenAI. Hostujete modely. Prevádzkujete infraštruktúru. Garantujete, že dáta nikdy neopustia vaše zariadenia v EÚ. A účtujete prémiu, ktorá odráža regulačné obmedzenie, nie komoditné náklady na výpočtový výkon.

Medzi americkým API a vaším vlastným rackom sedí stredná cesta, ktorú sa oplatí poznať: inferencia tretej strany hostovaná v EÚ. Mistral poskytuje modely blízko špičky z EÚ infraštruktúry pod EÚ právnym subjektom, viaceré členské štáty stavajú ponuky suverénneho cloudu a hyperškálové firmy predávajú EÚ hranice dát rôznej dôveryhodnosti (americká materská firma ostáva americkou materskou firmou na jurisdikčné účely, čo je presne to, čo niektorých regulátorov zaujíma). Pre klientov, ktorých obmedzením je jurisdikcia a nie fyzická kontrola, táto úroveň dodá väčšinu argumentu suverenity blízko ekonomike API a vy stále vlastníte integráciu, hodnotenie a nadstavbu súladu okolo nej. Odporúčajte ju, keď je on-prem prehnaný a americké API sú vylúčené; robí z vás poradcu, ktorý suverenitu správne dimenzuje, namiesto dodávateľa, ktorý ju predáva nadbytočne.

Trh je skutočný. Ale je užší, než naznačujú marketingové materiály väčšiny EÚ cloudových poskytovateľov. Neplánujte celý svoj biznis okolo klientov s dátovou suverenitou. Naplánujte pre nich ziskovú líniu služieb a zvyšok svojej AI praxe postavte okolo širších príležitostí v súlade a integrácii.

> **Kľúčové posolstvo:** Dátová suverenita je skutočná prémiová príležitosť pre klientov z bankovníctva, zdravotníctva, obrany a určitého verejného sektora, ktorí americké AI API doslova nemôžu použiť. Naceňte ju ako regulačnú nevyhnutnosť, nie infraštruktúru s prirážkou. Ale uvedomte si, že je to zisková nika, nie masový trh.

## Ako to pozicionovať

Najväčšia chyba, ktorú môžete urobiť, je predávať „súlad s AI Actom EÚ“ ako samostatný produkt. Tu je prečo: súlad je v mysli klienta náklad. Nikto sa nezobudí nadšený, že si kúpi súlad; je to vec, ktorú musí urobiť, a bude sa ju snažiť urobiť čo najlacnejšie. Ak predávate súlad ako položku, pozývate cenovú konkurenciu od každej konzultačnej firmy, právnej kancelárie a freelancera, ktorý vie prečítať nariadenie.

Namiesto toho integrujte súlad do svojej ponuky nasadenia AI. Ponuka nie je:

*„Pomôžeme vám dosiahnuť súlad s AI Actom EÚ.“*

Ponuka je:

*„Nasadzujeme AI vo vašej organizácii a každé nasadenie, ktoré robíme, je v súlade s AI Actom EÚ od prvého dňa.“*

Rozdiel je hlboký. V prvej ponuke ste nákladové stredisko. V druhej ste umožňovateľ, ktorý mimochodom odstraňuje veľké riziko. Súlad je zabalený do hodnoty, nepredáva sa ako réžia.

Toto pozicionovanie funguje obzvlášť dobre v kombinácii so schopnosťami z predchádzajúcich kapitol:

- **Proxy pre súkromie (kapitola 6) + súlad s AI Actom EÚ** = „Smerujeme vaše používanie AI cez EÚ infraštruktúru s plným regulačným súladom zabudovaným vnútri.“
- **Lokálne nasadenie (kapitola 7) + súlad s AI Actom EÚ** = „Nasadzujeme AI na zariadeniach vašich zamestnancov: žiadne dáta neopustia vašu organizáciu a každé nasadenie spĺňa požiadavky AI Actu EÚ.“
- **Testovanie a bezpečnosť (kapitola 8) + súlad s AI Actom EÚ** = „Testujeme a monitorujeme vaše AI systémy z hľadiska kvality, bezpečnosti a regulačného súladu ako jednu spravovanú službu.“

Každá z týchto je silnejším návrhom než ktorákoľvek zložka predávaná samostatne. Vrstva súladu robí technickú ponuku cennejšou a technická ponuka robí súlad hmatateľným, nie teoretickým.

### Školenie vášho tímu

Toto je investícia, ktorá sa vráti najrýchlejšie. AI Act EÚ je dosť nový na to, aby skutočná odbornosť bola vzácna. Ak váš tím rozumie požiadavkám nariadenia aj tomu, ako ich technicky implementovať, máte skutočný diferenciátor, ktorý pretrvá aspoň 18 – 24 mesiacov, kým trh dobehne.

Znalosti, ktoré potrebujete, nie sú hlboká právna odbornosť, ale praktické porozumenie:

- Ktoré systémy patria do ktorých kategórií rizika
- Čo konkrétne musia nasadzujúce subjekty urobiť (a dokedy)
- Čo obnáša posudzovanie zhody pre rôzne typy systémov
- Ako štruktúrovať technickú dokumentáciu spĺňajúcu požiadavky Aktu
- Čo musí monitorovacia a logovacia infraštruktúra zachytávať

Tím troch až piatich inžinierov, ktorí rozumejú týmto požiadavkám a vedia implementovať príslušné systémy, je cennejší než tím päťdesiatich, ktorí vedia stavať generickú cloudovú infraštruktúru. Akt vytvára znalostnú prémiu, ktorá odmeňuje skorú investíciu.

## Výhoda časovej osi

Harmonogram vymáhania vytvára konkrétne strategické okno. Väčšina podnikov je práve teraz v jednom z troch stavov:

**Nevedomí.** Používajú AI, ale nespojili si ju s povinnosťami AI Actu EÚ. Nevedia, že sú nasadzujúcimi subjektmi potenciálne vysokorizikových systémov. Patrí sem prekvapivo veľa firiem, najmä tých, ktoré AI nástroje prijali neformálne, bez centralizovaného nákupného procesu.

**Vedomí, ale paralyzovaní.** Vedia, že Akt existuje. Možno im právnik prezentoval prehľad na predstavenstve. Ale nemajú konkrétny implementačný plán, žiadnu internú odbornosť a žiadny pridelený rozpočet. Čakajú, kým im niekto povie, čo prakticky robiť.

**Aktívne sa pripravujúci.** Malá menšina, väčšinou veľké podniky a tie v silno regulovaných sektoroch. Začali programy súladu, ale zisťujú, že implementačná práca prevyšuje ich internú kapacitu.

Všetky tri skupiny potrebujú pomoc, ale stredná skupina, vedomí, ale paralyzovaní, je najväčšia a najvnímavejšia. Majú naliehavosť (termín august 2026 pre povinnosti vysokorizikových systémov nie je ďaleko), ale nie schopnosť. Poskytovateľ, ktorý vie prísť s jasnou metodikou posúdenia, konkrétnou implementačnou cestovnou mapou a preukázanou technickou schopnosťou, tieto zákazky vyhrá.

A tu je strategický bonus: partnerstvá v súlade sú lepkavé. Keď ste klientovi postavili systém riadenia rizík, zdokumentovali jeho AI nasadenia, implementovali jeho monitorovaciu infraštruktúru a nastavili jeho pracovné postupy hlásenia incidentov, prechod k inému poskytovateľovi je bolestivý a drahý. Klient by musel všetko znovu zdokumentovať, preškoliť personál na nové nástroje a znovu vybudovať dôveru s novým partnerom, to všetko, kým hodiny súladu tikajú ďalej.

To je druh štrukturálnej lepkavosti, akú kedysi poskytoval hosting infraštruktúry. Ibaže namiesto uzamknutia dátovou gravitáciou a nákladmi na migráciu je klient udržaný kontinuitou súladu a inštitucionálnymi znalosťami. Je to lepšia forma lock-inu, lebo je poháňaná dodanou hodnotou, nie uloženými nákladmi na zmenu.

> **Kľúčové posolstvo:** Harmonogram vymáhania vytvára úzke okno (zhruba odteraz do augusta 2026), v ktorom sa poskytovatelia, ktorí si vybudujú odbornosť v implementácii AI Actu EÚ, etablujú ako dôveryhodní partneri. Keď sú raz zabudovaní v infraštruktúre súladu klienta, tieto vzťahy sú prirodzene lepkavé. Skorí hráči budú mať trvanlivú výhodu.

## Realita verejného obstarávania

Mnohí poskytovatelia IT služieb v EÚ odvodzujú 30 – 40 % tržieb od vládnych zákaziek a zákaziek verejného sektora. Ak to opisuje váš biznis, stratégia GenAI nie je len technologická otázka; je to otázka obstarávania.

IT vo verejnom sektore naprieč EÚ sa typicky obstaráva cez rámcové dohody a viacročné tendre. Pridať „AI služby“ do existujúcej rámcovej zmluvy je zriedka také jednoduché ako aktualizovať katalóg služieb. Vo väčšine jurisdikcií to vyžaduje nový proces obstarávania, nové hodnotiace kritériá a často nové certifikácie od poskytovateľa.

**Čo to prakticky znamená:**

- **Cykly obstarávania trvajú 12 – 18 mesiacov.** Ak chcete v roku 2027 predávať AI služby vládnemu klientovi, musíte reagovať na tendre a obnovy rámcov teraz.
- **Existujúce rámce sú váš vstupný bod.** Ak už držíte rámcovú dohodu na spravované služby alebo poradenstvo s vládnym klientom, preskúmajte, či AI služby možno pozicionovať pod existujúce kategórie služieb (napr. „IT poradenstvo“, „systémová integrácia“, „správa infraštruktúry“). To je často rýchlejšie než nové obstarávanie.
- **Na certifikáciách záleží.** Niektoré členské štáty EÚ vyvíjajú špecifické certifikácie alebo štandardy súvisiace s AI pre vládnych dodávateľov. Byť skoro certifikovaný je konkurenčná výhoda pri hodnotení tendrov.
- **Bezpečnostné previerky a klasifikácia dát.** Vládne nasadenia AI často zahŕňajú utajované alebo citlivé dáta. Ak váš tím už drží relevantné bezpečnostné previerky, je to významná bariéra vstupu, ktorá chráni vašu pozíciu.
- **Výhoda zavedeného dodávateľa je skutočná.** Vládny klient s existujúcim vzťahom oveľa pravdepodobnejšie rozšíri váš mandát o AI služby, než aby spustil samostatné obstarávanie na nového poskytovateľa. Využite to.

**AI Act EÚ zosilňuje príležitosť vo verejnom sektore.** Vládne orgány sú samy nasadzujúcimi subjektmi AI systémov a musia Akt dodržiavať, často na úrovni vysokorizikovej klasifikácie (presadzovanie práva, imigrácia, verejné dávky, kritická infraštruktúra). Potrebujú implementačných partnerov, ktorí rozumejú technológii aj regulačným požiadavkám, a silno preferujú prácu s poskytovateľmi, ktorým už dôverujú.

> **Kľúčové posolstvo:** Ak verejný sektor predstavuje významný podiel vašich tržieb, začnite AI služby pozicionovať v existujúcich nástrojoch obstarávania už teraz. Cyklus obstarávania znamená, že príležitosti zmeškané dnes sa nevrátia 12 – 18 mesiacov. Váš status zavedeného dodávateľa je aktívum. Využite ho skôr, než ďalší tendrový cyklus vpustí nových konkurentov.

## Čo táto kapitola znamená pre vašu stratégiu

AI Act EÚ je trh na obsluhovanie, nie bremeno na znášanie. Nariadenie vytvára povinný dopyt po technickej implementačnej práci, ktorá sedí priamo v zóne kompetencie poskytovateľov IT služieb. Praje poskytovateľom so sídlom v EÚ, ktorí zdieľajú regulačné prostredie svojich klientov. Vytvára opakované tržby cez priebežné povinnosti monitorovania a hlásenia. A poskytuje prirodzenú lepkavosť, ktorá chráni pred tlakmi komoditizácie, o ktorých sme hovorili v predchádzajúcich kapitolách.

Konkrétne kroky:

1. **Investujte do školenia teraz.** Do ďalšieho kvartálu majte troch až piatich ľudí plynulých v praktických požiadavkách Aktu. Nie je to šesťmesačný projekt: jadro materiálu technickí ľudia so skúsenosťami so súladom vstrebú za týždne.

2. **Začnite zákazkami na inventarizáciu AI.** Ponúknite existujúcim klientom discovery cvičenie: aké AI systémy používate a ktoré spúšťajú povinnosti podľa AI Actu EÚ? Je to nízkorizikové, nízkonákladové a otvára dvere ku všetkému ostatnému.

3. **Baľte, nerozbaľujte.** Predávajte súlad ako súčasť svojich služieb nasadenia a správy AI, nie ako samostatný produkt. Marža je lepšia a pozicionovanie silnejšie.

4. **Postavte líniu služieb dátovej suverenity pre klientov, ktorí ju potrebujú.** Naceňte ju ako prémiovú ponuku. Neospravedlňujte sa za prirážku; klient nemá lacnejšiu alternatívu.

5. **Cieľte na termín august 2026.** Každý nasadzujúci subjekt vysokorizikového AI systému dovtedy potrebuje fungujúcu infraštruktúru súladu. Ten termín je váš najlepší obchodný nástroj na najbližších niekoľko mesiacov.

Nariadenie je zložité. Príležitosť je priamočiara.

> **Strážca čerstvosti** · *overené apríl 2026 · odhadovaný polčas rozpadu: ~18 – 24 mesiacov*
>
> Zákonný text AI Actu EÚ je stabilný. Vykonávacia krajina nie.
>
> - **Dátumy vymáhania** (feb. 2025, aug. 2025, aug. 2026, aug. 2027) sú pevne dané nariadením. **Termín august 2026 pre vysokorizikové systémy** je nosný dátum pre väčšinu rámcovania príležitosti v tejto kapitole.
> - **Vykonávacie usmernenia, harmonizované normy a postupy posudzovania zhody** sa stále publikujú, najmä Úradom pre AI, ENISA a európskymi normalizačnými organizáciami. Očakávajte zmysluplný nový materiál počas rokov 2026 – 2027.
> - **Národná transpozícia a určenie príslušných orgánov** sa líšia podľa členského štátu a vo viacerých jurisdikciách sa stále finalizujú. Dôsledky pre verejné obstarávanie (posledná časť kapitoly) sú obzvlášť špecifické pre členský štát.
> - **Ceny služieb** (posúdenia 20 – 50 tis. $, monitorovanie 3 – 10 tis. $/mesiac) sa stlačia, ako trh dozreje za úvodnú tlačenicu súladu, pravdepodobne 18 – 24 mesiacov po tom, ako termín august 2026 udrie.
>
> Pred citovaním klientom znovu overte zákonné odkazy voči aktuálnemu konsolidovanému zneniu nariadenia (EÚ) 2024/1689.

---

*Ďalej: [Kapitola 12: Cenové modely a balenie](12_pricing_models.md)*
