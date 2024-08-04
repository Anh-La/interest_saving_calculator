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

function intSchedule() {
    // Ensure return_rate is defined and is a number
    let return_rate = parseFloat(document.getElementById('return_rate').value) / 100;
    let starting_amount = parseFloat(document.getElementById('starting_amount').value);
    let annual_additional_contribution = parseFloat(document.getElementById('annual_additional_contribution').value);
    let number_of_years = parseInt(document.getElementById('number_of_years').value, 10);

    // Results calculation
    let total_interest_on_deposit = 0;
    let total_annual_additional_deposit = 0;
    let total_saving_result = starting_amount;

    let results = [];

    for (let year = 1; year <= number_of_years; year++) {
        const interest_on_deposit = total_saving_result * return_rate;
        total_interest_on_deposit += interest_on_deposit;

        total_annual_additional_deposit += annual_additional_contribution;

        const initial_deposit = total_saving_result;
        total_saving_result += annual_additional_contribution + interest_on_deposit;

        results.push({
            year: year,
            initial_deposit: initial_deposit.toFixed(2),
            rate: (return_rate * 100).toFixed(2),
            interest_on_deposit: interest_on_deposit.toFixed(2),
            additional_contribution: annual_additional_contribution.toFixed(2),
            total_balance: total_saving_result.toFixed(2)
        });
    }

    // Populate the table with results
    const tbody = document.getElementById('yearlyResults');
    if (tbody) {
        tbody.innerHTML = ''; // Clear existing rows

        results.forEach(result => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${result.year}</td>
                <td>${result.initial_deposit}</td>
                <td>${result.rate}</td>
                <td>${result.interest_on_deposit}</td>
                <td>${result.additional_contribution}</td>
                <td>${result.total_balance}</td>
            `;
            tbody.appendChild(row);
        });

        // Set the final values for totals
        document.getElementById('totalYear').innerText = number_of_years.toFixed(0);
        document.getElementById('totalRate').innerText = (return_rate * 100).toFixed(2);
        document.getElementById('totalInterestOnDeposit').innerText = total_interest_on_deposit.toFixed(2);
        document.getElementById('totalAdditionalDeposit').innerText = total_annual_additional_deposit.toFixed(2);
        document.getElementById('totalDeposit').innerText = (starting_amount + total_annual_additional_deposit).toFixed(2);
        document.getElementById('totalResult').innerText = total_saving_result.toFixed(2);
    } else {
        console.error('Element with ID "yearlyResults" not found.');
    }
}

function calculator() {
    // For summary table
    const number_of_years = parseFloat(document.getElementById('number_of_years').value);
    const starting_amount = parseFloat(document.getElementById('starting_amount').value);
    const annual_additional_contribution = parseFloat(document.getElementById('annual_additional_contribution').value);
    const return_rate = parseFloat(document.getElementById('return_rate').value);

    const total_additional_deposit = number_of_years * annual_additional_contribution;
    const total_interest = ((starting_amount * (1 + return_rate / 100) ** number_of_years) - starting_amount) + 
                            (total_additional_deposit * ((1 + return_rate / 100) ** number_of_years - 1) / (return_rate / 100));
    const total_result = starting_amount + total_additional_deposit + total_interest;

    document.getElementById('displayYears').innerText = number_of_years;
    document.getElementById('displayInitialDeposit').innerText = starting_amount.toFixed(2);
    document.getElementById('displayAdditionalSaving').innerText = total_additional_deposit.toFixed(2);
    document.getElementById('displayInterest').innerText = total_interest.toFixed(2);
    document.getElementById('displayTotalSaving').innerText = total_result.toFixed(2);
    
    // For schedule table
    intSchedule();
}

// Initial setup
document.addEventListener('DOMContentLoaded', function () {
    intSchedule();

    // Add event listeners to update the table and summary when inputs change
    document.getElementById('starting_amount').addEventListener('input', calculator);
    document.getElementById('number_of_years').addEventListener('input', calculator);
    document.getElementById('return_rate').addEventListener('input', calculator);
    document.getElementById('annual_additional_contribution').addEventListener('input', calculator);
});


document.addEventListener('DOMContentLoaded', (event) => {
    // Function to send results to Django
    function saveResults() {
        // Prepare the data from the tables
        const summaryData = {
            years: document.getElementById('displayYears').innerText,
            initialDeposit: document.getElementById('displayInitialDeposit').innerText,
            additionalSaving: document.getElementById('displayAdditionalSaving').innerText,
            interest: document.getElementById('displayInterest').innerText,
            totalSaving: document.getElementById('displayTotalSaving').innerText
        };

        const scheduleData = [];
        const rows = document.querySelectorAll('#yearlyResults tr');
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length > 0) {
                scheduleData.push({
                    year: cells[0].innerText,
                    initialDeposit: cells[1].innerText,
                    rate: cells[2].innerText,
                    interestOnDeposit: cells[3].innerText,
                    additionalContribution: cells[4].innerText,
                    //totalBalance: cells[5].innerText,
                    //compoundInterest: cells[6].innerText,
                    totalSavingResult: cells[5].innerText
                });
            }
        });

        const dataToSend = {
            summary: summaryData,
            schedule: scheduleData
        };

        // Send data to Django endpoint
        fetch('/save-json/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() // Function to get CSRF token from the form
            },
            body: JSON.stringify(dataToSend)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Utility function to get CSRF token
    function getCsrfToken() {
        const csrfTokenElement = document.querySelector('input[name="csrfmiddlewaretoken"]');
        return csrfTokenElement ? csrfTokenElement.value : '';
    }

    // Call saveResults function on button click or form submission
    document.getElementById('saveResultsButton').addEventListener('click', saveResults);
});
