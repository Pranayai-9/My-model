import json

nb = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# KiranaStock — Phase 1: Dataset Validation & Exploratory Data Analysis\n",
                "\n",
                "This notebook validates data integrity, confirms the inventory balance conservation equation,\n",
                "and analyzes historical retail sales patterns across the 20 products and 6 categories."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "\n",
                "# Load all core datasets\n",
                "categories = pd.read_csv('../data/raw/categories.csv')\n",
                "products = pd.read_csv('../data/raw/products.csv')\n",
                "sales = pd.read_csv('../data/raw/daily_sales.csv')\n",
                "inventory = pd.read_csv('../data/inventory/inventory_records.csv')\n",
                "\n",
                "print(f'Categories Shape:    {categories.shape}')\n",
                "print(f'Products Master Shape: {products.shape}')\n",
                "print(f'Daily Sales Shape:    {sales.shape}')\n",
                "print(f'Inventory Shape:      {inventory.shape}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Schema and Missing Value Inspection"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print('--- Daily Sales Null Values ---')\n",
                "print(sales.isnull().sum())\n",
                "print('\\n--- Inventory Records Null Values ---')\n",
                "print(inventory.isnull().sum())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Rigorous Inventory Conservation Check\n",
                "$$\\text{Closing Stock} = \\text{Opening Stock} + \\text{Units Received} - \\text{Units Sold} - \\text{Damaged Units}$$\n",
                "Every single row must strictly obey this identity."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "expected_closing = inventory['opening_stock'] + inventory['units_received'] - inventory['units_sold'] - inventory['damaged_units']\n",
                "conservation_passed = (inventory['closing_stock'] == expected_closing).all()\n",
                "print(f'Inventory conservation holds 100% across all rows: {conservation_passed}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Stock Continuity Check\n",
                "For each product, $\\text{Opening Stock}(t) = \\text{Closing Stock}(t-1)$."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "inv_sorted = inventory.sort_values(['product_id', 'date']).reset_index(drop=True)\n",
                "inv_sorted['prev_closing'] = inv_sorted.groupby('product_id')['closing_stock'].shift(1)\n",
                "continuity_check = (\n",
                "    inv_sorted['prev_closing'].isna() | (inv_sorted['opening_stock'] == inv_sorted['prev_closing'])\n",
                ").all()\n",
                "print(f'Day-to-day stock continuity holds for all records: {continuity_check}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Product Sales, Zero-Sales Days & Stockout Analysis"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "merged = pd.merge(sales, inventory, on=['date', 'product_id'], suffixes=('', '_dup'))\n",
                "merged = pd.merge(merged, products[['product_id', 'product_name', 'category_name', 'velocity_class']], on='product_id')\n",
                "\n",
                "product_summary = merged.groupby(['product_id', 'product_name', 'velocity_class']).agg(\n",
                "    mean_sales=('units_sold', 'mean'),\n",
                "    max_sales=('units_sold', 'max'),\n",
                "    zero_sales_days=('units_sold', lambda x: (x == 0).sum()),\n",
                "    zero_sales_pct=('units_sold', lambda x: round((x == 0).mean() * 100, 2)),\n",
                "    stockout_days=('stockout_flag', 'sum'),\n",
                "    stockout_pct=('stockout_flag', lambda x: round((x == 1).mean() * 100, 2)),\n",
                "    mean_closing_stock=('closing_stock', 'mean')\n",
                ").reset_index()\n",
                "\n",
                "product_summary"
            ]
        }
    ],
    "metadata": {
        "language_info": {"name": "python"}
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

with open("notebooks/01_dataset_eda_and_validation.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Notebook 01_dataset_eda_and_validation.ipynb created successfully.")
