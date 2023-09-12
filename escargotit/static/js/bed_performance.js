//  this handles the animation of the Loading pop up when Generate Forecast button is clicked
document.addEventListener('DOMContentLoaded', function() {
    const generateForecastForm = document.getElementById('generateForecastForm');
    const generateForecastButton = document.getElementById('generateForecastButton');
    const modal = document.getElementById('myModal');

    generateForecastButton.addEventListener('click', function() {
        // Show the modal
        modal.style.display = 'block';

        // Create a hidden input element to store the action URL
        const actionInput = document.createElement('input');
        actionInput.type = 'hidden';
        actionInput.name = 'action_url';
        actionInput.value = window.location.pathname;

        // Append the hidden input to the form
        generateForecastForm.appendChild(actionInput);

        // Submit the form after a short delay to allow the modal to display
        setTimeout(function() {
            generateForecastForm.submit();
        }, 1000); // Adjust the delay as needed
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


// Get all elements with class "label"
const labels = document.querySelectorAll(".label");

// Animate each label element
labels.forEach(function(label) {
    // Get the data attributes for startValue, endValue, and duration
    let startValue = parseInt(label.dataset.start);
    let endValue = parseInt(label.dataset.end);
    let duration = parseInt(label.dataset.duration);

    animateNumbers(label, startValue, endValue, duration);
});
