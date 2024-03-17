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
    button.addEventListener('click', (event) => {
      event.preventDefault(); // Evitar la acción por defecto del botón (enviar formulario)
      const modal = button.closest('.modal');
      // Limpiar todos los campos de formulario dentro del modal
      modal.querySelectorAll('input').forEach(input => {
        input.value = ''; // Establece el valor del campo a una cadena vacía
      });
      modal.classList.remove('is-active');
    });
  });
});

document.addEventListener('DOMContentLoaded', () => {
  // Obtener todos los botones que abren el modal
  var botones = document.querySelectorAll('.btn-vital'); // Usar querySelectorAll y la clase .btn-vital
  botones.forEach(function(boton) { // Iterar sobre todos los botones
    boton.addEventListener('click', function () {
      var id = this.getAttribute('data-id');
      var cedula = this.getAttribute('data-cedula');
      document.getElementById('idSeleccionado').value = id;
      document.getElementById('nombreSeleccionado').textContent = cedula;
    });
  });
});