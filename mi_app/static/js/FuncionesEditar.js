const inputnombrecliente = document.getElementById('.nombre');

inputNombreCliente.addEventListener('input', function () {
    // 1) Solo letras y números
    this.value = this.value.replace(/[^a-zA-Z0-9]/g, '');

    // 2) Validar longitud mínima
    if (this.value.length > 0 && this.value.length < 3) {
        this.setCustomValidity('Mínimo 3 caracteres');
    } else {
        this.setCustomValidity('');
    }
});

function multiplicacion(elemento) {
    const fila = elemento.closest('form');
    
    const PrecioProducto = parseFloat(fila.querySelector('precioporproducto').value) || 0;
    const CantidadProducto = parseFloat(fila.querySelector('cantidad-producto').value) || 0;
    const TasaPagoProducto = parseFloat(fila.querySelector('tasapago').value) || 0;
    const PrecioVenta = parseFloat(fila.querySelector('precio-venta').value) || 0;

    const ValorPorUnidad = PrecioProducto / CantidadProducto;
    const PrecioCompra = (PrecioProducto  / TasaPagoProducto);
    const total = ((PrecioVenta - PrecioProducto)/(TasaPagoProducto));
    const total2 = PrecioVenta - PrecioProducto;  

    fila.querySelector('.precioporunidad').value = ValorPorUnidad.toFixed(2);
    fila.querySelector('.preciod').value = PrecioCompra.toFixed(2);

    fila.querySelector('.gananciaD').value = total.toFixed(4);
    fila.querySelector('.gananciaBs').value = total2.toFixed(4);

    calcularTotalGeneral();
}