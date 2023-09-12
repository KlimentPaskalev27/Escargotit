
// Initialize the accordion
var accordions = document.querySelectorAll('.accordion-item');

accordions.forEach(function (accordion) {
    accordion.addEventListener('click', function () {
        this.classList.toggle('show');
    });
});

