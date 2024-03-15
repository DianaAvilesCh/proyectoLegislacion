$(document).ready(function () {
  $('#registerForm').submit(function (event) {
    event.preventDefault();

    var dniSinGuion = $('#dni').val().replace('-', '');
    $('#dni').val(dniSinGuion);
    var senecySinGuion = $('#rec_senecyt').val().replace('-', '');
    $('#rec_senecyt').val(senecySinGuion);

    showLoader();
    // Realiza la solicitud Ajax
    $.ajax({
      type: 'POST',
      url: '/register/',
      data: $('#registerForm').serialize(),
      success: function (data) {
        //console.error("Error en la solicitud AJAX:",data,data.formHTML)

        if(data.redirect_url=="login_custom")
          window.location.pathname = data.redirect_url;
        else
        {
          var registerForm = document.getElementById('registerForm');
          registerForm.innerHTML = data.formHTML;
          validarCedula()
          validarSenecyt()
        }
          
        // Oculta el indicador de carga
        hideLoader();
      },
      error: function (xhr, textStatus, errorThrown) {
        // Manejar errores si es necesario
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

function validarCedula() {
  var cedulaInput = document.getElementById('dni');
  var cedulaValue = cedulaInput.value.trim();
  var cedulaRegex = /\d{10}/g;
  if (cedulaRegex.test(cedulaValue)) {
      cedulaValue = `${cedulaValue.slice(0, 9)}-${cedulaValue.slice(9)}`;
  }
  if(cedulaValue.length == 10 && cedulaValue.slice(9)=="-"){
      cedulaValue = `${cedulaValue.slice(0, 9)}`;
  }  
  cedulaInput.value = cedulaValue;
}


document.getElementById('dni').addEventListener('input', validarCedula);