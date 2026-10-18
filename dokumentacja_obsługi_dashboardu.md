# Dokumentacja obsługi dashboardu – Climate Dashboard

## Opis projektu

Projekt pobiera dane klimatyczne ERA5 dla wybranych miast europejskich, przetwarza je do formatów dziennych/miesięcznych/rocznych i wizualizuje w interaktywnym dashboardzie Streamlit. Pliki `.parquet` zawierające przetworzone dane **nie są dołączane w repozytorium** i muszą zostać wygenerowane lokalnie przez uruchomienie notatników we właściwej kolejności.

---

## Instalacja bibliotek

W zależności od środowiska uruchomieniowego wybierz jedną z poniższych metod:

**pip:**
```bash
pip install cdsapi xarray netCDF4 pandas pyarrow geopandas plotly matplotlib catboost scikit-learn streamlit
```

**conda:**
```bash
conda install -c conda-forge cdsapi xarray netCDF4 pandas pyarrow geopandas plotly matplotlib scikit-learn streamlit
pip install catboost
```

---

## Kolejność uruchamiania notatników

### Krok 1 – Wczytanie i obróbka danych
`Wczytanie_obrobka.ipynb`

- Wczytuje surowy plik `.parquet`, czyści i przetwarza dane
- Wykonuje konwersję jednostek oraz obliczanie pochodnych zmiennych (punkt rosy, różnica temp–punkt rosy itp.)
- Dane wejściowe: `era5_europa_raw_1940_2026.parquet`

---

### Krok 2 – Agregacja
`agregacja.ipynb`

- Agreguje dane do poziomów: dziennego, miesięcznego i rocznego
- Generuje pliki:
  - `era5_europa_daily.parquet`
  - `era5_europa_monthly.parquet`
  - `era5_europa_yearly.parquet`

---

### Krok 3 – Wstępne wizualizacje (EDA)
`poczatkowe_wizualizacje_post_agregacja.ipynb`

- Eksploracyjna analiza danych na zagregowanych plikach
- Dane wejściowe: pliki dzienne/miesięczne/roczne `.parquet`

---

### Krok 4 – Prognoza temperatury (CatBoost)
`prognoza_tempC.ipynb`

- Trenuje model CatBoost do 7-dniowej prognozy temperatury
- Generuje pliki wynikowe:
  - `catboost_results_metrics.csv`
  - `catboost_test_predictions.csv`
  - `catboost_future_7day_forecast.csv`

---

### Krok 5 – Uruchomienie dashboardu
`app_streamlit_era5_dashboard.py`

Po wygenerowaniu wszystkich plików `.parquet` uruchom dashboard:

```bash
streamlit run app_streamlit_era5_dashboard.py
```

---

## Wymagane pliki danych (generowane lokalnie)

| Plik | Generowany w kroku |
|---|---|
| `era5_europa_raw_1940_2026.parquet` | Krok 1 (dane surowe) |
| `era5_europa_daily.parquet` | Krok 2 |
| `era5_europa_monthly.parquet` | Krok 2 |
| `era5_europa_yearly.parquet` | Krok 2 |
| `catboost_results_metrics.csv` | Krok 4 |
| `catboost_test_predictions.csv` | Krok 4 |
| `catboost_future_7day_forecast.csv` | Krok 4 |

> Wszystkie pliki należy umieścić w **tym samym folderze** co `app_streamlit_era5_dashboard.py`.
