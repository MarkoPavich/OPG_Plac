
function filter_categories(category_filter){  // Applies active classname for selected category, and removes it from other options. 

    const all_filters = document.getElementsByClassName("filter-category-option")
    
    for(let i=0; i<all_filters.length; i++){

        if(all_filters[i].id.includes(`blog-category-filter-${category_filter}`)) all_filters[i].className="filter-category-option active";
        else all_filters[i].className="filter-category-option";

    }
}

function do_pagination(total_pages, current_page, active_filter){  // Handles 'next' 'previous' and pagination page_numbers
    const max_page_nums = 3  // Controls the max number of page_num buttons per range
    const page_range = ((Math.ceil(current_page / max_page_nums) - 1) * max_page_nums) + 1;  // Calculates the first element of current page_range

    const pagination_nums_ul = document.querySelector("#pagination-numeration");  // Gets the page_nums ul DOM element
    const option_previous = document.querySelector("#pagination-previous");  // Get the 'next and previous' options DOM elements
    const option_next = document.querySelector("#pagination-next");

    let href_slug  // Init request slug variable

    // Create appropriate request slug

    if(active_filter === "all") href_slug = "/blog/filter?page=";  // Creates the request slug based on current filters set by user
    else href_slug = `/blog/filter?category=${active_filter}&page=`
    

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

    if(current_page <= 1) option_previous.className = "hide";
    else option_previous.firstElementChild.setAttribute("href", `${href_slug}${parseInt(current_page) - 1}`);

    if(current_page >= total_pages || total_pages === 0) option_next.className = "hide";
    else option_next.firstElementChild.setAttribute("href", `${href_slug}${parseInt(current_page) + 1}`);
}