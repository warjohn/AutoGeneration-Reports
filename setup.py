from setuptools import setup, find_packages

setup(
    name='sklearn_report_generator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "PyYAML",
        "matplotlib",
        "scikit-learn",
        "python-docx",
        "reportlab"
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
        '': ['fonts/*.ttf'],
    },
    include_package_data=True,
)