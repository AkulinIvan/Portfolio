// Modern portfolio interactions with Josh Comeau inspired animations
class PortfolioApp {
  constructor() {
    this.init();
  }

  init() {
    this.setupEventListeners();
    this.setupIntersectionObserver();
    this.setupSmoothScrolling();
    this.setupPageTransitions();
    this.setupMicroInteractions();
    this.setupPerformanceMonitoring();
  }

  setupEventListeners() {
    // Navbar scroll effect
    window.addEventListener('scroll', this.handleScroll.bind(this));
    
    // Form submissions
    document.querySelectorAll('form').forEach(form => {
      form.addEventListener('submit', this.handleFormSubmit.bind(this));
    });

    // Keyboard navigation
    document.addEventListener('keydown', this.handleKeyboardNavigation.bind(this));
  }

  setupIntersectionObserver() {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          
          // Add stagger effect for children
          if (entry.target.children) {
            Array.from(entry.target.children).forEach((child, index) => {
              child.style.animationDelay = `${index * 0.1}s`;
            });
          }
        }
      });
    }, observerOptions);

    // Observe all animatable elements
    document.querySelectorAll('.card-modern, .skill-card, .project-card, .timeline-item').forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(30px)';
      el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      this.observer.observe(el);
    });
  }

  setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(anchor.getAttribute('href'));
        if (target) {
          const offset = 80;
          const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
          
          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      });
    });
  }

  setupPageTransitions() {
    // Add page transition on link clicks
    document.querySelectorAll('a[href^="/"]').forEach(link => {
      link.addEventListener('click', (e) => {
        if (link.target === '_blank' || link.hasAttribute('download')) return;
        
        e.preventDefault();
        const href = link.getAttribute('href');
        
        // Show page transition
        const transition = document.querySelector('.page-transition');
        if (transition) {
          transition.classList.add('active');
          
          setTimeout(() => {
            window.location.href = href;
          }, 500);
        }
      });
    });
  }

  setupMicroInteractions() {
    // Add hover effects to interactive elements
    document.querySelectorAll('.btn-modern, .btn-outline-modern').forEach(btn => {
      btn.addEventListener('mouseenter', () => {
        btn.style.transform = 'translateY(-3px) scale(1.05)';
      });
      
      btn.addEventListener('mouseleave', () => {
        btn.style.transform = 'translateY(0) scale(1)';
      });
    });

    // Add typing effect to hero title
    this.typeWriterEffect();
  }

  setupPerformanceMonitoring() {
    // Log performance metrics
    window.addEventListener('load', () => {
      const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
      console.log(`Page loaded in ${loadTime}ms`);
      
      // Send to analytics (placeholder)
      this.trackPerformance(loadTime);
    });
  }

  handleScroll() {
    const navbar = document.querySelector('.navbar-modern');
    const scrolled = window.pageYOffset > 50;
    
    if (navbar) {
      navbar.classList.toggle('scrolled', scrolled);
    }
  }

  handleFormSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (submitBtn) {
      this.showLoadingState(submitBtn);
      
      // Simulate API call
      setTimeout(() => {
        this.hideLoadingState(submitBtn);
        this.showSuccessMessage(form, 'Сообщение успешно отправлено!');
      }, 2000);
    }
  }

  handleKeyboardNavigation(e) {
    // Escape key closes modals
    if (e.key === 'Escape') {
      this.closeAllModals();
    }
    
    // Tab key management for accessibility
    if (e.key === 'Tab') {
      this.manageFocus(e);
    }
  }

  showLoadingState(button) {
    button.classList.add('loading');
    button.disabled = true;
    
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Отправка...';
    button.dataset.originalText = originalText;
  }

  hideLoadingState(button) {
    button.classList.remove('loading');
    button.disabled = false;
    button.innerHTML = button.dataset.originalText;
  }

  showSuccessMessage(form, message) {
    const successMsg = document.createElement('div');
    successMsg.className = 'alert alert-success mt-3';
    successMsg.innerHTML = `<i class="fas fa-check-circle me-2"></i>${message}`;
    successMsg.setAttribute('role', 'alert');
    
    form.appendChild(successMsg);
    
    // Remove after 5 seconds
    setTimeout(() => {
      successMsg.remove();
    }, 5000);
  }

  typeWriterEffect() {
    const heroTitle = document.querySelector('.hero-title');
    if (!heroTitle) return;
    
    const text = heroTitle.textContent;
    heroTitle.textContent = '';
    
    let i = 0;
    const speed = 100;
    
    function type() {
      if (i < text.length) {
        heroTitle.textContent += text.charAt(i);
        i++;
        setTimeout(type, speed);
      }
    }
    
    // Start typing after hero section animation
    setTimeout(type, 1000);
  }

  trackPerformance(loadTime) {
    // Send to your analytics service
    if (loadTime < 1000) {
      console.log('🚀 Excellent performance!');
    } else if (loadTime < 3000) {
      console.log('✅ Good performance');
    } else {
      console.log('⚠️ Performance needs improvement');
    }
  }

  closeAllModals() {
    // Close any open modals
    document.querySelectorAll('.modal.show').forEach(modal => {
      const modalInstance = bootstrap.Modal.getInstance(modal);
      if (modalInstance) {
        modalInstance.hide();
      }
    });
  }

  manageFocus(e) {
    // Manage focus for better accessibility
    const focusableElements = document.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
    
    if (e.shiftKey && document.activeElement === firstElement) {
      e.preventDefault();
      lastElement.focus();
    } else if (!e.shiftKey && document.activeElement === lastElement) {
      e.preventDefault();
      firstElement.focus();
    }
  }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new PortfolioApp();
  
  // Console greeting
  console.log('%c🚀 Добро пожаловать в мое портфолио!', 
    'color: #2E8B57; font-size: 18px; font-weight: bold;');
  console.log('%c💻 Сделано с любовью к коду и вниманием к деталям', 
    'color: #63B3ED; font-size: 14px;');
});

// Service Worker registration for PWA capabilities
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(registration => {
        console.log('SW registered: ', registration);
      })
      .catch(registrationError => {
        console.log('SW registration failed: ', registrationError);
      });
  });
}