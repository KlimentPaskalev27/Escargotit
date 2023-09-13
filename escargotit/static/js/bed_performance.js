//  this handles the animation of the Loading pop up when Generate Forecast button is clicked
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('myModal');
    const generateHatchForecastButton = document.getElementById('generateHatchForecastButton');
    const generateMortalityForecastButton = document.getElementById('generateMortalityForecastButton');
    const generateMaturityForecastButton = document.getElementById('generateMaturityForecastButton');

    const loadingBar = document.getElementById('loadingBar');

    generateHatchForecastButton.addEventListener('click', function(event) {
        modal.style.display = 'block';
    });

    generateHatchForecastButton.addEventListener('click', function(event) {
        let width = 0;
        const interval = 200; // Interval in milliseconds
        const step = 1; // Increase width by 1% per step

        const animation = setInterval(function() {
            if (width >= 100) {
                clearInterval(animation);
            } else {
                width += step;
                loadingBar.style.width = width + '%';
            }
        }, interval);
    });

    generateMortalityForecastButton.addEventListener('click', function(event) {
        modal.style.display = 'block';
    });

    generateMortalityForecastButton.addEventListener('click', function(event) {
        let width = 0;
        const interval = 200; // Interval in milliseconds
        const step = 1; // Increase width by 1% per step

        const animation = setInterval(function() {
            if (width >= 100) {
                clearInterval(animation);
            } else {
                width += step;
                loadingBar.style.width = width + '%';
            }
        }, interval);
    });

    generateMaturityForecastButton.addEventListener('click', function(event) {
        modal.style.display = 'block';
    });

    generateMaturityForecastButton.addEventListener('click', function(event) {
        let width = 0;
        const interval = 200; // Interval in milliseconds
        const step = 1; // Increase width by 1% per step

        const animation = setInterval(function() {
            if (width >= 100) {
                clearInterval(animation);
            } else {
                width += step;
                loadingBar.style.width = width + '%';
            }
        }, interval);
    });
});



// Function to animate numbers incrementally
function animateNumbers(element, startValue, endValue, duration) {
    let range = endValue - startValue;
    let current = startValue;
    let increment = endValue > startValue ? 1 : -1;
    let stepTime = Math.abs(Math.floor(duration / range));
    let timer = setInterval(function() {
        current += increment;
        element.textContent = current;
        if (current === endValue) {
            clearInterval(timer);
        }
    }, stepTime);
}


// get all elements with class "label" and then
// animate each label element
const labels = document.querySelectorAll(".label");
labels.forEach(function(label) {
    // get the data attributes for startValue, endValue, and duration
    let startValue = parseInt(label.dataset.start);
    let endValue = parseInt(label.dataset.end);
    let duration = parseInt(label.dataset.duration);

    animateNumbers(label, startValue, endValue, duration);
});
