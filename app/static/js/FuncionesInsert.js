function validarFormulario() {
    // Seleccionamos los inputs por su clase
    const camposObligatorios = [
        document.querySelector('.nombre'),
        document.querySelector('.marca'),
        document.querySelector('.precio-producto'),
        document.querySelector('.cantidad-producto'),
        document.querySelector('.precioporunidad'),
        document.querySelector('.precio')
    ];

    let errores = [];

    camposObligatorios.forEach(campo => {
        // ⚠️ Protección: si el campo no existe, saltamos
        if (!campo) {
            console.warn("⚠️ Algún selector no encontró el elemento. Revisa las clases en el HTML.");
            return;
        }

        campo.classList.remove('error'); // Quitar error previo
        
        if (campo.value.trim() === "") {
            campo.classList.add('error'); // Borde rojo
            // Usamos el placeholder o el name para el mensaje (más amigable)
            errores.push(campo.placeholder || campo.name || 'campo');
        }
    });

    if (errores.length > 0) {
        alert("Faltan datos en: " + errores.join(", "));
        return false;
    }

    return true;
}

// Asignar al botón ( verifica el ID real en tu HTML)
document.getElementById('form').addEventListener('submit', function(e) {
    // Si la validación falla, bloqueamos el envío
    if (!validarFormulario()) {
        e.preventDefault(); 

        

    }
    
    // Si pasa la validación, el navegador envía el formulario normalmente
});

if (boton) {
    boton.addEventListener('click', function(e) {
        e.preventDefault();
        if (validarFormulario()) {
            console.log(" Validación exitosa. Guardando...");
            // Aquí va tu código para guardar los datos
            alert("¡Registro exitoso!");
        }
    });
} else {
    console.error(" No se encontró el botón. Revisa el ID en el HTML.");
}



function multiplicacion(elemento) {
    const fila = elemento.closest('form');
    
    const PrecioProducto = parseFloat(fila.querySelector('.precio-producto').value) || 0;
    const CantidadProducto = parseFloat(fila.querySelector('.cantidad-producto').value) || 0;
    const TasaPagoProducto = parseFloat(fila.querySelector('.tasapago').value) || 0;
    const TasaPagoProductoE = parseFloat(fila.querySelector('.tasapagoE').value) || 0;
    const PrecioVenta = parseFloat(fila.querySelector('.precio-venta').value) || 0;

    const ValorPorUnidad = CantidadProducto !==0 ? PrecioProducto / CantidadProducto : 0;
    const PrecioCompra = (PrecioProducto  / TasaPagoProducto);
    const PrecioCompraE = (PrecioProducto / TasaPagoProductoE)
    const total = ((PrecioVenta - PrecioProducto)/(TasaPagoProducto));
    const total2 = PrecioVenta - PrecioProducto;  

    fila.querySelector('.precioporunidad').value = ValorPorUnidad.toFixed(2);
    fila.querySelector('.preciod').value = PrecioCompra.toFixed(2);
    fila.querySelector('.precioe').value = PrecioCompraE.toFixed(2);
    fila.querySelector('.gananciaD').value = total.toFixed(4);
    fila.querySelector('.gananciaBs').value = total2.toFixed(4);

    calcularTotalGeneral();
}