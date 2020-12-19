

function show_hide_delivery_form(){
    const same_delivery = document.querySelector("#same-delivery-chckbox").checked;
    const blanket = document.querySelector("#delivery-block-blanket");

    if(same_delivery) blanket.className = "delivery-block-blanket";
    else blanket.className = "blanket-visible";
}


function show_hide_r1_form(){
    const need_r1 = document.querySelector("#need-r1-chckbox").checked;
    const blanket = document.querySelector("#r1-blanket");

    if(need_r1) blanket.className = "blanket-visible";
    else blanket.className = "delivery-block-blanket";

}


function validate_pcode_input(input){

    if(input.value != ""){

        const last_char = input.value[input.value.length - 1];

        // If input is not a number, or input has more than 5 chars -- remove last char
        if((last_char != parseInt(last_char)) || input.value.length > 5){
            input.value = input.value.slice(0, input.value.length - 1);
            is_valid = false;
        }
    }
}


function validate_phone_num(input){
    if(input.value != ""){
        const last_char = input.value[input.value.length - 1];

        if(last_char != parseInt(last_char)) input.value = input.value.slice(0, input.value.length - 1);
    }
}


function validate_OIB(input){
    if(input.value != ""){
        const last_char = input.value[input.value.length - 1];

        if((last_char != parseInt(last_char)) || input.value.length > 11) input.value = input.value.slice(0, input.value.length - 1);

    }
}


function submit_delivery_data(){
    // Flow control

    let submit = true;

    // Grab inputs

    const same_delivery = document.querySelector("#same-delivery-chckbox").checked;
    const need_r1 = document.querySelector("#need-r1-chckbox").checked;
    const remember_input = document.querySelector("#remember-input-chckbox");

    const user_input = {
        name: document.querySelector("#name"),
        surname: document.querySelector("#surname"),
        address: document.querySelector("#address"),
        post_code: document.querySelector("#post_code"),
        place: document.querySelector("#place"),
        phone: document.querySelector("#phone")
    }

    const delivery_input = {
        delivery_name: document.querySelector("#delivery_name"),
        delivery_surname: document.querySelector("#delivery_surname"),
        delivery_address: document.querySelector("#delivery_address"),
        delivery_post_code: document.querySelector("#delivery_post_code"),
        delivery_place: document.querySelector("#delivery_place"),
        delivery_phone: document.querySelector("#delivery_phone")
    }

    const company_input = {
        company_name: document.querySelector("#company_name"),
        OIB: document.querySelector("#OIB"),
        company_place: document.querySelector("#company_place"),
        company_post_code: document.querySelector("#company_post_code")
    }

    // verify fields not empty
    Object.keys(user_input).forEach(key => {
        if(!valide_fields(user_input, key)) submit = false;
    })

    if(!same_delivery){   // Validate delivery data, if is_same unchecked
        Object.keys(delivery_input).forEach(key => {
            if(!valide_fields(delivery_input, key)) submit = false;
        })
    }

    if(need_r1){  // Validate company data, if user needs r1
        Object.keys(company_input).forEach(key => {
            if(!valide_fields(company_input, key)) submit = false;
        })
    }

    console.log(submit)
    
}


// submit_delivery_data() helper -- Validates fields, and applies or clears tooltips and error classnames
function valide_fields(fields, key){
    const container = document.querySelector(`#${key}-container`);
    let is_valid = true;

    if(fields[key].value === ""){ // Check if empty
        is_valid = false;

        container.setAttribute("data-tooltip", "Ovo polje je obavezno");
        container.className = "error-tooltip";
    }
    else{ // else handoff to other checks

        const content = validate_strict_fields(fields[key], key)

        if(content.valid){  // If valid, remove possible tooltip and tooltip class
            container.removeAttribute("data-tooltip");
            container.className = "";
        }
        else{
            is_valid = false; // If not valid, set tooltip and tooltip class

            container.setAttribute("data-tooltip", content.tooltip);
            container.className = "error-tooltip";
        }

    }

    return is_valid;
}


// submit_delivery_data() helper -- verifies OIB and post code correct length, can be expanded for other checks
function validate_strict_fields(input, key){

    if(key.includes("post_code")){ // Check if post_code exactly 5 nums
        if(input.value.length != 5 || (input.value != parseInt(input.value))){
            return {valid: false, tooltip: "Polje mora sadržavati 5 znamenaka"};
        }
        else return {valid: true};
    }

    else if(key.includes("OIB")){  // Check if OIB exactly 11 nums
        if(input.value.length != 11 || (input.value != parseInt(input.value))){
            return {valid: false, tooltip: "Polje mora sadržavati 11 znamena"};
        }
        else return {valid: true};
    }

    else return {valid: true};
}