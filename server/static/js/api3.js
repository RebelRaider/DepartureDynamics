var url_api = "http://89.232.176.235/";
var token = localStorage.getItem("token");


function click_5()
{
    var model_Select = document.getElementById("model_type");
    var model_type = model_Select.options[model_Select.selectedIndex].value;

    model_name = document.getElementById("model_name").value;
    url5 = url_api + "api/v1/ml/new_model/train?token=" + token + "&model_name=" + model_name;
    url6 = url_api + "api/v1/ml/new_model/optimize?token=" + token + "&model_name=" + model_name;
    var fileInput = document.getElementById("csv-file");
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('file', file);
    if (model_type == "model")
    {    
        fetch(url5, {
            method: 'POST',
            body: formData,

        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json();
        }).then(data => {
            // Обработка ответа от сервера
            console.log(data);

        })
        .catch(error => {
            console.error('Ошибка при отправке файла:', error);
        });
    } else 
    {
        fetch(url6, {
            method: 'POST',
            headers: {
    
            },
            body: formData,

        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json();
        }).then(data => {
            // Обработка ответа от сервера
            console.log(data);
        })
        .catch(error => {
            console.error('Ошибка при отправке файла:', error);
        });

    }
}