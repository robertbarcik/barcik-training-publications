# Kapitola 4: Prečo hyperškálové firmy vyhrávajú na cene

> **V skratke**
>
> - Cenová výhoda hyperškálových firiem je štrukturálna, nie dočasná. Päť faktorov sa úročí: vlastný kremík (žiadna marža NVIDIE), využitie 85 % vs 35 %, inžinierstvo špecifické pre model, amortizácia rozsahom a strategické podceňovanie.
> - Lacnejšia práca v strednej a východnej Európe, nižšie marže ani lepšie open-source modely medzeru neuzavrú; má korene v kremíku a rozsahu.
> - Súčasné ceny API sú ceny na obsadenie trhu, dotované miliardami strategických investícií. Ustália sa na nákladových štruktúrach hyperškálových firiem, nie vašich.
> - Nič z toho neplatí pre klientov, ktorí nemôžu používať externé API. Tam súťažíte proti klientovmu internému IT tímu, súťaž, ktorú môžete vyhrať, pri maržiach spravovaných služieb.
>
> **Číslo, ktoré si zapamätať:** 10 – 30×, realistická celková nákladová výhoda najväčších poskytovateľov pri porovnateľnej kvalite oproti vášmu vlastne hostovanému stacku.

V kapitole 3 sme prepočítali vlastný hosting oproti prístupu cez API. Hlavné zistenie potrebuje pozorné čítanie. Áno, vlastne hostovaný model 20B pri vysokom využití vie podbehnúť *cenu* API strednej triedy pri 250+ používateľoch, ale to je malý model meraný oproti cenovke schopnejšieho. Porovnajte rovnaké s rovnakým (vaše náklady na token oproti cene API za *ekvivalentnú kvalitu modelu*) a medzera je 5× až 15× proti vám, v každom rozsahu, za štedrých predpokladov. Body zlomu v kapitole 3 existujú len preto, že menší model je niekedy pre záťaž dosť dobrý; nikdy nepochádzajú z toho, že by ste hyperškálové firmy prevádzkovo prekonali.

Mnohí čitatelia sa na tie čísla pozrú a pomyslia si: *toto je dočasné.* Ceny klesnú. Open-source modely dobehnú. Zoptimalizujeme. A niečo z toho je pravda: ceny klesajú, otvorené modely sa zlepšujú a sú skutočné optimalizácie, ktoré sa dajú urobiť.

Ale jadrová cenová medzera je štrukturálna, výsledok aspoň piatich úročiacich sa výhod, ktoré hyperškálové firmy majú a vy nie, nie trhová neefektivita čakajúca na opravu. Pochopiť tieto výhody nie je defétizmus; je to základ každej životaschopnej stratégie, ktorú diskutujeme v kapitolách 5 až 8.

## Vlastný kremík: jediný najväčší faktor

Keď spúšťate inferenciu na NVIDIA H100, neplatíte len za kremík. Platíte za hrubé marže NVIDIE, ktoré od začiatku boomu AI konzistentne presahujú 75 %. Z každého dolára, ktorý miniete na samotné GPU, je zhruba 75 centov hrubý zisk NVIDIE: marža nad výrobnými nákladmi. Tá marža je zapečená do každého vlastne hostovaného tokenu, ktorý vyprodukujete.

Google tú maržu neplatí. Jeho čipy TPU (Tensor Processing Unit) sú navrhnuté interne, vyrobené za nákladovú cenu v TSMC a nasadené výlučne v dátových centrách Googlu. Žiadny externý dodávateľ z kremíka nevyťahuje 75-percentnú maržu. Rovnaká logika platí pre čipy Trainium a Inferentia od Amazonu a pre akcelerátor Maia od Microsoftu, ktorý vstúpil do produkcie koncom roka 2025.

Výkonnostné charakteristiky sa líšia (TPU sú optimalizované na maticové operácie a inferenciu vo veľkých dávkach, nie na univerzálne GPU výpočty), ale pre špecifickú záťaž prevádzky transformerových modelov vo veľkom je vlastný kremík dramaticky lacnejší na užitočnú operáciu, nie iba konkurencieschopný s hardvérom NVIDIE.

Konzervatívne odhady kladú výhodu vlastného kremíka v nákladoch na FLOP na 3 – 5× v porovnaní s nákupom GPU NVIDIE za trhovú cenu. Niektoré interné analýzy naznačujú, že výhoda je špecificky pri inferencii ešte väčšia, lebo tieto čipy sa dajú navrhnúť presne na ten pomer pamäťovej priepustnosti a výpočtového výkonu, aký transformerová inferencia vyžaduje, namiesto univerzálneho návrhu, ktorý NVIDIA musí udržiavať, aby súčasne obslúžila hranie, vedecké výpočty a tréningové záťaže.

> **Kľúčové posolstvo:** Keď kupujete GPU NVIDIE, financujete hrubé marže NVIDIE 75 %+. Keď Google používa TPU, tá marža z nákladovej štruktúry zmizne. Tento jediný faktor tvorí 3 – 5-násobný rozdiel v nákladoch skôr, než sa zváži čokoľvek iné.

## Miery využitia: ekonomika prázdneho GPU o tretej ráno

GPU, ktoré nebeží inferenciu, je GPU, ktoré páli elektrinu a odpisy a pritom produkuje nula tokenov. To je problém využitia a vlastne hostované nasadenia zasahuje tvrdšie než takmer ktorýkoľvek iný faktor.

Typické podnikové nasadenie obsluhujúce jednu firmu alebo malý zhluk klientov uvidí dramatické kolísanie dopytu. Špičkové hodiny môžu hardvér nasýtiť. Noci, víkendy a sviatky ho nechajú nečinný. Realistické priemerné využitie dobre spravovaného podnikového GPU klastra sedí medzi 30 % a 40 %. Zle spravované (bežné u firiem nových v AI infraštruktúre) môžu klesnúť pod 20 %.

Hyperškálové firmy fungujú na priemernom využití 80 – 90 %+. Dosahujú to tromi mechanizmami, ktoré v menšom rozsahu jednoducho nie sú dostupné:

**Geografické vyhladzovanie dopytu.** Keď Európa spí, Amerika pracuje. Keď spí Amerika, preberá Ázia a Tichomorie. Globálna zákaznícka základňa naprieč všetkými časovými pásmami splošťuje krivku dopytu spôsobmi, aké regionálny poskytovateľ nikdy nedokáže.

**Rozmanitosť zákazníkov.** Milióny používateľov API s nekorelovanými vzormi záťaže vytvárajú prirodzené štatistické vyhladzovanie. Vaša dávková úloha vyplní medzeru, ktorú necháva utíchajúca chatová aplikácia iného zákazníka v reálnom čase.

**Priebežné dávkovanie.** Moderné inferenčné motory nespracúvajú jednu požiadavku naraz. Dynamicky dávkujú tisíce súbežných požiadaviek a plnia výpočtovú kapacitu GPU na teoretické maximum. Správa KV cache a plánovacie algoritmy potrebné na to, aby to bolo efektívne vo veľkom, predstavujú roky inžinierskych investícií.

Matematika je priamočiara. Ak váš hardvér beží na 35 % využití a hyperškálová firma na 85 %, hyperškálová firma vytiahne z toho istého dolára investície do hardvéru 2,4× viac užitočných tokenov. Je to funkcia rozsahu a rozmanitosti dopytu, nie optimalizácia, ktorú viete odinžinierovať lepším plánovacím softvérom.

> **Kľúčové posolstvo:** Vlastne hostované GPU typicky dosahujú 30 – 40 % využitie. Hyperškálové firmy bežia na 80 – 90 %+. Rovnaký hardvér, rovnaký odber, ale 2 – 3× viac užitočného výstupu na dolár, čisto z toho, že majú milióny rôznorodých používateľov naprieč globálnymi časovými pásmami.

## Optimalizácie špecifické pre model: inžinierska medzera

Keď vo vlastnej réžii hostujete open-source model, typicky ho spúšťate cez hotový obslužný framework: vLLM, TGI alebo podobný. Sú to dobré nástroje. Implementujú PagedAttention, základné priebežné dávkovanie a štandardnú kvantizáciu. Predstavujú špičku univerzálnej open-source inferencie.

Hyperškálové firmy pre svoje vlajkové modely univerzálne nástroje nepoužívajú.

**Architektúry zmesi expertov (MoE).** GPT-4o je takmer určite model zmesi expertov, rovnako Gemini a pravdepodobne viaceré ďalšie frontier systémy. MoE model môže mať 200 miliárd parametrov celkom, ale pre daný token aktivuje iba 20 – 30 miliárd. Dostanete kvalitu výstupu porovnateľnú s hustým modelom 200B za výpočtovú cenu modelu 30B. To je architektonická výhoda, ktorú poskytovateľ modelu zachytí, ale vlastne hostujúci poskytovateľ ju pri proprietárnych modeloch nezopakuje; najlepšie open-source MoE modely (Mixtral, DBRX) stále zaostávajú za frontier kvalitou.

**Vlastné CUDA jadrá a inferenčné pipeline.** Google, OpenAI a Anthropic udržiavajú každý tisíce inžinierskych hodín vlastného inferenčného kódu. Varianty Flash Attention vyladené na ich konkrétny hardvér. Vlastná správa pamäte využívajúca známe vzory prístupu. Implementácie špekulatívneho dekódovania, kde malý návrhový model predpovedá pravdepodobné pokračovania a dovolí veľkému modelu overiť viacero tokenov paralelne. Kvantizačné schémy po vrstvách, ktoré selektívne znižujú presnosť tam, kde je strata kvality minimálna.

**Spoločný návrh hardvéru a softvéru.** Keď ovládate čip aj softvérový stack, viete optimalizovať spôsobmi, ktoré sú s hotovými komponentmi nemožné. Softvérový stack TPU od Googlu je navrhnutý spolu s hardvérom. Prekladač, behové prostredie, plánovanie: všetko je optimalizované pre konkrétny kremík, na ktorom beží.

Kumulatívny účinok týchto optimalizácií je ďalší 3 – 5-násobný zisk v efektivite oproti tomu, čo dosiahnete s open-source nástrojmi na komoditnom hardvéri. Niektoré benchmarky odvetvia naznačujú, že medzera môže byť pri najväčších modeloch ešte širšia.

> **Kľúčové posolstvo:** Hyperškálové firmy bežia vlastné MoE architektúry, proprietárne CUDA jadrá, špekulatívne dekódovanie a spoločne navrhnuté hardvérovo-softvérové stacky. Vy bežíte hustý model na vLLM. Samotná inžinierska medzera stojí za ďalšie 3 – 5× v nákladovej efektivite.

## Amortizácia rozsahom: marginálny náklad jedného ďalšieho používateľa

Postaviť frontier LLM vyžaduje stovky miliónov až miliardy dolárov. Tréningový beh GPT-4 údajne stál vyše 100 miliónov dolárov. Výskumné tímy, dátové pipeline, infraštruktúra RLHF, bezpečnostné testovanie, platformové inžinierstvo: to sú fixné náklady, ktoré sa musia vrátiť.

Keď tie náklady rozložíte na milióny platiacich používateľov API, záťaž na používateľa sa stane triviálnou. Marginálny náklad na pridanie jedného ďalšieho zákazníka API (kým nepotrebujete pridať ďalšie GPU uzly) je fakticky nula. Infraštruktúra už beží. Model je už načítaný v pamäti. Jedna ďalšia požiadavka v dávke nezmení nič.

To sú klasické úspory z rozsahu, ale ich veľkosť je nezvyčajná. Pomer fixných a variabilných nákladov v obsluhe LLM je extrémny. Nákladovej štruktúre hyperškálovej firmy dominujú kapitálové výdavky (hardvér) a výskum a vývoj (vývoj modelov), oboje fixné. Variabilné náklady (elektrina na prírastkové výpočty, sieťová priepustnosť) sú na požiadavku nepatrné.

Pre vlastne hostujúceho poskytovateľa sa matematika obracia. Nesiete plné fixné náklady na hardvér a prevádzku, ale rozkladáte ich na oveľa menšiu používateľskú základňu. Vaša réžia na token z fixných nákladov môže byť 100× alebo 1 000× vyššia než u hyperškálovej firmy, jednoducho preto, že delíte tisíckami používateľov namiesto miliónov.

## Strategické podceňovanie: obsadzovanie trhu

Tu je faktor, ktorý robí porovnanie nákladov ešte jednostrannejším, než by naznačovali samotné štrukturálne výhody: súčasné ceny API sú ceny na zachytenie trhu, nie ceny odrážajúce náklady.

Google predáva vstupné tokeny Gemini Flash-Lite za 0,10 $ za milión. Pri tej cene je vierohodné, možno pravdepodobné, že Google predáva za náklady alebo pod nimi, aj na vlastnej optimalizovanej infraštruktúre. Prečo? Lebo každý vývojár, ktorý stavia na Gemini, je vývojár uzamknutý v Google Cloud Platform, konzumujúci služby Vertex AI, ukladajúci dáta v GCS a spúšťajúci susedné záťaže na GCE. API LLM je stratový produkt lákajúci do cloudového ekosystému.

OpenAI naceňuje agresívne, lebo v obsadzovacej fáze platformového trhu záleží na trhovom podiele viac než na zisku. S podporou investície Microsoftu a vlastných miliardových investičných kôl môže OpenAI udržiavať ceny pod nákladmi roky. Anthropic funguje pod podobnou logikou s podporou Amazonu.

Čísla rozprávajú príbeh jasne. Od začiatku roka 2024 do začiatku roka 2026 klesli ceny API LLM za ekvivalentnú schopnosť približne o 80 %. Výstup triedy GPT-4, ktorý začiatkom roka 2024 stál 30 $ za milión tokenov, dnes stojí cez GPT-4o 2,50 – 5,00 $. Ceny malých modelov sa zrútili ešte viac: GPT-4o-mini a Gemini Flash ponúkajú schopný výstup za 0,10 – 0,60 $ za milión tokenov.

Tieto ceny nie sú podlaha. Ale nie sú ani udržateľným odrazom skutočných nákladov. Sú výsledkom desiatok miliárd dolárov rizikového kapitálu a strategických investícií dotujúcich rastovú fázu najväčšieho platformového posunu od samotného cloud computingu.

> **Kľúčové posolstvo:** Súčasné ceny API sú ceny na zachytenie trhu, nie ceny odrážajúce náklady. Google, OpenAI a Anthropic majú za sebou miliardy strategických investícií a naceňujú tak, aby získali trhový podiel, nie aby maximalizovali maržu. Súťažíte proti dotovaným cenám navrch štrukturálnych nákladových výhod.

## Čo veci naozaj stoja

Ak preseknete strategické ceny a vyjdete z nákladov na hardvér, energiu a inžinierskych odhadov, tu je, čo frontier inferencia pravdepodobne stojí veľkých poskytovateľov na ich optimalizovanej infraštruktúre:

**Frontier modely** (GPT-4.1, Claude Sonnet, Gemini Pro): skutočné náklady poskytovateľa sú pravdepodobne **1 – 3 $ za milión výstupných tokenov** na plne optimalizovanom vlastnom kremíku pri vysokom využití. Predávajú za 2,00 – 15,00 $, čo znamená marže od tenkých po zdravé podľa modelu a poskytovateľa.

**Malé/rýchle modely** (GPT-4o-mini, Gemini Flash, Claude Haiku): skutočné náklady poskytovateľa sú pravdepodobne **0,05 – 0,20 $ za milión tokenov** v rozsahu hyperškálovej firmy. Predávajú za 0,10 – 0,60 $, čo znamená, že niektoré z nich sú skutočne ponuky blízko nákladov alebo pod nimi.

Teraz porovnajte tie čísla s tým, čo stojí vlastný hosting. Dobre vedené on-prem nasadenie open-source modelu **triedy 70B**, veľkosti, ktorú potrebujete, aby ste sa vôbec priblížili frontier kvalite, pristáva zhruba na **8 – 15 $ za milión výstupných tokenov** pri realistickom podnikovom využití (30 – 40 %), keď poctivo započítate odpisy hardvéru, energiu a prevádzku.

Na zosúladenie s kapitolou 3: vlastné nasadenie 20B pri 1 000 používateľoch vyšlo zhruba na 2 $ za milión výstupných tokenov. Oveľa lepšie, ale to je menší model pri priaznivom využití a jeho konkurent v API pri porovnateľnej kvalite je rozpočtová úroveň predávajúca za 0,40 – 0,60 $ za milión výstupu. V každom bode porovnateľnej kvality ekvivalent v API podbieha vaše náklady vlastného hostingu.

Nesúťažíte s cenou API. Nesúťažíte ani so skutočnými nákladmi poskytovateľa. Fungujete v zásadne inom nákladovom režime.

## Úročiaci sa účinok

Tieto výhody sa iba nesčítavajú; úročia sa. Zvážte celý reťazec:

| Výhoda | Nákladový násobok |
|---|---|
| Vlastný kremík vs. marže NVIDIE | 3 – 5× |
| Využitie (85 % vs. 35 %) | 2 – 2,5× |
| Optimalizácie modelov (MoE, vlastné jadrá) | 3 – 5× |
| Amortizácia rozsahom | 2 – 5× |
| **Kombinovaná teoretická výhoda** | **36 – 300×** |

Medzera v skutočnom svete je menšia než teoretické maximum, lebo tieto faktory sa prekrývajú a interagujú: využitie a amortizácia rozsahom sú sčasti tá istá výhoda počítaná dvakrát a čísla na používateľa v kapitole 3 už majú penalizáciu za využitie zapečenú na vašej strane účtu. Ale 10 – 30-násobná celková nákladová výhoda je pre najväčších poskytovateľov realistická. Aj konzervatívna 5 – 10-násobná medzera je zničujúca, ak sa snažíte súťažiť na cene.

## Kedy na výhode hyperškálových firiem nezáleží

Všetko vyššie je pravda a pre klientov, ktorí si môžu slobodne vybrať medzi vašou vlastne hostovanou službou a API hyperškálovej firmy, je to zničujúce. Ale existuje veľký a dôležitý segment podnikového trhu EÚ, kde je nákladová výhoda hyperškálových firiem irelevantná, lebo API hyperškálovej firmy nie je možnosť, ktorú si klient môže vybrať.

Zvážte európsku banku, ktorej tím pre súlad rozhodol, že finančné dáta zákazníkov nemôžu spracúvať externí poskytovatelia AI. Alebo obranného dodávateľa narábajúceho s utajovanými informáciami. Alebo zdravotnícky systém, kde pravidlá správy dát pacientov vylučujú akékoľvek externé API bez ohľadu na zmluvy poskytovateľa o spracovaní údajov.

Pre týchto klientov porovnanie neznie „váš GPU klaster vs. TPU farma Googlu“, ale skôr:

- **Vaša spravovaná AI infraštruktúra** vs. **klient, ktorý si ju postaví sám**
- **Vaša spravovaná AI infraštruktúra** vs. **žiadna AI vôbec**

V tomto porovnaní sú výhody hyperškálových firiem, ktoré sme vymenovali (vlastný kremík, miery využitia, MoE architektúry, amortizácia rozsahom), výhody, ku ktorým klient tiež nemá prístup. Klient čelí rovnakým nákupným cenám GPU, rovnakým výzvam s využitím, rovnakým obmedzeniam open-source modelov ako vy. Súťažíte za rovnakých podmienok.

A za rovnakých podmienok poskytovateľ IT služieb vyhráva, z tých istých dôvodov, z akých ste vždy vyhrávali proti interným IT oddeleniam: prevádzková špecializácia, zdieľané náklady naprieč viacerými klientmi, zrelé nástroje a schopnosť pritiahnuť a udržať zručných inžinierov účinnejšie, než dokáže banka alebo nemocnica.

Ako ukázala kapitola 3, marža spravovanej AI infraštruktúry pre on-prem klientov vyzerá pozoruhodne ako tradičné spravované služby: 40 – 55 %. Je to ziskový, udržateľný biznis a na trhu EÚ, kde regulované odvetvia predstavujú podstatný podiel podnikových výdavkov na IT, môže ísť pre mnohých poskytovateľov IT služieb o najväčšiu adresovateľnú príležitosť.

> **Kľúčové posolstvo:** Nákladové výhody hyperškálových firiem v tejto kapitole platia, keď majú klienti na výber. Mnohí podnikoví klienti v EÚ na výber nemajú. Pre regulované odvetvia, ktoré vyžadujú on-prem AI, súťažíte proti klientovmu internému tímu, nie proti TPU Googlu. To je súťaž, ktorú môžete vyhrať, pri maržiach, na ktorých sa dá postaviť biznis.

## Nepríjemný záver (pre klientov otvorených cloudu)

Pre klientov, ktorí môžu používať cloudové API, je medzera v nákladovej efektivite medzi API hyperškálových firiem a vlastne hostovanou inferenciou pravdepodobne najširšia štrukturálna medzera v celom dnešnom podnikovom softvéri. Je širšia než medzera medzi on-prem e-mailom a Gmailom. Je širšia než medzera medzi prevádzkou vlastnej CDN a používaním Cloudflare. Je širšia, lebo podkladová technológia, inferencia na GPU/TPU v masívnom rozsahu, má jedinečne extrémne výnosy z rozsahu.

Túto medzeru nemožno uzavrieť:

- **Lacnejšou prácou v strednej a východnej Európe.** Váš prevádzkový tím by mohol pracovať zadarmo a neuzavrelo by to 10-násobnú nákladovú medzeru, ktorá má korene v kremíku a využití.
- **Nižšími maržami.** Ani pri nulovej marži vaša nákladová štruktúra nedosiahne ich predajnú cenu.
- **Lepšími open-source modelmi.** Medzera v kvalite modelov sa zužuje. Medzera v *efektivite infraštruktúry* nie.
- **Čakaním, kým sa ceny ustália.** Ceny sa nakoniec ustália. Ustália sa na úrovni, ktorá odráža nákladové štruktúry hyperškálových firiem, nie vaše.

Pre tento segment klientov súťažiť na cene infraštruktúry nie je životaschopné. Ale to je len časť príbehu. Kapitola 5 pokrýva najrýchlejšiu krátkodobú cestu k tržbám (implementáciu AI, ktorú vaši dodávateľskí partneri už dodávajú) a tri kapitoly za ňou skúmajú biznis modely, ktoré fungujú naprieč oboma segmentmi klientov: proxy pre súkromie pre klientov otvorených cloudu s obavami o súlad (kapitola 6), lokálne nasadenie na zariadeniach zamestnancov (kapitola 7) a služby testovania, bezpečnosti a agentnej infraštruktúry (kapitola 8). Pre klientov vyžadujúcich on-prem ostáva infraštruktúrny biznis životaschopný a služby z kapitol 5 – 8 pridávajú maržu navrch.

> **Kľúčové posolstvo:** Vedzte, ktorú hru hráte. Pre klientov otvorených cloudu je nákladová výhoda hyperškálových firiem štrukturálna a trvalá: súťažte na odbornosti, nie na výpočtovom výkone. Pre klientov vyžadujúcich on-prem infraštruktúrny biznis funguje, lebo alternatíva hyperškálovej firmy pre nich neexistuje. Väčšina poskytovateľov IT služieb v EÚ bude obsluhovať oba segmenty a víťazmi budú tí, ktorí správne nacenia a napozicionujú pre každý.

---

> **Poznámka z júla 2026: riziko suverenity, ktoré táto kapitola nenaceňuje.** Všetko vyššie predpokladá, že špička ostane komerčne otvorená, teda že ktokoľvek s kreditnou kartou dostane najlepšie modely za klesajúce ceny. Tri mesiace po overení tejto kapitoly sa tento predpoklad ohol. Najschopnejšia úroveň modelov na trhu je momentálne dostupná iba malej množine preverených firiem, prevažne amerických, a úroveň pod ňou sa predáva cez nákladné API kredity za ťažkou vrstvou moderovania. Odstupňovaný môže byť samotný prístup, nielen cena. Pre klientov v EÚ je to druhý, nenacenený argument pre on-prem a lokálne stratégie neskôr v tejto brožúre a je témou sprievodnej brožúry [Merkantilizmus generatívnej AI](/mercantilism-of-genai-sk/#m-utility): mechanizmus 1, „inteligencia je utilita, nie produkt“.

---

> **Strážca čerstvosti** · *overené apríl 2026 · odhadovaný polčas rozpadu: ~9 mesiacov*
>
> Päť štrukturálnych výhod (vlastný kremík, využitie, optimalizácie modelov, amortizácia rozsahom, strategické podceňovanie) vydrží. Konkrétne tvrdenia, ktoré sa najpravdepodobnejšie posunú:
>
> - Číslo **„75 % hrubá marža NVIDIE“** sleduje verejné financie NVIDIE. Pokles capexu do AI alebo zmysluplná konkurencia od AMD MI300X či ponúk TPU na prenájom by ho mohla stlačiť do 12 – 18 mesiacov.
> - **„Strategické podceňovanie“**: poskytovatelia sa môžu posunúť k cenám odrážajúcim náklady, len čo sa trhový podiel ustáli. Ak sa to stane, očakávajte, že Gemini Flash-Lite, GPT-4o-mini a podobné rozpočtové úrovne poplávajú nahor (alebo sa rozdelia na platené/bezplatné úrovne).
> - Odhady **skutočných nákladov „1 – 3 $ za milión výstupných tokenov“** sú informované odhady z verejných zverejnení a analýz odvetvia. Berte ich ako smerové.
> - Generácie **Microsoft Maia, AWS Trainium/Inferentia, Google TPU** sa menia zhruba ročne; kým toto čítate, uvedená generácia môže byť nahradená.

---

*Kapitola 5 skúma cestu najmenšieho odporu: predaj a implementáciu AI funkcií, ktoré vaši existujúci dodávateľskí partneri vkladajú do produktov, ktoré vaši klienti už používajú.*
