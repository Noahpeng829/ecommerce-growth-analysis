# E-commerce Revenue Growth Analysis

[🇺🇸 English](README.md) | [🇹🇼 繁體中文](README.zh-TW.md)

## Project Overview

This project analyzes transactional, customer, and operational data from an e-commerce platform to identify the key drivers of revenue growth, customer retention, and customer satisfaction.

Using SQL, DuckDB, Python, and Power BI, the project builds an end-to-end analytics workflow that transforms raw business data into actionable insights and executive-level dashboards.

The project demonstrates practical data analytics skills commonly required for Data Analyst, Business Intelligence Analyst, and Product Analyst roles.

## Why This Project Matters

Many e-commerce companies focus heavily on customer acquisition, but sustainable growth depends on customer retention, operational efficiency, and customer experience.

This project demonstrates how business analytics can uncover actionable insights from transactional data and support strategic decision-making through data-driven analysis.

### Analytics Scope

- Data Warehouse Design
- Data Validation Framework
- KPI Development
- Customer Segmentation
- Cohort Retention Analysis
- Revenue Concentration Analysis
- Statistical Hypothesis Testing
- Executive Dashboard Development

---

## Business Problem

The management team wants to understand:

### Revenue Growth

* How has revenue evolved over time?
* Which product categories generate the highest revenue?
* What drives sustainable revenue growth?

### Customer Analytics

* Which customers contribute the most value?
* How concentrated is revenue among customers?
* How effective is customer retention?

### Operational Performance

* How does delivery performance impact customer satisfaction?
* Which product categories present business risks?
* What actions can improve customer experience and retention?

---

## Dataset

### Source

Olist Brazilian E-Commerce Public Dataset

### Scale

- 96K+ completed orders
- 93K+ customers
- 110K+ order items
- 100K+ payment records
- 100+ product categories
- Customer reviews
- Delivery records

### Business Domains

- Revenue Analytics
- Customer Analytics
- Operational Analytics

### Dataset Access

The original dataset is publicly available on Kaggle.

Due to repository size considerations, raw data files are not included in this repository.

Dataset source:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

After downloading the dataset, place the CSV files under:

```text
data/raw/
```

The project pipeline will automatically build the DuckDB database and analytical data model.


---

## Data Architecture

### End-to-End Analytics Workflow

This project follows an end-to-end analytics workflow, starting from raw transactional data and ending with business intelligence dashboards and actionable business recommendations.

![Analytics Workflow](assets/images/end_to_end_workflow.png)

### Star Schema Design

A dimensional star schema was implemented to support scalable analytical queries, KPI calculations, customer analytics, and business intelligence reporting.

The data model consists of:

- Fact Orders
- Fact Order Items
- Fact Payments
- Customer Dimension
- Product Dimension
- Seller Dimension

This structure enables efficient aggregation, customer behavior analysis, and dashboard performance optimization.

The architecture separates transactional facts from descriptive dimensions, enabling scalable business reporting and customer analytics.

![Star Schema](assets/images/star_schema.png)

---

## Demo

### Executive Overview

![Executive Overview](assets/images/executive_overview.png)

### Customer Analytics

![Customer Analytics](assets/images/customer_analytics.png)

### Interactive Dashboard Demo

The GIF below demonstrates dashboard navigation, KPI exploration, customer segmentation analysis, and cohort retention reporting.

![Dashboard Demo](assets/demo/dashboard_demo.gif)

---

## Live Dashboard

Interactive Power BI Dashboard

> Power BI Service deployment is currently in progress.
>
> The dashboard will be published as an interactive web application in a future update.

---

## Project Highlights

- Analyzed 96K+ completed orders and 93K+ customers.
- Identified that 97% of customers purchased only once, highlighting retention as the largest growth opportunity.
- Revealed that the top 20% of customers contributed 53.54% of total revenue.
- Found that delayed deliveries were associated with significantly lower review scores (2.57 vs 4.29).
- Developed RFM customer segmentation to identify high-value customer groups.
- Built a DuckDB-based analytics warehouse using a star schema architecture.
- Implemented data validation workflows to ensure analytical reliability.
- Created a data dictionary to document Power BI datasets and business definitions.
- Built executive-level Power BI dashboards for business stakeholders.

### Key Results

| Metric                       |    Value |
| ---------------------------- | -------: |
| Total Revenue                |  $15.42M |
| Total Orders                 |   96,469 |
| Total Customers              |   93,349 |
| Average Order Value          |  $159.86 |
| Average Review Score         | 4.16 / 5 |
| Delay Rate                   |    8.11% |
| Repeat Customer Rate         |     3.0% |
| Delayed Order Review Score   | 2.57 / 5 |
| On-Time Order Review Score   | 4.29 / 5 |
| Top 20% Revenue Contribution |   53.54% |

---

## Analytics Framework

The project follows a structured analytics workflow:

### 1. Data Modeling

* Build analytical fact and dimension tables
* Design a star schema data warehouse

### 2. Data Validation

* Verify data consistency
* Investigate duplicate records
* Validate cohort calculations

### 3. KPI Development

* Revenue KPI
* Customer KPI
* Delivery KPI
* Customer Satisfaction KPI

### 4. Customer Analytics

* RFM Segmentation
* Cohort Retention Analysis
* Revenue Concentration Analysis
* Customer Value Distribution Analysis

### 5. Business Intelligence

* Executive Dashboard
* Customer Analytics Dashboard

### 6. Business Recommendations

* Translate analytical findings into actionable business strategies

---

## Business Impact

The analysis uncovered three major business opportunities that could directly support revenue growth, customer retention, and customer satisfaction improvement.

### Customer Retention

* 97% of customers purchased only once.
* Only 3% of customers made repeat purchases.
* Retention represents the largest opportunity for sustainable revenue growth.

### Delivery Performance

- Delayed orders received an average review score of 2.57 compared to 4.29 for on-time deliveries.
- Improving logistics performance can directly improve customer satisfaction.

### High-Value Customer Management

* The top 20% of customers contributed 53.54% of revenue.
* CRM and loyalty programs should prioritize high-value customer segments.

---

## Skills Demonstrated

### SQL & Data Warehousing

* DuckDB
* Analytical SQL
* Star Schema Modeling
* Fact & Dimension Design

### Business Analytics

* KPI Design
* Revenue Analysis
* Customer Analytics
* Operational Performance Analysis
* Root Cause Analysis
* Hypothesis-Driven Analysis
* Statistical Hypothesis Testing
* Welch's t-test

### Customer Analytics

* RFM Segmentation
* Cohort Retention Analysis
* Customer Value Analysis
* Revenue Concentration Analysis

### Business Intelligence

* Power BI
* Dashboard Design
* Executive Reporting
* Data Storytelling

### Data Engineering

* ETL Workflow
* Data Validation
* Data Quality Investigation
* Data Dictionary Documentation
* Reproducible Analytics Pipeline

---

## Key SQL Techniques

The project heavily relies on analytical SQL to transform raw transactional data into business-ready datasets.

Key techniques include:

- Multi-table joins across customers, orders, products, reviews, and payments
- Common Table Expressions (CTEs) for modular query design
- Window functions for customer ranking and revenue distribution analysis
- Cohort table construction for retention analysis
- Revenue KPI calculations and aggregation
- RFM customer segmentation logic
- Data validation and duplicate record investigation
- Power BI dataset preparation and export

These SQL workflows were used to support customer analytics, revenue analysis, operational performance monitoring, and executive dashboard reporting.

---

## Deliverables

The project produces the following analytical outputs:

- Executive KPI Summary
- Revenue Analysis Tables
- Customer Segmentation Outputs
- Cohort Retention Tables
- Customer Value Distribution Analysis
- Statistical Hypothesis Testing Results
- Power BI Reporting Datasets
- Data Dictionary Documentation
- Executive and Customer Analytics Dashboards

---

## Repository Features

This repository is designed as a reproducible analytics project.

Key features include:

* Automated database creation using DuckDB
* Star schema analytical data model
* Data quality validation framework
* KPI calculation pipelines
* Customer analytics workflows
* Statistical hypothesis testing
* Power BI dataset generation
* Data dictionary documentation
* Modular Python analytics scripts
* Version-controlled analytics workflow

The entire analysis can be reproduced from raw data ingestion through dashboard generation using the provided scripts.

---


## Technology Stack

### Programming

* Python
* SQL

### Data Processing & Analytics

* Pandas
* NumPy
* SciPy

### Data Warehouse

* DuckDB (Embedded Analytical Database)

### Business Intelligence

* Power BI

### Data Validation

* SQL Validation Scripts
* Data Quality Investigation

### Version Control

* Git
* GitHub

---

## Dashboard Overview

### Executive Overview

The executive dashboard provides a high-level view of business performance, including:

* Revenue KPI
* Orders KPI
* Customer KPI
* Average Order Value (AOV)
* Review Score
* Delay Rate
* Revenue Trends
* Product Category Performance
* Category Risk Analysis

### Customer Analytics

The customer dashboard focuses on customer behavior and value:

* Customer Segment Distribution
* Revenue Contribution by Segment
* Revenue Distribution
* Cohort Retention Analysis
* Customer Value Insights

---

## Key Business Insights

### Revenue Growth

Revenue exceeded $1M per month during 2018, indicating strong platform growth and increasing customer adoption.

### Category Performance

Health & Beauty generated the highest revenue among all product categories.

Several high-revenue categories exhibited below-average review scores, suggesting potential customer experience and product quality risks.

### Customer Concentration

The top 20% of customers contributed approximately 53.54% of total revenue, indicating a moderate concentration of customer value.

### Customer Retention

97% of customers purchased only once, highlighting retention as the largest growth opportunity identified in this analysis.

### Delivery Performance

Delayed orders received significantly lower review scores than on-time deliveries, indicating a strong relationship between logistics performance and customer satisfaction.

---

## Analytics Results

The analysis produced several business-ready outputs that can support executive decision-making:

| Output                  | Description                                                          |
| ----------------------- | -------------------------------------------------------------------- |
| Executive KPI Summary   | Revenue, Orders, Customers, AOV, Review Score, Delay Rate            |
| Revenue Analysis        | Monthly revenue trends and state-level revenue performance           |
| Customer Segmentation   | RFM customer segmentation and revenue contribution analysis          |
| Cohort Analysis         | Customer retention trends across acquisition cohorts                 |
| Customer Value Analysis | Customer lifetime value and revenue concentration analysis           |
| Statistical Validation  | Hypothesis testing on delivery performance and customer satisfaction |
| Executive Insights      | Actionable business recommendations for growth and retention         |

These outputs were exported as reusable analytical datasets and integrated into Power BI dashboards for stakeholder reporting.


---

## Future Improvements

### Advanced Analytics

* Customer Churn Prediction
* Predictive Customer Lifetime Value Modeling
* Demand Forecasting
* Marketing Attribution Analysis

### Data Engineering

* Automated ETL Pipeline
* Cloud Data Warehouse Deployment

### Business Intelligence

* Power BI Service Deployment
* Interactive Online Dashboard

### Analytics Automation

* Scheduled Data Refresh
* Automated Reporting Workflow

---

## Project Structure

```text
ecommerce-growth-analysis/
│
├── assets/
│   ├── demo/
│   └── images/
│
├── dashboard/
│   └── ecommerce_revenue_growth_dashboard.pbix
│
├── data/
├── database/
├── outputs/
├── sql/
│
├── src/
│   ├── 01_create_database.py
│   ├── ...
│   ├── 22_segment_revenue_analysis.py
│   │
│   └── validation/
│       ├── validate_cohort_logic.py
│       ├── validate_fact_tables.py
│       ├── investigate_order_duplication.py
│       └── investigate_review_duplication.py
│
├── README.md
├── README.zh-TW.md
└── requirements.txt
```

---

## Usage

### Step 1: Build Database and Data Model

```bash
python src/01_create_database.py
python src/02_data_quality_check.py
python src/03_create_master_table.py
python src/04_create_star_schema.py
```

### Step 2: Validate KPIs and Revenue Logic

```bash
python src/05_kpi_validation.py
python src/06_revenue_analysis.py
python src/07_state_revenue_analysis.py
python src/08_revenue_validation.py
```

### Step 3: Analyze Product, Review, and Delivery Performance

```bash
python src/09_category_revenue_analysis.py
python src/10_category_review_analysis.py
python src/11_delivery_review_analysis.py
python src/12_category_delay_analysis.py
python src/13_category_delay_rate_analysis.py
python src/14_hypothesis_testing.py
```

### Step 4: Run Customer Analytics

```bash
python src/15_rfm_segmentation.py
python src/16_cohort_analysis.py
python src/17_clv_analysis.py
python src/18_customer_value_distribution.py
python src/22_segment_revenue_analysis.py
```

> Note:
> `17_clv_analysis.py` calculates historical customer value based on total customer revenue.
> Predictive CLV modeling is listed as a future improvement.

### Step 5: Generate Executive and Power BI Outputs

```bash
python src/19_executive_summary_tables.py
python src/20_export_powerbi_dataset.py
python src/21_create_data_dictionary.py
```

### Step 6: Run Validation Scripts

```bash
python src/validation/validate_cohort_logic.py
python src/validation/validate_fact_tables.py
python src/validation/investigate_order_duplication.py
python src/validation/investigate_review_duplication.py
```

### Step 7: Open Power BI Dashboard

Open the Power BI dashboard file:

```text
dashboard/ecommerce_revenue_growth_dashboard.pbix
```

Dashboard pages:

* Executive Overview
* Customer Analytics

---

## External Links

### GitHub Repository

https://github.com/Noahpeng829/ecommerce-growth-analysis

### Power BI Dashboard

Power BI Service deployment is currently in progress.

### LinkedIn

https://www.linkedin.com/in/noah-peng-7896b9374/

---

## Author

Noah Peng

Data Analyst | SQL | Python | Power BI | Customer Analytics | Business Intelligence

National Taipei University

Current Role

Data Analyst

Supporting Taiwan Power Research Institute Projects


GitHub: https://github.com/Noahpeng829

LinkedIn: https://www.linkedin.com/in/noah-peng-7896b9374/

