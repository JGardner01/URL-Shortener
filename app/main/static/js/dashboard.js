function displayShortURL(){

}

function copyURL(urlCode){
    navigator.clipboard.writeText(window.location.origin + "/" + urlCode)
}

function submitNewForm() {
    const url = document.getElementById("url").value
    const customShortCode = document.getElementById("customShortCode").value
    const expirationDate = document.getElementById("expirationDate").value
    const clickLimit = document.getElementById("clickLimit").value
    const password = document.getElementById("password").value
    const timezoneOffset = getTimezoneOffset()

    fetch("/shorten", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            url: url,
            customURLCode: customShortCode,
            expirationDate: expirationDate,
            timezoneOffset: timezoneOffset,
            clickLimit: clickLimit,
            password: password
        })
    })
        .then (response => response.json())
        .then(data => {
            if (data.success) {
                alert("Your URL was shortened successfully ("+ url + ")");
                location.reload(); //////
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => console.error("Error:", error));
}

function editURL(shortURLCode, originalURL, expirationDate, clickLimit){
    document.getElementById('shortURLCode').value = shortURLCode;
    document.getElementById('newCustomShortCode').placeholder = shortURLCode;
    document.getElementById('newExpirationDate').value = expirationDate;
    document.getElementById('newClickLimit').value = clickLimit || 0;
}

function submitEditForm() {
    const shortURLCode = document.getElementById('shortURLCode').value;
    const customShortCode = document.getElementById('newCustomShortCode').value;
    const newExpirationDate = document.getElementById('newExpirationDate').value;
    const newClickLimit = document.getElementById('newClickLimit').value;
    const newPassword = document.getElementById('newPassword').value;
    const timezoneOffset = getTimezoneOffset()

    fetch("/edit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            shortURLCode: shortURLCode,
            customURLCode: customShortCode,
            newExpirationDate: newExpirationDate,
            timezoneOffset: timezoneOffset,
            newClickLimit: newClickLimit,
            newPassword: newPassword
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Shortened URL ("+ shortURLCode + ") updated successfully!");
                location.reload();
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => console.error("Error:", error));


}

function deleteURL(urlCode){
    if (confirm("Are you sure you want to delete this shortened URL?")) {
        fetch("/delete", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({short_url_code: urlCode})
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Shortened URL ("+ urlCode + ") was deleted successfully");
                    const row = document.querySelector(`tr[data-url-code="${urlCode}"]`);
                    if (row) {
                        row.remove();
                    }
                } else {
                    alert("Error: " + (data.error));
                }
            })
            .catch(error => console.error("Error:", error));
    }
}

function getTimezoneOffset() {
    const timezoneOffset = new Date().getTimezoneOffset();
    const timezoneInput = document.createElement("input");
    timezoneInput.setAttribute("type", "hidden");
    timezoneInput.setAttribute("name", "timezoneOffset");
    timezoneInput.setAttribute("value", timezoneOffset);
    return timezoneInput;
}