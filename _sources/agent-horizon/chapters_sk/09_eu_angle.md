# Kapitola 9: Európsky uhol

---

Kapitola 1 naznačila myšlienku, že EÚ by mohla preskočiť fázu lock-inu u dodávateľa v agentnom prechode, rovnako ako pred desaťročím preskočila to najhoršie z fázy cloudového lock-inu. Táto kapitola ten argument vyslovuje výslovne. Je to jadro strategického argumentu brožúry pre európskych čitateľov.

Tvrdenie: kombinácia Aktu EÚ o umelej inteligencii, GDPR, noriem dátovej suverenity a hnutia za suverénnu AI dáva európskym podnikom motiváciu aj krytie zhora na to, aby prijali agentné architektúry, ktoré sú od prvého dňa nezávislé od modelu, viacregionálne a náročné na pozorovateľnosť, namiesto toho, aby prešli hlbokým záväzkom voči dodávateľovi a bolestivou migráciou.

To je skutočná možnosť. Nie jediná. A či by ju mal konkrétny podnik využiť, závisí od okolností. Ale štrukturálne sily ukazujú jedným smerom.

## AI Act ako vynucovacia sila

AI Act, ktorého postupné uplatňovanie sa začalo začiatkom roka 2025 a ktorý dosahuje svoje najzávažnejšie termíny v auguste 2026 a auguste 2027, nie je primárne rozhodnutím o frameworku. Je to vynucovacia sila, ktorá tvaruje architektúru okolo frameworkov.

Ustanovenia, na ktorých záleží najviac, sa vzťahujú na „nasadzujúce subjekty“ vysokorizikových AI systémov, ktorými, čo je kľúčové, bude väčšina podnikov používajúcich agentov. Nasadzujúce subjekty musia: zabezpečiť ľudský dohľad nad rozhodnutiami systému, uchovávať logy umožňujúce sledovateľnosť počas celého životného cyklu systému, monitorovať systém a hlásiť závažné incidenty, uchovávať logy aspoň šesť mesiacov a pri určitých kategóriách vykonať posúdenie vplyvu na základné práva.

Preložme to do architektonických dôsledkov.

**Sledovateľnosť vyžaduje pozorovateľnosť.** Produkčný agent bez štruktúrovaného logu stôp nespĺňa požiadavku na logovanie. Stack pozorovateľnosti z kapitoly 7 nie je voliteľná investícia; je to infraštruktúra súladu.

**Ľudský dohľad vyžaduje integračné háčiky.** Agent nemôže byť čierna skrinka. Ľudia musia mať možnosť kontrolovať, prebiť, zasiahnuť. Frameworky so silnými modelmi spätných volaní a háčikov to splnia ľahšie než frameworky očakávajúce autonómne vykonávanie. Ako by mala vyzerať ľudská strana týchto háčikov v prevádzke (schvaľovacie brány, eskalačné cesty, kedy odovzdanie pomôže a kedy len všetkých spomalí), je témou našej sprievodnej brožúry [LLM-Human Interaction Design Patterns](/llm-human-interaction-patterns/).

**Uchovávanie logov ťahá za sebou dátovú suverenitu.** Šesťmesačné uchovávanie, najmä pri agentoch narábajúcich s osobnými údajmi, vyvoláva otázku: *kde* sú logy uložené, *kto* má prístup. Ich uloženie v infraštruktúre amerického dodávateľa vytvára problémy s cezhraničným prenosom údajov. Európska infraštruktúra pod európskou právnou kontrolou je predvolená bezpečná odpoveď.

**Posúdenie vplyvu vyžaduje transparentnosť.** Pri každom vysokorizikovom prípade použitia treba opísať, čo systém robí, ako a ktoré práva ovplyvňuje. Nepriehľadné čierne skrinky (od frameworku alebo od dodávateľa modelu) to robia ťažším, než by malo byť.

Dokopy to tlačí k špecifickému *tvaru* agentnej architektúry: náročnej na pozorovateľnosť, s človekom v slučke, rešpektujúcej suverenitu, auditovateľnej od začiatku do konca. Tento tvar sa prirodzenejšie zhoduje s pozíciou nezávislý framework + európska infraštruktúra než s pozíciou hlboko integrovaného dodávateľského SDK.

### Rozpracovaný príklad: logovanie podľa AI Actu → architektúra

Agent nasadený na úverové poradenstvo v európskej retailovej banke sedí priamo pod klasifikáciou „vysokorizikový“. Požiadavka Aktu na logovanie a sledovateľnosť sa krok za krokom prekladá takto.

**Ktoré háčiky frameworku.** Potrebujete háčik pred modelom, po modeli, pred nástrojom a po nástroji: každá udalosť označená ID stopy viazaným na sedenie a identifikátorom používateľa. V LangGraphe je to jeden obslužný handler spätných volaní pripojený ku grafu. V OpenAI Agents SDK je to parameter `hooks` plus vlastný mantinel. V Claude Agent SDK je to zabudované API háčikov. ADK vystavuje udalosti životného cyklu cez svoj strom agentov. Framework určuje, koľko z toho napíšete a koľko nakonfigurujete.

**Ktoré úložisko pozorovateľnosti.** Stopy idú do úložiska iba na pripisovanie s možnosťou právneho zadržania (legal hold). Langfuse hostovaný vo vlastnej réžii v EÚ regióne Azure, LangSmith vo vlastnej réžii alebo vlastné objektové úložisko + dopytovacia vrstva. Úložisko musí podporovať pravidlá redakcie osobných údajov pri zápise a selektívne prehratie pri čítaní (na audit) bez obnovenia redigovaných polí.

**Ktorá politika uchovávania.** Minimum podľa AI Actu je šesť mesiacov. Pri úverovom poradenstve to interná banková regulácia tlačí na sedem rokov. Vrstvy uchovávania (horúce 90 dní, teplé 12 mesiacov, studené sedem rokov) namapované na náklady úložiska zhruba 1× / 0,3× / 0,05× za GB a mesiac.

**Ktorá kontrola prístupu.** Dáta stôp sú regulované osobné údaje. Prístup vyžaduje tiket + schvaľovateľa + zalogované čítanie. To je infraštruktúra vrstvy identity (nie práca agentného frameworku), ale musí sa čisto pripojiť na úložisko pozorovateľnosti.

Tri odseky, ku ktorým sa diskusie o výbere frameworku dostanú málokedy. V regulovaných nasadeniach sú to prvé odseky.

## Dátová suverenita: ostrejšia než kedysi

Pri prijímaní cloudu bola dátová suverenita pomalá, tichá starosť, ktorá záležala pri niektorých záťažiach. Pri prijímaní AI stvrdla.

Tri dôvody. **Trénovanie a inferencia AI sú s dátami prepletené viac, než bol výpočtový výkon tradične**: keď pošlete požiadavku na API OpenAI, neposielate len dopyt, ale aj kontext, systémový prompt, výstupy nástrojov a všetky dáta, ktoré má model zvážiť. Pri podnikových agentoch tento kontext bežne obsahuje osobné údaje, dôverné obchodné údaje alebo regulované informácie. Povrch súkromia pri používaní agentov je štrukturálne väčší než povrch súkromia pri prevádzke webového servera.

**Národné stratégie AI povýšili tému politicky.** Každá veľká európska krajina sformulovala postoj k suverénnej AI: že kritická AI infraštruktúra by nemala byť úplne závislá od amerických alebo čínskych dodávateľov. Nie je to len rétorika; produkuje konkrétne financovanie, infraštruktúru a regulačné kroky. Pre podniky v regulovaných sektoroch je zosúladenie s národnou stratégiou AI čoraz viac súčasťou toho, byť dobrým firemným občanom.

**EÚ aktívne investuje do suverénnych alternatív.** Verejné financovanie európskych modelov a poskytovateľov suverénneho cloudu robí príbeh „európskej alternatívy“ dôveryhodnejším než pri cloude. Či budú konkurencieschopné na špičke, je neisté. Či budú *dostatočné* pre široký rozsah podnikových prípadov použitia, je menej neisté. Pravdepodobne áno.

Výsledok: púšťať všetky agentné záťaže cez API hostované v USA je v roku 2026 politicky nabitejšie rozhodnutie, než bolo púšťať cloudové záťaže cez infraštruktúru hostovanú v USA v roku 2016. Ten náboj ovplyvňuje strategické voľby, aj keď litera zákona konkrétnu architektúru nevyžaduje.

> **Poznámka z júla 2026.** Tri mesiace po napísaní tejto kapitoly prestal byť argument hypotetický. Najschopnejšie americké modely boli znovu vydané za bránami: na najvyššej úrovni iba pre preverené firmy (prevažne americké), pod ňou nákladné moderované API. Prístup k špičke je teraz sám osebe odstupňovaný podľa jurisdikcie, čo je presne tá expozícia, ktorú má smerovací vzor nižšie absorbovať. Ako funguje prístup odstupňovaný podľa blokov a kam pravdepodobne smeruje, je zmapované v [Merkantilizme generatívnej AI](/mercantilism-of-genai/#m-bloc).

### Bočný panel: krajina suverénnej AI

Stlačená orientácia v tom, kto skutočne dodáva suverénne alternatívy, lebo mnohí architekti predpokladajú, že pole je redšie, než je.

**Poskytovatelia modelov.** Mistral (Francúzsko): najdôveryhodnejšie európske laboratórium z hľadiska špičky, s Mistral Large a rastúcou rodinou modelov s otvorenými váhami. Aleph Alpha (Nemecko): zamerané na podniky, s modelmi triedy Pharia navrhnutými na regulované nasadenie a so silným výkonom v nemčine. Stability AI (Spojené kráľovstvo): obrazové a textové modely s liberálnym licencovaním. Silo AI (Fínsko, kúpené AMD): viacjazyčné európske modely. Plus obvyklí zabehnutí hráči s otvorenými váhami, ktorých možno prevádzkovať na európskej infraštruktúre: rodina Llama od Mety, séria Qwen, Gemma.

**Suverénny cloud a inferencia.** OVHcloud (Francúzsko), Scaleway (Francúzsko), IONOS (Nemecko), Hetzner (Nemecko), Exoscale (Švajčiarsko): všetci ponúkajú inferenčné regióny iba v EÚ so zmluvnými zárukami rezidencie dát, ktoré americkí hyperškáloví dodávatelia čoraz častejšie vyrovnávajú svojimi suverénnymi ponukami pre EÚ, ale nie vždy *z nich vychádzajú*. Viaceré národné cloudové iniciatívy (nemecký Delos, francúzsky Bleu cez Orange + Capgemini + Microsoft) cielia striktne na verejný sektor.

**Európska pozorovateľnosť.** Langfuse je významná open-source možnosť, hostovateľná vo vlastnej réžii na európskej infraštruktúre. LangSmith vo vlastnej réžii je dostupný, ale novší. Vynára sa hŕstka dodávateľov pozorovateľnosti natívnych pre suverénny cloud.

Príbeh suverénnej AI nie je dokonalý (medzery v špičkových schopnostiach ostávajú a pri niektorých záťažiach pretrvajú), ale je dosť dôveryhodný na to, aby „môžeme používať iba americké API“ bolo v roku 2026 zvyčajne výrokom o rozpočte alebo pohodlí, nie o dostupnosti.

## Európsky smerovací vzor

Naprieč európskymi podnikovými AI programami získava prívržencov konkrétna architektúra. Stojí za výslovné pomenovanie.

**Po prvé.** Neutrálna orchestračná vrstva. Zvyčajne LangGraph, niekedy CrewAI, občas vlastná ľahká vrstva. Dôležitá vlastnosť je, že framework neviaže architektúru na konkrétny model.

**Po druhé.** Smerovacie rozhodnutie pre každú interakciu. Pri každej úlohe architektúra rozhodne, ktorý model, na základe citlivosti dát, zložitosti úlohy, nákladového profilu a niekedy jazyka. Citlivé osobné údaje → lokálne hostovaná Llama alebo Mistral. Ťažké uvažovanie s necitlivými dátami → Claude alebo GPT cez API. Jednoduché smerovacie rozhodnutia → malý lokálny model. Rozhodnutie je explicitné a auditovateľné.

**Po tretie.** Európska infraštruktúra pozorovateľnosti a auditu. Langfuse vo vlastnej réžii, LangSmith vo vlastnej réžii alebo vlastná audítorská vrstva, bežiaca na európskej infraštruktúre, vo vlastníctve podniku, s plnou kontrolou nad uchovávaním a prístupom.

Toto je agentný ekvivalent vzoru hybridného cloudu, ktorý zrelé európske podniky prijali koncom druhej dekády: použiť verejný cloud tam, kde je správnou odpoveďou, držať citlivé jadro pod priamou kontrolou, smerovať podľa záťaže namiesto upísania všetkého jednému poskytovateľovi. Nie najrýchlejšia architektúra na postavenie. Architektúra, ktorá prežije väčšinu politického a regulačného počasia.

## Čo by európski lídri mali skutočne urobiť

Päť stlačených smerov.

**Predpokladajte, že pozorovateľnosť a audit sú nevyhnutné.** Rozpočtujte ich od prvého dňa, nech si vyberiete akýkoľvek framework.

**Vyberajte frameworky s dôveryhodnou cestou k nezávislosti.** Buď nezávislý framework hneď od začiatku, alebo dodávateľské SDK, ktorého závislosť od vrstvy modelu vlastníte ako zámernú strategickú voľbu.

**Navrhujte so smerovaním na mysli.** Aj keď dnes používate jeden model, štruktúrujte systém tak, aby výber modelu pre každú interakciu bol zmenou konfigurácie, nie zmenou architektúry.

**Držte audítorské dáta v Európe.** Požiadavka na uchovávanie nie je tá ťažká časť. Ťažká je suverenita uchovávania. Umiestnite stopy, vyhodnocovacie dáta a stav agentov niekam, kde sa z nich nestane problém cezhraničného prenosu údajov.

**Sledujte regulačný postoj.** Aktívne. Obdobie 2026 až 2027 prinesie prvé zmysluplné vynucovacie kroky podľa AI Actu a tie kroky budú tvarovať normy odvetvia.

Pre väčšinu európskych podnikov stojí výsledná architektúra v prvom roku o niečo viac a za päť rokov podstatne menej v porovnaní s naivným prístupom cez dodávateľské SDK. Pre regulované podniky nemusí byť prístup cez dodávateľské SDK v čase, keď ich agentné programy dozrejú, ani právne životaschopný. Postoj, ktorý táto kapitola opisuje, je obhájiteľný štandard.

> **Čo si z tejto kapitoly odniesť:** EÚ má štrukturálne dôvody (AI Act, dátová suverenita, politika suverénnej AI, pamäť na cyklus cloudového lock-inu) preskočiť „hlboký záväzok voči dodávateľovi nasledovaný bolestivou migráciou“ a ísť rovno k hybridným, nezávislým agentným architektúram náročným na pozorovateľnosť. Nie každý európsky podnik by mal túto možnosť využiť, ale malo by ich to urobiť viac, než ich to robí dnes. Kompromisy medzi frameworkmi sa v Európe rozhodnejšie nakláňajú k nezávislosti než inde. Krajina suverénnej AI je redšia, než naznačujú americké naratívy, ale nie ošúchaná, dosť dôveryhodná na to, aby sa s ňou dalo plánovať. Európsky smerovací vzor (nezávislá orchestrácia + výber modelu pre každú interakciu + európska pozorovateľnosť) je architektúra, ktorá prežije väčšinu regulačného počasia.

---

*Ďalej: [Kapitola 10: Naozaj sa časová os stlačí?](10_squeezed_timeline.md)*
