import sys
import re
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QGroupBox, QFormLayout,
    QMessageBox, QAbstractItemView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class CotizacionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Cotizaciones - Velazcres")
        self.setGeometry(100, 100, 1100, 700)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # ===== Encabezado =====
        header = QLabel("Velazcres - Sistema de Cotizaciones")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("background-color: #343a40; color: white; padding: 10px;")
        main_layout.addWidget(header)

        # ===== Formularios (Cliente y Cotización) =====
        forms_layout = QHBoxLayout()

        # --- Formulario Cliente ---
        cliente_group = QGroupBox("Información del Cliente")
        cliente_form = QFormLayout()

        self.nombre_cliente = QLineEdit()
        self.nombre_cliente.setPlaceholderText("Nombre Apellido")
        cliente_form.addRow("Nombre Cliente:", self.nombre_cliente)

        self.rif_cliente = QLineEdit()
        self.rif_cliente.setPlaceholderText("11.XXX.XXX-X")
        self.rif_cliente.setMaxLength(12)
        cliente_form.addRow("RIF Fiscal:", self.rif_cliente)

        self.direccion_cliente = QLineEdit()
        self.direccion_cliente.setPlaceholderText("Estado, Municipio, Localidad, Avenida")
        cliente_form.addRow("Dirección:", self.direccion_cliente)

        self.web_cliente = QLineEdit()
        self.web_cliente.setPlaceholderText("www.ejemplo.com")
        cliente_form.addRow("Web:", self.web_cliente)

        self.email_cliente = QLineEdit()
        self.email_cliente.setPlaceholderText("ejemplo@email.com")
        cliente_form.addRow("Email:", self.email_cliente)

        self.telefono_cliente = QLineEdit()
        self.telefono_cliente.setPlaceholderText("0414 XXX XX XX")
        self.telefono_cliente.setMaxLength(11)
        cliente_form.addRow("Teléfono:", self.telefono_cliente)

        cliente_group.setLayout(cliente_form)
        forms_layout.addWidget(cliente_group, 1)

        # --- Formulario Cotización ---
        cotizacion_group = QGroupBox("Información de Cotización")
        cotizacion_form = QFormLayout()

        self.id_cotizacion = QLineEdit()
        self.id_cotizacion.setPlaceholderText("000001")
        cotizacion_form.addRow("ID Cotización:", self.id_cotizacion)

        self.tipo_moneda = QComboBox()
        self.tipo_moneda.addItems(["Bolívares Bs.", "Dólares $.", "Euros €."])
        cotizacion_form.addRow("Tipo de Moneda:", self.tipo_moneda)

        self.forma_pago = QComboBox()
        self.forma_pago.addItems(["Transferencia Bancaria", "Efectivo", "Pago Móvil"])
        cotizacion_form.addRow("Forma de Pago:", self.forma_pago)

        cotizacion_group.setLayout(cotizacion_form)
        forms_layout.addWidget(cotizacion_group, 1)

        main_layout.addLayout(forms_layout)

        # ===== Tabla de Productos =====
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "Items", "Cantidad", "Precio", "Subtotal", "Descuento", "Total"
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.tabla.setRowCount(1)

        # Fila inicial
        self.agregar_fila_producto(0)

        main_layout.addWidget(self.tabla)

        # Botones para agregar/eliminar filas
        botones_layout = QHBoxLayout()
        btn_agregar = QPushButton("+ Agregar Producto")
        btn_agregar.clicked.connect(self.agregar_fila)
        btn_eliminar = QPushButton("- Eliminar Última Fila")
        btn_eliminar.clicked.connect(self.eliminar_fila)
        botones_layout.addWidget(btn_agregar)
        botones_layout.addWidget(btn_eliminar)
        main_layout.addLayout(botones_layout)

        # ===== Tasas BCV =====
        tasas_layout = QHBoxLayout()

        tasas_layout.addWidget(QLabel("Tasa BCV (Dólar):"))
        self.tasa_bcv_dolar = QLineEdit()
        self.tasa_bcv_dolar.setReadOnly(True)
        self.tasa_bcv_dolar.setPlaceholderText("Buscando tasa...")
        tasas_layout.addWidget(self.tasa_bcv_dolar)

        tasas_layout.addWidget(QLabel("Tasa BCV (Euro):"))
        self.tasa_bcv_euro = QLineEdit()
        self.tasa_bcv_euro.setReadOnly(True)
        self.tasa_bcv_euro.setPlaceholderText("Buscando tasa...")
        tasas_layout.addWidget(self.tasa_bcv_euro)

        main_layout.addLayout(tasas_layout)

        # ===== Botón Guardar =====
        btn_guardar = QPushButton("Guardar Cotización")
        btn_guardar.setStyleSheet("background-color: #28a745; color: white; padding: 8px; font-weight: bold;")
        btn_guardar.clicked.connect(self.guardar_cotizacion)
        main_layout.addWidget(btn_guardar)

    def agregar_fila(self):
        row = self.tabla.rowCount()
        self.tabla.insertRow(row)
        self.agregar_fila_producto(row)

    def eliminar_fila(self):
        if self.tabla.rowCount() > 1:
            self.tabla.removeRow(self.tabla.rowCount() - 1)

    def agregar_fila_producto(self, row):
        # Columna 0: ComboBox de productos
        combo = QComboBox()
        combo.addItem("Selecciona un producto", 0)
        combo.addItem("Producto 1", 1)
        combo.addItem("Producto 2", 2)
        combo.addItem("Producto 3", 3)
        combo.addItem("Producto 4", 4)
        combo.addItem("Producto 5", 5)
        combo.addItem("Producto 6", 6)
        self.tabla.setCellWidget(row, 0, combo)

        # Columna 1: Cantidad
        cantidad = QLineEdit()
        cantidad.setPlaceholderText("1")
        cantidad.textChanged.connect(lambda _, r=row: self.calcular_fila(r))
        self.tabla.setCellWidget(row, 1, cantidad)

        # Columna 2: Precio
        precio = QLineEdit()
        precio.setPlaceholderText("1.000")
        precio.textChanged.connect(lambda _, r=row: self.calcular_fila(r))
        self.tabla.setCellWidget(row, 2, precio)

        # Columna 3: Subtotal (readonly)
        subtotal = QLineEdit()
        subtotal.setReadOnly(True)
        subtotal.setPlaceholderText("0.00")
        self.tabla.setCellWidget(row, 3, subtotal)

        # Columna 4: Descuento
        descuento = QLineEdit()
        descuento.setPlaceholderText("5%")
        descuento.textChanged.connect(lambda _, r=row: self.calcular_fila(r))
        self.tabla.setCellWidget(row, 4, descuento)

        # Columna 5: Total (readonly)
        total = QLineEdit()
        total.setReadOnly(True)
        total.setPlaceholderText("0.00")
        self.tabla.setCellWidget(row, 5, total)

    def parse_number(self, text):
        """Convierte texto a número, manejando formatos con puntos y comas."""
        if not text:
            return 0.0
        # Eliminar símbolos de moneda y espacios
        text = re.sub(r'[^\d.,-]', '', text)
        # Si tiene coma como decimal (formato europeo)
        if ',' in text and '.' in text:
            text = text.replace('.', '').replace(',', '.')
        elif ',' in text:
            text = text.replace(',', '.')
        try:
            return float(text)
        except ValueError:
            return 0.0

    def calcular_fila(self, row):
        try:
            cantidad_widget = self.tabla.cellWidget(row, 1)
            precio_widget = self.tabla.cellWidget(row, 2)
            descuento_widget = self.tabla.cellWidget(row, 4)
            subtotal_widget = self.tabla.cellWidget(row, 3)
            total_widget = self.tabla.cellWidget(row, 5)

            cantidad = self.parse_number(cantidad_widget.text()) if cantidad_widget else 0
            precio = self.parse_number(precio_widget.text()) if precio_widget else 0
            descuento_text = descuento_widget.text() if descuento_widget else "0"

            # Parsear descuento (puede ser "5" o "5%")
            descuento = self.parse_number(descuento_text.replace('%', ''))

            subtotal = cantidad * precio
            total = subtotal - (subtotal * descuento / 100)

            if subtotal_widget:
                subtotal_widget.setText(f"{subtotal:,.2f}")
            if total_widget:
                total_widget.setText(f"{total:,.2f}")
        except Exception as e:
            print(f"Error al calcular fila {row}: {e}")

    def guardar_cotizacion(self):
        # Validaciones básicas
        if not self.nombre_cliente.text().strip():
            QMessageBox.warning(self, "Validación", "Ingrese el nombre del cliente.")
            return

        # Recolectar datos
        datos = {
            "cliente": {
                "nombre": self.nombre_cliente.text(),
                "rif": self.rif_cliente.text(),
                "direccion": self.direccion_cliente.text(),
                "web": self.web_cliente.text(),
                "email": self.email_cliente.text(),
                "telefono": self.telefono_cliente.text(),
            },
            "cotizacion": {
                "id": self.id_cotizacion.text(),
                "moneda": self.tipo_moneda.currentText(),
                "forma_pago": self.forma_pago.currentText(),
            },
            "productos": []
        }

        for row in range(self.tabla.rowCount()):
            combo = self.tabla.cellWidget(row, 0)
            cantidad = self.tabla.cellWidget(row, 1)
            precio = self.tabla.cellWidget(row, 2)
            subtotal = self.tabla.cellWidget(row, 3)
            descuento = self.tabla.cellWidget(row, 4)
            total = self.tabla.cellWidget(row, 5)

            if combo and combo.currentIndex() > 0:
                datos["productos"].append({
                    "producto": combo.currentText(),
                    "cantidad": cantidad.text() if cantidad else "",
                    "precio": precio.text() if precio else "",
                    "subtotal": subtotal.text() if subtotal else "",
                    "descuento": descuento.text() if descuento else "",
                    "total": total.text() if total else "",
                })

        # Aquí podrías guardar en BD, JSON, etc.
        QMessageBox.information(
            self, "Cotización Guardada",
            f"Cotización guardada exitosamente.\n\n"
            f"Cliente: {datos['cliente']['nombre']}\n"
            f"Productos: {len(datos['productos'])}\n"
            f"Moneda: {datos['cotizacion']['moneda']}"
        )
        print(datos)  # Para debug


def main():
    app = QApplication(sys.argv)
    ventana = CotizacionApp()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()