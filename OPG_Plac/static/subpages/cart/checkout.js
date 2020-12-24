

function submit_confirmation(event){
    event.preventDefault()
    // Get elements

    let valid = true;;

    const payment_options = document.getElementsByName("paymentOption");
    let payment;

    const terms_accepted = document.querySelector("#accept-terms-chckbox").checked;

    const payment_options_container = document.querySelector("#payment-options-container");
    const accept_terms_container = document.querySelector("#accept-terms-hacky-tooltip-container");

    // get payment option
    payment_options.forEach(option => {
        if(option.checked) payment = option.value;
    })

    // Handle payment and no payment option selected
    if(payment === undefined){
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

    if(valid){
        const csrf_token = document.querySelector("[name=csrfmiddlewaretoken]").value;
        
        const request = new Request("/submit_confirmation", {
            headers: {"X-CSRFtoken": csrf_token}
        })

        fetch(request, {
            method: "POST",
            mode: "same-origin",
            body: JSON.stringify({

                payment_option: payment

            }),
            credentials: "same-origin"
        })

        .then(response => {
            if(response.status === 200){
                window.localStorage.removeItem("cart_count");
                location.href = "/Confirmation";
            }
            else alert("Oops, nešto ne valja");
        });

    }
}


