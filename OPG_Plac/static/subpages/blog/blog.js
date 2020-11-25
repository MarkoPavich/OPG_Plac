
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
                        <span>${preview.preview}</span><a class="blog-item-lnk" href="#">... Pročitaj više</a>
                    </div>
                </div>
            </div>
            `

            preview_container.innerHTML = article_preview + preview_container.innerHTML;

        })

        pagination(res.total_pages, category_filter, page_num);  // Draw paginagion nums on page

    })
}

function filter_categories(category_filter){
    current_filter = category_filter

    const all_filters = document.getElementsByClassName("filter-category-option")
    
    for(let i=0; i<all_filters.length; i++){

        if(all_filters[i].id.includes(`blog-category-filter-${category_filter}`)){
            all_filters[i].className="filter-category-option active";
        }

        else{
            all_filters[i].className="filter-category-option"
        }
    }

    get_blog_previews(category_filter, 1);
}

function pagination(total_pages, category_filter, current_page){
    const pagination_nums_ul = document.querySelector("#pagination-numeration");

    pagination_nums_ul.innerHTML = "";

    for(let i=1; i<total_pages + 1; i++){
        let elem_className = (i == current_page) ? "class='pagination-page-current'" : "";

        const pagination_num = `<li ${elem_className} onclick="get_blog_previews('${category_filter}', ${i})">${i}</li>`;

        pagination_nums_ul.innerHTML = pagination_nums_ul.innerHTML + pagination_num;
    }

    if(window.scrollY > 700){  // Return view to top of previews if scrolled down

        const subNav = document.querySelector("body > div.blog-intro-header-divider > div");
        subNav.scrollIntoView();

    }

 
}