/* Handles navbar search_bar result previews */

window.addEventListener("DOMContentLoaded", () => {   // Listen content loaded
	// Get elements
	const nav_search_bar = document.querySelector("#nav_search_bar_input");  
	const search_filters_box = document.querySelector("#nav-search-bar-search-filters-container");
	const search_bar = document.querySelector("#nav_search_bar_input");

	// Active classnames -- show or hide search results box
	const classNames = {
		show: "nav-search-bar-search-filters-container",
		hide: "nav-search-bar-search-filters-container hide-filters-box"
	}

	let search_delay;  // Used to bind timeOut triggered search_fn

	// Bound fn that links keyup listener to do_search fns. Makes possible for easy removeListener statement
	const link_search = function(){
		clearTimeout(search_delay); // Make sure not to call req for previous (most probably incomplete) input

		search_delay = setTimeout(() => { 
			get_search_results(search_filters_box, search_bar.value);
		}, 500)	// Allow some time for user to maybe add to query, before firing req
	}

	// Listen for searchbar focus
	nav_search_bar.addEventListener("focus", () => {
		search_filters_box.className = classNames.show; // enable results box

		search_bar.addEventListener("keyup", link_search);  // add keyup listener
	})

	// listen for loss of focus on input
	nav_search_bar.addEventListener("blur", () => {
		clearTimeout(search_delay); // prevent further req

		setTimeout(() => {
			search_filters_box.className = classNames.hide; // Remove results_box
			search_bar.removeEventListener("keyup", link_search);  // remove input keyup listener - prevent stacking and memory leaks
			search_filters_box.innerHTML = ""; // Clear previous results
		}, 200)  // Allow some time to process click events
	})
})


function get_search_results(search_filters_box, query){
	const csrf_token = document.querySelector("[name=csrfmiddlewaretoken]").value;
	
	const request = new Request(`/get_search_results?query=${query}`, {
		headers:{"X-CSRFtoken": csrf_token}
	})

	if(query != ""){
		fetch(request, {
			method: "GET",
			mode: "same-origin",
			credentials: "same-origin"
		})
		.then(response => {
			if(response.status === 200){
				response.json()
				.then(res => {
					render_search_results(search_filters_box, res.results);
				})
			}
		})
	}

	else search_filters_box.innerHTML = "";
}


function render_search_results(filters_box, results){
	filters_box.innerHTML = "";

	results.forEach(product => {
		const result_render = `
		        <div onclick="window.location.href='/proizvodi/viewitem/${product.seo_url}'" class="search-result-container">
		        	<a href="/proizvodi/viewitem/${product.seo_url}">
			            <div class="search-result-img-container">
			                <img src="${product.img}" alt="product_image">
			            </div>
		            </a>
			            <div class="search-result-info-container">
			                <a href="/proizvodi/viewitem/${product.seo_url}">${product.name}</a>
			                <div class="search-result-price-container">
								<a href="/proizvodi/viewitem/${product.seo_url}">${product.price}</a>
								<a href="/proizvodi/viewitem/${product.seo_url}">Kn</a>
			                </div>
			            </div>
		        </div>
		`

		filters_box.innerHTML = filters_box.innerHTML + result_render;
	})
}