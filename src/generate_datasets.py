"""
KiranaStock - Synthetic Dataset Generator
Simulates realistic historical daily sales and inventory dynamics for 20 retail products
across 6 categories over a 2-year horizon (730 days: 2024-11-21 to 2026-11-20).

Key realistic retail effects modeled:
1. Day-of-week seasonality (weekend grocery footfall spikes)
2. Monthly salary cycle (1st to 7th staple restock surges)
3. Indian festival calendar (Diwali, Holi, Makar Sankranti, Eid, Raksha Bandhan, Ganesh Chaturthi)
4. Weather/seasonal variations (Monsoon tea/snacks boost, summer dairy/beverages)
5. Promotion schedules and price elasticity
6. Realistic inventory replenishment policies (reorder points, lead times, batch orders)
7. Stockout dynamics (censored demand when available stock < latent demand)
8. Product shrinkage & damage (perishability for milk, carton handling damage)
"""

import os
import math
import random
import datetime
import numpy as np
import pandas as pd

# Set fixed random seed for strict reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_INV_DIR = os.path.join(BASE_DIR, "data", "inventory")
DATA_PROC_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(DATA_RAW_DIR, exist_ok=True)
os.makedirs(DATA_INV_DIR, exist_ok=True)
os.makedirs(DATA_PROC_DIR, exist_ok=True)

# 1. CATEGORIES MASTER
CATEGORIES = [
    {
        "category_id": "C001",
        "category_name": "Grains, Flours & Pulses",
        "description": "Essential dietary staples including raw rice, wheat flour, lentils, and beaten rice.",
        "avg_shelf_life_days": 180,
        "margin_percentage": 14.5,
        "storage_requirement": "Ambient Dry Storage"
    },
    {
        "category_id": "C002",
        "category_name": "Oils, Dairy & Sweeteners",
        "description": "Cooking oils, dairy milk pouches, and refined sweeteners.",
        "avg_shelf_life_days": 60,
        "margin_percentage": 10.2,
        "storage_requirement": "Mixed (Chilled for dairy, Ambient for oils/sugar)"
    },
    {
        "category_id": "C003",
        "category_name": "Spices & Condiments",
        "description": "Ground spices and whole seeds used daily in Indian cooking.",
        "avg_shelf_life_days": 365,
        "margin_percentage": 22.0,
        "storage_requirement": "Ambient Dry Storage (Airtight)"
    },
    {
        "category_id": "C004",
        "category_name": "Packaged Foods & Beverages",
        "description": "Tea, biscuits, instant noodles, and packaged snacks for quick consumption.",
        "avg_shelf_life_days": 120,
        "margin_percentage": 16.5,
        "storage_requirement": "Ambient Shelf Display"
    },
    {
        "category_id": "C005",
        "category_name": "Personal Care & Hygiene",
        "description": "Personal hygiene essentials such as toilet soaps, shampoo sachets, and toothpaste.",
        "avg_shelf_life_days": 540,
        "margin_percentage": 18.0,
        "storage_requirement": "Ambient Shelf Display"
    },
    {
        "category_id": "C006",
        "category_name": "Household Cleaning & Essentials",
        "description": "Cleaning agents including laundry detergent, dishwashing bars, and surface disinfectants.",
        "avg_shelf_life_days": 365,
        "margin_percentage": 17.5,
        "storage_requirement": "Ambient Storage (Away from food items)"
    }
]

# 2. PRODUCTS MASTER (20 SKUs)
PRODUCTS = [
    # C001 - Grains, Flours & Pulses
    {
        "product_id": "P001",
        "product_name": "Raw Rice (1 kg)",
        "category_id": "C001",
        "category_name": "Grains, Flours & Pulses",
        "sub_category": "Rice & Grains",
        "brand_tier": "Popular",
        "unit_of_measure": "kg",
        "cost_price": 54.00,
        "base_mrp": 65.00,
        "base_selling_price": 63.00,
        "margin_pct": 16.67,
        "shelf_life_days": 180,
        "storage_type": "Ambient Dry",
        "velocity_class": "Fast",
        "base_daily_demand": 14.0,
        "demand_dispersion": 1.20,
        "reorder_point": 25,
        "reorder_quantity": 60,
        "lead_time_days": 2,
        "damage_rate": 0.008
    },
    {
        "product_id": "P002",
        "product_name": "Whole Wheat Atta (5 kg)",
        "category_id": "C001",
        "category_name": "Grains, Flours & Pulses",
        "sub_category": "Flours",
        "brand_tier": "Popular",
        "unit_of_measure": "bag (5kg)",
        "cost_price": 208.00,
        "base_mrp": 240.00,
        "base_selling_price": 235.00,
        "margin_pct": 12.98,
        "shelf_life_days": 90,
        "storage_type": "Ambient Dry",
        "velocity_class": "Medium",
        "base_daily_demand": 6.2,
        "demand_dispersion": 1.15,
        "reorder_point": 12,
        "reorder_quantity": 30,
        "lead_time_days": 2,
        "damage_rate": 0.006
    },
    {
        "product_id": "P003",
        "product_name": "Toor Dal (1 kg)",
        "category_id": "C001",
        "category_name": "Grains, Flours & Pulses",
        "sub_category": "Pulses",
        "brand_tier": "Mass",
        "unit_of_measure": "kg",
        "cost_price": 138.00,
        "base_mrp": 160.00,
        "base_selling_price": 155.00,
        "margin_pct": 12.32,
        "shelf_life_days": 180,
        "storage_type": "Ambient Dry",
        "velocity_class": "Fast",
        "base_daily_demand": 9.5,
        "demand_dispersion": 1.15,
        "reorder_point": 18,
        "reorder_quantity": 45,
        "lead_time_days": 2,
        "damage_rate": 0.007
    },
    {
        "product_id": "P004",
        "product_name": "Poha (500 g)",
        "category_id": "C001",
        "category_name": "Grains, Flours & Pulses",
        "sub_category": "Breakfast Staples",
        "brand_tier": "Mass",
        "unit_of_measure": "packet (500g)",
        "cost_price": 36.00,
        "base_mrp": 45.00,
        "base_selling_price": 44.00,
        "margin_pct": 22.22,
        "shelf_life_days": 120,
        "storage_type": "Ambient Dry",
        "velocity_class": "Medium",
        "base_daily_demand": 7.0,
        "demand_dispersion": 1.25,
        "reorder_point": 14,
        "reorder_quantity": 35,
        "lead_time_days": 3,
        "damage_rate": 0.005
    },

    # C002 - Oils, Dairy & Sweeteners
    {
        "product_id": "P005",
        "product_name": "Sunflower Oil (1 L)",
        "category_id": "C002",
        "category_name": "Oils, Dairy & Sweeteners",
        "sub_category": "Edible Oils",
        "brand_tier": "Popular",
        "unit_of_measure": "pouch (1L)",
        "cost_price": 126.00,
        "base_mrp": 145.00,
        "base_selling_price": 140.00,
        "margin_pct": 11.11,
        "shelf_life_days": 180,
        "storage_type": "Ambient Dry",
        "velocity_class": "Fast",
        "base_daily_demand": 11.0,
        "demand_dispersion": 1.30,
        "reorder_point": 22,
        "reorder_quantity": 50,
        "lead_time_days": 2,
        "damage_rate": 0.012
    },
    {
        "product_id": "P006",
        "product_name": "White Sugar (1 kg)",
        "category_id": "C002",
        "category_name": "Oils, Dairy & Sweeteners",
        "sub_category": "Sweeteners",
        "brand_tier": "Mass",
        "unit_of_measure": "kg",
        "cost_price": 40.50,
        "base_mrp": 48.00,
        "base_selling_price": 46.00,
        "margin_pct": 13.58,
        "shelf_life_days": 365,
        "storage_type": "Ambient Dry",
        "velocity_class": "Fast",
        "base_daily_demand": 15.5,
        "demand_dispersion": 1.35,
        "reorder_point": 30,
        "reorder_quantity": 75,
        "lead_time_days": 2,
        "damage_rate": 0.008
    },
    {
        "product_id": "P007",
        "product_name": "Milk Pouch (500 ml)",
        "category_id": "C002",
        "category_name": "Oils, Dairy & Sweeteners",
        "sub_category": "Dairy",
        "brand_tier": "Popular",
        "unit_of_measure": "pouch (500ml)",
        "cost_price": 27.50,
        "base_mrp": 30.00,
        "base_selling_price": 30.00,
        "margin_pct": 9.09,
        "shelf_life_days": 2,
        "storage_type": "Refrigerated",
        "velocity_class": "Fast",
        "base_daily_demand": 46.0,
        "demand_dispersion": 1.15,
        "reorder_point": 15,
        "reorder_quantity": 55,
        "lead_time_days": 1,
        "damage_rate": 0.025
    },

    # C003 - Spices & Condiments
    {
        "product_id": "P008",
        "product_name": "Turmeric Powder (100 g)",
        "category_id": "C003",
        "category_name": "Spices & Condiments",
        "sub_category": "Ground Spices",
        "brand_tier": "Popular",
        "unit_of_measure": "packet (100g)",
        "cost_price": 26.00,
        "base_mrp": 35.00,
        "base_selling_price": 34.00,
        "margin_pct": 30.77,
        "shelf_life_days": 365,
        "storage_type": "Ambient Dry",
        "velocity_class": "Medium",
        "base_daily_demand": 5.2,
        "demand_dispersion": 1.20,
        "reorder_point": 10,
        "reorder_quantity": 25,
        "lead_time_days": 3,
        "damage_rate": 0.004
    },
    {
        "product_id": "P009",
        "product_name": "Red Chilli Powder (100 g)",
        "category_id": "C003",
        "category_name": "Spices & Condiments",
        "sub_category": "Ground Spices",
        "brand_tier": "Popular",
        "unit_of_measure": "packet (100g)",
        "cost_price": 34.00,
        "base_mrp": 45.00,
        "base_selling_price": 44.00,
        "margin_pct": 29.41,
        "shelf_life_days": 365,
        "storage_type": "Ambient Dry",
        "velocity_class": "Medium",
        "base_daily_demand": 5.8,
        "demand_dispersion": 1.22,
        "reorder_point": 12,
        "reorder_quantity": 30,
        "lead_time_days": 3,
        "damage_rate": 0.004
    },
    {
        "product_id": "P010",
        "product_name": "Cumin Seeds / Jeera (100 g)",
        "category_id": "C003",
        "category_name": "Spices & Condiments",
        "sub_category": "Whole Spices",
        "brand_tier": "Mass",
        "unit_of_measure": "packet (100g)",
        "cost_price": 48.00,
        "base_mrp": 65.00,
        "base_selling_price": 62.00,
        "margin_pct": 29.17,
        "shelf_life_days": 365,
        "storage_type": "Ambient Dry",
        "velocity_class": "Slow",
        "base_daily_demand": 3.6,
        "demand_dispersion": 1.35,
        "reorder_point": 8,
        "reorder_quantity": 20,
        "lead_time_days": 4,
        "damage_rate": 0.003
    },

    # C004 - Packaged Foods & Beverages
    {
        "product_id": "P011",
        "product_name": "Tea Leaves (250 g)",
        "category_id": "C004",
        "category_name": "Packaged Foods & Beverages",
        "sub_category": "Hot Beverages",
        "brand_tier": "Popular",
        "unit_of_measure": "carton (250g)",
        "cost_price": 98.00,
        "base_mrp": 120.00,
        "base_selling_price": 118.00,
        "margin_pct": 20.41,
        "shelf_life_days": 365,
        "storage_type": "Ambient Dry",
        "velocity_class": "Fast",
        "base_daily_demand": 10.5,
        "demand_dispersion": 1.20,
        "reorder_point": 18,
        "reorder_quantity": 45,
        "lead_time_days": 2,
        "damage_rate": 0.005
    },
    {
        "product_id": "P012",
        "product_name": "Glucose Biscuits (100 g)",
        "category_id": "C004",
        "category_name": "Packaged Foods & Beverages",
        "sub_category": "Biscuits & Cookies",
        "brand_tier": "Mass",
        "unit_of_measure": "packet (100g)",
        "cost_price": 8.40,
        "base_mrp": 10.00,
        "base_selling_price": 10.00,
        "margin_pct": 19.05,
        "shelf_life_days": 180,
        "storage_type": "Ambient Dry",
        "velocity_class": "Fast",
        "base_daily_demand": 34.0,
        "demand_dispersion": 1.25,
        "reorder_point": 50,
        "reorder_quantity": 120,
        "lead_time_days": 2,
        "damage_rate": 0.015
    },
    {
        "product_id": "P013",
        "product_name": "Instant Noodles (70 g)",
        "category_id": "C004",
        "category_name": "Packaged Foods & Beverages",
        "sub_category": "Ready-to-Cook",
        "brand_tier": "Popular",
        "unit_of_measure": "packet (70g)",
        "cost_price": 11.80,
        "base_mrp": 14.00,
        "base_selling_price": 14.00,
        "margin_pct": 18.64,
        "shelf_life_days": 240,
        "storage_type": "Ambient Dry",
        "velocity_class": "Fast",
        "base_daily_demand": 21.0,
        "demand_dispersion": 1.30,
        "reorder_point": 35,
        "reorder_quantity": 80,
        "lead_time_days": 2,
        "damage_rate": 0.010
    },
    {
        "product_id": "P014",
        "product_name": "Potato Chips (52 g)",
        "category_id": "C004",
        "category_name": "Packaged Foods & Beverages",
        "sub_category": "Salty Snacks",
        "brand_tier": "Popular",
        "unit_of_measure": "bag (52g)",
        "cost_price": 16.50,
        "base_mrp": 20.00,
        "base_selling_price": 20.00,
        "margin_pct": 21.21,
        "shelf_life_days": 120,
        "storage_type": "Ambient Dry",
        "velocity_class": "Fast",
        "base_daily_demand": 17.5,
        "demand_dispersion": 1.35,
        "reorder_point": 25,
        "reorder_quantity": 60,
        "lead_time_days": 2,
        "damage_rate": 0.015
    },

    # C005 - Personal Care & Hygiene
    {
        "product_id": "P015",
        "product_name": "Bathing Soap (100 g)",
        "category_id": "C005",
        "category_name": "Personal Care & Hygiene",
        "sub_category": "Soaps & Body Wash",
        "brand_tier": "Popular",
        "unit_of_measure": "bar (100g)",
        "cost_price": 32.50,
        "base_mrp": 40.00,
        "base_selling_price": 38.00,
        "margin_pct": 16.92,
        "shelf_life_days": 730,
        "storage_type": "Ambient Dry",
        "velocity_class": "Medium",
        "base_daily_demand": 8.0,
        "demand_dispersion": 1.15,
        "reorder_point": 16,
        "reorder_quantity": 40,
        "lead_time_days": 3,
        "damage_rate": 0.003
    },
    {
        "product_id": "P016",
        "product_name": "Shampoo Sachet (6 ml)",
        "category_id": "C005",
        "category_name": "Personal Care & Hygiene",
        "sub_category": "Hair Care",
        "brand_tier": "Mass",
        "unit_of_measure": "sachet (6ml)",
        "cost_price": 2.20,
        "base_mrp": 3.00,
        "base_selling_price": 3.00,
        "margin_pct": 36.36,
        "shelf_life_days": 730,
        "storage_type": "Ambient Dry",
        "velocity_class": "Fast",
        "base_daily_demand": 38.0,
        "demand_dispersion": 1.20,
        "reorder_point": 60,
        "reorder_quantity": 150,
        "lead_time_days": 2,
        "damage_rate": 0.010
    },
    {
        "product_id": "P017",
        "product_name": "Toothpaste (100 g)",
        "category_id": "C005",
        "category_name": "Personal Care & Hygiene",
        "sub_category": "Oral Care",
        "brand_tier": "Popular",
        "unit_of_measure": "tube (100g)",
        "cost_price": 48.00,
        "base_mrp": 60.00,
        "base_selling_price": 58.00,
        "margin_pct": 20.83,
        "shelf_life_days": 730,
        "storage_type": "Ambient Dry",
        "velocity_class": "Slow",
        "base_daily_demand": 4.5,
        "demand_dispersion": 1.25,
        "reorder_point": 10,
        "reorder_quantity": 25,
        "lead_time_days": 3,
        "damage_rate": 0.004
    },

    # C006 - Household Cleaning & Essentials
    {
        "product_id": "P018",
        "product_name": "Detergent Powder (1 kg)",
        "category_id": "C006",
        "category_name": "Household Cleaning & Essentials",
        "sub_category": "Laundry",
        "brand_tier": "Popular",
        "unit_of_measure": "packet (1kg)",
        "cost_price": 90.00,
        "base_mrp": 110.00,
        "base_selling_price": 105.00,
        "margin_pct": 16.67,
        "shelf_life_days": 730,
        "storage_type": "Ambient Dry",
        "velocity_class": "Medium",
        "base_daily_demand": 6.8,
        "demand_dispersion": 1.20,
        "reorder_point": 14,
        "reorder_quantity": 35,
        "lead_time_days": 3,
        "damage_rate": 0.006
    },
    {
        "product_id": "P019",
        "product_name": "Dishwashing Bar (200 g)",
        "category_id": "C006",
        "category_name": "Household Cleaning & Essentials",
        "sub_category": "Dish Care",
        "brand_tier": "Mass",
        "unit_of_measure": "bar (200g)",
        "cost_price": 16.00,
        "base_mrp": 20.00,
        "base_selling_price": 20.00,
        "margin_pct": 25.00,
        "shelf_life_days": 730,
        "storage_type": "Ambient Dry",
        "velocity_class": "Fast",
        "base_daily_demand": 16.0,
        "demand_dispersion": 1.20,
        "reorder_point": 25,
        "reorder_quantity": 60,
        "lead_time_days": 2,
        "damage_rate": 0.008
    },
    {
        "product_id": "P020",
        "product_name": "Floor Cleaner (500 ml)",
        "category_id": "C006",
        "category_name": "Household Cleaning & Essentials",
        "sub_category": "Surface Care",
        "brand_tier": "Popular",
        "unit_of_measure": "bottle (500ml)",
        "cost_price": 76.00,
        "base_mrp": 95.00,
        "base_selling_price": 92.00,
        "margin_pct": 21.05,
        "shelf_life_days": 730,
        "storage_type": "Ambient Dry",
        "velocity_class": "Slow",
        "base_daily_demand": 3.8,
        "demand_dispersion": 1.30,
        "reorder_point": 8,
        "reorder_quantity": 20,
        "lead_time_days": 4,
        "damage_rate": 0.005
    }
]

# 3. FESTIVAL CALENDAR (2024 to 2026)
# Each festival maps date ranges to category/product demand multipliers
FESTIVAL_EVENTS = [
    # 2024
    {"name": "Diwali 2024", "start": "2024-10-28", "end": "2024-11-04",
     "boost": {"C001": 1.4, "C002": 2.1, "C003": 1.5, "C004": 1.7, "C005": 1.3, "C006": 2.2}},
    {"name": "Christmas/NewYear 2024", "start": "2024-12-24", "end": "2025-01-01",
     "boost": {"C004": 1.45, "C002": 1.25}},
    
    # 2025
    {"name": "Makar Sankranti 2025", "start": "2025-01-13", "end": "2025-01-16",
     "boost": {"C001": 1.45, "C002": 1.5, "P006": 1.8}},
    {"name": "Holi 2025", "start": "2025-03-12", "end": "2025-03-16",
     "boost": {"C002": 1.8, "C004": 1.6, "C006": 1.5, "P005": 1.9, "P006": 1.8}},
    {"name": "Eid-ul-Fitr 2025", "start": "2025-03-29", "end": "2025-04-01",
     "boost": {"C001": 1.3, "C002": 1.7, "C003": 1.4, "P007": 1.6, "P006": 1.7}},
    {"name": "Raksha Bandhan 2025", "start": "2025-08-08", "end": "2025-08-10",
     "boost": {"C002": 1.6, "C004": 1.5, "P006": 1.7}},
    {"name": "Ganesh Chaturthi 2025", "start": "2025-08-26", "end": "2025-08-30",
     "boost": {"C001": 1.4, "C002": 1.6, "P004": 1.7, "P006": 1.8}},
    {"name": "Navratri & Dussehra 2025", "start": "2025-09-22", "end": "2025-10-03",
     "boost": {"C001": 1.35, "C002": 1.5, "C004": 1.4, "C006": 1.4}},
    {"name": "Diwali 2025", "start": "2025-10-17", "end": "2025-10-24",
     "boost": {"C001": 1.45, "C002": 2.2, "C003": 1.55, "C004": 1.75, "C005": 1.35, "C006": 2.3}},
    {"name": "Christmas/NewYear 2025", "start": "2025-12-24", "end": "2026-01-01",
     "boost": {"C004": 1.45, "C002": 1.25}},

    # 2026
    {"name": "Makar Sankranti 2026", "start": "2026-01-13", "end": "2026-01-16",
     "boost": {"C001": 1.45, "C002": 1.5, "P006": 1.8}},
    {"name": "Holi 2026", "start": "2026-03-02", "end": "2026-03-06",
     "boost": {"C002": 1.8, "C004": 1.6, "C006": 1.5, "P005": 1.9, "P006": 1.8}},
    {"name": "Eid-ul-Fitr 2026", "start": "2026-03-19", "end": "2026-03-22",
     "boost": {"C001": 1.3, "C002": 1.7, "C003": 1.4, "P007": 1.6, "P006": 1.7}},
    {"name": "Raksha Bandhan 2026", "start": "2026-08-27", "end": "2026-08-29",
     "boost": {"C002": 1.6, "C004": 1.5, "P006": 1.7}},
    {"name": "Ganesh Chaturthi 2026", "start": "2026-09-13", "end": "2026-09-17",
     "boost": {"C001": 1.4, "C002": 1.6, "P004": 1.7, "P006": 1.8}},
    {"name": "Navratri & Dussehra 2026", "start": "2026-10-10", "end": "2026-10-21",
     "boost": {"C001": 1.35, "C002": 1.5, "C004": 1.4, "C006": 1.4}},
    {"name": "Diwali 2026", "start": "2026-11-06", "end": "2026-11-13",
     "boost": {"C001": 1.45, "C002": 2.2, "C003": 1.55, "C004": 1.75, "C005": 1.35, "C006": 2.3}}
]

def get_festival_multiplier(dt_str, product):
    """Computes festival surge multiplier for a given date and product."""
    mult = 1.0
    cat_id = product["category_id"]
    p_id = product["product_id"]
    for fest in FESTIVAL_EVENTS:
        if fest["start"] <= dt_str <= fest["end"]:
            # Check specific product boost first
            if p_id in fest["boost"]:
                mult = max(mult, fest["boost"][p_id])
            elif cat_id in fest["boost"]:
                mult = max(mult, fest["boost"][cat_id])
    return mult

def get_day_of_week_multiplier(weekday, p_id):
    """
    Day of week footfall multiplier.
    Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4, Saturday=5, Sunday=6
    Kirana footfall peaks on weekends (Saturday & Sunday).
    """
    dow_map = {
        0: 0.90, # Mon
        1: 0.88, # Tue
        2: 0.92, # Wed
        3: 0.95, # Thu
        4: 1.08, # Fri
        5: 1.32, # Sat
        6: 1.38  # Sun
    }
    base = dow_map[weekday]
    # Impulse snacks and tea spike even higher on weekends
    if p_id in ["P011", "P012", "P013", "P014"]:
        if weekday in [5, 6]:
            base *= 1.12
    return base

def get_monthly_salary_multiplier(day_of_month, cat_id, p_id):
    """
    Indian monthly salary cycle (1st to 7th):
    Households purchase bulk monthly staples and cleaning supplies right after payday.
    Late month (21st onwards): Discretionary purchase drops, micro-packs (shampoo sachets) rise.
    """
    if 1 <= day_of_month <= 7:
        if cat_id in ["C001", "C006"]:
            return 1.42
        elif cat_id in ["C002", "C005"]:
            return 1.25
        else:
            return 1.10
    elif 22 <= day_of_month <= 31:
        if p_id == "P016": # Shampoo sachet
            return 1.18 # Sachet economy expands towards end of month
        elif cat_id in ["C001", "C006"]:
            return 0.88
        else:
            return 0.94
    return 1.0

def get_season_multiplier(month, p_id, cat_id):
    """
    Weather seasonality in India:
    - Monsoon (June-August): Maggi noodles, hot tea, biscuits surge.
    - Winter (Nov-Jan): Tea, spices, dal surge.
    - Summer (March-May): Higher daily milk turnover, light breakfast staples.
    """
    mult = 1.0
    # Monsoon (June - August)
    if month in [6, 7, 8]:
        if p_id in ["P011", "P013"]: # Tea, Instant Noodles
            mult *= 1.30
        elif p_id in ["P012", "P014"]: # Biscuits, Chips
            mult *= 1.20
    # Winter (Nov - Jan)
    elif month in [11, 12, 1]:
        if p_id in ["P011", "P008", "P009", "P010"]: # Tea & Spices
            mult *= 1.22
    # Summer (April - May)
    elif month in [4, 5]:
        if p_id == "P007": # Milk pouch
            mult *= 1.10
    return mult

def run_simulation(start_date, end_date):
    """
    Executes a discrete-event daily retail simulation over the specified date window.
    Strictly enforces:
    Closing Stock = Opening Stock + Units Received - Units Sold - Damaged Units
    Opening Stock(t) = Closing Stock(t-1)
    """
    cur_date = start_date
    dates = []
    while cur_date <= end_date:
        dates.append(cur_date)
        cur_date += datetime.timedelta(days=1)

    num_days = len(dates)
    print(f"Total simulation days: {num_days} ({dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')})")

    # Generate pre-scheduled promotional campaigns
    # E.g., 1-2 campaigns per month for select categories, lasting 3-6 days each
    promotions = {} # (p_id, dt_str) -> (is_promo, discount_pct)
    for p in PRODUCTS:
        p_id = p["product_id"]
        cat_id = p["category_id"]
        
        # Schedule periodic promotions (5-12 days per year on average)
        # Milk rarely has discounts; packaged snacks and staples have promotional runs
        if p_id == "P007": # Milk
            promo_rate = 0.01
        elif p["velocity_class"] == "Fast":
            promo_rate = 0.08
        else:
            promo_rate = 0.05
            
        d_idx = 0
        while d_idx < num_days:
            # Chance to initiate promo
            if random.random() < (promo_rate / 4.0):
                duration = random.randint(3, 6)
                discount = random.choice([5.0, 7.5, 10.0, 12.0])
                for off in range(duration):
                    if d_idx + off < num_days:
                        promotions[(p_id, dates[d_idx + off].strftime("%Y-%m-%d"))] = (1, discount)
                d_idx += duration + 10 # Cooldown period
            else:
                d_idx += 1

    daily_sales_rows = []
    inventory_rows = []

    # Initialize inventory states for each product
    # Realistic initial opening stock = 2.5 to 3.5 days of base demand
    inventory_state = {}
    pending_orders = {} # arrival_date_str -> list of (p_id, qty)

    for p in PRODUCTS:
        p_id = p["product_id"]
        init_stock = int(p["base_daily_demand"] * random.uniform(2.5, 3.8)) + p["reorder_point"]
        inventory_state[p_id] = {
            "current_stock": init_stock,
            "on_order": 0,
            "last_order_day": -99
        }

    # Simulate day by day across all products
    for day_idx, dt in enumerate(dates):
        dt_str = dt.strftime("%Y-%m-%d")
        weekday = dt.weekday()
        month = dt.month
        dom = dt.day

        # Step A: Process arriving replenishment shipments
        arriving_shipments = pending_orders.pop(dt_str, [])
        received_today = {p["product_id"]: 0 for p in PRODUCTS}
        for (arr_pid, arr_qty) in arriving_shipments:
            received_today[arr_pid] += arr_qty
            inventory_state[arr_pid]["on_order"] = max(0, inventory_state[arr_pid]["on_order"] - arr_qty)

        # Step B: For each product, compute opening stock, simulate demand, sales, shrinkage, closing stock
        for p in PRODUCTS:
            p_id = p["product_id"]
            cat_id = p["category_id"]
            state = inventory_state[p_id]

            opening_stock = state["current_stock"]
            units_received = received_today[p_id]

            # Promotion status
            is_promo, discount_pct = promotions.get((p_id, dt_str), (0, 0.0))
            
            # Selling price calculation
            base_sp = p["base_selling_price"]
            base_mrp = p["base_mrp"]
            if is_promo:
                unit_sp = round(base_mrp * (1.0 - discount_pct / 100.0), 2)
            else:
                # Small organic variation in everyday price within ₹1 of baseline
                unit_sp = base_sp

            # Compute latent customer demand using multi-factor multiplicative retail model
            dow_mult = get_day_of_week_multiplier(weekday, p_id)
            salary_mult = get_monthly_salary_multiplier(dom, cat_id, p_id)
            fest_mult = get_festival_multiplier(dt_str, p)
            season_mult = get_season_multiplier(month, p_id, cat_id)

            # Price elasticity effect: lower price during promotions stimulates demand
            price_elasticity = 1.35 if is_promo else 1.0

            # Combined expected demand mean
            lambda_demand = (
                p["base_daily_demand"] *
                dow_mult *
                salary_mult *
                fest_mult *
                season_mult *
                price_elasticity
            )

            # Draw latent demand from Negative Binomial distribution to capture retail overdispersion
            # Parametrization: mean = lambda_demand, variance = lambda_demand * dispersion
            dispersion = p["demand_dispersion"]
            variance = max(lambda_demand * dispersion, lambda_demand + 0.01)
            # NegBinomial parameter conversion: p_nb = mean / variance, r_nb = mean^2 / (variance - mean)
            p_nb = lambda_demand / variance
            r_nb = (lambda_demand ** 2) / (variance - lambda_demand)
            latent_demand = int(np.random.negative_binomial(r_nb, p_nb))
            if latent_demand < 0:
                latent_demand = 0

            # Compute damaged / expired units
            # Damaged items happen before or during daily handling
            damage_prob = p["damage_rate"]
            damaged_units = 0
            if (opening_stock + units_received) > 0 and random.random() < (damage_prob * 3.5):
                # Usually 1 unit, rarely 2 for fresh milk or glass/fragile items
                max_possible = min(3, opening_stock + units_received)
                damaged_units = random.randint(1, max_possible) if max_possible > 0 else 0

            # Stock available for sales
            stock_available = max(0, opening_stock + units_received - damaged_units)

            # Stockout and censored sales mechanics
            if latent_demand <= stock_available:
                units_sold = latent_demand
                closing_stock = stock_available - units_sold
                stockout_flag = 0
            else:
                # Demand exceeds available inventory! Stockout occurs
                units_sold = stock_available
                closing_stock = 0
                stockout_flag = 1 # Stock was exhausted during the day

            # Inventory balance check:
            # closing_stock = opening_stock + units_received - units_sold - damaged_units
            assert closing_stock == (opening_stock + units_received - units_sold - damaged_units), \
                f"Equation violated for {p_id} on {dt_str}!"

            # Update state for next day
            state["current_stock"] = closing_stock

            # Step C: Replenishment logic (Inventory ordering)
            # Reorder when effective inventory (closing stock + on_order) <= reorder_point
            effective_inv = closing_stock + state["on_order"]
            if effective_inv <= p["reorder_point"] and (day_idx - state["last_order_day"]) >= 1:
                # Order a batch
                batch_size = p["reorder_quantity"]
                # Daily milk is ordered daily for next morning delivery
                lead_time = p["lead_time_days"]
                # 5% chance of supplier delay (+1 day) simulating real kirana supply chain friction
                if p_id != "P007" and random.random() < 0.05:
                    lead_time += 1

                arr_date = dt + datetime.timedelta(days=lead_time)
                arr_date_str = arr_date.strftime("%Y-%m-%d")
                
                if arr_date_str not in pending_orders:
                    pending_orders[arr_date_str] = []
                pending_orders[arr_date_str].append((p_id, batch_size))
                state["on_order"] += batch_size
                state["last_order_day"] = day_idx

            # Record rows
            daily_sales_rows.append({
                "date": dt_str,
                "product_id": p_id,
                "units_sold": units_sold,
                "unit_selling_price": unit_sp,
                "discount_percentage": discount_pct,
                "promotion_flag": is_promo
            })

            inventory_rows.append({
                "date": dt_str,
                "product_id": p_id,
                "opening_stock": opening_stock,
                "units_received": units_received,
                "units_sold": units_sold,
                "damaged_units": damaged_units,
                "closing_stock": closing_stock,
                "stockout_flag": stockout_flag
            })

    return daily_sales_rows, inventory_rows

def main():
    print("=== KiranaStock Synthetic Dataset Generation ===")
    start_time = datetime.datetime.now()

    # 1. Save Categories Master CSV
    categories_df = pd.DataFrame(CATEGORIES)
    cat_path = os.path.join(DATA_RAW_DIR, "categories.csv")
    categories_df.to_csv(cat_path, index=False)
    print(f"[OK] Saved Categories Master: {cat_path} ({len(categories_df)} rows)")

    # 2. Save Products Master CSV
    # Select master columns for clean tabular presentation
    prod_master_cols = [
        "product_id", "product_name", "category_id", "category_name",
        "sub_category", "brand_tier", "unit_of_measure",
        "cost_price", "base_mrp", "base_selling_price", "margin_pct",
        "shelf_life_days", "storage_type", "velocity_class",
        "reorder_point", "reorder_quantity", "lead_time_days"
    ]
    products_df = pd.DataFrame(PRODUCTS)[prod_master_cols]
    prod_path = os.path.join(DATA_RAW_DIR, "products.csv")
    products_df.to_csv(prod_path, index=False)
    print(f"[OK] Saved Products Master: {prod_path} ({len(products_df)} rows)")

    # 3. Simulate 2 Years of Sales and Inventory Records (730 days)
    # 2024-11-21 to 2026-11-20
    start_date = datetime.date(2024, 11, 21)
    end_date = datetime.date(2026, 11, 20)

    sales_records, inventory_records = run_simulation(start_date, end_date)

    sales_df = pd.DataFrame(sales_records)
    inv_df = pd.DataFrame(inventory_records)

    sales_path = os.path.join(DATA_RAW_DIR, "daily_sales.csv")
    sales_df.to_csv(sales_path, index=False)
    print(f"[OK] Saved Daily Sales Dataset: {sales_path} ({len(sales_df)} rows)")

    inv_path = os.path.join(DATA_INV_DIR, "inventory_records.csv")
    inv_df.to_csv(inv_path, index=False)
    print(f"[OK] Saved Inventory Records: {inv_path} ({len(inv_df)} rows)")

    # 4. Rigorous Quality Verification
    print("\n--- Running Rigorous Mathematical and Relational Verifications ---")
    
    # Equation check
    balance_check = (inv_df["closing_stock"] == (
        inv_df["opening_stock"] + inv_df["units_received"] - inv_df["units_sold"] - inv_df["damaged_units"]
    )).all()
    print(f"1. Inventory conservation equation satisfied for 100% of rows: {balance_check}")
    assert balance_check, "Inventory conservation equation failure!"

    # Continuity check: opening_stock(t) == closing_stock(t-1)
    inv_df_sorted = inv_df.sort_values(["product_id", "date"]).reset_index(drop=True)
    inv_df_sorted["prev_closing"] = inv_df_sorted.groupby("product_id")["closing_stock"].shift(1)
    # Check rows where prev_closing is not NaN
    continuity_valid = (
        inv_df_sorted["prev_closing"].isna() | 
        (inv_df_sorted["opening_stock"] == inv_df_sorted["prev_closing"])
    ).all()
    print(f"2. Day-to-day stock continuity opening(t) == closing(t-1) verified: {continuity_valid}")
    assert continuity_valid, "Stock continuity violated!"

    # Sales vs Inventory consistency
    merged = pd.merge(sales_df, inv_df, on=["date", "product_id"], suffixes=("_sales", "_inv"))
    sales_match = (merged["units_sold_sales"] == merged["units_sold_inv"]).all()
    print(f"3. Sales and inventory units_sold match exactly across all 14,600 pairs: {sales_match}")
    assert sales_match, "Mismatch between sales and inventory units_sold!"

    # Check zero sales presence
    zero_sales_count = (sales_df["units_sold"] == 0).sum()
    zero_sales_pct = (zero_sales_count / len(sales_df)) * 100
    print(f"4. Zero-sales days captured: {zero_sales_count} rows ({zero_sales_pct:.2f}%)")
    assert zero_sales_count > 0, "Warning: Zero-sales days omitted!"

    # Stockout occurrences
    stockout_count = (inv_df["stockout_flag"] == 1).sum()
    stockout_pct = (stockout_count / len(inv_df)) * 100
    print(f"5. Stockout events captured: {stockout_count} events ({stockout_pct:.2f}%)")

    # Promotion occurrences
    promo_count = (sales_df["promotion_flag"] == 1).sum()
    promo_pct = (promo_count / len(sales_df)) * 100
    print(f"6. Promotion active days: {promo_count} events ({promo_pct:.2f}%)")

    duration = (datetime.datetime.now() - start_time).total_seconds()
    print(f"\n[DONE] Generation completed successfully in {duration:.2f} seconds!")

if __name__ == "__main__":
    main()
