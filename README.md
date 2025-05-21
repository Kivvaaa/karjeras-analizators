# 🧠 Prakses un algu analizators: Python projekts

## 🎯 Projekta uzdevums

Noslēguma projekta mērķis ir izstrādāt pilnvērtīgu Python programmatūru, kas **automatizē karjeras izpēti**, izmantojot datus no Latvijas darba un prakses tirgus. Projektā tiek izstrādāti divi atsevišķi, bet savstarpēji saistīti rīki:

1. **Algas analīzators** — rīks, kas izmanto tīmekļa parsēšanu (`Selenium`), lai analizētu aktuālās IT vakances vietnē [cv.lv](https://www.cv.lv) pēc lietotāja norādītajiem atslēgvārdiem un izvada informāciju par **vidējo, minimālo un maksimālo algu**.

2. **Prakses filtrs** — rīks, kas izmanto iepriekš apkopotu struktūrētu datu kopu (`vakances.json`), lai meklētu un filtrētu studentu prakses iespējas pēc interesēm, lokācijas, uzņēmuma un termiņa.

3. **Statistikas rīks praksēm** — papildfunkcija, kas analizē visas saglabātās **prakses no prakse.lv** un automātiski izvada:
- **kopējo atrasto prakšu skaitu**,  
- **biežākos uzņēmumus**,  
- **populārākās pilsētas**,  
- **termiņu sadalījumu** (minimālais, maksimālais, vidējais termiņš).

Tādējādi lietotājam ir iespēja:
- ne tikai meklēt konkrētas prakses,
- bet arī iegūt pārskatu par tirgus situāciju studentu praksēm Latvijā.

Lietotājs var brīvi izvēlēties, kurā virzienā strādāt: analizēt tirgus tendences, skatīt kopējo statistiku vai atrast reālu praksi, balstoties uz savām interesēm un kompetencēm.

## 📚 Izmantotās Python bibliotēkas

| Bibliotēka     | Pielietojums                                                                 |
|----------------|-------------------------------------------------------------------------------|
| `selenium`     | Tīmekļa parsēšanai gan no [prakse.lv](https://www.prakse.lv), gan [cv.lv](https://cv.lv); tiek izmantots meklēšanai, pogu nospiešanai, skrollēšanai un datu iegūšanai no vairākām lapām. |
| `bs4` (`BeautifulSoup`) | HTML satura strukturētai apstrādei no prakse.lv; izmanto vakanču bloku izvilkšanai un informācijas nolasīšanai. |
| `requests`     | HTTP pieprasījumu veikšanai, lai lejupielādētu atsevišķu vakanču lapas no prakse.lv. |
| `re`           | Regulāro izteiksmju izmantošanai — piemēram, lai izvilktu algas, termiņus un filtrētu nosaukumus ar nevēlamiem simboliem. |
| `json`         | Vakances datu saglabāšanai un ielādei no lokālā `vakances.json` faila. |
| `time`         | Pauzēm starp Selenium darbībām, lai nodrošinātu pareizu lapu ielādi. |
| `datetime`     | Termiņu pārveidošanai un salīdzināšanai, kā arī vidējā termiņa aprēķināšanai. |

## 🧱 Datu struktūras

Tika definētas sekojošas datu struktūras:

**Vakances dati (`vakances.json`)**  
Strukturēts saraksts (`list`) ar vakances objektiem (`dict`), kur katrs ieraksts satur sekojošus laukus:

- `"Title"` *(str)* — prakses nosaukums;
- `"Company"` *(str)* — uzņēmuma nosaukums;
- `"Location"` *(str)* — pilsēta vai lokācija;
- `"Deadline"` *(str)* — pieteikšanās termiņš (piemēram, `"līdz 15.06.2025"`);
- `"Link"` *(str)* — saite uz prakses sludinājumu;
- `"Requirements"` *(str)* — prasības praktikantam.

**Meklēšanas rezultāti**  
Filtrēts saraksts ar vakancēm, kuras atbilst lietotāja ievadītajiem kritērijiem (interese, vieta, uzņēmums, termiņš).

**Statistikas dati**  
Saraksti, kas satur:

- visas norādītās pilsētas (Location),
- uzņēmumus (Company),
- termiņu datumus (`datetime` formātā)

Izmanto, lai aprēķinātu kopējo skaitu, populārākās lokācijas un termiņu sadalījumu.

**Algu analīzes dati (`salary_list`)**  
Saraksts ar veseliem skaitļiem (`list[int]`), kur katra vērtība ir viena vakances mēnešalga. Tiek aprēķināta:

- vakancēm ar algu skaits,
- vidējā, minimālā un maksimālā alga.

## 🧪 Programmatūras izmantošanas metode

Lietotājs tiek aicināts palaist `main.py` failu, kurā notiek interaktīva saziņa caur konsoles izvēlni. Programma piedāvā trīs funkcionalitātes:

1. **Lejupielādēt jaunas vakances (no prakse.lv)**  
   Tiek izmantots `Selenium`, lai automātiski apmeklētu vietni [prakse.lv](https://www.prakse.lv), ielādētu visus aktuālos prakses sludinājumus un saglabātu tos strukturētā JSON failā `vakances.json`.  
   **Atkarībā no ierakstu skaita šis process var aizņemt aptuveni 5–6 minūtes. Izpildes laikā terminālī tiek parādīts progress, lai lietotājs varētu sekot līdzi procesa gaitai.**

2. **Meklēt un filtrēt prakses iespējas**  
   Lietotājs ievada interesējošu atslēgvārdu (piemēram, “programmēšana”), pilsētu, uzņēmuma nosaukumu vai termiņu. Programma atrod un attēlo visas vakances, kas atbilst šiem kritērijiem. Papildus iespējams apskatīt statistiku par visām saglabātajām praksēm: populārākās pilsētas, uzņēmumi, termiņi u.c.

3. **Analizēt algu informāciju (no cv.lv)**  
   Lietotājs ievada vienu atslēgvārdu (piemēram, “Python”, “SQL”), un programma izmanto `Selenium`, lai meklētu atbilstošās IT vakances vietnē [cv.lv](https://www.cv.lv), izgūst norādītās algas un aprēķina statistiku — vidējo, minimālo un maksimālo mēnešalgu.

---

Visi rezultāti tiek attēloti tieši konsolē. Programma ir paredzēta galalietotājam — nav nepieciešamas Python zināšanas vai manuāla failu apstrāde. Lietotājs mijiedarbojas ar sistēmu caur vienkāršām teksta ievadēm un saņem tūlītēju atgriezenisko saiti.

---

## ✅ Noslēgumā

Projekts sasniedz savu mērķi — automatizē ikdienas karjeras jautājumu risināšanu, piedāvājot trīs praktiskas funkcionalitātes vienuviet:

1. Reālu algu izpēti pēc prasmēm no aktuālām vakancēm vietnē cv.lv;
2. Sakārtotu un meklējamu prakses iespēju sarakstu no prakse.lv;
3. Kopējo statistiku par praksēm — top lokācijas, uzņēmumi un termiņi.

Tas parāda spēju izmantot Python datu iegūšanai no tīmekļa, to apstrādei un lietotājam saprotamas informācijas prezentēšanai.