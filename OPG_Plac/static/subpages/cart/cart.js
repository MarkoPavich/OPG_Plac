let timer;

function modify_item_quantity(index){
    const item_id = document.querySelector(`#item-id-${index}`).value;
    document.body.className = "no-tamper"

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
        timer = window.setTimeout(() => modify_item_quantity(index), 2000);
    }
}