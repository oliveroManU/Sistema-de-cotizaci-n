# Análisis del estado del sistema y ruta de desarrollo

## Alcance y fuentes

Este análisis contrasta el código que originalmente estaba en `mi_app/`
(ahora reorganizado bajo `app/`) con:

- `Capitulo1,2,3_Ledezma_Barreto.docx`: propósito, objetivos, alcance y
  planteamiento de la investigación.
- `CapituloIV_Barreto_Ledezma (1).docx`: resultados de las entrevistas y
  necesidades expresadas para el sistema.

El análisis de requisitos se hizo mediante revisión estática del código y los
documentos. Durante la reorganización se verificó el arranque y las vistas
principales con pruebas de humo; aún no existe una suite automatizada ni un
manifiesto de dependencias, por lo que esto no certifica el comportamiento de
extremo a extremo.

## Resumen ejecutivo

El proyecto tiene una base inicial de catálogo de productos: muestra, crea,
edita y elimina productos; procesa imágenes; y contiene cálculos relacionados
con costos, tasas de cambio y ganancias. También hay una pantalla que permite
armar visualmente renglones de cotización y calcular subtotales en el navegador.

Sin embargo, la función central del proyecto —registrar una cotización real,
asociarla a un cliente y conservarla— no está conectada a una operación
persistente del servidor. Los informes, el control de acceso por roles, la
generación y conservación de documentos, y el acceso compartido desde varios
dispositivos tampoco están implementados. Por tanto, el sistema es un prototipo
parcial, no una solución lista para uso operativo.

Se conserva la aplicación web como línea principal bajo `app/`; el prototipo
alternativo se trasladó a `legacy/ffgfg/`, sin mezclar sus bases de datos. El
siguiente hito debe ser completar el flujo de cotización de extremo a extremo
antes de añadir informes o automatizaciones.

## Matriz de requisitos

Estados:

- **Parcial:** hay una parte visible o una implementación limitada, pero no se
  cumple el flujo completo o faltan garantías importantes.
- **Pendiente:** no se encontró evidencia suficiente en la aplicación
  principal.
- **Pendiente de definir:** los documentos expresan la necesidad, pero no
  determinan reglas suficientes para implementarla correctamente.

| Requisito derivado de los documentos | Estado | Evidencia y brecha |
|---|---|---|
| Mantener un catálogo central de productos y consultar sus datos | **Parcial** | Hay consultas y pantallas de listado/mostrador. Los datos se guardan en SQLite; también existen bases distintas y una segunda implementación dentro de `ffgfg/`. |
| Crear, editar y eliminar productos | **Parcial** | Hay rutas Flask para alta, edición y eliminación. Existen dos flujos de edición, con campos y formularios diferentes; conviene consolidarlos y validar los datos en el servidor. |
| Registrar datos de costo, cantidad, precio, moneda, tasa y ganancia | **Parcial** | El formulario de producto contiene varios de estos campos y hay cálculos en JavaScript. No se evidencia una regla única y validada en servidor para los cálculos. |
| Calcular cotizaciones con precio, cantidad, IVA, tasa BCV de la fecha, ganancia y costo de compra | **Parcial** | La pantalla de inicio permite añadir productos y calcular subtotal/descuento/total en el navegador, y hay cálculos de costo y conversión en formularios de producto. No se encontró una cotización persistida ni cálculo completo de IVA y reglas comerciales en el servidor. La tasa y sus datos de vigencia no se guardan como parte de una cotización. |
| Registrar información del cliente ligada a una cotización | **Pendiente** | Hay campos HTML para nombre, RIF, dirección, web, correo y teléfono, pero no se encontró una ruta/tabla que los guarde como cliente o los relacione con una cotización. |
| Guardar, consultar y centralizar el historial de cotizaciones | **Pendiente** | No se encontró una entidad o tabla de cotización ni un historial consultable. Los totales de la pantalla no se envían a una ruta de guardado. |
| Emitir un documento de cotización accesible desde otros dispositivos | **Pendiente** | No se encontró generación de PDF/documento, descarga ni envío de una cotización completa. El formato final tampoco queda especificado en los documentos. |
| Compartir/sincronizar datos entre los dispositivos que usan el sistema | **Pendiente** | Hay archivos SQLite locales; no se encontró un servicio central, despliegue compartido o mecanismo de sincronización. Copiar el archivo de base de datos entre equipos no equivale a sincronización segura. |
| Generar informes mensuales sobre productos más solicitados y picos por fecha | **Pendiente** | No se encontraron consultas, vistas ni rutas de informes. Además, sin cotizaciones guardadas no existe la fuente de datos para calcular esos indicadores. |
| Generar y enviar el informe de forma automática el día 15 y conservarlo | **Pendiente / pendiente de definir** | El capítulo IV lo solicita, pero no hay programador, envío ni almacenamiento. Falta definir el canal de envío, los destinatarios y el periodo exacto que cubre cada informe. |
| Administrar usuarios y permisos mediante roles | **Pendiente** | No se encontró inicio de sesión, modelo de usuario, roles ni autorización en rutas. Es un requisito explícito de las entrevistas y una condición previa al uso de datos reales por varios usuarios. |
| Organizar la interfaz como módulos jerárquicos y usar la paleta de la empresa | **Parcial / pendiente de validar** | Hay navegación básica entre inicio, registro y productos, no una estructura padre/hijo. Se usan estilos Bootstrap y CSS local, pero no hay evidencia suficiente para confirmar que corresponden a la identidad visual de la empresa. |
| Clasificar productos por categorías | **Pendiente** | En el capítulo IV se menciona clasificar categorías; el modelo y los formularios observados contienen marca, pero no un campo o catálogo de categorías. Conviene confirmar si categoría es un requisito de negocio separado de marca. |

### Problemas técnicos que afectan el avance

1. **Ruta de base de datos unificada en la reorganización.** Antes, la ruta de
   alta de productos abría `Velazcress.db` relativa al directorio actual,
   mientras que los otros flujos usaban la base junto al código. Ahora las
   rutas de la aplicación comparten
   `instance/Velazcress.db`; las bases que queden en `legacy/` son copias de
   referencia y no deben mezclarse sin una migración.
2. **Cálculo de edición con error de sintaxis JavaScript.** En
   `app/static/js/FuncionesEditar.js` se declara dos veces `const PrecioVenta`
   en el mismo ámbito. El navegador no puede analizar ese archivo, por lo que
   las funciones de ese script no se ejecutan en la página que lo carga.
3. **La pantalla de cotización es de presentación, no un flujo guardado.** Los
   campos de cliente y cotización de `app/templates/index.html` no forman
   parte de un formulario enviado a una ruta de persistencia. El cálculo
   ejecutado en el navegador no sustituye validación ni cálculo autoritativo en
   el servidor.
4. **Tasas de cambio sin historial asociado.** Se intenta consultar la tasa
   externa desde el servidor y desde JavaScript, con comportamientos distintos.
   No se conserva una tasa fechada en cada operación ni se define una estrategia
   confiable ante indisponibilidad del servicio.
5. **Arranque y dependencias sin documentar.** No se encontró un archivo
   `requirements.txt`/`pyproject.toml`, una guía de arranque ni pruebas. Hay dos
   entornos virtuales locales y una copia alternativa del código, lo que hace
   ambiguo cuál es el entorno correcto.

## Ruta recomendada

### Fase 0 — Estabilizar la base de trabajo

- Mantener `app/` como única línea principal web; dejar `legacy/ffgfg/` como
  prototipo/legado, sin mezclar bases.
- La base de trabajo de la aplicación quedó en `instance/Velazcress.db`;
  respaldarla antes de cambiar el esquema.
- Crear un único entorno reproducible, declarar las dependencias reales,
  documentar el comando de inicio y configurar las rutas de archivos respecto
  a la ubicación de la aplicación, no al directorio actual.
- Centralizar la apertura de la base y comprobar que todas las rutas escriben y
  leen la misma base.
- Añadir una prueba mínima de arranque y pruebas de rutas de lectura/escritura.

**Criterio de salida:** una persona puede instalar y arrancar la app desde una
instrucción documentada, y una operación de producto aparece en el mismo
catálogo desde cualquiera de las vistas.

### Fase 1 — Definir el modelo de negocio y cerrar las reglas de cálculo

Antes de programar cálculos financieros, confirmar con la empresa:

- tasa de IVA aplicable, si puede cambiar y si se introduce manualmente o se
  obtiene de una fuente;
- fórmula de ganancia: porcentaje sobre costo (recargo) o margen sobre precio
  de venta;
- monedas admitidas, redondeo, tasa usada y fecha/hora que deben quedar
  impresas;
- vigencia de una cotización, descuentos, condiciones de pago y datos
  obligatorios del cliente.

Diseñar entidades relacionadas para productos, clientes, cotizaciones y líneas
de cotización. Guardar en cada cotización una instantánea del nombre/precio de
producto y de los parámetros usados (moneda, tasa fechada, impuesto,
descuento), para que un cambio futuro del catálogo no altere cotizaciones
históricas. El servidor debe validar entradas y calcular importes; el navegador
puede ayudar a previsualizarlos, pero no ser la única fuente del total.

**Criterio de salida:** un usuario crea una cotización, la vuelve a abrir y
obtiene exactamente los importes originales aunque cambien posteriormente el
producto o la tasa.

### Fase 2 — Completar el flujo de cotización

- Persistir los datos del cliente y la cabecera de la cotización.
- Persistir sus líneas, cantidades, precios, impuestos, descuentos, moneda,
  totales, fecha y estado.
- Crear el historial con búsqueda por número, cliente y fecha.
- Acordar estados mínimos (por ejemplo, borrador y emitida) antes de añadir
  más estados.
- Probar cálculos con valores normales, límites, entradas inválidas y monedas
  diferentes.

**Criterio de salida:** cotización completa, guardada, recuperable y con
totales reproducibles desde el servidor.

### Fase 3 — Acceso compartido, documentos y permisos

- Definir roles y permisos concretos con la empresa; proteger tanto las vistas
  como cada operación de escritura en el servidor.
- Generar un documento imprimible/descargable con todos los datos aprobados;
  PDF es una opción recomendable, pero el formato debe confirmarse.
- Desplegar una única instancia web accesible desde los equipos autorizados,
  con una base central y respaldos. No sincronizar copias de un archivo SQLite
  entre computadoras.
- SQLite puede mantenerse para un piloto de una sola instancia y baja
  concurrencia. Si varios usuarios escriben concurrentemente o el servicio se
  expone en red con crecimiento previsto, evaluar PostgreSQL antes de ese
  despliegue.

**Criterio de salida:** cada usuario ve solo las funciones permitidas y todos
los dispositivos consultan los mismos registros mediante el servidor.

### Fase 4 — Informes automáticos

- Construir los informes solo después de disponer de cotizaciones y líneas
  históricas confiables.
- Definir qué significa "producto más solicitado" (unidades cotizadas, número
  de cotizaciones u otro indicador) y el rango temporal.
- Generar, guardar y probar el informe del día 15; confirmar zona horaria,
  destinatarios y canal de envío antes de automatizar el envío.
- Registrar errores de generación/envío y permitir volver a generar el informe.

**Criterio de salida:** informe reproducible, almacenado y enviado al destino
aprobado, con evidencia de errores o éxito.

### Fase 5 — Pulir la interfaz y preparar el uso real

- Organizar la navegación por módulos padre/hijo, aplicar la paleta aprobada y
  probar la experiencia en los dispositivos objetivo.
- Reparar y probar los scripts actuales; en particular, corregir el error de
  sintaxis de `FuncionesEditar.js`.
- Añadir pruebas de aceptación basadas en los flujos reales de los usuarios,
  comprobaciones de permisos, copias de seguridad y restauración.
- Hacer un piloto con datos no sensibles, capacitar a los usuarios y validar
  sus resultados antes de migrar la operación diaria.

## Decisiones que conviene cerrar con la empresa

1. ¿Cuál es la tasa de IVA y cómo se aplica a cada cotización?
2. ¿La ganancia es recargo sobre costo o margen sobre venta? ¿Qué usuarios
   pueden modificarla?
3. ¿Qué datos de cliente son obligatorios y el cliente se reutiliza en futuras
   cotizaciones?
4. ¿Qué formato debe entregarse al cliente y cuánto tiempo es válida una
   cotización?
5. ¿Qué roles existen y qué puede ver/crear/editar/eliminar cada uno?
6. ¿El informe del día 15 se envía por correo u otro canal, a quién, y qué
   periodo resume?
7. ¿Desde qué dispositivos/red se utilizará el sistema y dónde se alojará?
8. ¿Las categorías de producto son necesarias además de la marca?

## Organización aplicada en esta entrega

La aplicación Flask quedó en `app/`, con un blueprint principal, plantillas y
archivos estáticos; `wsgi.py` es el punto de entrada. La base de trabajo se
trasladó a `instance/Velazcress.db`; los prototipos, plantillas no usadas y
archivos auxiliares se conservaron en `legacy/`. Las imágenes activas se
mantuvieron en `app/static/img/productos/`. El entorno virtual de la raíz se
conservó; el del prototipo permanece en `legacy/ffgfg/`. La reorganización no
añadió módulos de negocio nuevos ni cambió los flujos existentes
intencionalmente.
