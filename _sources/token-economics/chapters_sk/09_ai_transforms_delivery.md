# Kapitola 9: Keď AI mení vaše vlastné dodávanie

> **V skratke**
>
> - Tá istá AI, ktorú sa učíte predávať, mení spôsob, akým dodávate: 40 – 60 % odklonených ticketov je produkčná realita, nie predpoveď.
> - Ak vaše ceny účtujú vstupy (tickety, hodiny, licencie na používateľa) a AI vstupy zmenšuje, vaše tržby sa zmenšujú, kým fixné náklady ostávajú. Prejdite na ceny podľa výsledkov skôr, než vás k tomu klienti donútia.
> - Staff augmentation je zasiahnutý tvrdšie než servisný pult: time-and-materials predáva hodiny a AI zmenšuje hodiny na výsledok. Predávajte namiesto toho kapacitu a výsledky a rozdiel v produktivite si nechajte, namiesto toho, aby ste ho darovali.
> - Poctivá matematika stále funguje: odklon plus rýchlejší agenti znamenajú zhruba 3× kapacitu pri rovnakom počte ľudí, rozširovač marže, ak sa pohnete prví.
> - Najprv zaveďte AI vo vlastnej prevádzke. Vaše vlastné metriky pred a po sa stanú najdôveryhodnejšou obchodnou ponukou na trhu.
>
> **Číslo, ktoré si zapamätať:** 40 – 60 %, podiel rutinných ticketov, ktoré AI už v produkčných nasadeniach odkláňa.

Kapitoly 5 až 8 skúmali, ako predávať AI služby klientom: implementácie ekosystémov dodávateľov, proxy pre súkromie, lokálne nasadenia, testovanie, bezpečnosť a agentnú infraštruktúru. Na tom všetkom záleží. Ale je tu rozhovor, ktorý väčšina poskytovateľov IT služieb nevedie, a je to ten, ktorý rozhodne, či budú o tri roky ešte konkurencieschopní.

AI nie je len niečo, čo predávate; mení aj to, ako dodávate služby, ktoré už ponúkate.

Ak prevádzkujete prax spravovaných služieb (servisný pult, NOC, SOC, monitorovaciu prevádzku), AI ide po vašom modeli dodávania, či to plánujete, alebo nie. Poskytovatelia, ktorí to rozpoznajú a konajú prví, rozšíria svoje marže a naškálujú biznis. Tí, ktorí to ignorujú, sa ocitnú podťatí konkurentmi, ktorí zautomatizovali to, čo oni stále robia manuálne.

Táto kapitola je o vnútornej disrupcii, o ktorej nikto nechce hovoriť. Môže byť nepríjemná. Mala by byť.

---

## Servisný pult sa už mení

Najbezprostrednejší dopad je na servisnom pulte, funkcii podpory L1, ktorá tvorí základ väčšiny praxí spravovaných služieb. Čísla sa posunuli od špekulácie k prevádzkovej realite vo veľkom.

Odvetvové prieskumy kladú AI odklon nad **45 % prichádzajúcich B2B zákazníckych dopytov**, pričom sektory ako maloobchod a cestovanie prekračujú 50 %. Dobre navrhnuté AI systémy konzistentne dosahujú **40 – 60 % mieru odklonu** a horný koniec trhu tlačí ďalej: až **80 % rutinných dopytov** vybavených automaticky, bez ľudského zásahu.

To sú produkčné nasadenia vo veľkých podnikoch, nie laboratórne výsledky. Jedna poctivá výhrada: čísla nižšie sú dodávateľmi hlásené prípadové štúdie, výkladné skrine z vlastného marketingu platforiem, nie auditované odvetvové priemery. Čítajte ich ako „čo je dosiahnuteľné“, nie „čo je typické“:

| Firma / platforma | Metrika | Výsledok |
|---|---|---|
| Moveworks v Broadcome | Miera autonómneho vyriešenia | 88 % |
| Moveworks v Equinixe | Odklon ticketov | 68 % |
| Moveworks v Equinixe | Autonómne vyriešenie | 43 % |
| Zákazníci Aisery | Odklon ticketov | 75 % |
| Zákazníci Aisery | Úspora nákladov na personál podpory | 35 % |
| Unity | Odklonené tickety | 8 000 ticketov, úspora 1,3 milióna $ |
| NIB Health Insurance | Zníženie nákladov | 60 %, úspora 22 miliónov $ |

Dopad siaha za odklon. Agenti s asistenciou AI (ľudia pracujúci po boku AI nástrojov) riešia problémy o **47 % rýchlejšie** s o **25 % vyššou** mierou vyriešenia pri prvom kontakte. To znamená, že aj tickety, ktoré sa k človeku dostanú, sú vybavené efektívnejšie.

Zastavte sa na chvíľu pri tých číslach. Ak prevádzkujete 20-členný servisný pult a AI dokáže odkloniť 50 % prichádzajúcich ticketov a zároveň zrýchliť zvyšných agentov o 47 %, pozeráte sa na zásadne iný personálny model.

> **Nepríjemná matematika**: 50 % miera odklonu ticketov plus 47 % zlepšenie efektivity agentov znamená, že váš servisný pult by mohol zvládnuť zhruba trojnásobok súčasného objemu s rovnakým počtom ľudí. To je buď obrovská hrozba, alebo obrovská príležitosť, podľa toho, ako rýchlo sa pohnete.

---

## NOC a SOC: vyhorenie stretáva automatizáciu

Ak je transformácia servisného pultu o efektivite, transformácia NOC/SOC je o prežití. Personálna kríza v bezpečnostnej prevádzke je súčasná núdza, nie budúce riziko.

**71 % analytikov SOC hlási vyhorenie.** 64 % zvažuje odchod do roka. Takmer 70 % hlási poddimenzované tímy (Tines, prieskum *Voice of the SOC Analyst* medzi 468 analytikmi). Zďaleka nejde o pesimistický odľahlý prieskum, tieto čísla predstavujú štrukturálnu realitu odvetvia, ktoré generuje viac alertov, než ľudia dokážu spracovať.

AI tú medzeru zapĺňa, a zapĺňa ju rýchlo:

| Funkcia SOC/NOC | Zavedenie AI | Dopad |
|---|---|---|
| Triedenie a prioritizácia alertov | 73 % zautomatizovalo | 67 % hovorí o najväčšom okamžitom dopade AI |
| Obohacovanie alertov | 68 % zautomatizovalo | Znižuje manuálny prieskum na alert |
| Skrátenie času vyšetrovania | 60 %+ používateľov AI | Aspoň 25 % skrátenie, 21 % dosahuje >50 % |
| Reakcia na phishing | S asistenciou AI | Z 1 hodiny na 10 minút |

Metrika reakcie na phishing si zaslúži dôraz. Skrátenie reakčného času z hodiny na desať minút je zmena kategórie, nie prírastkové zlepšenie. Za čas, ktorý by ľudský analytik strávil vyšetrovaním jedného phishingového incidentu, pracovný postup s asistenciou AI vybaví šesť.

Pre poskytovateľov spravovaných bezpečnostných služieb to mení ekonomiku každého SOC kontraktu. Ak vaši SOC analytici s asistenciou AI zvládnu tri- až päťnásobný objem alertov, môžete buď obsluhovať viac klientov s tým istým tímom, alebo dodávať dramaticky lepšiu službu za tú istú cenu. Tak či tak je poskytovateľ, ktorý stále prevádzkuje čisto manuálny SOC, v štrukturálnej nevýhode.

---

## Samoopravná infraštruktúra: koniec rutinných alertov

Za servisným pultom a SOC mení AI aj samotné monitorovanie infraštruktúry. Samoopravné systémy (automatizované pracovné postupy, ktoré detegujú, diagnostikujú a riešia bežné infraštruktúrne problémy bez ľudského zásahu) sa posúvajú z okrajovej automatizácie na štandardnú prax.

ConnectWise hlási, že samoopravné pracovné postupy Automate už zvládajú **30 – 40 % rutinných alertov** bez ľudského zásahu. Výskum Gartneru zisťuje, že vyše **60 % veľkých podnikov** zavádza v roku 2026 samoopravné systémy poháňané AIOps, a analytické predpovede majú trh AIOps v ďalších piatich rokoch zhruba **zdvojnásobený**.

Čo to znamená pre poskytovateľa spravovaných služieb? Znamená to, že významná časť rutinnej monitorovacej a nápravnej práce, ktorá odôvodňuje váš mesačný paušál, sa automatizuje preč. Serveru došlo miesto na disku? Samooprava premaže logy. Služba spadla? Samooprava ju reštartuje. Certifikát exspiruje? Samooprava ho obnoví. To sú tickety každodenného chleba, ktoré zamestnávajú tímy NOC, a miznú.

> **Kľúčové posolstvo**: Samoopravná infraštruktúra neodstraňuje potrebu spravovaných služieb, ale odstraňuje potrebu *typu* spravovaných služieb, ktoré väčšina poskytovateľov momentálne dodáva. Hodnota sa posúva od „sledujeme vaše obrazovky a opravujeme rutinné problémy“ k „navrhujeme, nasadzujeme a optimalizujeme AI systémy, ktoré sledujú vaše obrazovky a opravujú rutinné problémy“.

---

## Hrozba pre model tržieb

Tu sa nepríjemnosť stáva finančnou.

Tradičné ceny MSP sú postavené na vstupoch: poplatky na používateľa, poplatky za ticket, sadzby za incident. Tieto modely predpokladajú relatívne stabilný vzťah medzi počtom používateľov alebo systémov a množstvom práce potrebnej na ich podporu.

AI ten predpoklad rozbíja.

**Ak účtujete za ticket a AI vyrieši 50 % ticketov, práve ste prišli o 50 % toho prúdu tržieb.** Práca zmizla a s ňou aj tržby. Analytici kanála predpovedajú, že sadzby na používateľa **klesnú v ďalších dvoch rokoch rádovo o 25 %** kvôli automatizácii: nie preto, že klienti sú nerozumní, ale preto, že náklady na dodanie služby skutočne klesajú a klienti to vedia.

Trh už reaguje. Aktivita fúzií a akvizícií MSP **vzrástla v roku 2024 o 50 %** (sledovatelia M&A v kanáli), keďže poskytovatelia, ktorí nedosiahnu efektivitu automatizácie, sa stávajú akvizičnými cieľmi pre tých, ktorí ju dosiahnu. Jedna trhová predpoveď (CyVent) predpokladá, že trh spravovaných bezpečnostných služieb sa konsoliduje zo zhruba **200 top MSSP na približne 120 do roku 2028**. To je 40 % pokles počtu nezávislých poskytovateľov.

Táto konsolidácia sleduje jasný vzorec, nie náhodu: poskytovatelia s pokročilou automatizáciou kupujú tých bez nej, absorbujú ich klientske základne a obsluhujú spojené portfólio s nižšími nákladmi. Ak ste poskytovateľ, ktorého kupujú, dostávate zlomok hodnoty, ktorú ste vybudovali. Ak ste ten, kto kupuje, kupujete tržby so zľavou, lebo viete, že tú istú službu dodáte s menším počtom ľudí.

| Hrozba | Časový rámec | Dopad |
|---|---|---|
| Stláčanie sadzieb na používateľa | Ďalších 24 mesiacov | Predpovedaný pokles 25 % |
| Pokles objemu ticketov z AI odklonu | Deje sa teraz | 40 – 60 % rutinných ticketov |
| Konsolidácia trhu MSP | Do roku 2028 | ~200 top MSSP na ~120 |
| Zrýchlenie M&A | Od roku 2024 | 50 % nárast MSP obchodov |

> **Hrozba pre tržby jednou vetou**: Ak váš cenový model účtuje vstupy (tickety, hodiny, incidenty) a AI vstupy znižuje, vaše tržby sa zmenšujú, kým vaše fixné náklady ostávajú, pokiaľ model nezmeníte prví.

---

## Zverák staff augmentation

Všetko vyššie je o spravovaných službách: ticketoch, alertoch, paušáloch. Pre mnohých poskytovateľov v strednej a východnej Európe je väčším biznisom prenájom ľudí. Vývojári, testeri a administrátori prenajímaní západným klientom na hodinu, na zmluvy time-and-materials, sú chrbtovou kosťou odvetvia IT služieb v SVE. Ak je to vaša tržbová základňa, táto časť je tá, pri ktorej sa treba zastaviť, lebo staff augmentation je voči AI exponovaný viac než servisný pult, nie menej.

Mechanizmus je ten istý, ktorý rozbíja ceny za ticket, aplikovaný na sadzobník. Time-and-materials predáva hodiny. AI zmenšuje hodiny potrebné na výsledok. Inžinier pracujúci so schopným programovacím asistentom dodá za deň zmysluplne viac a nákupný tím vášho klienta to vie, lebo jeho vlastné interné tímy pracujú rovnako. Ten rozhovor sa už deje pri rokovaniach o predĺžení: „vaši vývojári teraz používajú AI, tak prečo sa denná sadzba nepohla?“ Existujú len tri odpovede, ktoré klient prijme: nižšia sadzba, menej ľudí alebo iný spôsob nakupovania.

Expozícia je ostrejšia než v spravovaných službách zo štrukturálneho dôvodu. Paušál spravovaných služieb má zotrvačnosť; obnovuje sa, kým ho niekto nespochybní. T&M zmluva sa preceňuje pri každom predĺžení, každom novom zadaní, každom pridanom alebo odobratom človeku. Medzi produktivitou poháňanou AI a vašou tržbovou linkou nie je žiadny zmluvný nárazník. Keď každý inžinier dodá 1,5 – 2×, nemôžete fakturovať 1,5 – 2× hodín a žiadny klient vám nedovolí zvýšiť sadzby úmerne vášmu vybaveniu. Pri čistom T&M patrí zisk z produktivity klientovi a vy ste zaplatili za nástroje.

Obrat je prestať predávať hodiny a začať predávať kapacitu a výsledky. Nazvite to nearshoring 2.0: pracovné balíky s pevnou cenou vymedzené výstupom, tímové kapacitné predplatné („dodávací pod, ktorý za šprint dodá X“) a ceny viazané na výsledok, kde jednotkou je dokončená migrácia, dodaná sada funkcií, otestované vydanie. Logika zrkadlí matematiku servisného pultu z tejto kapitoly. Ak váš AI-augmentovaný tím dodá pracovný balík za 60 % starých hodín a naceníte ho na 85 % starej ceny, klient ušetrí, vy získate maržu a rozdiel v produktivite pristane na vašej strane stola, namiesto toho, aby bol darovaný cez defláciu fakturovaných hodín.

Poctivé problémy: vymedzovanie výsledkov je skutočne ťažké (z rovnakého dôvodu, prečo sú ceny podľa výsledkov najťažším modelom v kapitole 12), klienti zvyknutí na auditovateľné výkazy hodín sa môžu brániť nepriehľadným cenám a vaši projektoví manažéri sa musia naučiť odhadovať AI-augmentovanú rýchlosť, na ktorú ešte nikto nemá dlhé baseliny. Použiteľným mostom je zmiešaná zmluva: T&M so stropom a záväzkom produktivity, konvertujúca na balíky s pevnou cenou, ako obe strany budujú dôveru v nové baseliny. Čo použiteľné nie je, je čakať. Každý kvartál čistého T&M na AI-augmentovanom trhu je kvartál darovania vašich ziskov z produktivity nákupnému oddeleniu klienta.

---

## Obrat príležitosti: prečo je to vlastne dobrá správa

Teraz časť, pre ktorú sa oplatí túto kapitolu čítať a nielen sa jej báť.

AI je rozširovač marže, nielen znižovač počtu ľudí, ak prechod riadite premyslene. Dáta od poskytovateľov, ktorí AI už interne zaviedli, sú výrazné:

- **66 %** MSP uvádza automatizáciu ako spôsob škálovania **bez pridávania personálu**
- **76 %** zaznamenalo zvýšenú efektivitu; **40 %** uvádza nižšie mzdové náklady
- **78 %** klientov profesionálnych služieb zaznamenalo **nárast fakturovateľných hodín** (lebo AI vybavuje nefakturovateľnú administratívu)
- MSP hlásia zníženie prevádzkových nákladov o **30 – 50 %**

Matematika je priamočiara: **ak AI zníži vaše náklady na dodanie o 40 %, ale vy znížite ceny iba o 15 %, vaša marža rastie.** Ste ziskovejší na klienta a zároveň konkurencieschopnejší cenou. Toto je zriedkavý scenár, keď môžete súčasne zlepšiť marže aj trhovú pozíciu.

Zvážte konkrétny príklad. Prevádzkujete pult spravovaných služieb s 10 analytikmi, každý vás stojí 45 000 EUR s plnými nákladmi, podporujete 50 klientov za 3 000 EUR mesačne každý.

| Metrika | Pred AI | Po AI |
|---|---|---|
| Analytici na pulte | 10 | 6 (4 sa presunú do vašej novej praxe AI služieb) |
| Podporovaní klienti | 50 | 75 (rovnaká kvalita, o 50 % viac kapacity) |
| Mesačné tržby | 150 000 EUR | 210 000 EUR (75 klientov po 2 800 EUR, 7 % zníženie ceny) |
| Mesačné personálne náklady | 37 500 EUR (10 analytikov) | 37 500 EUR (všetkých 10 stále na výplatnej páske) + 5 000 EUR AI nástroje |
| Mesačná marža | 112 500 EUR (75 %) | 167 500 EUR (80 %) |

Všimnite si, že personálne náklady neklesajú: štyria presunutí analytici sú stále na vašej výplatnej páske. To je poctivá verzia tejto matematiky a stále funguje: znížili ste ceny, zvýšili tržby o 40 % a zlepšili maržu o päť percentuálnych bodov. A štyria presunutí analytici teraz budujú vašu prax AI služieb, fakturovateľnú prácu, ktorej tržby v tejto tabuľke ani nie sú započítané. Klienti sú spokojní, lebo platia menej. Váš tím je spokojný, lebo presunutí analytici robia zaujímavejšiu prácu. Váš biznis je silnejší v každej metrike.

To je príležitosť, ale iba ak sa pohnete skôr, než vám trh vynúti ruku.

---

## Evolúcia cenového modelu: od vstupov k výsledkom

Prechod od cien založených na vstupoch k cenám založeným na výsledkoch je prirodzeným dôsledkom toho, že automatizácia robí zo vstupov irelevantnú mieru hodnoty, a nie je voliteľný.

Priekopníci už ukazujú, ako to vyzerá. AI agent Fin od Intercomu účtuje **0,99 $ za AI vyriešenie**: nie za licenciu, nie za hodinu agenta, ale za vyriešenú konverzáciu. To zosúlaďuje tržby poskytovateľa s výsledkom klienta. Viac vyriešení znamená viac tržieb pre poskytovateľa a viac hodnoty pre klienta.

Pre poskytovateľov spravovaných služieb evolúcia sleduje jasnú cestu:

**Od**: cien za ticket, za používateľa, za hodinu, ktoré trestajú efektivitu.

**K**: cenám podľa výsledkov, ktoré ju odmeňujú.

Praktické štruktúry zahŕňajú:

- **Zmiešané základné poplatky s výsledkovými metrikami viazanými na AI**: základný paušál pokrývajúci službu plus bonusové zložky viazané na mieru automatizácie, priemerný čas do vyriešenia (MTTR) a plnenie SLA
- **Cenové koridory, ktoré sa flexibilne menia, ako AI zvláda viac práce**: mesačné poplatky, ktoré sa upravujú v definovaných pásmach, ako rastie miera automatizácie; klient platí menej za ticket, ale vy ziskovo vybavíte viac ticketov
- **Záruky výsledkov**: predávajte výsledok, nie činnosť. 99,9 % dostupnosť. MTTR pod 15 minút. 95 % miera vyriešenia pri prvom kontakte. Tieto záväzky sú to, na čom klientovi naozaj záleží, a s AI sú to záväzky, ktoré naozaj dokážete dodržať

> **Cenový postreh**: Predávajte výsledky (dostupnosť, rýchlosť vyriešenia, mieru vyriešenia pri prvom kontakte), nie vstupy ako hodiny, tickety alebo licencie. Keď AI zlacní vaše vstupy, ceny založené na vstupoch sú pretekmi ku dnu. Ceny podľa výsledkov vám umožnia zachytiť hodnotu toho, čo dodávate, nie náklady toho, ako to dodávate.

---

## Playbook vnútornej transformácie

Poznať krajinu nestačí. Tu je, čo naozaj urobiť, v poradí:

**1. Najprv zaveďte AI vo vlastnej prevádzke.** Jedzte vlastné varenie. Nasaďte AI triedenie na vlastnom servisnom pulte skôr, než ho budete predávať klientom. Implementujte AI obohacovanie alertov vo vlastnom SOC skôr, než ho navrhnete záujemcom. Ak ste netransformovali vlastné dodávanie, nemáte dôveryhodnosť hovoriť klientom, aby transformovali svoje.

**2. Merajte všetko.** Miery odklonu ticketov. Zlepšenia MTTR. Náklady na vyriešenie. Vyťaženosť analytikov pred a po AI. Miery automatizácie podľa kategórie ticketov. Tieto čísla sú vaše budúce obchodné podklady, nielen prevádzkové metriky.

**3. Použite dáta na stavbu externej ponuky.** „Skrátili sme vlastný čas vyriešenia o 47 % a náklady na ticket o 35 %; takto to isté urobíme pre vás.“ To je nekonečne presvedčivejšie než prezentácia dodávateľa. Je to dôkaz, nie sľub.

**4. Preškoľte vytlačený personál L1 na hodnotnejšiu prácu.** Dohľad nad AI, riešenie zložitých eskalácií, poradenstvo klientom, ladenie AI systémov, prompt engineering pre prevádzkové pracovné postupy. Ľudia, ktorí vášmu servisnému pultu rozumeli najlepšie, sú tí, ktorí dokážu spravovať AI, ktorá nahrádza jeho rutinné časti. Stratiť ich je plytvanie inštitucionálnymi znalosťami.

**5. Prepracujte cenové modely skôr, než vás o to klienti požiadajú.** Ak počkáte, kým klient povie „Prečo platím za tickety, ktoré rieši AI?“, vyjednávate zo slabosti. Ak proaktívne navrhnete model podľa výsledkov, ktorý klientovi ušetrí peniaze a zároveň ochráni vašu maržu, vyjednávate zo sily.

---

## Strategický imperatív

Buďme priami o tom, o čo ide.

Ak AI nezavediete interne, urobí to konkurent a podtne vás cenou, kým bude dodávať lepšiu službu. To je vzorec konsolidácie už viditeľný v dátach o M&A MSP, nie hypotéza.

Poskytovatelia, ktorí transformujú vlastné dodávanie prví, budú mať najdôveryhodnejšiu ponuku pre klientov. Budú mať metriky, prípadové štúdie a prevádzkovú zrelosť, ktorú žiadny marketing nenahradí. Budú mať aj štruktúru marže na investovanie do rastu, kým sa konkurenti stále snažia pokryť náklady.

Širšia trajektória je nezameniteľná. V prieskume Gartneru medzi vyše 700 CIO (2025) respondenti očakávajú, že do roku 2030 **žiadna IT práca nebude vykonaná ľuďmi bez asistencie AI**, **75 % vykonajú ľudia augmentovaní AI** a **25 % vykoná AI sama**. Gartner tiež predpovedá, že **40 % podnikových aplikácií bude do konca roka 2026 obsahovať agentov AI pre konkrétne úlohy**: nie 2030, budúci rok.

Otázka nie je, či AI transformuje váš model dodávania, ale či transformáciu povediete, alebo vás dobehne.

> **Čo si z tejto kapitoly odniesť**: Tá istá AI, ktorú sa učíte predávať klientom, súčasne mení spôsob, akým dodávate svoje existujúce služby. Poskytovatelia, ktorí ju zavedú interne ako prví (merajúc dopad, preškoľujúc tímy a prepracúvajúc ceny), rozšíria svoje marže, naškálujú kapacitu a postavia najdôveryhodnejšiu obchodnú ponuku na trhu. Poskytovatelia, ktorí čakajú, sa ocitnú na nesprávnej strane konsolidačnej vlny, ktorá už prebieha. Toto nie je problém budúcnosti. Čísla sú už skutočné, nástroje už dostupné a vaši konkurenti sa už hýbu.

---

> **Strážca čerstvosti** · *overené apríl 2026 · odhadovaný polčas rozpadu: ~9 mesiacov*
>
> Smer (AI stláča ekonomiku MSP, ceny podľa výsledkov vyhrávajú) je trvanlivý. Konkrétne metriky zostarnú:
>
> - **Miery odklonu z prípadových štúdií** (Moveworks 88 % v Broadcome, Aisera 75 %, NIB 60 % zníženie nákladov) sú ukotvené v konkrétnych nasadeniach dodávateľov; tieto čísla buď ďalej stúpnu, alebo ich každý rok nahradia novšie prípadové štúdie.
> - **Odvetvový priemer „45 % odklonu B2B ticketov“** kvartálne rastie, ako nástroje dozrievajú; očakávajte 55 – 65 % ako základ do roku 2027.
> - **Dáta o M&A MSP** (50 % nárast obchodov v roku 2024, projekcia konsolidácie 200 → 120 MSSP) odrážajú konkrétny bod konsolidačného cyklu. Konsolidačný príbeh pretrváva; konkrétne titulkové čísla sa pohnú.
> - **Rast trhu AIOps** a **stláčanie sadzieb na používateľa („25 % v ďalších dvoch rokoch“)** sú analytické projekcie; berte ich ako smerové a pred citovaním znovu overte voči čerstvým analytickým dátam.

> **Zdroje** · Prípadové štúdie servisného pultu (Moveworks v Broadcome/Equinixe, Aisera, Unity, NIB): prípadové štúdie publikované dodávateľmi. Čísla o vyhorení SOC: Tines, *Voice of the SOC Analyst*. Zavedenie samoopravy: výskum Gartneru. M&A MSP a konsolidácia MSSP: sledovatelia M&A v kanáli a trhová predpoveď CyVent. Projekcia IT práce 2030: prieskum Gartneru medzi CIO (2025).

---

*Ďalej: [Kapitola 10: Posun moci pri lock-ine](10_lock_in_power_shift.md)*
