$(document).ready(function() {
    $('.message a').click(function(){
        $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
    });
});

var url_api = "http://89.232.176.235";
$(document).ready(function () {
    $('.input-file input[type=file]').on('change', function(){
      let file = this.files[0];
      $(this).closest('.input-file').find('.input-file-text').html(file.name);
    });
  });
  var path1 = localStorage.getItem("bufer");
  var url_5 = url_api + path1 + ".csv";

  fetch(url_5)
  .then(response => {
    if (!response.ok) {
      throw new Error(`Ошибка загрузки файла: ${response.status} ${response.statusText}`);
    }
    return response.text();
  })
  .then(csvData => {
    // Используем PapaParse для парсинга CSV
    Papa.parse(csvData, {
      header: true, // Указываем, что первая строка содержит заголовки
      dynamicTyping: true, // Автоматически определяем тип данных
      complete: function(results) {
        // Результаты парсинга доступны в results.data
        const csvObject = {};

        results.data.forEach(row => {
          // Используем значение в колонке "emails" как ключ, а "predict" как значение
          csvObject[row.Email] = row.predict;
        });
        Email_csv = [];
        number_csv = [];  
        // Теперь у вас есть объект, где "emails" - ключи, "predict" - значения
        console.log(csvObject);
        var massive_csv = results.data.map(row => Object.values(row));

         /* var options = {
            chart: {
              type: 'bar'
            },
            series: [{
              name: 'sales',
              data: number_csv,
            }],
            xaxis: {
              categories: Email_csv,
            },
            plotOptions: {
              bar: {
                colors: {
                  ranges: [
                    { from: 0, to: 40, color: '#818181' }, // Серый для значений < 40
                    { from: 41, to: 69, color: '#8E9CFF' }, // Зеленый для значений от 40 до 70
                    { from: 70, to: 1000, color: '#6074FF' } // Красный для значений > 70
                  ]
                },
                columnWidth: '1%', // Ширина столбцов
              }
            }
          }
        
          var chart = new ApexCharts(document.getElementById("chart"), options);
          chart.render();*/
          anychart.onDocumentReady(function() {
          var chart = anychart.column();
          var series = chart.column(massive_csv);
          chart.xAxis().title("Email");
          chart.yAxis().title("");
          chart.container("chart");
          chart.xScroller(true);
          var labels = chart.xAxis().labels();
          labels.enabled(false);

          chart.draw();
          });
      }
    });

  })
  .catch(error => {
    console.error('Произошла ошибка:', error);
  });

    


  
  $('.input-file input[type=file]').on('change', function(){
    let file = this.files[0];
    $(this).closest('.input-file').find('.input-file-text').html(file.name);
  });

  jQuery(($) => {
    $('.select').on('click', '.select__head', function () {
        if ($(this).hasClass('open')) {
            $(this).removeClass('open');
            $(this).next().fadeOut();
        } else {
            $('.select__head').removeClass('open');
            $('.select__list').fadeOut();
            $(this).addClass('open');
            $(this).next().fadeIn();
        }
    });

    $('.select').on('click', '.select__item', function () {
        $('.select__head').removeClass('open');
        $(this).parent().fadeOut();
        $(this).parent().prev().text($(this).text());
        $(this).parent().prev().prev().val($(this).text());
    });

    $(document).click(function (e) {
        if (!$(e.target).closest('.select').length) {
            $('.select__head').removeClass('open');
            $('.select__list').fadeOut();
        }
    });
});