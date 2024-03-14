document.addEventListener('DOMContentLoaded', () => {

  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Add a click event on each of them
  $navbarBurgers.forEach(el => {
    el.addEventListener('click', () => {

      // Get the target from the "data-target" attribute
      const target = el.dataset.target;
      const $target = document.getElementById(target);

      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      el.classList.toggle('is-active');
      $target.classList.toggle('is-active');

    });
  });

});
//js de modales
document.addEventListener('DOMContentLoaded', () => {
  // Encuentra todos los botones que abren modales
  document.querySelectorAll('.modal-button').forEach(button => {
    button.addEventListener('click', () => {
      const modalID = button.getAttribute('data-target');
      const modal = document.getElementById(modalID);
      modal.classList.add('is-active');
    });
  });

  // Encuentra todos los elementos para cerrar modales
  document.querySelectorAll('.close-modal-button').forEach(button => {
    button.addEventListener('click', () => {
      const modal = button.closest('.modal');
      modal.classList.remove('is-active');
    });
  });
});

document.addEventListener('DOMContentLoaded', () => {
  console.log("ESTOY ENTRANDO");
  // Obtener todos los botones que abren el modal
  var botones = document.querySelectorAll('.btn-vital'); // Usar querySelectorAll y la clase .btn-vital
  botones.forEach(function(boton) { // Iterar sobre todos los botones
    boton.addEventListener('click', function () {
      var id = this.getAttribute('data-id');
      var nombre = this.getAttribute('data-nombre');
      var apellido = this.getAttribute('data-apellido');
      document.getElementById('idSeleccionado').textContent = id;
      document.getElementById('nombreSeleccionado').textContent = nombre+" "+apellido;
    });
  });
});