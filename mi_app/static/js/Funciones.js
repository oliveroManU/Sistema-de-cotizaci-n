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

function eliminarTodos() {
    const cuerpoTabla = document.getElementById('cuerpo-tabla');
    
    if (confirm('¿Estás seguro de que deseas eliminar todos los productos?')) {
        cuerpoTabla.innerHTML = `
            <tr>
                <th>
                    <select name="producto">
                        <option value="0" disabled selected>Selecciona un producto</option>
                        <option value="1">producto 1</option>
                        <option value="2">producto 2</option>
                        <option value="3">producto 3</option>
                        <option value="4">producto 4</option>
                        <option value="5">producto 5</option>
                        <option value="6">producto 6</option>
                    </select>
                </th>
                <td><input type="text" class="cantidad-producto" placeholder="1" oninput="multiplicacion(this)"></td>
                <td><input type="text" class="precio-producto" placeholder="1.000" oninput="multiplicacion(this)"></td>
                <td><input type="number" class="resultado-multiplicacion" readonly placeholder="0.00"></td>
                <td><input type="text" class="descuento" oninput="multiplicacion(this)" placeholder="5%"></td>
                <td><input type="text" class="total-fin" readonly></td>
                <td>
                    <button type="button" class="btn btn-danger btn-sm" onclick="eliminarFila(this)">Eliminar</button>
                </td>
            </tr>
        `;
        calcularTotalGeneral();
    }
}

function multiplicacion(elemento) {
    const fila = elemento.closest('tr');
    
    const valor1 = parseFloat(fila.querySelector('.precio-producto').value) || 0;
    const valor2 = parseFloat(fila.querySelector('.cantidad-producto').value) || 0;
    const descuentoProducto = parseFloat(fila.querySelector('.descuento').value) || 0;

    const subtotal = valor1 * valor2;
    const montoDescuento = subtotal * (descuentoProducto / 100);
    const total = subtotal - montoDescuento;

    fila.querySelector('.resultado-multiplicacion').value = subtotal.toFixed(2);
    fila.querySelector('.total-fin').value = total.toFixed(2);

    calcularTotalGeneral();
}

function calcularTotalGeneral() {
    const filas = document.querySelectorAll('#cuerpo-tabla tr');
    let totalGeneral = 0;

    filas.forEach(fila => {
        const totalFila = parseFloat(fila.querySelector('.total-fin').value) || 0;
        totalGeneral += totalFila;
    });

    const inputTotalGeneral = document.getElementById('total-general');
    if (inputTotalGeneral) {
        inputTotalGeneral.value = totalGeneral.toFixed(2);
    }
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