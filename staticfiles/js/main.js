let menu = document.querySelector('#menu-btn');
let navbar = document.querySelector('.navbar');

menu.onclick = () =>{
  menu.classList.toggle('fa-times');
  navbar.classList.toggle('active');
}

window.onscroll = () =>{
  menu.classList.remove('fa-times');
  navbar.classList.remove('active');
}
function showLoader() {
  $('#loader').show();
  document.getElementById('overlay').style.display = 'block';
}

function hideLoader() {
  $('#loader').hide();
  document.getElementById('overlay').style.display = 'none';
}

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
        // Redirige a la nueva ruta si es necesario
        window.location.pathname = data.redirect_url;
        // Oculta el indicador de carga
        hideLoader();
      },
      error: function () {
        // Manejar errores si es necesario
        hideLoader();
      }
    });
  });
  // Agrega un controlador de eventos al formulario
  $('#registerForm').submit(function (event) {
    event.preventDefault();

    // Muestra el indicador de carga antes de realizar la solicitud Ajax
    showLoader();

    // Realiza la solicitud Ajax
    $.ajax({
      type: 'POST',
      url: '/register/',
      data: $('#registerForm').serialize(),
      success: function (data) {
        

        // Redirige a la nueva ruta si es necesario
        window.location.pathname = data.redirect_url;
        // Oculta el indicador de carga
        hideLoader();
      },
      error: function () {
        // Manejar errores si es necesario
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