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
    console.log(question);
    console.log(lang);
    const code = document.getElementById("editor");
    let data = {
        code: code.value,
        language: lang,
        question_id: question
    };
    if (code !== null) {
        const execution_status = document.getElementById("execution-status");
        execution_status.innerHTML = "Running Code ...";
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
            console.log("api work");
            console.log(execution);
            execution_status.innerHTML = execution["status"];
        });
    }
}