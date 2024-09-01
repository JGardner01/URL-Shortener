function copyURL(urlCode){
    navigator.clipboard.writeText(window.location.origin + "/" + urlCode)
}

function editURL(shortURLCode, originalURL, expirationDate, clickLimit){
    document.getElementById('shortURLCode').value = shortURLCode;
    document.getElementById('customShortCode').value = shortURLCode;
    document.getElementById('newExpirationDate').value = expirationDate;
    document.getElementById('newClickLimit').value = clickLimit || '';

}

function submitEditForm() {
    const shortURLCode = document.getElementById('shortURLCode').value;
    const customShortCode = document.getElementById('customShortCode').value;
    const newExpirationDate = document.getElementById('newExpirationDate').value;
    const newClickLimit = document.getElementById('newClickLimit').value;
    const newPassword = document.getElementById('newPassword').value;

    const timezoneOffset = new Date().getTimezoneOffset();
    const newExpirationInput = document.getElementById("newExpirationDate");
    const timezoneInput = document.createElement("input");
    timezoneInput.setAttribute("type", "hidden");
    timezoneInput.setAttribute("name", "timezoneOffset");
    timezoneInput.setAttribute("value", timezoneOffset);
    newExpirationInput.parentNode.appendChild(timezoneInput)

    fetch("/edit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            shortURLCode: shortURLCode,
            customURLCode: customShortCode,
            newExpirationDate: newExpirationDate,
            newClickLimit: newClickLimit,
            newPassword: newPassword
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("URL updated successfully!");
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
