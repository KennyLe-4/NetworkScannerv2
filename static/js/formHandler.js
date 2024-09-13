$(document).ready(function() {
    $('#scanForm').on('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        showSpinner(); // Show the spinner

        // Perform AJAX request
        $.ajax({
            url: '/', // Ensure this is the correct endpoint
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                // Handle the response from the server
                console.log(response);
                hideSpinner(); // Hide the spinner
                // Optionally, update the page with the results
            },
            error: function() {
                // Handle errors
                alert('An error occurred. Please try again.');
                hideSpinner(); // Hide the spinner
            }
        });
    });
});