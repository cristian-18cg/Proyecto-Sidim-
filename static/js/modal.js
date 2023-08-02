// Espera a que se cargue el documento
document.addEventListener("DOMContentLoaded", function() {
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
  });
  