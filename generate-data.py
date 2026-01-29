#!/usr/bin/env python3
import pandas as pd
import json
import sys

# قراءة ملف الإكسل
print("قراءة ملف الإكسل...")
df = pd.read_excel('perfumes_list.xlsx', sheet_name='products_data (4)')

print(f"تم قراءة {len(df)} منتج")

# تحويل البيانات إلى قائمة من المنتجات
products = []

for index, row in df.iterrows():
    # التعامل مع الصور
    images = []
    if pd.notna(row['image_url']) and str(row['image_url']) != 'nan':
        images.append(str(row['image_url']))
    
    # تنظيف البيانات
    product = {
        'id': int(row['ID']) if pd.notna(row['ID']) else index + 1,
        'category': str(row['Category']).strip() if pd.notna(row['Category']) else '',
        'subCategory': str(row['Sub_Cat']).strip() if pd.notna(row['Sub_Cat']) else '',
        'barcode': str(row['Barcode']).strip() if pd.notna(row['Barcode']) else '',
        'itemName': str(row['Item_Name']).strip() if pd.notna(row['Item_Name']) else '',
        'perfumeNameEN': str(row['Perfume_Name']).strip() if pd.notna(row['Perfume_Name']) else '',
        'perfumeNameAR': str(row['Perfume_Name_Arabic']).strip() if pd.notna(row['Perfume_Name_Arabic']) else '',
        'topNotesEN': str(row['Top_Notes']).strip() if pd.notna(row['Top_Notes']) else '',
        'topNotesAR': str(row['Top_Notes_Arabic']).strip() if pd.notna(row['Top_Notes_Arabic']) else '',
        'heartNotesEN': str(row['Heart_Notes']).strip() if pd.notna(row['Heart_Notes']) else '',
        'heartNotesAR': str(row['Heart_Notes_Arabic']).strip() if pd.notna(row['Heart_Notes_Arabic']) else '',
        'baseNotesEN': str(row['Base_Notes']).strip() if pd.notna(row['Base_Notes']) else '',
        'baseNotesAR': str(row['Base_Notes_Arabic']).strip() if pd.notna(row['Base_Notes_Arabic']) else '',
        'descriptionEN': str(row['English_Description']).strip() if pd.notna(row['English_Description']) else '',
        'descriptionAR': str(row['Arabic_Description']).strip() if pd.notna(row['Arabic_Description']) else '',
        'seasonAR': str(row['Annual_seasons_Arabic']).strip() if pd.notna(row['Annual_seasons_Arabic']) else '',
        'seasonEN': str(row['Annual_seasons']).strip() if pd.notna(row['Annual_seasons']) else '',
        'dayNightAR': str(row['Day_Night_Arabic']).strip() if pd.notna(row['Day_Night_Arabic']) else '',
        'dayNightEN': str(row['Day_Night']).strip() if pd.notna(row['Day_Night']) else '',
        'images': images,
        'brandEN': str(row['Brand_EN']).strip() if pd.notna(row['Brand_EN']) else '',
        'brandAR': str(row['Brand_AR']).strip() if pd.notna(row['Brand_AR']) else '',
        'smell': str(row['smell']).strip() if pd.notna(row['smell']) else ''
    }
    
    # إزالة القيم "nan" النصية
    for key in product:
        if isinstance(product[key], str) and product[key] == 'nan':
            product[key] = ''
    
    products.append(product)

# إنشاء محتوى JavaScript
js_content = f"""// Lavish Perfumes - Products Data
// Auto-generated from Excel file
// Total Products: {len(products)}

const productsData = {json.dumps(products, ensure_ascii=False, indent=2)};

// Export for use in main.js
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = productsData;
}}
"""

# حفظ الملف
with open('js/products-data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"✓ تم إنشاء ملف js/products-data.js بنجاح!")
print(f"✓ عدد المنتجات: {len(products)}")

# عرض إحصائيات
categories = {}
subcategories = {}

for p in products:
    cat = p['category']
    subcat = p['subCategory']
    
    if cat:
        categories[cat] = categories.get(cat, 0) + 1
    if subcat:
        subcategories[subcat] = subcategories.get(subcat, 0) + 1

print(f"\n📊 إحصائيات الفئات:")
for cat, count in sorted(categories.items()):
    print(f"  - {cat}: {count} منتج")

print(f"\n📊 إحصائيات الأنواع:")
for subcat, count in sorted(subcategories.items()):
    print(f"  - {subcat}: {count} منتج")

print("\n✨ تم الانتهاء بنجاح!")
