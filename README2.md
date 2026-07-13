# 🛒 E-Commerce Order Analytics System

> Celebal Technologies – Week 8 Final Project

## 📌 Project Overview

This project simulates a real-world E-Commerce Analytics pipeline using Python, Pandas, SQLite, SQL, and Faker.

The system generates realistic e-commerce datasets, cleans and validates the data, loads it into SQLite, and performs advanced SQL analytics including:

- SQL Joins
- Aggregations
- Window Functions
- Common Table Expressions (CTEs)
- Cohort Analysis
- Customer Segmentation (RFM)
- Automated Test Cases

The project is modular, scalable, and follows industry-standard data engineering practices.

---

# 📂 Project Structure

```
ecommerce-analytics-system/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── database/
│   └── ecommerce.db
│
├── output/
│   └── sample_reports/
│
├── scripts/
│   ├── generate_data.py
│   ├── clean_data.py
│   ├── load_database.py
│   ├── report_cli.py
│   └── test_cases.py
│
├── sql/
│   ├── schema.sql
│   ├── aggregations.sql
│   ├── window_functions.sql
│   └── cohort_analysis.sql
│
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

---

# 🚀 Features

- Generate realistic datasets using Faker
- Introduce inconsistent records
- Clean datasets using Pandas
- Validate data quality
- Export cleaned CSV files
- SQLite relational database
- Primary & Foreign Keys
- SQL Aggregations
- SQL Window Functions
- Common Table Expressions
- Cohort Analysis
- Customer Segmentation (RFM)
- Automated Test Cases
- GitHub Ready

---

# 🛠 Technologies Used

- Python 3.x
- Pandas
- Faker
- SQLite
- SQL
- VS Code

---

# 📊 Dataset

Generated datasets:

| Dataset | Records |
|----------|---------|
| Customers | 1000 |
| Products | 500 |
| Orders | 5000 |
| Order Items | 18000+ |

---

# ▶️ How to Run

### Install dependencies

```bash
pip install -r requirements.txt
```

### Generate raw data

```bash
python scripts/generate_data.py
```

### Clean data

```bash
python scripts/clean_data.py
```

### Load SQLite Database

```bash
python scripts/load_database.py
```

### Run Test Cases

```bash
python scripts/test_cases.py
```

---

# 📈 SQL Analytics

Implemented SQL concepts:

- INNER JOIN
- GROUP BY
- Aggregate Functions
- Window Functions
- RANK()
- DENSE_RANK()
- ROW_NUMBER()
- NTILE()
- LAG()
- LEAD()
- Running Total
- Moving Average
- CTE
- Cohort Analysis
- Customer Segmentation

---

# 🧪 Testing

Implemented automated validation for:

- Database existence
- Duplicate Primary Keys
- Foreign Keys
- Discount validation
- Price validation
- Dataset validation

---

# 📷 Sample Workflow

```
Generate Data
        │
        ▼
Clean Data
        │
        ▼
SQLite Database
        │
        ▼
SQL Analytics
        │
        ▼
Reports
```

---

# 📚 Learning Outcomes

- Data Cleaning
- Data Validation
- Relational Database Design
- SQL Analytics
- Window Functions
- Cohort Analysis
- RFM Analysis
- Data Engineering Workflow

---

# 👨‍💻 Author

**Ridam Agrawal**

Celebal Technologies Data Engineering Internship

Week 8 Final Project


---
