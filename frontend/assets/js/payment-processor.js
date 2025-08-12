/**
 * NexusAGI Payment Processor
 * Handles all client-side payment operations with military-grade security
 */
class AGIPaymentProcessor {
    constructor() {
        this.paymentConfig = {
            stripeKey: 'pk_live_...', // Replace with your Stripe key
            endpoints: {
                initiate: '/api/payment/initiate',
                confirm: '/api/payment/confirm',
                webhook: '/api/payment/webhook'
            },
            currencies: {
                primary: 'ZAR',
                fallback: 'USD'
            },
            feeStructure: {
                owner: 0.6,
                aiFund: 0.2,
                reserve: 0.2
            }
        };
        
        this.cart = JSON.parse(localStorage.getItem('ai_cart')) || [];
        this.initPaymentElements();
    }

    // Initialize Stripe elements
    async initPaymentElements() {
        // Load Stripe.js only when needed
        if (!window.Stripe) {
            await this.loadScript('https://js.stripe.com/v3/');
        }
        
        this.stripe = Stripe(this.paymentConfig.stripeKey);
        this.elements = this.stripe.elements();
        
        // Mount card element
        const cardElement = this.elements.create('card', {
            style: {
                base: {
                    fontSize: '16px',
                    color: '#32325d',
                    '::placeholder': {
                        color: '#aab7c4'
                    }
                },
                invalid: {
                    color: '#fa755a',
                    iconColor: '#fa755a'
                }
            }
        });
        
        cardElement.mount('#card-element');
        this.cardElement = cardElement;
        
        // Set up form handler
        const paymentForm = document.getElementById('payment-form');
        if (paymentForm) {
            paymentForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.handlePaymentSubmit();
            });
        }
    }

    // Handle payment form submission
    async handlePaymentSubmit() {
        const submitButton = document.getElementById('submit-payment');
        submitButton.disabled = true;
        submitButton.textContent = 'Processing...';
        
        // Create payment intent
        const { clientSecret, error: intentError } = await this.createPaymentIntent();
        
        if (intentError) {
            this.showPaymentError(intentError);
            submitButton.disabled = false;
            submitButton.textContent = 'Pay Now';
            return;
        }
        
        // Confirm payment
        const { paymentIntent, error: confirmError } = await this.stripe.confirmCardPayment(
            clientSecret, {
                payment_method: {
                    card: this.cardElement,
                    billing_details: {
                        name: document.getElementById('cardholder-name').value
                    }
                }
            }
        );
        
        if (confirmError) {
            this.showPaymentError(confirmError);
        } else {
            await this.handleSuccessfulPayment(paymentIntent);
        }
        
        submitButton.disabled = false;
        submitButton.textContent = 'Pay Now';
    }

    // Create payment intent on backend
    async createPaymentIntent() {
        try {
            const response = await fetch(this.paymentConfig.endpoints.initiate, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': this.getCSRFToken()
                },
                body: JSON.stringify({
                    amount: this.calculateCartTotal(),
                    currency: this.paymentConfig.currencies.primary,
                    items: this.cart
                })
            });
            
            return await response.json();
        } catch (error) {
            console.error('Payment Intent Error:', error);
            return { error: { message: 'Connection failed. Please try again.' } };
        }
    }

    // Handle successful payment
    async handleSuccessfulPayment(paymentIntent) {
        // Verify with backend
        const verification = await this.verifyPayment(paymentIntent.id);
        
        if (verification.success) {
            // Show success UI
            this.showPaymentSuccess(paymentIntent);
            
            // Clear cart
            this.cart = [];
            localStorage.removeItem('ai_cart');
            
            // Trigger order fulfillment
            this.triggerFulfillment(paymentIntent);
        } else {
            this.showPaymentError({ message: 'Payment verification failed' });
        }
    }

    // Verify payment with backend
    async verifyPayment(paymentId) {
        try {
            const response = await fetch(`${this.paymentConfig.endpoints.confirm}/${paymentId}`, {
                headers: {
                    'X-CSRF-Token': this.getCSRFToken()
                }
            });
            return await response.json();
        } catch (error) {
            console.error('Verification Error:', error);
            return { success: false };
        }
    }

    // Trigger order fulfillment
    async triggerFulfillment(paymentIntent) {
        try {
            await fetch(`${this.paymentConfig.endpoints.webhook}/fulfill`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': this.getCSRFToken()
                },
                body: JSON.stringify({
                    paymentId: paymentIntent.id,
                    amount: paymentIntent.amount,
                    items: this.cart
                })
            });
        } catch (error) {
            console.error('Fulfillment Error:', error);
        }
    }

    // Calculate cart total in cents
    calculateCartTotal() {
        return this.cart.reduce((total, item) => total + (item.price * 100), 0);
    }

    // Get CSRF token from meta tag
    getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').content;
    }

    // Load external script
    loadScript(src) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = src;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    // Show payment error
    showPaymentError(error) {
        const errorElement = document.getElementById('card-errors');
        errorElement.textContent = error.message || 'Payment failed. Please try again.';
        errorElement.style.display = 'block';
        
        setTimeout(() => {
            errorElement.style.display = 'none';
        }, 5000);
    }

    // Show payment success
    showPaymentSuccess(paymentIntent) {
        const paymentForm = document.getElementById('payment-form');
        paymentForm.innerHTML = `
            <div class="payment-success">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                <h3>Payment Successful!</h3>
                <p>Order #${paymentIntent.id.slice(-8)}</p>
                <p>Amount: R${(paymentIntent.amount / 100).toFixed(2)}</p>
                <a href="/dashboard.html" class="button">View Order</a>
            </div>
        `;
    }

    // Add item to cart
    addToCart(item) {
        this.cart.push(item);
        localStorage.setItem('ai_cart', JSON.stringify(this.cart));
        this.updateCartUI();
    }

    // Update cart UI
    updateCartUI() {
        const cartCounter = document.getElementById('cart-counter');
        if (cartCounter) {
            cartCounter.textContent = this.cart.length;
            cartCounter.style.display = this.cart.length ? 'flex' : 'none';
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const paymentProcessor = new AGIPaymentProcessor();
    
    // Make available globally for cart operations
    window.AGIPayments = paymentProcessor;
    
    // Initialize cart display
    paymentProcessor.updateCartUI();
});
