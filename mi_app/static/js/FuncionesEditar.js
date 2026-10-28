function multiplicacion(elemento) {
    const fila = elemento.closest('form');
    
    const PrecioProducto = parseFloat(fila.querySelector('.precio-producto').value) || 0;
    const CantidadProducto = parseFloat(fila.querySelector('.cantidad-producto').value) || 0;
    // const TasaPagoProducto = parseFloat(fila.querySelector('.tasapago').value) || 0;
    const TasaPagoProductoHoy = parseFloat(fila.querySelector('.tasapagohoy').value) || 0;
    const PorcentajeDeGanancia = parseFloat(fila.querySelector('.porcentajeCV').value) || 0;

    const ValorPorUnidad = CantidadProducto !== 0 ? PrecioProducto / CantidadProducto : 0;
    fila.querySelector('.precioporunidad').value = ValorPorUnidad.toFixed(2);

     if (elemento.classList.contains('porcentajeCV')) {
        const nuevoPrecioVenta = PrecioProducto * (1 + PorcentajeDeGanancia / 100);
        fila.querySelector('.precio-venta').value = nuevoPrecioVenta.toFixed(2);

        

        

    }

    const PrecioVenta = parseFloat(fila.querySelector('.precio-venta').value) || 0;

    const PorcentajeValorActualDolar = TasaPagoProductoHoy !== 0 ? ((PrecioVenta - PrecioProducto)/(TasaPagoProductoHoy)) : 0;
    fila.querySelector('.ValorActualD').value = PorcentajeValorActualDolar.toFixed(4)

    // const PrecioDolaresHoy = TasaPagoProductoHoy !== 0 ? (PrecioProducto  / TasaPagoProductoHoy) : 0;
    // fila.querySelector('.preciod1').value = PrecioDolaresHoy.toFixed(4)

    const gananciabs = PrecioVenta - PrecioProducto;  
    fila.querySelector('.gananciaBs').value = gananciabs.toFixed(4);

    const GananciaSobreCosto = PrecioProducto * (PorcentajeDeGanancia / 100);
    fila.querySelector('.gananciasobrecosto').value = GananciaSobreCosto.toFixed(4); 

    const MargendeGanancia = PrecioVenta !== 0 ? ((PrecioVenta - PrecioProducto) / PrecioVenta) * 100: 0;
    fila.querySelector('.margen-ganancia').value = MargendeGanancia.toFixed(4);

        

    /// const PrecioDolares = TasaPagoProducto !== 0 ? (PrecioProducto  / TasaPagoProducto) : 0;
    /// const total = TasaPagoProducto !== 0 ? ((PrecioVenta - PrecioProducto)/(TasaPagoProducto)) : 0;
    /// const PorcentajeDevaluacion = ((TasaPagoProductoHoy - TasaPagoProducto)/TasaPagoProducto)*100

   
    /// fila.querySelector('.preciod').value = PrecioDolares.toFixed(2);
    /// fila.querySelector('.gananciaD').value = total.toFixed(4);
    /// fila.querySelector('.porcentajedevaluacion').value = PorcentajeDevaluacion.toFixed(2);
       

    calcularTotalGeneral();
}

document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('.precio-producto, .cantidad-producto, .tasapagohoy, .porcentajeCV, .precio-venta');
    inputs.forEach(input => {
        input.addEventListener('input', () => multiplicacion(input));
        multiplicacion(input); // Esto llena las cajas vacías al cargar la página
    });
});