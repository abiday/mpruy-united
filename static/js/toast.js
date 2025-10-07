// Custom Toast Notification System
// Position: Top-right corner
// Styling: Green for success, Red for error
// Features: Manual close button and auto-hide

let toastTimeout = null;

function showToast(message, type = 'success', duration = 3000) {
    const toastComponent = document.getElementById('toast-component');
    const toastMessage = document.getElementById('toast-message');
    const toastIcon = document.getElementById('toast-icon');
    
    if (!toastComponent || !toastMessage || !toastIcon) {
        console.error('Toast component not found');
        return;
    }
    
    // Clear any existing timeout
    if (toastTimeout) {
        clearTimeout(toastTimeout);
        toastTimeout = null;
    }
    
    // Set message
    toastMessage.textContent = message;
    
    // Set styling and icon based on type
    if (type === 'success') {
        toastComponent.className = 'fixed top-4 right-4 p-4 rounded-xl shadow-xl z-50 opacity-0 transition-all duration-300 transform translate-x-full max-w-sm bg-gradient-to-r from-green-600 to-green-700 text-white';
        toastIcon.innerHTML = `
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
        `;
    } else if (type === 'error') {
        toastComponent.className = 'fixed top-4 right-4 p-4 rounded-xl shadow-xl z-50 opacity-0 transition-all duration-300 transform translate-x-full max-w-sm bg-gradient-to-r from-red-600 to-red-700 text-white';
        toastIcon.innerHTML = `
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
        `;
    } else {
        // Default styling for other types
        toastComponent.className = 'fixed top-4 right-4 p-4 rounded-xl shadow-xl z-50 opacity-0 transition-all duration-300 transform translate-x-full max-w-sm bg-gradient-to-r from-blue-600 to-blue-700 text-white';
        toastIcon.innerHTML = `
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
        `;
    }
    
    // Show toast with animation
    setTimeout(() => {
        toastComponent.classList.remove('opacity-0', 'translate-x-full');
        toastComponent.classList.add('opacity-100', 'translate-x-0');
    }, 10);
    
    // Auto-hide after duration
    toastTimeout = setTimeout(() => {
        hideToast();
    }, duration);
}

function hideToast() {
    const toastComponent = document.getElementById('toast-component');
    
    if (!toastComponent) {
        return;
    }
    
    // Clear timeout if exists
    if (toastTimeout) {
        clearTimeout(toastTimeout);
        toastTimeout = null;
    }
    
    // Hide toast with animation
    toastComponent.classList.remove('opacity-100', 'translate-x-0');
    toastComponent.classList.add('opacity-0', 'translate-x-full');
}

// Make functions globally available
window.showToast = showToast;
window.hideToast = hideToast;
