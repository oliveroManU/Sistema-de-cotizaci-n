const inputnombrecliente = document.getElementById('nombre-cliente');
inputnombrecliente.addEventListener('input', function() {
    this.value = this.value.replace (/[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]/g, '');  
});



const RifFiscalCliente = document.getElementById('RIF');
RifFiscalCliente.addEventListener('input', function() {
    this.value = this.value.replace (/[^0-9]/g, '');
});

RifFiscalCliente.addEventListener('input', function (e) {
    // 1. Limpia todo lo que no sea número (reemplaza tus dos líneas de limpieza anteriores)
    let valorLimpioRif = e.target.value.replace(/\D/g, '');
    
    // 2. Agrupa de 4 en 4 y une con guiones
    let valorFormatearRif = valorLimpioRif.match(/.{1,8}/g)?.join('-') || '';
    
    // 3. Muestra el resultado en el input
    e.target.value = valorFormatearRif;
});

const TelefonoCliente = document.getElementById('telefono');
TelefonoCliente.addEventListener('input', function() {
    this.value = this.value.replace (/[^0-9]/g, '');

});

const email = document.getElementById('email');

function validarCorreo(val_email) {
  // 1. Verificar longitud mínima y máxima total (ej. mínimo 6: a@b.co, máximo 254)
    if (val_email.length < 6 || val_email.length > 254) {
        return false; 
  }
    const emailregex = /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
    if (!emailregex.test(val_email)){
        alert('Correo no valido')
    }

    const letras = val_email.split('@');
    if (letras[0].length > 48) {
        return false;
    }

    return true;
}

email.addEventListener('blur', function() {
    if (!validarCorreo(this.value.trim())) {
        alert('Correo no valido')
    }
})

const Descripcion = document.getElementById('descripcion')
if (Descripcion.length > 240) {
    alert('Mucho texto')
}

// GESTIÓN DE FILAS DE PRODUCTOS

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
    // 4. Tasa de pago (Bs por USD)
    const tasaEl = document.getElementById('tasapagohoy');
    const tasapago = parseFloat(tasaEl?.value) || 0;
    const subtotald = tasapago !== 0 ? subtotal / tasapago : 0;

    const subtotald1 = document.getElementById('total-generald');
    if (subtotald1) {
        subtotald1.value = subtotald.toFixed(2);
    }

    // 5. Descuento del panel (aplica sobre el subtotal)
    const inputPorDescuento = document.getElementById('pordescuentopanel');
    const PDescuentoPanel = parseFloat(inputPorDescuento?.value) || 0;
    const PorDescuento = subtotal * (PDescuentoPanel / 100);

   // 6. Precio con descuento (Bs)
    const PrecioMasDescuentoPanel = subtotal - PorDescuento;

    const subtotal2El = document.getElementById('descuentobs-panel');
    if (subtotal2El) {
        subtotal2El.value = PrecioMasDescuentoPanel.toFixed(2);
    }

    // 7. Precio con descuento en USD
    const PrecioMasDescuentoDolarPanel = tasapago !== 0 ? PrecioMasDescuentoPanel / tasapago : 0;

    const inputDescuentoDPanel = document.getElementById('descuentod-panel');
    if (inputDescuentoDPanel) {
        inputDescuentoDPanel.value = PrecioMasDescuentoDolarPanel.toFixed(2);
    }

    // 8. IVA sobre el precio con descuento (Bs)
    const PorcentajeIVA = 16;
    const MontoIVA = PrecioMasDescuentoPanel * (PorcentajeIVA / 100);
    const MontoConIVA = PrecioMasDescuentoPanel + MontoIVA;

    const inputMontoIvaBn = document.getElementById('monto-iva-bn');
    if (inputMontoIvaBn) {
        inputMontoIvaBn.value = MontoConIVA.toFixed(2);
    }

}
  
function validarFormulario() {
    const camposObligatorios = [
        document.getElementById('nombre-cliente'),
        document.getElementById('RIF'),
        document.getElementById('direccion-cliente'),
        document.getElementById('telefono'),
        document.getElementById('empresa'),
        document.getElementById('email'),
    ];
    const errores = [];

    // for...of so we can `break`/`return` cleanly if needed
    for (const campo of camposObligatorios) {
        if (!campo) {
            console.warn('⚠️ Selector no encontró el elemento. Revisa los IDs en el HTML.');
            continue;
        }
        campo.classList.remove('error');

        if (campo.value.trim() === '') {
            campo.classList.add('error');
            errores.push(campo.placeholder || campo.name || 'campo');
        }
    }
    // ← alerta DESPUÉS del loop, no dentro
    if (errores.length > 0) {
        alert('Faltan datos en: ' + errores.join(', '));
        return false;
    }
    return true;
}

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

// Ejecutar la función automáticamente en cuanto cargue la página
window.onload = function() {
    obtenerTasaBCV();
    obtenerTasaBCVEuro();
};

const EditarPrecio = document.getElementById('PRECIO');
EditarPrecio.addEventListener('input', function() {
   this.value = this.value.match(/[+-]?(?:\d+\.\d+|\d+\.|\.\d+|\d+)(?:[eE][+-]?\d+)?/)?.[0] || '';
});

// Reloj

