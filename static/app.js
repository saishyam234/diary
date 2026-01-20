function signup() {
    fetch("/api/signup", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: su_user.value,
            password: su_pass.value
        })
    }).then(r => r.json()).then(d => alert(d.message || d.error));
}

function login() {
    fetch("/api/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: li_user.value,
            password: li_pass.value
        })
    })
    .then(r => r.json())
    .then(d => {
        if (d.access_token) {
            localStorage.setItem("access", d.access_token);
            localStorage.setItem("refresh", d.refresh_token);
            alert("Login successful");
        } else {
            alert(d.error);
        }
    });
}

function logout() {
    localStorage.clear();
    alert("Logged out");
}

function addEntry() {
    fetch("/api/diary", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("access")
        },
        body: JSON.stringify({
            title: title.value,
            content: content.value
        })
    })
    .then(r => r.json())
    .then(d => {
        if (d.error === "Token expired") refreshToken(addEntry);
        else alert(d.message || d.error);
    });
}

function loadEntries() {
    fetch("/api/diary", {
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("access")
        }
    })
    .then(r => r.json())
    .then(data => {
        entries.innerHTML = "";
        data.forEach(e => {
            entries.innerHTML += `<li class="list-group-item"><b>${e.title}</b><br>${e.content}</li>`;
        });
    });
}

function refreshToken(callback) {
    fetch("/api/refresh", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            refresh_token: localStorage.getItem("refresh")
        })
    })
    .then(r => r.json())
    .then(d => {
        localStorage.setItem("access", d.access_token);
        callback();
    });
}
