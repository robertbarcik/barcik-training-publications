# Kapitola 2: Ako veľké jazykové modely naozaj bežia

> **V skratke**
>
> - Prevádzka LLM je dimenzovací problém, ktorý už poznáte, len s VRAM namiesto RAM a tokenmi za sekundu namiesto spojení.
> - Váhy modelu sú podlaha vášho pamäťového rozpočtu. KV cache (stav konverzácie na používateľa) je to, čo rastie so súbežnými používateľmi, a často sa vyrovná samotným váham.
> - Rýchlosť na používateľa má tvrdý strop: pamäťová priepustnosť delená veľkosťou modelu. Úzkym hrdlom je priepustnosť, nie výpočtový výkon.
> - Hardvérový dôsledok: model 20B obslúži 100 používateľov za menej než 80 000 $; model 120B potrebuje 600 000 $+. Výber modelu je infraštruktúrne rozhodnutie.
>
> **Číslo, ktoré si zapamätať:** 30 – 50 tokenov za sekundu na používateľa, cieľ interaktívneho zážitku, okolo ktorého sa dimenzuje všetko plánovanie kapacity.

Už viete, ako dimenzovať databázový server. Viete, že inštancia PostgreSQL obsluhujúca 500 súbežných spojení potrebuje isté množstvo RAM na zdieľané buffery, pracovnú pamäť a réžiu spojení. Viete odhadnúť, že 2TB databáza s ťažkou čítacou prevádzkou potrebuje konkrétne IOPS a istý počet CPU jadier.

Prevádzka veľkého jazykového modelu je rovnaký druh inžinierskeho problému, len s iným hardvérom. Úzke hrdlo sa presúva z CPU a RAM na GPU a VRAM, záťaž sa posúva z diskových I/O na násobenie matíc a jednotka škálovania sa mení zo „spojení“ na „tokeny za sekundu“. Ale proces uvažovania je identický: pochopiť nároky na zdroje, priradiť ich hardvéru a plánovať pre súbežných používateľov.

Táto kapitola vám to pochopenie dá.

## Parametre, presnosť a pamäť

Veľký jazykový model je vo svojom jadre obrovská zbierka číselných váh, nazývaných **parametre**, ktoré kódujú všetko, čo sa model naučil počas tréningu. Keď niekto pošle prompt, model prenásobí vstupné dáta cez tieto váhy vrstvu po vrstve, aby vyprodukoval výstup. Každý jeden parameter musí byť načítaný do pamäte GPU skôr, než model spracuje čo i len jeden token.

To je základné obmedzenie. Na rozdiel od tradičnej aplikácie, kde môžete dáta stránkovať medzi RAM a diskom, parametre LLM musia sedieť vo VRAM (vyhradenej pamäti GPU) s mimoriadne rýchlym prístupom. Celý model musí byť rezidentný, stále, pre každú požiadavku.

Pamäťová stopa závisí od dvoch vecí: počtu parametrov a číselnej presnosti použitej na uloženie každého z nich.

### Formáty presnosti

Každý parameter je číslo. Koľko bajtov použijete na uloženie toho čísla, sa nazýva jeho **presnosť**:

- **FP16 (polovičná presnosť)**: 2 bajty na parameter (plná kvalita, žiadna strata presnosti)
- **INT8 (8-bitová kvantizácia)**: 1 bajt na parameter (minimálna strata kvality pri väčšine úloh)
- **INT4 (4-bitová kvantizácia)**: 0,5 bajtu na parameter (citeľné zníženie kvality pri zložitom uvažovaní, ale životaschopné pre mnohé produkčné prípady použitia)

Predstavte si to ako bitrate zvuku. MP3 s 320 kbps je takmer nerozoznateľné od CD. MP3 so 128 kbps stačí na hudbu v pozadí. Súbor so 64 kbps funguje pre hlasové hovory. „Správna“ kvalita závisí od prípadu použitia.

### Pamäťová matematika pre skutočné modely

Tu je, čo to znamená pre dve reprezentatívne veľkosti modelov, veľký model frontier triedy (120B parametrov) a schopný model strednej veľkosti (20B parametrov):

| Veľkosť modelu | FP16 (2 bajty) | INT8 (1 bajt) | INT4 (0,5 bajtu) |
|---|---|---|---|
| **120B parametrov** | ~240 GB VRAM | ~120 GB VRAM | ~60 – 70 GB VRAM |
| **20B parametrov** | ~40 GB VRAM | ~20 GB VRAM | ~10 – 12 GB VRAM |

Model 120B v plnej presnosti potrebuje 240 GB VRAM len na váhy. Žiadne jednotlivé GPU na trhu nemá toľko pamäte, čo znamená, že model musíte rozložiť cez viacero GPU. Model 20B pri INT4 sa naproti tomu pohodlne zmestí na jediné spotrebiteľské GPU s 24 GB VRAM.

> **Kľúčové posolstvo**: Váhy modelu sú základný pamäťový náklad, ekvivalent vašej „minimálnej RAM“. Ale tak ako databázový server potrebuje pamäť nad rámec dátových súborov, LLM potrebuje VRAM nad rámec váh modelu. Najväčším dodatočným spotrebiteľom je KV cache.

## KV cache: kde vás zasiahnu súbežní používatelia

Tu to začína byť zaujímavé pre každého, kto premýšľa o nasadeniach pre viacerých používateľov.

Keď model spracúva konverzáciu, počíta medzihodnoty nazývané **kľúče a hodnoty** (KV) pre každý token v kontexte. Tie sa cachujú, aby ich model nemusel prepočítavať pre každý nový token, ktorý generuje. To je **KV cache** a rastie s každým tokenom v každej aktívnej konverzácii.

Ak ste prevádzkovali databázu, predstavte si KV cache ako ekvivalent pamäte sedenia na úrovni spojenia. Každý aktívny používateľ spotrebúva podiel pamäte úmerný dĺžke svojej konverzácie.

### Náklad KV na token: pracovný vzorec

Odsek vyššie hovoril, že KV cache rastie s každým tokenom v každej aktívnej konverzácii. Skutočný náklad na token je zhruba:

> **bajty na token ≈ 2 × n_layers × n_kv_heads × head_dim × bytes_per_element**

Dvojka pokrýva kľúče a hodnoty. Kritický člen je **n_kv_heads**: nie plný počet hláv pozornosti, ale počet hláv *kľúčov/hodnôt*. Moderné modely používajú **Grouped-Query Attention (GQA)**, kde mnoho hláv dopytu zdieľa malý počet KV hláv. To je jediný najväčší dôvod, prečo sa KV cache medzi rokmi 2022 a 2025 dramaticky zmenšila.

Referenčné čísla pri FP16:

| Architektúra modelu | KV na token (FP16) | Konverzácia 10K tokenov | Konverzácia 100K tokenov |
|---|---|---|---|
| Llama 3 70B (GQA, 8 KV hláv, 80 vrstiev) | ~320 KB | ~3,2 GB | ~32 GB |
| Agresívne návrhy GQA / MQA / MLA | ~30 – 100 KB | ~0,3 – 1 GB | ~3 – 10 GB |
| Staršie MHA (éra GPT-3, bez GQA) | niekoľko MB | ~25 – 50 GB | nepraktické |

Desaťnásobný rozptyl naprieč architektúrami je dôvod, prečo súhrnné číslo v ďalšej časti („80 – 150 GB pre 100 používateľov pri 16K tokenov na modeli 120B“) predpokladá KV-efektívny návrh, typicky MQA, MLA alebo KV cache kvantizovanú do FP8. Ak vo vlastnej réžii hostujete model, ktorý žiadnu z týchto techník nepoužíva, vaša stopa KV môže byť ľahko 5 – 10× titulkového čísla.

### Matematika vážnie vo veľkom rozsahu

Zvážte realistický podnikový scenár: 100 súbežných používateľov pracujúcich s modelom so 120B parametrami. Niektorí vedú priamočiare sedenia otázok a odpovedí (kontext 4K – 8K). Iní spúšťajú agentné pracovné postupy (generovanie kódu, analýza dokumentov, viackrokové uvažovanie), ktoré tlačia na 32K – 128K tokenov na sedenie.

Konzervatívny priemer 16K aktívnych kontextových tokenov naprieč 100 používateľmi znamená 1,6 milióna tokenov stavu KV cache, ktoré musia súčasne žiť vo VRAM. Pre model 120B sa to prekladá zhruba na **80 – 150 GB dodatočnej VRAM** navrch váh modelu, podľa architektúry modelu a presnosti.

Nechajte si to sadnúť: KV cache pre 100 používateľov môže vyžadovať toľko VRAM ako samotné váhy modelu.

| Zložka | 120B pri FP16 | 120B pri INT8 |
|---|---|---|
| Váhy modelu | 240 GB | 120 GB |
| KV cache (100 používateľov, priem. kontext 16K) | 80 – 150 GB | 80 – 150 GB |
| Réžia behu (aktivácie, buffery) | 20 – 40 GB | 15 – 30 GB |
| **Celková potrebná VRAM** | **340 – 430 GB** | **215 – 300 GB** |

Všimnite si, že kvantizácia váh modelu pomáha prvému riadku, ale KV cache sa nezmenšuje úmerne; závisí od skrytých rozmerov modelu a počtu hláv pozornosti, nie od presnosti váh. Preto samotná kvantizácia problém škálovania pre viacerých používateľov nerieši.

### Tri veci, ktoré sa volajú „cachovanie“

Slovo „cachovanie“ sa v obsluhe LLM objavuje v troch rôznych kontextoch a ich zamieňanie vedie k nesprávnym intuíciám o nákladoch a kapacite.

**1. KV cache vo VRAM.** To, čo opisujú vzorce vyššie: stav na token, ktorý rastie počas aktívnej konverzácie, žije v pamäti GPU a uvoľní sa, keď sedenie skončí alebo sa vytlačí. Je to **kapacitný** náklad: každý bajt, ktorý pridelíte jednému používateľovi, je bajt, ktorý nemôžete dať inému.

**2. Cachovanie promptov v API (zľava dodávateľa).** Keď OpenAI, Anthropic, DeepSeek a ďalší inzerujú „cachované vstupné tokeny za ~10 % bežnej ceny“, uchovávajú predpočítaný stav KV pre *prefix* vášho promptu, v odstupňovanej horúcej pamäti (HBM → DRAM, občas NVMe), nie na disku. TTL sú krátke: Anthropic má predvolených 5 minút, predĺžiteľných na 1 hodinu. Zásah do cache preskočí krok prefill, takže platíte zľavu **a** dostanete oveľa rýchlejší čas do prvého tokenu. Zľava odráža ušetrený výpočtový výkon, nie ušetrené úložisko.

**3. Nečinné konverzácie v chatbotovom rozhraní.** Keď používateľ zavrie dlhú konverzáciu v ChatGPT alebo Claude.ai a zajtra ju znovu otvorí, dodávateľ **nedrží** KV vo VRAM. Uchováva iba **text** konverzácie. Pri obnovení model znovu prefilluje celú históriu od nuly, čo je ten citeľný oneskorený štart pred prvou odpoveďou pri konverzácii s dlhou históriou.

Invariant, ktorý to spája: **len čo začne dekódovanie, stopa VRAM na token je identická bez ohľadu na to, ako sa tam KV dostalo**. Zásahy do cache šetria výpočtový výkon prefillu, čas do prvého tokenu a (pri API) peniaze; nemenia priepustnosť ani VRAM na token počas generovania.

Jedna nuansa pre vlastných hostiteľov: **Automatic Prefix Caching** (APC) vo vLLM skutočne drží stav KV vo VRAM naprieč ťahmi. To je výborné pre viacťahové sedenia s krátkou nečinnosťou, ale zbytočné pre „používateľ sa vráti zajtra“. Dodávatelia API riešia zajtrajší prípad masívnym odstupňovaným úložiskom a agresívnym vytláčaním vo veľkom; malé vlastne hostované prevádzky túto ekonomiku nezopakujú; pre nich je prefix caching iba funkcia „ostať teplý pár minút“.

> **Kľúčové posolstvo**: Pri dimenzovaní GPU infraštruktúry sú váhy modelu podlaha, nie strop. Pri nasadeniach pre viacerých používateľov KV cache často dominuje plánovaniu pamäte. Každý ďalší súbežný používateľ s dlhým kontextovým oknom stojí skutočnú VRAM.

## Priepustnosť: tokeny za sekundu na používateľa

Pamäť určuje, či sa model zmestí. **Priepustnosť** určuje, či je zážitok prijateľný.

Dobrý interaktívny zážitok vyžaduje **30 – 50 tokenov za sekundu** na používateľa. Pod 20 tokenmi/s používatelia vnímajú citeľné oneskorenie. Nad 50 sa výstup zdá v podstate okamžitý: úzkym hrdlom sa stáva rýchlosť čítania, nie generovania.

Pre 100 súbežných používateľov to znamená, že vaša infraštruktúra musí udržať **3 000 – 5 000 tokenov za sekundu súhrnne**. Je to ekvivalent dimenzovania sieťovej priepustnosti pre súbežné spojenia: každý používateľ potrebuje zaručené minimum a infraštruktúra musí zvládnuť súhrnnú špičku.

Priepustnosť závisí od výpočtového výkonu GPU (meraného v TFLOPS), pamäťovej priepustnosti (ako rýchlo sa dáta hýbu medzi VRAM a výpočtovými jednotkami) a toho, ako efektívne obslužný softvér plánuje prácu naprieč viacerými požiadavkami.

### Strop jedného prúdu: priepustnosť ÷ veľkosť modelu

Existuje jednoduchý vzorec „na obálku“, ktorý vysvetľuje, prečo na pamäťovej priepustnosti tak záleží. Na vygenerovanie **jedného** tokenu musí GPU prečítať **celé váhy modelu** z VRAM cez výpočtové jednotky a späť. Takže strop priepustnosti na prúd je zhruba:

> **tokeny/s (jeden prúd) ≈ pamäťová priepustnosť ÷ veľkosť modelu v pamäti**

Rozpracovaný príklad: model 20B pri INT8 (~20 GB váh) na jedinom H100 (3,35 TB/s = 3 350 GB/s):

3 350 ÷ 20 ≈ **167 tokenov/s na prúd** (teoretický strop; v skutočnosti typicky o 30 % nižšie kvôli čítaniu KV cache, réžii pozornosti a medzerám medzi kernelmi).

Z toho vypadávajú dva dôsledky:

1. **Menšie modely pôsobia svižnejšie**, lebo strop škáluje 1:1 s veľkosťou modelu. Model 20B na H100 má zhruba 6× vyšší strop na prúd než model 120B na tom istom hardvéri, čo je väčšina dôvodu, prečo malý model pôsobí na interaktívnych používateľov responzívnejšie, bez ohľadu na to, koľko výpočtového výkonu naň nasypete.
2. **Dávkovanie je pri obsluhe viacerých používateľov nevyhnutné.** Váhy modelu sa čítajú raz na generačný krok a uplatnia sa naprieč každým používateľom v dávke. Prečítať 120 GB váh na obsluhu ôsmich používateľov v jednej dávke stojí v podstate rovnakú priepustnosť ako obslúžiť jedného, a preto uzol 8× H100 udrží 30 – 50 tokenov/s pre 20 – 30 súbežných používateľov namiesto jedného používateľa na teoretickom maxime.

Preto v tabuľke GPU, ktorá nasleduje, záleží pri inferenčných záťažiach viac na stĺpci priepustnosti než na stĺpci TFLOPS. Málokedy vám dôjde výpočtový výkon skôr než priepustnosť.

## GPU hardvér: praktické porovnanie

Ak ste zvyknutí porovnávať procesory Xeon a EPYC a pamäť DDR4 a DDR5, táto tabuľka je váš GPU ekvivalent:

| GPU | VRAM | Pamäťová priepustnosť | FP16 TFLOPS | Nákupná cena (za kus) | Typický prípad použitia |
|---|---|---|---|---|---|
| **NVIDIA H100 SXM** | 80 GB HBM3 | 3,35 TB/s | 989 | 25 000 – 40 000 $ | Frontier modely, produkcia s vysokou priepustnosťou |
| **NVIDIA H200 SXM** | 141 GB HBM3e | 4,8 TB/s | 989 | 30 000 – 45 000 $ | Veľké modely potrebujúce maximum VRAM |
| **NVIDIA A100 SXM** | 80 GB HBM2e | 2,0 TB/s | 312 | 15 000 – 17 000 $ | Predchádzajúca generácia, dobrý pomer cena/výkon |
| **NVIDIA A100** | 40 GB HBM2e | 1,6 TB/s | 312 | 10 000 – 12 000 $ | Rozpočtová produkcia, menšie modely |
| **NVIDIA L40S** | 48 GB GDDR6X | 864 GB/s | 362 | 7 000 – 10 000 $ | Optimalizované na inferenciu, dátové centrum |
| **NVIDIA RTX 4090** | 24 GB GDDR6X | 1,0 TB/s | 330 | 1 600 – 2 000 $ | Vývoj, ľahká produkcia |

Pár vecí vyčnieva. H100 a H200 sú v pamäťovej priepustnosti v inej lige: 3 – 5× rýchlejšie než L40S. Pri inferencii LLM je pamäťová priepustnosť často úzkym hrdlom, lebo generovanie každého tokenu vyžaduje prečítať celé váhy modelu z pamäte. Pozoruhodných je aj 141 GB VRAM na H200: udrží model 120B pri INT8 na jedinom GPU (hoci na priepustnosť vo veľkom by ste stále potrebovali viacero GPU).

RTX 4090 si zaslúži pozornosť z iného dôvodu. Za zhruba 1 800 $ dodáva prekvapivo schopný inferenčný výkon pre menšie modely. Jej 24 GB VRAM obmedzuje, čo dokáže spustiť, ale pre kvantizovaný model 20B je to legitímna možnosť.

## Konkrétne konfigurácie: čo obslúži 100 používateľov

Poskladajme kúsky dokopy s konkrétnymi hardvérovými konfiguráciami.

### Konfigurácia 1: model 120B pre 100 používateľov

Model 120B pri INT8 potrebuje ~120 GB na váhy plus 80 – 150 GB na KV cache. Potrebujete podstatnú súhrnnú VRAM a výpočtový výkon.

**Hardvér**: uzol 8× H100 80 GB (640 GB celkovej VRAM, prepojenie NVLink)

Jeden taký uzol (v cene 200 000 – 400 000 $) poskytuje dosť VRAM a priepustnosti na obsluhu **20 – 30 súbežných používateľov** pri dobrej priepustnosti. Váhy modelu spotrebujú asi 120 GB (pri INT8), čo necháva ~520 GB na KV cache, aktivácie a réžiu dávkovania. To znie štedro, kým nezapočítate dlhokontextové agentné sedenia, ktoré zožerú 1 – 2 GB KV cache každé.

Pre 100 súbežných používateľov plánujte **3 – 4 uzly**, celkovú investíciu 600 000 – 1 600 000 $ len do GPU hardvéru, pred rackmi, sieťou, napájaním a chladením.

### Konfigurácia 2: model 20B pre 100 používateľov

Model 20B je zásadne iná záležitosť. Pri FP16 potrebujú váhy ~40 GB. Pri INT8 ~20 GB. Pri INT4 ~10 – 12 GB.

| Zostava | Hardvér | Odhadovaná cena | Súbežní používatelia |
|---|---|---|---|
| **Plná presnosť** | 2× H100 80 GB | 50 000 – 80 000 $ | ~100 používateľov |
| **Kvantizované INT8** | 4× A6000 alebo L40S (48 GB každé) | 28 000 – 40 000 $ | ~100 používateľov |
| **Kvantizované INT4** | 2× RTX 4090 (24 GB každá) | 3 200 – 4 000 $ | Ľahšie záťaže, 20 – 40 používateľov |
| **Jediné GPU** | 1× H100 alebo A100 80 GB | 15 000 – 40 000 $ | 50 – 80 používateľov |

Jediné H100 alebo A100 80 GB pohodlne udrží model 20B pri FP16 s dostatkom miesta na KV cache a obslúži 50 – 80 súbežných používateľov pri dobrej priepustnosti. Dve H100 pri FP16 zvládnu 100 používateľov s rezervou.

Ekonomika je tu pozoruhodná. Kým model 120B vyžaduje pre 100 používateľov vyše pol milióna dolárov v GPU, model 20B obslúži rovnaký počet používateľov za menej než 80 000 $ a s kvantizáciou INT8 na kartách L40S za menej než 40 000 $.

> **Kľúčové posolstvo**: Skok z 20B na 120B nie je 6-násobný nárast nákladov, ale skôr 10 – 20-násobný, keď započítate KV cache, sieťovanie medzi uzlami a prémiové ceny špičkových GPU. Otázka pre vašich klientov znie, či ten rozdiel v kvalite odôvodňuje rozdiel v nákladoch pre ich konkrétny prípad použitia.

## Obslužný softvér: strojovňa

Mať správne GPU je nutné, ale nie postačujúce. Softvérová vrstva, ktorá sedí medzi modelom a prichádzajúcimi požiadavkami, robí obrovský rozdiel v tom, koľko používateľov váš hardvér naozaj obslúži. Je to analógia rozdielu medzi spustením surového binárneho MySQL a jeho spustením za správne nakonfigurovaným poolerom spojení s optimalizáciou dopytov.

### Kľúčové obslužné frameworky

**vLLM** je súčasný štandard produkčnej obsluhy LLM. Jeho kľúčovou inováciou je **PagedAttention**, technika správy pamäte pre KV cache, ktorá funguje ako stránkovanie virtuálnej pamäte v operačnom systéme. Namiesto predalokovania maximálnej dĺžky kontextu pre každú požiadavku alokuje pamäť KV cache po stránkach a dynamicky ich uvoľňuje. Už toto samo môže zlepšiť priepustnosť 2 – 4× oproti naivnej obsluhe.

**Text Generation Inference (TGI)** od Hugging Face je ďalšia solídna produkčná možnosť, obzvlášť dobre integrovaná s ekosystémom modelov Hugging Face. Podporuje kvantizáciu, tenzorový paralelizmus a priebežné dávkovanie hneď z krabice.

**llama.cpp** volí iný prístup: je optimalizovaný na spúšťanie kvantizovaných modelov na spotrebiteľskom hardvéri vrátane inferencie iba na CPU. Výkon je nižší než u GPU-natívnych frameworkov, ale beží všade a je na svoju váhovú kategóriu pozoruhodne efektívny.

**MLX** je framework Applu na spúšťanie modelov na Apple Silicon. Ak majú vaši klienti flotily MacBookov alebo Mac Studií s M2/M3/M4, MLX umožňuje lokálnu inferenciu s využitím zjednotenej pamäťovej architektúry. Mac Studio so 192 GB zjednotenej pamäte dokáže spustiť model 70B, čo preskúmame v kapitole 7.

### Tri techniky, na ktorých záleží

**Tenzorový paralelizmus** rozdelí model cez viacero GPU v jednom uzle. Každé GPU drží výsek každej vrstvy a počas každého dopredného prechodu spolu komunikujú cez vysokorýchlostné prepojenia NVLink. Takto spustíte model 120B cez 8 H100: model je priveľký pre akékoľvek jedno GPU, tak ho rozdelíte. Predstavte si to ako prekladanie RAID, ale pre vrstvy neurónovej siete namiesto diskových blokov.

**Priebežné dávkovanie** je to, čo robí obsluhu viacerých používateľov ekonomicky životaschopnou. Namiesto spracovania jednej požiadavky naraz (alebo čakania na naplnenie pevnej dávky) obslužný framework dynamicky pridáva nové požiadavky do bežiacej dávky a odoberá dokončené. Používateľ, ktorý položí krátku otázku, dostane odpoveď bez čakania, kým sa dokončí 4 000-tokenové generovanie iného používateľa. Je to LLM ekvivalent multiplexovania HTTP/2: prekladanie viacerých prúdov na tom istom spojení.

**Špekulatívne dekódovanie** používa malý, rýchly „návrhový“ model na predpovedanie niekoľkých tokenov dopredu a potom ich overí v jedinom prechode cez veľký model. Keď sú predpovede správne (čo je pri rutinnom texte často), dostanete viacero tokenov za výpočtovú cenu jedného overovacieho kroku. Zrýchlenie je pri vhodných záťažiach typicky 1,5 – 2,5×. Je to v podstate predikcia vetvenia pre jazykové modely: špekuluj, over a prijmi alebo zamietni.

## Čo to znamená pre váš infraštruktúrny biznis

Ak dnes pre klientov spravujete serverovú infraštruktúru, všetko v tejto kapitole sa mapuje na zručnosti, ktoré už máte. Plánovanie kapacity, monitorovanie výkonu, správa pamäte, orchestrácia viacerých uzlov: to sú vaše kľúčové kompetencie uplatnené na nový hardvér.

Kritické rozdiely sú:

1. **Kapitálová náročnosť je vyššia.** Dobre vybavený databázový server stojí 20 000 – 50 000 $. Jediný inferenčný uzol s 8 GPU stojí 200 000 – 400 000 $. Stávky na jedno nasadenie sú o rád väčšie.

2. **Záťaž je viazaná na pamäť, nie na výpočtový výkon.** Tradičné servery majú často nevyužitú RAM. GPU inferencia je takmer vždy obmedzená VRAM; viac času strávite optimalizáciou alokácie pamäte než využitia CPU.

3. **Zhoda modelu s hardvérom záleží nesmierne.** Vybrať model 120B tam, kde by stačil doladený 20B, nielen mrhá peniazmi; môže to zrútiť celý biznisový prípad. Výber modelu je dnes infraštruktúrne rozhodnutie.

Ďalšia kapitola vezme tieto hardvérové reality a premení ich na úplné porovnanie nákladov s komerčnými API. Kedy dáva vlastný hosting zmysel? Pri akom počte používateľov? Pre ktoré záťaže? Odpoveď, ako by ste čakali, závisí úplne od čísel.

> **Strážca čerstvosti** · *overené apríl 2026 · odhadovaný polčas rozpadu: ~4 – 6 mesiacov*
>
> Táto kapitola cituje konkrétne ceny hardvéru a stav frameworkov; oboje sa hýbe rýchlo. Pri čítaní alebo citovaní znovu overte:
>
> - **Nákupné ceny GPU** v porovnávacej tabuľke hardvéru (H100, H200, A100, L40S, RTX 4090). Počas roka 2025 a do roku 2026 klesali o 10 – 20 % medziročne; očakávajte ďalšie zmäkčovanie, ako sa Blackwell dodáva vo veľkom.
> - **Krajina obslužných frameworkov**: vLLM ostáva produkčným štandardom, ale súťaží s TGI, SGLang a čoraz viac s behovými prostrediami špecifickými pre dodávateľov. Špekulatívne dekódovanie, nástupcovia PagedAttention a optimalizácie špecifické pre MoE sa objavujú každý kvartál.
> - **Pomery konfigurácia – používatelia** (napr. „2× H100 obslúži 100 používateľov pri INT8“) sa posúvajú, ako sa zlepšuje efektivita inferencie. Dnešná konfigurácia pre 100 používateľov môže o 12 mesiacov obslúžiť 150 – 200 používateľov na tom istom hardvéri.
> - **Architektúra KV cache a špecifiká cachovania promptov v API**: KV na token silno závisí od počtu KV hláv (návrhy MHA vs GQA vs MQA vs MLA sa líšia 10× a viac) a ceny a TTL cachovania promptov u dodávateľov sa revidujú každý kvartál. Pri citovaní znovu overte referenčné čísla Llama 3 70B a TTL Anthropicu 5 minút / 1 hodina.
>
> Štrukturálne rámcovanie (VRAM dominuje dimenzovaniu, KV cache škáluje so súbežnými používateľmi, priepustnosť je úzke hrdlo) je stabilné a dobre zostarne.
