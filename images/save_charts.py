#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从 datasets/ 读取数据，生成所有图表并保存为 PNG 到 images/ 目录。
使用与 main.ipynb 完全相同的 matplotlib 配置以确保中文正常渲染。
"""
import pandas as pd
import numpy as np
import matplotlib
# 不使用 Agg，使用默认 backend 以获得与 Jupyter 一致的中文渲染
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os, sys

warnings.filterwarnings('ignore')

# === 中文字体：与 main.ipynb Cell 5 完全一致 ===
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

DATASET_DIR = 'datasets'
OUTPUT_DIR = 'images'
os.makedirs(OUTPUT_DIR, exist_ok=True)

COLORS = {
    'primary': '#2c3e50', 'secondary': '#3498db', 'accent': '#e74c3c',
    'green': '#27ae60', 'orange': '#f39c12', 'purple': '#9b59b6', 'teal': '#1abc9c',
    'red': '#e74c3c',
}

def save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, format='png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f'  OK {name}')

# === 加载数据 ===
print("Loading datasets...")
yearly_kpi = pd.read_excel(f'{DATASET_DIR}/yearly_kpi.xlsx')
region_stats = pd.read_excel(f'{DATASET_DIR}/region_stats.xlsx')
state_stats = pd.read_excel(f'{DATASET_DIR}/state_stats.xlsx')
segment_summary = pd.read_excel(f'{DATASET_DIR}/segment_summary.xlsx')
subcategory_stats = pd.read_excel(f'{DATASET_DIR}/subcategory_stats.xlsx')
monthly_sales = pd.read_excel(f'{DATASET_DIR}/monthly_sales.xlsx')
shipping_stats = pd.read_excel(f'{DATASET_DIR}/shipping_stats.xlsx')
discount_impact = pd.read_excel(f'{DATASET_DIR}/discount_impact.xlsx')
rfm = pd.read_excel(f'{DATASET_DIR}/rfm.xlsx')
df = pd.read_excel(f'{DATASET_DIR}/Sample - Superstore.xlsx')

def find_col(cols, candidates):
    for c in candidates:
        if c in cols: return c
    for c in cols:
        for cand in candidates:
            if cand.lower() in str(c).lower(): return c
    return None

yk_cols = yearly_kpi.columns.tolist()
SALES_COL = find_col(yk_cols, ['Sales', '销售额'])
PROFIT_COL = find_col(yk_cols, ['Profit', '利润'])
ORDERS_COL = find_col(yk_cols, ['Orders', '订单数'])
CUSTOMERS_COL = find_col(yk_cols, ['Customers', '客户数'])
MARGIN_COL = find_col(yk_cols, ['利润率_%', 'Profit_Margin_%', '利润率'])
AOV_COL = find_col(yk_cols, ['客单价', 'AOV', 'Avg_Order_Value'])

# ============================================================
# Chart 1: 年度趋势概览 (cell 5 in notebook)
# ============================================================
print("Generating charts...")
fig, axes = plt.subplots(2, 3, figsize=(20, 11))
fig.suptitle('年度核心指标趋势', fontsize=18, fontweight='bold', y=1.01)
years = yearly_kpi['year'] if 'year' in yearly_kpi.columns else yearly_kpi.iloc[:,0]

ax = axes[0,0]
sales_data = yearly_kpi[SALES_COL]
bars = ax.bar(range(len(years)), sales_data/1000, color=[COLORS['secondary'], COLORS['teal'], COLORS['purple'], COLORS['orange']])
for bar, val in zip(bars, sales_data/1000):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, f'${val:.0f}K', ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.set_title('年销售额 (K$)', fontsize=14, fontweight='bold')
ax.set_xticks(range(len(years))); ax.set_xticklabels(years); ax.set_ylabel('销售额 (K$)')

ax = axes[0,1]
profit_data = yearly_kpi[PROFIT_COL]
bars = ax.bar(range(len(years)), profit_data/1000, color=[COLORS['secondary'], COLORS['teal'], COLORS['purple'], COLORS['orange']])
for bar, val in zip(bars, profit_data/1000):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'${val:.0f}K', ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.set_title('年利润 (K$)', fontsize=14, fontweight='bold')
ax.set_xticks(range(len(years))); ax.set_xticklabels(years); ax.set_ylabel('利润 (K$)')

ax = axes[0,2]
margin_data = yearly_kpi[MARGIN_COL]
ax.plot(range(len(years)), margin_data, marker='o', linewidth=3, markersize=12, color=COLORS['primary'], markerfacecolor=COLORS['accent'])
for i, val in enumerate(margin_data):
    ax.annotate(f'{val:.1f}%', (i, val), textcoords="offset points", xytext=(0,15), ha='center', fontsize=11, fontweight='bold')
ax.set_title('整体利润率 (%)', fontsize=14, fontweight='bold')
ax.set_xticks(range(len(years))); ax.set_xticklabels(years); ax.set_ylabel('利润率 (%)')
ax.axhline(y=margin_data.mean(), color='gray', linestyle='--', alpha=0.5, label=f'均值: {margin_data.mean():.1f}%')
ax.legend()

ax = axes[1,0]
orders_data = yearly_kpi[ORDERS_COL]
bars = ax.bar(range(len(years)), orders_data, color=[COLORS['secondary'], COLORS['teal'], COLORS['purple'], COLORS['orange']])
for bar, val in zip(bars, orders_data):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 15, f'{val:,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.set_title('年订单数', fontsize=14, fontweight='bold')
ax.set_xticks(range(len(years))); ax.set_xticklabels(years)

ax = axes[1,1]
customers_data = yearly_kpi[CUSTOMERS_COL]
bars = ax.bar(range(len(years)), customers_data, color=[COLORS['secondary'], COLORS['teal'], COLORS['purple'], COLORS['orange']])
for bar, val in zip(bars, customers_data):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, f'{val:,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.set_title('年活跃客户数', fontsize=14, fontweight='bold')
ax.set_xticks(range(len(years))); ax.set_xticklabels(years)

ax = axes[1,2]
aov_data = yearly_kpi[AOV_COL]
ax.plot(range(len(years)), aov_data, marker='s', linewidth=3, markersize=12, color=COLORS['primary'], markerfacecolor=COLORS['green'])
for i, val in enumerate(aov_data):
    ax.annotate(f'${val:.0f}', (i, val), textcoords="offset points", xytext=(0,15), ha='center', fontsize=11, fontweight='bold')
ax.set_title('平均客单价 ($)', fontsize=14, fontweight='bold')
ax.set_xticks(range(len(years))); ax.set_xticklabels(years); ax.set_ylabel('客单价 ($)')
plt.tight_layout()
save(fig, '01_yearly_trends.png')

# ============================================================
# Chart 2: 数据分布 (cell 6 in notebook)
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(20, 11))
fig.suptitle('数据分布与业务维度概况', fontsize=18, fontweight='bold')

ax = axes[0,0]
cat_counts = df['Category'].value_counts()
ax.pie(cat_counts.values, labels=cat_counts.index, autopct='%1.1f%%', colors=[COLORS['secondary'], COLORS['teal'], COLORS['purple']])
ax.set_title('产品类别分布', fontsize=13, fontweight='bold')

ax = axes[0,1]
seg_counts = df['Segment'].value_counts()
ax.pie(seg_counts.values, labels=seg_counts.index, autopct='%1.1f%%', colors=[COLORS['secondary'], COLORS['orange'], COLORS['teal']])
ax.set_title('客户细分分布', fontsize=13, fontweight='bold')

ax = axes[0,2]
region_counts = df['Region'].value_counts()
ax.pie(region_counts.values, labels=region_counts.index, autopct='%1.1f%%', colors=[COLORS['secondary'], COLORS['teal'], COLORS['purple'], COLORS['orange']])
ax.set_title('区域分布', fontsize=13, fontweight='bold')

ax = axes[1,0]
ship_counts = df['Ship Mode'].value_counts()
ax.pie(ship_counts.values, labels=ship_counts.index, autopct='%1.1f%%', colors=[COLORS['secondary'], COLORS['teal'], COLORS['orange'], COLORS['purple']])
ax.set_title('配送模式分布', fontsize=13, fontweight='bold')

ax = axes[1,1]
df['Sales'].hist(bins=50, ax=ax, color=COLORS['secondary'], alpha=0.75, edgecolor='white')
ax.axvline(df['Sales'].mean(), color=COLORS['accent'], linestyle='--', linewidth=2, label=f'均值: ${df["Sales"].mean():.0f}')
ax.axvline(df['Sales'].median(), color=COLORS['green'], linestyle='--', linewidth=2, label=f'中位数: ${df["Sales"].median():.0f}')
ax.set_title('销售额分布', fontsize=13, fontweight='bold')
ax.set_xlabel('销售额 ($)'); ax.set_ylabel('频次'); ax.legend()

ax = axes[1,2]
profit_margin_data = df['Profit Margin'].dropna() * 100
ax.hist(profit_margin_data, bins=50, color=COLORS['teal'], alpha=0.75, edgecolor='white')
ax.axvline(profit_margin_data.mean(), color=COLORS['accent'], linestyle='--', linewidth=2, label=f'均值: {profit_margin_data.mean():.1f}%')
ax.axvline(0, color='red', linestyle='-', linewidth=1)
ax.set_title('利润率分布 (%)', fontsize=13, fontweight='bold')
ax.set_xlabel('利润率 (%)'); ax.set_ylabel('频次'); ax.legend()
plt.tight_layout()
save(fig, '02_distribution.png')

# ============================================================
# Chart 3: 月度销售与利润趋势 (cell 8 in notebook)
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(22, 12))
fig.suptitle('月度销售与利润趋势', fontsize=18, fontweight='bold')
monthly = monthly_sales.copy()
monthly['date_label'] = monthly['Order Year-Month'].astype(str)

ax = axes[0,0]
ax.fill_between(range(len(monthly)), monthly['Sales']/1000, alpha=0.3, color=COLORS['secondary'])
ax.plot(range(len(monthly)), monthly['Sales']/1000, linewidth=2, color=COLORS['secondary'], label='月销售额')
if 'Sales_MA12' in monthly.columns:
    ax.plot(range(len(monthly)), monthly['Sales_MA12']/1000, linewidth=2.5, color=COLORS['accent'], linestyle='--', label='12月移动平均')
ax.set_title('月度销售额趋势 (K$)', fontsize=14, fontweight='bold')
ax.legend(loc='upper left')
peak_idx = monthly['Sales'].idxmax()
ax.annotate(f'峰值: ${monthly.loc[peak_idx, "Sales"]:,.0f}', (peak_idx, monthly.loc[peak_idx, 'Sales']/1000),
            textcoords="offset points", xytext=(0,10), ha='center', fontsize=9,
            arrowprops=dict(arrowstyle='->', color=COLORS['accent']))

ax = axes[0,1]
colors_bar = [COLORS['green'] if v >= 0 else COLORS['red'] for v in monthly['Profit']]
ax.bar(range(len(monthly)), monthly['Profit']/1000, color=colors_bar, alpha=0.7, width=1)
if 'Profit_MA12' in monthly.columns:
    ax.plot(range(len(monthly)), monthly['Profit_MA12']/1000, linewidth=2.5, color=COLORS['primary'], linestyle='--', label='12月移动平均')
ax.axhline(y=0, color='black', linewidth=0.5)
ax.set_title('月度利润 (K$)', fontsize=14, fontweight='bold')
ax.legend(loc='upper left')

ax = axes[1,0]
ax.fill_between(range(len(monthly)), monthly['Orders'], alpha=0.3, color=COLORS['purple'])
ax.plot(range(len(monthly)), monthly['Orders'], linewidth=2, color=COLORS['purple'], marker='o', markersize=3)
ax.set_title('月度订单数', fontsize=14, fontweight='bold')

ax = axes[1,1]
margin_col = 'Profit_Margin' if 'Profit_Margin' in monthly.columns else 'Profit Margin'
ax.plot(range(len(monthly)), monthly[margin_col]*100, linewidth=2, color=COLORS['teal'])
ax.axhline(y=monthly[margin_col].mean()*100, color=COLORS['accent'], linestyle='--', alpha=0.7, label=f'均值: {monthly[margin_col].mean()*100:.1f}%')
ax.fill_between(range(len(monthly)), monthly[margin_col]*100, alpha=0.15, color=COLORS['teal'])
ax.set_title('月度平均利润率 (%)', fontsize=14, fontweight='bold')
ax.legend(loc='upper left')

tick_positions = range(0, len(monthly), 6)
tick_labels = [monthly['date_label'].iloc[i][:7] for i in tick_positions]
for ax_obj in axes.flatten():
    ax_obj.set_xticks(tick_positions)
    ax_obj.set_xticklabels(tick_labels, rotation=45, ha='right', fontsize=8)
plt.tight_layout()
save(fig, '03_monthly_trends.png')

# ============================================================
# Chart 4: 季节性分析 (cell 9 in notebook)
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
fig.suptitle('销售季节性分析', fontsize=18, fontweight='bold')

monthly_mean = df.groupby('Month').agg(Sales=('Sales', 'mean'), Profit=('Profit', 'mean')).reset_index()
ax = axes[0,0]
ax.fill_between(monthly_mean['Month'], monthly_mean['Sales']/1000, alpha=0.3, color=COLORS['secondary'])
ax.plot(monthly_mean['Month'], monthly_mean['Sales']/1000, marker='o', linewidth=2.5, color=COLORS['secondary'])
ax.set_title('各月平均销售额 (K$)', fontsize=13, fontweight='bold')
ax.set_xlabel('月份'); ax.set_xticks(range(1,13))

ax = axes[0,1]
years_list = sorted(df['Year'].unique())
quarterly = df.groupby(['Year', 'Quarter'])['Sales'].sum().unstack(level=0)
x = np.arange(len(quarterly.index)); width = 0.2
colors_yr = [COLORS['secondary'], COLORS['teal'], COLORS['purple'], COLORS['orange']]
for i, year in enumerate(years_list):
    offset = (i - len(years_list)/2 + 0.5) * width
    ax.bar(x + offset, quarterly[year]/1000, width, label=f'{year}', color=colors_yr[i], alpha=0.85)
ax.set_title('季度销售额对比 (K$)', fontsize=13, fontweight='bold')
ax.set_xlabel('季度'); ax.set_xticks(x); ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4']); ax.legend()

ax = axes[0,2]
weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
weekday_sales = df.groupby('Weekday')['Sales'].sum().sort_index()
colors_wd = [COLORS['secondary'] if i < 5 else COLORS['accent'] for i in range(7)]
ax.bar(range(7), weekday_sales.values/1000, color=colors_wd, alpha=0.85)
ax.set_title('周内销售额分布 (K$)', fontsize=13, fontweight='bold')
ax.set_xticks(range(7)); ax.set_xticklabels(weekday_names, rotation=45)

ax = axes[1,0]
pivot = df.pivot_table(values='Sales', index='Month', columns='Year', aggfunc='sum')
sns.heatmap(pivot/1000, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'K$'})
ax.set_title('年度 x 月度销售额热力图 (K$)', fontsize=13, fontweight='bold')
ax.set_ylabel('月份'); ax.set_xlabel('年份')

ax = axes[1,1]
for year in years_list:
    year_data = df[df['Year'] == year]
    monthly_sales_year = year_data.groupby('Month')['Sales'].sum()
    monthly_cum = monthly_sales_year.cumsum()
    ax.plot(monthly_cum.index, monthly_cum.values/1000, marker='o', linewidth=2.5, label=f'{year}', markersize=6)
ax.set_title('年累计销售额曲线 (K$)', fontsize=13, fontweight='bold')
ax.set_xlabel('月份'); ax.set_xticks(range(1,13)); ax.legend()

ax = axes[1,2]
if 'Sales_YoY' in monthly.columns:
    yoy_valid = monthly.dropna(subset=['Sales_YoY'])
    colors_yoy = [COLORS['green'] if v >= 0 else COLORS['red'] for v in yoy_valid['Sales_YoY']]
    ax.bar(range(len(yoy_valid)), yoy_valid['Sales_YoY'], color=colors_yoy, alpha=0.7)
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.axhline(y=yoy_valid['Sales_YoY'].mean(), color=COLORS['secondary'], linestyle='--', label=f'平均: {yoy_valid["Sales_YoY"].mean():.1f}%')
    ax.set_title('月度销售同比增长率 (%)', fontsize=13, fontweight='bold'); ax.legend()
plt.tight_layout()
save(fig, '04_seasonality.png')

# ============================================================
# Chart 5: 产品分析 — 帕累托+子品类利润率+品类饼图+品类对比 (cell 14 in notebook)
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(20, 14))
fig.suptitle('产品结构与盈利分析', fontsize=18, fontweight='bold')

ax = axes[0,0]
subcat_sorted = subcategory_stats.sort_values('Sales', ascending=False).copy()
subcat_sorted['cumsum'] = subcat_sorted['Sales'].cumsum() / subcat_sorted['Sales'].sum() * 100
x_pos = range(len(subcat_sorted))
ax.bar(x_pos, subcat_sorted['Sales']/1000, color=COLORS['secondary'], alpha=0.8)
ax2 = ax.twinx()
ax2.plot(x_pos, subcat_sorted['cumsum'], 'o-', color=COLORS['accent'], linewidth=2.5, markersize=6)
ax2.axhline(y=80, color='gray', linestyle='--', alpha=0.5, label='80% 销售额')
n80 = (subcat_sorted['cumsum'] <= 80).sum()
ax.set_title(f'帕累托图：子品类销售额 (前{n80}个子品类贡献80%)', fontsize=13, fontweight='bold')
ax.set_xticks(x_pos)
ax.set_xticklabels(subcat_sorted['Sub-Category'], rotation=45, ha='right', fontsize=8)
ax.set_ylabel('销售额 (K$)', color=COLORS['secondary'])
ax2.set_ylabel('累计占比 (%)', color=COLORS['accent']); ax2.legend(loc='lower right')

ax = axes[0,1]
margin_sorted = subcategory_stats.sort_values('Profit_Margin_%')
colors_margin = [COLORS['red'] if v < 0 else (COLORS['teal'] if v < 10 else COLORS['green']) for v in margin_sorted['Profit_Margin_%']]
ax.barh(range(len(margin_sorted)), margin_sorted['Profit_Margin_%'], color=colors_margin, alpha=0.85)
ax.axvline(x=0, color='black', linewidth=0.8)
ax.set_title('子品类利润率 (%)', fontsize=13, fontweight='bold')
ax.set_yticks(range(len(margin_sorted)))
ax.set_yticklabels(margin_sorted['Sub-Category'], fontsize=9)
for i, val in enumerate(margin_sorted['Profit_Margin_%']):
    ax.text(val + (0.5 if val >= 0 else -5), i, f'{val:.1f}%', va='center', fontsize=8, fontweight='bold')

ax = axes[1,0]
cat_stats = df.groupby('Category').agg(Sales=('Sales', 'sum'), Profit=('Profit', 'sum')).reset_index()
cat_stats['Margin'] = cat_stats['Profit'] / cat_stats['Sales'] * 100
colors_cat = [COLORS['secondary'], COLORS['teal'], COLORS['purple']]
ax.pie(cat_stats['Sales'], labels=cat_stats['Category'], autopct='%1.1f%%', colors=colors_cat,
       explode=[0.02, 0.02, 0.02], textprops={'fontsize': 11})
ax.set_title('各类别销售额占比', fontsize=13, fontweight='bold')

ax = axes[1,1]
x = np.arange(len(cat_stats)); width = 0.35
bars1 = ax.bar(x - width/2, cat_stats['Sales']/1000, width, label='销售额 (K$)', color=COLORS['secondary'], alpha=0.8)
ax2 = ax.twinx()
bars2 = ax2.bar(x + width/2, cat_stats['Margin'], width, label='利润率 (%)', color=COLORS['orange'], alpha=0.8)
for bar, val in zip(bars2, cat_stats['Margin']):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f'{val:.1f}%', ha='center', fontsize=11, fontweight='bold')
ax.set_title('各类别销售额与利润率', fontsize=13, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(cat_stats['Category'])
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
plt.tight_layout()
save(fig, '05_product_analysis.png')

# ============================================================
# Chart 6: 折扣影响分析 (cell 15 in notebook)
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(20, 13))
fig.suptitle('折扣策略影响分析', fontsize=18, fontweight='bold')
discount = discount_impact.copy()

ax = axes[0,0]
x = np.arange(len(discount)); width = 0.35
bars1 = ax.bar(x - width/2, discount['Total_Sales']/1000, width, label='销售额 (K$)', color=COLORS['secondary'], alpha=0.85)
ax2 = ax.twinx()
bars2 = ax2.bar(x + width/2, discount['Profit_Margin_%'], width, label='利润率 (%)',
                color=[COLORS['green'], COLORS['teal'], COLORS['orange'], COLORS['accent'], COLORS['red']], alpha=0.85)
for bar, val in zip(bars2, discount['Profit_Margin_%']):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (1 if val>=0 else -8), f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')
ax.set_title('折扣带：销售额 vs 利润率', fontsize=13, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(discount['Discount_Band'], rotation=20, ha='right', fontsize=8)
ax.set_ylabel('销售额 (K$)'); ax2.set_ylabel('利润率 (%)')

ax = axes[0,1]
colors_profit = [COLORS['green'] if v >= 0 else COLORS['red'] for v in discount['Total_Profit']]
bars = ax.bar(range(len(discount)), discount['Total_Profit']/1000, color=colors_profit, alpha=0.85)
ax.axhline(y=0, color='black', linewidth=0.8)
for bar, val in zip(bars, discount['Total_Profit']/1000):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (1 if val>=0 else -10), f'${val:+,.0f}K', ha='center', fontsize=10, fontweight='bold')
ax.set_title('折扣带利润贡献 (K$)', fontsize=13, fontweight='bold')
ax.set_xticks(range(len(discount))); ax.set_xticklabels(discount['Discount_Band'], rotation=20, ha='right', fontsize=8)

ax = axes[1,0]
colors_pie = ['#27ae60', '#2ecc71', '#f39c12', '#e67e22', '#e74c3c']
ax.pie(discount['Row_Pct_%'], labels=discount['Discount_Band'], autopct='%1.1f%%', colors=colors_pie, textprops={'fontsize': 8})
ax.set_title('各折扣带交易行占比', fontsize=13, fontweight='bold')

ax = axes[1,1]
cat_discount = df.groupby(['Category', 'Discount_Band']).agg(Profit_Margin=('Profit Margin', 'mean')).reset_index()
pivot_cd = cat_discount.pivot(index='Category', columns='Discount_Band', values='Profit_Margin')
discount_order = ['No Discount (0%)', 'Low (0-20%)', 'Medium (20-40%)', 'High (40-60%)', 'Very High (60%+)']
pivot_cd = pivot_cd.reindex(columns=[d for d in discount_order if d in pivot_cd.columns])
sns.heatmap(pivot_cd*100, annot=True, fmt='.1f', cmap='RdYlGn', center=0, ax=ax, cbar_kws={'label': '利润率 (%)'})
ax.set_title('各类别 x 折扣带 利润率 (%)', fontsize=13, fontweight='bold')
ax.set_xlabel('折扣带')
plt.tight_layout()
save(fig, '06_discount_impact.png')

# ============================================================
# Chart 7: 交叉销售 — 品类共现矩阵 (cell 16 in notebook)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 8))
order_cats = df.groupby('Order ID')['Category'].apply(set).reset_index()
co_matrix = np.zeros((3, 3))
cat_list = sorted(df['Category'].unique())
for _, cats in order_cats.iterrows():
    cat_set = cats['Category']
    for i, c1 in enumerate(cat_list):
        for j, c2 in enumerate(cat_list):
            if c1 in cat_set and c2 in cat_set:
                co_matrix[i, j] += 1
np.fill_diagonal(co_matrix, [df[df['Category']==c]['Order ID'].nunique() for c in cat_list])
sns.heatmap(co_matrix, annot=True, fmt='.0f', xticklabels=cat_list, yticklabels=cat_list, cmap='YlOrRd', ax=ax)
ax.set_title('品类共现矩阵 (订单数)', fontsize=14, fontweight='bold')
ax.set_xlabel('品类'); ax.set_ylabel('品类')
plt.tight_layout()
save(fig, '07_cross_selling.png')

# ============================================================
# Chart 8: 客户画像 (cell 18 in notebook)
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('客户整体画像', fontsize=16, fontweight='bold')
seg_profile = df.groupby('Segment').agg(Sales=('Sales', 'sum'), Profit=('Profit', 'sum'), Orders=('Order ID', 'nunique'), Customers=('Customer ID', 'nunique')).reset_index()
seg_profile['Profit_Margin'] = seg_profile['Profit'] / seg_profile['Sales'] * 100

ax = axes[0]
ax.pie(seg_profile['Sales'], labels=seg_profile['Segment'], autopct='%1.1f%%', colors=[COLORS['secondary'], COLORS['teal'], COLORS['orange']])
ax.set_title('各客户段销售额占比', fontsize=12, fontweight='bold')

ax = axes[1]
x = np.arange(len(seg_profile)); width = 0.35
ax.bar(x - width/2, seg_profile['Sales']/1000, width, label='销售额 (K$)', color=COLORS['secondary'], alpha=0.85)
ax2 = ax.twinx()
ax2.bar(x + width/2, seg_profile['Profit_Margin'], width, label='利润率 (%)', color=COLORS['orange'], alpha=0.85)
ax.set_title('销售额与利润率对比', fontsize=12, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(seg_profile['Segment'])

ax = axes[2]
ax.bar(range(len(seg_profile)), seg_profile['Orders'] / seg_profile['Customers'], color=[COLORS['secondary'], COLORS['teal'], COLORS['orange']])
ax.set_title('客户人均下单次数', fontsize=12, fontweight='bold')
ax.set_xticks(range(len(seg_profile))); ax.set_xticklabels(seg_profile['Segment'])
for i, val in enumerate(seg_profile['Orders'] / seg_profile['Customers']):
    ax.text(i, val + 0.03, f'{val:.2f}', ha='center', fontsize=11, fontweight='bold')
plt.tight_layout()
save(fig, '08_customer_profile.png')

# ============================================================
# Chart 9: RFM 分析 (cell 20 in notebook)
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(20, 13))
fig.suptitle('客户价值细分分析 (RFM)', fontsize=18, fontweight='bold')
seg = segment_summary.copy()

ax = axes[0,0]
seg_sorted = seg.sort_values('Count_Share_%', ascending=False)
colors_rfm = ['#2c3e50', '#3498db', '#e74c3c', '#f39c12', '#1abc9c', '#9b59b6', '#e67e22', '#95a5a6', '#34495e']
ax.pie(seg_sorted['Count'], labels=seg_sorted['Customer group'], autopct='%1.1f%%', colors=colors_rfm[:len(seg_sorted)], textprops={'fontsize': 7})
ax.set_title('客户分层分布', fontsize=13, fontweight='bold')

ax = axes[0,1]
seg_by_sales = seg.sort_values('Total_Sales', ascending=True)
colors_sales = [COLORS['green'] if 'Champion' in cg or 'Loyal' in cg else (COLORS['accent'] if 'Risk' in cg or 'Hibernat' in cg or 'Lost' in cg else COLORS['secondary']) for cg in seg_by_sales['Customer group']]
bars = ax.barh(range(len(seg_by_sales)), seg_by_sales['Total_Sales']/1000, color=colors_sales, alpha=0.85)
ax.set_yticks(range(len(seg_by_sales))); ax.set_yticklabels(seg_by_sales['Customer group'], fontsize=9)
ax.set_title('各客户层销售贡献 (K$)', fontsize=13, fontweight='bold')
for bar, val, share in zip(bars, seg_by_sales['Total_Sales']/1000, seg_by_sales['Sales_Share_%']):
    ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, f'${val:.0f}K ({share:.1f}%)', va='center', fontsize=9)

ax = axes[0,2]
seg_by_margin = seg.sort_values('Avg_Profit_Margin_%')
colors_margin2 = [COLORS['red'] if v < 10 else (COLORS['orange'] if v < 13 else COLORS['green']) for v in seg_by_margin['Avg_Profit_Margin_%']]
ax.barh(range(len(seg_by_margin)), seg_by_margin['Avg_Profit_Margin_%'], color=colors_margin2, alpha=0.85)
ax.axvline(x=seg['Avg_Profit_Margin_%'].mean(), color=COLORS['secondary'], linestyle='--', label=f'均值: {seg["Avg_Profit_Margin_%"].mean():.1f}%')
ax.set_yticks(range(len(seg_by_margin))); ax.set_yticklabels(seg_by_margin['Customer group'], fontsize=9)
ax.set_title('各客户层利润率 (%)', fontsize=13, fontweight='bold'); ax.legend()

ax = axes[1,0]
rfm_scores = rfm['RFM_Score'].value_counts().sort_index()
colors_score = ['#e74c3c' if s <= 6 else '#f39c12' if s <= 9 else '#2ecc71' if s <= 12 else '#27ae60' for s in rfm_scores.index]
ax.bar(rfm_scores.index, rfm_scores.values, color=colors_score, alpha=0.85)
ax.set_title('RFM 分数分布', fontsize=13, fontweight='bold')
ax.set_xlabel('RFM Score (3-15)'); ax.set_ylabel('客户数')

ax = axes[1,1]
segment_dist = df['Segment'].value_counts()
colors_seg = [COLORS['secondary'], COLORS['teal'], COLORS['orange']]
ax.pie(segment_dist.values, labels=segment_dist.index, autopct='%1.1f%%', colors=colors_seg, textprops={'fontsize': 10})
ax.set_title('客户类型分布 (CRM Segment)', fontsize=13, fontweight='bold')

ax = axes[1,2]
champ_loyal = rfm[rfm['Segment_RFM'].isin(['Champions', 'Loyal Customers'])]
other = rfm[~rfm['Segment_RFM'].isin(['Champions', 'Loyal Customers'])]
metrics = ['Recency', 'Frequency', 'Monetary', 'Avg_Profit_Margin']
labels_rfm = ['Recency\n(天)', 'Frequency\n(次)', 'Monetary\n($)', '利润率\n(%)']
x = np.arange(len(metrics)); width = 0.35
champ_vals = [champ_loyal['Recency'].mean(), champ_loyal['Frequency'].mean(), champ_loyal['Monetary'].mean()/100, champ_loyal['Avg_Profit_Margin'].mean()*100]
other_vals = [other['Recency'].mean(), other['Frequency'].mean(), other['Monetary'].mean()/100, other['Avg_Profit_Margin'].mean()*100]
ax.bar(x - width/2, champ_vals, width, label='Champions+Loyal', color=COLORS['green'], alpha=0.85)
ax.bar(x + width/2, other_vals, width, label='其他客户', color=COLORS['secondary'], alpha=0.5)
ax.set_title('高价值客户 vs 其他对比', fontsize=13, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(labels_rfm, fontsize=9); ax.legend()
plt.tight_layout()
save(fig, '09_rfm_analysis.png')

# ============================================================
# Chart 10: 地理分析 (cell 23 in notebook)
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(22, 14))
fig.suptitle('地理市场与区域分析', fontsize=18, fontweight='bold')
region = region_stats.copy()

ax = axes[0,0]
x = np.arange(len(region)); width = 0.35
ax.bar(x - width/2, region['Sales']/1000, width, label='销售额 (K$)', color=COLORS['secondary'], alpha=0.85)
ax2 = ax.twinx()
ax2.bar(x + width/2, region['Profit_Margin_%'], width, label='利润率 (%)', color=[COLORS['green'], COLORS['teal'], COLORS['orange'], COLORS['accent']], alpha=0.85)
for bar, val in zip(ax2.containers[0], region['Profit_Margin_%']):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')
ax.set_title('区域销售额与利润率', fontsize=13, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(region['Region'])
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

ax = axes[0,1]
top_states = state_stats.sort_values('Sales', ascending=True).tail(15)
colors_state = [COLORS['green'] if v >= 10 else (COLORS['accent'] if v >= 0 else COLORS['red']) for v in top_states['Profit_Margin_%']]
bars = ax.barh(range(len(top_states)), top_states['Sales']/1000, color=colors_state, alpha=0.85)
ax.set_yticks(range(len(top_states))); ax.set_yticklabels(top_states['State'], fontsize=8)
ax.set_title('Top 15 州销售额 (K$)', fontsize=13, fontweight='bold')
for bar, val, margin in zip(bars, top_states['Sales']/1000, top_states['Profit_Margin_%']):
    ax.text(bar.get_width() + 3, bar.get_y() + bar.get_height()/2, f'${val:.0f}K ({margin:.1f}%)', va='center', fontsize=7)

ax = axes[0,2]
region_order = region_stats['Region'].tolist()
plot_data = [df[df['Region'] == r]['Profit Margin'].dropna() * 100 for r in region_order]
bp = ax.boxplot(plot_data, labels=region_order, patch_artist=True, showfliers=False)
colors_box = [COLORS['secondary'], COLORS['teal'], COLORS['purple'], COLORS['orange']]
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color); patch.set_alpha(0.6)
ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
ax.set_title('区域利润率分布 (箱线图)', fontsize=13, fontweight='bold')
ax.set_ylabel('利润率 (%)')

ax = axes[1,0]
state_filtered = state_stats[state_stats['Orders'] >= 20].copy()
scatter = ax.scatter(state_filtered['Sales'], state_filtered['Profit_Margin_%'], s=state_filtered['Orders']/2, alpha=0.6, c=state_filtered['Profit_Margin_%'], cmap='RdYlGn', edgecolors='black', linewidth=0.5)
ax.axhline(y=0, color='red', linestyle='--', alpha=0.3)
for _, row in state_filtered.nlargest(5, 'Sales').iterrows():
    ax.annotate(row['State'], (row['Sales'], row['Profit_Margin_%']), textcoords="offset points", xytext=(5,5), fontsize=8, fontweight='bold')
ax.set_title('州级效率前沿 (销售额 vs 利润率)', fontsize=13, fontweight='bold')
ax.set_xlabel('销售额 ($)'); ax.set_ylabel('利润率 (%)')

ax = axes[1,1]
city_stats = df.groupby('City').agg(Sales=('Sales', 'sum'), Profit=('Profit', 'sum')).reset_index()
top_cities = city_stats.sort_values('Sales', ascending=True).tail(20)
colors_city = [COLORS['green'] if v >= 0 else COLORS['red'] for v in top_cities['Profit']]
ax.barh(range(len(top_cities)), top_cities['Sales']/1000, color=colors_city, alpha=0.85)
ax.set_yticks(range(len(top_cities))); ax.set_yticklabels(top_cities['City'], fontsize=7)
ax.set_title('Top 20 城市销售额 (K$)', fontsize=13, fontweight='bold')

ax = axes[1,2]
region_cat = df.groupby(['Region', 'Category'])['Sales'].sum().unstack(fill_value=0)
region_cat_pct = region_cat.div(region_cat.sum(axis=1), axis=0) * 100
region_cat_pct.plot(kind='barh', stacked=True, ax=ax, color=[COLORS['secondary'], COLORS['teal'], COLORS['purple']])
ax.set_title('区域 x 类别 销售结构', fontsize=13, fontweight='bold')
ax.set_xlabel('占比 (%)'); ax.legend(loc='lower right', fontsize=9)
plt.tight_layout()
save(fig, '10_geo_analysis.png')

# ============================================================
# Chart 11: 物流分析 (cell 24 in notebook)
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(22, 13))
fig.suptitle('物流配送与时效分析', fontsize=18, fontweight='bold')
ship = shipping_stats.copy()

ax = axes[0,0]
colors_ship = [COLORS['secondary'], COLORS['teal'], COLORS['orange'], COLORS['purple']]
ax.pie(ship['Order_Share_%'], labels=ship['Ship Mode'], autopct='%1.1f%%', colors=colors_ship, textprops={'fontsize': 9})
ax.set_title('配送模式订单占比', fontsize=13, fontweight='bold')

ax = axes[0,1]
ship_order = ['Same Day', 'First Class', 'Second Class', 'Standard Class']
ship_data = [df[df['Ship Mode'] == m]['Ship Days'].dropna() for m in ship_order]
bp = ax.boxplot(ship_data, labels=ship_order, patch_artist=True, showfliers=False)
for patch, color in zip(bp['boxes'], [COLORS['green'], COLORS['teal'], COLORS['orange'], COLORS['secondary']]):
    patch.set_facecolor(color); patch.set_alpha(0.6)
ax.set_title('各模式配送天数分布', fontsize=13, fontweight='bold'); ax.set_ylabel('配送天数')

ax = axes[0,2]
x = np.arange(len(ship)); width = 0.35
ax.bar(x - width/2, ship['Sales']/1000, width, label='销售额 (K$)', color=COLORS['secondary'], alpha=0.8)
ax2 = ax.twinx()
ax2.bar(x + width/2, ship['Profit_Margin_%'], width, label='利润率 (%)', color=[COLORS['green'], COLORS['teal'], COLORS['orange'], COLORS['purple']], alpha=0.8)
for bar, val in zip(ax2.containers[0], ship['Profit_Margin_%']):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')
ax.set_title('配送模式：销售额与利润率', fontsize=13, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(ship['Ship Mode'], fontsize=8)
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

ax = axes[1,0]
ship_year = df.groupby(['Year', 'Ship Mode'])['Order ID'].nunique().unstack(fill_value=0)
ship_year_pct = ship_year.div(ship_year.sum(axis=1), axis=0) * 100
ship_year_pct.plot(kind='area', stacked=True, ax=ax, alpha=0.7, color=colors_ship)
ax.set_title('配送模式年度趋势 (%)', fontsize=13, fontweight='bold')
ax.set_xlabel('年份'); ax.set_ylabel('占比 (%)'); ax.legend(loc='upper left', fontsize=8)

ax = axes[1,1]
ship_month = df.groupby('Order Year-Month')['Ship Days'].mean().reset_index()
ax.plot(range(len(ship_month)), ship_month['Ship Days'], linewidth=2, color=COLORS['secondary'])
ax.fill_between(range(len(ship_month)), ship_month['Ship Days'], alpha=0.2, color=COLORS['secondary'])
ax.axhline(y=ship_month['Ship Days'].mean(), color=COLORS['accent'], linestyle='--', label=f'平均: {ship_month["Ship Days"].mean():.1f}天')
ax.set_title('月度平均配送天数趋势', fontsize=13, fontweight='bold'); ax.legend()

ax = axes[1,2]
ship_cat = df.groupby(['Ship Mode', 'Category'])['Sales'].sum().unstack(fill_value=0)
ship_cat_pct = ship_cat.div(ship_cat.sum(axis=1), axis=0) * 100
ship_cat_pct_reindex = ship_cat_pct.reindex(ship_order)
ship_cat_pct_reindex.plot(kind='barh', stacked=True, ax=ax, color=[COLORS['secondary'], COLORS['teal'], COLORS['purple']])
ax.set_title('配送模式 x 类别 销售结构', fontsize=13, fontweight='bold')
ax.set_xlabel('占比 (%)'); ax.legend(loc='lower right', fontsize=9)
plt.tight_layout()
save(fig, '11_shipping_analysis.png')

# ============================================================
# Chart 12: 相关性分析 (cell 26 in notebook)
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(20, 8))
fig.suptitle('相关性分析与利润归因', fontsize=18, fontweight='bold')

ax = axes[0]
corr_cols = ['Sales', 'Quantity', 'Discount', 'Profit', 'Profit Margin', 'Ship Days']
corr_matrix = df[corr_cols].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='RdBu_r', center=0, vmin=-1, vmax=1, square=True, ax=ax, mask=mask, cbar_kws={'label': '相关系数'})
ax.set_title('数值变量相关性矩阵', fontsize=14, fontweight='bold')

ax = axes[1]
from scipy import stats
sample = df.sample(min(3000, len(df)), random_state=42)
scatter = ax.scatter(sample['Discount']*100, sample['Profit Margin']*100, c=sample['Profit Margin']*100, cmap='RdYlGn', alpha=0.4, s=10, edgecolors='none')
ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
ax.set_title('折扣率 vs 利润率 (散点, n=3000)', fontsize=14, fontweight='bold')
ax.set_xlabel('折扣率 (%)'); ax.set_ylabel('利润率 (%)')
slope, intercept, r_value, p_value, std_err = stats.linregress(sample['Discount'], sample['Profit Margin'])
x_line = np.linspace(0, 0.8, 100)
ax.plot(x_line*100, (intercept + slope*x_line)*100, 'b-', linewidth=2, label=f'回归线 (R^2={r_value**2:.3f}, p<0.001)')
ax.legend()
plt.colorbar(scatter, ax=ax, label='利润率 (%)')
plt.tight_layout()
save(fig, '12_correlation.png')

# ============================================================
# Chart 13: 利润瀑布图 (cell 27 in notebook)
# ============================================================
fig, ax = plt.subplots(figsize=(16, 8))
discount = discount_impact.copy()
colors_wf = [COLORS['green'] if v >= 0 else COLORS['red'] for v in discount['Total_Profit']]
bars_data = []; bottoms = []; prev = 0
for i, (band, profit) in enumerate(zip(discount['Discount_Band'], discount['Total_Profit'])):
    bottoms.append(0 if i == 0 else prev)
    bars_data.append(profit)
    prev += profit

x = np.arange(len(discount))
ax.bar(x, [max(0, v) for v in bars_data], bottom=bottoms, color=colors_wf, alpha=0.85, edgecolor='white')
for i, (val, bottom, color) in enumerate(zip(bars_data, bottoms, colors_wf)):
    if val < 0:
        ax.bar(i, abs(val), bottom=bottom + val, color=color, alpha=0.85, edgecolor='white')

for i, (val, total) in enumerate(zip(discount['Total_Profit'], discount['Total_Sales'])):
    ax.text(i, total/1000 + 20, f'利润: ${val:+,.0f}\n销售额: ${total:,.0f}', ha='center', fontsize=10, fontweight='bold')

ax.axhline(y=0, color='black', linewidth=0.8)
ax.set_title('利润瀑布图：各折扣带的利润贡献', fontsize=16, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(discount['Discount_Band'], rotation=20, ha='right', fontsize=9)
ax.set_ylabel('累计 (K$)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x/1000:,.0f}K'))
plt.tight_layout()
save(fig, '13_profit_waterfall.png')

# ============================================================
# Chart 14: 产品矩阵 — 销售额 vs 利润率气泡图 (from cell 14)
# ============================================================
fig, ax = plt.subplots(figsize=(12, 8))
subcat = subcategory_stats.copy()
scatter = ax.scatter(subcat['Sales'], subcat['Profit_Margin_%'], s=subcat['Orders']*2, alpha=0.6, c=subcat['Profit_Margin_%'], cmap='RdYlGn', edgecolors='black', linewidth=0.5)
ax.axhline(y=0, color='red', linestyle='--', alpha=0.3)
ax.axhline(y=subcat['Profit_Margin_%'].mean(), color='blue', linestyle='--', alpha=0.5, label=f'平均利润率: {subcat["Profit_Margin_%"].mean():.1f}%')
ax.axvline(x=subcat['Sales'].mean(), color='gray', linestyle='--', alpha=0.5, label=f'平均销售额: ${subcat["Sales"].mean():,.0f}')
for _, row in subcat.iterrows():
    ax.annotate(row['Sub-Category'], (row['Sales'], row['Profit_Margin_%']), textcoords="offset points", xytext=(5,5), fontsize=8)
ax.set_title('产品矩阵：销售额 vs 利润率 (气泡大小=订单量)', fontsize=14, fontweight='bold')
ax.set_xlabel('销售额 ($)'); ax.set_ylabel('利润率 (%)'); ax.legend()
plt.colorbar(scatter, ax=ax, label='利润率 (%)')
plt.tight_layout()
save(fig, '14_product_matrix.png')

print(f"\nAll {len(os.listdir(OUTPUT_DIR))} charts saved to {OUTPUT_DIR}/")
