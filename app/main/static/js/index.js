document.addEventListener("DOMContentLoaded", function () {
   const timezoneOffset = new Date().getTimezoneOffset();
   const expirationInput = document.getElementById("expirationDate");

   const timezoneInput = document.createElement("input");
   timezoneInput.setAttribute("type", "hidden");
   timezoneInput.setAttribute("name", "timezoneOffset");
   timezoneInput.setAttribute("value", timezoneOffset);
   expirationInput.parentNode.appendChild(timezoneInput)
});

function openURL(url){

   window.open(url, '_blank');

}

function copyURL(urlCode){
   if (urlCode.startsWith("http")){
      navigator.clipboard.writeText(urlCode)
   }
   else{
      navigator.clipboard.writeText(window.location.origin + "/" + urlCode)
   }
}