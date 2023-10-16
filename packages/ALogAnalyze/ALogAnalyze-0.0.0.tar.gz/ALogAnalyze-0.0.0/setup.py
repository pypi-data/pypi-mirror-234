import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ALogAnalyze",
    version="0.0.0",
    author="zengjf",
    author_email="zengjf42@163.com",
    description="Android Log Analyze",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.0",
    install_requires=[
        'VisualLog>=0.0.15',
        'PyQt5'
    ],
    include_package_data=True,
    entry_points={"console_scripts": ["aloganalyze=ALogAnalyze:main"]},
)
