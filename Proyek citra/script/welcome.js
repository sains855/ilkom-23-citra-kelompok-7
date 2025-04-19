document.addEventListener("DOMContentLoaded", function() {
    // Animasi before/after untuk slide grayscale
    const before = document.querySelector(".image-before");
    const after = document.querySelector(".image-after");
    
    before.style.opacity = "1";
    after.style.opacity = "0";
    before.style.zIndex = "2";
    after.style.zIndex = "1";
    
    let isBeforeVisible = true;
    setInterval(() => {
        if (isBeforeVisible) {
            before.style.opacity = "0";
            after.style.opacity = "1";
            before.style.zIndex = "1";
            after.style.zIndex = "2";
        } else {
            before.style.opacity = "1";
            after.style.opacity = "0";
            before.style.zIndex = "2";
            after.style.zIndex = "1";
        }
        isBeforeVisible = !isBeforeVisible;
    }, 5000);
});
document.addEventListener("DOMContentLoaded", function() {
    const slider = document.getElementById("slider");
    let currentSlide = 0;
    const totalSlides = 3;
    let slideInterval;

    function updateSlider() {
        slider.style.transform = `translateX(-${currentSlide * 100}vw)`;
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % totalSlides;
        updateSlider();
        resetInterval();
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
        updateSlider();
        resetInterval();
    }

    function resetInterval() {
        clearInterval(slideInterval);
        slideInterval = setInterval(nextSlide, 8000);
    }

    // Make functions global for HTML onclick
    window.nextSlide = nextSlide;
    window.prevSlide = prevSlide;

    // Start auto-sliding
    slideInterval = setInterval(nextSlide, 8000);
});