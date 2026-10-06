const inputnombrecliente = document.getElementById('nombre');

if (inputNombreCliente){ 
    inputNombreCliente.addEventListener('input', function () {
    this.value = this.value.replace(/[^a-zA-Z0-9]/g, '');
    if (this.value.length > 0 && this.value.length < 3) {
        this.setCustomValidity('Mínimo 3 caracteres');
    } else {
        this.setCustomValidity('');
    }
});
}

function multiplicacion(elemento) {
    const fila = elemento.closest('form');
    
    const PrecioProducto = parseFloat(fila.querySelector('.precio-producto').value) || 0;
    const CantidadProducto = parseFloat(fila.querySelector('.cantidad-producto').value) || 0;
    const TasaPagoProducto = parseFloat(fila.querySelector('.tasapago').value) || 0;
    const TasaPagoProductoHoy = parseFloat(fila.querySelector('.tasapagohoy').value) || 0;
    const PrecioVenta = parseFloat(fila.querySelector('.precio-venta').value) || 0;

    const ValorPorUnidad = CantidadProducto !== 0 ? PrecioProducto / CantidadProducto : 0;
    const PrecioDolares = TasaPagoProducto !== 0 ? (PrecioProducto  / TasaPagoProducto) : 0;
    const PrecioDolaresHoy = TasaPagoProducto !== 0 ? (PrecioProducto  / TasaPagoProductoHoy) : 0;
    const total = TasaPagoProducto !== 0 ? ((PrecioVenta - PrecioProducto)/(TasaPagoProducto)) : 0;
    const total2 = PrecioVenta - PrecioProducto;  
    const ValorActualDolar = TasaPagoProducto !== 0 ? ((PrecioVenta - PrecioProducto)/(TasaPagoProductoHoy)) : 0;
    const ValorActualBs = PrecioDolares * TasaPagoProductoHoy;  

    fila.querySelector('.precioporunidad').value = ValorPorUnidad.toFixed(2);
    fila.querySelector('.preciod').value = PrecioDolares.toFixed(2);
    fila.querySelector('.preciod1').value = PrecioDolaresHoy.toFixed(2);
    fila.querySelector('.gananciaD').value = total.toFixed(4);
    fila.querySelector('.gananciaBs').value = total2.toFixed(4);
    fila.querySelector('.ValorActualD').value = ValorActualDolar.toFixed(4);
    fila.querySelector('.ValorActualBs').value = ValorActualBs.toFixed(4);

    calcularTotalGeneral();
}