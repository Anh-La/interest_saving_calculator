
// Customise form
document.addEventListener('DOMContentLoaded', function() {
        
    var initialAmountInput = document.getElementById('starting_amount');
    var initialRangeInput = document.getElementById('starting_amount_range');
    var periodInput = document.getElementById('number_of_years');
    var periodRangeInput = document.getElementById('number_of_years_range');
    var rateInput = document.getElementById('return_rate');
    var rateRangeInput = document.getElementById('return_rate_range');
    var additionalAmountInput = document.getElementById('annual_additional_contribution');
    var additionalRangeInput = document.getElementById('annual_additional_contribution_range');

    //match value field with value range
    initialAmountInput.addEventListener('input', function() {
        initialRangeInput.value = initialAmountInput.value;
    });

    initialRangeInput.addEventListener('input', function() {
        initialAmountInput.value = initialRangeInput.value;
    });

    periodInput.addEventListener('input', function() {
        periodRangeInput.value = periodInput.value;
    });

    periodRangeInput.addEventListener('input', function() {
        periodInput.value = periodRangeInput.value;
    });

    rateInput.addEventListener('input', function() {
        rateRangeInput.value = rateInput.value;
    });

    rateRangeInput.addEventListener('input', function() {
        rateInput.value = rateRangeInput.value;
    });

    additionalAmountInput.addEventListener('input', function() {
        additionalRangeInput.value = additionalAmountInput.value;
    });

    additionalRangeInput.addEventListener('input', function() {
        additionalAmountInput.value = additionalRangeInput.value;
    });
    
    
});

// Function to convert data from the form to Json
$(document).ready(function() {
    // Function to update results on form change
    $('#dataForm input').on('input', function() {
        // Serialize form data to send via AJAX
        var formData = $('#dataForm').serializeArray();

        // Convert form data to JSON
        var jsonData = convertToJson(formData);

        // Save JSON to a file using Blob and URL.createObjectURL
        var blob = new Blob([jsonData], { type: 'application/json' });
        var url = URL.createObjectURL(blob);

        // Create a link element to trigger the download
        var a = document.createElement('a');
        a.href = url;
        a.download = 'input.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        // Send AJAX request to update results (optional)
        $.ajax({
            type: 'POST',
            url: '{% url "index" %}',  // Replace with your view URL
            data: formData,
            success: function(response) {
                // Update results on success
                $('#results').html(response);
            }
        });
    });

    // Function to convert form data to JSON
    function convertToJson(formData) {
        var formDataObject = {};
        $(formData).each(function(index, obj) {
            formDataObject[obj.name] = obj.value;
        });

        var jsonData = JSON.stringify(formDataObject);
        console.log(jsonData); // Optional: Log JSON data for debugging

        return jsonData;
    }
});

