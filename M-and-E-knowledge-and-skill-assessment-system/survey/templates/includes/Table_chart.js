var store_average = [];
var store_survey_name = [];
var ministry_info = [];
var surveyData = {};
var store_ministries = [];
fetch('http://127.0.0.1:8000/get_json/')
    .then(res => res.json())
    .then(data => {
        var surveyTypeInput = document.getElementById('survey_type');
        // var surveyTableBody_1 = document.getElementById('surveyTable').getElementsByTagName('tbody')[0];
        var surveyTableBody_2 = document.getElementById('survey_detail').getElementsByTagName('tbody')[0];
        var surveyTableBody_3 = document.getElementById('general_Survey_Info').getElementsByTagName('tbody')[0];
        var select_ministry = document.getElementById("ministry-select");
        var selectElement = document.getElementById("survey-select");
        var selectYear = document.getElementById("survey_year");
        var myCheckbox = document.getElementById('myonoffswitch');
        var mySelect = document.getElementById('survey-select');
        var option_table2 = document.getElementById('section1');
        var option_table1 = document.getElementById('section2');
        var column_chart = document.getElementById('container');
        const button = document.getElementById('getSelectedValuesBtn');

        button.onclick = () => handleButtonClick(data);


        // Populate the survey type options
        data.survey_type.forEach(surveyType => {
            var option = document.createElement('option');
            option.value = surveyType.id;
            option.textContent = surveyType.name;
            surveyTypeInput.appendChild(option);
        });

        myCheckbox.addEventListener('change', function () {
            if (!myCheckbox.checked) {
                mySelect.disabled = true;
            } else {
                mySelect.disabled = false;
            }
        });





        surveyTypeInput.addEventListener('change', function () {
            var selectedSurveyTypeId = parseInt(surveyTypeInput.value);
            console.log('Selected survey:', selectedSurveyTypeId);
            clearTable(surveyTableBody_2);
            clearOptions(select_ministry);
            clearOptions(selectElement);
            selectYear.addEventListener('change', function () {
                var selectedYear = parseInt(selectYear.value);
                console.log('Selected Year:', selectedYear);
                clearTable(surveyTableBody_2);
                clearOptions(select_ministry);
                clearOptions(selectElement);



                if (selectedSurveyTypeId && myCheckbox.checked && selectedYear) {
                    var surveys = data.survey.filter(survey => survey.survey_type_id === selectedSurveyTypeId && new Date(survey.created_at).getFullYear() === selectedYear);

                    surveys.forEach(survey => {

                        var option = document.createElement("option");
                        option.value = '';
                        option.textContent = 'Select Survey';

                        option.value = survey.id;
                        option.textContent = survey.name;
                        selectElement.appendChild(option);

                        selectElement.addEventListener('change', function () {
                            var selectedSurvey = selectElement.value;
                            console.log('Selected survey:', selectedSurvey);


                            var selectedSurveyId = parseInt(selectElement.value);
                            for (var i = 0; i < data.surveys.length; i++) {
                                if (data.surveys[i].id === selectedSurveyId) {
                                    selectedSurvey = data.surveys[i];
                                    break;
                                }
                            }
                            // Get the line ministry from the selected survey
                            if (selectedSurvey) {
                                var lineMinistries = selectedSurvey.line_ministries;
                                while (select_ministry.firstChild) {
                                    select_ministry.removeChild(select_ministry.firstChild)
                                }
                                lineMinistries.forEach(function (lineMinistry) {
                                    var ministry_option = document.createElement("option");
                                    ministry_option.value = lineMinistry.id;
                                    ministry_option.textContent = lineMinistry.name;
                                    select_ministry.append(ministry_option)

                                });
                                console.log('Line ministries:', lineMinistries);
                            }

                            else {
                                console.log('Selected survey not found');
                            }

                            select_ministry.addEventListener("change", function () {
                                if (select_ministry) {
                                    clearTable(surveyTableBody_2)
                                }
                                var selectedLineMinistry = parseInt(select_ministry.value);

                                user = null;
                                weightedSum = 0;
                                data.users.forEach(function (users) {
                                    if (users.Line_ministry_id === selectedLineMinistry) {
                                        user = users.id;
                                        return;
                                    }
                                });
                                console.log("User Id" + user);



                                var selectedUserResponses = data.user_response.filter(function (userResponse) {
                                    return userResponse.submitted_by_id === user && userResponse.forsurvey_id === selectedSurveyId;
                                });


                                console.log("user Response for surveyID" + selectedSurveyId)
                                console.log(selectedUserResponses);

                                userResponseId = null
                                selectedUserResponses.forEach(function (userResponse) {
                                    if (userResponse.submitted_by_id === user) {
                                        userResponseId = userResponse.id;
                                        return;  // Exit the loop once a match is found
                                    }
                                });
                                console.log("yry " + userResponseId)

                                if (userResponseId !== null) {
                                    var answers = data.answer.filter(function (answer) {
                                        return answer.response_id === userResponseId;
                                    });

                                    console.log(answers);
                                    var answerValues = answers.map(function (answer) {
                                        return {
                                            value: parseFloat(answer.answertext),
                                            questionId: answer.forquestion_id
                                        };
                                    });

                                    var weightedSum = 0;
                                    var totalWeight = 0;
                                    var total_weightedinPercent = 0;
                                    var count = 0;
                                    var total_answer = 0;
                                    answerValues.forEach(function (answer) {
                                        var question = data.questions.find(function (q) {
                                            return q.id === answer.questionId;
                                        });


                                        if (question) {
                                            var weight = question.weight;
                                            console.log("the question :" + question.title + "the weight:" + weight)


                                            var total_weight = 0
                                            if (!isNaN(answer.value)) {
                                                weightedSum += answer.value * weight;
                                                totalWeight += weight;
                                                total_answer += answer.value;


                                            }

                                            var weighted__Sum = 0;

                                            if (totalWeight > 0) {
                                                var weightedAverage = weightedSum / totalWeight;
                                                var row = surveyTableBody_2.insertRow();
                                                var question_cell = row.insertCell();
                                                question_cell.textContent = question.title;
                                                row.insertCell().textContent = answer.value;
                                                question_cell.classList.add('limited-width');
                                                row.insertCell().textContent = weight;
                                                console.log(totalWeight)
                                                row.insertCell().textContent = answer.value * weight;
                                                var totalresult = answer.value * weight
                                                var max_value = 10;

                                                var weightedinPercent = ((totalresult) / (max_value * weight)) * 100;
                                                count++;
                                                total_weightedinPercent += weightedinPercent;
                                                // console.log("hello" + total_weightedinPercent + " "+ count);

                                                row.insertCell().textContent = weightedinPercent + "%";
                                                var x = weightedinPercent;
                                                var newCell = row.insertCell();
                                                newCell.id = 'Indicator';
                                                if (x >= 90) {
                                                    newCell.textContent = " Very Good";
                                                    newCell.style.backgroundColor = "#52B788";
                                                } else if (x >= 80) {
                                                    newCell.textContent = "Good";
                                                    newCell.style.backgroundColor = "#C2FA41";
                                                } else if (x >= 60) {
                                                    newCell.textContent = "Satisfactory";
                                                    newCell.style.backgroundColor = "#C1FA61";

                                                } else if (x >= 50) {
                                                    newCell.textContent = "Poor";
                                                    newCell.style.backgroundColor = "#FAEB41";


                                                } else if (x >= 40) {
                                                    newCell.textContent = "Very Poor";
                                                    newCell.style.backgroundColor = " #FA7D41";


                                                } else {
                                                    newCell.textContent = "Extremely Poor";
                                                    newCell.style.backgroundColor = "#FA7D41";


                                                }

                                                console.log("Weighted average of answers: " + weightedAverage.toFixed(2));
                                            } else {
                                                console.log("No valid answers found for the selected line ministry.");
                                            }


                                        }
                                    });

                                }


                                else {
                                    console.log("No user_response ID found for the selected line ministry.");
                                }
                                var totalRow = surveyTableBody_2.insertRow();
                                var labelCell = totalRow.insertCell();
                                labelCell.textContent = 'Total';

                                var valueCell = totalRow.insertCell();
                                valueCell.textContent = total_answer;

                                var weightCell = totalRow.insertCell();
                                weightCell.textContent = totalWeight;

                                var weightCell = totalRow.insertCell();
                                weightCell.textContent = weightedSum;

                                var averageCell = totalRow.insertCell();
                                var average = total_weightedinPercent / count;
                                averageCell.textContent = average.toFixed(2) + "%";
                                surveyTableBody_2.appendChild(totalRow);
                                option_table1.style.display = "block";
                                console.log(average);



                                console.log('Selected survey:', selectedSurvey);
                                console.log("Selected line ministry: " + selectedLineMinistry);
                            });
                        });
                        var selectedSurvey = (selectElement.value);
                        console.log('Selected survey:', selectedSurvey);

                    });

                    // initializeDataTable();
                }
                else if (selectedSurveyTypeId && !myCheckbox.checked || selectYear) {

                    var survey_s = data.survey.filter(survey => survey.survey_type_id === selectedSurveyTypeId && new Date(survey.created_at).getFullYear() === selectedYear);
                    if (survey_s) {
                        console.log("Hello");
                        var lineMinistries = []
                        survey_s.forEach(function (survey) {
                            var matchingSurvey = data.surveys.find(s => s.id === survey.id)
                            console.log(matchingSurvey);
                            if (matchingSurvey) {
                                lineMinistries = lineMinistries.concat(matchingSurvey.line_ministries);
                            }
                        });
                        var uniqueLineMinistries = lineMinistries.filter((ministry, index, self) =>
                            index === self.findIndex(m => m.name === ministry.name)
                        );

                        uniqueLineMinistries.forEach(function (lineMinistry) {
                            var ministry_option = document.createElement("option");
                            ministry_option.value = lineMinistry.id;
                            ministry_option.textContent = lineMinistry.name;
                            select_ministry.append(ministry_option)

                        });

                        select_ministry.addEventListener("change", function () {
                            store_average = [];
                            store_survey_name = [];

                            if (select_ministry) {
                                clearArrays(store_average, store_survey_name)
                                clearTable(surveyTableBody_3);
                                var selectedLineMinistry = parseInt(select_ministry.value);
                                console.log(selectedLineMinistry)
                            }


                            var surveysWithSelectedMinistry = [];

                            data.surveys.forEach(function (survey) {
                                if (survey_s.some(function (s) { return s.id === survey.id; })) {
                                    var hasSelectedMinistry = survey.line_ministries.some(function (ministry) {
                                        return ministry.id === selectedLineMinistry;
                                    });

                                    if (hasSelectedMinistry) {
                                        surveysWithSelectedMinistry.push(survey.id);
                                    }
                                }
                            });

                            console.log(surveysWithSelectedMinistry);


                            user = null;
                            data.users.forEach(function (users) {
                                if (users.Line_ministry_id === selectedLineMinistry) {
                                    user = users.id;
                                    return;
                                }
                            });
                            console.log("User Id" + user);



                            surveysWithSelectedMinistry.forEach(function (surveyId) {

                                var selectedUserResponses = data.user_response.filter(function (userResponse) {
                                    return userResponse.submitted_by_id === user && userResponse.forsurvey_id === surveyId;
                                });


                                console.log("user Response for surveyID" + surveyId)
                                console.log(selectedUserResponses);



                                userResponseId = null
                                selectedUserResponses.forEach(function (userResponse) {
                                    if (userResponse.submitted_by_id === user) {
                                        userResponseId = userResponse.id;
                                        return;
                                    }
                                });
                                console.log(userResponseId);


                                if (userResponseId !== null) {
                                    var answers = data.answer.filter(function (answer) {
                                        return answer.response_id === userResponseId;
                                    });

                                    var answerValues = answers.map(function (answer) {
                                        return {
                                            value: parseFloat(answer.answertext),
                                            questionId: answer.forquestion_id
                                        };
                                    });

                                    var weightedSum = 0;
                                    var totalWeight = 0;
                                    var total_weightedinPercent = 0;
                                    var count = 0;
                                    var total_answer = 0;
                                    answerValues.forEach(function (answer) {
                                        var question = data.questions.find(function (q) {
                                            return q.id === answer.questionId;
                                        });


                                        if (question) {
                                            var weight = question.weight;
                                            console.log("the question :" + question.title + "the weight:" + weight)


                                            var total_weight = 0
                                            if (!isNaN(answer.value)) {
                                                weightedSum += answer.value * weight;
                                                totalWeight += weight;
                                                total_answer += answer.value;


                                            }

                                            var weighted__Sum = 0;

                                            if (totalWeight > 0) {
                                                var weightedAverage = weightedSum / totalWeight;

                                                // console.log(totalWeight)

                                                var totalresult = answer.value * weight
                                                var max_value = 10;

                                                var weightedinPercent = ((totalresult) / (max_value * weight)) * 100;
                                                count++;
                                                total_weightedinPercent += weightedinPercent;
                                                // console.log("hello" + total_weightedinPercent + " "+ count);

                                                var x = weightedinPercent;

                                                console.log("Weighted average of answers: " + weightedAverage.toFixed(2));
                                            } else {
                                                console.log("No valid answers found for the selected line ministry.");
                                            }

                                        }


                                    });



                                }

                                var average = total_weightedinPercent / count;

                                if (average) {

                                    var totalRow = surveyTableBody_3.insertRow();
                                    var survey = data.survey.find(function (survey) {
                                        return survey.id === surveyId;
                                    });
                                    var surveyName = survey ? survey.name : "survey not found";
                                    store_survey_name.push(surveyName);
                                    totalRow.insertCell().textContent = surveyName;


                                    var valueCell = totalRow.insertCell();
                                    valueCell.textContent = total_answer;

                                    var weightCell = totalRow.insertCell();
                                    weightCell.textContent = totalWeight;

                                    var weightCell = totalRow.insertCell();
                                    weightCell.textContent = weightedSum;

                                    var averageCell = totalRow.insertCell();
                                    var appr = average.toFixed(2);
                                    averageCell.textContent = appr + "%";
                                    store_average.push(appr);
                                    surveyTableBody_3.appendChild(totalRow);

                                }
                                option_table2.style.display = "block";
                                var ministry = data.line_ministry.find(function (ministry) {
                                    return ministry.id === selectedLineMinistry;
                                });
                                var ministry_name = ministry ? ministry.name : "survey not found";


                                draw_columnChart(store_survey_name, store_average, ministry_name);
                                console.log("here I am" + store_average);
                                console.log("here I am" + store_survey_name);
                                console.log("here I am" + ministry_name);


                            });
                        });

                    }

                }
            });
        });


    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });


function clearTable(tableBody) {
    while (tableBody.firstChild) {
        tableBody.removeChild(tableBody.firstChild);
    }
}
function clearOptions(select) {
    while (select.firstChild) {
        select.removeChild(select.firstChild);
    }
}
function exportTableToExcel(tableId, filename = '') {
    var downloadLink;
    var dataType = 'application/vnd.ms-excel';
    var tableSelect = document.getElementById(tableId);
    var tableHTML = tableSelect.outerHTML.replace(/ /g, '%20');

    filename = filename ? filename + '.xlsb' : 'excel_data.xlsb';

    downloadLink = document.createElement("a");

    document.body.appendChild(downloadLink);

    if (navigator.msSaveOrOpenBlob) {
        var blob = new Blob(['\ufeff', tableHTML], {
            type: dataType
        });
        navigator.msSaveOrOpenBlob(blob, filename);
    } else {
        downloadLink.href = 'data:' + dataType + ', ' + tableHTML;
        downloadLink.download = filename;
        downloadLink.click();
    }
}
function clearArrays(param1, param2) {
    param1.length = 0;
    param2.length = 0;

}
document.getElementById('exportButton').onclick = function () {
    exportTableToExcel('survey_detail', 'exported_table');
}
document.getElementById('exportButton_1').onclick = function () {
    exportTableToExcel('surveyTable', 'exported_table');
}

document.getElementById('exportButton_2').onclick = function () {
    exportTableToExcel('general_Survey_Info', 'exported_table');
}
Highcharts.chart('pieChart', {
    chart: {
        type: 'variablepie'
    },
    title: {
        text: 'Countries compared by population density and total area, 2022.',
        align: 'left'
    },
    tooltip: {
        headerFormat: '',
        pointFormat: '<span style="color:{point.color}">\u25CF</span> <b> {point.name}</b><br/>' +
            'Area (square km): <b>{point.y}</b><br/>' +
            'Population density (people per square km): <b>{point.z}</b><br/>'
    },
    series: [{
        minPointSize: 10,
        innerSize: '20%',
        zMin: 0,
        name: 'countries',
        borderRadius: 5,
        data: [{
            name: 'Spain',
            y: 505992,
            z: 92
        }, {
            name: 'France',
            y: 551695,
            z: 119
        }, {
            name: 'Poland',
            y: 312679,
            z: 121
        }, {
            name: 'Czech Republic',
            y: 78865,
            z: 136
        }, {
            name: 'Italy',
            y: 301336,
            z: 200
        }, {
            name: 'Switzerland',
            y: 41284,
            z: 213
        }, {
            name: 'Germany',
            y: 357114,
            z: 235
        }],
        colors: [
            '#4caefe',
            '#3dc3e8',
            '#2dd9db',
            '#1feeaf',
            '#0ff3a0',
            '#00e887',
            '#23e274'
        ]
    }]
});
function draw_columnChart(x, y, z) {
    const numericStoreAverage = y.map(value => parseFloat(value));
    Highcharts.chart('container', {
        chart: {
            type: 'column'
        },
        title: {
            text: z,
            align: 'left'
        },
        subtitle: {
            text:
                '',
            align: 'left'
        },
        xAxis: {
            categories: x,
            crosshair: true,
            accessibility: {
                description: 'Countries'
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: ''
            }
        },
        tooltip: {
            valueSuffix: ''
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [
            {
                name: 'Average',
                data: numericStoreAverage
            }
            // ,
            // {
            //   name: 'Wheat',
            //   data: [51086, 136000, 5500, 141000, 107180, 77000]
            // }
        ]
    });
}



// function initializeDataTable() {
//     var table = $('#example').DataTable( {
//         lengthChange: true,
//         buttons: [ 'copy', 'excel', 'pdf', 'colvis' ]
//     } );

//     table.buttons().container()
//         .insertBefore( '#example_filter' );
// }


$(document).ready(function () {
    var table = $('#example').DataTable({
        lengthChange: true,
        buttons: ['copy', 'excel', 'pdf', 'colvis']
    });

    table.buttons().container()
        .insertBefore('#example_filter');
});


var selectedOptions = [];
function handleButtonClick(data) 
{
    function getSelectedValues() {
        var selectElement = document.getElementById('lineMinistrySelect');
        if (selectElement === null) {
            console.log("Select element not found");
            return;
        }
        var selectedOptions = Array.from(selectElement.selectedOptions).map(function (option) {
            return parseInt(option.value, 10); // Convert the ID to an integer
        });
        console.log(selectedOptions);
        var surveyIds = data.surveys
            .filter(survey => selectedOptions.every(ministryId => survey.line_ministries.some(ministry => ministry.id === ministryId)))
            .map(survey => survey.id);
        userResponseId = null;
        for (var i = 0; i < surveyIds.length; i++) {
            var surveyId = surveyIds[i];
            console.log(surveyId);
            for (var j = 0; j < selectedOptions.length; j++) {
                var lineMinistryId = selectedOptions[j];
                console.log(lineMinistryId);
                var userFound = false;
                for (var k = 0; k < data.users.length; k++) {
                    var user = data.users[k];
                    if (user.Line_ministry_id === lineMinistryId) {
                        userFound = true;
                        for (var l = 0; l < data.user_response.length; l++) {
                            var response = data.user_response[l];

                            if (response.forsurvey_id === surveyId && response.submitted_by_id === user.id) {
                                userResponseId = response.id;
                                break;
                            }
                        }
                        break;
                    }
                }
                if (userResponseId !== null) {
                    var answers = data.answer.filter(function (answer) {
                        return answer.response_id === userResponseId;
                    });
                    var answerValues = answers.map(function (answer) {
                        return {
                            value: parseFloat(answer.answertext),
                            questionId: answer.forquestion_id
                        };
                    });
                    var weightedSum = 0;
                    var totalWeight = 0;
                    var total_weightedinPercent = 0;
                    var count = 0;
                    var total_answer = 0;
                    answerValues.forEach(function (answer) {
                        var question = data.questions.find(function (q) {
                            return q.id === answer.questionId;
                        });
                        if (question) {
                            var weight = question.weight;
                            console.log("the question :" + question.title + "the weight:" + weight)
                            var total_weight = 0
                            if (!isNaN(answer.value)) {
                                weightedSum += answer.value * weight;
                                totalWeight += weight;
                                total_answer += answer.value;
                            }
                            var weighted__Sum = 0;
                            if (totalWeight > 0) {
                                var weightedAverage = weightedSum / totalWeight;
                                var totalresult = answer.value * weight
                                var max_value = 10;
                                var weightedinPercent = ((totalresult) / (max_value * weight)) * 100;
                                count++;
                                total_weightedinPercent += weightedinPercent;
                                var x = weightedinPercent;
                                console.log("Weighted average of answers: " + weightedAverage.toFixed(2) + "by   " + user.id + "for survey " + surveyId);
                            } else {
                                console.log("No valid answers found for the selected line ministry.");
                            }
                        }
                    });
                    var average = total_weightedinPercent / count;
                    console.log("Average " + average);
                    var Objects = {};
                    Objects.lineMinistries = lineMinistryId;
                    Objects.survey = surveyId;
                    Objects.average = average

                    ministry_info.push(Objects);

                    console.log(ministry_info);

                }
            }
        }
    }
    const selectedMinistries = getSelectedValues();
    console.log(selectedMinistries);
    console.log(ministry_info);


    for (var key in ministry_info) {
        var entry = ministry_info[key];
        var surveyId = entry.survey;
        var lineMinistryId = entry.lineMinistries;
        var average = entry.average;
        if (!store_ministries.includes(lineMinistryId)) {

            store_ministries.push(lineMinistryId);
        }

        if (surveyData[surveyId] === undefined) {

            surveyData[surveyId] = [average];

        } else {

            surveyData[surveyId].push(average);


        }
    }

    for (var surveyId in surveyData) {
        var average = surveyData[surveyId];
        console.log(`Survey ID: ${surveyId}`);
        console.log(average);
        console.log("-----------------");
        console.log(surveyData);
        draw_chart_withMultiple_column();

    } function draw_chart_withMultiple_column() {
        var formattedData = [];

        for (var surveyId in surveyData) {
console.log("ghjsd");
console.log(surveyId);

            var survey = data.survey.find(function (survey) {
                        return survey.id == surveyId;
                    });
        var surveyName = survey ? survey.name : "survey not found";

        
            var surveysIds= surveyData[surveyId];
            formattedData.push({
                name: surveyName,
                data: surveysIds
            });
        }
        var result = ministry_info.map(function (obj) {
            return { lineMinistries: obj.lineMinistryId };
        });
        var ministryNames = [];

for (var i = 0; i < store_ministries.length; i++) {
var Ministry = data.line_ministry.find(function (ministry) {
return ministry.id === store_ministries[i];
                    });
      if(Ministry){
        ministryNames.push(Ministry.name);
      }
      else{
        console.log("No name");
      }
}

console.log(ministryNames);
        Highcharts.chart('barCharts', {
            chart: {
                type: 'column'
            },
            title: {
                text: ''
            },
            xAxis: {
                categories: ministryNames
            },
            credits: {
                enabled: false
            },
            plotOptions: {
                column: {
                    borderRadius: '25%'
                }
            },
            series: formattedData
        });
    }
}
