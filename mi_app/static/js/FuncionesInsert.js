const inputnombrecliente = document.getElementById('nombre-producto');

inputnombrecliente.addEventListener('input', function() {

    // Acepta solo letras
    this.value = this.value.replace (/[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]/g, '');  

});

function multiplicacion(elemento) {
    const fila = elemento.closest('form');
    
    const PrecioProducto = parseFloat(fila.querySelector('.precio-producto').value) || 0;
    const CantidadProducto = parseFloat(fila.querySelector('.cantidad-producto').value) || 0;
    const TasaPagoProducto = parseFloat(fila.querySelector('.tasapago').value) || 0;
    const PrecioVenta = parseFloat(fila.querySelector('.precio-venta').value) || 0;

    const ValorPorUnidad = CantidadProducto !==0 ? PrecioProducto / CantidadProducto : 0;
    const PrecioCompra = (PrecioProducto  / TasaPagoProducto);
    const total = ((PrecioVenta - PrecioProducto)/(TasaPagoProducto));
    const total2 = PrecioVenta - PrecioProducto;  

    fila.querySelector('.precioporunidad').value = ValorPorUnidad.toFixed(2);
    fila.querySelector('.preciod').value = PrecioCompra.toFixed(2);

    fila.querySelector('.gananciaD').value = total.toFixed(4);
    fila.querySelector('.gananciaBs').value = total2.toFixed(4);

    calcularTotalGeneral();
}