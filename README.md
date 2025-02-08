# Sklearn Report Generator

This Python library helps generate detailed reports for scikit-learn models. It can create reports in various formats such as HTML, PDF, and DOCX. The library supports model training, metric evaluation, and report generation for both classification and regression tasks.

## Installation

To install the library, use `pip`:

```bash
  pip install sklearn_report_generator
```

## Usage

After installation, you can use the SklearnReportGenerator to train a model, generate predictions, and create reports.

### Example
```commandline
from utils.reportGeneration import SklearnReportGenerator

if __name__ == "__main__":
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    data = load_iris()
    X = data.data
    y = data.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    report_generator = SklearnReportGenerator(config_file='/your-file-path/config.yaml', output_format="PDF")
    report_generator.fit(X_train, y_train, X_test, y_test)
    report_generator.predict(X_test)
```

## Configuration Example

The configuration file (config.yaml) defines the transformers, model, selection parameters (optional), and metrics to be used in the report generation.
```commandline
transformers:
  - name: StandardScaler
    params: {}
  - name: OneHotEncoder
    params:
      handle_unknown: ignore
model:
  name: KNeighborsClassifier
  params:
    weights: 'distance'
    algorithm: 'ball_tree'
    leaf_size: 1
selectionParams:
  enable: True
  name: GridSearchCV
  params:
    cv: 5
    verbose: 3
    n_jobs: 20
  param_grid:
    KNeighborsClassifier__leaf_size: [1, 2, 20]
metrics:
  - name: accuracy_score
    params: {}
  - name: precision_score
    params:
      average: weighted
      zero_division: 0
```

## Configuration Breakdown

1. transformers: List of data preprocessing steps. Examples include StandardScaler and OneHotEncoder. Parameters can be customized for each transformer.
2. model: Defines the model to be used (e.g., KNeighborsClassifier) and its hyperparameters.
3. selectionParams: Optional grid search (or other selection models) for hyperparameter tuning. GridSearchCV is enabled in this example with cross-validation (cv), verbosity, and parallelization (n_jobs).
4. metrics: List of metrics used to evaluate the model's performance. For example, accuracy_score and precision_score.

## Report Generation

Once the model is trained, a report will be generated in the specified format. The available formats are:

    HTML: Generates an HTML report with metrics and graphs.
    PDF: Generates a PDF report with metrics and graphs.
    DOCX: Generates a DOCX report with metrics and graphs.

The report will be saved in a directory named reports, with a timestamp in the file name to ensure uniqueness.

## Example Report Output

The report includes:

- Training time
- Model metrics (e.g., accuracy, precision)
- Visualizations such as confusion matrix (for classification tasks) - _there may be bugs in development_
- ROC curve (for binary classification tasks) - _there may be bugs in development_

#### _This version of the library is in testing and will be developed and improved in the future. In subsequent versions it is planned to add new functions, improve data processing and expand reporting capabilities_
