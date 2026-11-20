# KiranaStock — Demand Forecasting & Inventory Optimization for Indian Kirana Stores

A machine learning-powered demand forecasting and inventory replenishment engine built for Indian MSME Kirana stores to eliminate **overstocking of slow-moving goods** and **understocking of fast-moving essentials** through historical daily sales analysis, seasonal modeling, and inventory tracking.

---

## 📌 Project Overview

Traditional kirana stores frequently face two interconnected inventory management challenges:
1. **Understocking Fast-Moving SKUs**: Fast-moving consumer goods (such as milk pouches, glucose biscuits, and staples) sell out quickly, especially during weekends, salary cycles, or festival surges. A stockout leads to lost sales and dissatisfied customers.
2. **Overstocking Slow-Moving SKUs**: Products with low or lumpy customer velocity (such as specialty whole spices, floor cleaners, or large packs) occupy precious, constrained shelf space, tie up working capital, and risk physical damage or expiration.

**KiranaStock** solves this by formulating retail demand forecasting as a machine learning regression task, predicting the expected 7-day daily demand for each product while tracking stock availability to un-censor sales during stockout events.

---

## 🗂️ Repository Architecture & Directory Flow

The project directory structure is organized as follows:

```
KiranaStock/
│
├── data/
│   ├── raw/
│   │   ├── products.csv              # Product Master (20 SKUs with cost, MRP, velocity, ROP)
│   │   ├── categories.csv            # Category Master (6 retail categories)
│   │   └── daily_sales.csv           # Historical daily sales (14,600 records across 730 days)
│   │
│   ├── inventory/
│   │   └── inventory_records.csv     # Daily inventory movements, stockouts & replenishment
│   │
│   └── processed/
│       └── .gitkeep                  # Feature-engineered & train/test split datasets
│
├── notebooks/
│   └── 01_dataset_eda_and_validation.ipynb  # Dataset inspection, conservation checks & EDA
│
├── src/
│   ├── __init__.py
│   ├── generate_datasets.py          # Ground-truth synthetic dataset simulation engine
│   └── create_notebook.py           # EDA notebook builder
│
├── models/
│   └── .gitkeep                      # Trained model weights (Random Forest, XGBoost)
│
├── inventory/
│   └── inventory-categories.md       # Product & category specification catalog
│
├── initial.md                        # Project initial concept and vision notes
├── model-summary.md                  # Model pipeline checkpoints and architecture diagram
├── problem-statement.md              # Formal retail MSME problem statement
└── README.md                         # Comprehensive project documentation & Phase 1 deliverables
```

---

## 📋 Phase 1: Dataset Design & Construction Deliverables

---

### Task 1: Finalized Product Master

The Product Master contains **20 representative SKUs** categorized into **6 core kirana categories**, reflecting standard pack sizes, procurement costs, Maximum Retail Prices (MRP), gross margins, shelf life, and velocity classes.

Located at: [`data/raw/products.csv`](data/raw/products.csv)

| Product ID | Product Name | Category ID | Category Name | Sub-Category | Unit of Measure | Cost (₹) | MRP (₹) | Base SP (₹) | Margin (%) | Shelf Life (Days) | Storage Type | Velocity Class | ROP (Units) | Order Batch (Units) | Lead Time (Days) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **P001** | Raw Rice (1 kg) | C001 | Grains, Flours & Pulses | Rice & Grains | kg | 54.00 | 65.00 | 63.00 | 16.67% | 180 | Ambient Dry | Fast | 25 | 60 | 2 |
| **P002** | Whole Wheat Atta (5 kg) | C001 | Grains, Flours & Pulses | Flours | bag (5kg) | 208.00 | 240.00 | 235.00 | 12.98% | 90 | Ambient Dry | Medium | 12 | 30 | 2 |
| **P003** | Toor Dal (1 kg) | C001 | Grains, Flours & Pulses | Pulses | kg | 138.00 | 160.00 | 155.00 | 12.32% | 180 | Ambient Dry | Fast | 18 | 45 | 2 |
| **P004** | Poha (500 g) | C001 | Grains, Flours & Pulses | Breakfast Staples | packet (500g) | 36.00 | 45.00 | 44.00 | 22.22% | 120 | Ambient Dry | Medium | 14 | 35 | 3 |
| **P005** | Sunflower Oil (1 L) | C002 | Oils, Dairy & Sweeteners | Edible Oils | pouch (1L) | 126.00 | 145.00 | 140.00 | 11.11% | 180 | Ambient Dry | Fast | 22 | 50 | 2 |
| **P006** | White Sugar (1 kg) | C002 | Oils, Dairy & Sweeteners | Sweeteners | kg | 40.50 | 48.00 | 46.00 | 13.58% | 365 | Ambient Dry | Fast | 30 | 75 | 2 |
| **P007** | Milk Pouch (500 ml) | C002 | Oils, Dairy & Sweeteners | Dairy | pouch (500ml) | 27.50 | 30.00 | 30.00 | 9.09% | 2 | Refrigerated | Fast | 15 | 55 | 1 |
| **P008** | Turmeric Powder (100 g) | C003 | Spices & Condiments | Ground Spices | packet (100g) | 26.00 | 35.00 | 34.00 | 30.77% | 365 | Ambient Dry | Medium | 10 | 25 | 3 |
| **P009** | Red Chilli Powder (100 g) | C003 | Spices & Condiments | Ground Spices | packet (100g) | 34.00 | 45.00 | 44.00 | 29.41% | 365 | Ambient Dry | Medium | 12 | 30 | 3 |
| **P010** | Cumin Seeds / Jeera (100 g) | C003 | Spices & Condiments | Whole Spices | packet (100g) | 48.00 | 65.00 | 62.00 | 29.17% | 365 | Ambient Dry | Slow | 8 | 20 | 4 |
| **P011** | Tea Leaves (250 g) | C004 | Packaged Foods & Beverages | Hot Beverages | carton (250g) | 98.00 | 120.00 | 118.00 | 20.41% | 365 | Ambient Dry | Fast | 18 | 45 | 2 |
| **P012** | Glucose Biscuits (100 g) | C004 | Packaged Foods & Beverages | Biscuits & Cookies | packet (100g) | 8.40 | 10.00 | 10.00 | 19.05% | 180 | Ambient Dry | Fast | 50 | 120 | 2 |
| **P013** | Instant Noodles (70 g) | C004 | Packaged Foods & Beverages | Ready-to-Cook | packet (70g) | 11.80 | 14.00 | 14.00 | 18.64% | 240 | Ambient Dry | Fast | 35 | 80 | 2 |
| **P014** | Potato Chips (52 g) | C004 | Packaged Foods & Beverages | Salty Snacks | bag (52g) | 16.50 | 20.00 | 20.00 | 21.21% | 120 | Ambient Dry | Fast | 25 | 60 | 2 |
| **P015** | Bathing Soap (100 g) | C005 | Personal Care & Hygiene | Soaps & Wash | bar (100g) | 32.50 | 40.00 | 38.00 | 16.92% | 730 | Ambient Dry | Medium | 16 | 40 | 3 |
| **P016** | Shampoo Sachet (6 ml) | C005 | Personal Care & Hygiene | Hair Care | sachet (6ml) | 2.20 | 3.00 | 3.00 | 36.36% | 730 | Ambient Dry | Fast | 60 | 150 | 2 |
| **P017** | Toothpaste (100 g) | C005 | Personal Care & Hygiene | Oral Care | tube (100g) | 48.00 | 60.00 | 58.00 | 20.83% | 730 | Ambient Dry | Slow | 10 | 25 | 3 |
| **P018** | Detergent Powder (1 kg) | C006 | Household Cleaning & Essentials | Laundry Care | packet (1kg) | 90.00 | 110.00 | 105.00 | 16.67% | 730 | Ambient Dry | Medium | 14 | 35 | 3 |
| **P019** | Dishwashing Bar (200 g) | C006 | Household Cleaning & Essentials | Dish Care | bar (200g) | 16.00 | 20.00 | 20.00 | 25.00% | 730 | Ambient Dry | Fast | 25 | 60 | 2 |
| **P020** | Floor Cleaner (500 ml) | C006 | Household Cleaning & Essentials | Surface Care | bottle (500ml) | 76.00 | 95.00 | 92.00 | 21.05% | 730 | Ambient Dry | Slow | 8 | 20 | 4 |

---

### Task 2: Daily Sales Dataset Schema

Located at: [`data/raw/daily_sales.csv`](data/raw/daily_sales.csv)  
**Total Records:** 14,600 rows (730 days $\times$ 20 products, covering November 21, 2024 to November 20, 2026).

- **Primary Key:** `(date, product_id)`
- **Foreign Key:** `product_id` references `data/raw/products.csv (product_id)`
- **Target Variable for ML:** `units_sold`
- **Zero-Sales Handling:** All 20 products have an explicit row for every date. Days with no sales are recorded as `units_sold = 0` to prevent survivorship bias and zero-censoring.

#### Schema Definition

| Column | Data Type | Nullable | Constraints / Values | Description |
| :--- | :--- | :--- | :--- | :--- |
| `date` | `DATE` (`YYYY-MM-DD`) | No | `2024-11-21` to `2026-11-20` | Calendar date of transaction |
| `product_id` | `VARCHAR(4)` | No | `P001` through `P020` | Unique product SKU identifier |
| `units_sold` | `INTEGER` | No | $\ge 0$ | Number of listed units sold (**Target variable**) |
| `unit_selling_price` | `DECIMAL(8,2)` | No | $> 0.00$ (in INR ₹) | Effective selling price per unit on that day |
| `discount_percentage`| `DECIMAL(5,2)` | No | $0.0 \le x \le 20.0$ | Percentage discount applied relative to base MRP |
| `promotion_flag` | `TINYINT` | No | `0` (No) or `1` (Active) | Indicates whether a promotional deal was active |

---

### Task 3: Inventory Dataset Schema

Located at: [`data/inventory/inventory_records.csv`](data/inventory/inventory_records.csv)  
**Total Records:** 14,600 rows (730 days $\times$ 20 products).

- **Primary Key:** `(date, product_id)`
- **Foreign Key:** `product_id` references `data/raw/products.csv (product_id)`
- **Physical Inventory Conservation Law:** Every single record strictly obeys:
  $$\text{closing\_stock}_t = \text{opening\_stock}_t + \text{units\_received}_t - \text{units\_sold}_t - \text{damaged\_units}_t$$
- **Temporal Continuity:** For every product $i$:
  $$\text{opening\_stock}_{t+1} = \text{closing\_stock}_t$$
- **Stockout Mechanics & Demand Un-Censoring:**
  When $\text{stockout\_flag} = 1$, the shop ran out of stock during the day ($\text{closing\_stock} = 0$). The observed `units_sold` is capped by available inventory rather than true customer latent demand ($D_t \ge \text{available\_stock}$).

#### Schema Definition

| Column | Data Type | Nullable | Constraints / Values | Description |
| :--- | :--- | :--- | :--- | :--- |
| `date` | `DATE` (`YYYY-MM-DD`) | No | `2024-11-21` to `2026-11-20` | Inventory recording date |
| `product_id` | `VARCHAR(4)` | No | `P001` through `P020` | Unique product identifier |
| `opening_stock` | `INTEGER` | No | $\ge 0$ | Physical inventory available at store opening (06:00 AM) |
| `units_received` | `INTEGER` | No | $\ge 0$ | Replenishment stock delivered by distributor during day |
| `units_sold` | `INTEGER` | No | $\ge 0$ | Daily units sold (matches `daily_sales.csv`) |
| `damaged_units` | `INTEGER` | No | $\ge 0$ | Unsellable units due to leakage, pouch burst, or rodent damage |
| `closing_stock` | `INTEGER` | No | $\ge 0$ | Verified stock on hand at store close (10:00 PM) |
| `stockout_flag` | `TINYINT` | No | `0` (In Stock) or `1` (Stockout) | Flags whether product became unavailable during business hours |

---

### Task 4: Complete Data Dictionary

The comprehensive data dictionary covers all 4 generated datasets.

#### Table 1: Categories Master (`data/raw/categories.csv`)
1. `category_id` *(String, Primary Key)*: 4-character identifier (`C001` to `C006`).
2. `category_name` *(String)*: Human-readable retail category name.
3. `description` *(String)*: Detailed functional scope of the category.
4. `avg_shelf_life_days` *(Integer)*: Average product shelf life in days across the category.
5. `margin_percentage` *(Float)*: Typical average gross retailer margin percentage for the category.
6. `storage_requirement` *(String)*: Environmental storage constraints (e.g., Ambient Dry, Refrigerated).

#### Table 2: Product Master (`data/raw/products.csv`)
1. `product_id` *(String, Primary Key)*: Unique SKU identifier (`P001` to `P020`).
2. `product_name` *(String)*: Name and standard retail pack size.
3. `category_id` *(String, Foreign Key)*: References `categories.csv (category_id)`.
4. `category_name` *(String)*: Category name for denormalized query convenience.
5. `sub_category` *(String)*: Detailed sub-department classification (e.g., Rice & Grains, Dairy).
6. `brand_tier` *(String)*: Market positioning (`Popular`, `Mass`, `Value`).
7. `unit_of_measure` *(String)*: Unit descriptor (`kg`, `bag (5kg)`, `pouch (1L)`, `sachet (6ml)`).
8. `cost_price` *(Float)*: Wholesale procurement cost in Indian Rupees (₹).
9. `base_mrp` *(Float)*: Manufacturer Maximum Retail Price (₹).
10. `base_selling_price` *(Float)*: Standard daily retail counter selling price (₹).
11. `margin_pct` *(Float)*: Gross markup percentage calculated as $((MRP - Cost) / MRP) \times 100$.
12. `shelf_life_days` *(Integer)*: Number of days before product expiration or quality degradation.
13. `storage_type` *(String)*: Storage conditions (`Ambient Dry`, `Refrigerated`).
14. `velocity_class` *(String)*: Demand velocity categorization (`Fast`, `Medium`, `Slow`).
15. `reorder_point` *(Integer)*: Inventory threshold ($ROP$) triggering purchase order placement.
16. `reorder_quantity` *(Integer)*: Standard wholesale replenishment batch size ($EOQ$).
17. `lead_time_days` *(Integer)*: Expected business days between supplier order and store delivery.

#### Table 3: Daily Sales (`data/raw/daily_sales.csv`)
1. `date` *(Date)*: Transaction date in ISO-8601 (`YYYY-MM-DD`).
2. `product_id` *(String, Foreign Key)*: References `products.csv (product_id)`.
3. `units_sold` *(Integer, Target Variable)*: Actual units purchased by customers.
4. `unit_selling_price` *(Float)*: Effective per-unit price charged to the consumer (in ₹).
5. `discount_percentage` *(Float)*: Promotional discount percentage applied to base MRP.
6. `promotion_flag` *(Integer)*: Binary flag (`1` if a special promotional campaign was active, `0` otherwise).

#### Table 4: Inventory Records (`data/inventory/inventory_records.csv`)
1. `date` *(Date)*: Inventory balance date (`YYYY-MM-DD`).
2. `product_id` *(String, Foreign Key)*: References `products.csv (product_id)`.
3. `opening_stock` *(Integer)*: Available inventory units at the start of business day.
4. `units_received` *(Integer)*: Total quantity of stock replenished from distributors on that date.
5. `units_sold` *(Integer)*: Total units sold out of available inventory during the day.
6. `damaged_units` *(Integer)*: Count of broken, burst, leaked, or expired units removed from stock.
7. `closing_stock` *(Integer)*: Remaining units on shelf/backroom at the end of the day.
8. `stockout_flag` *(Integer)*: Binary indicator (`1` if inventory hit zero during trading hours, `0` otherwise).

---

### Task 5: Dataset Construction Strategy (Approach B: Synthetic Dataset)

To model real-world Indian kirana retail dynamics with high fidelity, the simulation combines domain knowledge from FMCG retail science with discrete-event inventory simulation.

#### 1. Mathematical Demand Decomposition Model
Customer latent demand $D_{i,t}$ for product $i$ on day $t$ is formulated as a multiplicative multi-factor process:

$$\mu_{i,t} = \lambda_{0,i} \times M_{\text{dow}}(t, i) \times M_{\text{salary}}(t, i) \times M_{\text{fest}}(t, i) \times M_{\text{season}}(t, i) \times M_{\text{price}}(t, i)$$

Where:
- $\lambda_{0,i}$: Product baseline daily demand rate.
- $M_{\text{dow}}$: **Day-of-Week Effect**. Kirana footfall surges on Saturday ($1.32\times$) and Sunday ($1.38\times$). Impulse snack and tea products experience an additional weekend multiplier ($1.12\times$).
- $M_{\text{salary}}$: **Monthly Payday Cycle**. In Indian residential neighborhoods, the 1st to 7th of every month sees bulk grocery purchasing ("ration stocking"). Staple categories ($C001, C006$) experience a $1.42\times$ surge. Towards month-end (22nd–31st), bulk purchases decline ($0.88\times$), while single-use micro-packs (shampoo sachets $P016$) increase ($1.18\times$) due to daily cash-flow budgeting.
- $M_{\text{fest}}$: **Indian Festival Calendar**. Explicit date ranges for major Indian festivals across 2024–2026:
  - *Diwali*: Multiplier up to $2.2\times$ for sugar and edible oils, $2.3\times$ for cleaning products (deep cleaning tradition).
  - *Holi*: Multipliers up to $1.9\times$ for edible oils, snacks, and sugar.
  - *Makar Sankranti & Pongal*: Spikes for sugar, dal, and rice ($1.45\times$ to $1.8\times$).
  - *Eid-ul-Fitr*: Spikes for milk pouch, sugar, and vermicelli/rice ($1.6\times$ to $1.7\times$).
  - *Ganesh Chaturthi & Raksha Bandhan*: Spikes for poha, sugar, and sweets preparation.
- $M_{\text{season}}$: **Weather & Climate Seasonality**.
  - *Monsoon (June–August)*: Higher demand for tea ($P011$, $+30\%$) and instant noodles ($P013$, $+30\%$) during rainy spells ("chai & maggi").
  - *Winter (Nov–Jan)*: Higher demand for hot tea ($+22\%$) and whole/ground spices.
  - *Summer (April–May)*: High turnover for fresh milk.
- $M_{\text{price}}$: **Price Elasticity & Promotions**. Periodic promotional campaigns (3 to 6 days duration) with $5\%$ to $12\%$ discounts generate a price-elasticity demand lift of $1.35\times$.

#### 2. Stochastic Demand Sampling with Overdispersion
Customer purchases do not follow a restrictive Poisson distribution where $\text{Var}(X) = \mathbb{E}[X]$. Real retail demand exhibits **overdispersion** ($\text{Var}(X) > \mathbb{E}[X]$). Latent demand is sampled from a **Negative Binomial distribution**:

$$D_{i,t} \sim \text{NegBinomial}(r, p)$$

$$\text{with } p = \frac{\mu}{\sigma^2}, \quad r = \frac{\mu^2}{\sigma^2 - \mu}, \quad \sigma^2 = \mu \times \delta_i$$

Where $\delta_i \in [1.15, 1.35]$ is the product-specific dispersion parameter.

#### 3. Closed-Loop Inventory Simulation & Censored Demand
For each product across all 730 consecutive simulation days:
1. Arriving replenishment orders are received into opening stock.
2. Handling/perishability damage is sampled: $\text{damaged\_units} \sim \text{Binomial}$.
3. Available stock for trading is determined:
   $$\text{stock\_available} = \max(0, \text{opening\_stock} + \text{units\_received} - \text{damaged\_units})$$
4. **Censored Sales vs. Latent Demand Resolution**:
   - If $D_{i,t} \le \text{stock\_available}$:
     $$\text{units\_sold} = D_{i,t}, \quad \text{closing\_stock} = \text{stock\_available} - \text{units\_sold}, \quad \text{stockout\_flag} = 0$$
   - If $D_{i,t} > \text{stock\_available}$:
     $$\text{units\_sold} = \text{stock\_available}, \quad \text{closing\_stock} = 0, \quad \text{stockout\_flag} = 1$$
5. **Replenishment Trigger**: When effective inventory ($\text{closing\_stock} + \text{on\_order}$) drops to or below $\text{reorder\_point}$, a purchase order of $\text{reorder\_quantity}$ is dispatched with lead time $L_i$ (plus occasional 1-day distributor logistics delay).

---

## 🔬 Dataset Verification & Statistical Summary

Running the generator script (`src/generate_datasets.py`) verified the dataset against strict mathematical and relational constraints:

```
=== KiranaStock Synthetic Dataset Generation ===
[OK] Saved Categories Master: data/raw/categories.csv (6 rows)
[OK] Saved Products Master:   data/raw/products.csv (20 rows)
Total simulation days:        730 (2024-11-21 to 2026-11-20)
[OK] Saved Daily Sales:       data/raw/daily_sales.csv (14,600 rows)
[OK] Saved Inventory Records: data/inventory/inventory_records.csv (14,600 rows)

--- Rigorous Mathematical and Relational Verifications ---
1. Inventory conservation equation satisfied for 100% of rows: True
2. Day-to-day stock continuity opening(t) == closing(t-1) verified: True
3. Sales and inventory units_sold match exactly across all 14,600 pairs: True
4. Zero-sales days captured: 933 rows (6.39%)
5. Stockout events captured: 3,238 events (22.18%)
6. Promotion active days: 794 events (5.44%)
```

### Product Sales & Stockout Profile

| SKU | Product Name | Velocity Class | Mean Sales/Day | Max Sales/Day | Zero-Sales Days (%) | Stockout Rate (%) | Mean Closing Stock |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **P001** | Raw Rice (1 kg) | Fast | 15.31 | 50 | 1.37% | 13.97% | 24.69 |
| **P002** | Whole Wheat Atta (5 kg) | Medium | 6.58 | 19 | 1.64% | 10.55% | 13.81 |
| **P003** | Toor Dal (1 kg) | Fast | 10.38 | 32 | 1.64% | 12.05% | 19.62 |
| **P004** | Poha (500 g) | Medium | 6.60 | 20 | 9.18% | 23.56% | 12.15 |
| **P005** | Sunflower Oil (1 L) | Fast | 12.52 | 39 | 1.37% | 12.60% | 22.01 |
| **P006** | White Sugar (1 kg) | Fast | 17.83 | 56 | 0.82% | 11.51% | 32.35 |
| **P007** | Milk Pouch (500 ml) | Fast (Perishable) | 44.54 | 70 | 0.00% | 51.92% | 6.77 |
| **P008** | Turmeric Powder (100 g) | Medium | 4.84 | 18 | 11.78% | 25.75% | 8.45 |
| **P009** | Red Chilli Powder (100 g)| Medium | 5.57 | 16 | 9.18% | 23.01% | 10.70 |
| **P010** | Cumin Seeds (100 g) | Slow | 2.98 | 13 | 22.33% | 28.90% | 6.97 |
| **P011** | Tea Leaves (250 g) | Fast | 12.52 | 42 | 2.05% | 20.41% | 16.11 |
| **P012** | Glucose Biscuits (100 g)| Fast | 36.33 | 115 | 4.25% | 25.75% | 38.63 |
| **P013** | Instant Noodles (70 g) | Fast | 23.22 | 65 | 2.33% | 20.00% | 27.87 |
| **P014** | Potato Chips (52 g) | Fast | 18.24 | 60 | 4.52% | 27.26% | 18.62 |
| **P015** | Bathing Soap (100 g) | Medium | 7.48 | 26 | 7.26% | 22.19% | 14.30 |
| **P016** | Shampoo Sachet (6 ml) | Fast | 40.95 | 93 | 1.64% | 20.68% | 53.75 |
| **P017** | Toothpaste (100 g) | Slow | 4.45 | 15 | 8.49% | 18.08% | 9.66 |
| **P018** | Detergent Powder (1 kg) | Medium | 6.51 | 26 | 8.77% | 22.19% | 12.79 |
| **P019** | Dishwashing Bar (200 g) | Fast | 16.68 | 60 | 3.01% | 20.96% | 21.54 |
| **P020** | Floor Cleaner (500 ml) | Slow | 2.98 | 14 | 26.16% | 32.19% | 6.51 |

---

## 🚀 How to Reproduce & Regenerate Data

To re-run the synthetic dataset generator from scratch:

```bash
# From repository root
python src/generate_datasets.py
```

To run exploratory data analysis:
```bash
jupyter notebook notebooks/01_dataset_eda_and_validation.ipynb
```

---

## 🔮 Next Steps: Phase 2 Roadmap

1. **Feature Engineering**:
   - Lagged sales features: $t-1, t-2, t-7, t-14, t-30$.
   - Rolling statistics: 7-day, 14-day, 30-day rolling mean, standard deviation, min, max.
   - Calendar features: Day of week, day of month, month, weekend indicator, festival proximity flags.
   - Price & promotion indicators: Discount percentage, promotion active.
   - Demand un-censoring adjustment for historical stockout days.
2. **Model Training & Benchmarking**:
   - Baseline models: 7-day moving average, Naive previous week baseline.
   - Machine Learning models: Random Forest Regressor, XGBoost Regressor, LightGBM.
   - Evaluation metrics: MAE, RMSE, WAPE (Weighted Absolute Percentage Error), and Pinball Loss for quantile inventory buffers.
3. **Inventory Reorder Optimization**:
   - Predicted 7-day demand vs current closing stock to dynamically recommend purchase orders and avoid overstocking slow-movers or stockouts of fast-movers.
