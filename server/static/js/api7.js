var url_api = "http://89.232.176.235/";
var token = localStorage.getItem("token");


function click_feedback()
    {
        name_ = document.getElementById("name").value;
        email_ = document.getElementById("email").value;
        problema_ = document.getElementById("problema").value;

        url_feedback = url_api + "api/v1/feedback?fio=" + name_ + "&email=" + email_ + "&message=" + problema_;
        fetch(url_feedback, {
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
        })
        .catch(error => {
            // Обработка ошибки
            console.error('Validation Error:', error);
        });
    }
