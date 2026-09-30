<div align="center">
<h1>Kuching Air Quality Prediction</h1>
<p><strong>Bayesian optimization · PM2.5 prediction · AQI visualization</strong></p>
<p>Final Year Project — Muhamad Hafizzuddin Bin Haslin</p>
<p>Universiti Teknologi MARA · Supervisor: Madam Azlina Narawi</p>
</div>

> **Upload status:** The dashboard, primary notebook, Kuching datasets, and Kuching model files are available. Additional DOE/Bintulu/Miri datasets, reports, figures, archived notebooks, and result workbooks are prepared but awaiting the remaining upload. References below describe the complete project package.

## About the research

**Improving Air Quality Prediction Using Bayesian Optimization for Feature Selection and Hyperparameter Tuning** investigates Random Forest, XGBoost, CatBoost, and Support Vector Regression using Kuching air-quality observations. A stacking ensemble combines the optimized base learners using an XGBoost meta-learner.

The repository includes a Flask dashboard, research notebooks, saved model artifacts, datasets, exported experiment results, and academic reports. These materials are shared as a research portfolio and reproducibility resource, not an operational air-quality advisory service.

## Explore the project

| Resource | Contents |
| --- | --- |
| [Dashboard backend](main.py) | File ingestion, preprocessing, predictions, AQI mapping, and Excel export |
| [Dashboard interface](templates/index.html) | Browser interface for exploring predictions and results |
| [Main research notebook](FYP_AirQuality_Kuching-master.ipynb) | Feature selection, tuning, stacking, evaluation, and export |
| [Kuching data](Dataset%20Kuching/) | Original supplied datasets and preprocessing variants |
| DOE data (pending upload) | Supplied DOE workbooks |
| Academic reports (pending upload) | Full supplied chapter and report PDFs |
| Recorded results (pending upload) | Workbook consumed by the dashboard |
| [Saved model](saved_model/) | Kuching artifacts and separate Miri experiment artifacts |

## Dashboard features

- Upload CSV or Excel pollutant records.
- Predict PM2.5 using saved model artifacts without retraining.
- Compare observed and predicted concentrations.
- Map predicted PM2.5 to the AQI categories implemented in the code.
- Inspect model comparisons and export an Excel report.

**Input requirement:** the current upload workflow expects `NO2`, `O3`, `CO`, `PM10`, and observed `PM2.5`; `Date` is optional. It uses observed PM2.5 for evaluation and drops rows missing that target. This is an evaluation/nowcasting workflow, not a future forecast endpoint accepting only a date.

## Run the dashboard on Windows

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

The app expects `saved_model/stacking_model.pkl`, `saved_model/scaler.pkl`, and `saved_model/all_features.pkl`. Keep these files together. It reads comparison data from `Kuching_model_results.xlsx`.

The supplied dependency versions are broad minimums, not a locked training environment. Serialized estimators can fail to load with different scikit-learn, XGBoost, or CatBoost versions. Model loading is not proof of reproduction, and a page loading successfully is not proof that the model loaded: the current loader suppresses exceptions. Use only model files from a source you trust.

## Research workflow

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

Training and sensitivity analysis can be computationally expensive. They are not required to browse the repository or start inference with compatible saved artifacts. Run notebooks from the repository root so relative paths resolve.

## Results and experiment provenance

The existing repository documented an optimized Random Forest R² of **0.9407** and stacking R² of **0.9276**. These are previously reported reference-run values, not newly reproduced measurements in this update. Consult the results workbook (pending upload), notebook outputs, and reports for their associated experiment context. This documentation update does not claim that all archived runs share identical metrics or that stacking necessarily outperforms every individual model.

`FYP_AirQuality_Kuching-master.ipynb` is the primary implementation documented here. The `mock` notebook and `etc/` notebooks are retained as supplied research variants, not interchangeable reproductions of the primary run. Bintulu and Miri datasets and models are supporting experiments; `main.py` loads the root `saved_model` artifacts for the Kuching dashboard.

## AQI interpretation

The code maps PM2.5 to AQI using its embedded breakpoint table: the first concentration interval is **0.0–12.0**, followed by **12.1–35.4**. This documents the implementation; it does not assert equivalence to current US EPA guidance or Malaysia's official API calculation. No breakpoint changes were made in this update. See [implementation notes](docs/IMPLEMENTATION_NOTES.md).

## Data, reports, and attribution

The datasets and full reports are included at the author's request. DOE is credited as the data source in the original project documentation. Public availability of this repository does not establish a separate open-data license or transfer third-party rights. No blanket software or dataset license has been assigned in this update; retain source attribution and consult the relevant rights holder before redistribution.

## Repository maintenance

This update restores the uploaded project's working folder paths, adds the dashboard and supporting material, and removes generated training logs and temporary local files from the current tree. Python source, notebooks, datasets, reports, and model bytes are preserved from the supplied archive. No model training, serialized-model execution, or experiment rerun was performed during preparation.
