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
    const PorcentajeValorActualDolar = TasaPagoProducto !== 0 ? ((PrecioVenta - PrecioProducto)/(TasaPagoProductoHoy)) : 0;
    const PorcentajeCompraVenta =  ((PrecioVenta - PrecioProducto) / PrecioProducto) * 100 
    const PorcentajeDevaluacion = ((TasaPagoProductoHoy - TasaPagoProducto)/TasaPagoProducto)*100
    

    fila.querySelector('.precioporunidad').value = ValorPorUnidad.toFixed(2);
    fila.querySelector('.preciod').value = PrecioDolares.toFixed(2);
    fila.querySelector('.preciod1').value = PrecioDolaresHoy.toFixed(2);
    fila.querySelector('.gananciaD').value = total.toFixed(4);
    fila.querySelector('.gananciaBs').value = total2.toFixed(4);
    fila.querySelector('.porcentajeCV').value = PorcentajeCompraVenta.toFixed(2);
    fila.querySelector('.ValorActualD').value = PorcentajeValorActualDolar.toFixed(4);
    fila.querySelector('.porcentajedevaluacion').value = PorcentajeDevaluacion.toFixed(2);
    

    calcularTotalGeneral();
}