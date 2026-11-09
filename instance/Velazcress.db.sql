BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "productos-vendidos" (
	"id-venta"	INTEGER,
	"nombre"	TEXT,
	"precio"	NUMERIC,
	"cantidad"	INTEGER,
	"moneda"	TEXT,
	"tasapago"	NUMERIC,
	"precioventa"	NUMERIC,
	"ganancia"	NUMERIC,
	PRIMARY KEY("id-venta" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "productos" (
	"id"	INTEGER,
	"nombre"	TEXT,
	"marca"	TEXT,
	"moneda"	TEXT,
	"precio"	NUMERIC,
	"cantidad"	INTEGER,
	"precioporunidad"	NUMERIC,
	"tasapago"	NUMERIC,
	"precioD"	NUMERIC,
	"precio_venta"	NUMERIC,
	"ganancia_estimadaD"	NUMERIC,
	"ganancia_estimadaBs"	NUMERIC,
	"descripcion"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "clientes" (
	"id_cliente"	INTEGER,
	"nombre"	TEXT,
	"RIF"	TEXT,
	"direccion"	TEXT,
	"email"	TEXT,
	"telefono"	TEXT,
	PRIMARY KEY("id_cliente" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "usuarios" (
	"id"	INTEGER,
	"nombre"	TEXT NOT NULL,
	"password_hash"	TEXT NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	"nivel"	TEXT NOT NULL DEFAULT 'operador',
	"activo"	INTEGER DEFAULT 1,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "reg_cotizaciones" (
	"id"	INTEGER,
	"producto_id"	INTEGER NOT NULL,
	"fecha"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"nombre_producto"	TEXT,
	"marca_producto"	TEXT,
	"precio_unitario"	REAL,
	"cantidad"	INTEGER,
	"precio_total"	REAL,
	"tasa_bcv"	REAL,
	"porcentaje_ganancia"	REAL,
	"precio_venta"	REAL,
	"ganancia_bs"	REAL,
	"ganancia_usd"	REAL,
	"ganancia_sobre_costo"	REAL,
	"margen_ganancia"	REAL,
	"monto_iva"	REAL,
	"precio_con_iva"	REAL,
	"monto_iva_usd"	REAL,
	FOREIGN KEY("producto_id") REFERENCES "productos"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "detalle_pedido" (
	"id"	INTEGER,
	"pedido_id"	INTEGER,
	"codigo_producto"	TEXT,
	"cliente_nombre"	TEXT,
	"precio_unitario"	REAL,
	"cantidad"	INTEGER,
	"precio"	REAL,
	"tasa_pago"	REAL,
	"porcentaje_cv"	REAL,
	"precio_venta"	REAL,
	"valor_d"	REAL,
	"ganancia_sobre_costo"	REAL,
	"margen_ganancia"	REAL,
	"descuento"	REAL,
	"pdescuento"	REAL,
	"descuento_bs"	REAL,
	"descuento_d"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("pedido_id") REFERENCES "pedidos"("id")
);
CREATE TABLE IF NOT EXISTS "pedidos" (
	"id"	INTEGER,
	"fecha"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"cliente"	TEXT,
	"tasa"	REAL,
	"subtotal"	REAL,
	"subtotal_d"	REAL,
	"porc_descuento"	REAL,
	"subtotal_descuento"	REAL,
	"total_iva"	REAL,
	"subtotal_descuento_d"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "GLOBAL_HISTORY" (
	"CODIGO"	INTEGER,
	"USER_ACTION"	TEXT NOT NULL,
	"ACTION"	TEXT NOT NULL,
	"DATE_HOUR"	TEXT NOT NULL,
	"OPERATION_DETAILS"	TEXT,
	PRIMARY KEY("CODIGO" AUTOINCREMENT)
);
INSERT INTO "productos" VALUES (1,'Helix','Shell','Bs.',212000,20,10600,875.65,0,237440,28.5978,25440,NULL);
INSERT INTO "productos" VALUES (2,'Aceite_Premiun','Shell','Bs.',20000,5,4000,889.58,0,22400,2.6979,2400,NULL);
INSERT INTO "productos" VALUES (4,'wqqwqwq','qwqwqwq','Bs.',1212212,12,101017.67,897.54,1350.59,0,0,0,NULL);
INSERT INTO "clientes" VALUES (1,'oliver moises','23323232','Miranda, Guarenas','oliver@gmail.com','12121212');
INSERT INTO "usuarios" VALUES (1,'Admin','scrypt:32768:8:1$Aq2TyRMo0mLie6fY$1180fb272d3a3daef7260fd817190563b7a8b309fd958c3e1f2aef57dd7bb8b08692ec620d29724668bd965864f5477578e7f549a6e62111766a969807791f7b','admin@velazcress.com','admin',1);
INSERT INTO "usuarios" VALUES (2,'21212121','scrypt:32768:8:1$eThmJeuaQvDZVEng$d8edecb48364dd21ee539138149fa0cc9f69fde48a86def61de6e5b6d8ab71388c6c895f4d74b9c55bad60ffaf9d502692825f519f9e3504e5ed284dc69e20d1','12121@gasaysa','operador',0);
INSERT INTO "usuarios" VALUES (3,'Oliver_Ledezma','scrypt:32768:8:1$Ovl091JtNKXJx0XY$311bcf313791c1d45bdad2938a342d8b3fecb353e8f4fe5d42e74538aeaffb41e19492d8a170460fb1ddbebffb686b431fc6f972870f6475280d108ec62719b3','oliver@velezcress.com','operador',1);
INSERT INTO "reg_cotizaciones" VALUES (1,1,'2026-10-30 03:45:48',NULL,NULL,10600.0,20,212000.0,889.26,12.0,237440.0,25440.0,28.6081,25440.0,10.7143,37990.4,275430.4,42.72);
INSERT INTO "reg_cotizaciones" VALUES (2,1,'2026-10-30 03:57:31',NULL,NULL,10600.0,20,212000.0,889.26,12.0,237440.0,25440.0,28.6081,25440.0,10.7143,37990.4,275430.4,42.72);
INSERT INTO "reg_cotizaciones" VALUES (3,1,'2026-10-30 04:21:53','Helix','Shell',10600.0,20,212000.0,889.26,12.0,237440.0,25440.0,28.6081,25440.0,10.7143,37990.4,275430.4,42.72);
INSERT INTO "reg_cotizaciones" VALUES (4,1,'2026-10-31 02:31:34','Helix','Shell',10600.0,20,212000.0,889.58,12.0,237440.0,25440.0,28.5978,25440.0,10.7143,37990.4,275430.4,42.71);
INSERT INTO "reg_cotizaciones" VALUES (5,2,'2026-11-02 13:43:11','Aceite_Premiun','Shell',4000.0,5,20000.0,889.58,12.0,22400.0,2400.0,2.6979,2400.0,10.7143,3584.0,25984.0,4.03);
INSERT INTO "detalle_pedido" VALUES (1,15,'1','Cliente Prueba',12121.0,11,133331.0,894.89,11.0,147997.41,16.3891,14666.41,190.0901,1.0,1479.97,146517.44,163.73);
INSERT INTO "detalle_pedido" VALUES (2,16,'2','Cliente Prueba',23323.0,2323,54179329.0,894.89,232.0,179875372.28,140459.7697,125696043.28,130.1205,2323.0,4178504898.06,-3998629525.78,-4468291.66);
INSERT INTO "detalle_pedido" VALUES (3,16,'1','Cliente Prueba',23232.0,2323,53967936.0,0.0,23.0,66380561.28,0.0,12412625.28,181.3008,22.0,14603723.48,51776837.8,0.0);
INSERT INTO "detalle_pedido" VALUES (4,17,'1','Cliente Prueba',12121.0,1221,14799741.0,896.12,12.0,16575709.92,1981.8427,1775968.92,189.2857,12.0,1989085.19,14586624.73,16277.54);
INSERT INTO "detalle_pedido" VALUES (5,19,'1','ewewewewe',121.0,12,1452.0,896.12,12.0,1626.24,0.1944,174.24,189.2857,12.0,195.15,1431.09,1.6);
INSERT INTO "detalle_pedido" VALUES (6,20,'1','ewewewew',12000.0,10,120000.0,896.12,12.0,134400.0,16.0693,14400.0,189.2857,7.0,9408.0,124992.0,139.48);
INSERT INTO "detalle_pedido" VALUES (7,21,'1','dsssssssss',12212.0,12,146544.0,896.12,12.0,164129.28,19.6238,17585.28,189.2857,12.0,19695.51,144433.77,161.18);
INSERT INTO "detalle_pedido" VALUES (8,21,'1','dsssssssss',12.0,12,144.0,896.12,12.0,161.28,0.0193,17.28,189.2857,12.0,19.35,141.93,0.16);
INSERT INTO "detalle_pedido" VALUES (9,22,'1','',12.0,22,264.0,897.54,12.0,295.68,0.0353,31.68,189.2857,12.0,35.48,260.2,0.29);
INSERT INTO "detalle_pedido" VALUES (10,24,'2','',12.0,12,144.0,897.54,12.0,161.28,0.0193,17.28,189.2857,12.0,19.35,141.93,0.16);
INSERT INTO "detalle_pedido" VALUES (11,24,'2','',12.0,12,144.0,897.54,12.0,161.28,0.0193,17.28,189.2857,112.0,180.63,-19.35,-0.02);
INSERT INTO "detalle_pedido" VALUES (12,25,'1','ddddd',12.0,12,144.0,897.54,12.0,161.28,0.0193,17.28,189.2857,12.0,19.35,141.93,0.16);
INSERT INTO "pedidos" VALUES (1,'2026-11-05 04:15:58',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pedidos" VALUES (2,'2026-11-05 04:18:53',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pedidos" VALUES (3,'2026-11-05 04:30:22',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pedidos" VALUES (4,'2026-11-05 04:32:56',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pedidos" VALUES (5,'2026-11-05 04:37:13',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pedidos" VALUES (6,'2026-11-05 04:40:44',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pedidos" VALUES (7,'2026-11-05 04:42:25',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pedidos" VALUES (8,'2026-11-05 04:58:07',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pedidos" VALUES (9,'2026-11-05 05:02:41',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pedidos" VALUES (10,'2026-11-05 05:05:35',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pedidos" VALUES (11,'2026-11-05 05:08:05',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pedidos" VALUES (12,'2026-11-05 05:11:04',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pedidos" VALUES (13,'2026-11-05 05:17:04',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pedidos" VALUES (14,'2026-11-05 05:22:11',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pedidos" VALUES (15,'2026-11-05 05:28:12',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pedidos" VALUES (16,'2026-11-05 05:49:09',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "pedidos" VALUES (17,'2026-11-06 03:17:32','Cliente Prueba',0.0,14586624.73,NULL,NULL,NULL,16920484.69,NULL);
INSERT INTO "pedidos" VALUES (18,'2026-11-06 03:25:04','desdsds',896.12,14334.57,NULL,NULL,NULL,16628.1,NULL);
INSERT INTO "pedidos" VALUES (19,'2026-11-06 03:30:29','ewewewewe',896.12,1431.09,NULL,NULL,NULL,1660.06,NULL);
INSERT INTO "pedidos" VALUES (20,'2026-11-06 04:49:07','ewewewew',896.12,124992.0,NULL,NULL,NULL,144990.72,NULL);
INSERT INTO "pedidos" VALUES (21,'2026-11-06 05:02:14','dsssssssss',896.12,144575.7,NULL,NULL,NULL,167707.81,NULL);
INSERT INTO "pedidos" VALUES (22,'2026-11-07 01:52:16','',0.0,260.2,NULL,NULL,NULL,301.83,NULL);
INSERT INTO "pedidos" VALUES (23,'2026-11-07 01:52:39','eqeqeqeqe',897.54,-375.78,NULL,NULL,NULL,-435.9,NULL);
INSERT INTO "pedidos" VALUES (24,'2026-11-07 01:53:33','',0.0,122.58,NULL,NULL,NULL,142.19,NULL);
INSERT INTO "pedidos" VALUES (25,'2026-11-07 01:53:57','ddddd',897.54,141.93,NULL,NULL,NULL,164.64,NULL);
INSERT INTO "GLOBAL_HISTORY" VALUES (1,'Admin (ID: 1)','Crear usuario','2026-11-06T22:22:55-04:00','{"email": "12121@gasaysa", "nivel": "operador", "nombre": "21212121", "usuario_id": 2}');
INSERT INTO "GLOBAL_HISTORY" VALUES (2,'Admin (ID: 1)','Desactivar usuario','2026-11-06T22:23:01-04:00','{"email": "12121@gasaysa", "nombre": "21212121", "usuario_id": 2}');
INSERT INTO "GLOBAL_HISTORY" VALUES (3,'Admin (ID: 1)','Crear usuario','2026-11-06T22:23:34-04:00','{"email": "oliver@velezcress.com", "nivel": "operador", "nombre": "Oliver_Ledezma", "usuario_id": 3}');
INSERT INTO "GLOBAL_HISTORY" VALUES (4,'Oliver_Ledezma (ID: 3)','Crear producto','2026-11-06T22:24:05-04:00','{"cantidad": 1, "nombre": "", "precio": 0.0, "precio_venta": 0.0, "producto_id": 3}');
INSERT INTO "GLOBAL_HISTORY" VALUES (5,'Oliver_Ledezma (ID: 3)','Eliminar producto','2026-11-06T22:24:35-04:00','{"datos": {"cantidad": 1, "descripcion": null, "ganancia_estimadaBs": 0, "ganancia_estimadaD": 0, "id": 3, "marca": "", "moneda": "Bs.", "nombre": "", "precio": 0, "precioD": 0, "precio_venta": 0, "precioporunidad": 0, "tasapago": 897.54}, "producto_id": 3}');
INSERT INTO "GLOBAL_HISTORY" VALUES (6,'Oliver_Ledezma (ID: 3)','Crear producto','2026-11-06T22:36:06-04:00','{"cantidad": 12, "nombre": "wqqwqwq", "precio": 1212212.0, "precio_venta": 0.0, "producto_id": 4}');
COMMIT;
