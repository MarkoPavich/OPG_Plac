document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#product-results-sort_filter").addEventListener("change", applySortFilter);
    selectAppliedSortOption();
})

function open_close_category_submenu(id, is_sidebar){  // Flips submenu_options classnames - shows or hides the menu

    const sidebar_prefix = is_sidebar ? "sidebar-" : "";

    const classNames = {
        "submenu_active": "product-subfilter-container show_submenu",
        "submenu_inactive": "product-subfilter-container ",
        "mark_menu_open": " submenu-open"
    };

    const target_block_element = document.querySelector(`#${sidebar_prefix}category-option-${id}`);
    const target_submenu_element = document.querySelector(`#${sidebar_prefix}submenu-option-${id}`);

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
            <a ${className} href="/proizvodi?category=${parent_category}&subcategory=${subcategory}">${subcategory}</a>
            </li>

            `
        })
    }
}

function do_pagination(total_pages, current_page, active_filter, active_subfilter, search_query){  // Handles 'next' 'previous' and pagination page_numbers
    const max_page_nums = 6  // Controls the max number of page_num buttons per range
    const page_range = ((Math.ceil(current_page / max_page_nums) - 1) * max_page_nums) + 1;  // Calculates the first element of current page_range

    const pagination_nums_ul = document.querySelector("#pagination-numeration");  // Gets the page_nums ul DOM element
    const option_previous = document.querySelector("#pagination-previous");  // Get the 'next and previous' options DOM elements
    const option_next = document.querySelector("#pagination-next");

    let page_param = window.location.search.replace(/[&\?]page=\w*&?/, "");  // RegExp page param from location search
    if(page_param[0] !== "?") page_param = "?" + page_param; // Add '?' to the beginning of the slug if regex removed it 

    if(page_param.length > 1) page_param = page_param + "&page=";  // Reformat search slug
    else page_param = page_param + "page=";

    const href_slug = window.location.pathname + page_param;
    

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

    if(current_page === 1) option_previous.className = "hide";
    else option_previous.firstElementChild.setAttribute("href", `${href_slug}${parseInt(current_page) - 1}`);

    if(current_page === total_pages || total_pages === 0) option_next.className = "hide";
    else option_next.firstElementChild.setAttribute("href", `${href_slug}${parseInt(current_page) + 1}`);

}

function open_side_filter_menu(){
    const sidebar = document.querySelector("#category-filter-mobile-side-menu-container");
    const sidebar_background = document.querySelector("#sidebar-active-background");

        sidebar.className = "category-filter-mobile-side-menu-container category_filter_active";
        sidebar_background.className = "active-close-background";
}


function close_side_filter_menu(){
    const sidebar = document.querySelector("#category-filter-mobile-side-menu-container");
    const sidebar_background = document.querySelector("#sidebar-active-background");

    sidebar.className = "category-filter-mobile-side-menu-container";
    sidebar_background.className = "";
}


function applySortFilter(event){
    const sort_filter = event.target.value;

    let search_slug = window.location.search.replace(/[&\?]sort=\w+&?/, "");  // RegExp remove sort_slug
    search_slug = search_slug.replace(/[&\?]?page=\w+&?/, "");  // RegExp remove page_slug

    console.log(search_slug)

    // Cleanup and reformat search_slug
    if(search_slug.length > 1) search_slug = search_slug + `&sort=${sort_filter}`;
    else{
        search_slug = search_slug.replace("?", "");
        search_slug = search_slug + `?sort=${sort_filter}`;
    }

    if(search_slug[0] !== "?") search_slug = "?" + search_slug;

    location.href = location.pathname + search_slug;
}


function selectAppliedSortOption(){
    const sort_filter = window.location.search.match(/[&\?]sort=(\w+)&?/);  // RegExp capture active sort filter
    const dropdown = document.querySelector("#product-results-sort_filter");

    let option_applied = false;  // flow control
    
    if(sort_filter){
        Object.keys(dropdown.options).forEach(key => {
            if(dropdown.options[key].value === sort_filter[1]){
                dropdown.options[key].setAttribute("selected", "selected");
                option_applied = true;
            } 
        })
    }

    if(!option_applied){  // Fallback
        Object.keys(dropdown.options).forEach(key => {
            if(dropdown.options[key].value === "name_asc") dropdown.options[key].setAttribute("selected", "selected");
        })
    }
}