# Kapitola 1: Moment GenAI pre poskytovateľov IT služieb

> **V skratke**
>
> - Dvadsať rokov bol biznis o prevádzkovaní infraštruktúry medzi dodávateľom a klientom. GenAI to pre polovicu trhu láme: dodávateľ je teraz lacnejší než prostredník.
> - Dve klientske reality. Klienti otvorení cloudu si môžu kúpiť AI od hyperškálových firiem 5 – 15× lacnejšie, než ju viete obslúžiť vy pri porovnateľnej kvalite modelu. Klienti vyžadujúci on-prem stále potrebujú presne to, čo ste vždy predávali: spravovanú infraštruktúru.
> - Otázky, ktoré klienti dnes kladú (ktorý model, ako udržať dáta súkromné, ako integrovať, ako hodnotiť kvalitu, ako byť v súlade), sú otázky odbornosti, nie hostingu.
> - Päťročná otázka: budú vaše hlavné tržby pochádzať z infraštruktúry, ktorú prevádzkujete, alebo z odbornosti, ktorú dodávate?
>
> **Číslo, ktoré si zapamätať:** 5 – 15×, cenová výhoda poskytovateľov API pri porovnateľnej kvalite oproti vášmu vlastnému hostingu, pre klientov, ktorí si môžu slobodne vybrať. Kapitola 4 tento rozsah odvodzuje.

---

## Biznis, ktorý dával dokonalý zmysel

Dvadsať rokov matematika fungovala nádherne.

Stredne veľký európsky poskytovateľ IT služieb, taký s 50 až 500 zamestnancami, pôsobiaci z Prahy, Bratislavy, Varšavy alebo Mníchova, postavil svoj biznis na vrstvenej ponuke. V základe: hosting a infraštruktúrne služby generujúce stabilné opakované tržby. Navrchu: profesionálne služby (architektonické poradenstvo, systémová integrácia, bezpečnostné audity, práca na súlade), kde bývali skutočné marže.

Toto rozlíšenie je dôležité. Mnohí poskytovatelia IT služieb dosahujú 30 – 60 % hrubú maržu na profesionálnych službách a poradenstve, kým hosting infraštruktúry beží na 15 – 30 %. Hosting bol často kotvou, ktorá vás dostala do vzťahu s klientom; tržby zo služieb boli to, čo robilo biznis ziskovým. Typické portfólio zahŕňalo kolokáciu a hosting, spravovanú prevádzku infraštruktúry so SLA, projekty migrácie do cloudu a rastúcu vrstvu poradenskej a integračnej práce navrchu.

Tento model bol odolný. Keď začiatkom druhej dekády udrela cloudová vlna, poskytovatelia sa prispôsobili. Namiesto predaja fyzického serverového priestoru predávali cloudovú kapacitu od AWS, Azure alebo Google Cloud a pridávali navrch správu, migráciu a optimalizáciu. Marže na infraštruktúre sa stlačili, ale vrstva služieb sa rozšírila: poradenstvo v cloudovej architektúre, optimalizácia nákladov, správa multi-cloudu. Celková ekonomika stále fungovala.

Keď prišla mobilná revolúcia, jadra biznisu sa sotva dotkla. Mobilné aplikácie potrebovali backendy. Backendy potrebovali hosting. Cyklus pokračoval.

Ani prechod na DevOps a kontajnery, hoci vyžadoval nové zručnosti, model zásadne neohrozil. Klastre Kubernetes musia niekde bežať. Niekto ich musí prevádzkovať. Hodnotový reťazec sa posunul, ale podkladová logika, *prevádzkujeme infraštruktúru, aby ste vy nemuseli*, ostala nedotknutá.

To už neplatí.

## Prečo GenAI láme model prostredníka

Každý predchádzajúci technologický posun zachoval základnú ekonomickú štruktúru: poskytovateľ IT služieb sedel medzi technologickým dodávateľom a klientom a pridával hodnotu znižovaním zložitosti a poskytovaním prevádzkovej odbornosti. Marža poskytovateľa pochádzala z rozdielu medzi tým, čo platil za výpočtový výkon, a tým, čo účtoval klientom za spravovaný výpočtový výkon.

Generatívna AI túto štruktúru obracia a pochopiť prečo vyžaduje pozrieť sa, ako ekonomika naozaj funguje.

Keď predávate cloudový hosting, kupujete výpočtový výkon za hromadnú sadzbu a predávate ho s prirážkou. Virtuálny stroj, ktorý vás u hyperškálovej firmy stojí 200 EUR mesačne, môže ísť klientovi za 300 – 350 EUR so správou v cene. Klient prémiu platí ochotne, lebo kupuje vašu prevádzkovú odbornosť, váš monitoring, vaše záruky SLA: vašu ľudskú prácu obalenú okolo výpočtového výkonu.

Teraz zvážte, čo sa deje s veľkými jazykovými modelmi. Poprední poskytovatelia API (OpenAI, Anthropic, Google, Mistral) fungujú v rozsahoch, ktoré produkujú mimoriadnu jednotkovú ekonomiku. Milión tokenov spracovaných schopným modelom strednej triedy ako Gemini Flash stojí cez API 0,30 $ na vstupe a 2,50 $ na výstupe. Vlajkový model ako Claude Opus 4.6 stojí 5,00 $ za milión vstupných tokenov a 25,00 $ za milión výstupných tokenov. Tieto ceny stabilne klesajú a nič nenaznačuje, že by prestali.

Tu je nepríjemná aritmetika. Keby ste chceli vo vlastnej réžii hostovať porovnateľný open-source model (povedzme model so 120 miliardami parametrov bežiaci na vlastnej GPU infraštruktúre), samotný hardvér na obsluhu 100 súbežných používateľov by stál 600 000 až 1,2 milióna dolárov na nákup. Prenájom ekvivalentnej cloudovej GPU kapacity vychádza na 25 000 až 50 000 dolárov mesačne. A to ešte pred započítaním talentu v ML inžinierstve na prevádzku, práce na optimalizácii inferencie, aktualizácií modelov a nevyhnutného cyklu obnovy hardvéru.

Pre väčšinu záťaží vo väčšine rozsahov, v akých poskytovatelia IT služieb v EÚ pôsobia, je API 5- až 15-krát lacnejšie než vlastný hosting modelu ekvivalentnej kvality (kapitola 4 tento rozsah odvodzuje a ukazuje, prečo je štrukturálny). Nie o trochu lacnejšie, nie okrajovo lacnejšie: dramaticky, štrukturálne lacnejšie.

> **Jadro problému**: V tradičných IT službách bol prostredník lacnejší než dodávateľ, lebo prostredník agregoval dopyt. V GenAI je dodávateľ lacnejší než prostredník, lebo dodávateľ agreguje ponuku v rozsahu, akému sa žiadny prostredník nevyrovná.

Toto je štrukturálny dôsledok toho, ako veľké jazykové modely fungujú, nie dočasná trhová podmienka. Natrénovať frontier model stojí stovky miliónov dolárov, ale keď je natrénovaný, marginálny náklad na obsluhu jednej ďalšej požiadavky je nepatrný a ďalej sa zmenšuje, ako infraštruktúra poskytovateľa škáluje. Hyperškálové firmy, ktoré tieto modely trénujú a obsluhujú, fungujú v rozsahu, kde už amortizovali náklady na tréning naprieč miliónmi platiacich používateľov. Túto nákladovú štruktúru nezopakujete rackom GPU vo frankfurtskom dátovom centre.

## Dva druhy klientov, dve rôzne reality

Kým usúdime, že starý model je mŕtvy, musíme urobiť dôležité rozlíšenie. Nie všetci klienti sú rovnakí a ekonomika sa vyvíja veľmi rôzne podľa toho, ktorý druh obsluhujete.

**Klienti otvorení cloudu** môžu posielať dáta externým API. Môžu mať nejaké politiky správy dát, ale ich kľúčové biznisové dáta sú už v AWS alebo Azure. Pre týchto klientov platí ekonomika prostredníka opísaná vyššie v plnej sile. Môžu si zajtra zaregistrovať API kľúč OpenAI a argument pre vašu vlastne hostovanú infraštruktúru sa na cene predáva ťažko.

**Klienti vyžadujúci on-prem** nemôžu alebo nechcú posielať dáta externým poskytovateľom API. Patria sem banky pod prísnymi regulačnými rámcami, poskytovatelia zdravotnej starostlivosti narábajúci s dátami pacientov, obranní dodávatelia, organizácie verejného sektora, právne kancelárie s povinnosťou mlčanlivosti voči klientom a každý podnik, ktorého tímy pre súlad alebo právne tímy nakreslili tvrdú čiaru proti externým AI API. Pre týchto klientov je cena API hyperškálovej firmy irelevantná; nie je to možnosť, ktorú si môžu vybrať.

Toto rozlíšenie záleží nesmierne, lebo pre on-prem klientov ekonomické porovnanie neznie „vaša cena vlastného hostingu vs. cena API“, ale skôr:

- Vaša spravovaná AI služba vs. klient stavajúci vlastnú GPU infraštruktúru a najímajúci vlastný ML tím
- Vaša spravovaná AI služba vs. klient bez akejkoľvek AI

To je tradičná ekonomika IT služieb. A funguje. Klient, ktorý potrebuje on-prem AI a nemá odbornosť na jej prevádzku, zaplatí rozumnú prémiu za vašu prevádzkovú odbornosť, tak ako ju platil za spravované servery, spravované databázy a spravované klastre Kubernetes.

Podiel vašej klientskej základne v každej kategórii určí, koľko z vášho tradičného biznis modelu prežije prechod ku GenAI. Na silne regulovaných trhoch EÚ (najmä v strednej a východnej Európe, kde klienti z bankovníctva, poisťovníctva, zdravotníctva a verejného sektora často majú prísne požiadavky na rezidenciu dát) môže byť on-prem segment väčší, než si myslíte.

> **Kľúčové rozlíšenie:** Pre klientov otvorených cloudu sú poskytovatelia API 5 – 15× lacnejší než vy pri porovnateľnej kvalite a model prostredníka je rozbitý. Pre klientov vyžadujúcich on-prem súťažíte s klientovou alternatívou urobiť si to sám alebo sa zaobísť bez, nie s poskytovateľmi API. Sú to dve zásadne rôzne ekonomické hry a musíte vedieť, ktorú hráte s ktorým klientom.

Obe ekonomiky skúmame podrobne v kapitole 3. Zatiaľ pochopte, že obraz je jemnejší než „vlastný hosting nikdy nefunguje“. Závisí úplne od toho, koho obsluhujete a prečo.

## Predchádzajúci scenár sa neprenáša (pre polovicu vašich klientov)

Poskytovatelia IT služieb už technologické prechody prežili a existuje lákavý vzor, do ktorého sa dá spadnúť: „Prispôsobili sme sa cloudu. Prispôsobili sme sa kontajnerom. Prispôsobíme sa AI.“

Pre klientov otvorených cloudu je táto sebadôvera nemiestna. GenAI nie je primárne nová infraštruktúrna kategória (ďalšia vec na hosting, ďalšia vec na správu). Infraštruktúrnu vrstvu čoraz viac komoditizujú samotní poskytovatelia modelov. OpenAI, Anthropic a Google predávajú plne spravovanú inferenčnú infraštruktúru, nie iba modely. Nie je tu žiadny server, ktorý by ste spravovali. Nie je tu žiadny klaster, ktorý by ste optimalizovali. Klient si môže za päť minút zaregistrovať API kľúč a začať posielať požiadavky.

Pre klientov vyžadujúcich on-prem je však inštinkt prispôsobiť sa v skutočnosti správny. Títo klienti stále potrebujú niekoho, kto obstará GPU hardvér, nasadí modely, optimalizuje inferenciu, rieši aktualizácie a monitoruje produkčné systémy. To je prevádzková odbornosť obalená okolo infraštruktúry, presne služba, ktorú predávate desaťročia. Technológia sa mení (GPU namiesto CPU, vLLM namiesto Apache), ale vzťah je rovnaký: prevádzkujete zložitú infraštruktúru, aby klient nemusel.

Výzvou je, že aj pri on-prem klientoch sa požiadavky na zručnosti posunuli. Spravovať GPU klastre a inferenčné ML pipeline je niečo iné než spravovať virtuálne stroje a databázy. Tomuto prechodu sa podrobne venujeme v kapitole 13.

### Čo klient teraz naozaj potrebuje

Skutočné výzvy, ktorým klienti pri GenAI čelia, sú iné než tie, ktorým čelili pri cloude alebo mobile:

- **Ktorý model použiť na ktorú úlohu?** Krajina sa mení mesačne. Model, ktorý bol pred šiestimi mesiacmi najlepší na generovanie kódu, môžu dnes prekonávať traja konkurenti za polovičnú cenu.
- **Ako udržať svoje dáta súkromné?** Mnohé európske organizácie, najmä v regulovaných odvetviach, nemôžu bez starostlivej architektonickej práce posielať dáta zákazníkov americkým poskytovateľom API.
- **Ako integrovať AI do existujúcich pracovných postupov?** To je otázka systémovej integrácie a biznis procesov, nie infraštruktúry.
- **Ako hodnotiť kvalitu?** Na rozdiel od webového servera, ktorý buď odpovie, alebo nie, LLM môže produkovať jemne nesprávny, zaujatý alebo halucinovaný výstup. Testovanie a validácia vyžadujú úplne nové prístupy.
- **Ako byť v súlade s AI Actom EÚ?** Regulačné požiadavky na nasadzovanie AI systémov v Európe sú skutočné a rastú a väčšina klientov netuší, kde začať.

Všimnite si, čo majú tieto otázky spoločné: sú o odbornosti, integrácii, hodnotení a súlade, nie primárne o hostingu alebo infraštruktúre. To je ten posun: od predaja výpočtového výkonu k predaju inteligencie o inteligencii.

## Päťročná otázka

Tu je otázka, pri ktorej by práve teraz mal sedieť každý vedúci tím poskytovateľa IT služieb v Európe:

> **Budú o päť rokov vaše hlavné tržby pochádzať z infraštruktúry, ktorú prevádzkujete, alebo z odbornosti, ktorú dodávate?**

Nie je to rečnícka otázka a odpoveď nie je zjavná. Obe cesty môžu fungovať, ale vyžadujú zásadne odlišné investície, odlišný talent, odlišné vzťahy s klientmi a odlišné cenové modely.

Cesta infraštruktúry je širšia, než mnohí komentátori naznačujú, najmä na európskom trhu. Regulované odvetvia, ktoré nemôžu používať externé API, organizácie s prísnymi požiadavkami na dátovú suverenitu, veľkoobjemové záťaže, kde sa nákladová krivka nakloní v prospech vlastného hardvéru, a scenáre nasadenia na okraji siete, to všetko predstavuje skutočný dopyt po spravovanej AI infraštruktúre. Na niektorých trhoch EÚ môže tento segment predstavovať väčšinu podnikového dopytu po AI. Túto ekonomiku podrobne skúmame v kapitolách 3 a 4.

Cesta odbornosti je širšia, ale vyžaduje transformáciu. Ak sa vaša organizácia obráti k AI poradenstvu, integrácii, testovaniu, súladu a spravovaným službám inteligencie, adresovateľný trh je veľký a rastie. Ale je to iný biznis než ten, ktorý ste prevádzkovali. Vyžaduje iných ľudí, iné obchodné postupy a ochotu pustiť sa pohodlnej predvídateľnosti opakovaných tržieb z infraštruktúry.

Väčšina poskytovateľov skončí s nejakou kombináciou oboch. Otázka je, ktorá vedie.

## Existujú životaschopné cesty, ale nie tá stará

Buďme priami v tom, čo táto brožúra tvrdí a čo nie.

Netvrdíme, že poskytovatelia IT služieb v EÚ sú odsúdení na zánik. Európsky trh IT služieb je veľký, rastie a tvarujú ho regulačné a kultúrne faktory, ktoré vytvárajú skutočné konkurenčné výhody pre lokálnych poskytovateľov. Obavy o dátovú suverenitu, požiadavky na súlad s AI Actom EÚ, jazyková a kultúrna špecifickosť a číra zložitosť integrácie AI do existujúcich podnikových pracovných postupov. To všetko vytvára dopyt, ktorý samotné hyperškálové firmy nedokážu uspokojiť.

Netvrdíme ani, že každý poskytovateľ sa musí cez noc stať AI firmou. Transformácia je spektrum a správna pozícia na tom spektre závisí od vašich súčasných schopností, klientskej základne a chuti riskovať.

Čo tvrdíme, je toto: **starý scenár potrebuje zásadnú úpravu, ale nie úplné opustenie.** Pre klientov otvorených cloudu predaj výpočtového výkonu s prirážkou proti cenám API hyperškálových firiem nefunguje. Pre klientov vyžadujúcich on-prem je spravovaná AI infraštruktúra prirodzeným a ziskovým rozšírením vášho existujúceho biznisu. Pre oboch pridanie služieb odbornosti, integrácie, súladu a hodnotenia navrch infraštruktúry vytvára podstatne viac hodnoty než infraštruktúra samotná.

Poskytovatelia, ktorí rozpoznajú dvojakú povahu tohto trhu (a podľa toho investujú), majú okno príležitosti. Trh GenAI je stále dosť mladý na to, aby bola odbornosť vzácna, osvedčené postupy ešte neustálené a klienti skutočne neistí, ako postupovať. Tá neistota je vaša príležitosť. Pre niektorých klientov to znamená „budeme to hostovať za vás, lebo vy do cloudu nemôžete“. Pre iných to znamená „spravíme, aby AI fungovala vo vašom kontexte, nech model beží kdekoľvek“.

## Čo vám táto brožúra ukáže

Kapitoly, ktoré nasledujú, stavajú argument systematicky.

**Kapitoly 2 – 4** kladú ekonomický základ. Prejdeme, ako veľké jazykové modely naozaj bežia na úrovni hardvéru, potom postavíme podrobné porovnanie nákladov medzi vlastným hostingom a používaním API v rôznych rozsahoch, pre klientov otvorených cloudu aj vyžadujúcich on-prem. Vysvetlíme, prečo je nákladová výhoda hyperškálových firiem štrukturálna, nie dočasná, a identifikujeme, kde vlastný hosting stále dáva ekonomický zmysel.

**Kapitola 5** skúma cestu najmenšieho odporu: predaj a implementáciu vstavanej AI od vašich existujúcich dodávateľských partnerov: Microsoft Copilot, SAP Joule, ServiceNow AI a ďalších. Pre mnohých poskytovateľov je to najrýchlejšia cesta k tržbám z AI.

**Kapitoly 6 – 8** skúmajú tri ďalšie nezávislé biznis modely: proxy pre súkromie (smerovanie AI cez vyhovujúcu európsku vrstvu), lokálne nasadenie na zariadeniach zamestnancov (rastúci trh, ako sa zlepšujú modely na zariadení) a testovanie, bezpečnosť a agentnú infraštruktúru (kde sa prevádzková odbornosť poskytovateľa priamo mapuje na nové požiadavky AI).

**Kapitola 9** rieši nepríjemnú internú otázku: ako AI premieňa váš vlastný model dodávania služieb. Ak AI zvládne 40 – 60 % tiketov L1, mení to vašu nákladovú štruktúru, obsadenie aj ceny.

**Kapitoly 10 – 14** pokrývajú širšiu strategickú krajinu: ako sa posúva dynamika lock-inu, ako AI Act EÚ vytvára skutočnú príležitosť v súlade, ako naceňovať a baliť AI služby, kde nájsť talent na trhu strednej a východnej Európy a čo sa stane, ak neurobíte nič. Posledná kapitola poskytuje konkrétnu 18-mesačnú cestovnú mapu.

V celom texte používame skutočné čísla. Cenové dáta uvádzané v tejto brožúre sú aktuálne k aprílu 2026 a čerpané z verejných cenníkov, zverejnených sadzieb za prenájom GPU a trhových cien hardvéru. Kde odhadujeme, ukazujeme svoje predpoklady. Kde sú čísla neisté, hovoríme to.

> **Čo si z tejto kapitoly odniesť**: Prechod ku GenAI vytvára dve odlišné reality. Pre klientov otvorených cloudu sú poskytovatelia API 5 – 15× lacnejší než vy pri obsluhe AI porovnateľnej kvality; model prostredníckej prirážky je rozbitý. Pre klientov vyžadujúcich on-prem je spravovaná AI infraštruktúra životaschopný, ziskový biznis, ktorý stavia na vašej existujúcej odbornosti. Väčšina poskytovateľov IT služieb v EÚ bude obsluhovať oba segmenty a víťazmi budú tí, ktorí pochopia, ktorú ekonomickú hru hrajú s ktorým klientom. Zvyšok tejto brožúry vám dáva čísla a stratégie pre obe.

---

> **Strážca čerstvosti** · *overené apríl 2026 · odhadovaný polčas rozpadu: ~12 – 18 mesiacov*
>
> Štrukturálny argument tejto kapitoly (prostrednícka prirážka rozbitá pre klientov otvorených cloudu, spravovaná infraštruktúra životaschopná pre klientov vyžadujúcich on-prem) je trvanlivý. Užšie tvrdenia, ktoré treba časom znovu overiť:
>
> - Konkrétny pomer „5 – 15× lacnejšie“ API vs. vlastný hosting pri porovnateľnej kvalite sa prepočítava v kapitolách 3 a 4 v každom vydaní; sledujte, či sa to číslo rozšíri (ako hyperškálové firmy nasadia viac vlastného kremíka) alebo zúži (ako sa zlepší efektivita open-source).
> - Rozdelenie medzi klientmi v EÚ otvorenými cloudu a vyžadujúcimi on-prem sa posúva, ako hyperškálové firmy pridávajú funkcie rezidencie dát v EÚ; podrobnosti pozri v Strážcovi čerstvosti kapitoly 6.

---

*Ďalej: [Kapitola 2: Ako veľké jazykové modely naozaj bežia](02_infrastructure_economics.md)*
