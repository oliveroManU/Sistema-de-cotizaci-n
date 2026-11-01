# Sistema de cotizaciones - Velazcres C.A.

Aplicación web Flask para apoyar la gestión de productos y cotizaciones.

## Estructura

```text
.
├── app/
│   ├── __init__.py
│   ├── blueprints/
│   │   └── main/             # Rutas actuales de la aplicación
│   ├── templates/            # Plantillas Jinja activas
│   └── static/               # CSS, JavaScript e imágenes
├── docs/                     # Análisis y documentación
├── instance/                 # Base de datos local (no se versiona)
├── legacy/                   # Prototipos y archivos que no usa la app
├── wsgi.py                   # Punto de entrada Flask
└── .gitignore
```

La aplicación principal se ejecuta desde `wsgi.py`. Las rutas de la base de
datos y las imágenes se resuelven desde la aplicación, no desde el directorio
actual de la terminal.

## Ejecución local

Activa el entorno virtual que contiene Flask y las dependencias existentes, y
desde la raíz del proyecto ejecuta:

```powershell
python wsgi.py
```

La aplicación utiliza `instance/Velazcress.db`. Ese archivo contiene datos
locales y está excluido de Git; respáldalo antes de cualquier cambio de esquema.
No mezcles esa base con copias que permanecen dentro de `legacy/`.

## Interfaz

Las plantillas activas comparten `app/templates/base.html`. `theme.css` conserva
el tema Bootstrap suministrado y `brand.css` aplica la identidad visual de
Velazcres (carbón, plata y dorado), con principios de jerarquía, contraste,
espaciado y accesibilidad inspirados en Material Design 3. Estos estilos no
cambian las reglas de cálculo ni la persistencia del sistema.

## Legacy

`legacy/ffgfg/` contiene el prototipo alternativo y sus archivos. Las plantillas
sin uso, una página HTML exportada y archivos auxiliares también se conservaron
bajo `legacy/` como referencia, pero no forman parte del arranque Flask.

## Estado y siguientes pasos

El catálogo de productos está parcialmente implementado; la persistencia de
cotizaciones, usuarios/roles y reportes aún está pendiente. Consulta el
[análisis del estado y la ruta de desarrollo](docs/ANALISIS_ESTADO_Y_RUTA.md).
