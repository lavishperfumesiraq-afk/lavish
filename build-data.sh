#!/bin/bash
# Script to generate products data from Excel file

echo "🔄 Lavish Perfumes - تحويل بيانات المنتجات"
echo "============================================"
echo ""

# Check if Python and required packages are available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير متوفر"
    exit 1
fi

# Install required packages
echo "📦 تثبيت المكتبات المطلوبة..."
pip3 install -q pandas openpyxl 2>/dev/null || pip install -q pandas openpyxl 2>/dev/null

# Run the conversion script
echo ""
echo "🔄 بدء تحويل البيانات..."
python3 process_excel.py

# Check if successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ تم إنشاء ملف البيانات بنجاح!"
    echo "📁 الملف: js/products-data.js"
    echo ""
    echo "🚀 الموقع جاهز للاستخدام!"
    echo "   افتح index.html في المتصفح"
else
    echo ""
    echo "❌ حدث خطأ في التحويل"
    exit 1
fi
