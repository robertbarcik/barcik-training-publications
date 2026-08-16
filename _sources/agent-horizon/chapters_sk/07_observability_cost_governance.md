# Kapitola 7: Pozorovateľnosť, vyhodnocovanie a náklady

---

Vojdite do miestnosti, kde inžinieri debatujú o frameworkoch na agentov, a budete počuť o riadiacom toku, správe stavu a multiagentných vzoroch. Vojdite do miestnosti, kde tí istí inžinieri vysvetľujú nasadenie svojho agenta finančnému riaditeľovi, a budete počuť tri otázky: *funguje to, ako to vieme a koľko nás to stojí?*

V prvej miestnosti sa vedú technické hádky. V druhej sa schvaľujú rozpočty. Podniky, ktoré s agentmi uspejú, prišli na to, že práve v druhej miestnosti musí pristáť väčšina ich inžinierskeho úsilia. Táto kapitola je o vrstve, ktorá leží naprieč každým frameworkom, každým modelom a každým protokolom a ktorá sa stáva rozdielom medzi nasadeným pilotom a odloženým.

V cloudových pojmoch je to vrstva Datadogu. Vrstva Splunku. Vrstva, ktorá v zrelých cloudových nasadeniach predstavuje významný podiel celkových výdavkov na infraštruktúru, a v zrelých agentných nasadeniach to bude rovnako.

## Prečo je pozorovateľnosť agentov ťažšia než pozorovateľnosť mikroslužieb

V klasickej webovej službe je pozorovateľnosť dobre pochopená. Logujte požiadavky, sledujte distribuované volania, merajte latencie, upozorňujte na chyby, počítajte SLO. Povrch je stabilný. Chybové režimy sú známe. Agenti väčšinu týchto predpokladov rozbíjajú.

**„Správny“ výstup nie je dobre definovaný.** Webová služba buď vráti 200, alebo nie. Agent vráti prirodzený jazyk, volanie nástroja, čiastočnú odpoveď, sebaisto nesprávnu odpoveď. Neexistuje jediný stavový kód pre „agent sa mýlil“.

**Vykonávanie je nedeterministické.** Ten istý agent, ten istý vstup, rôzne volané nástroje, v rôznom poradí, s rôznymi argumentmi naprieč behmi. Ladenie reprodukovaním zlyhávajúceho prípadu je ťažšie.

**Spätná väzba je pomalá.** Chyba v službe vyvolá okamžité upozornenie. Chyba kvality v agentovi sa nemusí ukázať, kým používateľ o týždeň neoznačí nepresnú odpoveď, a dovtedy môžu byť vinná verzia modelu, prompt aj rozhovor už iné.

**Náklady sú naviazané na kvalitu.** Upovedaný agent náchylný na halucinácie nie je len nesprávny; je aj drahý, lebo volá viac nástrojov, častejšie opakuje a spáli viac tokenov na interakciu. Kvalita a náklady sú prepletené.

Dôsledok: klasická pozorovateľnosť je nutná, ale nie postačujúca. Potrebujete stopy a chyby ako pri mikroslužbe. Potrebujete aj vrstvu špecifickú pre agentov (zaznamenávanie trajektórií, vyhodnocovanie, priraďovanie nákladov na tokeny, pracovné postupy ľudskej revízie), ktorá v tradičných nástrojoch nemá obdobu.

## Štyri piliere

Nástroje špecifické pre agentov, ktoré vznikli v rokoch 2025 až 2026 (LangSmith, Langfuse, Phoenix, Braintrust), sú rôzne pokusy o ten istý problém. Organizujú sa okolo štyroch pilierov.

**Stopy.** Každá interakcia agenta vyprodukuje stopu: postupnosť volaní modelu, vyvolaní nástrojov, delegovaní podagentom a prechodov stavu, ktoré viedli k výstupu. Dobrá stopa vám dovolí prehrať presne to, čo sa stalo, s každým promptom, odpoveďou a medzirozhodnutím viditeľným. Pre ladenie nevyhnutné. Pre audit často povinné podľa regulačných rámcov, ako je AI Act.

**Vyhodnocovanie.** Agent bez testovacieho postroja je agent, ktorého neviete zlepšiť. Môžete zmeniť prompt, vymeniť model, upraviť graf a dúfať; alebo spustiť zmeny nad korpusom reprezentatívnych vstupov so známymi očakávanými výstupmi a zmerať rozdiel. Vyhodnocovanie je najmenej okázalá časť inžinierstva agentov a jedna z tých s najväčšou pákou. Tímy, ktoré investujú do dobrých vyhodnocovacích sád, dodávajú rýchlejšie, iterujú s väčšou istotou a chytia regresie skôr než používatelia.

Najzáludnejšia časť vyhodnocovania agentov je, že „správny“ výstup je často rozsah, nie reťazec. Tu prichádza vyhodnocovanie *LLM ako sudca*: použitie jedného modelu na známkovanie výstupov iného podľa hodnotiacich kritérií. Ak sa robí dobre, dramaticky škáluje vyhodnocovanie. Ak sa robí zle, nemeria nič a pritom vyzerá dôkladne. Pohľad v rozsahu brožúry na to, ako LLM sudcovia obstoja pod nepriateľským tlakom, nájdete v našej výskumnej správe [Warden](/warden/).

**Priraďovanie nákladov.** Agenti produkujú náklady na viacerých vrstvách: inferencia modelu, vyvolania nástrojov (platené API), výpočtový výkon orchestrácie (úložisko trvanlivosti LangGraphu, hostovaný sandbox OpenAI), ľudská revízia. Priraďovanie týchto nákladov podľa používateľa, pracovného postupu, funkcie a tímu je to, čo oddeľuje nasadenie, ktoré ostane v rozpočte, od nasadenia, ktoré prepáli kvartálny rozpočet na AI za šesť týždňov. Nástroje sú stále rané (väčšina podnikov si stavia interné dashboardy, namiesto toho, aby kupovala hotové), ale rýchlo sa zlepšujú.

Konkrétne varovanie: náklady na tokeny jednej interakcie agenta sa môžu líšiť o rád v závislosti od volaní nástrojov, natiahnutého kontextu a opakovaní. Pozorovateľnosť nákladov musí byť na úrovni interakcie, nie iba mesiaca, inak vás dlhý chvost pohryzie.

**Signály kvality.** Okrem štruktúrovaného vyhodnocovania potrebujú produkční agenti ľahké priebežné signály. Palec hore/dole od používateľa, miery odchodu, vzory nadväzujúcich správ („to je zle“, „nie, myslel som...“), čas do vyriešenia. Agentné ekvivalenty miery chýb a percentilov latencie. Ich zachytávanie a spätné vkladanie do vyhodnocovacích sád a iterácie promptov je mašinéria priebežného zlepšovania.

## Krajina nástrojov

| Nástroj | Pozícia |
|---|---|
| LangSmith | Ekosystém LangChain/LangGraph. Najhlbšia integrácia s LangGraphom, najsilnejší príbeh vyhodnocovania + stôp v nezávislom tábore. |
| Langfuse | Open-source alternatíva, nezávislá od dodávateľa, silná možnosť vlastného hostovania pre dátovo citlivé nasadenia. |
| Phoenix (Arize) | Zameraný na vyhodnocovanie, široká podpora modelov, väzby na nástroje pozorovateľnosti ML. |
| Braintrust | Vyhodnocovanie na prvom mieste so zameraním na LLM ako sudcu vo veľkom. |
| W&B Weave | Rozšírenie Weights & Biases do pozorovateľnosti LLM. |
| Natívne od dodávateľa | Každé dodávateľské SDK dodáva vlastnú základnú pozorovateľnosť. Použiteľné pre jedného dodávateľa, slabé pre viacerých. |

Strategický bod: vrstva pozorovateľnosti agentov sa rýchlo stáva vlastnou softvérovou kategóriou, analogickou k APM pre cloud. Podniky minú skutočné peniaze na nástroje, ktoré robia rozdiel medzi prevádzkyschopným a nefunkčným.

## Riadenie nákladov nie je voliteľné

Jedno z najľahšie prehliadnuteľných zlyhaní v raných nasadeniach agentov sú utekajúce výdavky. Dobre navrhnutý agent, ktorý volá tri nástroje na interakciu po 0,003 € každý, je lacný. Ten istý agent pod tlakom (viac opakovaní, viac kontextu, viac volaní nástrojov, viac sebareflexie) môže ľahko zdesaťnásobiť svoje náklady bez toho, aby si to niekto všimol, kým nepríde faktúra.

Malá množina praktík oddeľuje disciplinované nasadenia od nedisciplinovaných. **Nákladové rozpočty na interakciu** (agent pozná vlastný nákladový limit a zastaví sa, keď sa k nemu blíži). **Stropy na používateľa alebo nájomcu** (zneužívajúci používateľ alebo chybná integrácia by nemali za deň spáliť mesačný rozpočet na AI). **Smerovanie modelov podľa nákladov** (drahý model na ťažké otázky, lacný model na smerovanie a klasifikáciu; úspory sa rýchlo úročia). **Rozpočtovanie volaní nástrojov** (ak agent volá päť nástrojov, keď by stačili dva, je to otázka kvality aj nákladov). **Kompakcia a hygiena kontextu** (kompakcia kontextu, cachovanie promptov, disciplinované promptovanie vedia znížiť náklady trojnásobne a viac bez dotknutia sa kvality modelu).

Toto nie je exotický materiál. Je to tá istá disciplína, ktorú si cloudoví inžinieri vyvinuli okolo rezervovaných inštancií, automatického škálovania a spätného účtovania podľa značiek. Agentná éra si vyvinie vlastnú verziu. Biznisovú stránku tejto disciplíny (čo tokeny naozaj stoja, kto platí a ktoré cenové modely prežijú kontakt s agentmi) pokrýva v rozsahu brožúry [The Token Economics](/token-economics/). Podniky, ktoré si túto disciplínu vybudujú skoro, minú podstatne menej na jednotku hodnoty z agentov.

## Regulačná vynucovacia sila

Najmä pre európske podniky (a kapitola 9 sa k tomu vracia) pozorovateľnosť nie je len pohodlie pre vývojárov. Je to regulačná požiadavka. AI Act vyžaduje od subjektov nasadzujúcich vysokorizikové AI systémy uchovávať logy umožňujúce sledovateľnosť počas celého životného cyklu systému, uchovávať ich aspoň šesť mesiacov a preukazovať ľudský dohľad. Tieto požiadavky bez vrstvy pozorovateľnosti splniť nemôžete.

Dôsledok: pre regulované podniky je stack pozorovateľnosti **infraštruktúrou súladu skôr než infraštruktúrou kvality**. Voľby (granularita stôp, doby uchovávania, kontroly prístupu, audítorské pracovné postupy) majú právne, nielen prevádzkové dôsledky. Kapitola 9 pokrýva architektúru nasadenia v súlade s pravidlami EÚ podrobne.

**Veľmi málo podnikov má v roku 2026 zavedenú zrelú prax pozorovateľnosti. Väčšina je niekde medzi „logujeme volania modelu“ a „máme dashboard, ale nikto sa naň nepozerá“. Medzera medzi týmito dvoma stavmi a „toto funguje“ je jediný najväčší prediktor toho, či agentný program dozreje na niečo strategické.**

---

*Ďalej: [Kapitola 8: Otázka lock-inu](08_lock_in_question.md)*
