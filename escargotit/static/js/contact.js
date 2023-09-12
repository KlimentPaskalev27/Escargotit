
// Initialize the accordion
$(document).ready(function() {
    // Add the 'show' class to the first FAQ item to expand it by default
    $('.accordion .card:first').addClass('show');

    // Handle accordion toggle
    $('.accordion .btn-link').click(function() {
        $(this).closest('.card').toggleClass('show');
        $(this).closest('.card').siblings().removeClass('show');
    });
});
