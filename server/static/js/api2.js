var url_api = "http://89.232.176.235/";

document.addEventListener('DOMContentLoaded', function() {

    username_me = document.getElementById("username_me");
    first_name_me = document.getElementById("first_name_me");
    last_name_me = document.getElementById("last_name_me");
    email_me = document.getElementById("email_me");
    password_me = document.getElementById("password_me");
    token = localStorage.getItem("token");

    url3 = url_api + "api/v1/me?token=" + token;
    console.log(url3);
    fetch(url3, {
        method: 'GET',

    }).then(response => {
        return response.json();
    })
    .then(data => {
        // Обработка успешного ответа
        console.log('Successful Response:', data);
        
        username_me.value = data.username;
        first_name_me.value = data.first_name;
        last_name_me.value = data.last_name;
        email_me.value = data.email;
    })
    .catch(error => {
        // Обработка ошибки
        console.error('Validation Error:', error);
    });



})

function Reset_Password() {
    old_password = document.getElementById("old_password").value;
    new_password = document.getElementById("new_password").value;
    url4= url_api + "api/v1/user/reset_password?token=" + token + "&old=" + old_password + "&new=" + new_password;

    fetch(url4, {
        method: 'POST',
        headers: {

        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Обработка успешного ответа
        console.log('Successful Response:', data);
        
        if (data.status == false)
        {
            console.log("not reset");
        } else {
            console.log("succes reset");
        }
    })
    .catch(error => {
        // Обработка ошибки
        console.error('Validation Error:', error);
    });
}