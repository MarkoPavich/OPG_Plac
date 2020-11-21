
function adjust_navbar(){  // Switches between mobile (hamburger_menu) navbar, and regular navbar
    if(window.innerWidth < 500){
        document.querySelector("#nav-menu").className = "hide";
        document.querySelector("#toggle").className = "toggle";
    }

    else{
        document.querySelector("#nav-menu").className = "nav-menu";
        document.querySelector("#toggle").className = "hide";
    }
}

// Enables selective load of listeners -- Pass 'noscroll' to disable navbar on top transparency 
function load_navbar_listeners(mode){   
    window.addEventListener("DOMContentLoaded", adjust_navbar);
    window.addEventListener("resize", adjust_navbar);

    let navbar = document.querySelector("#navbar");
    let search_bar = document.querySelector("#nav-search-bar");

    if(mode !== "noscroll"){

        window.addEventListener("scroll", () =>{
        
            if(window.scrollY >= 10){
                navbar.className = "navbar navbar-top";
                search_bar.className = "nav-search-bar";
            }
            
            else{
                navbar.className = "navbar";
                search_bar.className = "hide";
            }
        })
    }

    else {
        navbar.className = "navbar navbar-top";
        search_bar.className = "nav-search-bar";
    }
}

