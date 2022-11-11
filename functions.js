

$(document).ready(function(){
    $(".get").click(function(){
        var a;
        /*$.get("grades.txt", function(text){
            a = text
            alert("Name:" + a);
        }, 'text');
        */
        $.ajax({
            url: "http://127.0.0.1:5000/grades",
            success: function (data){
                //const blockOfText = JSON.stringify(data);
                //const obj = JSON.parse(blockOfText);
                //Have to clear display
                a = Name.value;
                console.log(data[a]);
                alert("Grade of " + a + " is: " + data[a]);
                $('#GradeDisplay').append("The grade of "+ a + " is " + data[a])
            }
        });
    });
    $(".getAll").click(function(){
        $.ajax({
            url: "http://127.0.0.1:5000/grades",
            success: function (data){
                const blockOfText = JSON.stringify(data, null, 4);
                //const obj = JSON.parse(blockOfText);
                //document.body.innerHTML = blockOfText;
                $("#gradeTable tbody tr").remove();
                console.log(Object.keys(data));
                console.log(Object.values(data));
                var student = '';
                $.each(data, function(key, value){
                    //Initialize a new row
                    student += '<tr>'
                    student += '<td>' + key + '</td>';
                    student += '<td>' + value + '</td>';    
                    student +=  '<\tr>'
                });
                $('#gradeTable').append(student);
            }
        });        
    });


    $(".addStudent").click(function(){
        //Making a POST call
        var name, grade;
        name = $('#Name').val();
        grade = parseFloat($('#Grade').val());

        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "http://127.0.0.1:5000/grades");
        xhttp.setRequestHeader("Content-Type", "application/json");
        const body = {"name":name, "grade": grade};
        xhttp.send(JSON.stringify(body));
        xhttp.onload = function() {
            
        };

        newStudent = '';
        newStudent += '<tr>';
        newStudent += '<td>' + Name.value + '</td>';
        newStudent += '<td>' + Grade.value + '</td>';
        newStudent += '</tr>';
        $('#gradeTable').append(newStudent);

    });


    $(".editGrade").click(function(){
        var name, grade;
        name = $('#Name').val();
        grade = parseFloat($('#Grade').val());
        var xhttp = new XMLHttpRequest();
        xhttp.open("PUT", "http://127.0.0.1:5000/grades/" + encodeURIComponent(name));
        xhttp.setRequestHeader("Content-Type", "application/json");
        const body = {"grade": grade};
        xhttp.send(JSON.stringify(body));
        xhttp.onload = function() {
            
        };        
    });
    $(".deleteGrade").click(function(){
        var name, grade;
        name = $('#Name').val();
        grade = parseFloat($('#Grade').val());
        var xhttp = new XMLHttpRequest();
        xhttp.open("DELETE", "http://127.0.0.1:5000/grades/" + encodeURIComponent(name));
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send();
        xhttp.onload = function() {
            
        };        
    });
    $(".enrollStudent").click(function(){
        var username, classname;
        username = String($('#username').val());
        classname = String($('#classname').val());
        var xhttp = new XMLHttpRequest();
        xhttp.open("PUT", "http://127.0.0.1:5000/enroll");
        xhttp.setRequestHeader("Content-Type", "application/json");
        const body = {"username": username ,"classname": classname};
        xhttp.send(JSON.stringify(body));
        xhttp.onload = function() {      

        };
    });
    $(".deleteStudent").click(function(){
        var username, classname;
        username = String($('#username').val());
        classname = String($('#classname').val());
        var xhttp = new XMLHttpRequest();
        xhttp.open("DELETE", "http://127.0.0.1:5000/unenroll");
        xhttp.setRequestHeader("Content-Type", "application/json");
        const body = {"username": username ,"classname": classname};
        xhttp.send(JSON.stringify(body));
        xhttp.onload = function() {      

        };
    });

});