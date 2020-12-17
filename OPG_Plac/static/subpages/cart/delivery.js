

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