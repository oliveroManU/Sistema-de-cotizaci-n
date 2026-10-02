const inputnombrecliente = document.getElementById('nombre-producto');

inputnombrecliente.addEventListener('input', function() {

    // Acepta solo letras
    this.value = this.value.replace (/[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]/g, '');  

});

function multiplicacion(elemento) {
    const fila = elemento.closest('form');
    
    const valor1 = parseFloat(fila.querySelector('.precio-producto').value) || 0;
    const valor2 = parseFloat(fila.querySelector('.cantidad-producto').value) || 0;
    const TasaPagoProducto = parseFloat(fila.querySelector('.tasapago').value) || 0;
    const PrecioVenta = parseFloat(fila.querySelector('.precioventa').value) || 0;

    const gasto = valor1 / valor2;
    const PrecioCompra = (valor1  / TasaPagoProducto);
    const total = PrecioVenta - PrecioCompra;
    const total2 = PrecioVenta - valor1;  

    fila.querySelector('.multiplicacion-precio-cantidad').value = gasto.toFixed(2);
    fila.querySelector('.preciocompra').value = PrecioCompra.toFixed(2);

    fila.querySelector('.total-fin').value = total.toFixed(2);
    fila.querySelector('.total-fin2').value = total2.toFixed(2);

    calcularTotalGeneral();
}