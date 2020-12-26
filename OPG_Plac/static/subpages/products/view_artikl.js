document.addEventListener("DOMContentLoaded", () => {

    document.querySelector("#product-count-total").addEventListener("change", validate_input_quantity);
    document.querySelector("#add-to-cart-btn").addEventListener("click", add_to_cart);

})

let item_id;


function set_item_id(id){
    item_id = id;
}


function flip_imgs(img_small_frame_elem){
    const img_big_frame = document.querySelector("#article-image-big");

    img_big_frame.src = img_small_frame_elem.firstElementChild.src;
}


function add_sub(op){
    const input = document.querySelector("#product-count-total");

    if(op === "add") input.value= parseInt(input.value) + 1;
    else if(op === "sub" && parseInt(input.value) > 0) input.value = parseInt(input.value) - 1;

    validate_input_quantity();
}


function validate_input_quantity(){
    const input = document.querySelector("#product-count-total");

    if(input.value != parseInt(input.value) || parseInt(input.value) === 0){
        input.value = 1;
        input.style.border = "solid 3px red";
    }

    else input.style.border = "";
}


function add_to_cart(){
    const btn = document.querySelector("#add-to-cart-btn");
    const input = document.querySelector("#product-count-total");
    
    const btn_cn_before = btn.className;
    const btn_txt_cn_before = btn.firstChild.className;
    
    const cart_icon_count = document.querySelector("#nav_cart_item_count");
    const cart_icon_count_copy = document.querySelector("#nav_cart_item_count_mobile");

    if(input.value != parseInt(input.value)  || parseInt(input.value) === 0) validate_input_quantity();

    else
    {

        // Apply loading behaviour to notify 'busy' to user
        btn.className = btn.className + " btn-loading";
        btn.firstChild.className = btn.firstChild.className + " btn-txt-loading";

        btn.removeEventListener("click", add_to_cart);  // Disable click listener

        const csrf_token = document.querySelector('[name=csrfmiddlewaretoken').value;
        const request = new Request(
            "/add_to_cart",
            {headers: {"X-CSRFtoken": csrf_token}});

        fetch(request, {
            method: "POST",
            body: JSON.stringify(
                {
                    item_id: item_id,
                    quantity: input.value
                }
            ),
            credentials: "same-origin"

        })

        .then(response => {
            switch (response.status)
            {
                case 200:

                    response.json()
                    .then(res => {

                        btn.className = btn_cn_before;
                        btn.firstChild.className = btn_txt_cn_before;
    
                        cart_icon_count.innerHTML = res.items_in_cart;
                        cart_icon_count_copy.innerHTML = res.items_in_cart;
                        window.localStorage.setItem("cart_count", res.items_in_cart)
    
                        btn.addEventListener("click", add_to_cart);
                        alert_banner_show();

                    })
                    break;

                case 404:
                    window.location.href = "/prijava";
                    break;
                
                default:
                    alert("Oops, nešto nije u redu..");
            }   

        })
    }
}