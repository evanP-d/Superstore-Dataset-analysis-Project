# Superstore Business Data Analysis

Comprehensive business analysis based on the Sample - Superstore dataset (2014–2017), covering sales trends, product structure, customer value, geographic markets, and logistics. Delivered through Python analysis reports and Tableau dashboards.

## Project Structure

```
.
├── main.ipynb                                 # Core analysis notebook (6 modules)
├── datasets/                                   # Exported analysis datasets (11 Excel files)
│   ├── Sample - Superstore.xlsx                # Main dataset (with derived fields)
│   ├── Sample - Superstore.csv                 # Original CSV dataset
│   ├── yearly_kpi.xlsx                         # Annual KPI summary
│   ├── monthly_sales.xlsx                      # Monthly sales aggregation
│   ├── subcategory_stats.xlsx                  # Sub-Category performance data
│   ├── region_stats.xlsx                       # Regional performance summary
│   ├── state_stats.xlsx                        # State-level performance data
│   ├── rfm.xlsx                                # RFM customer segmentation data
│   ├── segment_summary.xlsx                    # Customer segment summary
│   ├── shipping_stats.xlsx                     # Shipping mode analysis
│   └── discount_impact.xlsx                    # Discount impact analysis
├── images/                                     # Chart images (14 PNGs)
│   ├── save_charts.py                          # Chart generation script
│   ├── 01_yearly_trends.png                    # Yearly KPI trends
│   ├── 02_distribution.png                     # Data distribution overview
│   ├── 03_monthly_trends.png                   # Monthly sales & profit trends
│   ├── 04_seasonality.png                      # Seasonality analysis
│   ├── 05_product_analysis.png                 # Product structure & profitability
│   ├── 06_discount_impact.png                  # Discount strategy impact
│   ├── 07_cross_selling.png                    # Category co-occurrence matrix
│   ├── 08_customer_profile.png                 # Customer profile overview
│   ├── 09_rfm_analysis.png                     # RFM customer segmentation
│   ├── 10_geo_analysis.png                     # Geographic market analysis
│   ├── 11_shipping_analysis.png                # Shipping & logistics analysis
│   ├── 12_correlation.png                      # Correlation & profit attribution
│   ├── 13_profit_waterfall.png                 # Profit waterfall chart
│   └── 14_product_matrix.png                   # Product matrix (bubble chart)
├── reports/                                    # Report output
│   └── analysis_report.pdf                     # Analysis report
├── tableau_report/                             # Tableau dashboard & screenshots
│   ├── Superstore_analysis_dashboard.twb       # Tableau workbook
│   ├── Overview.png                            # Overview dashboard screenshot
│   ├── Sales.png                               # Sales dashboard screenshot
│   ├── Products.png                            # Products dashboard screenshot
│   └── Backgrounds/                            # Dashboard background images
├── README.md                                   # Chinese README
└── README.en.md                                # This file
```
  
## Analysis Modules

| Module | Content |
|--------|---------|
| **Module 1** Data Prep & Overview | Data cleaning, time dimension derivation, core KPI dashboard, yearly trends, data distribution |
| **Module 2** Sales Trends & Time Series | Monthly trends (12-month MA), seasonality, annual heatmap, cumulative curves, growth decomposition |
| **Module 3** Product Structure & Profit | Category/Sub-Category drill-down, Pareto analysis, product matrix, discount impact, cross-selling |
| **Module 4** Customer Value & RFM | Customer profile, RFM model, 9-tier segmentation, CLV estimation |
| **Module 5** Geography & Logistics | Regional comparison, state-level top/bottom, region×category cross analysis, shipping efficiency |
| **Module 6** Insights & Recommendations | Correlation matrix, profit attribution, strategic recommendations, monitoring KPIs |


## Tableau Dashboard

`tableau_report/Superstore_analysis_dashboard.twb` is the companion Tableau workbook. Based on **full-year 2017 data**, it provides simple BI visualizations across three perspectives:

| Dashboard | Description |
|-----------|-------------|
| **Overview-annual** | KPI cards, monthly trend sparklines, regional/category/segment distribution |
| **Sales-annual** | Sales rankings, high-sales-low-profit items, discount effect analysis |
| **Products-annual** | Product treemap, top/tail ranking, discount-profitability correlation |

## Requirements

- Python 3.10+
- Conda environment: `data_ana_project_env`

### Core Dependencies

```
pandas  numpy  matplotlib  seaborn  plotly  scipy  openpyxl  kaleido
```

## Quick Start

```bash
# Activate environment
conda activate data_ana_project_env

# Launch Jupyter Notebook
jupyter notebook main.ipynb

# Generate analysis report
```

## Dataset

Source: Tableau Sample - Superstore, containing US retail order data from 2014–2017 (9,994 transactions, 793 customers, 1,862 products).

Key fields: Order ID, Order Date, Ship Date, Sales, Profit, Quantity, Discount, Category, Sub-Category, Segment, Region, State, City, Ship Mode, etc.

During analysis, `main.ipynb` derives additional fields (shipping days, profit margin, loss flag, discount band, etc.) and auto-exports aggregated results to the `datasets/` directory.
