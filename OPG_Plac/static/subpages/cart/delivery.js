

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
    // Grab inputs

    const same_delivery = document.querySelector("#same-delivery-chckbox").checked;
    const need_r1 = document.querySelector("#need-r1-chckbox").checked;

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

    Object.keys(delivery_input).forEach(key => {
        console.log(`${key}: ${delivery_input[key].value}`)
    })



}