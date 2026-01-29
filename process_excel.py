#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import json
import os

def clean_value(value):
    """تنظيف القيم من nan وغيرها"""
    if pd.isna(value):
        return ""
    value_str = str(value).strip()
    if value_str.lower() == 'nan':
        return ""
    return value_str

def process_images(image_url):
    """معالجة روابط الصور"""
    if pd.isna(image_url) or str(image_url).strip().lower() == 'nan':
        return []
    
    url = str(image_url).strip()
    if url:
        return [url]
    return []

try:
    print("🔄 بدء معالجة ملف الإكسل...")
    
    # قراءة الملف
    excel_path = '/home/user/perfumes_list.xlsx'
    df = pd.read_excel(excel_path, sheet_name='products_data (4)')
    
    print(f"✓ تم قراءة {len(df)} سطر من الملف")
    
    # معالجة البيانات
    products = []
    
    for index, row in df.iterrows():
        product = {
            'id': int(row['ID']) if pd.notna(row['ID']) else index + 1,
            'category': clean_value(row['Category']),
            'subCategory': clean_value(row['Sub_Cat']),
            'barcode': clean_value(row['Barcode']),
            'itemName': clean_value(row['Item_Name']),
            'perfumeNameEN': clean_value(row['Perfume_Name']),
            'perfumeNameAR': clean_value(row['Perfume_Name_Arabic']),
            'topNotesEN': clean_value(row['Top_Notes']),
            'topNotesAR': clean_value(row['Top_Notes_Arabic']),
            'heartNotesEN': clean_value(row['Heart_Notes']),
            'heartNotesAR': clean_value(row['Heart_Notes_Arabic']),
            'baseNotesEN': clean_value(row['Base_Notes']),
            'baseNotesAR': clean_value(row['Base_Notes_Arabic']),
            'descriptionEN': clean_value(row['English_Description']),
            'descriptionAR': clean_value(row['Arabic_Description']),
            'seasonAR': clean_value(row['Annual_seasons_Arabic']),
            'seasonEN': clean_value(row['Annual_seasons']),
            'dayNightAR': clean_value(row['Day_Night_Arabic']),
            'dayNightEN': clean_value(row['Day_Night']),
            'images': process_images(row['image_url']),
            'brandEN': clean_value(row['Brand_EN']),
            'brandAR': clean_value(row['Brand_AR']),
            'smell': clean_value(row['smell'])
        }
        
        products.append(product)
    
    print(f"✓ تمت معالجة {len(products)} منتج")
    
    # إنشاء محتوى JavaScript
    js_content = f"""// Lavish Perfumes - Products Data
// Auto-generated from Excel file
// Total Products: {len(products)}
// Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

const productsData = """
    
    # إضافة البيانات بصيغة JSON جميلة
    js_content += json.dumps(products, ensure_ascii=False, indent=2)
    
    js_content += """;

// Export if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = productsData;
}

console.log(`✓ تم تحميل ${productsData.length} منتج من Lavish Perfumes`);
"""
    
    # حفظ الملف
    output_path = 'js/products-data.js'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✓ تم إنشاء {output_path} بنجاح!")
    
    # إحصائيات
    categories = {}
    subcategories = {}
    
    for p in products:
        if p['category']:
            categories[p['category']] = categories.get(p['category'], 0) + 1
        if p['subCategory']:
            subcategories[p['subCategory']] = subcategories.get(p['subCategory'], 0) + 1
    
    print(f"\n📊 إحصائيات:")
    print(f"   إجمالي المنتجات: {len(products)}")
    print(f"\n   الفئات ({len(categories)}):")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"      • {cat}: {count} منتج")
    
    print(f"\n   الأنواع ({len(subcategories)}):")
    for subcat, count in sorted(subcategories.items(), key=lambda x: x[1], reverse=True):
        print(f"      • {subcat}: {count} منتج")
    
    print(f"\n✅ تم الانتهاء بنجاح!")
    print(f"📁 حجم الملف: {os.path.getsize(output_path) / 1024:.2f} KB")
    
except Exception as e:
    print(f"❌ خطأ: {str(e)}")
    import traceback
    traceback.print_exc()
