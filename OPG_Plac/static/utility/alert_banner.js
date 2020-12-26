const classNames = {
    show: "alert-banner alert-show",
    remove: "alert-banner alert-goaway",
    hide: "alert-banner alert-hide"
};

let banner_timer;

function alert_banner_dismiss(){
    const banner = document.querySelector("#alert-banner");
    banner.className = classNames.remove;

    clearTimeout(banner_timer);
    banner_timer = window.setTimeout(() => {
        banner.className = classNames.hide;
    }, 270)
}

function alert_banner_show(){
    const banner = document.querySelector("#alert-banner");
    banner.className = classNames.show;

    clearTimeout(banner_timer);
    banner_timer = setTimeout(alert_banner_dismiss, 2000); // Auto dismiss after 2sec
}