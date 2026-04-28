# 🌍 Africa Climate Monitor


## 🚀 Live Dashboard

**Access the deployed dashboard here:**  
👉 **[https://african-climate-challenge-week0.streamlit.app](https://african-climate-challenge-week0.streamlit.app)** 👈

---

An interactive Streamlit dashboard for visualizing and analyzing climate data across five African nations (Ethiopia, Kenya, Nigeria, Sudan, Tanzania) from 2015-2026.

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Development Process](#development-process)
- [Technical Architecture](#technical-architecture)
- [Installation & Setup](#installation--setup)
- [Usage Instructions](#usage-instructions)
- [Dashboard Walkthrough](#dashboard-walkthrough)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)

## 📖 Project Overview

This dashboard was developed as part of EthioClimate Analytics' contribution to positioning Ethiopia as a data-informed host for global climate negotiations. The tool enables interactive exploration of climate patterns, extreme events, and cross-country comparisons to support evidence-based policy recommendations.

### Business Problem
African nations face disproportionate climate impacts despite minimal emissions. Decision-makers need interactive tools to visualize and compare climate vulnerabilities across countries to advocate for targeted adaptation funding.

### Solution
An interactive Streamlit dashboard that provides:
- Real-time filtering by country and year range
- Comparative visualizations of temperature and precipitation patterns
- Statistical validation of climate differences
- Exportable summary statistics

## ✨ Features

| Feature | Description | Interactive Elements |
|---------|-------------|---------------------|
| **Country Selector** | Multi-select dropdown to compare 1-5 countries | ✅ Checkboxes |
| **Year Range Slider** | Zoom into specific time periods (2015-2026) | ✅ Slider |
| **Variable Selector** | Toggle between 7 climate variables | ✅ Dropdown |
| **Temperature Trends** | Line charts with monthly and seasonal patterns | ✅ Hover tooltips, zoom, pan |
| **Precipitation Analysis** | Boxplots, extreme event tracking | ✅ Threshold slider |
| **Summary Statistics** | Country comparisons with download option | ✅ Interactive bar charts |
| **Statistical Insights** | Kruskal-Wallis test results | ✅ Metrics display |

## 🛠️ Development Process

### Phase 1: Data Collection & Cleaning (Week 1)

**Objective:** Prepare raw climate data for analysis

```python
# Data cleaning steps performed:
1. Standardized date formats across all countries
2. Handled missing values using forward fill
3. Removed duplicate records (0 found)
4. Validated physical plausibility (0 impossible values)
5. Added derived columns: Year, Month, Season
6. Flagged outliers using Z-score method (|Z| > 3)
```

**Key Decisions:**
- ✅ **Kept all 132 outliers** after verifying they represent real seasonal extremes
- ✅ Used median instead of mean for skewed precipitation data
- ✅ Applied log transformation for visualization of heavy-tailed distributions

**Data Quality Checks:**
```
Physically impossible rows: 0
Missing values: 0
Duplicate rows: 0
Outlier rows: 132 (3.21% of data) - all verified as real events
```

### Phase 2: Exploratory Data Analysis (Week 2)

**Objective:** Identify patterns, trends, and anomalies

**Temperature Analysis:**
- Identified significant temperature differences across countries (Kruskal-Wallis: H=15,393, p<0.001)
- Ethiopia: 16.1°C (coolest, most stable)
- Sudan: 28.8°C (warmest, most variable)
- Temperature range: 12.7°C between warmest and coolest countries

**Precipitation Analysis:**
- Highly skewed distribution confirmed (mean=3.63 vs median=0.82 mm/day)
- Ethiopia: Bimodal pattern with 63% of rain in July-September
- Sudan: Extreme dry spells (120-165 consecutive days)
- Nigeria: Highest flood risk (intense rainfall events)

**Outlier Investigation:**
- All 132 outliers were seasonal extremes, not data errors
- Precipitation outliers: 95 events (monsoon season)
- Temperature outliers: 21 events (dry season cold spells)
- Humidity outliers: 13 events (extreme dry conditions)

### Phase 3: Statistical Testing (Week 3)

**Objective:** Validate significance of observed differences

**Assumption Checks:**
```python
# Normality (D'Agostino's test)
Ethiopia: p=0.0683 ✅ Normal
Kenya: p=0.0099 ❌ Not Normal
Nigeria: p=0.0000 ❌ Not Normal
Sudan: p=0.0000 ❌ Not Normal
Tanzania: p=0.0000 ❌ Not Normal

# Homogeneity of variances (Levene's test)
Levene statistic: 2836.92, p=0.0000 ❌ Variances unequal
```

**Final Test Used: Kruskal-Wallis (Non-parametric)**
- H-statistic: 15,393.0
- P-value: p < 0.0001
- Degrees of freedom: 4
- **Conclusion:** Temperature differences are highly significant and not due to chance

### Phase 4: Dashboard Development (Week 4)

**Objective:** Build interactive visualization platform

**Technology Selection:**
| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Frontend | Streamlit | Fast prototyping, built-in widgets |
| Visualization | Plotly | Interactive hover, zoom, pan |
| Statistics | SciPy | Kruskal-Wallis, normality tests |
| Data Processing | Pandas | Efficient filtering aggregation |

**Development Challenges & Solutions:**

| Challenge | Solution |
|-----------|----------|
| Hover showing all countries at once | Changed `hovermode='x unified'` to `hovermode='closest'` |
| Boxplot deprecated palette warning | Replaced seaborn with Plotly boxplot |
| GroupBy apply warning | Added `include_groups=False` parameter |
| Streamlit caching errors | Fixed decorator syntax: `@st.cache_data` |

## 🏗️ Technical Architecture

### Data Flow Diagram
```
CSV Files → load_data() → Combined DataFrame → filter_data() → Filtered DataFrame
                                                                    ↓
                                                    ┌───────────────┴───────────────┐
                                                    ↓                               ↓
                                            aggregate_monthly()           calculate_summary_stats()
                                                    ↓                               ↓
                                            Plotly Charts                   Summary Tables
```

### Key Functions (utils.py)

| Function | Purpose | Caching |
|----------|---------|---------|
| `load_data()` | Load and combine all CSV files | ✅ @st.cache_data |
| `filter_data()` | Apply country/year filters | ✅ @st.cache_data |
| `aggregate_monthly()` | Resample to monthly averages | ✅ @st.cache_data |
| `calculate_summary_stats()` | Compute descriptive statistics | ✅ @st.cache_data |
| `get_variable_label()` | Human-readable variable names | ❌ No cache needed |

## 💻 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Git
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/semegn19/climate-challenge-week0.git
cd climate-challenge-week0
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Dashboard
```bash
streamlit run app/main.py
```

The dashboard will open automatically at `http://localhost:8501`

## 🎮 Usage Instructions

### Quick Start Guide

1. **Select Countries** (Sidebar)
   - Click dropdown to choose 1-5 countries
   - Default: All countries selected

2. **Adjust Year Range** (Sidebar)
   - Drag slider to focus on specific years
   - Range: 2015-2026

3. **Choose Variable** (Sidebar)
   - Temperature variables: T2M, T2M_MAX, T2M_MIN
   - Precipitation: PRECTOTCORR
   - Humidity: RH2M
   - Wind: WS2M
   - Specific humidity: QV2M

4. **Navigate Tabs**
   - 📈 Temperature Trends: Time-series and seasonal patterns
   - 💧 Precipitation Analysis: Boxplots and extreme events
   - 📊 Summary Statistics: Tables and bar charts
   - 🔬 Statistical Insights: Kruskal-Wallis results

### Interactive Features

| Action | How to Use | Result |
|--------|-----------|--------|
| **Hover for values** | Mouse over any data point | Tooltip shows exact value |
| **Zoom** | Click and drag on chart | Magnifies selected area |
| **Reset zoom** | Double-click chart | Returns to full view |
| **Hide countries** | Click country in legend | Toggles visibility |
| **Export chart** | Click camera icon | Downloads as PNG |
| **Download stats** | Click download button | Saves CSV file |

### Example Analysis Workflow

**Scenario:** Compare Ethiopia vs Sudan temperature trends (2015-2020)

1. Sidebar: Select only Ethiopia and Sudan
2. Year range: 2015-2020
3. Variable: T2M
4. Tab: Temperature Trends
5. Hover over lines to compare monthly values
6. Note: Sudan consistently warmer by ~12°C

## 📊 Dashboard Walkthrough

### Tab 1: Temperature Trends

**Chart 1: Time Series**
- X-axis: Date (monthly resolution)
- Y-axis: Temperature (°C)
- Each line: Different country
- **Interactive feature:** Hover shows exact month and temperature

**Chart 2: Seasonal Patterns**
- X-axis: Month (Jan-Dec)
- Y-axis: Average temperature
- Shows annual cycle across all years

### Tab 2: Precipitation Analysis

**Chart 1: Distribution Boxplot**
- Shows spread of daily rainfall by country
- Red dots: Mean values
- Box: Interquartile range (25th-75th percentile)

**Chart 2: Extreme Events**
- Adjust threshold slider (default: 20mm/day)
- View total or yearly trends
- Identify flood-risk countries

### Tab 3: Summary Statistics

**Table:** Mean, median, std dev, min, max by country
**Bar Chart:** Visual comparison of means
**Download Button:** Export data for external analysis

### Tab 4: Statistical Insights

**Kruskal-Wallis Results:**
- H-statistic: 15,393.0 (very large = strong evidence)
- P-value: p < 0.001 (highly significant)
- **Conclusion:** Real temperature differences exist


## 👥 Contributors

- **Data Analyst:** Semegn Mulugeta

## 📧 Contact

For questions or support:
- **GitHub Issues:** [https://github.com/semegn19/climate-challenge-week0/issues](https://github.com/semegn19/climate-challenge-week0/issues)

---

**Last Updated:** April 2026
**Version:** 1.0.0
**Status:** Production Ready ✅

*"Data-driven insights for Africa's climate resilience"*
```