// ============================================
// Lavish Perfumes - Main JavaScript
// ============================================

// Global Variables
let allProducts = [];
let filteredProducts = [];
let currentPage = 1;
const productsPerPage = 12;

// Filters State
let filters = {
    search: '',
    category: 'all',
    subCategory: 'all',
    sort: 'default'
};

// ============================================
// Initialize App
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Lavish Perfumes - Loading...');
    
    // Load products data
    if (typeof productsData !== 'undefined') {
        allProducts = productsData;
        filteredProducts = [...allProducts];
        console.log(`✓ تم تحميل ${allProducts.length} منتج`);
        
        // Initialize app
        initializeApp();
    } else {
        console.error('❌ خطأ: لم يتم تحميل بيانات المنتجات');
        showError('عذراً، حدث خطأ في تحميل المنتجات');
    }
});

// ============================================
// Initialize App Functions
// ============================================
function initializeApp() {
    setupEventListeners();
    updateFilterButtons();
    renderProducts();
    hideLoading();
    
    console.log('✓ تم تهيئة الموقع بنجاح');
}

// ============================================
// Event Listeners
// ============================================
function setupEventListeners() {
    // Mobile Menu Toggle
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileNav = document.getElementById('mobileNav');
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileNav.classList.toggle('active');
        });
    }
    
    // Search Input
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function(e) {
            filters.search = e.target.value.trim().toLowerCase();
            applyFilters();
        }, 300));
    }
    
    // Category Filter Buttons
    const categoryButtons = document.querySelectorAll('#categoryFilter .filter-btn');
    categoryButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active from all
            categoryButtons.forEach(b => b.classList.remove('active'));
            // Add active to clicked
            this.classList.add('active');
            
            filters.category = this.getAttribute('data-category');
            applyFilters();
        });
    });
    
    // Sub-Category Filter Buttons
    const subCategoryButtons = document.querySelectorAll('#subCategoryFilter .filter-btn');
    subCategoryButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active from all
            subCategoryButtons.forEach(b => b.classList.remove('active'));
            // Add active to clicked
            this.classList.add('active');
            
            filters.subCategory = this.getAttribute('data-subcategory');
            applyFilters();
        });
    });
    
    // Sort Select
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            filters.sort = this.value;
            applyFilters();
        });
    }
    
    // Reset Filters Button
    const resetBtn = document.getElementById('resetFilters');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetFilters);
    }
    
    // Load More Button
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', loadMoreProducts);
    }
    
    // Modal Close
    const modalClose = document.getElementById('modalClose');
    const modalOverlay = document.getElementById('modalOverlay');
    
    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }
    if (modalOverlay) {
        modalOverlay.addEventListener('click', closeModal);
    }
    
    // Scroll to Top Button
    const scrollToTopBtn = document.getElementById('scrollToTop');
    if (scrollToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollToTopBtn.classList.add('visible');
            } else {
                scrollToTopBtn.classList.remove('visible');
            }
        });
        
        scrollToTopBtn.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
    
    // Smooth Scroll for Navigation Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                
                // Close mobile menu if open
                if (mobileNav) {
                    mobileNav.classList.remove('active');
                }
            }
        });
    });
}

// ============================================
// Filter Functions
// ============================================
function applyFilters() {
    console.log('🔍 تطبيق الفلاتر:', filters);
    
    filteredProducts = allProducts.filter(product => {
        // Search filter
        if (filters.search) {
            const searchLower = filters.search;
            const matchesSearch = 
                product.perfumeNameAR.toLowerCase().includes(searchLower) ||
                product.perfumeNameEN.toLowerCase().includes(searchLower) ||
                product.itemName.toLowerCase().includes(searchLower) ||
                product.descriptionAR.toLowerCase().includes(searchLower) ||
                product.descriptionEN.toLowerCase().includes(searchLower);
            
            if (!matchesSearch) return false;
        }
        
        // Category filter
        if (filters.category !== 'all' && product.category !== filters.category) {
            return false;
        }
        
        // Sub-category filter
        if (filters.subCategory !== 'all') {
            const subCatUpper = filters.subCategory.toUpperCase();
            const productSubCat = product.subCategory.toUpperCase();
            
            if (!productSubCat.includes(subCatUpper)) {
                return false;
            }
        }
        
        return true;
    });
    
    // Apply sorting
    sortProducts();
    
    // Reset pagination
    currentPage = 1;
    
    // Update UI
    renderProducts();
    updateResultsCount();
}

function sortProducts() {
    switch (filters.sort) {
        case 'name-asc':
            filteredProducts.sort((a, b) => 
                a.perfumeNameAR.localeCompare(b.perfumeNameAR, 'ar'));
            break;
        case 'name-desc':
            filteredProducts.sort((a, b) => 
                b.perfumeNameAR.localeCompare(a.perfumeNameAR, 'ar'));
            break;
        case 'brand':
            filteredProducts.sort((a, b) => 
                a.category.localeCompare(b.category));
            break;
        default:
            // Keep default order
            break;
    }
}

function resetFilters() {
    // Reset filters state
    filters = {
        search: '',
        category: 'all',
        subCategory: 'all',
        sort: 'default'
    };
    
    // Reset UI
    document.getElementById('searchInput').value = '';
    document.getElementById('sortSelect').value = 'default';
    
    // Reset filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-category') === 'all' || 
            btn.getAttribute('data-subcategory') === 'all') {
            btn.classList.add('active');
        }
    });
    
    // Apply filters
    applyFilters();
}

function updateFilterButtons() {
    // Get unique categories
    const categories = [...new Set(allProducts.map(p => p.category))].filter(c => c);
    
    // You can dynamically update filter buttons here if needed
    console.log('الفئات المتوفرة:', categories);
}

// ============================================
// Render Functions
// ============================================
function renderProducts() {
    const productsGrid = document.getElementById('productsGrid');
    const noResults = document.getElementById('noResults');
    const loadMoreContainer = document.getElementById('loadMoreContainer');
    
    if (!productsGrid) return;
    
    // Clear grid
    productsGrid.innerHTML = '';
    
    // Check if no results
    if (filteredProducts.length === 0) {
        noResults.style.display = 'block';
        loadMoreContainer.style.display = 'none';
        return;
    }
    
    noResults.style.display = 'none';
    
    // Calculate products to show
    const totalToShow = currentPage * productsPerPage;
    const productsToRender = filteredProducts.slice(0, totalToShow);
    
    // Render products
    productsToRender.forEach(product => {
        const productCard = createProductCard(product);
        productsGrid.appendChild(productCard);
    });
    
    // Show/hide load more button
    if (totalToShow < filteredProducts.length) {
        loadMoreContainer.style.display = 'block';
    } else {
        loadMoreContainer.style.display = 'none';
    }
    
    console.log(`✓ تم عرض ${productsToRender.length} من ${filteredProducts.length} منتج`);
}

function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.onclick = () => openProductModal(product);
    
    // Get image URL
    const imageUrl = product.images && product.images.length > 0 
        ? product.images[0] 
        : 'https://via.placeholder.com/400x400/F5E6C8/D4AF37?text=No+Image';
    
    // Create card HTML
    card.innerHTML = `
        <div class="product-image-container">
            <img src="${imageUrl}" alt="${product.perfumeNameAR}" class="product-image" 
                 onerror="this.src='https://via.placeholder.com/400x400/F5E6C8/D4AF37?text=Lavish'">
            ${product.category ? `<div class="product-badge">${product.category}</div>` : ''}
        </div>
        <div class="product-info">
            ${product.category ? `<div class="product-category">${product.category}</div>` : ''}
            <h3 class="product-name">${product.perfumeNameAR || product.itemName}</h3>
            ${product.perfumeNameEN ? `<p class="product-name-en">${product.perfumeNameEN}</p>` : ''}
            ${product.descriptionAR ? `<p class="product-description">${truncateText(product.descriptionAR, 100)}</p>` : ''}
            <div class="product-meta">
                ${product.subCategory ? `<span class="product-tag">${product.subCategory}</span>` : ''}
                ${product.seasonAR ? `<span class="product-tag">${product.seasonAR}</span>` : ''}
            </div>
        </div>
    `;
    
    return card;
}

function loadMoreProducts() {
    currentPage++;
    renderProducts();
    
    // Scroll to new products
    const productsSection = document.getElementById('productsGrid');
    if (productsSection) {
        const lastProduct = productsSection.lastElementChild;
        if (lastProduct) {
            lastProduct.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }
}

function updateResultsCount() {
    const resultsCount = document.getElementById('resultsCount');
    if (resultsCount) {
        resultsCount.textContent = filteredProducts.length;
    }
}

// ============================================
// Modal Functions
// ============================================
function openProductModal(product) {
    const modal = document.getElementById('productModal');
    const modalBody = document.getElementById('modalBody');
    
    if (!modal || !modalBody) return;
    
    // Get image URL
    const imageUrl = product.images && product.images.length > 0 
        ? product.images[0] 
        : 'https://via.placeholder.com/600x600/F5E6C8/D4AF37?text=No+Image';
    
    // Create modal content
    modalBody.innerHTML = `
        <div class="modal-product-grid">
            <div class="modal-image-gallery">
                <img src="${imageUrl}" alt="${product.perfumeNameAR}" class="modal-main-image"
                     onerror="this.src='https://via.placeholder.com/600x600/F5E6C8/D4AF37?text=Lavish'">
            </div>
            
            <div class="modal-product-details">
                <h2>${product.perfumeNameAR || product.itemName}</h2>
                ${product.perfumeNameEN ? `<h3>${product.perfumeNameEN}</h3>` : ''}
                
                ${product.category ? `
                    <div class="modal-info-section">
                        <h4>العلامة التجارية</h4>
                        <p>${product.category}</p>
                    </div>
                ` : ''}
                
                ${product.descriptionAR ? `
                    <div class="modal-info-section">
                        <h4>الوصف</h4>
                        <p>${product.descriptionAR}</p>
                    </div>
                ` : ''}
                
                ${product.topNotesAR || product.heartNotesAR || product.baseNotesAR ? `
                    <div class="modal-info-section">
                        <h4>المكونات</h4>
                        <div class="notes-grid">
                            ${product.topNotesAR ? `
                                <div class="note-item">
                                    <h5>المقدمة</h5>
                                    <p>${product.topNotesAR}</p>
                                </div>
                            ` : ''}
                            ${product.heartNotesAR ? `
                                <div class="note-item">
                                    <h5>القلب</h5>
                                    <p>${product.heartNotesAR}</p>
                                </div>
                            ` : ''}
                            ${product.baseNotesAR ? `
                                <div class="note-item">
                                    <h5>القاعدة</h5>
                                    <p>${product.baseNotesAR}</p>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                ` : ''}
                
                ${product.seasonAR || product.dayNightAR ? `
                    <div class="modal-info-section">
                        <h4>معلومات إضافية</h4>
                        <div class="product-meta">
                            ${product.subCategory ? `<span class="product-tag">${product.subCategory}</span>` : ''}
                            ${product.seasonAR ? `<span class="product-tag">${product.seasonAR}</span>` : ''}
                            ${product.dayNightAR ? `<span class="product-tag">${product.dayNightAR}</span>` : ''}
                        </div>
                    </div>
                ` : ''}
                
                <div class="modal-info-section">
                    <a href="https://instagram.com/lavish_perfumes_iraq" target="_blank" class="btn btn-primary">
                        <i class="fab fa-instagram"></i>
                        تواصل معنا للطلب
                    </a>
                </div>
            </div>
        </div>
    `;
    
    // Show modal
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const modal = document.getElementById('productModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// ============================================
// Utility Functions
// ============================================
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
}

function hideLoading() {
    const loadingSpinner = document.getElementById('loadingSpinner');
    if (loadingSpinner) {
        loadingSpinner.style.display = 'none';
    }
}

function showError(message) {
    const productsGrid = document.getElementById('productsGrid');
    if (productsGrid) {
        productsGrid.innerHTML = `
            <div class="no-results">
                <i class="fas fa-exclamation-circle"></i>
                <h3>خطأ</h3>
                <p>${message}</p>
            </div>
        `;
    }
    hideLoading();
}

// ============================================
// Console Welcome Message
// ============================================
console.log('%c🌟 Lavish Perfumes 🌟', 'font-size: 24px; color: #D4AF37; font-weight: bold;');
console.log('%cLuxury Perfumes Website', 'font-size: 14px; color: #666;');
console.log('%c✨ Developed with care ✨', 'font-size: 12px; color: #D4AF37;');
