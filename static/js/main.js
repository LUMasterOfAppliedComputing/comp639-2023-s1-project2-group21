jQuery.validator.setDefaults({
    debug: true,
    success: "valid"
});


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

        }
    })

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
                        getAllMentors("#myTable", "/mentor/getAllJson")
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
            $.alert("Looks like you haven't completed our survey, before you use our system you must complete all the them")
        }
    })
}

function getAllMentors(formId, url, columns, flag) {
    setTimeout(3000);
    $.ajax({
            url: url,
            type: "get",
            dataType: "JSON",
            success: function (data) {
                var columnDefs = []
                if (flag) {
                    columnDefs = [
                        {
                            "targets": -1,
                            "render": function (data, type, full, meta) {
                                return "<input type='button' onclick='alert(2)' value='edit'> <input type='button' onclick='alert(1)' value='delete' {%end if%}>"
                            }
                        }]
                }
                if ($.fn.dataTable.isDataTable(formId)) {
                    console.log("dataTable1")
                    let dataTable1 = $(formId).dataTable();
                    dataTable1.fnClearTable()
                    dataTable1.fnAddData(data, true)
                } else {
                    $(formId).dataTable({
                        "bAutoWidth": true,
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
