# ⛷️ Ski Resort Snowfall Analysis  
A Python package for cleaning, exploring, and analyzing ski resort snowfall data. This project follows the full data-science pipeline: data collection, cleaning/wrangling, exploratory data analysis (EDA), and documentation.

Here is the link to our website containing the Technical Report, Tutorial, and Documentation: https://ella-walker.github.io/weather_api_project/

## Features
- **Data Cleaning**: Functions to clean and preprocess snowfall data.
- **Exploratory Data Analysis**: Tools to visualize and analyze snowfall trends.
- **Documentation**: Comprehensive documentation to guide users through the package functionalities.
- **Testing**: Unit tests to ensure code reliability and correctness.
- **Version Control**: Managed with Git for efficient collaboration and version tracking.

## Installation
To install the package, clone the repository and run:
```bash
pip install -e .
```

## Usage
Import the package in your Python scripts and use the provided functions for data cleaning and analysis:
```python
from weather_package.analysis import add, run_analysis_pipeline

df_clean = run_cleaning_pipeline(
    url="https://en.wikipedia.org/wiki/List_of_ski_areas_and_resorts_in_the_United_States",
    email="your_email@byu.edu"
)

from weather_package.cleaning import run_cleaning_pipeline

run_analysis_pipeline(df_clean)
```
