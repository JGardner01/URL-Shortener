function displayShortURL(shortURLCode, originalURL, createdDate, lastAccessed, expirationDate, clickCount, clickLimit, qr){
    document.getElementById("displayShortURL").value = window.location.origin + "/" + shortURLCode;
    document.getElementById("displayShortURL").href = window.location.origin + "/" + shortURLCode;
    document.getElementById("displayOriginalURL").value = originalURL;
    document.getElementById("displayCreatedDate").value = formatDateTime(createdDate);

    if (lastAccessed !== null && lastAccessed !== undefined && lastAccessed !== "None"){
        document.getElementById("displayLastAccessed").value = formatDateTime(lastAccessed);
    } else {
        document.getElementById("displayLastAccessed").value = "Never";
    }

    document.getElementById("displayExpirationDate").value = formatDateTime(expirationDate);

    if (clickLimit){
        document.getElementById("displayClickCount").value = clickCount + "/" + clickLimit;
    } else{
        document.getElementById("displayClickCount").value = clickCount;
    }

    document.getElementById("displayQRCode").src = "data:image/png;base64," + qr;
    document.getElementById("qrDownload").onclick({

    });
}

function submitNewForm() {
    const url = document.getElementById("url").value
    const customShortCode = document.getElementById("customShortCode").value
    const expirationDate = document.getElementById("expirationDate").value
    const clickLimit = document.getElementById("clickLimit").value
    const password = document.getElementById("password").value
    const timezoneOffset = new Date().getTimezoneOffset();

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
                alert("Your URL was shortened successfully \n("+ url + ")");
                location.reload();

                //displayShortURL(data.short_url_code, url, data.created_date, null, data.expiration_date, 0, clickLimit, data.qr);
                //var modal = new bootstrap.Modal(document.getElementById("displayShortUrlModal"));
                //modal.show();

            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => console.error("Error:", error));
}

function editURL(shortURLCode, originalURL, expirationDate, clickLimit){
    document.getElementById("shortURLCode").value = shortURLCode;
    document.getElementById("newCustomShortCode").placeholder = shortURLCode;
    document.getElementById("newExpirationDate").value = expirationDate;
    document.getElementById("newClickLimit").value = clickLimit || 0;
}

function submitEditForm() {
    const shortURLCode = document.getElementById("shortURLCode").value;
    const customShortCode = document.getElementById("newCustomShortCode").value;
    const newExpirationDate = document.getElementById("newExpirationDate").value;
    const newClickLimit = document.getElementById("newClickLimit").value;
    const newPassword = document.getElementById("newPassword").value;
    const timezoneOffset = new Date().getTimezoneOffset();

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

function shareURL(shortURLCode, qr){
    document.getElementById("shareShortURL").value = window.location.origin + "/" + shortURLCode;
    document.getElementById("shareShortURL").href = window.location.origin + "/" + shortURLCode;
    document.getElementById("shareQRCode").src = "data:image/png;base64," + qr;
}

function copyURL(urlCode){
    if (urlCode.startsWith("http")){
        navigator.clipboard.writeText(urlCode)
    }
    else{
        navigator.clipboard.writeText(window.location.origin + "/" + urlCode)
    }
}

function copyQR(qr){

}

function openURL(url){

    window.open(url, '_blank');

}

function formatDateTime(dateTimeString){
    const dateTime = new Date(dateTimeString);
    const day = String(dateTime.getDay()).padStart(2, '0');
    const month = String(dateTime.getMonth()).padStart(2, '0');
    const year = String(dateTime.getFullYear());
    const hour = String(dateTime.getHours()).padStart(2, '0');
    const min = String(dateTime.getMinutes()).padStart(2, '0');

    return `${day}-${month}-${year} ${hour}:${min}`
}