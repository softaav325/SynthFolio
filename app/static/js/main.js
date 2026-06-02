/**
 * Main Application Logic
 * Handles: Theme switching, Scroll animations, Project filtering, Modals, and Form validation.
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // --- Theme Management ---
    const initTheme = () => {
        const themeToggleBtn = document.getElementById('theme-toggle');
        const darkIcon = document.getElementById('theme-toggle-dark-icon');
        const lightIcon = document.getElementById('theme-toggle-light-icon');

        if (!themeToggleBtn) return;

        const setTheme = (theme) => {
            if (theme === 'dark') {
                document.documentElement.classList.add('dark');
                if (lightIcon) lightIcon.classList.remove('hidden');
                if (darkIcon) darkIcon.classList.add('hidden');
            } else {
                document.documentElement.classList.remove('dark');
                if (lightIcon) lightIcon.classList.add('hidden');
                if (darkIcon) darkIcon.classList.remove('hidden');
            }
            localStorage.setItem('color-theme', theme);
        };

        // Initial load
        const savedTheme = localStorage.getItem('color-theme');
        const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setTheme(savedTheme || (systemDark ? 'dark' : 'light'));

        themeToggleBtn.addEventListener('click', () => {
            const isDark = document.documentElement.classList.contains('dark');
            setTheme(isDark ? 'light' : 'dark');
        });
    };

    // --- Scroll Animations (Intersection Observer) ---
    const initScrollAnimations = () => {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in-up');
                    entry.target.style.opacity = '1';
                    observer.unobserve(entry.target); // Animate only once
                }
            });
        }, observerOptions);

        // Target all elements with specific animation classes
        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            el.style.opacity = '0';
            observer.observe(el);
        });
    };

    // --- Project Filtering ---
    const initProjectFilter = () => {
        const filterBtns = document.querySelectorAll('.filter-btn');
        const projects = document.querySelectorAll('.project-card');

        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const category = btn.dataset.category;

                // Update buttons state
                filterBtns.forEach(b => {
                    b.classList.remove('active', 'bg-primary', 'text-white');
                    if (b === btn) btn.classList.add('active');
                });

                // Filter cards with a slight delay for smooth transition
                projects.forEach(card => {
                    if (category === 'all' || card.dataset.category === category) {
                        card.style.display = 'block';
                        setTimeout(() => { card.style.opacity = '1'; card.style.transform = 'translateY(0)'; }, 10);
                    } else {
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(20px)';
                        setTimeout(() => { card.style.display = 'none'; }, 300);
                    }
                });
            });
        });
    };

    // --- Modal Management ---
    const initModals = () => {
        const modals = document.querySelectorAll('[id^="modal-"]');
        
        // Close on backdrop click
        modals.forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.add('hidden');
                    document.body.style.overflow = 'auto';
                }
            });
        });
    };

    // --- Form Validation ---
    const initFormValidation = () => {
        const contactForm = document.querySelector('form[action*="contact"]');
        if (!contactForm) return;

        contactForm.addEventListener('submit', (e) => {
            const email = contactForm.querySelector('input[type="email"]');
            const message = contactForm.querySelector('textarea');
            
            let isValid = true;
            
            // Simple regex for email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email.value)) {
                alert('Пожалуйста, введите корректный адрес электронной почты.');
                isValid = false;
            }

            if (message.value.trim().length < 10) {
                alert('Сообщение слишком короткое. Пожалуйста, опишите вашу задачу подробнее.');
                isValid = false;
            }

            if (!isValid) e.preventDefault();
        });
    };

    // --- Smooth Scrolling ---
    const initSmoothScroll = () => {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    };

    // Launch all systems
    initTheme();
    initScrollAnimations();
    initProjectFilter();
    initModals();
    initFormValidation();
    initSmoothScroll();
});
