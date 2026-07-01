# Price Predictions Using ML Models

## Overview
This project uses machine learning models to predict prices based on historical data and various features. It implements multiple algorithms to provide accurate price forecasting for better decision-making.

## Features
- Data preprocessing and feature engineering
- Multiple ML model implementations (Linear Regression, Random Forest, XGBoost, etc.)
- Model evaluation and comparison
- Price prediction on new data
- Visualization of predictions vs actual values

## Requirements
```
python>=3.8
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
xgboost>=1.5.0
matplotlib>=3.4.0
seaborn>=0.11.0
```

## Installation
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure
```
.
├── data/
│   ├── train_data.csv
│   └── test_data.csv
├── models/
│   ├── train_models.py
│   ├── predict.py
│   └── evaluate.py
├── notebooks/
│   └── analysis.ipynb
├── utils/
│   ├── preprocessing.py
│   └── visualization.py
├── requirements.txt
└── README.md
```

## Usage

### Training Models
```python
python models/train_models.py --data data/train_data.csv
```

### Making Predictions
```python
python models/predict.py --model models/best_model.pkl --input data/test_data.csv
```

### Model Evaluation
```python
python models/evaluate.py --model models/best_model.pkl --test_data data/test_data.csv
```

## Models Implemented
- **Linear Regression**: Baseline model for linear relationships
- **Random Forest**: Ensemble method for non-linear patterns
- **XGBoost**: Gradient boosting for improved accuracy
- **Support Vector Regression**: For complex feature relationships

## Results
The models are evaluated using:
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score

## Author
Rakesh

## License
MIT License
