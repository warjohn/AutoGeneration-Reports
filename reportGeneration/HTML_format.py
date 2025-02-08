
class GenerateHtmlReport():

    @classmethod
    def generateReport(cls, report_file, model_name, train_time, result_metrics):
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("<html><head><title>Отчёт о модели</title></head><body>")
            f.write(f"<h1>Отчёт о модели {model_name}</h1>")
            f.write(f"<p><b>Время обучения:</b> {train_time:.4f} секунд</p>")
            f.write("<h2>Метрики:</h2><ul>")
            for key, value in result_metrics.items():
                f.write(f"<li><b>{key}:</b> {value:.4f}</li>")
            f.write("</ul>")
            f.write("</body></html>")