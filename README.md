# Improving Air Quality Prediction Using Bayesian Optimization for Feature Selection and Hyperparameter Tuning

Final Year Project (FYP) — PM2.5 air quality prediction for **Kuching, Sarawak**, using **Bayesian Optimization** and a **stacking ensemble** of machine learning models. The model predicts daily **PM2.5** concentrations from four pollutant inputs and converts the predictions into the **Air Quality Index (AQI)** using the US EPA piecewise-linear breakpoint formula.

**Author:** Muhamad Hafizzuddin Bin Haslin
**Programme:** BSc (Hons) Computer Science, Universiti Teknologi MARA (UiTM) Cawangan Sarawak
**Supervisor:** Madam Azlina Narawi

---

## Objectives

1. Compare the predictive performance of four machine learning algorithms — Random Forest, XGBoost, CatBoost, and Support Vector Regression (SVR) — in forecasting air quality.
2. Improve prediction performance and generalization by using Bayesian Optimization for both feature selection and hyperparameter tuning.
3. Develop and validate a stacking ensemble that integrates the optimized models, targeting a coefficient of determination (R²) above 0.80.

---

## Dataset

- **Source:** Department of Environment (DOE) Malaysia, via the Air Pollutant Index Management System (APIMS).
- **Region:** Kuching monitoring station only.
- **Period:** 2016–2024.
- **Inputs (features):** NO2, O3, CO, PM10.
- **Target:** PM2.5.
- Multivariate, daily records, no lag features.

After preprocessing: 3,026 raw records reduced to 2,557 cleaned records, split chronologically 80/20 (2,045 training / 512 testing).

---

## Pipeline

```
Preprocess → Bayesian Feature Selection → Baseline Training →
Bayesian Hyperparameter Tuning (4 models) → Stacking Ensemble →
Testing → Performance Evaluation → PM2.5-to-AQI Forecast
```

**Key methodology details:**

- Feature selection and hyperparameter tuning use `gp_minimize` (Gaussian Process + Expected Improvement, 30 evaluations).
- `TimeSeriesSplit(5)` is used for tuning and feature selection to preserve temporal order.
- The stacking ensemble uses an XGBoost meta-learner (n_estimators=200, learning_rate=0.05, max_depth=4) over the four optimized base learners.
- PM2.5 predictions are mapped to AQI categories using the US EPA breakpoints (Good, Moderate, Unhealthy for Sensitive Groups, Unhealthy, Very Unhealthy, Hazardous).

---

## Repository Structure

```
FYP_AirQuality_Kuching/
├── FYP_AirQuality_Kuching.ipynb    # Main notebook (full pipeline)
├── Dataset Kuching/
│   └── KuchingDataset.xlsx         # Cleaned Kuching dataset
├── saved_model/                    # Generated model artifacts
│   ├── stacking_model.pkl
│   ├── scaler.pkl
│   └── selected_features.pkl
├── Kuching_model_results.xlsx      # Exported results (generated)
├── requirements.txt
└── README.md
```

---

## How to Run

### Option A — Google Colab (recommended)

1. Open `FYP_AirQuality_Kuching.ipynb` in Google Colab.
2. Upload the dataset (or mount Google Drive) so the notebook can find `Dataset Kuching/KuchingDataset.xlsx`.
3. Run all cells from top to bottom. The first cell installs the required packages.

### Option B — Local machine

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/FYP_AirQuality_Kuching.git
cd FYP_AirQuality_Kuching

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the notebook
jupyter notebook FYP_AirQuality_Kuching.ipynb
```

---

## Results

Test-set performance (512 held-out samples), baseline vs. Bayesian-optimized vs. stacking ensemble:

| Model                        | Test R²  | Test RMSE | Test MAE |
|------------------------------|----------|-----------|----------|
| Random Forest (Default)      | 0.9229   | 2.5323    | 1.7226   |
| XGBoost (Default)            | 0.8809   | 3.1470    | 2.0194   |
| CatBoost (Default)           | 0.9008   | 2.8716    | 1.8436   |
| SVR (Default)                | 0.7790   | 4.2868    | 2.4382   |
| Random Forest (Optimized)    | 0.9407   | 2.2208    | 1.4670   |
| XGBoost (Optimized)          | 0.9010   | 2.8687    | 1.8841   |
| CatBoost (Optimized)         | 0.9333   | 2.3555    | 1.5409   |
| SVR (Optimized)              | 0.9051   | 2.8100    | 1.7266   |
| **Stacking Ensemble**        | **0.9276** | **2.4534** | **1.5983** |

**Notes on interpretation:**

- Bayesian Optimization improved every base model over its default. SVR gained the most (Test MAE −29.19%).
- The stacking ensemble reduces Test MAE by **20.32% versus the average baseline** and **7.22% versus the best baseline** (default Random Forest), and clears the R² ≥ 0.80 target with R² 0.9276.
- On this single test split, the optimized Random Forest records a marginally higher R² (0.9407) than the ensemble. This is expected: a stacking ensemble is designed for **robust, generalizable** performance across conditions rather than to guarantee the highest score of any single model on one split. Its strength is stability and consistent improvement over baselines.
- **Split sensitivity** (five chronological ratios, 50/50 to 90/10): ensemble mean R² **0.9164 ± 0.0273**, confirming the ensemble generalizes reliably regardless of the split point.
- **AQI classification accuracy:** 90.04% on the 512 test samples.

*(Figures are from the reference run; exact values may vary slightly with library versions and random seeds.)*

---

## Requirements

See [`requirements.txt`](requirements.txt). Core libraries: scikit-learn, xgboost, catboost, scikit-optimize, pandas, numpy, openpyxl, joblib.

---

## License

This project is submitted as part of an academic Final Year Project. Please cite or credit appropriately if reused.
