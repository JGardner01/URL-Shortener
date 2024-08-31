function copyURL(urlCode){
    navigator.clipboard.writeText(window.location.origin + "/" + urlCode)
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