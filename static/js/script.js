/*
===========================================================================
TRAVEL & TOURISM PORTAL - JAVASCRIPT
BIT233 - Web Technology Assignment

Client-Side Functionality and Validation
===========================================================================

JAVASCRIPT BASICS FOR BEGINNERS:
- JavaScript makes web pages interactive
- Runs in the browser (client-side)
- Can manipulate HTML elements (DOM manipulation)
- Can validate forms before submission
- Can make websites more dynamic and responsive
*/

// ===========================================================================
// DOCUMENT READY - Wait for page to load before running scripts
// ===========================================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('Travel Portal JS Loaded');
    
    // Initialize all features
    initFormValidation();
    initDateValidation();
    initBookingCalculator();
    initSearchFilters();
    initAlerts();
    initScrollAnimations();
});


// ===========================================================================
// FORM VALIDATION
// ===========================================================================

/**
 * Initialize form validation for all forms
 * 
 * Client-side validation provides instant feedback to users
 * Server-side validation (in Flask) is still required for security
 */
function initFormValidation() {
    // Get all forms with class 'needs-validation'
    const forms = document.querySelectorAll('.needs-validation');
    
    // Loop through forms and add validation
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            // Check if form is valid
            if (!form.checkValidity()) {
                event.preventDefault();  // Stop form submission
                event.stopPropagation();
            }
            
            // Add Bootstrap validation classes
            form.classList.add('was-validated');
        }, false);
    });
}


// ===========================================================================
// DATE VALIDATION
// ===========================================================================

/**
 * Ensure travel dates are in the future
 * 
 * This prevents users from booking tours for past dates
 */
function initDateValidation() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    
    dateInputs.forEach(input => {
        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        input.setAttribute('min', today);
        
        // Add change event listener
        input.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const currentDate = new Date();
            currentDate.setHours(0, 0, 0, 0);  // Reset time to midnight
            
            if (selectedDate < currentDate) {
                this.setCustomValidity('Travel date must be in the future');
                this.classList.add('is-invalid');
            } else {
                this.setCustomValidity('');
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
    });
}


// ===========================================================================
// BOOKING CALCULATOR
// ===========================================================================

/**
 * Calculate total booking amount in real-time
 * 
 * When user changes number of travelers, automatically update total price
 */
function initBookingCalculator() {
    const travelersInput = document.getElementById('number_of_travelers');
    const pricePerPerson = document.getElementById('price_per_person');
    const totalAmountDisplay = document.getElementById('total_amount_display');
    
    // Check if elements exist (only on booking page)
    if (travelersInput && pricePerPerson && totalAmountDisplay) {
        const basePrice = parseFloat(pricePerPerson.textContent);
        
        // Update total when travelers input changes
        travelersInput.addEventListener('input', function() {
            const travelers = parseInt(this.value) || 0;
            
            // Validate number of travelers
            if (travelers < 1) {
                this.setCustomValidity('Number of travelers must be at least 1');
                totalAmountDisplay.textContent = '0';
                return;
            }
            
            if (travelers > 50) {
                this.setCustomValidity('Maximum 50 travelers per booking');
                return;
            }
            
            // Clear custom validity
            this.setCustomValidity('');
            
            // Calculate and display total
            const total = basePrice * travelers;
            totalAmountDisplay.textContent = total.toFixed(2);
            
            // Add animation to total
            totalAmountDisplay.style.transform = 'scale(1.1)';
            setTimeout(() => {
                totalAmountDisplay.style.transform = 'scale(1)';
            }, 200);
        });
        
        // Trigger calculation on page load
        travelersInput.dispatchEvent(new Event('input'));
    }
}


// ===========================================================================
// SEARCH FILTERS
// ===========================================================================

/**
 * Handle search and filter functionality
 * 
 * Real-time filtering of packages (optional enhancement)
 */
function initSearchFilters() {
    const searchForm = document.getElementById('search-form');
    
    if (searchForm) {
        // Add submit event listener
        searchForm.addEventListener('submit', function(e) {
            // Form will submit normally with GET parameters
            console.log('Search submitted');
        });
    }
    
    // Price range slider functionality (if exists)
    const minPriceInput = document.getElementById('min_price');
    const maxPriceInput = document.getElementById('max_price');
    
    if (minPriceInput && maxPriceInput) {
        // Ensure max price is greater than min price
        minPriceInput.addEventListener('change', function() {
            const minPrice = parseFloat(this.value) || 0;
            const maxPrice = parseFloat(maxPriceInput.value) || Infinity;
            
            if (maxPrice < minPrice && maxPrice !== 0) {
                alert('Maximum price must be greater than minimum price');
                this.value = '';
            }
        });
        
        maxPriceInput.addEventListener('change', function() {
            const minPrice = parseFloat(minPriceInput.value) || 0;
            const maxPrice = parseFloat(this.value) || Infinity;
            
            if (maxPrice < minPrice && maxPrice !== 0) {
                alert('Maximum price must be greater than minimum price');
                this.value = '';
            }
        });
    }
}


// ===========================================================================
// ALERT AUTO-DISMISS
// ===========================================================================

/**
 * Automatically dismiss alert messages after 5 seconds
 * 
 * Improves user experience by clearing old messages
 */
function initAlerts() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            // Use Bootstrap's fade-out animation
            alert.classList.add('fade-out');
            
            // Remove element after animation
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
        
        // Add close button functionality
        const closeBtn = alert.querySelector('.btn-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                alert.classList.add('fade-out');
                setTimeout(() => alert.remove(), 500);
            });
        }
    });
}


// ===========================================================================
// SCROLL ANIMATIONS
// ===========================================================================

/**
 * Add animations when elements come into viewport
 * 
 * Makes the page more dynamic and engaging
 */
function initScrollAnimations() {
    // Create Intersection Observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, {
        threshold: 0.1  // Trigger when 10% of element is visible
    });
    
    // Observe all cards and feature boxes
    const animatedElements = document.querySelectorAll('.card, .feature-box, .testimonial-card');
    animatedElements.forEach(el => {
        observer.observe(el);
    });
}


// ===========================================================================
// CONFIRMATION DIALOGS
// ===========================================================================

/**
 * Confirm before deleting/cancelling
 * 
 * Prevents accidental deletions
 */
function confirmCancel(bookingId) {
    return confirm('Are you sure you want to cancel this booking? This action cannot be undone.');
}

// Attach to cancel buttons
document.addEventListener('DOMContentLoaded', function() {
    const cancelButtons = document.querySelectorAll('.cancel-booking-btn');
    
    cancelButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirmCancel(this.dataset.bookingId)) {
                e.preventDefault();
            }
        });
    });
});


// ===========================================================================
// PASSWORD STRENGTH CHECKER
// ===========================================================================

/**
 * Check password strength and show visual feedback
 * 
 * Helps users create secure passwords
 */
function checkPasswordStrength(password) {
    let strength = 0;
    const feedback = [];
    
    // Check length
    if (password.length >= 8) {
        strength += 1;
    } else {
        feedback.push('At least 8 characters');
    }
    
    // Check for uppercase
    if (/[A-Z]/.test(password)) {
        strength += 1;
    } else {
        feedback.push('One uppercase letter');
    }
    
    // Check for lowercase
    if (/[a-z]/.test(password)) {
        strength += 1;
    } else {
        feedback.push('One lowercase letter');
    }
    
    // Check for numbers
    if (/\d/.test(password)) {
        strength += 1;
    } else {
        feedback.push('One number');
    }
    
    // Check for special characters
    if (/[!@#$%^&*]/.test(password)) {
        strength += 1;
    } else {
        feedback.push('One special character (!@#$%^&*)');
    }
    
    return {
        strength: strength,
        feedback: feedback
    };
}

// Initialize password strength checker on registration page
document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    const strengthIndicator = document.getElementById('password-strength');
    const strengthText = document.getElementById('password-strength-text');
    
    if (passwordInput && strengthIndicator) {
        passwordInput.addEventListener('input', function() {
            const result = checkPasswordStrength(this.value);
            const percentage = (result.strength / 5) * 100;
            
            // Update progress bar
            strengthIndicator.style.width = percentage + '%';
            
            // Update color based on strength
            strengthIndicator.classList.remove('bg-danger', 'bg-warning', 'bg-success');
            if (percentage < 40) {
                strengthIndicator.classList.add('bg-danger');
                strengthText.textContent = 'Weak: ' + result.feedback.join(', ');
            } else if (percentage < 80) {
                strengthIndicator.classList.add('bg-warning');
                strengthText.textContent = 'Medium: ' + result.feedback.join(', ');
            } else {
                strengthIndicator.classList.add('bg-success');
                strengthText.textContent = 'Strong!';
            }
        });
    }
});


// ===========================================================================
// BOOKING AVAILABILITY CHECK
// ===========================================================================

/**
 * Check available slots before booking
 * 
 * Prevents overbooking
 */
function checkAvailability(packageId, travelers) {
    const availableSlots = parseInt(document.getElementById('available_slots').textContent);
    
    if (travelers > availableSlots) {
        alert(`Sorry, only ${availableSlots} slots available for this package.`);
        return false;
    }
    
    return true;
}


// ===========================================================================
// SMOOTH SCROLL TO SECTIONS
// ===========================================================================

/**
 * Smooth scroll to anchor links
 * 
 * Better user experience when navigating page sections
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        
        // Skip if href is just "#" (empty)
        if (href === '#') return;
        
        const target = document.querySelector(href);
        
        if (target) {
            e.preventDefault();
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});


// ===========================================================================
// IMAGE LAZY LOADING (Performance Optimization)
// ===========================================================================

/**
 * Lazy load images as they come into viewport
 * 
 * Improves page load performance
 */
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
});


// ===========================================================================
// FORM AUTO-SAVE (Optional Enhancement)
// ===========================================================================

/**
 * Save form data to localStorage to prevent data loss
 * 
 * Useful for long forms like booking forms
 */
function saveFormData(formId) {
    const form = document.getElementById(formId);
    
    if (!form) return;
    
    // Get all form inputs
    const inputs = form.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        // Save on input change
        input.addEventListener('change', function() {
            const key = `${formId}_${this.name}`;
            localStorage.setItem(key, this.value);
        });
        
        // Load saved value
        const key = `${formId}_${input.name}`;
        const savedValue = localStorage.getItem(key);
        if (savedValue && input.type !== 'password') {
            input.value = savedValue;
        }
    });
    
    // Clear saved data on successful submission
    form.addEventListener('submit', function() {
        inputs.forEach(input => {
            const key = `${formId}_${input.name}`;
            localStorage.removeItem(key);
        });
    });
}


// ===========================================================================
// DYNAMIC PACKAGE FILTERING (Optional Client-Side Enhancement)
// ===========================================================================

/**
 * Filter packages without page reload
 * 
 * Faster user experience with instant filtering
 */
function filterPackages() {
    const searchInput = document.getElementById('keyword');
    const categorySelect = document.getElementById('category');
    const packages = document.querySelectorAll('.package-card');
    
    if (!searchInput || !packages.length) return;
    
    const filterFunc = () => {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedCategory = categorySelect ? categorySelect.value : '';
        
        packages.forEach(packageCard => {
            const title = packageCard.querySelector('.card-title').textContent.toLowerCase();
            const destination = packageCard.querySelector('.destination').textContent.toLowerCase();
            const category = packageCard.dataset.category || '';
            
            const matchesSearch = title.includes(searchTerm) || destination.includes(searchTerm);
            const matchesCategory = !selectedCategory || category === selectedCategory;
            
            if (matchesSearch && matchesCategory) {
                packageCard.style.display = 'block';
                packageCard.classList.add('animate-in');
            } else {
                packageCard.style.display = 'none';
            }
        });
    };
    
    // Add event listeners
    searchInput.addEventListener('input', filterFunc);
    if (categorySelect) {
        categorySelect.addEventListener('change', filterFunc);
    }
}


// ===========================================================================
// STAR RATING SYSTEM (For Reviews - Optional Enhancement)
// ===========================================================================

/**
 * Interactive star rating
 */
function initStarRating() {
    const starContainers = document.querySelectorAll('.star-rating');
    
    starContainers.forEach(container => {
        const stars = container.querySelectorAll('.star');
        const input = container.querySelector('input[type="hidden"]');
        
        stars.forEach((star, index) => {
            star.addEventListener('click', () => {
                const rating = index + 1;
                input.value = rating;
                
                // Update star display
                stars.forEach((s, i) => {
                    if (i < rating) {
                        s.classList.add('active');
                    } else {
                        s.classList.remove('active');
                    }
                });
            });
        });
    });
}


// ===========================================================================
// UTILITY FUNCTIONS
// ===========================================================================

/**
 * Format currency
 */
function formatCurrency(amount) {
    return 'NPR ' + parseFloat(amount).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
}

/**
 * Format date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

/**
 * Show loading spinner
 */
function showLoading() {
    const loader = document.createElement('div');
    loader.id = 'page-loader';
    loader.className = 'spinner';
    document.body.appendChild(loader);
}

/**
 * Hide loading spinner
 */
function hideLoading() {
    const loader = document.getElementById('page-loader');
    if (loader) {
        loader.remove();
    }
}


/*
===========================================================================
JAVASCRIPT CONCEPTS EXPLAINED:

1. Event Listeners:
   - Listen for user actions (click, input, change, submit)
   - Execute functions when events occur
   - Syntax: element.addEventListener('event', function)

2. DOM Manipulation:
   - Access HTML elements: document.querySelector(), getElementById()
   - Modify elements: element.textContent, element.style
   - Add/remove classes: classList.add(), classList.remove()

3. Form Validation:
   - Client-side: Quick feedback, better UX
   - Server-side: Secure, cannot be bypassed
   - Always use both!

4. Local Storage:
   - Store data in browser
   - Persists across page reloads
   - Limited to strings (use JSON for objects)
   - Syntax: localStorage.setItem(key, value)

5. Async Operations:
   - setTimeout: Delay execution
   - Fetch API: Make HTTP requests (AJAX)
   - Promises: Handle async results

6. Best Practices:
   - Always validate user input
   - Provide clear error messages
   - Make UI responsive and intuitive
   - Consider accessibility
   - Test on different browsers
===========================================================================
*/
