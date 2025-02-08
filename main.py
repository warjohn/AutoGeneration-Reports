from reportGeneration.reportGeneration import SklearnReportGenerator

if __name__ == "__main__":
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    data = load_iris()
    X = data.data
    y = data.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    report_generator = SklearnReportGenerator(config_file='config.yaml', output_format="PDF")
    report_generator.fit(X_train, y_train, X_test, y_test)
    report_generator.predict(X_test)
