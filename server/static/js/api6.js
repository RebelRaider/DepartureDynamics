var url_api = "http://89.232.176.235/";
var token = localStorage.getItem("token");
url10=url_api + "api/v1/history/mail?token=" + token;
fetch(url10, {
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
    history_1 = document.getElementById("history1");

    length = data.result.length;
    k = 0;
    while (k < length)
    {
        tr1 = document.createElement('tr');
        th1 = document.createElement('td');
        th2 = document.createElement('td');
        th3 = document.createElement('td');
        th4 = document.createElement('td');
        th5 = document.createElement('td');
        th6 = document.createElement('td');
        a_1 = document.createElement('button');
        a_2 = document.createElement('button');
        predict_name = data.result[k].data_path.split("/");
        predict_file = data.result[k].save_to.split("/");
        date1 = data.result[k].created.split("T");
        console.log(predict_file[4]);
        th1.textContent = data.result[k].id;
        th2.textContent = predict_name[4];
        th3.textContent = "mail";
        th4.textContent = date1[0];
        a_1.textContent = "Скачать";
        a_1.href = url_api + data.result[k].data_path;
        a_1.download = url_api + data.result[k].data_path;
        th5.appendChild(a_1);
        
        a_2.textContent = "Удалить запись";
        a_2.addEventListener("click", Click_11(data.result[k].data_path));

        th6.appendChild(a_2);
            
        //th6.onclick = Click_11(data.result[k].predict_name);


        tr1.appendChild(th1);
        tr1.appendChild(th2);
        tr1.appendChild(th3);
        tr1.appendChild(th4);
        tr1.appendChild(th5);
        tr1.appendChild(th6);

        history_1.appendChild(tr1);
        k++;
    }
})
.catch(error => {
    // Обработка ошибки
    console.error('Validation Error:', error);
});

function Click_11(predict_name_1)
{
        url11 = url_api + "api/v1/mail/delete?token=" + token + "&name=" + predict_name_1;
        fetch(url11, {
            method: 'DELETE',
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

        
        
url12=url_api + "api/v1/model?token=" + token;
fetch(url12, {
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
    history_2 = document.getElementById("history1");

    length = data.models.length;
    k = 0;
    while (k < length)
    {
        tr1_1 = document.createElement('tr');
        th1_1 = document.createElement('th');
        th2_1 = document.createElement('th');
        th3_1 = document.createElement('th');
        th4_1 = document.createElement('th');
        th5_1 = document.createElement('th');
        th6_1 = document.createElement('th');
        a1_1 = document.createElement('button');
        date2 = data.models[k].created.split("T");
        th1_1.textContent = data.models[k].id;
        th2_1.textContent = data.models[k].model_name;
        th3_1.textContent = "model";
        th4_1.textContent = date2[0];
        th5_1.textContent = "-";
        a1_1.textContent = "Удалить запись";
        a1_1.addEventListener("click", Click_12(data.models[k].model_name));
        th6_1.appendChild(a1_1);
            
        //th5_1.onclick = Click_12(data.models[k].model_name );


        tr1_1.appendChild(th1_1);
        tr1_1.appendChild(th2_1);
        tr1_1.appendChild(th3_1);
        tr1_1.appendChild(th4_1);
        tr1_1.appendChild(th5_1);
        tr1_1.appendChild(th6_1);


        history_2.appendChild(tr1_1);
        k++;
    }
})
.catch(error => {
    // Обработка ошибки
    console.error('Validation Error:', error);
});

function Click_12(model_name)
{
    url13 = url_api + "api/v1/model/delete?token=" + token + "&model_name=" + model_name;
    fetch(url13, {
        method: 'DELETE',
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

url14=url_api + "api/v1/predict?token=" + token;
fetch(url14, {
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
    history_3 = document.getElementById("history1");

    length = data.predicts.length;
    k = 0;
    while (k < length)
    {
        tr1_2 = document.createElement('tr');
        th1_2 = document.createElement('th');
        th2_2 = document.createElement('th');
        th3_2 = document.createElement('th');
        th4_2 = document.createElement('th');
        th5_2 = document.createElement('th');
        th6_2 = document.createElement('th');
        a2 = document.createElement('button');
        a2_1 = document.createElement('button');
        date3 = data.predicts[k].created.split("T");

        predict_file_1 = data.predicts[k].predict_file.split("/");
        path__1= data.predicts[k].prediction;
        console.log(path__1);
        localStorage.setItem('bufer', path__1);

        predict_name_1 = data.predicts[k].predict_name.split("/");
        name1 = data.predicts[k].predict_name.split(".");
        th1_2.textContent = data.predicts[k].id;
        th2_2.textContent = data.predicts[k].predict_name;
        th3_2.textContent = "predict";
        th4_2.textContent = date3[0];
        a2.textContent = "Ссылка";
        a2.addEventListener("click", () => predict_dashboard(path__1))
        th5_2.appendChild(a2);
        a2_1.textContent = "Удалить запись";
        a2_1.addEventListener("click", Click_13(data.predicts))
        th6_2.appendChild(a2_1);

            
        //th6_2.onclick = Click_12(data.predicts[k].predict_name);


        tr1_2.appendChild(th1_2);
        tr1_2.appendChild(th2_2);
        tr1_2.appendChild(th3_2);
        tr1_2.appendChild(th4_2);
        tr1_2.appendChild(th5_2);
        tr1_2.appendChild(th6_2);


        history_3.appendChild(tr1_2);
        k++;
    }
})
.catch(error => {
    // Обработка ошибки
    console.error('Validation Error:', error);
});

function Click_13(predict_name)
{
url15 = url_api + "api/v1/predict/delete?token=" + token + "&predict_name=" + predict_name;
fetch(url15, {
    method: 'DELETE',
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

function predict_dashboard(path)
{
    window.location.replace("/dashboard");
}

