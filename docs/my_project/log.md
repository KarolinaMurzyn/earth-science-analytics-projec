 ## 9.03.2026

Postęp: wybór tematu: "Zmiany klimatyczne na wybranych terenach - analiza trendów w danych z Copernicus Climate Data Store"

Problemy / kwestie do przedyskutowania:

## 16.03.2026

Postęp: 
- zapoznanie się z datasetem ERA5 daily statistics https://cds.climate.copernicus.eu/datasets/derived-era5-single-levels-daily-statistics?tab=download&fbclid=IwY2xjawQk-SBleHRuA2FlbQIxMABzcnRjBmFwcF9pZBAyMjIwMzkxNzg4MjAwODkyAAEeDV6jJCqm5RjlbCSsy0kVYeSa_q7puL6eND7QTjLFBv0a2XvXKdjiY9H8FM0_aem_lk5sSg-70WrsdF1SSNpb5g,
- wybór parametrów meteorologicznych do analizy,
- wybór miast do analizy: Oslo, Kraków, Barcelona (ustalenie zakresu współrzędnych),
- ustalenie zakresu czasowego analizy: 2000–2025,
- ustalenie sposobu pobierania danych: dla każdego dnia i każdego miesiąca z częstotliwością co 6 godzin,
- ustalenie strefy czasowej danych (UTC+1),
- podział pracy w zespole – każda osoba odpowiada za pobranie danych dla okresu 8 lat - do nastepnych zajęć

Wybrane zmienne do projektu:
10m u-component of wind, 10m v-component of wind, 2m dewpoint temperature, 2m temperature, total precipitation, total cloud cover (z możliwością rozszerzenia w dalszym etapie)

Problemy / kwestie do przedyskutowania:
- wybór optymalnego zestawu zmiennych z dużej liczby dostępnych
- ustalenie odpowiednich zakresów przestrzennych (bounding box) dla wybranych miast, aby ograniczyć wielkość pobieranych danych,
- potencjalnie duży rozmiar danych

## 23.03.2026
Postęp:
- pobranie danych dla Krakowa i Oslo i dodanie zmian na githuba wraz ze skryptami 

Problemy / kwestie do przedyskutowania:
- narazie dane zostały pobrane dla Krakowa i Oslo (bez Barcelony) ze względu na bardzo długi czas pobierania

## 30.03.2026
Postęp:
- pobranie danych dla Krakowa i Oslo i dodanie zmian na githuba wraz ze skryptami - lata 2000-2005
- wstępna analiza eksploracyjna wybranych czynników w wybranych latach

Problemy / kwestie do przedyskutowania:
- pytanie, czy obowiązkowe jest ściąganie danych skryptem dostarczonym przez Pana w dniu 30.03, czy możemy zostać przy swoim sposobie (długim ale zakońcoznym sukcesem)

## 13.04.2026
Postęp:
- Pobranie danych dla 9 państw w Europie po 4 miasta skryptem dostarczonym przez Pana 
- wczytanie danych, konwersja jednostek,
- stworzenie nowych zmiennych
     - rok, miesiąc, dzień
     - temp_dew_diff: różnica między temperaturą powietrza a temperaturą punktu rosy jest wskaźnikiem wilgotności powietrza i stopnia jego nasycenia parą wodną. Małe wartości oznaczają powietrze wilgotne, natomiast duże wartości wskazują na powietrze suche
     - humidity: wilgotność względna określa stopień nasycenia powietrza parą wodną i jest jedną z podstawowych charakterystyk klimatu. Wysokie wartości wilgotności są typowe dla obszarów nadmorskich, natomiast niskie dla obszarów o klimacie suchym i kontynentalnym
 - uzupełnienie braków w kolumnie z opadami
 - sprawdzenie, czy występują wartości odstające - czy pomiary są realne
 - wstepne statytyki opisowe na poziomie Państw i miast w każdym państwie i ogólnie
 - połączenie danych w jeden zbiór - kod z zapisem do parquet, ale plik .parquet nie dodany na repo, bo za duży rozmiar 

Problemy / kwestie do przedyskutowania:
- pomysł na finalny dashboard
- jak agregować?

Ustalone na spotkaniu:
- wykres rozkładu dla każdego miasta dorobic
- agreagcja roczna do niektorych wykresow potrzebna napewno bo sie zamarzą wykresy
- agregacja miesięczna do niektórych wykresow itd
- agregacja na dniowe najlepiej finalnie i pozniej juz predykcji itp. suma dobowa opadów
- WAŻNE: w jaki sposob poakzac bardzo intensywne opady ktore trwały np. tylko 3 h, analiza ekstremów opadow na danych godiznowych np. 3h okeinko (rollng window), albo kolumna suma dobowa i suma od jakiegos progu i np. prog to (max - coś) w danym dniu i pwoiedziec z ilu godzin sumujemy wtedy i ze wtedy 4h była ulewa --> finalnie 1 kolumna: suma opadów na dzień, 2 kolumna: suma opadów ale od jakiegoś progu, 3 kolumna: powiedzieć z ilu h sumowlaiśmy w tej 2 kolumnie i wtedy wiemy że np. była ulewa przez 4h
- dashboard:
- ze jest mozliwosc wyboru miast konkretnych, nie robic filtrów na szerkosci i dlg geografiucznej a lista wybieralna maist, że jedna statysyke dla kilku miast poakzywać


## 27.04.2026 | Agregacja czasowa
Postęp:
- Wczytano dane ERA5,
- Zaimplementowano agregację dobową z funkcją ekstremów opadowych
  (próg ulewy ≥10.1 mm/h wg klasyfikacji meteorologicznej)
- Kolumny opadowe: tpmm_sum / tpmm_extreme / extreme_hours
- Zbudowano agregację miesięczną i roczną na bazie danych dobowych
- Dane zapisano do Parquet: daily / monthly / yearly
- Przeprowadzono wstępną EDA: statystyki opisowe, rankingi ekstremów.


## 04.05.2026
Postęp: 
 - Dodano ekstrema temperaturowe (upały oraz mrozy)
 - Wstępna wizualizacja zmiennych.


 ## 04.05.2026 
Postęp:
- stworzenie kompletnego dashboardu klimatycznego w Streamlit,
- implementacja interaktywnych filtrów (kraje, miasta, zakres lat, metryki),
- wizualizacja trendów rocznych dla wybranych parametrów,
- dodanie analizy ekstremów klimatycznych (upały, mróz, ulewy),
- implementacja sezonowości miesięcznej (wykresy + mapa ciepła),
- stworzenie mapy lokalizacji z wykorzystaniem współrzędnych geograficznych,
- dodanie rankingów lokalizacji (TOP / BOTTOM / TOP+BOTTOM / wszystkie),
- możliwość wyboru liczby lokalizacji w rankingach (parametr N),
- wizualne rozróżnienie TOP i BOTTOM na wykresach,
- dodanie tabeli danych oraz możliwości eksportu do CSV,
- poprawa wyglądu dashboardu (layout, styl, karty metryk, spójna estetyka),
- optymalizacja działania (cache, agregacje, przygotowanie danych).

Problemy / kwestie do przedyskutowania:
- ewentualne rozszerzenie dashboardu o predykcję (modele ML / time series),
- możliwość dodania animacji zmian klimatu w czasie.

 ## 18.05.2026 
Postęp:
- Rozszerzono projekt o moduł predykcyjny dla średniej temperatury dobowej.
- Przygotowano dane do modelowania na podstawie agregacji dobowej ERA5.
- Zaimplementowano feature engineering dla szeregów czasowych: opóźnienia temperatury, wilgotności, prędkości wiatru i opadów.
- Dodano cechy sezonowe: dzień roku, miesiąc oraz transformacje sinus/cosinus.
- Przygotowano modele CatBoost dla prognozowania temperatury od 1 do 7 dni do przodu.
- Zastosowano podejście direct multi-horizon forecasting — osobny model dla każdego horyzontu prognozy.
- Wykonano chronologiczny podział danych na zbiór treningowy, walidacyjny i testowy.
- Obliczono metryki jakości prognoz: MAE i RMSE dla każdego horyzontu.
- Zapisano wyniki predykcji i metryki do plików CSV w celu dalszej wizualizacji w dashboardzie.
- Przygotowano wstępne wizualizacje błędów prognozy według horyzontu, miasta i kraju.
- Zrobiono predykcje na realne 7 dni do przodu czyli 27.03-02.04 bo dane kończyły się na 26.03 i zapis wyników do .csv żeby wykorzystać je w dashboardzie
- direct multi-horizon forecasting artykuły: https://medium.com/@aeon.toolkit/forecasting-horizons-da426b7a6c24
- https://skforecast.org/0.16.0/user_guides/direct-multi-step-forecasting.html

Do raportu/dokumnatcji/log trzeba dodać opis notebooka prognoza_tempC czyli opis jego, wnioski itp


## 25.05.2026
Postęp:
- Rozszerzono dashboard klimatyczny o nową zakładkę „Prognoza temperatury”.
- Zintegrowano wcześniej przygotowane modele predykcyjne z aplikacją Streamlit.
- Dodano wizualizację prognoz średniej temperatury na kolejne 7 dni dla wybranych lokalizacji.
- Prognozy zostały połączone z głównymi filtrami dashboardu (kraje, miasta, zakres danych), dzięki czemu użytkownik może analizować wyłącznie wybrane lokalizacje bez dodatkowych filtrów w zakładce prognoz.
- Dodano interaktywny wykres prognoz temperatury dla wielu miast jednocześnie.
- Dodano tabelę prognoz z możliwością przeglądu wartości dla kolejnych dni i horyzontów prognozy.
- Dodano ranking najcieplejszych i najchłodniejszych lokalizacji według prognozowanej temperatury.
- Dodano mapę prognoz temperatury dla wybranego dnia prognozy.
- Ulepszono wygląd i użyteczność dashboardu:
  - nowy panel boczny z opisem projektu,
  - uproszczenie filtrów,
  - poprawa estetyki wykresów i kart,
  - lepsze dopasowanie layoutu do analizy wielu lokalizacji.
- Zoptymalizowano integrację danych prognozowanych zapisanych w plikach CSV z istniejącym dashboardem ERA5.

Problemy / kwestie do przedyskutowania:
- możliwość rozszerzenia prognoz o kolejne zmienne meteorologiczne (opady, wilgotność, wiatr),
- możliwość dodania dłuższego horyzontu prognozy,