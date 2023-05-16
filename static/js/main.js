jQuery.validator.setDefaults({
    debug: true,
    success: "valid"
});


/**
 *  a function to initial a Datatable by passing
 *      formId:     the pre-required empty <table id="formId" > and with initialed <th>(s)
 *
 *      URL:        the back-end route as datasource to load the data of a datatable
 *
 *      columns:    the columns where each column should be put
 *
 *      flag:       indicate if a set of button is required
 *
 *   checkboxFlag :   indicate if a checkbox is needed in front of each row is required
 *
 *      target:     if button required then target is where the but located in the table.
 *
 *      btns:       an array of object that represent the button name and function to be called on click the button
 *
 **/
function renderDataTable(formId, url, columns, flag, checkboxFlag, target, btns) {
    setTimeout(1000);
    debugger
    $.ajax({
            url: url,
            type: "get",
            dataType: "JSON",
            success: function (data) {
                var columnDefs = []
                if (flag) {
                    columnDefs.push(
                        {
                            "render": function (data, type, meta, row) {
                                var btn = ""
                                console.log(data)
                                console.log(meta)
                                console.log(row)
                                debugger
                                btns.forEach(button => {
                                    console.log(button.btnName)
                                    if (button.btnName == 'Edit' && meta.if_current_mentor != '1') {
                                        btn += "<input type='button' onclick='" + button['func'] + "(" + (meta.id) + ")' class='hide' value='" + button['btnName'] + "'> "
                                    } else {
                                        btn += "<input type='button' onclick='" + button['func'] + "(" + (meta.id) + ")' value='" + button['btnName'] + "'> "
                                    }
                                })
                                return btn
                            },
                            "targets": target
                        }
                    )
                }
                if (checkboxFlag) {
                    columnDefs.push(
                        {
                            "render": function (data, type, meta, row) {
                                var btn = "<div align='center'><input type=\"checkbox\" name=\"ckb-jobid\" value=" + (meta.id) + "></div>"
                                return btn;
                            },
                            "targets": 0
                        }
                    )
                }
                if ($.fn.dataTable.isDataTable(formId)) {
                    console.log("dataTable1")
                    let dataTable1 = $(formId).dataTable();
                    dataTable1.fnClearTable()
                    dataTable1.fnAddData(data, true)
                } else {
                    $(formId).dataTable({
                        "bAutoWidth": true,
                        select: {
                            style: 'os',
                            selector: 'td:first-child'
                        },
                        "dataSrc": "",
                        "order": [[0, "desc"]],  // HERE !! ERROR TRIGGER!
                        "lengthMenu": [[10, 50, 100, -1], [10, 50, 100, "All"]],
                        "data": data,
                        "columns": columns,
                        "columnDefs": columnDefs
                    });
                }
            },
            error: function (xhr, status, error) {

            }
        }
    );
}

$(function () {
    $("#noti").on("click", function (func) {
        allMembers = []
        $.ajax({
            url: "getAllUserByUserType",
            type: "get",
            data: {"role": "2", "to": "messageBox"}
        }).then(function (response) {
            console.log(response);

            let allMem = response.filter(item => {
                return item[10] == 0
            }).reduce((acc, curr) => {
                console.log(curr[10])
                acc[curr[0]] = curr[1] + ' ' + curr[2];
                return acc;
            }, {});
            console.log(typeof allMem)
            var myObject = {"0": "All", ...allMem};

            const sortedArray = Object.entries(myObject).sort();

            // Convert the sorted array back to an object
            const sortedObject = Object.fromEntries(sortedArray);

            // Multiple inputs of different types
            $.MessageBox({
                message: "<b>Notifications</b>",
                buttonFail: "Cancel",

                input: {
                    text1: {
                        type: "text",
                        label: "Title:",
                        title: "Input some title",
                        required: 'true'
                    },
                    select1: {
                        type: "select",
                        label: "Receiver:",
                        title: "Select one member or all members",
                        options: sortedObject,
                    },
                    text2: {
                        type: "textarea",
                        label: "Content:",
                        title: "Input some other text",
                        maxlength: 200
                    },

                },

                filterDone: function (data) {
                    if (data['text1'] == '' || data['text1'] === null) return "Please fill the title";
                    if (data['text2'] == '' || data['text2'] === null) return "Please fill the content";
                    if (data['select1'] === "" || data['select1'] === null) return "Please choose at least one member";
                    return $.ajax({
                        url: "addMessage",
                        type: "post",
                        dataType: "JSON",
                        data: data
                    }).then(function (response) {
                        if (response == false) return "some thing wrong happened, could you try again later.";
                        else {
                            if (response.code == "MessageSentCode") {
                                $.MessageBox(response.message)
                            }
                        }
                    });
                },

                top: "auto"
            }).then(function (data) {
            });


        });

    })

    $("#notiList").on("click", function (func) {
        allMembers = []
        $.ajax({
            url: "/getAllMyMsg",
            type: "get",
        }).then(function (response) {
            console.log(response);
            if (response.data.length == 0) {
                return $.MessageBox("you don't have any messages!")
            }
            var table = $("<table>", {
                css: {
                    "width": "520px",
                    "margin-top": "1rem"
                }
            });

            var headerRow = $("<tr>");
            $("<th>").text("Title").appendTo(headerRow);
            $("<th>").text("Sent Date").appendTo(headerRow);
            headerRow.appendTo(table);

            $.each(response.data, function (index, item) {
                var dataRow = $('<tr onclick=notiDetail(' + item[0] + ')>');
                $("<td>").text(item[3]).appendTo(dataRow);
                $("<td>").text(item[2]).appendTo(dataRow);
                dataRow.appendTo(table);
            });

            table.appendTo("body");
            $.MessageBox({
                message: "Your Message List:",
                input: table
            }).done(function (data) {
                console.log(data);
            });


        }).then(function (data) {
        });
    });
    $('#memberList th.sortable').click(function () {
        var table = $(this).parents('table').eq(0);
        var rows = table.find('tr:gt(0)').toArray().sort(compare($(this).index()));
        this.asc = !this.asc;
        if (!this.asc) {
            rows = rows.reverse();
        }
        for (var i = 0; i < rows.length; i++) {
            table.append(rows[i]);
        }
    });
    $('#trainerList th.sortable').click(function () {
        var table = $(this).parents('table').eq(0);
        var rows = table.find('tr:gt(0)').toArray().sort(compare($(this).index()));
        this.asc = !this.asc;
        if (!this.asc) {
            rows = rows.reverse();
        }
        for (var i = 0; i < rows.length; i++) {
            table.append(rows[i]);
        }
    });

    // Compare function for sorting the table
    function compare(index) {
        return function (a, b) {
            var valA = getCellValue(a, index);
            var valB = getCellValue(b, index);
            return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.localeCompare(valB);
        }
    }

    // Get the value of a table cell
    function getCellValue(row, index) {
        return $(row).children('td').eq(index).text();
    }

})

function notiDetail(id) {
    $.ajax({
        url: "/getAllMyMsg",
        type: "get",
        dataType: "JSON",
        data: {"dataId": id},
    }).then(function (response) {
        console.log(response.data)
        $.confirm({
            boxWidth: '30%',
            useBootstrap: false,
            title: response.data[0][3],
            content: "<br>" + response.data[0][1] + "<br><br><br><br><br><br><br><br><br>" + response.data[0][2] + "<br> Sent By Admin",
            buttons: {
                OK: function () {
                },


            }
        });
    })
}

function sendRequest(url, data, method, ifDirect) {
    $.ajax({
        url: url,
        type: method,
        dataType: "JSON",
        data: data,
        success: function (response) {
            console.log(response)
            if (response.code == "SUCCESS") {
                if (ifDirect != 0) {
                    $.MessageBox(response.message + " success!!")
                }
            } else if (response.code == "DeleteUserSUCCESS") {
                $.MessageBox(response.message)
                location.reload();
            } else if (response.code == "UserUnsubscribe") {
                $.MessageBox(response.message)
                location.href = "/"
            } else {
                $.MessageBox(response.message)
            }


        }, fail: function (response) {
            console.log(response)

        }
    })
}

function doUnsubscribe(data) {
    $.confirm({
        theme: 'dark',
        title: 'Unsubscription',
        content: 'Are you sure that you wanna quit from Lincoln Fitness Club?',
        buttons: {
            confirm: function () {
                deleteMember(data, 0)
                location.href = "/logout"
            },
            cancel: function () {

            }

        }
    });
}

function deleteMember(data, ifDirect) {
    var formData = {'userId': data}
    console.log(formData)

    sendRequest('/removeUser', formData, "get", ifDirect);
}

// need more work for the ClassBooking confirmation pop up
function bookingClass(classId, userId) {
    $.confirm({
        theme: 'dark',
        title: 'Send Email',
        content: 'Are you sure?',
        buttons: {
            confirm: function () {
                confirmBooking(classId, userId)
                location.href = "/login"
            },
            cancel: function () {
            }

        }
    });
}

function checkEmail(email, id) {
    $.ajax({
        url: "/users/checkEmail",
        type: "get",
        dataType: "JSON",
        data: {"email": email},
    }).then(data => {
        console.log("asdasd")
        if (data.code == "ok") {
            if (id) {
                id = "#" + id
                $(id).addClass("error")
            }
            $.alert("email is already registered")
        } else {
            if (id) {
                id = "#" + id
                $(id).removeClass("error")
            }
        }
    })
}

function addMentor(fromdata) {

    $.ajax({
        url: "/users/addOrUpdate",
        type: "POST",
        dataType: "JSON",
        data: fromdata,
    }).then(data => {
        if (data.code == 'ok') {
            $.alert("Mentor has been added successfully")
            var btn = [
                {
                    "btnName": "edit",
                    "func": "alert"
                }, {
                    "btnName": "delete",
                    "func": "alert"
                }];
            renderDataTable("#myTableOne", "/mentor/getAllJson", [
                {"data": "first_name"},
                {"data": "phone"},
                {"data": "email"},
                {"data": "company_name"},
            ], true, 3, btn)
        }
    })

}

function validateQueForm() {

    var form = $("#queForm");
    form.validate({
        rules: {
            que_1: {
                required: true,

            },
            que_2: {
                required: true,

            },
            que_3: {
                required: true,

            },
            que_4: {
                required: true,

            },
            que_5: {
                required: true,

            },
            que_5: {
                required: true,

            },
            que_6: {
                required: true,

            },
            que_7: "required",
            que_8: "required",
            que_9: "required",
            que_10: "required"
        }
        ,
        errorPlacement: function (error, element) {
            return true;
        }
    });
    let valid = form.valid();
    debugger
    if (!valid) {
        $.MessageBox("please fill out all required information in correct format");
    }
    return valid
}


function sendEmailPassword(email) {
    $.ajax({
        url: "/users/checkEmail",
        type: "get",
        dataType: "JSON",
        data: {"email": email},
    }).then(data => {
        if (data.code == 'ok') {
            $.ajax({
                url: "/users/sendPasswordEmail",
                type: "get",
                dataType: "JSON",
                data: {"email": email},
            }).then(data => {
                console.log(data)
            })
        } else {
            $.confirm({
                theme: 'dark',
                title: 'Send Email',
                content: 'Email doesn\'t exist',
                buttons: {
                    confirm: function () {
                    }
                }
            });
        }
    })
}


function validateTrainerForm() {

    var form = $("#trainerRegiForm");
    form.validate({
        rules: {
            firstname: {
                required: true,
                lettersonly: true
            },
            familyname: {
                required: true,
                lettersonly: true
            },
            email: {
                required: true,
                email: true
            },
            gender: "required",
            qualifications: "required",
            phone: {
                required: true,
                digits: true,
                minlength: 10,
                maxlength: 11
            },
            summary: "required",

        },
        errorPlacement: function (error, element) {
            return true;
        }
    });
    let valid = form.valid();
    if (!valid) {
        $.MessageBox("please fill out all required information in correct format")
    }
    return valid
}

function validateForm() {

    var form = $("#regiForm");
    form.validate({
        rules: {
            firstname: {
                required: true,
                lettersonly: true
            },
            lastname: {
                required: true,
                lettersonly: true
            },
            alternativeName: {
                required: true,
                lettersonly: true
            },
            preferName: {
                required: true,
                lettersonly: true
            },
            studentNo: {
                required: true,
                digits: true
            },
            password: {
                required: true,
                minlength: 6,
                maxlength: 15
            },
            phone: {
                required: true,
                digits: true
            },
            gender: "required",
            dob: "required",
            email: {
                required: true,
                email: true
            }

        },
        errorPlacement: function (error, element) {
            return true;
        }
    });
    let valid = form.valid();
    if (!valid) {
        $.MessageBox("please fill out all required information in correct format");
    }
    return valid
}

function processPayment(data, userId) {

    data = {
        "sessionId": data,
        "userId": userId
    }
    sendRequest("/addPayment", data, "post")
}

function updatePassword(role) {
    var formData = serializeData("form#forgotPass");

    $.validator.addMethod("passwordEqual", function (value, element) {
        let forpassword = $('#forpassword').val();
        let conpassword = $('#forconpassword').val();
        console.log(forpassword, conpassword)
        return forpassword == conpassword;
    }, "Passwords must be same");
    var form = $("#forgotPass");
    form.validate({
            rules: {
                forpassword: {
                    required: true,
                    passwordEqual: true
                },
                conpassword: {
                    required: true,
                    passwordEqual: true
                }

            },
            errorPlacement: function (error, element) {
                return true;
            }

        }
    )
    let valid = form.valid();
    if (!valid) {
        $.MessageBox("Passwords must be same");
    } else {
        $.ajax({
            url: "/users/changePassword",
            type: "POST",
            data: formData
        }).then(data => {
            if (data.code == 'ok') {
                $.MessageBox("your password has been changed.")
            } else {
                $.MessageBox(data.message)
            }
        })
    }

}

function checksendEmail() {
    $.confirm({
        theme: 'dark',
        title: 'Enter your email',
        content: '' +
            '<form action="" class="formName">' +
            '<div class="form-group">' +
            '<label>Your email address</label>' +
            '<input type="text" placeholder="John.Doe@gmail.com" class="email form-control" required />' +
            '</div>' +
            '</form>',

        buttons: {
            Send: function () {
                var email = this.$content.find('.email').val();
                if (!email) {
                    $.alert('provide a valid email');
                    return false;
                }
                sendEmailPassword(email)
            },
            cancel: function () {
            }

        }
    });
}

function extraMultipul(selectedOptions, formData) {
    const result = selectedOptions.reduce((acc, {name, value}) => {
        acc[name] = acc[name] || [];
        acc[name].push(value);
        return acc;
    }, {});

    console.log(result);
    for (var objA in formData) {
        for (var objB in result) {
            if (objB === objA) {
                formData[objA] = result[objB]
            }
        }
    }
}

function submitQA() {
    validResult = validateQueForm()
    console.log(validResult)
    var formData = serializeData("form#queForm");
    console.log(formData)

    var selectedOptions = $("#queForm input[name='que_7']:checked").serializeArray();
    var selectedOptionsQ8 = $("#queForm input[name='que_8']:checked").serializeArray();

    extraMultipul(selectedOptions, formData);
    extraMultipul(selectedOptionsQ8, formData);


    let data1 = JSON.stringify(formData);
    let data2 = JSON.parse(data1);
    console.log(data1);
    $.ajax({
        url: "/studentQuestions/addQuestionAnswer",
        type: "POST",
        dateType: 'json',
        data: data2
    }).then(data => {
        if(data.code='ok'){
            $.alert("your survey has been updated successfully")
        }
    })

}

function hideQuestions(preOrNext) {
    var elements = $('#queForm .sideContainer');
    console.log(elements.length)
    var displayIndex = -1
    var hideIndex = -1
    if (preOrNext == 'next') {
        for (let i = 0; i < elements.length; i++) {
            if (elements[i].className.indexOf('hide') > 0 && displayIndex > 0) {

                if (i < hideIndex + 2) {
                    $(elements[i]).removeClass("hide")
                }
                if (hideIndex > elements.length - 4) {
                    $('#btnNext').addClass('hide')
                    $('#submitQABtn').removeClass('hide')
                }
            } else if (elements[i].className.indexOf('hide') < 0) {
                if (i >= elements.length - 2) {
                    $('#submitQABtn').removeClass('hide')
                    continue;
                } else {
                    $('#btnPrev').removeClass('hide')

                }
                if (hideIndex < displayIndex + 2) {
                    hideIndex = displayIndex + 2
                    displayIndex = i;
                }

                $(elements[i]).addClass("hide")
            }
        }

    } else {
        for (let i = elements.length - 1; i >= 0; i--) {
            if (elements[i].className.indexOf('hide') > 0 && displayIndex > 0) {

                if (i > hideIndex - 2) {
                    $(elements[i]).removeClass("hide")
                }
                if (hideIndex <= 1) {
                    $('#submitQABtn').addClass('hide')
                    $('#btnPrev').addClass('hide')
                    continue;
                }
                $('#btnNext').removeClass('hide')

            } else if (elements[i].className.indexOf('hide') < 0) {

                if (hideIndex > displayIndex - 2) {
                    displayIndex = i;
                    hideIndex = displayIndex - 2
                }
                $('#submitQABtn').addClass('hide')

                $(elements[i]).addClass("hide")
            }
        }
    }

}


function preferStudents() {
    var idArr = []
    $('input:checkbox').each(function () {
        if ($(this).prop('checked') == true) {
            idArr.push($(this).val());
        }
    });
    //todo add to mentor prefer student table.
    alert(idArr)
}

async function addNewMentor() {
    $.ajax({
        url: "/company/getAllJson",
        type: "GET",

    }).then(data => {
        console.log(data);
        var options = "";
        for (let dataKey in data) {
            options += "<option value='" + data[dataKey]['id'] + "'>" + data[dataKey]['company_name'] + "</option>"
        }
        console.log(options)
        $.confirm({
            theme: 'dark',
            title: 'Enter mentor information',
            content: '' +
                '<form id="mentorForm" class="formName">' +
                '<div class="form-group">' +
                '<input type="hidden" name="role" value="1" />' +
                '<label>Mentor email address</label>' +
                '<input type="text" placeholder="John.Doe@gmail.com" id="mentorEmail" name="email" class="email form-control" ' +
                'required onblur="checkEmail(this.value,this.id)" />' +
                '<label>Password</label>' +
                '<input type="password" name="password" class="password form-control" required />' +
                '<label>Phone</label>' +
                '<input type="text" name="phone" class="password form-control" required />' +
                '<label>Mentor First Name</label>' +
                '<input type="text" placeholder="Jone" name="firstname" class="fname form-control" required />' +
                '<label>Mentor Last Name</label>' +
                '<input type="text" placeholder="Doe" name="lastname" class="lastname form-control" required />' +
                '<label>Mentor Company</label>' +
                '<select id="menCompany" name="menCompany" class="menCompany form-control">' + options + '</select>' +
                '</div>' +
                '</form>',

            buttons: {
                Save: async function () {
                    var email = this.$content.find('.email').val();
                    var fname = this.$content.find('.fname').val();
                    var password = this.$content.find('.password').val();
                    var lastname = this.$content.find('.lastname').val();
                    var menCompany = this.$content.find('.menCompany').val();
                    if (!email) {
                        $.alert('provide a valid email');
                        return false;
                    }
                    var formData = serializeData("form#mentorForm")
                    const checkResult = await ajaxCall("/users/checkEmail", "get", {"email": formData.email})


                    if (checkResult.code == 'ok') {
                        $.alert('email is already registered, please change another email address');
                        return false;
                    } else {
                        addMentor(formData)
                    }

                },
                cancel: function () {
                }

            }
        })
    })
}


function checkUserStatus(id) {
    $.ajax({
        url: "/student/getStudentById",
        type: "get",
        dataType: "JSON",
        data: {"id": id}
    }).then(data => {
        if (data.data == 2) {
            $.alert("Looks like you haven't completed our survey, before you use our system you must complete all of them")
        }
    })
}

function checkCompanyProject(companyId) {
    $.ajax({
        url: "/project/getProjectsByCompanyId",
        type: "get",
        dataType: "JSON",
        data: {"comId": companyId}
    }).then(data => {
        alert(data.data)
    })
}

function checkStudentProfile(studentId) {
    $.ajax({
        url: "/studentQuestions/getByStudentId",
        type: "get",
        dataType: "JSON",
        data: {"studentId": studentId}
    }).then(data => {
        if (data.code = 'ok') {
            let questionData = data.data;
            console.log(questionData)
            var td = ''
            questionData.forEach(question => {
                td += '<tr><td>'
                console.log(question.question)
                var que = JSON.parse(question.question)
                td += que.title + "</td><td>"
                if (que.type == "1") {
                    td += que.option[question.question_answer] + "</td>"
                } else {
                    td += question.question_answer + "</td>"
                }
                td += "</tr>"
            })
            $.confirm({
                boxWidth: '1200px',
                useBootstrap: false,
                title: 'Survey Answers',
                content: '' +
                    ' <table id="myTableStudent" class="display">' +
                    '      <thead>' +
                    '        <tr>' +
                    '         <th>Question</th>' +
                    '         <th>Answer</th>' +
                    '        </tr>' +
                    '      </thead>' +
                    '      <tbody>' + td + '</tbody>' +
                    ' </table>'
            })

        }
    })
}


async function ajaxCall(url, type, data) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: url,
            type: type,
            dataType: "JSON",
            data: data,
            success: function (data) {
                resolve(data);
            },
            error: function (xhr, status, error) {
                reject(error);
            }
        });
    });
}

async function myFunction() {
    try {
        const myData = await ajaxCall();
        // do something with myData
    } catch (error) {
        console.error(error);
    }
}

function addOrUpdateUser(type) {
    //add or update a student
    if (type == 2) {
        if (validateForm()) {
            var formData = serializeData("form#regiForm");
            console.log(formData)
            // check if a student no is exist
            $.ajax({
                url: "/users/checkStudentExsit",
                type: "POST",
                data: formData
            }).then(data => {
                console.log(data)
                if (data.code != 'ERROR') {
                    $.ajax({
                        url: "/users/addOrUpdate",
                        type: "POST",
                        data: formData
                    }).then(data => {
                        if (data.code == 'ok') {
                            $.MessageBox(data.message);
                        }
                    })

                } else {
                    $.MessageBox(data.message)
                }
            });


        }
    } else {
        if (validateTrainerForm()) {
            var formData = serializeData("form#trainerRegiForm");
            console.log(formData)
            sendRequest('/addOrUpdateMember', formData, "POST", "form#trainerRegiForm");
        }
    }
}

function moveUp(button) {

    var row = $(button).closest('tr');
    var previousRow = row.prev('tr');

    if (previousRow.length !== 0) {
        previousRow.before(row);
    }


}

function moveDown(button) {

    var row = $(button).closest('tr');
    var after = row.next('tr');

    if (after.length !== 0) {
        after.after(row);
    }


}

function checkPreferredStudent(pid) {
    location.href = '/student/getAll?pid=' + pid
}

function addPreferredProject() {
    var idArr = []
    $('input:checkbox').each(function () {
        debugger
        console.log($(this))
        if ($(this).prop('checked') == true) {
            idArr.push($(this).val());
        }
    });
    if (idArr.length < 3) {
        $.alert("At least three project need to chosen before your rank them")
        return;
    }

    //todo add to mentor prefer student table.
    $.ajax({
        url: "/project/getProjectByIds?idArr=" + idArr,
        type: "GET",
        data: idArr,
    }).then(data => {
        console.log(data);
        var options = ""
        for (let i = 0; i < data.data.length; i++) {
            let item = data.data[i];
            console.log(item)
            options += "<tr>" +
                "<td class='hide' name='proId' value='" + item['id'] + "'>" + item['id'] + "</td>" +
                "<td>" + item['project_title'] + "</td>" +
                "<td>" + item['type_name'] + "</td>" +
                "<td>" + item['company_name'] + "</td>" +
                "<td><button onclick='moveUp(this)' >Up</button></td>" +
                "<td><button onclick='moveDown(this)'>Down</button></td></tr>"
        }

        console.log(options)
        $.confirm({
            theme: 'dark',
            boxWidth: '900px',
            useBootstrap: false,
            title: 'Rank your preference',
            content: '' +
                ' <table id="tablePreProject" class="display">\n' +
                '        <thead>\n' +
                '          <tr class="odd">\n' +
                '           <th width="33%">Project Name</th>\n' +
                '           <th  width="33%">Project Type</th>\n' +
                '           <th  width="33%">Company</th>\n' +
                '          </tr>\n' +
                '        </thead>\n' +
                '        <tbody>' + options +
                '        </tbody>' +
                ' </table>',

            buttons: {
                Save: async function () {
                    var rankedProjvalues = [];
                    $('#tablePreProject [name="proId"]').each(function (eachh) {
                        console.log(eachh)
                        console.log(this.innerHTML)
                        rankedProjvalues.push(parseInt(this.innerHTML));
                    });
                    console.log(rankedProjvalues)
                    const result = ajaxCall("/studentProject/add", "get", {
                        "pidList": rankedProjvalues
                    })
                    if (result.code == 'error') {
                        $.alert('Something wrong, please try again later');
                        return false;
                    } else {
                        $.alert('Your project preferences has been updated successfully');
                    }


                },
                cancel: function () {
                }

            }
        })
    })
}

function serializeData(form, include, exclude) {
    let form2 = $(form);
    var obj = form2.serializeArray();
    include = include || [];
    exclude = exclude || [];
    var holder = {};
    for (var i = 0; i < obj.length; i++) {
        var key = obj[i]['name'];
        var val = obj[i]['value'];
        if (exclude.indexOf(key) > -1) continue;
        if (0 === include.length || include.indexOf(key) > -1) {
            holder[key] = val;
        }
    }
    return holder;
}

// reset password for all user

async function resetPassword(id) {
    $.ajax({
        url: "/company/getAllJson",
        type: "GET",

    }).then(data => {
        console.log(data);
        //  var options = "";
        // for (let dataKey in data) {
        //     options += "<option value='" + data[dataKey]['id'] + "'>" + data[dataKey]['company_name'] + "</option>"
        // }
        // console.log(options)
        $.confirm({
            theme: 'dark',
            title: 'Enter mentor information',
            content: '' +
                '<form id="mentorForm" class="formName">' +
                '<div class="form-group">' +
                '<input type="hidden" name="role" value="1" />' +
                '<label>Old password</label>' +
                '<input type="password" name="oldpassword" class="oldpassword form-control" required />' +
                '<label>Password</label>' +
                '<input type="password" name="password" class="password form-control" required />' +
                '<label>Confirm Password</label>' +
                '<input type="password" name="conpassword" class="conpassword form-control" required />' +
                '</form>',

            buttons: {
                Save: async function () {
                    var oldpassword = this.$content.find('.oldpassword').val();
                    var password = this.$content.find('.password').val();
                    var conpassword = this.$content.find('.conpassword').val();
                    console.log(password, oldpassword, conpassword)
                    if (password != conpassword) {
                        $.alert('Please input the same password');
                        return false;

                    }
                    var formData = serializeData("form#mentorForm")
                    const checkResult = await ajaxCall("/users/checkPassword", "get", {
                        "id": id,
                        "oldpassword": formData.oldpassword
                    })

                    var jsonData = {
                        "userId": id,
                        "password": password
                    }
                    if (checkResult.code == 'error') {
                        $.alert('Password is wrong, please input again');
                        return false;
                    } else {
                        resetPassword2(jsonData)
                        // renderDataTable("#myTable", "/mentor/getAllJson")
                    }

                },
                cancel: function () {
                }

            }
        })
    })
}


function resetPassword2(fromdata) {
    debugger
    $.ajax({
        url: "/users/resetpassword",
        type: "POST",
        dataType: "JSON",
        data: fromdata,
    }).then(data => {
        if (data.code == 'ok') {
            $.alert("Password has been reset")

        }
    })

}