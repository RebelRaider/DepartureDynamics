var url_api = "http://89.232.176.235/";
var token = localStorage.getItem("token");




    function click_7()
    {
        path = document.getElementById("path");
        time1 = document.getElementById("time1").value;
        time2 = document.getElementById("time2").value;
        date1 = document.getElementById("date1");
        date2 = document.getElementById("date2");
        date3 = document.getElementById("date3");
        date4 = document.getElementById("date4");
        time1_1 = time1.split(":");
        time2_1 = time2.split(":");
        var fileInput = document.getElementById("csvfile");
        var file = fileInput.files[0];
        var formData = new FormData();
        formData.append('file', file);
        var url9 = url_api + "api/v1/mail/parse?token=" + token + "&start_date_baseline=" + date1.value + "T00:00:00&end_date_baseline=" + date2.value + "T00:00:00&start_date_comparison=" + date3.value + "T00:00:00&end_date_comparison=" + date4.value + "T00:00:00&work_start_time_hours=" + time1_1[0] + "&work_start_time_minutes=" + time1_1[1] + "&work_end_time_hours=" + time2_1[0] + "&work_end_time_minutes=" + time2_1[1] + "&path_to_save=" + path.value;
        console.log(url9);
//&start_date_baseline=2023-08-09&end_date_baseline=2023-09-09&start_date_comparison=2023-09-09end_date_comparison=2023-10-09&work_start_time_hours=08&work_start_time_minutes=00&work_end_time_hours=18&work_end_time_minutes=00&path_to_save=Test111
        fetch(url9, {
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