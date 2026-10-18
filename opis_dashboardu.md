# Dashboard Klimatyczny ERA5 – Opis

Interaktywna aplikacja webowa (Streamlit) do analizy temperatury, opadów, wilgotności i ekstremów klimatycznych dla ponad 20 miast europejskich. Dane pochodzą z reanaliz ERA5 (lata 1940–2026) i obejmują 8 krajów: Polskę, Hiszpanię, Norwegię, Grecję, Węgry, Turcję, Włochy, Rumunię i Francję.

---

## Panel boczny (Sidebar)

Umożliwia filtrowanie całego dashboardu:

- **Kraj** – wybór jednego lub wielu krajów (multiselect)
- **Miasto** – wybór miast z zaznaczonych krajów (domyślnie do 12 miast)
- **Zakres lat** – suwak określający przedział czasowy analizy
- **Główna metryka** – wybór metryki sterującej wykresami (m.in. średnia/min/max temperatura, opady roczne, wilgotność, prędkość wiatru, dni upalne, dni silnego mrozu, dni z ulewą)

<img width="247" height="553" alt="image" src="https://github.com/user-attachments/assets/e9a7a8a6-3f68-40e2-8175-fa170835d736" />

---

## Karty podsumowania

Wyświetlane tuż pod tytułem – 5 kart metryk:

- Liczba krajów w bieżącym filtrze
- Liczba miast w bieżącym filtrze
- Zakres analizowanych lat
- Średnia temperatura [°C]
- Średnia roczna suma opadów [mm]

<img width="951" height="189" alt="image" src="https://github.com/user-attachments/assets/9891307c-f6f4-438f-ba2f-40502313e8b4" />


---

## Zakładki
<img width="719" height="54" alt="image" src="https://github.com/user-attachments/assets/1bdff155-42a1-4468-b49a-ae0f43e66008" />


### 1. Trendy roczne
Liniowy wykres wybranej metryki w czasie – osobno dla poszczególnych miast oraz uśredniony dla krajów.

<img width="1063" height="807" alt="image" src="https://github.com/user-attachments/assets/b1d3ae6b-3d54-4d18-83ca-fbac1fc71eed" />


### 2. Ekstrema klimatyczne
- Wykresy liniowe liczby dni upalnych, dni silnego mrozu i dni z ulewą – według krajów lub miast
- Pogrupowany wykres słupkowy porównujący średnią roczną liczbę dni ekstremalnych między miastami

 <img width="1089" height="865" alt="image" src="https://github.com/user-attachments/assets/cc9f8bd2-4ce3-48f5-8334-e2af51a59f57" />


### 3. Sezonowość miesięczna
- Wykres liniowy średniego przebiegu miesięcznego wybranej metryki dla wszystkich miast
- Mapa ciepła (heatmap) miesięcy dla wybranych lokalizacji

<img width="1071" height="738" alt="image" src="https://github.com/user-attachments/assets/b8470f06-0620-4273-9cb1-db07d8a0f0df" />


### 4. Mapa lokalizacji
- Interaktywna mapa scatter Europy z punktami miast kolorowanymi wybraną metryką
- Karty z wartością najwyższą, najniższą, średnią i medianą

<img width="1054" height="610" alt="image" src="https://github.com/user-attachments/assets/ca49e25f-2e2a-4bfa-aa19-df65194c4df5" />

- Ranking TOP/BOTTOM N lokalizacji na mapie (wykres słupkowy)
- Automatyczna interpretacja tekstowa wyników
- Tabela lokalizacji z wartościami i współrzędnymi geograficznymi

<img width="1074" height="841" alt="image" src="https://github.com/user-attachments/assets/adc0fd7f-d1a0-44b4-9e5a-e378145b6975" />


### 5. Rankingi
Poziomy wykres słupkowy z rankingiem lokalizacji w trybie TOP N / BOTTOM N / TOP+BOTTOM N / Wszystkie według wybranej metryki oraz tabela z wartościami.

<img width="1071" height="703" alt="image" src="https://github.com/user-attachments/assets/f8261417-aee8-487e-b9e6-ad46942ddf6f" />


### 6. Dane
Podgląd surowych danych na poziomie rocznym, miesięcznym lub dziennym z możliwością pobrania przefiltrowanych danych jako plik CSV.

<img width="1045" height="393" alt="image" src="https://github.com/user-attachments/assets/ac965717-84d7-4ae7-8099-653a3f1600f1" />


### 7. Prognoza temperatury
- Prognoza średniej temperatury na kolejne 7 dni (model CatBoost)
- Wykres liniowy prognozy dla wybranych miast

<img width="1069" height="495" alt="image" src="https://github.com/user-attachments/assets/64cc1f79-1047-4a10-8127-22e456842c64" />

- Interaktywna mapa prognozy dla wybranego dnia (suwak)
<img width="1069" height="495" alt="image" src="https://github.com/user-attachments/assets/f361c256-7e15-4cb5-ab46-b0744c2ad644" />

- Ranking najcieplejszych i najchłodniejszych lokalizacji w horyzoncie prognozy

<img width="1060" height="364" alt="image" src="https://github.com/user-attachments/assets/fb267c70-90a0-40c0-9f73-cb1b2abe4ce0" />

- Tabela szczegółowa z wartościami prognoz

<img width="1056" height="338" alt="image" src="https://github.com/user-attachments/assets/de8bc934-dbb2-4f77-8bd1-b5072a153d72" />






---
