function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function judge_code(question, lang) {
    let code_value = editor.getValue();
    console.log(code_value);
    let data = {
        code: code_value,
        language: lang,
        question_id: question
    };
    if (code_value !== null) {
        const execution_status = document.getElementById("execution-status");
        const msg = document.getElementById("message");
        const op = document.getElementById("output");
        execution_status.innerHTML = "Processing ...";
        const fetchPromise = fetch('/api/judge/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": 'application/json;charset=utf-8',
            },
            body: JSON.stringify(data)
        });
        console.log(JSON.stringify(data))
        fetchPromise.then(response => {
            return response.json();
        }).then(execution => {
            console.log(execution);
            if (execution["status"] == "Wrong Answer"){
                execution_status.innerHTML = execution["status"] + ":(";
                execution_status.style.color = "red";
                op.innerHTML = execution["output"];
            }
            else if (execution["status"] == "Accepted"){
                execution_status.innerHTML = execution["status"] + "👍";
                execution_status.style.color = "green";
                op.innerHTML = execution["output"];
            }
            execution_status.innerHTML = execution["status"];
            op.innerHTML = execution["output"];
            msg.innerHTML = execution["error"];
        });
    }
}

function submit_code (ques, stu, assg) {
    let code_value = editor.getValue();
    console.log(code_value);
    var blob = new Blob([code_value], { type: 'text/plain' });
    var file = new File([blob], "foo.txt", {type: "text/plain"});
    console.log(file);
    let data = {
        submission: file,
        question: ques,
        student: stu,
        assignment: assg
    };
    if (code_value !== null) {
        const execution_status = document.getElementById("execution-status");
        const msg = document.getElementById("message");
        const op = document.getElementById("output");
        execution_status.innerHTML = "Processing ...";
        const fetchPromise = fetch('/api/submissions/create', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": 'application/json;charset=utf-8',
                //'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: JSON.stringify(data)
        });
        console.log(JSON.stringify(data))
        fetchPromise.then(response => {
            return response.json();
        }).then(execution => {
            console.log(execution);
            if (execution["status"] == "Wrong Answer"){
                execution_status.innerHTML = execution["status"] + ":(";
                execution_status.style.color = "red";
                op.innerHTML = execution["output"];
            }
            else if (execution["status"] == "Accepted"){
                execution_status.innerHTML = execution["status"] + "👍";
                execution_status.style.color = "green";
                op.innerHTML = execution["output"];
            }
            execution_status.innerHTML = execution["status"];
            op.innerHTML = execution["output"];
            msg.innerHTML = execution["error"];
        });
    }
}