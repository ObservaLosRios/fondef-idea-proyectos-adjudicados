# Fondef Project Analysis ETL

## Overview
This project implements a robust ETL (Extract, Transform, Load) pipeline to process Fondef project data. It follows SOLID principles and Clean Code practices to ensure maintainability and scalability.

## Project Structure
```
.
├── data/
│   ├── raw/            # Original datasets
│   └── processed/      # Cleaned and transformed data
├── docs/               # Documentation
├── notebooks/          # Jupyter notebooks for exploration
├── src/                # Source code
│   ├── extract.py      # Data extraction logic
│   ├── transform.py    # Data transformation logic
│   ├── load.py         # Data loading logic
│   ├── pipeline.py     # ETL orchestration
│   └── interfaces.py   # Abstract base classes
├── main.py             # Entry point
└── requirements.txt    # Project dependencies
```

## Setup
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the ETL pipeline:
```bash
python main.py
```

## Data Analysis & Visualization
The project includes a comprehensive analysis of the processed data:

### Notebooks
- `notebooks/basic_analysis.ipynb`: Contains exploratory data analysis (EDA) using Pandas and Plotly.

### Web Dashboard
A interactive dashboard is available in the `docs/` folder. It visualizes key metrics such as:
- Evolution of projects per year.
- Budget distribution by area.
- Evolution of amounts by area.
- Top 5 areas by number of projects.

To view the dashboard locally, open `docs/index.html` in your web browser.

## Architecture
The project uses a modular architecture based on interfaces:
- **IDataSource**: Abstraction for reading data.
- **IDataTransformer**: Abstraction for processing data.
- **IDataLoader**: Abstraction for saving data.

This allows easy extension (e.g., adding new data sources or transformation steps) without modifying existing code (Open/Closed Principle).
