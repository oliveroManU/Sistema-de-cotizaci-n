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
   // const PrecioVenta = parseFloat(fila.querySelector('.precioventa').value) || 0;

    const ValorPorUnidad = PrecioProducto / CantidadProducto;
    const PrecioCompra = (PrecioProducto  / TasaPagoProducto);
   // const total = ((PrecioVenta - PrecioProducto)/(TasaPagoProducto));
   // const total2 = PrecioVenta - PrecioProducto;  

    fila.querySelector('.precioporunidad').value = ValorPorUnidad.toFixed(2);
    fila.querySelector('.preciod').value = PrecioCompra.toFixed(2);

    fila.querySelector('.total-fin').value = total.toFixed(4);
    fila.querySelector('.total-fin2').value = total2.toFixed(4);

    calcularTotalGeneral();
}