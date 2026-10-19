/**
 * Global JavaScript for Theme Original (Shopify OS 2.0)
 * High-performance Vanilla JS handling Cart Drawer, Variant Selection, and Mobile Nav.
 */

class CartDrawer {
  constructor() {
    this.drawer = document.getElementById('CartDrawer');
    this.overlay = document.getElementById('CartDrawerOverlay');
    this.triggers = document.querySelectorAll('[data-cart-drawer-trigger]');
    this.closeButtons = document.querySelectorAll('[data-cart-drawer-close]');
    
    this.init();
  }

  init() {
    this.triggers.forEach(trigger => {
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        this.open();
      });
    });

    this.closeButtons.forEach(btn => {
      btn.addEventListener('click', () => this.close());
    });

    if (this.overlay) {
      this.overlay.addEventListener('click', () => this.close());
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') this.close();
    });

    // Intercept standard add to cart forms
    document.addEventListener('submit', (e) => {
      const form = e.target;
      if (form.matches('form[action*="/cart/add"]')) {
        e.preventDefault();
        this.handleAddToCart(form);
      }
    });
  }

  open() {
    if (this.drawer) this.drawer.classList.add('active');
    if (this.overlay) this.overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  close() {
    if (this.drawer) this.drawer.classList.remove('active');
    if (this.overlay) this.overlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  async handleAddToCart(form) {
    const submitBtn = form.querySelector('[type="submit"]');
    const originalText = submitBtn ? submitBtn.innerHTML : '';
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span>Adding...</span>';
    }

    try {
      const formData = new FormData(form);
      const response = await fetch(window.routes.cart_add_url || '/cart/add.js', {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      });

      if (!response.ok) {
        throw new Error('Failed to add item to cart');
      }

      await this.refreshCart();
      this.open();
    } catch (err) {
      console.error(err);
      alert('Could not add product to cart. Please try again.');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    }
  }

  async refreshCart() {
    try {
      const res = await fetch('/cart.js');
      const cart = await res.json();
      
      // Update badge
      document.querySelectorAll('[data-cart-count]').forEach(el => {
        el.textContent = cart.item_count;
        el.style.display = cart.item_count > 0 ? 'flex' : 'none';
      });

      // Update drawer content
      const itemsContainer = document.getElementById('CartDrawerItems');
      const subtotalEl = document.getElementById('CartDrawerSubtotal');
      
      if (subtotalEl) {
        subtotalEl.textContent = this.formatMoney(cart.total_price);
      }

      if (itemsContainer) {
        if (cart.items.length === 0) {
          itemsContainer.innerHTML = '<p class="cart-empty-text">Your cart is empty.</p>';
        } else {
          itemsContainer.innerHTML = cart.items.map(item => `
            <div class="cart-drawer-item" data-line-key="${item.key}">
              <img src="${item.featured_image.url || ''}" alt="${item.title}" width="70" height="70" style="object-fit:cover; border-radius:6px;">
              <div class="cart-drawer-item__details" style="flex-grow:1;">
                <h4 style="font-size:0.95rem; font-weight:600;">${item.product_title}</h4>
                ${item.variant_title ? `<p style="font-size:0.8rem; color:#64748b;">${item.variant_title}</p>` : ''}
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.5rem;">
                  <span style="font-size:0.85rem; font-weight:700;">${this.formatMoney(item.final_line_price)}</span>
                  <span style="font-size:0.85rem; color:#64748b;">Qty: ${item.quantity}</span>
                </div>
              </div>
            </div>
          `).join('');
        }
      }
    } catch (e) {
      console.error('Failed to refresh cart:', e);
    }
  }

  formatMoney(cents) {
    return (cents / 100).toLocaleString('en-US', { style: 'currency', currency: window.shopCurrency || 'USD' });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.cartDrawer = new CartDrawer();
});
