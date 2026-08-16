# Kapitola 11: Výber vášho stacku

---

Krajina je zmapovaná. MCP je všadeprítomný protokol na prístupovej vrstve. A2A je vznikajúci protokol pre komunikáciu agent–agent. Orchestračná vrstva sa delí na dodávateľské SDK a nezávislé frameworky. Pozorovateľnosť je prvotriedna starosť. Lock-in má ostré odpovede pre každého dodávateľa. EÚ má konkrétne dôvody sledovať inú architektúru. Predpoveď má šesť vyvrátiteľných indikátorov.

Táto kapitola rozhodnutie stláča. Nie do rebríčka; rebríčky zle starnú. Do piatich otázok, kde vaše poctivé odpovede určia architektúru, ktorá vám sedí, plus rozhodovací strom, ktorý odpovede vykreslí vizuálne, plus rozpracovaná prípadová štúdia regulovanej európskej banky, plus krátky epilóg.

## Päť otázok

Prejdite ich po poradí. Každá zužuje pole.

**1. Kde už leží vaša cloudová vernosť?** Úplne na Google Cloud → ADK je predvolený kandidát. Úplne na AWS → Strands. Úplne na Azure alebo Microsoft 365 → Azure AI Foundry Agent Service. Prenositeľní medzi cloudmi alebo multi-cloud z politiky → prirodzeným stredom sa stávajú nezávislé frameworky (LangGraph, CrewAI). Stavať proti srsti vášho cloudového ekosystému stojí mesiace zbytočnej integračnej práce.

**2. Aká tvrdá je vaša požiadavka na výmenu modelu?** Tvrdá (musíte smerovať podľa súladu / nákladov / jazyka, alebo máte mandát proti lock-inu z predstavenstva) → nezávislý framework. LangGraph je obhájiteľný štandard. Claude Agent SDK je okamžite diskvalifikované; OpenAI Agents SDK je hraničné. Mäkká (uprednostňujete prenositeľnosť, ale neprestavali by ste kvôli nej všetko) → dodávateľské SDK sú životaschopné, najmä ADK a OpenAI Agents. Žiadna → všetky frameworky sú na stole; vyberajte podľa ostatných otázok.

**3. Koľko regulačnej alebo audítorskej váhy leží na tomto nasadení?** Ťažká (bankovníctvo, poisťovníctvo, zdravotníctvo, verejný sektor, obrana, vysokorizikové podľa AI Actu) → pozorovateľnosť a audit sú nevyhnutné. LangGraph + LangSmith (alebo Langfuse vo vlastnej réžii) je najbežnejšie obhájiteľná architektúra. Stredná (GDPR, niektoré sektorové pravidlá) → dodávateľské SDK ostávajú životaschopné s doplnkovou pozorovateľnosťou. Ľahká (interná produktivita, necitlivé) → riadia ostatné otázky.

**4. Ako veľmi potrebujete koordináciu viacerých agentov?** Áno, kľúčovo → vedie ADK, s natívnym A2A a hierarchickou štruktúrou. CrewAI je silná dvojka na prototypovanie; LangGraph viacero agentov zvládne, ale vyžaduje viac explicitného inžinierstva. Možno neskôr → vyberte framework s dôveryhodnou cestovnou mapou pre viacerých agentov + A2A. Jeden agent, pravdepodobne navždy → môže stačiť aj základné LLM v slučke. Najčastejšia chyba tu je preceniť potrebu; mnohé podniky dodávajú systémy s tromi agentmi tam, kde by prácu zvládol jeden dobre promptovaný agent.

**5. Koľko interného inžinierskeho talentu na AI máte?** Hlboký → celý rozsah otvorený; nezávislé frameworky sú príťažlivejšie, lebo si ich cenu môžete dovoliť. Stredný → dodávateľské SDK vstrebú viac inžinierskej záťaže; nezávislé sú životaschopné, ale spotrebujú viac kapacity, než čakáte. Obmedzený → dodávateľské SDK sú správny štandard. Nezávislý framework bez tímu, ktorý ho ťahá, je zlyhaný projekt, ktorý čaká, kým sa stane. Buďte tu neúprosní: podniky sú najviac v pokušení odpovedať optimisticky.

## Rozhodovací strom

<div style="margin: 2rem 0; padding: 1rem; border: 1px solid #e2e8f0; border-radius: 8px; background: #f8fafc; overflow-x: auto;">
<svg viewBox="0 0 780 520" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 780px; height: auto; font-family: 'Helvetica Neue', Arial, sans-serif;">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"/>
    </marker>
    <style>
      .q-node { fill: #1e3a5f; }
      .q-text { fill: white; font-size: 12px; font-weight: 700; }
      .q-sub { fill: rgba(255,255,255,0.85); font-size: 10px; }
      .leaf { stroke-width: 2; }
      .leaf-booklets { fill: #eff6ff; stroke: #3b82f6; }
      .leaf-reports { fill: #f5f3ff; stroke: #8b5cf6; }
      .leaf-guides { fill: #fffbeb; stroke: #d97706; }
      .leaf-text { font-size: 11px; font-weight: 700; fill: #1e293b; }
      .leaf-sub { font-size: 9.5px; fill: #475569; }
      .edge { stroke: #94a3b8; stroke-width: 1.5; fill: none; }
      .edge-label { font-size: 10px; fill: #475569; font-weight: 600; }
    </style>
  </defs>

  <!-- Title -->
  <text x="390" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1e3a5f">Agentný stack · rozhodovací strom</text>

  <!-- Root: Q3 Regulatory weight -->
  <rect class="q-node" x="320" y="40" width="140" height="44" rx="6"/>
  <text class="q-text" x="390" y="58" text-anchor="middle">O3: Regulačná váha?</text>
  <text class="q-sub" x="390" y="72" text-anchor="middle">Vysoké riziko? Audit?</text>

  <!-- Branch Heavy -->
  <path class="edge" d="M 380 84 L 200 120" marker-end="url(#arrow)"/>
  <text class="edge-label" x="270" y="98">Ťažká</text>

  <!-- Branch Light/Medium -->
  <path class="edge" d="M 400 84 L 580 120" marker-end="url(#arrow)"/>
  <text class="edge-label" x="490" y="98">Ľahká / stredná</text>

  <!-- Q2 Model swap (on heavy path) -->
  <rect class="q-node" x="130" y="125" width="140" height="44" rx="6"/>
  <text class="q-text" x="200" y="143" text-anchor="middle">O2: Výmena modelu?</text>
  <text class="q-sub" x="200" y="157" text-anchor="middle">Smerovanie / anti-lock-in?</text>

  <!-- Q1 Cloud (on light/med path) -->
  <rect class="q-node" x="510" y="125" width="140" height="44" rx="6"/>
  <text class="q-text" x="580" y="143" text-anchor="middle">O1: Cloudová vernosť?</text>
  <text class="q-sub" x="580" y="157" text-anchor="middle">GCP / AWS / Azure / iná?</text>

  <!-- Leaves on heavy path -->
  <path class="edge" d="M 170 169 L 90 210" marker-end="url(#arrow)"/>
  <text class="edge-label" x="115" y="190">Tvrdá</text>
  <path class="edge" d="M 230 169 L 310 210" marker-end="url(#arrow)"/>
  <text class="edge-label" x="280" y="190">Mäkká / žiadna</text>

  <!-- Leaf: LangGraph + Langfuse self-hosted (Heavy + Hard) -->
  <rect class="leaf leaf-booklets" x="10" y="215" width="175" height="90" rx="6"/>
  <text class="leaf-text" x="97" y="235" text-anchor="middle">LangGraph + vlastný</text>
  <text class="leaf-text" x="97" y="250" text-anchor="middle">Langfuse / LangSmith</text>
  <text class="leaf-sub" x="97" y="270" text-anchor="middle">Smerovanie medzi modelmi,</text>
  <text class="leaf-sub" x="97" y="283" text-anchor="middle">stopy audítorskej kvality,</text>
  <text class="leaf-sub" x="97" y="296" text-anchor="middle">pozorovateľnosť v EÚ regióne</text>

  <!-- Leaf: Azure AI Foundry Agent Service with heavy compliance (Heavy + Soft/None) -->
  <rect class="leaf leaf-reports" x="230" y="215" width="175" height="90" rx="6"/>
  <text class="leaf-text" x="317" y="235" text-anchor="middle">Foundry Agent Service</text>
  <text class="leaf-text" x="317" y="250" text-anchor="middle">alebo ADK na Vertex EU</text>
  <text class="leaf-sub" x="317" y="270" text-anchor="middle">Súlad od dodávateľa,</text>
  <text class="leaf-sub" x="317" y="283" text-anchor="middle">suverénny región + DPA,</text>
  <text class="leaf-sub" x="317" y="296" text-anchor="middle">doplniť o Langfuse</text>

  <!-- Leaves on light/medium path (Q1) -->
  <path class="edge" d="M 550 169 L 460 210" marker-end="url(#arrow)"/>
  <text class="edge-label" x="490" y="190">GCP / AWS / Azure</text>
  <path class="edge" d="M 610 169 L 700 210" marker-end="url(#arrow)"/>
  <text class="edge-label" x="670" y="190">Neutrálna</text>

  <!-- Leaf: Vendor SDK fit to cloud (Light + Major cloud) -->
  <rect class="leaf leaf-guides" x="380" y="215" width="175" height="90" rx="6"/>
  <text class="leaf-text" x="467" y="235" text-anchor="middle">Dodávateľské SDK</text>
  <text class="leaf-text" x="467" y="250" text-anchor="middle">podľa vášho cloudu</text>
  <text class="leaf-sub" x="467" y="270" text-anchor="middle">ADK na GCP,</text>
  <text class="leaf-sub" x="467" y="283" text-anchor="middle">Strands na AWS,</text>
  <text class="leaf-sub" x="467" y="296" text-anchor="middle">Azure Agent na Azure</text>

  <!-- Q5 Talent (Neutral branch) -->
  <rect class="q-node" x="620" y="215" width="140" height="44" rx="6"/>
  <text class="q-text" x="690" y="233" text-anchor="middle">O5: Interný talent?</text>
  <text class="q-sub" x="690" y="247" text-anchor="middle">Hĺbka AI inžinierstva</text>

  <!-- Talent leaves -->
  <path class="edge" d="M 650 259 L 570 310" marker-end="url(#arrow)"/>
  <text class="edge-label" x="590" y="286">Hlboký / stredný</text>
  <path class="edge" d="M 720 259 L 720 310" marker-end="url(#arrow)"/>
  <text class="edge-label" x="728" y="290">Malý</text>

  <!-- Leaf: LangGraph or CrewAI (Neutral + Deep) -->
  <rect class="leaf leaf-booklets" x="480" y="315" width="175" height="80" rx="6"/>
  <text class="leaf-text" x="567" y="335" text-anchor="middle">LangGraph (produkcia)</text>
  <text class="leaf-text" x="567" y="350" text-anchor="middle">alebo CrewAI (prototypy)</text>
  <text class="leaf-sub" x="567" y="370" text-anchor="middle">Vlastná pozorovateľnosť</text>
  <text class="leaf-sub" x="567" y="383" text-anchor="middle">+ autentifikácia</text>

  <!-- Leaf: OpenAI Agents or LLM-in-a-loop (Neutral + Limited) -->
  <rect class="leaf leaf-guides" x="660" y="315" width="115" height="80" rx="6"/>
  <text class="leaf-text" x="717" y="335" text-anchor="middle">OpenAI Agents SDK</text>
  <text class="leaf-text" x="717" y="350" text-anchor="middle">alebo LLM v slučke</text>
  <text class="leaf-sub" x="717" y="370" text-anchor="middle">Dodávateľ nesie záťaž;</text>
  <text class="leaf-sub" x="717" y="383" text-anchor="middle">dodať rýchlo</text>

  <!-- Note at bottom -->
  <text x="390" y="465" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">O4 (viac agentov) a O5 (talent) zužujú výber v každom liste; O1 môže prebiť ťažkú vetvu, ak je cloudový záväzok absolútny.</text>
  <text x="390" y="488" text-anchor="middle" font-size="10" fill="#64748b">Legenda farieb: modrá = skôr nezávislé · fialová = dodávateľ s vrstvou súladu · jantárová = rýchla dodávateľská cesta</text>

</svg>
</div>

Strom je pomôcka na rýchle skenovanie, nie náhrada premýšľania. Prípadová štúdia nižšie ukazuje, ako sa otázky skutočne riešia v praxi a kde bola odpoveď stromu nesprávna.

## Rozpracovaný prípad: regulovaná európska banka

Prejdime si kompozitný prípad; detaily sú zliate z reálnych zákaziek, konkrétnosti zmenené.

Stredne veľká európska retailová banka. Zhruba 4 000 zamestnancov v štyroch krajinách EÚ. Retailové produkty (hypotéky, spotrebné úvery, karty), divízia správy majetku, žiadne investičné bankovníctvo. Technologický stack: dominantne Azure, trochu on-prem mainframe pre jadro bankovníctva (obvyklá architektúra európskej banky). Interná vývojárska kapacita: solídna v Jave/.NET, rodiaca sa v AI. Sponzorstvo z vedenia od prevádzkového riaditeľa, ktorému predstavenstvo povedalo, že banka „musí v roku 2026 dodať niečo zmysluplné s AI“, a ktorý si dáva pozor, ktorá zmysluplná vec to bude.

Prípad použitia: interný poradenský asistent pre manažérov vzťahov s klientmi. Zhrnúť klientovo portfólio, označiť anomálie, vytiahnuť relevantné produktové ponuky, pripraviť poznámky na stretnutie, navrhnúť nadväzujúce e-maily. Nie pre zákazníkov. Nerozhoduje o úveroch. Ale neustále sa dotýka osobných údajov a v časti prípravy na stretnutia susedí s regulovanými poradenskými pracovnými postupmi.

### Prechod piatimi otázkami

**O1 Cloudová vernosť.** Primárne Azure, ale s vrstvou suverenity: dáta klientov pre regulované pracovné postupy sa musia spracúvať v regiónoch EÚ a interný bezpečnostný tím je otvorene nepriateľský k akejkoľvek architektúre, ktorá sa natvrdo viaže na jedného amerického dodávateľa. Prvý inštinkt: Azure AI Foundry Agent Service. Strom nesúhlasí (pozri nižšie).

**O2 Výmena modelu.** Tvrdá. Bezpečnostná politika výslovne vyžaduje, aby sa inferencia s osobnými údajmi dala presunúť k inému poskytovateľovi modelu do štyroch týždňov, ak sa konkrétny dodávateľ stane nedostupným alebo nesúladným. Nie je to teoretické: tím sa už v minulosti popálil pri náhlej zmene politiky dodávateľa na inom produkte.

**O3 Regulačná váha.** Ťažká. Pracovné postupy susediace s poradenstvom sa pravdepodobne klasifikujú ako vysokorizikové podľa AI Actu (hoci na judikatúru okolo rozsahu „poradenstva“ ešte čakáme). Šesťmesačné uchovávanie logov je podlaha; interná banková regulácia ho pri čomkoľvek, čo sa dotýka poradenského obsahu, tlačí na sedem rokov. Ročný interný audit + štvrťročná externá kontrola súladu.

**O4 Viac agentov.** Zmysluplne áno. Konečná architektúra chce troch špecialistov: agenta na vyhľadávanie (ťahá dáta klienta a katalóg produktov), poradenského agenta (uvažuje o odporúčaniach), agenta pre súlad (kontroluje výstupy voči politike a označí čokoľvek, čo potrebuje ľudskú revíziu). Smerovanie medzi nimi je štruktúrované, nie ad hoc.

**O5 Talent.** Stredný so sklonom k obmedzenému. Tím má dvoch inžinierov, ktorí už stavali LLM aplikácie. Ani jeden neprevádzkoval LangGraph v produkcii. Kapacita vstrebať krivku učenia je skutočná, ale ohraničená kvartálnym tlakom na dodanie.

### Čo povedal strom

Ťažká regulácia + tvrdá výmena → **LangGraph + Langfuse vo vlastnej réžii, Azure v regióne EÚ, smerovanie medzi modelmi**. To je modrý list.

Architektúra by bola: LangGraph na orchestráciu; Langfuse vo vlastnej réžii na Azure North Europe pre pozorovateľnosť/audit; MCP servery pred CRM, katalógom produktov a knižnicou politík; smerovanie modelov pre každú interakciu: Claude cez Azure (partnerstvo Anthropicu s Azure, so zmluvnou zárukou regiónu EÚ) na úlohy náročné na uvažovanie; lokálne hostovaný Mistral na úlohy dotýkajúce sa osobných údajov; A2A medzi tromi špecializovanými agentmi s kartami agentov registrovanými v internom registri.

To je architektonicky správna odpoveď. Je to aj miesto, kde sa odpoveď rámca a to, čo tím skutočne urobil, rozišli.

### Kde sme rámec prebili

Banka dodala verziu 1 na **OpenAI Agents SDK** cez Azure OpenAI, nie na LangGraphe.

Dôvodom bola O5. Dvaja inžinieri schopní v AI nemali kapacitu súčasne sa učiť LangGraph, postaviť Langfuse vo vlastnej réžii, nakonfigurovať smerovanie medzi modelmi *a* dodať pilot v kvartáli, ku ktorému sa prevádzkový riaditeľ zaviazal. Odpoveď správna podľa rámca bola vzhľadom na organizačnú realitu neuskutočniteľná. A dodať niečo dosť dobré v sľúbenom okne záležalo strategicky viac než dodať architektonicky dokonalú vec o šesť mesiacov neskôr.

Čo sme urobili namiesto toho: OpenAI Agents SDK na orchestráciu, Azure OpenAI s Claudom v regióne EÚ (ktorého Microsoft ponúka od Anthropicu cez trhovisko Azure) ako predvoleným modelom, Azure Monitor + tenký interný obal na sledovanie ako vrstva pozorovateľnosti, natívne mantinely dodávateľa, MCP servery pre interné systémy. Zapísali sme (výslovne, do záznamu o architektonickom rozhodnutí), že ide o dočasnú voľbu, že cieľom migrácie je LangGraph + Langfuse a že určité funkcie (delegovanie medzi agentmi cez A2A, trvanlivé vykonávanie pre dlho bežiace kontroly súladu) sa odložia do migrácie.

Na LangGraph sme migrovali v deviatom mesiaci. Migrácia trvala sedem týždňov vrátane prepnutia pozorovateľnosti. Trvala by dlhšie, keby sme architektúru verzie 1 nenavrhli s vedomím, že je dočasná: konkrétne keby sme nedržali prompty a sady nástrojov čo najviac nezávislé od frameworku a neinvestovali skoro do MCP serverov (ktoré boli tým jedným kúskom, ktorý sa vôbec nemusel meniť). Prompty a MCP servery sa presunuli doslova. Orchestrácia sa čisto prepísala, len čo mal tím kapacitu.

### Čo prípad učí

**Odpoveď správna podľa rámca často nie je odpoveďou správnou podľa načasovania.** Verzia 1, ktorá sa dodá na kompromisnom stacku a zmigruje sa, je často lepšia než verzia 1, ktorá je architektonicky nepoškvrnená a dodá sa o osem mesiacov neskôr. Rozhodovací strom vám dá cieľ. Nie vždy vám dá poradie.

**Zachovanie možností stojí menej, než si ľudia myslia, ak naň navrhujete.** Dve veci, ktoré urobili migráciu zvládnuteľnou (MCP servery pre interné systémy a prompty napísané nezávisle od frameworku), stáli tím verzie 1 zhruba o 10 % viac inžinierskeho času než plne dodávateľsky viazaná alternatíva. Tých 10 % ušetrilo 60 % na migrácii.

**Pozorovateľnosť je to najťažšie na dodatočné doplnenie.** Najslabšou časťou architektúry verzie 1 bola tenká interná vrstva sledovania. Keď sme v jedenástom mesiaci potrebovali pre kontrolu súladu auditovať konkrétne poradenské odporúčanie zo štvrtého mesiaca, stopy existovali, ale neboli prehľadávateľné tak, ako by to ponúkla skutočná platforma pozorovateľnosti. Keby som to robil znova, minul by som tri týždne navyše na postavenie Langfuse už vo verzii 1, aj na dodávateľskom SDK. Všetko ostatné sa dá doplniť dodatočne. História stôp nie.

**Hodiny „musíme migrovať do 3. kvartálu“ zafungovali.** Zapísanie dočasnej povahy do záznamu o rozhodnutí, s pomenovaným cieľom migrácie a pomenovaným dátumom, je to, čo tím udržalo pred zosunutím do stázy „dodávateľské SDK funguje dobre, načo migrovať?“. Záznam mal zuby, lebo ho podpísali traja seniorní zadávatelia. Bez toho by stack verzie 1 pravdepodobne bežal dodnes.

## Epilóg: čo prežije

Táto brožúra bola súborom mentálnych modelov. Vrstvová torta. Paralela s cloudom. Dva protokoly. Dve rodiny frameworkov. Rozsahy lock-inu. Hypotéza európskeho preskoku. Predpoveď so šiestimi indikátormi. Rámec piatich otázok. Prípadová štúdia vyššie.

Ktoré z nich budú o osemnásť mesiacov stále užitočné?

Vrstvová torta bude. Otázka „na ktorej vrstve toto sedí?“ je trvanlivý návyk, ktorý sa vyplatí zakaždým, keď sa oznámi nový kus technológie. Na MCP bude stále záležať; viac, nie menej. Vrstva pozorovateľnosti bude väčšia a zrelšia. A2A bude buď všadeprítomné, alebo ho nahradí niečo, čo rieši ten istý problém pod iným menom; v každom prípade koncept prežije.

Konkrétne frameworky sú ťažšie. LangGraph bude veľmi pravdepodobne stále nezávislým štandardom. Budúcnosť CrewAI je neistejšia. ADK bude pokračovať, lebo motivácie Googlu sa nemenia. Claude Agent SDK sa buď rozšíri, alebo dramaticky zúži podľa toho, ako veľmi bude širší trh chcieť ovládanie počítača špecifické pre Clauda. OpenAI Agents SDK sa predpovedá najťažšie; závisí od rozhodnutí vnútri OpenAI, ktoré nevidíme. Azure a AWS pretrvajú, lebo ich materské firmy to potrebujú.

Konkrétne čísla budú všetky nesprávne. 97 miliónov stiahnutí MCP bude nejaké väčšie číslo. 44 000 hviezdičiek CrewAI sa pohne. Presné schopnosti dodávateľov sa posunú. Každé číslo o nákladoch bude potrebovať revíziu. To je v poriadku. Čísla tu sú, aby ukotvili mentálny model, nie aby niesli váhu samy osebe.

Čo by som povedal kolegovi, ktorý sa pýta, ako túto knihu použiť v roku 2027: *začnite vrstvovou tortou, verte štandardu MCP, vlastnite svoju pozorovateľnosť, rešpektujte lock-in vedome, a keď dôjde na výber stacku, prejdite päť otázok a potom buďte poctiví v tom, ktorú odpoveď dokážete tento kvartál skutočne vykonať.* Zvyšok si aktualizujete, ako sa horizont posúva.

**Konkrétnosti sa zmenia. Disciplína nie.**

---

*Koniec brožúry.*
