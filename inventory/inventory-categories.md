# KiranaStock — Inventory & Product Categories Master

CATEGORY DEFINITION:
<img width="1024" height="572" alt="image" src="https://github.com/user-attachments/assets/456e1f81-79b4-42ea-8a11-67e36bfa44ec" />

This document defines the 6 inventory categories and 20 stock-keeping units (SKUs) selected for the **KiranaStock** retail demand forecasting engine.

---

## 1. Product Categories (6 Categories)

| Category ID | Category Name | Description | Avg Margin | Storage Requirement | Shelf Life |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **C001** | Grains, Flours & Pulses | Essential dietary staples including raw rice, whole wheat atta, toor dal, and beaten rice (poha). | ~14.5% | Ambient Dry Storage | 90–180 days |
| **C002** | Oils, Dairy & Sweeteners | High-frequency cooking mediums, fresh daily milk pouches, and refined table sugar. | ~10.2% | Mixed (Refrigerated for milk, Ambient for oils & sugar) | 2–365 days |
| **C003** | Spices & Condiments | Ground powders and whole aromatic seeds used daily in Indian cooking. | ~22.0% | Ambient Dry (Moisture-proof airtight) | 365 days |
| **C004** | Packaged Foods & Beverages | Packaged tea, glucose biscuits, instant noodles, and impulse potato chips. | ~16.5% | Ambient Shelf Display | 120–365 days |
| **C005** | Personal Care & Hygiene | Fast-moving personal care products: bathing soaps, single-use shampoo sachets, and toothpaste. | ~18.0% | Ambient Shelf Display | 540–730 days |
| **C006** | Household Cleaning & Essentials | Fabric care detergents, dishwashing bars, and surface floor disinfectant cleaners. | ~17.5% | Ambient Shelf (Segregated from food) | 365–730 days |

---

## 2. Product Catalog (20 SKUs)

### Category C001: Grains, Flours & Pulses
1. **P001 — Raw Rice (1 kg)**
   - *Sub-Category:* Rice & Grains
   - *Unit of Measure:* 1 kg bag
   - *Cost Price:* ₹54.00 | *Base MRP:* ₹65.00 | *Base Selling Price:* ₹63.00
   - *Velocity Class:* Fast-moving staple
   - *Shelf Life:* 180 days | *Storage:* Ambient Dry
   - *Lead Time:* 2 days | *Reorder Point:* 25 units | *Order Batch:* 60 units

2. **P002 — Whole Wheat Atta (5 kg)**
   - *Sub-Category:* Flours
   - *Unit of Measure:* 5 kg bag
   - *Cost Price:* ₹208.00 | *Base MRP:* ₹240.00 | *Base Selling Price:* ₹235.00
   - *Velocity Class:* Medium-moving staple (high bulk)
   - *Shelf Life:* 90 days | *Storage:* Ambient Dry
   - *Lead Time:* 2 days | *Reorder Point:* 12 units | *Order Batch:* 30 units

3. **P003 — Toor Dal (1 kg)**
   - *Sub-Category:* Pulses & Lentils
   - *Unit of Measure:* 1 kg pack
   - *Cost Price:* ₹138.00 | *Base MRP:* ₹160.00 | *Base Selling Price:* ₹155.00
   - *Velocity Class:* Fast-moving staple
   - *Shelf Life:* 180 days | *Storage:* Ambient Dry
   - *Lead Time:* 2 days | *Reorder Point:* 18 units | *Order Batch:* 45 units

4. **P004 — Poha (500 g)**
   - *Sub-Category:* Breakfast Staples
   - *Unit of Measure:* 500 g packet
   - *Cost Price:* ₹36.00 | *Base MRP:* ₹45.00 | *Base Selling Price:* ₹44.00
   - *Velocity Class:* Medium-moving breakfast staple
   - *Shelf Life:* 120 days | *Storage:* Ambient Dry
   - *Lead Time:* 3 days | *Reorder Point:* 14 units | *Order Batch:* 35 units

---

### Category C002: Oils, Dairy & Sweeteners
5. **P005 — Sunflower Oil (1 L)**
   - *Sub-Category:* Edible Cooking Oils
   - *Unit of Measure:* 1 L pouch
   - *Cost Price:* ₹126.00 | *Base MRP:* ₹145.00 | *Base Selling Price:* ₹140.00
   - *Velocity Class:* Fast-moving kitchen essential
   - *Shelf Life:* 180 days | *Storage:* Ambient Dry
   - *Lead Time:* 2 days | *Reorder Point:* 22 units | *Order Batch:* 50 units

6. **P006 — White Sugar (1 kg)**
   - *Sub-Category:* Sweeteners
   - *Unit of Measure:* 1 kg pack
   - *Cost Price:* ₹40.50 | *Base MRP:* ₹48.00 | *Base Selling Price:* ₹46.00
   - *Velocity Class:* Fast-moving staple
   - *Shelf Life:* 365 days | *Storage:* Moisture-free Dry Storage
   - *Lead Time:* 2 days | *Reorder Point:* 30 units | *Order Batch:* 75 units

7. **P007 — Milk Pouch (500 ml)**
   - *Sub-Category:* Fresh Dairy
   - *Unit of Measure:* 500 ml pouch
   - *Cost Price:* ₹27.50 | *Base MRP:* ₹30.00 | *Base Selling Price:* ₹30.00
   - *Velocity Class:* Ultra-fast perishable daily staple
   - *Shelf Life:* 2 days | *Storage:* Refrigerated / Cold Crate
   - *Lead Time:* 1 day (daily morning replenishment) | *Reorder Point:* 15 units | *Order Batch:* 55 units

---

### Category C003: Spices & Condiments
8. **P008 — Turmeric Powder (100 g)**
   - *Sub-Category:* Ground Spices
   - *Unit of Measure:* 100 g packet
   - *Cost Price:* ₹26.00 | *Base MRP:* ₹35.00 | *Base Selling Price:* ₹34.00
   - *Velocity Class:* Medium-moving spice
   - *Shelf Life:* 365 days | *Storage:* Ambient Dry
   - *Lead Time:* 3 days | *Reorder Point:* 10 units | *Order Batch:* 25 units

9. **P009 — Red Chilli Powder (100 g)**
   - *Sub-Category:* Ground Spices
   - *Unit of Measure:* 100 g packet
   - *Cost Price:* ₹34.00 | *Base MRP:* ₹45.00 | *Base Selling Price:* ₹44.00
   - *Velocity Class:* Medium-moving spice
   - *Shelf Life:* 365 days | *Storage:* Ambient Dry
   - *Lead Time:* 3 days | *Reorder Point:* 12 units | *Order Batch:* 30 units

10. **P010 — Cumin Seeds / Jeera (100 g)**
    - *Sub-Category:* Whole Spices
    - *Unit of Measure:* 100 g packet
    - *Cost Price:* ₹48.00 | *Base MRP:* ₹65.00 | *Base Selling Price:* ₹62.00
    - *Velocity Class:* Slow-moving high-value spice
    - *Shelf Life:* 365 days | *Storage:* Ambient Dry
    - *Lead Time:* 4 days | *Reorder Point:* 8 units | *Order Batch:* 20 units

---

### Category C004: Packaged Foods & Beverages
11. **P011 — Tea Leaves (250 g)**
    - *Sub-Category:* Hot Beverages
    - *Unit of Measure:* 250 g carton
    - *Cost Price:* ₹98.00 | *Base MRP:* ₹120.00 | *Base Selling Price:* ₹118.00
    - *Velocity Class:* Fast-moving beverage
    - *Shelf Life:* 365 days | *Storage:* Ambient Dry
    - *Lead Time:* 2 days | *Reorder Point:* 18 units | *Order Batch:* 45 units

12. **P012 — Glucose Biscuits (100 g)**
    - *Sub-Category:* Biscuits & Cookies
    - *Unit of Measure:* 100 g packet
    - *Cost Price:* ₹8.40 | *Base MRP:* ₹10.00 | *Base Selling Price:* ₹10.00
    - *Velocity Class:* Ultra-fast impulse purchase
    - *Shelf Life:* 180 days | *Storage:* Ambient Dry Display
    - *Lead Time:* 2 days | *Reorder Point:* 50 units | *Order Batch:* 120 units

13. **P013 — Instant Noodles (70 g)**
    - *Sub-Category:* Ready-to-Cook Foods
    - *Unit of Measure:* 70 g packet
    - *Cost Price:* ₹11.80 | *Base MRP:* ₹14.00 | *Base Selling Price:* ₹14.00
    - *Velocity Class:* Fast-moving snack
    - *Shelf Life:* 240 days | *Storage:* Ambient Dry Display
    - *Lead Time:* 2 days | *Reorder Point:* 35 units | *Order Batch:* 80 units

14. **P014 — Potato Chips (52 g)**
    - *Sub-Category:* Salty Snacks
    - *Unit of Measure:* 52 g pouch
    - *Cost Price:* ₹16.50 | *Base MRP:* ₹20.00 | *Base Selling Price:* ₹20.00
    - *Velocity Class:* Fast-moving impulse snack
    - *Shelf Life:* 120 days | *Storage:* Ambient Display (Hang-strips)
    - *Lead Time:* 2 days | *Reorder Point:* 25 units | *Order Batch:* 60 units

---

### Category C005: Personal Care & Hygiene
15. **P015 — Bathing Soap (100 g)**
    - *Sub-Category:* Soaps & Cleansers
    - *Unit of Measure:* 100 g bar
    - *Cost Price:* ₹32.50 | *Base MRP:* ₹40.00 | *Base Selling Price:* ₹38.00
    - *Velocity Class:* Medium-moving hygiene staple
    - *Shelf Life:* 730 days | *Storage:* Ambient Shelf
    - *Lead Time:* 3 days | *Reorder Point:* 16 units | *Order Batch:* 40 units

16. **P016 — Shampoo Sachet (6 ml)**
    - *Sub-Category:* Hair Care
    - *Unit of Measure:* 6 ml single-use sachet
    - *Cost Price:* ₹2.20 | *Base MRP:* ₹3.00 | *Base Selling Price:* ₹3.00
    - *Velocity Class:* Ultra-fast micro-ticket item (Indian sachet retail model)
    - *Shelf Life:* 730 days | *Storage:* Ambient Hanging Strips
    - *Lead Time:* 2 days | *Reorder Point:* 60 units | *Order Batch:* 150 units

17. **P017 — Toothpaste (100 g)**
    - *Sub-Category:* Oral Care
    - *Unit of Measure:* 100 g tube
    - *Cost Price:* ₹48.00 | *Base MRP:* ₹60.00 | *Base Selling Price:* ₹58.00
    - *Velocity Class:* Slow-to-medium moving essential
    - *Shelf Life:* 730 days | *Storage:* Ambient Shelf
    - *Lead Time:* 3 days | *Reorder Point:* 10 units | *Order Batch:* 25 units

---

### Category C006: Household Cleaning & Essentials
18. **P018 — Detergent Powder (1 kg)**
    - *Sub-Category:* Laundry Care
    - *Unit of Measure:* 1 kg pack
    - *Cost Price:* ₹90.00 | *Base MRP:* ₹110.00 | *Base Selling Price:* ₹105.00
    - *Velocity Class:* Medium-moving bulky essential
    - *Shelf Life:* 730 days | *Storage:* Ambient Dry (Away from food)
    - *Lead Time:* 3 days | *Reorder Point:* 14 units | *Order Batch:* 35 units

19. **P019 — Dishwashing Bar (200 g)**
    - *Sub-Category:* Dish Care
    - *Unit of Measure:* 200 g bar
    - *Cost Price:* ₹16.00 | *Base MRP:* ₹20.00 | *Base Selling Price:* ₹20.00
    - *Velocity Class:* Fast-moving daily kitchen essential
    - *Shelf Life:* 730 days | *Storage:* Ambient Dry
    - *Lead Time:* 2 days | *Reorder Point:* 25 units | *Order Batch:* 60 units

20. **P020 — Floor Cleaner (500 ml)**
    - *Sub-Category:* Surface Disinfectants
    - *Unit of Measure:* 500 ml bottle
    - *Cost Price:* ₹76.00 | *Base MRP:* ₹95.00 | *Base Selling Price:* ₹92.00
    - *Velocity Class:* Slow-moving cleaning chemical
    - *Shelf Life:* 730 days | *Storage:* Ambient Shelf (Chemical section)
    - *Lead Time:* 4 days | *Reorder Point:* 8 units | *Order Batch:* 20 units

---

## 3. Data Integration References
- Product Master CSV: `data/raw/products.csv`
- Category Master CSV: `data/raw/categories.csv`
- Daily Sales Dataset: `data/raw/daily_sales.csv`
- Daily Inventory Movements: `data/inventory/inventory_records.csv`
