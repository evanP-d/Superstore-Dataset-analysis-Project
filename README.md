# Superstore 商业数据分析项目

基于 Sample - Superstore 数据集（2014–2017）的全方位业务分析，涵盖销售趋势、产品结构、客户价值、地理市场与物流等维度，输出 Python 分析报告与 Tableau 仪表板。

## 项目结构

```
.
├── main.ipynb                                 # 核心分析 Notebook（6 大模块）
├── datasets/                                   # 分析数据集导出（11 个 Excel）
│   ├── Sample - Superstore.xlsx                # 主数据集（含派生字段）
│   ├── Sample - Superstore.csv                 # 原始 CSV 数据集
│   ├── yearly_kpi.xlsx                         # 年度 KPI 汇总
│   ├── monthly_sales.xlsx                      # 月度销售额聚合
│   ├── subcategory_stats.xlsx                  # Sub-Category 产品绩效
│   ├── region_stats.xlsx                       # 区域绩效汇总
│   ├── state_stats.xlsx                        # 州级绩效数据
│   ├── rfm.xlsx                                # RFM 客户分层数据
│   ├── segment_summary.xlsx                    # 客户分层汇总
│   ├── shipping_stats.xlsx                     # 物流配送模式分析
│   └── discount_impact.xlsx                    # 折扣影响分析
├── images/                                     # 可视化图表（14 张 PNG）
│   ├── save_charts.py                          # 图表生成脚本
│   ├── 01_yearly_trends.png                    # 年度趋势概览
│   ├── 02_distribution.png                     # 数据分布概况
│   ├── 03_monthly_trends.png                   # 月度销售与利润趋势
│   ├── 04_seasonality.png                      # 季节性分析
│   ├── 05_product_analysis.png                 # 产品结构与盈利分析
│   ├── 06_discount_impact.png                  # 折扣策略影响分析
│   ├── 07_cross_selling.png                    # 品类共现矩阵
│   ├── 08_customer_profile.png                 # 客户整体画像
│   ├── 09_rfm_analysis.png                     # RFM 客户细分分析
│   ├── 10_geo_analysis.png                     # 地理市场与区域分析
│   ├── 11_shipping_analysis.png                # 物流配送与时效分析
│   ├── 12_correlation.png                      # 相关性分析与利润归因
│   ├── 13_profit_waterfall.png                 # 利润瀑布图
│   └── 14_product_matrix.png                   # 产品矩阵（气泡图）
├── reports/                                    # 分析报告输出
│   └── analysis_report.pdf                     # 分析报告
├── tableau_report/                             # Tableau 仪表板及截图
│   ├── Superstore_analysis_dashboard.twb       # Tableau 工作簿
│   ├── Overview.png                            # 概览仪表板截图
│   ├── Sales.png                               # 销售仪表板截图
│   ├── Products.png                            # 产品仪表板截图
│   └── Backgrounds/                            # 仪表板背景素材
├── README.md                                   # 本文件（中文）
└── README.en.md                                # English version
```
  
## 分析模块

| 模块 | 内容 |
|------|------|
| **模块 1** 数据准备与概览 | 数据清洗、时间维度派生、核心 KPI 仪表盘、年度趋势、数据分布 |
| **模块 2** 销售趋势与时间序列 | 月度趋势（12 月移动平均）、季节性分析、年度热力图、累计曲线、增长因子分解 |
| **模块 3** 产品结构与利润 | Category/Sub-Category 钻取、帕累托分析、产品矩阵、折扣影响、交叉销售 |
| **模块 4** 客户价值与 RFM | 客户画像、RFM 模型构建、9 层客户分层、CLV 估算 |
| **模块 5** 地理市场与物流 | 区域对比、州级 Top/Bottom、区域×品类交叉、物流配送模式与时效 |
| **模块 6** 综合洞察与建议 | 相关性矩阵、利润归因、战略建议、监控指标体系 |


## Tableau 仪表板

`tableau_report/Superstore_analysis_dashboard.twb` 为本项目配套的 Tableau 交互式报表文件，以 **2017 全年数据** 为基准做了简单的 BI 可视化展示：

| 仪表板 | 说明 |
|--------|------|
| **Overview-annual** | 年度概览 — KPI 指标卡、月度趋势迷你图、区域/品类/客户细分分布 |
| **Sales-annual** | 销售年度分析 — 销售额排名、高销低利商品、折扣效果分析 |
| **Products-annual** | 产品年度分析 — 产品树形图、Top/Tail 销售、折扣利润率关联 |

## 环境要求

- Python 3.10+
- Conda 环境：`data_ana_project_env`

### 核心依赖

```
pandas  numpy  matplotlib  seaborn  plotly  scipy  openpyxl  kaleido
```

## 快速开始

```bash
# 激活环境
conda activate data_ana_project_env

# 运行 Jupyter Notebook
jupyter notebook main.ipynb

# 生成分析报告
```

## 数据集说明

原始数据来源：Tableau Sample - Superstore，包含 2014–2017 年美国零售订单数据（9,994 条交易记录、793 位客户、1,862 个产品）。

主要字段：Order ID、Order Date、Ship Date、Sales、Profit、Quantity、Discount、Category、Sub-Category、Segment、Region、State、City、Ship Mode 等。

分析过程中通过 `main.ipynb` 派生了发货天数、利润率、亏损标记、折扣分段等字段，运行完毕后自动将聚合结果导出至 `datasets/` 目录。
