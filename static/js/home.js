const prev = document.querySelector("#prev");
const next = document.querySelector("#next");

const slides = document.querySelectorAll(".home-slide");

let currentIndex = 0;

next.addEventListener("click", handleNextClicked);
prev.addEventListener("click", handlePrevClicked);

function handleNextClicked() {
    let currentPage = slides[currentIndex];
    currentPage.classList.remove("current");
    currentIndex++;
    if (currentIndex >= slides.length) {
        currentIndex = slides.length - 1;
    }
    slides[currentIndex].classList.add("current");
}


function handlePrevClicked() {
    let currentPage = slides[currentIndex];
    currentPage.classList.remove("current");
    currentIndex--;
    if (currentIndex < 0) {
        currentIndex = 0;
    }
    slides[currentIndex].classList.add("current");
}





