$(document).ready(function () {
  $('#registerForm').submit(function (event) {
    event.preventDefault();
    const csrftoken = getCookie('csrftoken');
    showLoader();
    $.ajax({
      type: 'POST',
      headers: {'X-CSRFToken': csrftoken},
      url: '/register/',
      data: $('#registerForm').serialize(),
      success: function (data) {
        if (data.result == 'success') {
          window.location.pathname = data.redirect_url;
        } 
        else{
          for (var field in data.errors) {
            for (var i = 0; i < data.errors[field].length; i++) {
              mostrarAlerta(data.errors[field][i], 'danger', '#alertMessage');
            }
          }
        }
        hideLoader();
      },
      error: function (xhr, textStatus, errorThrown) {
        console.error("Error en la solicitud AJAX:", textStatus, errorThrown);
        hideLoader();
      }
    });
  });

});

document.addEventListener('DOMContentLoaded', function () {
  var mostrarPasswordCheckbox = document.getElementById('mostrarPassword');
  var passwordInput1 = document.getElementById('password1');
  var passwordInput2 = document.getElementById('password2');

  mostrarPasswordCheckbox.addEventListener('change', function () {
    passwordInput1.type = this.checked ? 'text' : 'password';
    passwordInput2.type = this.checked ? 'text' : 'password';    
  });
});

function mostrarAlerta(mensaje, tipo,direccion) {
  var alertMessage = $(direccion);

  var errorHTML = '<div class="alert alert-' + tipo + '">' + mensaje + '</div>';

  alertMessage.append(errorHTML).show();
  setTimeout(function () {
      alertMessage.hide();
      alertMessage.empty();
  }, 15000); 
}