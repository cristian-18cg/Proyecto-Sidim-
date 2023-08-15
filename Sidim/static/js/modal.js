// Espera a que se cargue el documento
/*document.addEventListener("DOMContentLoaded", function() {
    // Obtén el elemento del logo
    var logo = document.querySelector("user-icon");
  
    // Agrega un evento de clic al logo
    logo.addEventListener("click", function() {
      // Obtén el modal por su ID
      var modal = document.getElementById("registroModal");
  
      // Activa el modal utilizando el método modal() de Bootstrap
      // asegúrate de haber incluido los archivos JavaScript de Bootstrap en tu página
      var bootstrapModal = new bootstrap.Modal(modal);
      bootstrapModal.show();
    });
  });*/
  



  $(document).ready(function () {
    // Mostrar ventana modal de inicio de sesión al hacer clic en el ícono de usuario
    console.log("¡El archivo mi_script.js está funcionando correctamente!");
    $('#user-icon').click(function () {
      $('#loginModal').addClass('open');
    });

    // Mostrar ventana modal de registro al hacer clic en el enlace "Regístrate"
    $('#registerLink').click(function () {
      $('#registerModal').addClass('open');
      $('#loginModal').removeClass('open'); // Ocultar ventana modal de inicio de sesión si estaba abierta
    });

    // Mostrar ventana modal de inicio de sesión al hacer clic en el botón "Volver atrás" en el formulario de registro
    $('#backToLogin').click(function () {
      $('#loginModal').addClass('open');
      $('#registerModal').removeClass('open'); // Ocultar ventana modal de registro
    });

    // Cerrar ventana modal al hacer clic fuera del contenido
    $('.modal-side').click(function (event) {
      if (!$(event.target).parents('.modal-content').length) {
        $('.modal-side').removeClass('open');
      }
    });


    // Cerrar ventana modal al hacer clic en el botón de cerrar
    $('.close').click(function () {
      $('.modal-side').removeClass('open');
    });
  });

  
  
  
  
  //evita que se cierre el modal si hay errores 
  
  