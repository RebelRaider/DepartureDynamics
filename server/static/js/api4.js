var url_api = "http://89.232.176.235/";
var token = localStorage.getItem("token");
document.addEventListener("DOMContentLoaded", function () {
    

        url7 = url_api + "api/v1/model?token=" + token;
        var select_item = document.getElementById("select_1");

        fetch(url7, {
            method: 'GET',
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
            
            length = data.models.length;
            k = 0;
            console.log(data.models[0].model_name + ':' + data.models[0].model_type);

            while (k < length)
            {
                op = document.createElement('option');
                op.textContent = data.models[k].model_name + ':' + data.models[k].model_type;
                select_item.appendChild(op);
                k++;
            }
        })
        .catch(error => {
            // Обработка ошибки
            console.error('Validation Error:', error);
        });

    
})

function click_6()
    {
        predict_name = document.getElementById("model_name_1").value;
        var model_Select = document.getElementById("select_1");
        var model_type = model_Select.options[model_Select.selectedIndex].textContent;
        name1 = model_type.split(":");
        url8 = url_api + "api/v1/inference?token=" + token + "&model_name=" + name1[0] + "&predict_name=" + predict_name;
        var fileInput = document.getElementById("csv_file");
        var file = fileInput.files[0];
        var formData = new FormData();
        formData.append('file', file);
        fetch(url8, {
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
