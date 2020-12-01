
function open_close_category_submenu(id){  // Flips submenu_options classnames - shows or hides the menu

    const classNames = {
        "submenu_active": "product-subfilter-container show_submenu",
        "submenu_inactive": "product-subfilter-container ",
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


function populate_submenu(subcategories_array, elem_id, parent_id, parent_category, active_subcategory){
    const elem = document.querySelector(`#${elem_id}`)

    if(subcategories_array.length === 0){
        const parent = document.querySelector(`#${parent_id}`)
        parent.getElementsByTagName("svg")[0].style = "visibility: hidden";
    }

    else{
        subcategories_array.forEach(subcategory => {
            let className = subcategory === active_subcategory ? "class=active-subfilter" : "";

            elem.firstElementChild.innerHTML = elem.firstElementChild.innerHTML + `
            
            <li>
            <a ${className} href="/proizvodi/filter?category=${parent_category}&subcategory=${subcategory}">${subcategory}</a>
            </li>

            `
        })
    }
}

function do_pagination(total_pages, current_page, active_filter, active_subfilter){  // Handles 'next' 'previous' and pagination page_numbers
    const max_page_nums = 6  // Controls the max number of page_num buttons per range
    const page_range = ((Math.ceil(current_page / max_page_nums) - 1) * max_page_nums) + 1;  // Calculates the first element of current page_range

    const pagination_nums_ul = document.querySelector("#pagination-numeration");  // Gets the page_nums ul DOM element
    const option_previous = document.querySelector("#pagination-previous");  // Get the 'next and previous' options DOM elements
    const option_next = document.querySelector("#pagination-next");

    let href_slug  // Init request slug variable

    // Create appropriate request slug

    if(active_filter === "None") href_slug = "/proizvodi/filter?page=";  // Creates the request slug based on current filters set by user
    else href_slug = active_subfilter === "None" ? `/proizvodi/filter?category=${active_filter}&page=` : `/proizvodi/filter?category=${active_filter}&subcategory=${active_subfilter}&page=`;
    

    // Generate numerated page links

    for(let i=page_range; (i<page_range + max_page_nums && i<total_pages + 1); i++){
        let elem_className = (i == current_page) ? "class='pagination-page-current'" : "";

        const pagination_num = `<li ${elem_className}><a href='${href_slug}${i}'>${i}</a></li>`;

        pagination_nums_ul.innerHTML = pagination_nums_ul.innerHTML + pagination_num;
    }

    // Handle page_range jump options

    if(page_range != 1) pagination_nums_ul.innerHTML = `<li><a href='${href_slug}${page_range - 1}'> ... </a></li>` + pagination_nums_ul.innerHTML;
    if(page_range + max_page_nums < total_pages) pagination_nums_ul.innerHTML = pagination_nums_ul.innerHTML + `<li><a href='${href_slug}${page_range + max_page_nums}'> ... </a></li>`;


    // Handle previous - next buttons

    if(current_page == 1) option_previous.className = "hide";
    else option_previous.firstElementChild.setAttribute("href", `${href_slug}${parseInt(current_page) - 1}`);

    if(current_page == total_pages) option_next.className = "hide";
    else option_next.firstElementChild.setAttribute("href", `${href_slug}${parseInt(current_page) + 1}`);

}