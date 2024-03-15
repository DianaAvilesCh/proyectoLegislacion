$(document).ready(function () {
    // Agrega un controlador de eventos al formulario
    $('#loginForm').submit(function (event) {
        event.preventDefault();
        // Muestra el indicador de carga antes de realizar la solicitud Ajax
        showLoader();
        // Realiza la solicitud Ajax
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
    var passwordInput1 = document.getElementById('password1');
    var passwordInput2 = document.getElementById('password2');
  
    mostrarPasswordCheckbox.addEventListener('change', function () {
      // Cambiar el tipo de entrada del campo de contraseña
      if(passwordInput==null){
        passwordInput1.type = this.checked ? 'text' : 'password';
        passwordInput2.type = this.checked ? 'text' : 'password';
      }else{
        passwordInput.type = this.checked ? 'text' : 'password';
      }
      
    });
  });