# Implementation and reproducibility notes

## Preserved behavior

- The app reads saved artifacts using joblib. Dependency minimums do not guarantee compatibility with the environment in which the artifacts were trained.
- Input cleaning converts zero pollutant values to missing values. Predictor missing values are filled using means from the uploaded batch; missing PM2.5 rows are removed.
- Lag columns are constructed only if requested by the stored feature names. The current notebook and older experiments should be reviewed separately.
- The loader suppresses model/comparison exceptions. Investigate the original exception in a development environment if predictions are unavailable.
- `python main.py` enables Flask debug mode. The README uses `python -m flask --app main run` for a local run without that option. Public deployment needs a production serving configuration.
- The AQI table and rounding logic are preserved from the uploaded code. The code labels them EPA breakpoints, but no current regulatory equivalence is asserted here.

## Research variants

The main notebook uses an XGBoost meta-learner. The `mock` notebook imports RidgeCV and contains a different experimental configuration; do not combine results from these variants without identifying the run.

The main notebook performs chronological train/test splits, but stacking uses ordinary KFold internally. The sensitivity experiment reuses selected features and tuned parameters rather than independently rerunning optimization for each split. Its results should be interpreted with those choices in mind.

## Included files

All supplied datasets, report PDFs, notebooks, figures, model artifacts, and result workbooks are included. Training logs (`catboost_info`), Python caches, local assistant settings, and temporary Excel lock files are excluded. The root-level duplicate Kuching data and model files from the previous repository are relocated into the paths used by the application and notebook.

The original `requirements-1.txt` is retained. `requirements.txt` provides the same dashboard dependencies; `requirements-training.txt` adds notebook and optimization dependencies. No exact environment lock was available, so none was invented.
