

function submit_login(event){
    if(event != undefined) event.preventDefault();

    const email_field = document.querySelector("#login_form_email");
    const password_field = document.querySelector("#login_form_password");

    let submit = true;

    if(email_field.value === ""){
        email_field.style.border = "solid 2px red";
        email_field.placeholder = "Email područje je obavezno !"

        submit = false;
    }

    else{
        email_field.style.border = "";
        email_field.placeholder = "";
    }

    if(password_field.value === ""){
        password_field.style.border = "solid 2px red";
        password_field.placeholder = "Područje lozinke je obavezno !";

        submit = false;
    }

    else{
        password_field.style.border = "";
        password_field.placeholder = "";
    }

    if(submit){
        const csrf_token = document.querySelector('[name=csrfmiddlewaretoken').value;
        const request = new Request(
            "/login",
            {headers: {"X-CSRFtoken": csrf_token}}
        );

        document.body.style.cursor = "wait";  // Notify pending status to user

        fetch(request, {
            method: "POST",
            body: JSON.stringify(
                {
                    email: email_field.value,
                    password: password_field.value
                }
            )
        })
        .then(response => {
            switch (response.status)
            {
                case 200:
                    email_field.value = "";
                    password_field.value = "";
                    location.reload();
                    break;
                
                case 401:
                    email_field.value = "";
                    password_field.value = "";

                    email_field.style.border = "solid 2px red";
                    password_field.style.border = "solid 2px red";

                    email_field.placeholder = "Neispravan email ili lozinka";
                    password_field.placeholder = email_field.placeholder;
                    
                    document.body.style.cursor = "";
                    break;
                
                default:
                    alert("Oops, nešto ne valja");
                    document.body.style.cursor = "";
            }
        })
    }
}