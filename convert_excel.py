import pandas as pd
import json

# قراءة ملف الإكسل
df = pd.read_excel('/home/user/perfumes_list.xlsx', sheet_name='products_data (4)')

# تحويل البيانات إلى قائمة من المنتجات
products = []

for index, row in df.iterrows():
    # تنظيف البيانات من القيم الفارغة
    product = {
        'id': int(row['ID']) if pd.notna(row['ID']) else index + 1,
        'category': str(row['Category']) if pd.notna(row['Category']) else '',
        'subCategory': str(row['Sub_Cat']) if pd.notna(row['Sub_Cat']) else '',
        'barcode': str(row['Barcode']) if pd.notna(row['Barcode']) else '',
        'itemName': str(row['Item_Name']) if pd.notna(row['Item_Name']) else '',
        'perfumeNameEN': str(row['Perfume_Name']) if pd.notna(row['Perfume_Name']) else '',
        'perfumeNameAR': str(row['Perfume_Name_Arabic']) if pd.notna(row['Perfume_Name_Arabic']) else '',
        'topNotesEN': str(row['Top_Notes']) if pd.notna(row['Top_Notes']) else '',
        'topNotesAR': str(row['Top_Notes_Arabic']) if pd.notna(row['Top_Notes_Arabic']) else '',
        'heartNotesEN': str(row['Heart_Notes']) if pd.notna(row['Heart_Notes']) else '',
        'heartNotesAR': str(row['Heart_Notes_Arabic']) if pd.notna(row['Heart_Notes_Arabic']) else '',
        'baseNotesEN': str(row['Base_Notes']) if pd.notna(row['Base_Notes']) else '',
        'baseNotesAR': str(row['Base_Notes_Arabic']) if pd.notna(row['Base_Notes_Arabic']) else '',
        'descriptionEN': str(row['English_Description']) if pd.notna(row['English_Description']) else '',
        'descriptionAR': str(row['Arabic_Description']) if pd.notna(row['Arabic_Description']) else '',
        'seasonAR': str(row['Annual_seasons_Arabic']) if pd.notna(row['Annual_seasons_Arabic']) else '',
        'seasonEN': str(row['Annual_seasons']) if pd.notna(row['Annual_seasons']) else '',
        'dayNightAR': str(row['Day_Night_Arabic']) if pd.notna(row['Day_Night_Arabic']) else '',
        'dayNightEN': str(row['Day_Night']) if pd.notna(row['Day_Night']) else '',
        'images': str(row['Images']).split(',') if pd.notna(row['Images']) else [],
        'brandEN': str(row['Brand_EN']) if pd.notna(row['Brand_EN']) else '',
        'brandAR': str(row['Brand_AR']) if pd.notna(row['Brand_AR']) else '',
        'imageUrl': str(row['image_url']) if pd.notna(row['image_url']) else '',
        'smell': str(row['smell']) if pd.notna(row['smell']) else ''
    }
    products.append(product)

# حفظ البيانات كملف JSON
with open('products_data.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f"تم تحويل {len(products)} منتج بنجاح!")
print(f"أول 3 منتجات:")
for i, p in enumerate(products[:3]):
    print(f"\n{i+1}. {p['perfumeNameAR']} ({p['perfumeNameEN']})")
    print(f"   الفئة: {p['category']} - {p['subCategory']}")
