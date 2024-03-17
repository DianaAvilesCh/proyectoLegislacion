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