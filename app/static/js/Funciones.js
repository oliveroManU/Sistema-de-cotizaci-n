const inputnombrecliente = document.getElementById('nombre-cliente');

inputnombrecliente.addEventListener('input', function() {

    // Acepta solo letras
    this.value = this.value.replace (/[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]/g, '');  

});

const RifFiscalCliente = document.getElementById('riff-cliente');

RifFiscalCliente.addEventListener('input', function() {

    this.value = this.value.replace (/[^0-9]/g, '');

});


const TelefonoCliente = document.getElementById('Telefono-client');

TelefonoCliente.addEventListener('input', function() {

    this.value = this.value.replace (/[^0-9]/g, '');

});

// ===============================
// GESTIÓN DE FILAS DE PRODUCTOS
// ===============================


function eliminarFila(boton) {
    const fila = boton.closest('tr');
    const cuerpoTabla = document.getElementById('cuerpo-tabla');
    
    if (cuerpoTabla.rows.length > 1) {
        fila.remove();
    } else {
        fila.querySelectorAll('input').forEach(input => {
            input.value = '';
        });
        fila.querySelector('select').selectedIndex = 0;
    }
    
    calcularTotalGeneral();
}

function multiplicacion(elemento) {
    const fila = elemento.closest('tr');
    
    const ValorPorUnidad = parseFloat(fila.querySelector('.precioporunidad').value) || 0;
    const CantidadProducto = parseFloat(fila.querySelector('.cantidad-producto').value) || 0;
    // const TasaPagoProducto = parseFloat(fila.querySelector('.tasapago').value) || 0;
    const TasaPagoProductoHoy = parseFloat(fila.querySelector('.tasapagohoy').value) || 0;
    const PorcentajeDeGanancia = parseFloat(fila.querySelector('.porcentajeCV').value) || 0;

    const PrecioProducto = CantidadProducto !== 0 ? ValorPorUnidad * CantidadProducto : 0;
    fila.querySelector('.precio-producto').value = PrecioProducto.toFixed(2);

     if (elemento.classList.contains('porcentajeCV')) {
        const nuevoPrecioVenta = PrecioProducto * (1 + PorcentajeDeGanancia / 100);
        fila.querySelector('.precio-venta').value = nuevoPrecioVenta.toFixed(2);

    }

    const PrecioVenta = parseFloat(fila.querySelector('.precio-venta').value) || 0;

    const PorcentajeValorActualDolar = TasaPagoProductoHoy !== 0 ? ((PrecioVenta - PrecioProducto)/(TasaPagoProductoHoy)) : 0;
    fila.querySelector('.ValorActualD').value = PorcentajeValorActualDolar.toFixed(4)

    // const PrecioDolaresHoy = TasaPagoProductoHoy !== 0 ? (PrecioProducto  / TasaPagoProductoHoy) : 0;
    // fila.querySelector('.preciod1').value = PrecioDolaresHoy.toFixed(4)

    // const gananciabs = PrecioVenta - PrecioProducto;  
    // fila.querySelector('.gananciaBs').value = gananciabs.toFixed(4);

    

    const GananciaSobreCosto = PrecioProducto * (PorcentajeDeGanancia / 100);
    fila.querySelector('.gananciasobrecosto').value = GananciaSobreCosto.toFixed(4); 

    const MargendeGanancia = PrecioVenta !== 0 ? ((PrecioVenta + PrecioProducto) / PrecioVenta) * 100: 0;
    fila.querySelector('.margen-ganancia').value = MargendeGanancia.toFixed(4);

    const PDescuento = parseFloat(fila.querySelector('.descuento').value) || 0;
    
    if (elemento.classList.contains('descuento')) {
        const PorDescuento = PrecioVenta * (PDescuento / 100);
        fila.querySelector('.pdescuento').value = PorDescuento.toFixed(2);

    }

    const PorcentajeDescuento = parseFloat(fila.querySelector('.pdescuento').value) || 0;

    const PrecioMasDescuento = PrecioVenta - PorcentajeDescuento;
    // const  = PrecioVenta - MontoDescuento;

    // Aquí asignas el valor a tus inputs (asegúrate de que estos nombres coincidan con tu HTML)
    if (fila.querySelector('.monto-iva')) {
        fila.querySelector('.monto-iva').value = PorcentajeDescuento.toFixed(2);
    }
    if (fila.querySelector('.descuentobs')) {
        fila.querySelector('.descuentobs').value = PrecioMasDescuento.toFixed(2);
    }

    // precio total con IVA incluido en dólares:
    const PrecioMasDescuentoDolar = TasaPagoProductoHoy !== 0 ? (PrecioMasDescuento / TasaPagoProductoHoy) : 0;
    if (fila.querySelector('.descuentod')) {
        fila.querySelector('.descuentod').value = PrecioMasDescuentoDolar.toFixed(2);
    }   

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

// Ponemos 'TasaPagoHoy' entre los paréntesis para recibir el valor de la otra función
function calcularTotalGeneral() {
    const filas = document.querySelectorAll('#cuerpo-tabla tr');
    let totalGeneral = 0;

    // 1. Primero calculamos el total general sumando las filas
    filas.forEach(fila => {
        const totalFila = parseFloat(fila.querySelector('.descuentobs').value) || 0;
        totalGeneral += totalFila;
    });

    const inputTotalGeneral = document.getElementById('total-general');
    if (inputTotalGeneral) {
        inputTotalGeneral.value = totalGeneral.toFixed(2);
    }

    const subtotal = totalGeneral; 
    const PorcentajeIVA = 16;
    const MontoIVA = subtotal * (PorcentajeIVA / 100);
    const MontoConIVA = subtotal + MontoIVA;

    const inputMontoIvaBn = document.getElementById('monto-iva-bn');
    if (inputMontoIvaBn) {
        inputMontoIvaBn.value = MontoConIVA.toFixed(2); 
    }
    
  
}

function pasarvalores() {
    document.getElementById('nombre-cliente-c') = document.getElementById('nombre-cliente')
}
// ===============================
// BANCO CENTRAL DE VENEZUELA
// ===============================

async function obtenerTasaBCV() {
    try {
        // Petición a una API pública que rastrea el BCV en formato JSON
        let respuesta = await fetch('https://rates.dolarvzla.com/bcv/current.json');
        let datos = await respuesta.json();

        // Extraemos la tasa del dólar oficial
        let tasaOficial = datos.current.usd;

        // Asignamos el valor al input que tiene id="tasaBcvDolar"
        document.getElementById('tasaBcvDolar').value = tasaOficial.toFixed(4);

    } catch (error) {
        console.error("No se pudo obtener la tasa del BCV:", error);
        document.getElementById('tasaBcvDolar').placeholder = "Error al cargar";
    }
}

async function obtenerTasaBCVEuro() {
    try {
        // Petición a la API pública que rastrea las tasas del BCV
        let respuesta = await fetch('https://rates.dolarvzla.com/bcv/current.json');
        let datos = await respuesta.json();

        // Extraemos la tasa oficial del Euro (.eur en lugar de .usd)
        let tasaEuro = datos.current.eur;

        // Asignamos el valor al input que tiene id="tasaBcvEuro"
        document.getElementById('tasaBcvEuro').value = tasaEuro.toFixed(4);

    } catch (error) {
        console.error("No se pudo obtener la tasa del Euro:", error);
        document.getElementById('tasaBcvEuro').placeholder = "Error al cargar";
    }
}

// Ejecutar la función automáticamente en cuanto cargue la página
window.onload = function() {
    obtenerTasaBCV();
    obtenerTasaBCVEuro();
};

const EditarPrecio = document.getElementById('PRECIO');

EditarPrecio.addEventListener('input', function() {

   this.value = this.value.match(/[+-]?(?:\d+\.\d+|\d+\.|\.\d+|\d+)(?:[eE][+-]?\d+)?/)?.[0] || '';





});


