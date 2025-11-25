// Debug utilities for the application

// Enable debug mode
window.DEBUG = true;

// Debug logging function
function debugLog(message, data = null) {
    if (window.DEBUG) {
        const timestamp = new Date().toISOString();
        console.log(`[${timestamp}] ${message}`, data || '');
    }
}

// Log all fetch requests
const originalFetch = window.fetch;
window.fetch = function(...args) {
    debugLog('🌐 Fetch request:', {
        url: args[0],
        method: args[1]?.method || 'GET',
        body: args[1]?.body
    });
    
    return originalFetch.apply(this, args)
        .then(response => {
            debugLog('📥 Fetch response:', {
                url: args[0],
                status: response.status,
                statusText: response.statusText,
                headers: Object.fromEntries(response.headers.entries())
            });
            return response;
        })
        .catch(error => {
            debugLog('❌ Fetch error:', error);
            throw error;
        });
};

// Log all console errors
const originalError = console.error;
console.error = function(...args) {
    debugLog('❌ Console error:', args);
    originalError.apply(console, args);
};

// Log page load
window.addEventListener('load', () => {
    debugLog('✅ Page loaded');
    debugLog('   URL:', window.location.href);
    debugLog('   User Agent:', navigator.userAgent);
});

// Log unhandled errors
window.addEventListener('error', (event) => {
    debugLog('❌ Unhandled error:', {
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
        error: event.error
    });
});

// Log unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
    debugLog('❌ Unhandled promise rejection:', event.reason);
});

debugLog('🔧 Debug mode enabled');

