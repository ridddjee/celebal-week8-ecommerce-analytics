# 🛒 E-Commerce Order Analytics System

> **Celebal Technologies – Week 8 Final Project**

An end-to-end **E-Commerce Order Analytics System** built using **Python, Pandas, SQLite, and SQL**. The project demonstrates data generation, data cleaning, database design, SQL analytics, and command-line reporting.

---

# 📌 Project Overview

Online businesses generate thousands of orders every day. Raw order data often contains:

- Missing values
- Invalid emails
- Incorrect date formats
- Duplicate or inconsistent records
- Broken relationships between tables

This project builds a complete ETL pipeline to clean and analyze e-commerce data and generate business insights.

---

# 🚀 Features

## Data Generation
- Generate realistic fake data using Faker
- 1000+ Customers
- 500+ Products
- 5000+ Orders
- Multiple Order Items

Intentional inconsistencies:
- Missing Customer IDs
- Invalid Emails
- Mixed Date Formats
- Negative Quantities (Returns)
- Mixed Case Product Names

---

## Data Cleaning

- Fix invalid dates
- Handle missing values
- Normalize product names
- Validate emails
- Check referential integrity
- Export cleaned datasets

---

## Database

SQLite database with:

- Primary Keys
- Foreign Keys
- CHECK Constraints
- Indexes

---

## SQL Analytics

Includes:

- Revenue Analysis
- Top Customers
- Monthly Trends
- Return Analysis
- Running Totals
- DENSE_RANK()
- LAG()
- CTEs
- NTILE()
- Cohort Analysis
- Product Pair Analysis

---

## Command Line Reporting

Interactive CLI that generates:

- Daily Report
- Weekly Report
- Monthly Report

Displays:

- Total Orders
- Revenue
- Unique Customers
- Top Products
- Previous Period Comparison

---

## Edge Case Testing

Validates:

- Invalid Order References
- Discount > 100
- Quantity = 0
- Future Order Dates

---

# 📂 Project Structure

```text
ecommerce-analytics-system/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── database/
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

# ⚙️ Technologies Used

- Python 3.x
- Pandas
- Faker
- SQLite
- SQL
- VS Code

---

# 📊 Database Schema

Tables:

- customers
- products
- orders
- order_items

Relationships:

```
Customers
    |
    |
Orders
    |
    |
Order Items
    |
    |
Products
```

---

# ▶️ How to Run

## 1. Clone Repository

```bash
git clone <repository-url>
cd ecommerce-analytics-system
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Generate Data

```bash
python scripts/generate_data.py
```

## 4. Clean Data

```bash
python scripts/clean_data.py
```

## 5. Load SQLite Database

```bash
python scripts/load_database.py
```

## 6. Execute SQL Queries

Run SQL files in SQLite:

- aggregations.sql
- window_functions.sql
- cohort_analysis.sql

## 7. Generate Reports

```bash
python scripts/report_cli.py
```

## 8. Execute Test Cases

```bash
python scripts/test_cases.py
```

---

# 📈 Business Insights

The project helps answer questions like:

- Which category generates the most revenue?
- Who are the top customers?
- Which products are frequently purchased together?
- What is the customer retention rate?
- Which customers are at risk?
- Which categories have the highest return rate?

---

# 🎯 Learning Outcomes

- ETL Pipeline
- Data Cleaning
- SQL Analytics
- Window Functions
- CTEs
- Cohort Analysis
- Customer Segmentation
- SQLite Database Design
- Python Automation

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Ridam Agrawal**

B.Tech (Computer Science)

Celebal Technologies Data Engineering Internship

2026