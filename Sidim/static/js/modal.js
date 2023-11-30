
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





// Muestra el modal y establece el mensaje de error cuando sea necesario
function showErrorModal(message) {
const errorMessageElement = document.getElementById('errorMessage');
errorMessageElement.textContent = message;
const errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
errorModal.show();
}





  