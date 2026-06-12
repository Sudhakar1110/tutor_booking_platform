/* ============================================================
   TUTOR BOOKING PLATFORM - Website JavaScript
   Frappe v15 + ERPNext v15 Compatible
   ============================================================ */

(function() {
    'use strict';

    // ========== NAVBAR TOGGLE ==========
    window.toggleNavbar = function() {
        var links = document.getElementById('navbarLinks');
        if (links) {
            links.classList.toggle('open');
        }
    };

    // Close navbar when clicking outside
    document.addEventListener('click', function(e) {
        var navbar = document.querySelector('.navbar');
        var links = document.getElementById('navbarLinks');
        if (navbar && links && !navbar.contains(e.target)) {
            links.classList.remove('open');
        }
    });

    // ========== FAQ ACCORDION ==========
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.faq-question').forEach(function(btn) {
            btn.addEventListener('click', function() {
                this.classList.toggle('active');
                var answer = this.nextElementSibling;
                if (answer) {
                    answer.classList.toggle('open');
                }
            });
        });
    });

    // ========== FORM SUBMISSION HANDLING ==========
    document.addEventListener('DOMContentLoaded', function() {
        // Handle all AJAX form submissions
        document.querySelectorAll('form[data-ajax="true"], form.contact-form, ' +
            '#studentRegistrationForm, #tutorRegistrationForm, #loginForm, ' +
            '#bookingForm, #demoClassForm').forEach(function(form) {
            form.addEventListener('submit', function(e) {
                var action = this.getAttribute('action');
                // Only handle API method calls
                if (action && action.includes('/api/method/')) {
                    e.preventDefault();
                    submitFormAjax(this);
                }
                // Regular form submissions proceed normally
            });
        });
    });

    // ========== AJAX FORM SUBMIT ==========
    function submitFormAjax(form) {
        var submitBtn = form.querySelector('button[type="submit"]');
        var originalText = submitBtn ? submitBtn.innerHTML : '';
        
        // Show loading
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        }

        var formData = new FormData(form);
        var actionUrl = form.getAttribute('action');

        // Submit via fetch
        fetch(actionUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Frappe-CSRF-Token': getCookie('csrf_token') || getCookie('X-Frappe-CSRF-Token')
            }
        })
        .then(function(response) { return response.json(); })
        .then(function(data) {
            // Show success message
            showAlert('success', 'Success! Your request has been submitted.');
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
            form.reset();
            
            // Redirect if provided
            if (data.redirect_url) {
                setTimeout(function() {
                    window.location.href = data.redirect_url;
                }, 1500);
            }
        })
        .catch(function(error) {
            showAlert('error', 'Something went wrong. Please try again.');
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        });
    }

    // ========== ALERT SYSTEM ==========
    function showAlert(type, message) {
        // Remove existing alerts
        document.querySelectorAll('.alert-dismissible').forEach(function(el) {
            el.remove();
        });

        var alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-' + (type === 'error' ? 'error' : 'success') + ' alert-dismissible';
        alertDiv.style.cssText = 'position:fixed;top:90px;right:20px;z-index:9999;max-width:400px;box-shadow:0 4px 12px rgba(0,0,0,0.15);animation:slideIn 0.3s ease;';
        alertDiv.innerHTML = '<span>' + (type === 'error' ? '❌' : '✅') + '</span> ' + message;
        
        document.body.appendChild(alertDiv);
        
        setTimeout(function() {
            alertDiv.style.opacity = '0';
            alertDiv.style.transition = 'opacity 0.3s ease';
            setTimeout(function() { alertDiv.remove(); }, 300);
        }, 4000);
    }

    // ========== COOKIE HELPER ==========
    function getCookie(name) {
        var value = '; ' + document.cookie;
        var parts = value.split('; ' + name + '=');
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    // ========== SMOOTH SCROLL ==========
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
            anchor.addEventListener('click', function(e) {
                var target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    });

    // ========== COUNTER ANIMATION ==========
    function animateCounters() {
        document.querySelectorAll('.hero-stat .number, .stat-card .number').forEach(function(el) {
            var text = el.textContent;
            var target = parseInt(text.replace(/[^0-9]/g, ''));
            if (isNaN(target) || target === 0) return;
            
            var suffix = text.replace(/[0-9]/g, '');
            var duration = 2000;
            var start = 0;
            var startTime = null;

            function step(timestamp) {
                if (!startTime) startTime = timestamp;
                var progress = Math.min((timestamp - startTime) / duration, 1);
                var current = Math.floor(progress * target);
                el.textContent = current.toLocaleString() + suffix;
                if (progress < 1) {
                    requestAnimationFrame(step);
                } else {
                    el.textContent = target.toLocaleString() + suffix;
                }
            }
            requestAnimationFrame(step);
        });
    }

    // Run counter animation when in viewport
    if ('IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    animateCounters();
                    observer.disconnect();
                }
            });
        });
        var heroStats = document.querySelector('.hero-stats');
        if (heroStats) observer.observe(heroStats);
    } else {
        // Fallback
        window.addEventListener('load', animateCounters);
    }

    // Add slide-in animation keyframes
    var style = document.createElement('style');
    style.textContent = '@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }';
    document.head.appendChild(style);

    console.log('Tutor Booking Platform - Website loaded successfully');
})();
