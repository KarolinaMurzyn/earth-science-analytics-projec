## Analiza eksploracyjna danych (EDA) – wnioski

Analiza obejmuje dane godzinowe ERA5 dla 9 krajów europejskich (Polska, Francja, Hiszpania, Norwegia, Rumunia, Turcja, Węgry, Włochy, Grecja) i 36 miast za okres **1940–2026** (~3 mln rekordów na kraj).

### Temperatura

- Najcieplejsze kraje: **Grecja (śr. 16,33°C), Turcja (14,94°C), Włochy (14,79°C), Hiszpania (14,76°C)**
- Najzimniejszy kraj: **Norwegia (śr. 4,25°C)** – ekstremum min. –36°C
- Polska, Rumunia, Węgry wykazują **klimat kontynentalny/umiarkowany** ze średnią ~8–11°C
- Najcieplejsze miasto: **Antalya (18,06°C)**, najzimniejsze: **Tromsø (0,68°C)**

### Opady

- Najwięcej opadów: **Norwegia (śr. 0,163 mm/h)** i **Bergen** jako najbardziej deszczowe miasto
- Najmniej opadów: **Grecja (0,072 mm/h), Hiszpania (0,061 mm/h)**
- Braki danych w kolumnie opadów były wyłącznie **MNAR** (brak opadu = brak wartości) – uzupełnione zerami

### Wilgotność i punkt rosy

- Najwyższa wilgotność względna: **Norwegia (~79%) i Polska (~79%)**
- Najniższa: **Turcja (~66%) i Hiszpania (~68%)**
- Różnica temperatura–punkt rosy (wskaźnik suchości): największa w **Turcji (~7,4°C) i Hiszpanii (~6,9°C)**, najniższa w **Norwegii (~3,5°C)**
- Kraje południowe mają wyższy punkt rosy (więcej pary wodnej), ale niższą wilgotność względną, co wynika z wyższych temperatur

### Wiatr

- Najsilniejszy wiatr: **Polska (śr. 3,62 m/s)**
- Najsłabszy wiatr: **Grecja (śr. 2,22 m/s)**

### Jakość danych

- Brak duplikatów we wszystkich zbiorach
- Brak braków danych po uzupełnieniu opadów zerami
- Wartości mieściły się w fizycznie możliwych zakresach (temperatury –36°C do +45°C, opady do 27 mm/h, wiatr do ~20 m/s)

---

## Model predykcji temperatury – opis i wyniki

### Metodologia

Zastosowano podejście **direct multi-horizon forecasting** z modelem **CatBoost** – dla każdego horyzontu prognozy (od 1 do 7 dni) trenowany był **osobny model**. Podejście to wybrano świadomie zamiast recursive forecasting, które kumuluje błędy przy wielokrotnym użyciu własnych predykcji.

**Cechy wejściowe (feature engineering):**
- Wartości historyczne temperatury z lagami: 1, 2, 3, 7, 14, 21, 30, 60, 365 dni
- Różnice między lagami: `templag1–lag7`, `templag7–lag14`, `templag7–lag30`
- Kroczące średnie i odchylenia standardowe (okna 7, 14, 30 dni) – liczone wyłącznie na danych historycznych (bez data leakage)
- Lagi dla wilgotności, prędkości wiatru i opadów (1, 2, 3, 7, 14, 30 dni)
- Cechy sezonowe: `sin/cos(dzień roku)`, `sin/cos(miesiąc)`, `dzień roku`, `miesiąc`
- Zmienne kategoryczne: `miasto`, `kraj`

**Podział danych (chronologiczny):**
| Zbiór | Zakres dat |
|---|---|
| Treningowy | do 2016-01-01 (~986 tys. próbek) |
| Walidacyjny | 2016–2021 (~65,7 tys. próbek) |
| Testowy | od 2021-01-01 (~68,8 tys. próbek) |

### Wyniki – błędy predykcji na zbiorze testowym

| Horyzont prognozy | MAE (°C) | RMSE (°C) |
|---|---|---|
| **1 dzień** | **1,87** | **2,47** |
| 2 dni | 2,16 | 2,81 |
| 3 dni | 2,30 | 2,98 |
| 4 dni | 2,39 | 3,08 |
| 5 dni | 2,43 | 3,14 |
| 6 dni | 2,47 | 3,18 |
| **7 dni** | **2,49** | **3,21** |

### Interpretacja wyników

- Błąd **RMSE rośnie wraz z horyzontem** – z 2,47°C dla 1 dnia do 3,21°C dla 7 dni, co jest zgodne z oczekiwaniami: im dalej w przyszłość, tym trudniejsza prognoza
- **MAE na poziomie ~1,9–2,5°C** oznacza, że model przeciętnie myli się o ok. 2°C, co jest bardzo dobrym wynikiem dla prognozy dziennej temperatury w skali całej Europy (36 miast, różne klimaty)
- Największy skok błędu następuje między horyzontem 1 a 2 dni, potem krzywa błędu stabilizuje się – model uczy się wzorców sezonowych i lagów dobrze
- Dashboard wyświetla **prognozę na 7 kolejnych dni** dla każdego wybranego miasta, bazując na ostatnich dostępnych danych (ostatnia data w zbiorze: 2026-03-26)