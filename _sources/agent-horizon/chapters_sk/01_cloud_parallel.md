# Kapitola 1: Paralela s cloudom

---

Ak ste v podnikovom IT viac než desať rokov, spôsob, akým sa v roku 2026 debatuje o vývoji agentov, by vám mal pripadať podozrivo známy.

Traja dodávatelia základných modelov (Google, OpenAI, Anthropic) tlačia vyleštené, názorovo vyhranené vývojárske sady, s ktorými postavíte agenta za jedno popoludnie, pokiaľ ostanete v ich ekosystéme. Menší zhluk dodávateľsky neutrálnych frameworkov (LangGraph, CrewAI) trvá na tom, že jedinou zodpovednou voľbou sú prenositeľné abstrakcie, ktoré prežijú zmenu poskytovateľa modelu. Medzi tým sa protokol s názvom Model Context Protocol (MCP) potichu stal štandardným spôsobom, akým agenti siahajú po nástrojoch a dátach. Je otvorený, spravovaný nadáciou, má desiatky miliónov stiahnutí SDK mesačne a väčšina odvetvia sa o ňom prestala hádať.

Vymeňte mená a máte takmer presne rozhovor, ktorý sme viedli medzi rokmi 2010 a 2015. Vyleštené dodávateľské sady boli AWS, Azure, GCP. Neutrálne frameworky boli Kubernetes a Docker. Tichý protokol bol HTTP. Debata nebola o tom, *či* ísť do cloudu; bola o tom, či sa upísať *jednému* cloudu a prijať lock-in, alebo stavať na prenositeľných abstrakciách a zaplatiť daň za abstrakciu vopred.

Tvrdenie tejto brožúry je, že agentná krajina znovu prehráva cloudový scenár. Nie v každom detaile a nie rovnakou rýchlosťou. Ale dosť blízko na to, aby vás funkčný mentálny model toho, ako prebehol prechod do cloudu, dostal väčšinu cesty k funkčnému mentálnemu modelu toho, ako prebehne prechod k agentom.

**Základné modely sú nový výpočtový výkon. MCP je nové HTTP. Dodávateľské agentné SDK sú nová platforma ako služba. Nezávislé frameworky ako LangGraph sú nový Kubernetes.** To je jednovetová verzia zvyšku tejto knihy.

## Prečo paralela platí

Hŕstka hyperškálových dodávateľov má na dne stacku nedobytnú nákladovú výhodu. V roku 2012 nikto nedokázal vyrovnať cenu AWS za jadro, lebo AWS amortizoval svoju infraštruktúru naprieč miliónmi zákazníkov. Dnes nikto nedokáže vyrovnať cenu OpenAI alebo Anthropicu za token, lebo amortizovali náklady na trénovanie naprieč podobne obrovskou používateľskou základňou. Nákladová krivka je štrukturálna, nie dočasná. Prenajímať je lacnejšie než vlastniť, s výnimkou úzkej množiny záťaží, kde súlad s predpismi, latencia alebo dátová suverenita vynucujú inú voľbu.

Dodávatelia, ktorí predávajú lacnú spodnú vrstvu, sa vám snažia predať aj vrstvu nad ňou. AWS nepredával iba EC2: tlačil Elastic Beanstalk, Lambdu, SageMaker a desiatky ďalších spravovaných služieb, ktoré sú mimoriadne pohodlné, kým nikdy nebudete chcieť z AWS odísť. Dodávatelia základných modelov robia to isté: Google tlačí ADK + Vertex, OpenAI tlačí Agents SDK s hostovanými sandboxmi, Anthropic tlačí Claude Agent SDK so zabudovanými nástrojmi na ovládanie počítača. Gravitačný ťah je identický.

A v oboch prípadoch v reakcii vznikla neutrálna stredná vrstva. Nie preto, že by dodávateľské ponuky boli zlé, ale preto, že kritická masa podnikov usúdila, že možnosť vymeniť spodnú vrstvu bez prepisovania tej hornej stojí za tie inžinierske náklady.

## Kde sa paralela láme

Dobrá analógia je taká, ktorú viete záťažovo otestovať. Táto má dve trhliny, ktoré stojí za to označiť hneď na úvod.

**Časová os je stlačená.** Prechod do cloudu potreboval približne desaťročie, kým dosiahol ustálený tvar. Agentný stack sa dostal od „zaujímavého experimentu“ (koniec 2022) k „ustálenému protokolu plus súperiacim frameworkom“ (začiatok 2026) za menej než štyri roky. Či to znamená, že konečný tvar príde o ďalšie štyri roky, alebo či sme v ekvivalente roka 2010 s ďalším desaťročím vretia pred sebou, je otvorená otázka. Kapitola 10 ju berie vážne.

**Lock-in je hlbší.** Keď podnik migroval z AWS, PostgreSQL bol stále PostgreSQL a Java bola stále Java. Časti špecifické pre dodávateľa (fronty, DNS, identita) boli nahraditeľné. V agentnom svete, keď podnik stavia na schopnosti Clauda ovládať počítač, tá schopnosť nie je prenositeľná abstrakcia; je zapečená do toho, ako bol model Anthropicu trénovaný. Nemôžete pustiť ten istý pracovný postup cez GPT-4o a čakať, že sa bude správať rovnako. Lock-in v cloudovej ére bol väčšinou o okolitých službách. Lock-in v agentnej ére môže siahať až dole k samotnému správaniu modelu.

Obe výhrady si založte a majte ich na pamäti pri čítaní. Cloudová analógia je lešenie, nie stavebný plán.

## Európska vráska

Jedna črta cloudovej éry stojí za včasné pomenovanie, lebo sa pravdepodobne zopakuje. Európsky prechod do cloudu bol pomalší než americký. GDPR ešte nebolo plne v platnosti, ale normy ochrany údajov urobili z cezhraničného prenosu dát živú inžiniersku, nielen právnu otázku. Predvídateľný dôsledok: kým sa európske podniky vážne presunuli do cloudu, mohli preskočiť bolestivé skoré lekcie. Multi-cloud už bol uznaný vzor; dodávatelia už boli prinútení ponúkať nástroje na prenositeľnosť. Európsky trh v podstate **preskočil fázu 1**.

Existuje dôveryhodný argument, že EÚ to s agentmi urobí znova. AI Act je silnejšia vynucovacia sila, než bolo GDPR pre cloud. Obavy o suverenitu sú ostrejšie, nie miernejšie. A hnutie za suverénnu AI naprieč Európou tlačí architektonický vzor (smerovanie nezávislé od modelu s vykonávaním on-prem alebo v regióne EÚ pre regulované dáta), ktorý vyzerá skôr ako zrelý agentný stack než ako raný.

Či k preskoku naozaj dôjde, závisí od vecí, ktoré sú v apríli 2026 skutočne nepoznateľné. Ale vzor je dosť silný na to, aby si každý európsky podnik, ktorý plánuje svoju agentnú stratégiu, položil aspoň otázku: *chystáme sa zopakovať cloudový cyklus, alebo preskočiť dopredu?* Kapitola 9 to rozvíja priamo.

Zvyšok tejto brožúry je rozpracovaním obrazu vyššie. Cieľom až po kapitolu 11 je byť dosť konkrétny na to, aby ste po dočítaní vedeli kolegovi povedať, čo je MCP, prečo ADK a LangGraph nie sú v tej istej kategórii a čo by s tým vaša organizácia mala vlastne robiť.

---

*Ďalej: [Kapitola 2: Vrstvová torta](02_layer_cake.md)*
