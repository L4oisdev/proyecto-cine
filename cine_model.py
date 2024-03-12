import sqlite3 as sql
from cine_db import Database
from cine_view import View

# métodos relacionados con la interacción con la base de datos
class ModelDB:

    def __init__(self):
        self.db = Database()
    
    #--------- Boletos ---------#
    def crear_boleto(self, id_horario, id_asiento):
        try:
            conexion = sql.connect("cine.db")
            cursor = conexion.cursor()
            query = f'INSERT INTO boletos (id_horario, id_asiento) VALUES ({id_horario}, {id_asiento})' 
            cursor.execute(query)
            conexion.commit()  
            return True 
                
        except sql.Error as error:
            print("Error al crear boleto:", error)


    def leer_boleto(self, id_horario, id_asiento):
        try:
            conexion = sql.connect("cine.db")
            cursor = conexion.cursor()
            query = "SELECT * FROM boletos WHERE id_horario = ? AND id_asiento = ?"
            vals = (id_horario, id_asiento,)
            cursor.execute(query, vals)
            boleto = cursor.fetchone()
            
            if boleto == None:
                return False
            return True
        
        except sql.Error as error:
            print("Error al leer los boletos:", error)


    def leer_boletos(self):
        try:
            conexion = sql.connect("cine.db")
            cursor = conexion.cursor()
            query = "SELECT * FROM boletos"
            cursor.execute(query)
            boletos = cursor.fetchall()

            return boletos
        
        except sql.Error as error:
            print("Error al leer los boletos:", error)


    
    #--------- Asientos ---------#
    def leer_asientos_sala(self, id_sala):
        try:
            conexion = sql.connect("cine.db")
            cursor = conexion.cursor()
            query = "SELECT * FROM asientos WHERE id_sala = ?"
            vals = (id_sala, )
            cursor.execute(query, vals)
            records = cursor.fetchall()

            return records
        
        except sql.Error as error:
            print("Error al leer los asientos:", error)


    def leer_asiento(self, id_sala, numero_as, fila_as):
        try:
            conexion = sql.connect("cine.db")
            cursor = conexion.cursor()
            query = "SELECT * FROM asientos WHERE id_sala = ? AND numero_as = ? AND fila_as = ?"
            vals = (id_sala, numero_as, fila_as)
            cursor.execute(query, vals)
            asiento = cursor.fetchone()

            return asiento

        except sql.Error as error:
            print("Error al leer el asiento:", error)
            return None

        
    def leer_asientos(self, id_sala):
        
        try:
            conexion = sql.connect("cine.db")
            cursor = conexion.cursor()
            query = """
                SELECT
                    a.id_asiento,
                    a.id_sala,
                    a.numero_as,
                    a.fila_as
                FROM asientos a
                INNER JOIN salas s ON a.id_sala = s.id_sala
                WHERE s.id_sala = ?;
             """
            cursor.execute(query, (id_sala,))
            asientos = cursor.fetchall()

            return asientos

        except sql.Error as error:
            print("Error al leer el asientos:", error)
        return None
     
        
    #--------- Sala ---------#
    def leer_sala(self, id_sala):
        try:
            conexion = sql.connect("cine.db")
            cursor = conexion.cursor()
            query = 'SELECT * FROM salas WHERE id_sala = ?' 
            vals = (id_sala,)
            cursor.execute(query, vals)
            record = cursor.fetchone()
            return record
        
        except sql.Error as error:
            print("Error al leer sala:", error)
        

    #--------- Peliulas ---------#
    def leer_pelicula(self, id_pelicula):
        try:
            conexion = sql.connect("cine.db")
            cursor = conexion.cursor()
            query = 'SELECT * FROM peliculas WHERE id_pelicula = ?' 
            vals = (id_pelicula,)
            cursor.execute(query, vals)
            record = cursor.fetchone()
            return record
        
        except sql.Error as error:
            print("Error al leer la pelicula:", error)
    

    #--------- Horario ---------#
    def leer_horario(self, id_horario):
        try:
            conexion = sql.connect("cine.db")
            cursor = conexion.cursor()
            query = 'SELECT * FROM horarios WHERE id_horario = ?' 
            vals = (id_horario,)
            cursor.execute(query, vals)
            horario = cursor.fetchone()
            return horario
        
        except sql.Error as error:
            print("Error al leer la pelicula:", error)
    

   
# métodos relacionados con la lógica de la aplicación
class ModelLogic:

    def __init__(self):
        self.db = Database()
        self.view = View() 

    #--------- CLIENTES ---------#
    def agregar_cliente(self):
        nombre = input("Ingrese el nombre del cliente: ")
        apellido = input("Ingrese el apellido del cliente: ")
        email = input("Ingrese el email del cliente: ")
        pass_cliente = input("Ingrese la contraseña del cliente: ")

        datos_cliente = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "pass_cliente": pass_cliente
        }

        self.db.insertData("clientes", datos_cliente)

    def eliminar_cliente(self):
        id_cliente = int(input("Ingrese el ID del cliente que desea eliminar: "))
        self.db.deleteData("clientes", "id_cliente", id_cliente)

    def editar_cliente(self):
        id_cliente = int(input("Ingrese el ID del cliente que desea editar: "))
        # Obtener los datos actuales del cliente
        cliente_actual = self.db.selectDataById("clientes", "id_cliente", id_cliente)
        if cliente_actual:
            # Solicitar los nuevos datos al usuario
            nuevo_nombre = input(f"Nuevo nombre ({cliente_actual[1]}): ")
            nuevo_apellido = input(f"Nuevo Apellido ({cliente_actual[2]}): ")
            nuevo_email = input(f"Nuevo email ({cliente_actual[3]}): ")
            nueva_contrasena = input(f"Nueva contraseña ({cliente_actual[4]}): ")

            # Actualizar los datos en la base de datos
            datos_actualizados = {
                "nombre": nuevo_nombre if nuevo_nombre else cliente_actual[1],
                "apellido  ": nuevo_apellido if nuevo_apellido else cliente_actual[2],
                "email": nuevo_email if nuevo_email else cliente_actual[3],
                "pass_cliente": nueva_contrasena if nueva_contrasena else cliente_actual[4]
            }

            self.db.updateData("clientes", datos_actualizados, "id_cliente", id_cliente)
        else:
            print("No se encontró ningún cliente con el ID proporcionado.")


    #--------- PELICULAS ---------#
    def agregar_pelicula(self):
        titulo = input("Ingrese el título de la película: ")
        director = input("Ingrese el nombre del director: ")
        genero = input("Ingrese el género de la película: ")
        duracion = int(input("Ingrese la duración de la película en minutos: "))
        sinopsis = input("Ingrese la sinopsis de la película: ")

        datos_pelicula = {
            "titulo": titulo,
            "director": director,
            "genero": genero,
            "duracion": duracion,
            "sinopsis": sinopsis
        }

        self.db.insertData("peliculas", datos_pelicula)

    def editar_pelicula(self):
        id_pelicula = int(input("Ingrese el ID de la película que desea editar: "))
        # Obtener los datos actuales de la película
        pelicula_actual = self.db.selectDataById("peliculas", "id_pelicula", id_pelicula)
        if pelicula_actual:
            # Solicitar los nuevos datos al usuario
            nuevo_titulo = input(f"Nuevo título ({pelicula_actual[1]}): ")
            nuevo_director = input(f"Nuevo director ({pelicula_actual[2]}): ")
            nuevo_genero = input(f"Nuevo género ({pelicula_actual[3]}): ")
            nueva_duracion = input(f"Nueva duración ({pelicula_actual[4]}): ")
            nueva_sinopsis = input(f"Nueva sinopsis ({pelicula_actual[5]}): ")

            # Actualizar los datos en la base de datos
            datos_actualizados = {
                "titulo": nuevo_titulo if nuevo_titulo else pelicula_actual[1],
                "director": nuevo_director if nuevo_director else pelicula_actual[2],
                "genero": nuevo_genero if nuevo_genero else pelicula_actual[3],
                "duracion": nueva_duracion if nueva_duracion else pelicula_actual[4],
                "sinopsis": nueva_sinopsis if nueva_sinopsis else pelicula_actual[5]
            }

            self.db.updateData("peliculas", datos_actualizados, "id_pelicula", id_pelicula)
        else:
            print("No se encontró ninguna película con el ID proporcionado.")

    def eliminar_pelicula(self):
        id_pelicula = int(input("Ingrese el ID de la película que desea eliminar: "))
        self.db.deleteData("peliculas", "id_pelicula", id_pelicula)


    #--------- FACTURAS ---------#
    def crear_factura(self):
        id_cliente = int(input("Ingrese el ID del cliente: "))
        id_pelicula = int(input("Ingrese el ID de la película: "))
        fecha_compra = input("Ingrese la fecha de compra (YYYY-MM-DD): ")
        total_consumo = float(input("Ingrese el total del consumo: "))

        datos_factura = {
            "id_cliente": id_cliente,
            "id_pelicula": id_pelicula,
            "fecha_compra": fecha_compra,
            "total_consumo": total_consumo
        }

        self.db.insertData("facturas", datos_factura)


    #--------- LOGIN ---------#
    def iniciar_sesion_admin(self):
        while True:
            usuario = input("Usuario: ")
            contrasena = input("Contraseña: ")
            if self.db.verificar_credenciales("administradores", "user_admn", "pass_admn", usuario, contrasena):
                print("Inicio de sesión exitoso.")
                break
            else:
                print("Credenciales incorrectas. Inténtelo de nuevo.")


    def iniciar_sesion_cliente(self):

        while True:
            print("Inicie sección")
            email = input("Ingrese su Email: ")
            contrasena = input("Ingrese su Contraseña: ")
            if self.db.verificar_credenciales("clientes", "email", "pass_cliente", email, contrasena):
                print("Inicio de sesión exitoso.")
                break
            else:
                print("Credenciales incorrectas. Inténtelo de nuevo.")
    


# métodos relacionados con la interacción con el usuario
class ModelInteraction: 

    def __init__(self):
        self.view = View()
        self.db = Database()


    def ver_cartelera(self):
        peliculas = self.db.getData("peliculas")
        horarios = self.db.getData("horarios")
        self.view.leer_cartelera(peliculas, horarios)



    def ver_todas_peliculas(self):
        peliculas = self.db.getData("peliculas")
        self.view.leer_pelicula(peliculas)



class Model:

    def __init__(self):
        self.logica = ModelLogic()
        self.db = ModelDB()
        self.interaction = ModelInteraction()
