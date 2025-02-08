from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


class GeneratePdfReport():
    pdfmetrics.registerFont(TTFont('TimesNewRoman', '../fonts/Times_New_Roman.ttf'))

    @classmethod
    def generatereport(cls, report_file, model_name, train_time, result_metrics):
        pdf_file = report_file.replace(".html", ".pdf")
        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.setFont("TimesNewRoman", 12)
        c.drawString(100, 750, f"Отчёт о модели {model_name}")
        c.drawString(100, 730, f"Время обучения: {train_time:.4f} секунд")
        c.drawString(100, 710, "Метрики:")
        y_position = 690
        for key, value in result_metrics.items():
            c.drawString(100, y_position, f"{key}: {value:.4f}")
            y_position -= 20
        c.save()