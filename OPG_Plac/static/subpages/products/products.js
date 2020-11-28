
function open_close_category_submenu(id){  // Flips submenu_options classnames - shows or hides the menu

    const classNames = {
        "submenu_active": "product-subfilter-container show_submenu",
        "submenu_inactive": "product-subfilter-container",
        "mark_menu_open": " submenu-open"
    };

    const target_block_element = document.querySelector(`#category-option-${id}`);
    const target_submenu_element = document.querySelector(`#submenu-option-${id}`);

    if(target_submenu_element.className === classNames["submenu_inactive"]){
        target_submenu_element.className = classNames["submenu_active"];
        target_block_element.className = target_block_element.className + classNames["mark_menu_open"];

    } else{
        target_submenu_element.className = classNames["submenu_inactive"];
        target_block_element.className = target_block_element.className.replace(classNames["mark_menu_open"], "");
    }

    document.activeElement.getBoundingClientRect()
}


function mark_active(){
    const classNames = {
    }
}


function populate_submenu(subcategories_array, elem_id, parent_id){
    const elem = document.querySelector(`#${elem_id}`)

    if(subcategories_array.length === 0){
        const parent = document.querySelector(`#${parent_id}`)
        parent.getElementsByTagName("svg")[0].style = "visibility: hidden";
    }

    else{
        subcategories_array.forEach(subcategory => {
            elem.firstElementChild.innerHTML = elem.firstElementChild.innerHTML + `
            
            <li>
            <a href="${subcategory}">${subcategory}</a>
            </li>

            `
        })
    }
}