from setuptools import setup, find_packages

setup(
    name='sklearn_report_generator',
    version='0.2.3',
    packages=find_packages(),
    install_requires=[
        "uvicorn",
        "fastapi",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "reportlab",
        "python-docx",
        "PyYAML",
        "setuptools",
        "starlette",
        'jinja2',
        'python-multipart'
    ],
    author='Menar',
    author_email='johnvoroninA@gmail.com',
    description='Autogeneration reports for sklearn',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/warjohn/AutoGeneration-Reports.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_data={
        'reportGeneration': ['fonts/*.ttf'],
        'reportGeneration.styles': ['web/static/*.css'],
        'reportGeneration.web': ['web/templates/*.html'],
        'reportGeneration.database': ['database/*']
    },
    include_package_data=True,
)