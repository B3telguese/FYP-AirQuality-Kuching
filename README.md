<div align="center">

# 🌿 Kuching Air Quality Prediction

### From pollutant observations to PM2.5 predictions

**Bayesian optimization · Stacking ensemble · AQI visualization**

<p>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Flask-111827?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
<img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="scikit-learn" />
<img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter" />
</p>

**[📄 Read the report](Report%20n%20Dataset/Report%20FYP.pdf)** ·
**[📊 Explore datasets](Report%20n%20Dataset/)** ·
**[📓 View notebook](FYP_AirQuality_Kuching-master.ipynb)** ·
**[🚀 Local setup](#-run-the-dashboard-on-windows)**

Final Year Project · **Muhamad Hafizzuddin Bin Haslin**  
Universiti Teknologi MARA · Supervisor: **Madam Azlina Narawi**

</div>

---

## 🎯 About the research

**Improving Air Quality Prediction Using Bayesian Optimization for Feature Selection and Hyperparameter Tuning** investigates Random Forest, XGBoost, CatBoost, and Support Vector Regression using Kuching air-quality observations. A stacking ensemble combines the optimized base learners using an XGBoost meta-learner.

The repository includes a Flask dashboard, the primary research notebook, saved Kuching model artifacts, datasets for three Sarawak cities, and the FYP report. These materials are shared as a research portfolio and reproducibility resource, not an operational air-quality advisory service.

## 🧭 Explore the project

| Start here | What you can explore |
| :--- | :--- |
| 📄 [FYP report](Report%20n%20Dataset/Report%20FYP.pdf) | Research background, methodology, and findings |
| 📓 [Research notebook](FYP_AirQuality_Kuching-master.ipynb) | Feature selection, tuning, stacking, evaluation, and export |
| 📊 [Kuching datasets](Report%20n%20Dataset/Dataset%20Kuching/) | Primary study datasets |
| 🗂️ [Bintulu datasets](Report%20n%20Dataset/Dataset%20Bintulu/) · [Miri datasets](Report%20n%20Dataset/Dataset%20Miri/) | Supporting city datasets and preprocessing files |
| 🖥️ [Dashboard backend](main.py) · [Interface](templates/index.html) | Upload, prediction, visualization, and Excel export |
| 🧠 [Saved Kuching model](saved_model/) | Model, scaler, and feature artifacts |
| 🔎 [Implementation notes](docs/IMPLEMENTATION_NOTES.md) | Validation details and interpretation limits |

**Just browsing?** Open the report, datasets, or notebook directly on GitHub. No installation or model training is needed.

## 🖥️ Dashboard features

- Upload CSV or Excel pollutant records.
- Predict PM2.5 using saved model artifacts without retraining.
- Compare observed and predicted concentrations.
- Map predicted PM2.5 to the AQI categories implemented in the code.
- Inspect model comparisons and export an Excel report.

**Input requirement:** the current upload workflow expects `NO2`, `O3`, `CO`, `PM10`, and observed `PM2.5`; `Date` is optional. It uses observed PM2.5 for evaluation and drops rows missing that target. This is an evaluation/nowcasting workflow, not a future forecast endpoint accepting only a date.

## 🚀 Run the dashboard on Windows

Clone the repository and open CMD in its root:

```cmd
git clone https://github.com/B3telguese/FYP-AirQuality-Kuching.git
cd FYP-AirQuality-Kuching
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m flask --app main run
```

Open **http://127.0.0.1:5000/**. This command serves the app locally without enabling the debug mode configured in `python main.py`.

The app expects `saved_model/stacking_model.pkl`, `saved_model/scaler.pkl`, and `saved_model/all_features.pkl`. Keep these files together. The comparison view also reads `Kuching_model_results.xlsx`, which is not currently uploaded. That view requires the original workbook in the repository root.

The supplied dependency versions are broad minimums, not a locked training environment. Serialized estimators can fail to load with different scikit-learn, XGBoost, or CatBoost versions. Model loading is not proof of reproduction, and a page loading successfully is not proof that the model loaded: the current loader suppresses exceptions. Use only model files from a source you trust.

## 🔬 Research workflow

1. Load Kuching pollutant observations and preprocess them.
2. Define predictor variables and PM2.5 as the regression target.
3. Split the observations and scale the predictors.
4. Select features using Bayesian optimization.
5. Train baseline models and tune the four model families.
6. Combine the tuned models with an XGBoost stacking meta-learner.
7. Evaluate regression performance, investigate split sensitivity, and map PM2.5 to AQI categories.

The main notebook uses `TimeSeriesSplit` for optimization and `cv=5` KFold within stacking. These are different validation procedures; the stacking folds should not be described as time-series cross-validation. Its `passthrough=True` setting passes input features alongside base-model predictions to the meta-learner.

To open the training notebook, separately install the training dependencies:

```cmd
python -m pip install -r requirements-training.txt
jupyter lab FYP_AirQuality_Kuching-master.ipynb
```

Training and sensitivity analysis can be computationally expensive. They are not required to browse the repository or start inference with compatible saved artifacts. The datasets currently live under `Report n Dataset/`. Before running the notebook, adjust its dataset paths to match this layout (for example, `Report n Dataset/Dataset Kuching/KuchingDataset.xlsx`).

## 📈 Results and experiment provenance

The existing repository documented an optimized Random Forest R² of **0.9407** and stacking R² of **0.9276**. These are previously reported reference-run values, not newly reproduced measurements in this update. Consult the notebook outputs and [FYP report](Report%20n%20Dataset/Report%20FYP.pdf) for the associated experiment context. The results workbook is not currently included. This documentation update does not claim that all archived runs share identical metrics or that stacking necessarily outperforms every individual model.

`FYP_AirQuality_Kuching-master.ipynb` is the primary implementation documented here. Bintulu and Miri datasets support additional experiments; `main.py` uses the Kuching artifacts in `saved_model/`.

## 🌬️ AQI interpretation

The code maps PM2.5 to AQI using its embedded breakpoint table: the first concentration interval is **0.0–12.0**, followed by **12.1–35.4**. This documents the implementation; it does not assert equivalence to current US EPA guidance or Malaysia's official API calculation. No breakpoint changes were made in this update. See [implementation notes](docs/IMPLEMENTATION_NOTES.md).

## 📚 Data, reports, and attribution

The datasets and full reports are included at the author's request. DOE is credited as the data source in the original project documentation. Public availability of this repository does not establish a separate open-data license or transfer third-party rights. No blanket software or dataset license has been assigned in this update; retain source attribution and consult the relevant rights holder before redistribution.

## 👤 Author

**Muhamad Hafizzuddin Bin Haslin** · Universiti Teknologi MARA  
Supervisor: **Madam Azlina Narawi**

[View more projects](https://github.com/B3telguese?tab=repositories)

<details>
<summary><strong>Documentation and reproducibility notes</strong></summary>

This README describes the files currently published in the repository. No model training or experiment rerun was performed as part of this presentation update. Reported scores remain attributed to the original research.

</details>
