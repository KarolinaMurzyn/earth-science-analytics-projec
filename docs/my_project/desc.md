# Projekt – Analiza zmian klimatycznych w Europie z wykorzystaniem danych ERA5

## Cel

Celem projektu jest analiza długoterminowych zmian klimatycznych w wybranych krajach i miastach Europy na podstawie danych ERA5 pochodzących z Copernicus Climate Data Store. Projekt obejmuje identyfikację trendów temperatury, opadów, wilgotności oraz ekstremalnych zjawisk pogodowych, a także budowę modelu prognozowania temperatury powietrza na kolejne dni.

Końcowym efektem projektu jest interaktywny dashboard umożliwiający eksplorację danych historycznych oraz prezentację prognoz klimatycznych dla wybranych lokalizacji.

---

## Metody

W projekcie wykorzystano następujące metody analizy danych:

- eksploracyjną analizę danych (EDA),
- analizę trendów czasowych,
- analizę sezonowości miesięcznej,
- analizę ekstremów klimatycznych (upały, mrozy, intensywne opady),
- agregację danych do poziomu dziennego, miesięcznego oraz rocznego,
- wizualizację przestrzenną z wykorzystaniem map,
- tworzenie rankingów lokalizacji według wybranych wskaźników klimatycznych,
- prognozowanie temperatury metodami uczenia maszynowego.

Do budowy modelu predykcyjnego wykorzystano algorytm CatBoost w podejściu direct multi-horizon forecasting, gdzie dla każdego horyzontu prognozy od 1 do 7 dni trenowany był oddzielny model.

---

## Techniczna implementacja

Projekt został zrealizowany w języku Python z wykorzystaniem środowiska Jupyter Notebook oraz aplikacji Streamlit.

Wykorzystane biblioteki:

- pandas
- numpy
- pyarrow
- plotly
- streamlit
- scikit-learn
- catboost
- matplotlib
- geopandas
- xarray

Proces przetwarzania danych obejmował:

1. Pobranie danych ERA5.
2. Czyszczenie i transformację danych.
3. Konwersję jednostek meteorologicznych.
4. Tworzenie nowych zmiennych opisujących warunki klimatyczne.
5. Agregację danych do różnych poziomów czasowych.
6. Analizę eksploracyjną.
7. Budowę modelu prognostycznego.
8. Implementację dashboardu analitycznego.

Dane przechowywane są w formacie Parquet, co umożliwia szybkie przetwarzanie wielomilionowych zbiorów danych.

---

## Dane

Źródłem danych jest Copernicus Climate Data Store (ERA5).

Zakres projektu obejmuje:

- lata 1940–2026,
- 8 krajów europejskich,
- ponad 30 miast europejskich,
- dane godzinowe agregowane do poziomu dziennego, miesięcznego i rocznego.

Analizowane zmienne obejmują między innymi:

- temperaturę powietrza,
- temperaturę punktu rosy,
- opady atmosferyczne,
- zachmurzenie,
- prędkość wiatru,
- wilgotność względną.

---

## Wyniki

Przeprowadzona analiza pozwoliła na:

- identyfikację różnic klimatycznych pomiędzy krajami Europy,
- analizę zmian temperatury i opadów w czasie,
- identyfikację lokalizacji najbardziej narażonych na ekstremalne zjawiska pogodowe,
- ocenę sezonowości analizowanych parametrów,
- budowę modelu prognozującego średnią temperaturę na kolejne 7 dni.

Uzyskany model osiągnął błąd MAE od około 1,9°C dla prognozy jednodniowej do około 2,5°C dla prognozy siedmiodniowej.

---

## Dashboard

W ramach projektu opracowano interaktywny dashboard Streamlit umożliwiający:

- analizę trendów rocznych,
- analizę ekstremów klimatycznych,
- analizę sezonowości,
- prezentację danych na mapie Europy,
- generowanie rankingów lokalizacji,
- eksport danych,
- prezentację prognoz temperatury na kolejne 7 dni,
- mapową wizualizację prognoz,
- porównanie najcieplejszych i najchłodniejszych lokalizacji w prognozowanym okresie.

Dashboard stanowi końcowy element projektu i umożliwia wygodną analizę danych klimatycznych bez konieczności pracy bezpośrednio na kodzie źródłowym.