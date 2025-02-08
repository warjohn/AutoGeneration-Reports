import time
import datetime
import sklearn as sk


from .generatelogs import generateLog
from .LoaderConfig import LoaderConfig
from .calculateMetrics import CalculateMetrics
from .drawgraph import Draw
from .HTML_format import GenerateHtmlReport
from .PDF_format import GeneratePdfReport
from .DOCS_format import GenerateDocsReport

class SklearnReportGenerator(sk.base.BaseEstimator):
    """
    :param
        config_file - yaml configuration file, which contains full pipeline
        output_format - format fot output format

    """
    def __init__(self, config_file, output_format = "HTML"):
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.report_dir = "reports"
        self.testDir = f"{self.report_dir}/test_{self.timestamp}"
        self.config_file = config_file
        self.format = output_format # default - HTML
        self.model = None
        self.metrics = []
        self.pipeline = None
        self._load_config()

        logs = generateLog(self.testDir)
        logs.setLog()

    def _load_config(self):
        loader = LoaderConfig(self.config_file)
        self.pipeline = loader.generateWay()
        self.model = loader.model
        self.metrics = loader.metrics
        self.pictures = loader.pictures

    def fit(self, X, y, X_test=None, y_test=None, *args, **kwargs):
        start_time = time.time()
        self.pipeline.fit(X, y, *args, **kwargs)
        end_time = time.time()
        self.train_time = end_time - start_time

        self.X_train, self.y_train = X, y
        self.X_test, self.y_test = X_test, y_test
        return self

    def predict(self, X):
        y_pred = self.pipeline.predict(X)
        self._generate_report(X, y_pred)
        return y_pred

    def _generate_report(self, X, y_pred):
        report_file = f"{self.testDir}/report_{self.model.__class__.__name__}_{self.timestamp}.html"
        task_type = "classification" if sk.base.is_classifier(self.model) else "regression"

        calculater = CalculateMetrics(self.metrics, task_type)
        metrics_result = calculater.calculate(self.y_test, y_pred)
        draw = Draw(rootdir=self.testDir)

        if "confusion_matrix" in self.pictures and task_type == "classification":
            draw.create_confusion_matrix(self.y_test, y_pred)
        if "roc_curve" in self.pictures and task_type == "classification" and len(set(self.y_test)) == 2:
            draw.create_roc_auc(self.y_test, y_pred)

        if self.format == "HTML":
            GenerateHtmlReport().generateReport(report_file, self.model.__class__.__name__, self.train_time, metrics_result)
        elif self.format == "PDF":
            GeneratePdfReport().generatereport(report_file, self.model.__class__.__name__, self.train_time, metrics_result)
        elif self.format == "DOCS":
            GenerateDocsReport().generateReport(report_file, self.model.__class__.__name__, self.train_time, metrics_result)

