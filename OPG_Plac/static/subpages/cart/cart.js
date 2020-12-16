let timer;

function update_item_quantity(index){
    const item_id = document.querySelector(`#item-id-${index}`).value;
    const quantity = document.querySelector(`#item-quantity-counter-${index}`).value;

    const view_overlay = document.querySelector("#overlay");

    view_overlay.style.visibility = "visible"; // Prevent further user input

    const csrf_token = document.querySelector("[name=csrfmiddlewaretoken]").value;

    const request = new Request("/update_cart_item_quantity", {
        headers: {"X-CSRFtoken": csrf_token}
    });


    fetch(request, {
        method: "PUT",
        mode: "same-origin",
        body: JSON.stringify({
            item_id: item_id,
            quantity: quantity
        }),
        credentials: "same-origin"
    })

    .then(response => {
        if (response.status === 200) location.reload();
        else
        {
            response.json()
            .then(res => {
                console.log(res.message);
                view_overlay.style.visibility = "";
                alert("Oops, nešto ne valja");
            })
        }
    })

}


function remove_item_from_cart(event, item_id){
    event.preventDefault();

    const csrf_token = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const request = new Request("/remove_item_from_cart", 
    {headers: {"X-CSRFtoken": csrf_token}});

    fetch(request, {
        method: "DELETE",
        mode: "same-origin",
        body: JSON.stringify({

            item_id: item_id

        }),
        credentials: "same-origin"
    })

    .then(response => {
        if(response.status === 200) location.reload();
        else
        {
            response.json()
            .then(res => console.log(res))
        }
    })
}


function add_sub(op, index){
    const input = document.querySelector(`#item-quantity-counter-${index}`);

    if(op === "add") input.value= parseInt(input.value) + 1;
    else if(op === "sub" && parseInt(input.value) > 0) input.value = parseInt(input.value) - 1;

    validate_input_quantity(index);
}


function validate_input_quantity(index){
    clearTimeout(timer);
    const input = document.querySelector(`#item-quantity-counter-${index}`);

    if(input.value != parseInt(input.value) || parseInt(input.value) === 0){
        input.value = 1;
        input.style.border = "solid 3px red";
    }

    else
    {
        input.style.border = "";
        timer = window.setTimeout(() => update_item_quantity(index), 500);
    }
}