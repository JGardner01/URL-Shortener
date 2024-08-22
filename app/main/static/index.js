document.addEventListener("DOMContentLoaded", function () {
   const timezoneOffset = new Date().getTimezoneOffset();
   const expirationInput = document.getElementById("expirationDate");

   const timezoneInput = document.createElement("input");
   timezoneInput.setAttribute("type", "hidden");
   timezoneInput.setAttribute("name", "timezoneOffset");
   timezoneInput.setAttribute("value", timezoneOffset);
   expirationInput.parentNode.appendChild(timezoneInput)
});