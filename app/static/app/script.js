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

function show_execution_status (execution) {
    const execution_status_div = document.getElementById("execution");
    execution_status_div.innerHTML = "";
    var message = document.createElement('div');
    message.setAttribute('id', 'message');

    var output = document.createElement('div');
    output.setAttribute('id', 'output');
    
    if (execution["status"] == "Wrong Answer"){
        message.innerHTML = execution["status"] + "😢";
        output.innerHTML = execution["output"];
    }
    else if (execution["status"] == "Accepted"){
        message.innerText += execution["status"] + "👍";
        output.innerText += execution["output"];
    }
    else {
        output.innerText += execution["output"];
        message.innerText += execution["error"];
    }
    execution_status_div.appendChild(message);
    execution_status_div.appendChild(output);
}

function judge_code(question, lang) {
    let code_value = editor.getValue();
    const api_url = window.origin + '/api/';
    let execution_status = document.getElementById("execution");
    if (code_value !== null) {
        let data = {
            code: code_value,
            language: lang,
            question_id: question
        };
        execution_status.style.display = 'block';
        execution_status.innerHTML = "Processing ...";
        const fetchPromise = fetch(api_url+'judge/', {
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
            show_execution_status(execution);
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