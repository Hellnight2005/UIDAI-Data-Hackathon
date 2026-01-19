# UIDAI-Data-Hackathon

Data-driven analysis of Aadhaar enrolment and update datasets to uncover operational stress, service gaps, and lifecycle insights for governance decision-making.

## Project Structure

The repository is organized as follows to ensure easy navigation and reproducibility:

```
├── data/
│   ├── raw/             # Raw datasets (CSV files)
│   └── processed/       # Cleaned and processed data files
├── docs/                # Documentation and methodology
├── notebooks/           # Jupyter notebooks for analysis and visualization
├── reports/             # Generated reports and insights
│   └── figures/         # Plots and graphs generated from analysis
└── src/                 # Source code and scripts
    ├── biometric/       # Scripts related to biometric analysis
    ├── enrolment/       # Scripts related to enrolment analysis
    ├── solutions/       # Solution implementations
    └── general/         # General utility and helper scripts
```

## Folder Details

- **data/**: Contains all data used in the project. `raw` contains the original datasets, while `processed` contains data that has been cleaned or transformed.
- **docs/**: Includes detailed documentation about the methodology and other relevant project information.
- **notebooks/**: Jupyter notebooks containing the exploratory data analysis (EDA), model training, and visualization code.
- **reports/**: Final reports, insights, and generated figures.
- **src/**: Python scripts for data processing, analysis, and solution implementation. Organized by module (biometric, enrolment, etc.).

## Getting Started

1.  **Data**: Ensure you have the necessary data in `data/raw/` (or use the provided sample data).
2.  **Notebooks**: Explore the `notebooks/` directory to follow the analysis steps.
3.  **Scripts**: Use the scripts in `src/` for batch processing or specific tasks.
