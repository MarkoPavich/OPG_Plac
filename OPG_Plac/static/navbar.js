
let navbar_scroll = "scroll";  // State variable


function adjust_navbar_width(){  // Switches between mobile (hamburger_menu) navbar, and regular navbar
    if(window.innerWidth < 500){
        document.querySelector("#nav-menu").className = "hide";
        document.querySelector("#toggle").className = "toggle";
    }

    else{
        document.querySelector("#nav-menu").className = "nav-menu";
        document.querySelector("#toggle").className = "hide";
    }

    if(document.querySelector("#nav_hamburger_sidebar").className === "nav-hamburger-sidebar sidebar-open") openSidebar();
}


function adjust_navbar_scroll(){  // Switches between navbar with transparent background without search, and vice versa. based on scroll position. 

    const navbar = document.querySelector("#navbar");
    const search_bar = document.querySelector("#nav-search-bar");
    
    if(window.scrollY >= 10){
        navbar.className = "navbar navbar-top";
        search_bar.className = "nav-search-bar";
    }
    
    else{
        navbar.className = "navbar";
        search_bar.className = "hide";
    }
}


function openSidebar(event){  // Opens and closes mobile hamburger menu. Disables navbar scroll listener and forces opaque layout while active.
    
    if(event != undefined) event.preventDefault();

    const sidebar = document.querySelector("#nav_hamburger_sidebar");
    const navbar = document.querySelector("#navbar");
    const search_bar = document.querySelector("#nav-search-bar");

    if(sidebar.className === "nav-hamburger-sidebar sidebar-hidden"){

        sidebar.className = "nav-hamburger-sidebar sidebar-open";

        navbar.className = "navbar navbar-top";
        search_bar.className = "nav-search-bar";

        if(navbar_scroll === "scroll"){
            window.removeEventListener("scroll", adjust_navbar_scroll);
        }

    }

    else{
        sidebar.className = "nav-hamburger-sidebar sidebar-hidden";

        if(navbar_scroll === "scroll"){
            adjust_navbar_scroll();
            window.addEventListener("scroll", adjust_navbar_scroll);
        }
    }

}


// Enables selective load of listeners -- Pass 'noscroll' to disable 'navbar on top' transparency 
function load_navbar_listeners(mode){   
    window.addEventListener("DOMContentLoaded", adjust_navbar_width);
    window.addEventListener("resize", adjust_navbar_width);

    const navbar = document.querySelector("#navbar");
    const search_bar = document.querySelector("#nav-search-bar");


    if(mode !== "noscroll"){
        adjust_navbar_scroll();
        window.addEventListener("scroll", adjust_navbar_scroll)
    }
    else {
        navbar.className = "navbar navbar-top";
        search_bar.className = "nav-search-bar";

        navbar_scroll = "noscroll"
    }
}


 // Modal signup window


function open_modal_signup_form(){
    const modal = document.querySelector("#modal_signup_form");

    modal.className = modal.className + " modal-active";
}


function close_modal_signup_form(event){
	if(event != undefined) event.preventDefault()

    const modal = document.querySelector("#modal_signup_form");

    const inputs = {
        first_name: document.querySelector("#signup_first_name"),
        last_name: document.querySelector("#signup_last_name"),
        email: document.querySelector("#signup_email"),
        password: document.querySelector("#signup_password"),
        pass_conf: document.querySelector("#signup_confirm_password")
    }

    // clear inputs on close
    Object.keys(inputs).forEach(key => {
    	inputs[key].style.border = "";
    	inputs[key].value = "";
    })

    modal.className = "modal-bg"
}


function submit_signup_form(event){  // Runs client-side form validation, and submits user registration data
    // Prevent default submit
    event.preventDefault()

    // flow and control variables
    let submit = true;
    const password_min_length = 8

    // Get input elements

    const inputs = {
        first_name: document.querySelector("#signup_first_name"),
        last_name: document.querySelector("#signup_last_name"),
        email: document.querySelector("#signup_email"),
        password: document.querySelector("#signup_password"),
        pass_conf: document.querySelector("#signup_confirm_password")
    }
    
    // Validate input data present
    Object.keys(inputs).forEach(key =>{
        if(inputs[key].value === ""){
            submit = false;
            inputs[key].style.border = "solid 2px red";
        } 

        else inputs[key].style.border = "";

    })

    // Validate passwords match

    if(inputs["password"].value != inputs["pass_conf"].value){
        submit = false;

        inputs["password"].style.border = "solid 2px red";
        inputs["pass_conf"].style.border = inputs["password"].style.border;

        inputs["password"].value = "";
        inputs["pass_conf"].value = "";

        inputs["password"].placeholder = "Lozinke se moraju podudarati !";
        inputs["pass_conf"].placeholder = inputs["password"].placeholder;

        submit = false;
    }

    // Validate Passwords adhere to min length
    else if(inputs["password"].value.length < password_min_length){
        inputs["password"].value = "";
        inputs["pass_conf"].value = "";

        inputs["password"].style.border = "solid 2px red";
        inputs["pass_conf"].style.border = inputs["password"].style.border;

        inputs["password"].placeholder = `Minimalno ${password_min_length} znakova`;
        inputs["pass_conf"].placeholder = inputs["password"].placeholder;

        submit = false;
    }

    // If all checks OK, submit user data to backend
    if(submit){
        document.body.style.cursor = "wait";  // notify user an action is under way 

        // Pack request with csrf_token
        const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const request = new Request(
            "/user_registration", 
            {headers: {"X-CSRFToken": csrf_token}})
        
        fetch(request,  
            {
                method: "POST",
                body: JSON.stringify(  // Pack user registration data in JSON
                    {
                        first_name: inputs["first_name"].value,
                        last_name: inputs["last_name"].value,
                        email: inputs["email"].value,
                        password: inputs["password"].value,
                        confirm_password: inputs["pass_conf"].value
                    }
                    
                ), credentials: "same-origin"
            })

            .then(response => {
                document.body.style.cursor = "";

                switch(response.status){
                	case 200:
	                	document.body.style.cursor = "";
                        close_modal_signup_form();
                        window.localStorage.removeItem("cart_count")
	                	location.reload();
	                	break;

	                case 400:
	                	document.body.style.cursor = "";

	                	response.json()
	                	.then(res => {

	                		if(res.error === "mail_already_exists"){

			                	inputs["email"].style.border = "solid 2px red";
	                			inputs["email"].value = "";
                				inputs["email"].placeholder = "email already exists !";

                            }

                            else if(res.error === "not_matching_passwords"){
                                alert("Passwords dont match, please try again");
                                close_modal_signup_form();
                            }
                            
                            else alert("Oops, Something went wrong, please try again, or later");
                        })
                        break;

                    default:
                        document.body.style.cursor = "";
	                	close_modal_signup_form();
                        alert("Oops, Something went wrong, please try again, or later from here");
                }
            }
        )
    }
}


function pull_cart_count(){
    const cart_icon_count = document.querySelector("#nav_cart_item_count");
    const cart_icon_mobile_copy = document.querySelector("#nav_cart_item_count_mobile");

    if(localStorage.getItem("cart_count") != null){
        cart_icon_count.innerHTML = localStorage.getItem("cart_count");
        cart_icon_mobile_copy.innerHTML = localStorage.getItem("cart_count");
    }

    else
    {
        const csrf_token = document.querySelector("[name=csrfmiddlewaretoken]").value;

        const request = new Request("/pull_cart_count", 
        {headers: {"X-CSRFtoken": csrf_token}}
        )

        fetch(request, {

            method: "GET",
            credentials: "same-origin",
            mode: "same-origin"

        })

        .then(response => {

            if(response.status === 200)
            {
                response.json()
                .then(res => {

                    cart_icon_count.innerHTML = res.in_cart;
                    cart_icon_mobile_copy.innerHTML = res.in_cart;
                    window.localStorage.setItem("cart_count", res.in_cart);

                })
            }

            else
            {
                response.json()
                .then(res => {
                    console.log(res.message);
                })
            }
        })
    }
}