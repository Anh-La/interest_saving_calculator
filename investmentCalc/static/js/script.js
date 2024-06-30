    document.addEventListener('DOMContentLoaded', function() {
        
        var initialAmountInput = document.getElementById('starting_amount');
        var initialRangeInput = document.getElementById('starting_amount_range');
        var periodInput = document.getElementById('number_of_years');
        var periodRangeInput = document.getElementById('number_of_years_range');
        var rateInput = document.getElementById('return_rate');
        var rateRangeInput = document.getElementById('return_rate_range');
        var additionalAmountInput = document.getElementById('annual_additional_contribution');
        var additionalRangeInput = document.getElementById('annual_additional_contribution_range');

        //submission on timer
        //format number
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
    function convertToJson() {
        let form = document.getElementById("dataForm");
        let formData = {};
        for (let i = 0; i < form.elements.length; i++) {
            let element = form.elements[i];
            if (element.type !== "submit") {
                formData[element.name] = element.value;
            }
        }   
    }
    