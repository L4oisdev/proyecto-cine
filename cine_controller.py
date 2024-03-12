from cine_view import View
from cine_model import Model
from cine_db import Database


class Main:
    def __init__(self):
        self.view = View()
        self.model = Model()
        self.db = Database()


    def run(self):
        self.view.start()
        self.menu_principal()


    #--------- métodos relacionados con los menús ---------#
    def menu_principal(self):
        while True:
            self.view.menu_principal()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.model.logica.iniciar_sesion_cliente()
                self.menu_clientes()
            elif opcion == "2":
                self.model.logica.iniciar_sesion_admin()
                self.menu_admin()
            elif opcion == "3":
                self.view.end()
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")


    def menu_clientes(self):
        while True:
            self.view.menu_post_registro_cliente()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.model.interaction.ver_cartelera()
                self.menu_comprar_boleto()
            elif opcion == "2":
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")
    

    def menu_admin(self):
        while True:
            self.view.menu_admin()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.menu_peliculas()
            elif opcion == "2":
                self.administrar_clientes()
            elif opcion == "3":
                self.administrar_facturas()
            elif opcion == "4":
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")


    def menu_peliculas(self):
        while True:
            self.view.menu_Peliculas()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.model.logica.agregar_pelicula()
            elif opcion == "2":
                self.model.logica.editar_pelicula()
            elif opcion == "3":
                self.model.logica.eliminar_pelicula()
            elif opcion == "4":
                self.model.interaction.ver_todas_peliculas()
            elif opcion == "5":
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")



    #--------- métodos relacionados con la compra de boletos ---------#
    def menu_comprar_boleto(self):   

        while True:
            opcion_compra = input("Desea comprar un boleto? (Y/N): ")

            if opcion_compra.lower() == "y":
                funcion = input("Ingrese el numero de la funcion: ")
                while opcion_compra == "y":
                    boleto = self.comprar_boleto(funcion)
                    if boleto == True:
                        opcion_compra = input("¿Desea comprar OTRO boleto de esta misma funcion?(Y/N):")
                    else:
                        opcion_compra = "n"
            elif opcion_compra.lower() == "n":
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")


    def verificar_asiento_ocupado(self, id_horario, id_asiento):
        try:
            # Consultar la base de datos para verificar si el asiento está ocupado
            asiento = self.model.db.leer_boleto(id_horario, id_asiento,)
            
            # Si se encontró un asiento, significa que está ocupado
            if asiento:
                return True
            else:
                return False

        except Exception as e:
            print('Error al verificar el estado del asiento:', e)
            return True  # En caso de error, asumimos que el asiento está ocupado para evitar que se venda


    def mostrar_boleto(self, id_horario, asiento, fila):

        hora = self.model.db.leer_horario(id_horario)
        peli = self.model.db.leer_pelicula(hora[1])
        self.view.leer_boleto(peli[1],peli[4], hora[3], hora[4], asiento, fila)


    def comprar_boleto(self, id_horario):
        try:

            asientos = []
            horario = self.db.selectDataById("horarios", "id_horario", id_horario)
            if not isinstance(horario, tuple):
                print('No se encontró ningún horario con el ID especificado.')
                return False
 
            id_sala = horario[2]
            sala = self.model.db.leer_sala(id_sala)
            boletos = self.model.db.leer_boletos()
            asientosNumbers = self.model.db.leer_asientos(id_sala)

            sala_capacidad = sala[3]


            for asiento in range(sala_capacidad):
                j = 0
                for boleto in boletos:
                    if boleto[2] == asientosNumbers[asiento][0] and boleto[1] == int(id_horario): 
                        j = 1
                if j == 0:
                    asientos.append('0')

                else:
                    asientos.append('X')


            self.view.leer_asientos_sala(asientos, sala)
        
            fila = input("¿Qué fila quieres?: ")
            asiento = int(input(f"Elige un asiento de la fila {fila.upper()}: "))
            filas = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':11,'L':12}
            fila_numero = filas.get(fila.upper())
            asiento_numero = self.model.db.leer_asiento(id_sala, asiento, fila_numero)
            if fila_numero is None:
                print('La fila especificada no existe en la sala.')
                return False

            # Marcar el asiento como ocupado antes de verificar si está disponible
            asientos[asiento - 1] = 'X'

            # Verificar si el asiento está ocupado consultando la base de datos
            asiento_ocupado = self.verificar_asiento_ocupado(id_horario, asiento_numero[0])
            if asiento_ocupado:
                print('¡Asiento ocupado, escoge otro!')
                return False

            if self.model.db.crear_boleto(id_horario, asiento_numero[0]):
                print('¡Boleto comprado exitosamente!')
                self.mostrar_boleto(id_horario, asiento_numero[2], fila_numero)
                return True
            
            else:
                print('¡Error al comprar el boleto!')
                return False

        except Exception as e:
            print('Error al comprar boleto:', e)
            return False



    def administrar_clientes(self):
       
        while True:
            self.view.menu_clientes()
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.model.logica.agregar_cliente()
            elif opcion == "2":
                self.model.logica.editar_cliente()
            elif opcion == "3":
                self.model.logica.eliminar_cliente()
            elif opcion == "4":
                self.view.ver_todos_los_clientes()
            elif opcion == "5":
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")


    def administrar_facturas(self):
       
        while True:
            self.view.menu_facturas()
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                # Lógica para crear factura
                pass
            elif opcion == "2":
                # Lógica para ver todas las facturas
                pass
            elif opcion == "3":
                # Lógica para ver una factura específica
                pass
            elif opcion == "4":
                # Lógica para actualizar una factura
                pass
            elif opcion == "5":
                # Lógica para eliminar una factura
                pass
            elif opcion == "6":
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")



if __name__ == "__main__":
    main = Main()
    main.run()
