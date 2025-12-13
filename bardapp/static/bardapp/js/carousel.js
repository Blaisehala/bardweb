// static/js/carousel.js

class HeroCarousel {
    constructor() {
        this.slides = document.querySelectorAll('.hero-carousel-slide');
        this.indicators = document.querySelectorAll('.hero-carousel-indicator');
        this.prevBtn = document.getElementById('prevBtn');
        this.nextBtn = document.getElementById('nextBtn');
        this.currentSlide = 0;
        this.autoPlayInterval = null;
        
        console.log('Carousel initialized:', {
            slides: this.slides.length,
            indicators: this.indicators.length,
            prevBtn: !!this.prevBtn,
            nextBtn: !!this.nextBtn
        });
        
        if (this.slides.length > 0) {
            this.init();
        }
    }

    init() {
        // Indicator clicks
        this.indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', () => {
                console.log('Indicator clicked:', index);
                this.goToSlide(index);
                this.resetAutoPlay();
            });
        });

        // Arrow clicks
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => {
                console.log('Previous button clicked');
                this.previousSlide();
                this.resetAutoPlay();
            });
        }

        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => {
                console.log('Next button clicked');
                this.nextSlide();
                this.resetAutoPlay();
            });
        }

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') {
                this.previousSlide();
                this.resetAutoPlay();
            } else if (e.key === 'ArrowRight') {
                this.nextSlide();
                this.resetAutoPlay();
            }
        });

        // Touch swipe support
        let touchStartX = 0;
        let touchEndX = 0;

        const carouselContainer = this.slides[0].parentElement;

        carouselContainer.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        });

        carouselContainer.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            this.handleSwipe(touchStartX, touchEndX);
        });

        // Start autoplay
        this.startAutoPlay();
    }

    handleSwipe(startX, endX) {
        if (endX < startX - 50) {
            this.nextSlide();
            this.resetAutoPlay();
        }
        if (endX > startX + 50) {
            this.previousSlide();
            this.resetAutoPlay();
        }
    }

    goToSlide(index) {
        console.log('Going to slide:', index);
        
        // Remove active state from current slide
        this.slides[this.currentSlide].classList.remove('opacity-100', 'pointer-events-auto');
        this.slides[this.currentSlide].classList.add('opacity-0', 'pointer-events-none');
        
        // Update indicator - remove active state
        this.indicators[this.currentSlide].classList.remove('w-8', 'rounded-md', 'bg-white');
        this.indicators[this.currentSlide].classList.add('w-2.5', 'rounded-full', 'bg-white/50');
        
        // Update current slide index
        this.currentSlide = index;
        
        // Add active state to new slide
        this.slides[this.currentSlide].classList.remove('opacity-0', 'pointer-events-none');
        this.slides[this.currentSlide].classList.add('opacity-100', 'pointer-events-auto');
        
        // Update indicator - add active state
        this.indicators[this.currentSlide].classList.remove('w-2.5', 'rounded-full', 'bg-white/50');
        this.indicators[this.currentSlide].classList.add('w-8', 'rounded-md', 'bg-white');
    }

    nextSlide() {
        const next = (this.currentSlide + 1) % this.slides.length;
        this.goToSlide(next);
    }

    previousSlide() {
        const prev = (this.currentSlide - 1 + this.slides.length) % this.slides.length;
        this.goToSlide(prev);
    }

    startAutoPlay() {
        this.autoPlayInterval = setInterval(() => {
            this.nextSlide();
        }, 6000);
    }

    resetAutoPlay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
        }
        this.startAutoPlay();
    }
}

// Initialize carousel
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.hero-carousel-slide')) {
        new HeroCarousel();
    }
});