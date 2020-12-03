

function flip_imgs(img_small_frame_elem){
    const img_big_frame = document.querySelector("#article-image-big");

    img_big_frame.src = img_small_frame_elem.firstElementChild.src;
}

function add_sub(op){
    const display = document.querySelector("#product-count-total");

    if(op === "add") display.innerHTML= parseInt(display.innerHTML) + 1;

    if(op === "sub" && parseInt(display.innerHTML) > 0) display.innerHTML = parseInt(display.innerHTML) - 1
}