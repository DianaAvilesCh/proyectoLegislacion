document.addEventListener('DOMContentLoaded', () => {
    console.log("ENTRANDO A EDIT");
    // Obtener todos los botones que abren el modal
    var botones = document.querySelectorAll('.btn-edit-vital'); // Usar querySelectorAll y la clase .btn-vital
    botones.forEach(function(boton) { // Iterar sobre todos los botones
      boton.addEventListener('click', function () {
        var id = this.getAttribute('data-id');
        var idpac = this.getAttribute('data-idpac');
        var fecha = this.getAttribute('data-fecha');
        var hora = this.getAttribute('data-hora');
        var temperatura = this.getAttribute('data-temperatura');
        var presion_art = this.getAttribute('data-presion_art');
        var pulse = this.getAttribute('data-pulse');
        var frec_respiratoria = this.getAttribute('data-frec_respiratoria');
        var peso = this.getAttribute('data-peso');
        var talla = this.getAttribute('data-talla');
        var glucosa = this.getAttribute('data-glucosa');
        document.getElementById('idSeleccionado').value = id;
        document.getElementById('idpac').value = idpac;
        document.getElementById('date').value = fecha;
        document.getElementById('time').value = hora;
        document.getElementById('temp').value = temperatura;
        document.getElementById('arterial').value = presion_art;
        document.getElementById('pulso').value = pulse;
        document.getElementById('respiratoria').value = frec_respiratoria;
        document.getElementById('peso').value = peso;
        document.getElementById('talla').value = talla;
        document.getElementById('glucosa').value = glucosa;
        
      });
    });
  });