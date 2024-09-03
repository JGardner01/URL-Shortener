function getFullURL(shortURLCode){
    return window.location.origin + '/' + shortURLCode;
}

function shareEmail(shortURLCode, qr) {
    const url = getFullURL(shortURLCode)
    const qrImage = `<img src="data:image/png;base64,${qr}" alt="QR Code">`;
    const body = encodeURIComponent(url) + encodeURIComponent(qrImage);
    window.open(`mailto:?&body=${body}`, '_blank');
}

function shareOnX(shortURLCode) {
    const url = getFullURL(shortURLCode)
    window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}`, '_blank');
}

function shareOnFacebook(shortURLCode) {
    const url = getFullURL(shortURLCode)
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`, '_blank');
}

function shareOnLinkedIn(shortURLCode) {
    const url = getFullURL(shortURLCode)
    window.open(`https://www.linkedin.com/sharing/share-offsite/?text=${encodeURIComponent(url)}`, '_blank');
}

function shareOnWhatsapp(shortURLCode) {
    const url = getFullURL(shortURLCode)
    window.open(`https://api.whatsapp.com/send?text=${url}`, '_blank');
}

function shareOnReddit(shortURLCode) {
    const url = getFullURL(shortURLCode)
    window.open(`https://www.reddit.com/submit?url=${encodeURIComponent(url)}`, '_blank');
}