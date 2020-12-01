
function get_blog_previews(category_filter, page_num){  // API call -- server returns paginated blog previews for rendering in blog overview page

    const request = new Request(`get_article_previews?filter=${category_filter}&page=${page_num}`)

    fetch(request)
    .then(response => response.json())
    .then(res => {

        const preview_container = document.querySelector("#blog-previews-container");
        preview_container.innerHTML = "";

        res.previews.forEach(preview => {

            const article_preview =`

            <div class="blog-card-container">

                <div onclick="viewItem('${preview.seo_url}')" class="blog-item-image-box">
                    <img class="blog-item-img-content" src="${preview.img}" alt="blog_img">
                </div>
            
                <div class="blog-item-text-content-container">
                    <div class="blog-item-text-headline">
                        <h2 onclick="viewItem('${preview.seo_url}')">${preview.title}</h2>
                    </div>
            
                    <div class="blog-item-content-snip">
                        <span>${preview.preview}</span><a class="blog-item-lnk" href="/blog/viewitem?article=${preview.seo_url}">... Pročitaj više</a>
                    </div>
                </div>
            </div>
            `

            preview_container.innerHTML = article_preview + preview_container.innerHTML;

        })

        pagination(res.total_pages, category_filter, page_num);  // Draw paginagion nums on page

    })
}

function filter_categories(category_filter){  // Applies active classname for selected category, and removes it from other options. 

    const all_filters = document.getElementsByClassName("filter-category-option")
    
    for(let i=0; i<all_filters.length; i++){

        if(all_filters[i].id.includes(`blog-category-filter-${category_filter}`)){
            all_filters[i].className="filter-category-option active";
        }

        else{
            all_filters[i].className="filter-category-option";
        }
    }

    get_blog_previews(category_filter, 1);  // Get previews with selected category
}

function pagination(total_pages, category_filter, current_page){  // Handles 'next' 'previous' and pagination page_numbers at the bottom of the page
    const max_page_nums = 3  // Controls the max number of page_num buttons per range
    const page_range = ((Math.ceil(current_page / max_page_nums) - 1) * max_page_nums) + 1;  // Calculates the first element of current page_range

    const pagination_nums_ul = document.querySelector("#pagination-numeration");

    const option_previous = document.querySelector("#blog-pagination-previous");
    const option_next = document.querySelector("#blog-pagination-next");

    pagination_nums_ul.innerHTML = "";

    for(let i=page_range; (i<page_range + max_page_nums && i<total_pages + 1); i++){
        let elem_className = (i == current_page) ? "class='pagination-page-current'" : "";

        const pagination_num = `<li ${elem_className} onclick="get_blog_previews('${category_filter}', ${i})">${i}</li>`;

        pagination_nums_ul.innerHTML = pagination_nums_ul.innerHTML + pagination_num;
    }

    if(page_range != 1) pagination_nums_ul.innerHTML = `<li onclick="get_blog_previews('${category_filter}', ${page_range - 1})"> ... </li>` + pagination_nums_ul.innerHTML;
    if(page_range + max_page_nums < total_pages) pagination_nums_ul.innerHTML = pagination_nums_ul.innerHTML + `<li onclick="get_blog_previews('${category_filter}', ${page_range + max_page_nums})"> ... </li>`

    if(current_page == 1) option_previous.className = "hide";

    else{
        option_previous.className = "";
        option_previous.setAttribute("onclick", `get_blog_previews("${category_filter}", "${parseInt(current_page) - 1}")`);
    }

    if(current_page < total_pages){
        option_next.className = ""
        option_next.setAttribute("onclick", `get_blog_previews("${category_filter}", "${parseInt(current_page) + 1}")`);
    }

    else option_next.className = "hide";

    if(window.scrollY > 700){  // Return view to top of previews if scrolled down

        const subNav = document.querySelector("body > div.blog-intro-header-divider > div");
        subNav.scrollIntoView();

    }
}

// ToDo redo this via classic href get request