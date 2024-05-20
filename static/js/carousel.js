const carousel = document.querySelector('.carousel');
const slides = document.querySelectorAll('.carousel-item');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');

let currentIndex = 0;

// Move to next slide
nextBtn.addEventListener('click', () => {
    console.log("Next")
    currentIndex = (currentIndex + 1) % slides.length;
    updateCarousel();
});

// Move to previous slide
prevBtn.addEventListener('click', () => {
    console.log("Prev")
    currentIndex = (currentIndex - 1 + slides.length) % slides.length;
    updateCarousel();
});

// Update carousel slide
function updateCarousel() {
    const offset = -currentIndex * 770;
    document.querySelector('.carousel-container').style.transform = "translateX(" + offset + "px)";
}