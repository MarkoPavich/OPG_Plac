

function validate_inputs(){
    // Get elements

    let valid = true;

    const payment_opt_cod = document.querySelector("#payment-opt-cod");
    const payment_opt_transfer = document.querySelector("#payment_opt_transfer");

    const terms_accepted = document.querySelector("#accept-terms-chckbox").checked;

    const payment_options_container = document.querySelector("#payment-options-container");
    const accept_terms_container = document.querySelector("#accept-terms-hacky-tooltip-container");

    // Handle no payment option selected
    if(!payment_opt_cod.checked && !payment_opt_transfer.checked){
        valid = false;

        payment_options_container.setAttribute("data-tooltip", "Odaberite način plaćanja");
        payment_options_container.className = "payment-options-block error-tooltip";
    }

    else{
        payment_options_container.removeAttribute("data-tooltip");
        payment_options_container.className = "payment-options-block";
    }

    // Handle terms not accepted
    if(!terms_accepted){
        valid = false;

        accept_terms_container.setAttribute("data-tooltip", "Morate se složiti s općim uvjetima");
        accept_terms_container.className = "error-tooltip";
    }

    else{
        accept_terms_container.removeAttribute("data-tooltip");
        accept_terms_container.removeAttribute("class");
    }
}


