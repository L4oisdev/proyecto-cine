import sqlite3 as sql 

class Database:

    # Crear base de datos
    def createDB(self):

        try:
            conexion = sql.connect("cine.db")
            conexion.commit()
            conexion.close()

            print("Base de datos creada con exito")

        except sql.Error as error:
            print("Error al crear la base de datos {}".format(error))


    def createTable(self):

        try:
            conexion = sql.connect("cine.db")

            cursor = conexion.cursor()

            # Crear tabla administradores
            cursor.execute(
                """ CREATE TABLE IF NOT EXISTS administradores(
                        id_admin INTEGER NOT NULL PRIMARY KEY,
                        user_admn TEXT NOT NULL,
                        pass_admn TEXT NOT NULL 
                    )
                """
            )

            # Crear tabla clientes
            cursor.execute(
                """ CREATE TABLE IF NOT EXISTS clientes(
                        id_cliente INTEGER NOT NULL PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        apellido TEXT NOT NULL,
                        email TEXT NOT NULL,
                        pass_cliente TEXT NOT NULL
                    )
                """
            )

            # Crear tabla salas
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS salas(
                        id_sala INTEGER NOT NULL PRIMARY KEY,
                        num_filas INTEGER NOT NULL,
                        asientos_fila INTEGER NOT NULL,
                        capacidad INTEGER NOT NULL
                        )
                """
                )
            
            # Crear tabla peliculas
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS peliculas(
                        id_pelicula INTEGER PRIMARY KEY AUTOINCREMENT,
                        titulo TEXT NOT NULL,
                        director TEXT NOT NULL,
                        genero TEXT NOT NULL,
                        duracion INTEGER NOT NULL,
                        sinopsis TEXT NOT NULL 
                        )
                """
            )
            
            # Crear tabla asientos
            cursor.execute(
                """ CREATE TABLE IF NOT EXISTS asientos(
                        id_asiento INTEGER NOT NULL PRIMARY KEY,
                        id_sala INTEGER NOT NULL,
                        fila_as INTEGER NOT NULL,
                        FOREIGN KEY (id_sala) REFERENCES salas(id_sala)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE
                    )
                """
            )
            
            # Crear tabla horarios
            cursor.execute(
                """ CREATE TABLE IF NOT EXISTS horarios(
                        id_horario INTEGER PRIMARY KEY,
                        id_pelicula INTEGER,
                        id_sala INTEGER,
                        fecha DATE,
                        hora TIME,
                        FOREIGN KEY (id_pelicula) REFERENCES Peliculas(id_pelicula),
                        FOREIGN KEY (id_sala) REFERENCES Salas(id_sala)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE
                    )
                """
                )
            
            # Crear tabla boletos
            cursor.execute(
            """ CREATE TABLE IF NOT EXISTS boletos(
                    id_boleto INTEGER PRIMARY KEY,
                    id_horario INTEGER NOT NULL,
                    id_asiento INTEGER NOT NULL,
                    FOREIGN KEY (id_horario) REFERENCES horarios(id_horario),
                    FOREIGN KEY (id_asiento) REFERENCES asientos(id_asiento)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                )
            """
            )

            conexion.commit()
            conexion.close()

            print("Tablas creadas, con exito")

        except sql.Error as error:
            print("Error al crear las Tablas {}".format(error))


    def insertData(self, tabla, datos):

        try:
            conexion = sql.connect("cine.db")
            cursor = conexion.cursor()

            # Consulta con placeholders para evitar inyección SQL
            columnas = ", ".join(datos.keys())
            valores = tuple(datos.values())
            consulta = f"INSERT INTO {tabla} ({columnas}) VALUES ({', '.join(['?'] * len(valores))})"

            # Ejecuta la consulta con los valores
            cursor.execute(consulta, valores)

            conexion.commit()
            conexion.close()

            print(f"Datos insertados en la tabla {tabla}")

        except sql.Error as error:
            print("Error al insertar datos:", error)

    
    def updateData(self, tabla, datos, id_campo, id_valor):

        try:
            conexion = sql.connect("cine.db")
            cursor = conexion.cursor()

            # Consulta con placeholders para evitar inyección SQL
            columnas = ", ".join([f"{k} = ?" for k in datos.keys()])
            condicion = f"{id_campo} = ?"
            valores = tuple(datos.values()) + (id_valor,)
            consulta = f"UPDATE {tabla} SET {columnas} WHERE {condicion}"

            # Ejecuta la consulta con los valores
            cursor.execute(consulta, valores)

            conexion.commit()
            conexion.close()

            print(f"Datos actualizados en la tabla {tabla}")

        except sql.Error as error:
            print("Error al actualizar datos:", error)


    def selectDataById(self, tabla, id_campo, id_valor):
        try:
            conexion = sql.connect("cine.db")
            cursor = conexion.cursor()
            cursor.execute(f"SELECT * FROM {tabla} WHERE {id_campo} = ?", (id_valor,))
            registro = cursor.fetchone()
            conexion.close()
            return registro
        
        except sql.Error as error:
            print("Error al seleccionar datos por ID:", error)


    def getData(self, tabla):

        try:
            conexion = sql.connect("cine.db")
            cursor = conexion.cursor()
            cursor.execute(f"SELECT * FROM {tabla}")
            registros = cursor.fetchall()
            conexion.close()
            return registros
        
        except sql.Error as error:
            print("Error al seleccionar datos:", error)


    def deleteData(self, tabla, id_campo, id_valor):

        try:
            conexion = sql.connect("cine.db")
            cursor = conexion.cursor()

            condicion = f"{id_campo} = ?"
            valores = (id_valor,)
            consulta = f"DELETE FROM {tabla} WHERE {condicion}"

            # Ejecuta la consulta con los valores
            cursor.execute(consulta, valores)

            conexion.commit()
            conexion.close()

            print(f"Datos eliminados de la tabla {tabla}")

        except sql.Error as error:
            print("Error al eliminar datos:", error)

        
    def verificar_credenciales(self, tabla, campo_usuario, campo_contrasena, usuario, contrasena):
        try:
            conexion = sql.connect("cine.db")
            cursor = conexion.cursor()
            query = f"SELECT * FROM {tabla} WHERE {campo_usuario} = ? AND {campo_contrasena} = ?"
            cursor.execute(query, (usuario, contrasena))
            resultado = cursor.fetchone()
            conexion.close()
            return resultado is not None
        
        except sql.Error as error:
            print("Error al verificar credenciales:", error)


                
if __name__ == "__main__":

    base = Database()
    # base.createDB()
    # base.createTable()


    #--------- HORARIOS ---------#
    # conexion = sql.connect("cine.db")
    # cursor = conexion.cursor()

    # datos_horarios = [
    # (1, 1, 3, '18-03-2024', '20:00'),
    # (2, 1, 1, '18-03-2024', '20:30'),
    # (3, 2, 4, '18-03-2024', '19:00'),

    # (4, 2, 5, '18-03-2024', '19:00'),
    # (5, 3, 2, '18-03-2024', '19:00'),
    # (6, 3, 4, '18-03-2024', '21:30'),

    # (7, 4, 2, '18-03-2024', '21:45'),
    # (8, 4, 1, '18-03-2024', '17:30'),
    # (9, 5, 3, '18-03-2024', '17:30'),
    # (10, 5, 5, '18-03-2024', '21:45'),

    # (11, 6, 6, '18-03-2024', '21:45'),
    # (12, 6, 7, '18-03-2024', '18:00'),
    # (13, 7, 6, '18-03-2024', '18:00'),
    # (14, 7, 7, '18-03-2024', '21:45'),
    # ]

    # # Insertar datos en la tabla horarios
    # for horario in datos_horarios:
    #     cursor.execute("INSERT INTO horarios (id_horario, id_pelicula, id_sala, fecha, hora) VALUES (?, ?, ?, ?, ?)", horario)


    # # Guardar los cambios y cerrar la conexión
    # conexion.commit()
    # conexion.close()


    #--------- ASIENTOS ---------#
    # conexion = sql.connect("cine.db")
    # cursor = conexion.cursor()

    # salas_info = {
    #     1: (10, 15), --> sala 1: 10 filas, 15 asientos por fila
    #     2: (8, 12),  --> sala 2: 8 filas, 12 asientos por fila
    #     3: (12, 20), --> sala 3: 12 filas, 20 asientos por fila
    #     4: (9, 18),  --> sala 4: 9 filas, 18 asientos por fila
    #     5: (6, 10),  --> sala 5: 6 filas, 10 asientos por fila
    #     6: (7, 11),  --> sala 6: 7 filas, 11 asientos por fila
    #     7: (11, 16)  --> sala 7: 11 filas, 16 asientos por fila
    # }

    # # Función para generar los asientos para una sala específica
    # def generar_asientos(sala_id, num_filas, num_asientos_por_fila):
    #     asientos = []
    #     filas = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':11,'L':12}
    #     for fila_letra in filas.keys():
    #         fila_num = filas[fila_letra]
    #         for asiento_num in range(1, num_asientos_por_fila + 1):
    #             asientos.append((sala_id, asiento_num, fila_num,))
    #     return asientos


    # # Función para insertar los asientos en la base de datos
    # def insertar_asientos():
    #     try:
    #         conexion = sql.connect("cine.db")
    #         cursor = conexion.cursor()

    #         for sala_id, (num_filas, num_asientos_por_fila) in salas_info.items():
    #             asientos = generar_asientos(sala_id, num_filas, num_asientos_por_fila)
    #             cursor.executemany("INSERT INTO asientos (id_sala, numero_as, fila_as) VALUES (?, ?, ?)", asientos)
            
    #         conexion.commit()
    #         print("Asientos generados y agregados correctamente a la base de datos.")

    #     except sql.Error as error:
    #         print("Error al insertar los asientos:", error)
    #     finally:
    #         conexion.close()

    # insertar_asientos()


    # conexion = sql.connect("cine.db")
    # cursor = conexion.cursor()

    # cursor.execute(
    #     """  CREATE TABLE IF NOT EXISTS boletos(
    #                 id_boleto INTEGER PRIMARY KEY,
    #                 id_horario INTEGER NOT NULL,
    #                 id_asiento INTEGER NOT NULL,
    #                 FOREIGN KEY (id_horario) REFERENCES horarios(id_horario),
    #                 FOREIGN KEY (id_asiento) REFERENCES asientos(id_asiento)
    #                 ON DELETE CASCADE
    #                 ON UPDATE CASCADE
    #             )
    #         """
    # )
    
    # conexion.commit()
    # conexion.close()


    # conexion = sql.connect("cine.db")
    # cursor = conexion.cursor()

    # cursor.execute(
    #     """DELETE FROM boletos"""
    # )

    # conexion.commit()
    # conexion.close()

        