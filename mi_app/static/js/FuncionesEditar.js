function multiplicacion(elemento) {
    const fila = elemento.closest('form');
    
    const PrecioProducto = parseFloat(fila.querySelector('.precio-producto').value) || 0;
    const CantidadProducto = parseFloat(fila.querySelector('.cantidad-producto').value) || 0;
    const TasaPagoProducto = parseFloat(fila.querySelector('.tasapago').value) || 0;
    const TasaPagoProductoHoy = parseFloat(fila.querySelector('.tasapagohoy').value) || 0;
    const PrecioVenta = parseFloat(fila.querySelector('.precio-venta').value) || 0;
<<<<<<< HEAD
    const Porcentaje = parseFloat(fila.querySelector('.porcentaje').value) || 0;
=======
    const PorcentajeDeGanancia = parseFloat(fila.querySelector('.porcentajeCV').value) || 0;
     if (elemento.classList.contains('porcentajeCV')) {
        const nuevoPrecioVenta = PrecioProducto * (1 + PorcentajeDeGanancia / 100);
        fila.querySelector('.precio-venta').value = nuevoPrecioVenta.toFixed(2);
    }

    // Ahora sí, leemos el precio de venta (ya actualizado si venía del %)
    const PrecioVenta = parseFloat(fila.querySelector('.precio-venta').value) || 0;

>>>>>>> 12dd4d1fc98b3967652de2714ba3e320f9107df3

    const ValorPorUnidad = CantidadProducto !== 0 ? PrecioProducto / CantidadProducto : 0;
    const PrecioDolares = TasaPagoProducto !== 0 ? (PrecioProducto  / TasaPagoProducto) : 0;
    const PrecioDolaresHoy = TasaPagoProducto !== 0 ? (PrecioProducto  / TasaPagoProductoHoy) : 0;
    const total = TasaPagoProducto !== 0 ? ((PrecioVenta - PrecioProducto)/(TasaPagoProducto)) : 0;
    const total2 = PrecioVenta - PrecioProducto;  
    const PorcentajeValorActualDolar = TasaPagoProducto !== 0 ? ((PrecioVenta - PrecioProducto)/(TasaPagoProductoHoy)) : 0;
    const PorcentajeDevaluacion = ((TasaPagoProductoHoy - TasaPagoProducto)/TasaPagoProducto)*100
    const PorcentajeDeGananciaSobreCosto = (PrecioProducto*(1 + PorcentajeDeGanancia))
    const MargendeGanancia = ((PorcentajeDeGananciaSobreCosto - PrecioProducto)/PorcentajeDeGananciaSobreCosto)*100
    
    // Funciones

    fila.querySelector('.precioporunidad').value = ValorPorUnidad.toFixed(2);
    fila.querySelector('.preciod').value = PrecioDolares.toFixed(2);
    fila.querySelector('.preciod1').value = PrecioDolaresHoy.toFixed(2);
    fila.querySelector('.gananciaD').value = total.toFixed(4);
    fila.querySelector('.gananciaBs').value = total2.toFixed(4);
    fila.querySelector('.ValorActualD').value = PorcentajeValorActualDolar.toFixed(4);
    fila.querySelector('.porcentajedevaluacion').value = PorcentajeDevaluacion.toFixed(2);
<<<<<<< HEAD
=======
    fila.querySelector('.gananciasobrecosto').value = PorcentajeDeGananciaSobreCosto.toFixed(4); 
    fila.querySelector('.margen-ganancia').value = MargendeGanancia.toFixed(4);   
>>>>>>> 12dd4d1fc98b3967652de2714ba3e320f9107df3

    calcularTotalGeneral();
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.precio-producto').forEach(multiplicacion);
});