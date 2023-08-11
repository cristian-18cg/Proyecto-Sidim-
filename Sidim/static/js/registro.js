// Función para mostrar el formulario de registro
function showRegisterForm() {
    document.getElementById('registerForm').style.display = 'block';
  }
  
  // Función para ocultar el formulario de registro
  function hideRegisterForm() {
    document.getElementById('registerForm').style.display = 'none';
  }
  
  // Obtener el enlace "Regístrate"
  var registerLink = document.getElementById('registerLink');
  
  // Agregar un controlador de eventos al enlace
  registerLink.addEventListener('click', function(event) {
    event.preventDefault(); // Evitar el comportamiento predeterminado del enlace
    showRegisterForm(); // Mostrar el formulario de registro
  });
  
  // Obtener el botón "Cerrar" en el formulario de registro
  var closeButton = document.getElementById('closeButton');
  
  // Agregar un controlador de eventos al botón "Cerrar"
  closeButton.addEventListener('click', function(event) {
    event.preventDefault(); // Evitar el comportamiento predeterminado del botón
    hideRegisterForm(); // Ocultar el formulario de registro
  });
  