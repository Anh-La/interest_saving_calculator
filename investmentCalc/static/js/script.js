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

// Calculate result and return in the summary
function calculator() {
    //for summary table
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
    
    //for schedule table
    intSchedule();
    // let total_interest_on_deposit = 0;
    // let total_annual_additional_deposit = 0;
    // let total_deposit = 0;
    // let total_compound_interest = 0;
    // let total_saving_result = 0;

    // let tbody = document.getElementById('yearlyResults');
    // tbody.innerHTML = '';

    // for (let year = 1; year <= number_of_years; year++) {
    //     const interest_on_deposit = starting_amount * (return_rate / 100);
    //     const additional_investment = annual_additional_contribution;
    //     const compound_interest = (starting_amount + additional_investment) * (1 + return_rate / 100) - (starting_amount + additional_investment);
    //     const total_balance = starting_amount + additional_investment + compound_interest;

    //     total_interest_on_deposit += interest_on_deposit;
    //     total_annual_additional_deposit += additional_investment;
    //     total_deposit = starting_amount + total_additional_deposit;
    //     total_compound_interest += compound_interest;
    //     total_saving_result = total_balance;

    //     let row = tbody.insertRow();
    //     row.insertCell(0).innerText = year;
    //     row.insertCell(1).innerText = starting_amount.toFixed(2);
    //     row.insertCell(2).innerText = return_rate.toFixed(2);
    //     row.insertCell(3).innerText = interest_on_deposit.toFixed(2);
    //     row.insertCell(4).innerText = additional_investment.toFixed(2);
    //     row.insertCell(5).innerText = total_deposit.toFixed(2);
    //     row.insertCell(6).innerText = compound_interest.toFixed(2);
    //     row.insertCell(7).innerText = total_balance.toFixed(2);

    //     starting_amount += total_saving_result; // Update the starting amount for the next year
    // }
    // document.getElementById('totalInitialDeposit').innerText = (starting_amount - total_additional_deposit).toFixed(2);
    // document.getElementById('totalRate').innerText = return_rate.toFixed(2);
    // document.getElementById('totalInterestOnDeposit').innerText = total_interest_on_deposit.toFixed(2);
    // document.getElementById('totalAdditionalDeposit').innerText = total_annual_additional_deposit.toFixed(2);
    // document.getElementById('totalDeposit').innerText = total_deposit.toFixed(2);
    // document.getElementById('totalCompoundInterest').innerText = total_compound_interest.toFixed(2);
    // document.getElementById('totalResult').innerText = total_saving_result.toFixed(2);
};

function intSchedule() {
    // Ensure return_rate is defined and is a number
    let return_rate = parseFloat(document.getElementById('return_rate').value);
    if (isNaN(return_rate)) {
        return_rate = 0; // or handle error appropriately
    }

    let starting_amount = parseFloat(document.getElementById('starting_amount').value);
    let annual_additional_contribution = parseFloat(document.getElementById('annual_additional_contribution').value);
    let number_of_years = parseInt(document.getElementById('number_of_years').value, 10);
    
    //for schedule table
    let total_interest_on_deposit = 0;
    let total_annual_additional_deposit = 0;
    let total_deposit = 0;
    let total_compound_interest = 0;
    let total_saving_result = 0;

    let tbody = document.getElementById('yearlyResults');
    tbody.innerHTML = '';

    for (let year = 1; year <= number_of_years; year++) {
        const interest_on_deposit = starting_amount * (return_rate / 100);
        const additional_investment = annual_additional_contribution;
        const compound_interest = (starting_amount + additional_investment) * (1 + return_rate / 100) - (starting_amount + additional_investment);
        const total_balance = starting_amount + additional_investment + compound_interest;

        total_interest_on_deposit += interest_on_deposit;
        total_annual_additional_deposit += additional_investment;
        total_deposit = starting_amount + total_annual_additional_deposit;
        total_compound_interest += compound_interest;
        total_saving_result = total_balance;

        let row = tbody.insertRow();
        row.insertCell(0).innerText = year;
        row.insertCell(1).innerText = starting_amount.toFixed(2);
        row.insertCell(2).innerText = return_rate.toFixed(2);
        row.insertCell(3).innerText = interest_on_deposit.toFixed(2);
        row.insertCell(4).innerText = additional_investment.toFixed(2);
        row.insertCell(5).innerText = total_deposit.toFixed(2);
        row.insertCell(6).innerText = compound_interest.toFixed(2);
        row.insertCell(7).innerText = total_balance.toFixed(2);

        starting_amount += total_saving_result; // Update the starting amount for the next year
    }
    document.getElementById('totalInitialDeposit').innerText = (starting_amount - total_annual_additional_deposit).toFixed(2);
    document.getElementById('totalRate').innerText = return_rate.toFixed(2);
    document.getElementById('totalInterestOnDeposit').innerText = total_interest_on_deposit.toFixed(2);
    document.getElementById('totalAdditionalDeposit').innerText = total_annual_additional_deposit.toFixed(2);
    document.getElementById('totalDeposit').innerText = total_deposit.toFixed(2);
    document.getElementById('totalCompoundInterest').innerText = total_compound_interest.toFixed(2);
    document.getElementById('totalResult').innerText = total_saving_result.toFixed(2);
};
