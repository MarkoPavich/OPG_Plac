
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

function openSidebar(event){  // Opens, and closes mobile hamburger menu. Disables navbar scroll listener and forces opaque layout while active.
    
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

// Enables selective load of listeners -- Pass 'noscroll' to disable navbar on top transparency 
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


function open_modal_signup_form(){
    const modal = document.querySelector("#modal_signup_form");

    modal.className = modal.className + " modal-active";
}


function close_modal_signup_form(){
    const modal = document.querySelector("#modal_signup_form");

    modal.className = "modal-bg"
}

