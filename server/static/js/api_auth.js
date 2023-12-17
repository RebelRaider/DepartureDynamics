var url_api = "http://89.232.176.235/";

document.addEventListener('DOMContentLoaded', function() {

    var authForm = document.getElementById('login-form');
    authForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        email1 = document.getElementById('username').value;
        password1 = document.getElementById('password').value;

        url1 = url_api + "api/v1/user/auth/sign-in?email=" + email1 + "&password=" + password1;

        fetch(url1, {
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
                console.log("error");
            } else {
                localStorage.setItem('token', data.token);
                window.location.replace('/lk');
            }
        })
        .catch(error => {
            // Обработка ошибки
            console.error('Validation Error:', error);
        });
    })

    var registerForm = document.getElementById('register_form');
    registerForm.addEventListener('submit', function(event){
        event.preventDefault();

        username2 = document.getElementById('name0').value;
        first_name2 = document.getElementById('name1').value;
        last_name2 = document.getElementById('name2').value;
        email2 = document.getElementById('email1').value;
        password2 = document.getElementById('password1').value;
        
        url2 = url_api + "api/v1/user/auth/sign-up?username=" + username2 + "&first_name=" + first_name2 + "&last_name=" + last_name2 + "&email=" + email2 + "&password=" + password2;


        fetch(url2, {
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
            location.reload();
        })
        .catch(error => {
            // Обработка ошибки
            console.error('Validation Error:', error);
        });
    })

})

