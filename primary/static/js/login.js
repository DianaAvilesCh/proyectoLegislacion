$(document).ready(function () {
    $('#loginForm').submit(function (event) {
        event.preventDefault();
        showLoader();
        $.ajax({
        type: 'POST',
        url: '/login_custom/',
        data: $('#loginForm').serialize(),
        success: function (data) {
            console.log(data.result)
            if(data.result=="1")
                window.location.pathname = data.redirect_url;
            else
                $('#error-message').html(data.message);

            hideLoader();
            console.log()
        },
        error: function () {
            hideLoader();
        }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var mostrarPasswordCheckbox = document.getElementById('mostrarPassword');
    var passwordInput = document.getElementById('password');
  
    mostrarPasswordCheckbox.addEventListener('change', function () {

      passwordInput.type = this.checked ? 'text' : 'password';
      
    });
  });