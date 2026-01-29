#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lavish Perfumes - Simple Excel to JS Converter
Converts Excel product data to JavaScript file
"""

import sys
import json

try:
    import pandas as pd
    print("✓ Pandas imported successfully")
except ImportError:
    print("❌ Error: pandas is not installed")
    print("📦 Install it using: pip install pandas openpyxl")
    sys.exit(1)

def clean(value):
    """Clean and normalize values"""
    if pd.isna(value) or str(value).lower() == 'nan':
        return ""
    return str(value).strip()

def get_images(url):
    """Process image URL"""
    if pd.isna(url) or not url or str(url).lower() == 'nan':
        return []
    return [clean(url)] if clean(url) else []

try:
    print("\n" + "="*60)
    print("🌟 Lavish Perfumes - Data Conversion Tool")
    print("="*60)
    
    excel_path = '/home/user/perfumes_list.xlsx'
    print(f"\n📂 Reading: {excel_path}")
    
    # Read Excel
    df = pd.read_excel(excel_path, sheet_name='products_data (4)')
    print(f"✓ Loaded {len(df)} rows")
    
    # Process data
    products = []
    print(f"\n🔄 Processing products...")
    
    for idx, row in df.iterrows():
        product = {
            'id': int(row['ID']) if pd.notna(row['ID']) else idx + 1,
            'category': clean(row['Category']),
            'subCategory': clean(row['Sub_Cat']),
            'barcode': clean(row['Barcode']),
            'itemName': clean(row['Item_Name']),
            'perfumeNameEN': clean(row['Perfume_Name']),
            'perfumeNameAR': clean(row['Perfume_Name_Arabic']),
            'topNotesEN': clean(row['Top_Notes']),
            'topNotesAR': clean(row['Top_Notes_Arabic']),
            'heartNotesEN': clean(row['Heart_Notes']),
            'heartNotesAR': clean(row['Heart_Notes_Arabic']),
            'baseNotesEN': clean(row['Base_Notes']),
            'baseNotesAR': clean(row['Base_Notes_Arabic']),
            'descriptionEN': clean(row['English_Description']),
            'descriptionAR': clean(row['Arabic_Description']),
            'seasonAR': clean(row['Annual_seasons_Arabic']),
            'seasonEN': clean(row['Annual_seasons']),
            'dayNightAR': clean(row['Day_Night_Arabic']),
            'dayNightEN': clean(row['Day_Night']),
            'images': get_images(row['image_url']),
            'brandEN': clean(row['Brand_EN']),
            'brandAR': clean(row['Brand_AR']),
            'smell': clean(row['smell'])
        }
        products.append(product)
        
        # Progress indicator
        if (idx + 1) % 50 == 0:
            print(f"   Processed: {idx + 1}/{len(df)}")
    
    print(f"✓ Processed {len(products)} products")
    
    # Generate JavaScript file
    print(f"\n📝 Generating JavaScript file...")
    
    js_code = f"""// Lavish Perfumes - Products Data
// Auto-generated from Excel file
// Total Products: {len(products)}
// Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

const productsData = """
    
    js_code += json.dumps(products, ensure_ascii=False, indent=2)
    
    js_code += """;

// Log loaded products
console.log(`✓ Lavish Perfumes: تم تحميل ${productsData.length} منتج`);

// Stats
const stats = {
    total: productsData.length,
    categories: [...new Set(productsData.map(p => p.category))].filter(c => c).length,
    withImages: productsData.filter(p => p.images && p.images.length > 0).length
};
console.log('📊 Statistics:', stats);
"""
    
    # Write to file
    output_file = 'js/products-data.js'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_code)
    
    # Get file size
    import os
    file_size = os.path.getsize(output_file)
    
    print(f"✓ Created: {output_file}")
    print(f"✓ File size: {file_size / 1024:.2f} KB")
    
    # Statistics
    categories = {}
    subcategories = {}
    with_images = 0
    
    for p in products:
        if p['category']:
            categories[p['category']] = categories.get(p['category'], 0) + 1
        if p['subCategory']:
            subcategories[p['subCategory']] = subcategories.get(p['subCategory'], 0) + 1
        if p['images']:
            with_images += 1
    
    print(f"\n📊 Statistics:")
    print(f"   Total Products: {len(products)}")
    print(f"   With Images: {with_images}")
    print(f"   Categories: {len(categories)}")
    print(f"   Sub-categories: {len(subcategories)}")
    
    print(f"\n🏷️  Top Categories:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"      • {cat}: {count}")
    
    print(f"\n📦 Sub-Categories:")
    for subcat, count in sorted(subcategories.items(), key=lambda x: x[1], reverse=True):
        print(f"      • {subcat}: {count}")
    
    print("\n" + "="*60)
    print("✅ SUCCESS! Data conversion completed")
    print("="*60)
    print(f"\n🚀 Next steps:")
    print(f"   1. Open index.html in your browser")
    print(f"   2. Browse {len(products)} perfumes")
    print(f"   3. Enjoy your Lavish Perfumes website! ✨")
    print()

except FileNotFoundError:
    print(f"\n❌ Error: Excel file not found at {excel_path}")
    print("📁 Make sure the file exists at the correct location")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ Error occurred: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
