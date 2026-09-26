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

const SeleccionProducto = document.getElementById('precio-producto');

function multiplicacion(){
   // let select = document.getElementById('select-producto');
    //let cantidadSeleccionada = parseFloat(select.value) || 0;
    let valor1 = parseFloat(document.getElementById('precio-producto').value) || 0;
    let valor2 = parseFloat(document.getElementById('cantidad-producto').value) || 0;

    let subtotal = valor1 * valor2;
    let descuentoproducto = parseFloat(document.getElementById('descuento').value) || 0;

    let montodescuento = subtotal * (descuentoproducto/100 );
    let Total = subtotal - montodescuento;


    document.getElementById('resultado-multiplicacion').value = subtotal;
    document.getElementById('Totalfin').value = Total.toFixed(3);
}

//Banco Central de Venezuela

async function obtenerTasaBCV() {
    try {
        // Petición a una API pública que rastrea el BCV en formato JSON
        let respuesta = await fetch('https://rates.dolarvzla.com/bcv/current.json');
        let datos = await respuesta.json();

        // Extraemos la tasa del dólar oficial
        let tasaOficial = datos.current.usd;

        // Asignamos el valor al input que tiene id="tasaBcv"
        document.getElementById('tasaBcvDolar').value = tasaOficial.toFixed(4);

        // Opcional: si ya tienes una función para calcular totales, puedes llamarla aquí
        // calcularTotal(); 

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

        // Asignamos el valor al input que tiene id="tasaBcv"
        document.getElementById('tasaBcvEuro').value = tasaEuro.toFixed(4);

        // Opcional: Si tienes una función de cálculo, puedes llamarla aquí para actualizar los totales
        // calcularTotal();

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