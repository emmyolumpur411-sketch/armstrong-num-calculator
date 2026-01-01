// Main JavaScript file for Armstrong Number Calculator

document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Basic HTML5 validation will handle most cases
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Email validation
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const email = this.value;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (email && !emailRegex.test(email)) {
                this.setCustomValidity('Please enter a valid email address');
            } else {
                this.setCustomValidity('');
            }
        });
    });
    
    // Phone validation
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const phone = this.value.replace(/\D/g, '');
            if (phone && (phone.length < 10 || phone.length > 15)) {
                this.setCustomValidity('Phone number must be 10-15 digits');
            } else {
                this.setCustomValidity('');
            }
        });
    });
    
    // Password confirmation validation
    const passwordInputs = document.querySelectorAll('input[name="password"]');
    const confirmPasswordInputs = document.querySelectorAll('input[name="confirm_password"]');
    
    if (passwordInputs.length && confirmPasswordInputs.length) {
        const password = passwordInputs[0];
        const confirmPassword = confirmPasswordInputs[0];
        
        confirmPassword.addEventListener('blur', function() {
            if (this.value !== password.value) {
                this.setCustomValidity('Passwords do not match');
            } else {
                this.setCustomValidity('');
            }
        });
        
        password.addEventListener('input', function() {
            if (confirmPassword.value) {
                confirmPassword.dispatchEvent(new Event('blur'));
            }
        });
    }
});
