# 🚖 Uber Fare Prediction using Machine Learning

## 📌 Project Overview

This project predicts the fare of an Uber ride based on trip details such as pickup location, drop-off location, passenger count, date, and time. Two machine learning algorithms—**Linear Regression** and **Random Forest Regression**—are implemented and compared to determine the best-performing model.

---

## 🎯 Objective

The main objectives of this project are to:

- Preprocess the Uber Fare dataset.
- Detect and remove outliers.
- Perform correlation analysis.
- Train Linear Regression and Random Forest Regression models.
- Evaluate and compare model performance using R² Score, RMSE, and MAE.

---

## 📂 Dataset

- **Dataset:** Uber Fares Dataset
- **Source:** https://www.kaggle.com/datasets/yasserh/uber-fares-dataset

---

## 🛠️ Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

---

## 📋 Project Workflow

1. Import Libraries
2. Load Dataset & Exploratory Data Analysis (EDA)
3. Data Preprocessing
4. Feature Engineering (Haversine Distance)
5. Outlier Detection using IQR
6. Correlation Analysis
7. Train-Test Split
8. Linear Regression
9. Random Forest Regression
10. Model Evaluation & Comparison

---

## 📊 Evaluation Metrics

The models are evaluated using:

- **R² Score**
- **RMSE (Root Mean Squared Error)**
- **MAE (Mean Absolute Error)**

---

## 📈 Results

Both models were trained and evaluated on the processed dataset.

The comparison showed that **Random Forest Regression** outperformed **Linear Regression**, achieving a higher R² Score and lower RMSE and MAE, making it the better model for predicting Uber fares.

---

## 📁 Project Structure

```
Uber-Fare-Prediction/
│
├── data/
│   └── uber.csv
│
├── Uber_Fare_Prediction.ipynb
├── README.md
├── requirements.txt
└── .gitignore
```

---

## ▶️ How to Run

1. Clone this repository.

```bash
git clone https://github.com/your-username/Uber-Fare-Prediction.git
```

2. Install the required libraries.

```bash
pip install -r requirements.txt
```

3. Open the Jupyter Notebook.

```bash
jupyter notebook
```

4. Run all cells in **Uber_Fare_Prediction.ipynb**.

---

## 👨‍💻 Author

**Harsh Gopinath Chavan**

GitHub: https://github.com/harsh8767
