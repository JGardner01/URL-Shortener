function checkPasswordsMatch(){
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;

    if (password !== confirmPassword){
        console.log("False")
        return false;
    }

    console.log("True")
    return true;
}