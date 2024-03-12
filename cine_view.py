from cine_db import Database

class View:
    def __init__(self):
        self.db = Database()

    def start(self):
        print('--------------------------------------')
        print(' ¡BIENVENIDO AL SISTEMA DE CINEMAX  ')
        print('--------------------------------------')

    def end(self):
        print('--------------------------------------')
        print('       ¡GRACIAS, VUELVA PRONTO!       ')
        print('--------------------------------------')
    

    #--------- Menús ---------#
    def menu_principal(self):
            
        print('--------------------------------------')
        print('            MENU CINEMAX           ')
        print('--------------------------------------')
        print('1.- Registrarse')
        print('2.- Administrar')
        print('3.- Salir')
        

    def menu_post_registro_cliente(self):
        print('--------------------------------------')
        print('         Bievenido al Sistema       ')
        print('--------------------------------------')
        print("1. Ver la cartelera")
        print("2. Salir")


    #--------- Administradores ---------#
    def menu_admin(self):
            
        print('--------------------------------------')
        print('            ADMINISTRACION            ')
        print('--------------------------------------')
        print('1.- Peliculas')
        print('2.- Clientes')
        print('3.- Facturas')
        print('4.- Salir')


    def menu_Peliculas(self):
            
        print('--------------------------------------')
        print('              PELICULAS           ')
        print('--------------------------------------')
        print('1.- Agregar Peliculas')
        print('2.- Editar Peliculas')
        print('3.- Eliminar Peliculas')
        print('4.- Ver Todas las peliculas')
        print('5.- Salir')


    def menu_clientes(self):
            
        print('--------------------------------------')
        print('               CLIENTES            ')
        print('--------------------------------------')
        print('1.- Agregar cliente')
        print('2.- Editar cliente')
        print('3.- Eliminar cliente')
        print('4.- Ver Todos los clientes')
        print('5.- Salir')


    def menu_facturas(self):
            
        print('--------------------------------------')
        print('               FACTURAS           ')
        print('--------------------------------------')
        print('1.- Nombre del cliente')
        print('2.- Nombre de la película')
        print('3.- Fecha de compra')
        print('4.- Total del consumo')
        print('5.- Salir')


    #--------- Cartelera ---------#
    def menu_cartelera(self):
            
        print('--------------------------------------')
        print('               CARTELERA              ')
        print('--------------------------------------')
        print('1.- Cartelera')
        print('3.- Salir')


    def leer_cartelera(self, peliculas, horarios):
            
        for pelicula in peliculas:
        # Imprimir información de la película
            print('--------------------------------------')
            print(pelicula[1].center(40))
            print('--------------------------------------')
            print('Director:'.ljust(10), pelicula[2])
            print('Genero:'.ljust(10), pelicula[3])
            print('Duracion:'.ljust(10), pelicula[4])
            print('Sinopsis:'.ljust(10), pelicula[5])
            print('--------------------------------------')

        # Imprimir información de los horarios para esta película
            print('HORARIOS'.center(40))
            for horario in horarios:
                if horario[1] == pelicula[0]:
                    print(' '*5, 'No. Funcion:', horario[0])
                    print(' '*11, 'Hora:', horario[4])
                    print(' '*11, 'Sala:', horario[2])
                    print(' '*5, '---------------------')


    #--------- Pelicula---------#
    def leer_pelicula(self, peliculas):
     
        for pelicula in peliculas:
        # Imprimir información de la película
            print('--------------------------------------')
            print(pelicula[1].center(40))
            print('--------------------------------------')
            print('ID Peli:'.ljust(10), pelicula[0])
            print('Director:'.ljust(10), pelicula[2])
            print('Genero:'.ljust(10), pelicula[3])
            print('Duracion:'.ljust(10), pelicula[4])
            print('Sinopsis:'.ljust(10), pelicula[5])
            print('--------------------------------------')


    #--------- Boleto ---------#
    def leer_boleto(self, titulo, duracion, fecha, hora, asientos, fila,):
        filas = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H', 9:'I', 10:'J', 11:'K', 12:'L'}
        print('--------------------------------------')
        print('              BOLETO           ')
        print('--------------------------------------')
        print('Pelicula: '.ljust(12),titulo)
        print('Duracion: '.ljust(12), duracion)
        print('Fecha: '.ljust(12), fecha)
        print('Hora: '.ljust(12), hora)
        print('Asiento: '.ljust(12), filas[fila],'-',asientos)
        print('Precio: '.ljust(12), "$300")
        print('--------------------------------------')


    #--------- Sala ---------#
    def leer_sala(self, salas):

        for sala in salas:
            print('--------------------------------------')
            print('              Sala:',sala[0])
            print('--------------------------------------')
            print('Numero de Filas: '.ljust(12), sala[1])
            print('asientoss por Fila: '.ljust(12), sala[2])
            print('--------------------------------------')


    def leer_salas(self, salas):
        print('-'*35)
        print('Salas'.center(35))
        print('-'*35)
        print('ID:'.ljust(5)+'Num Filas:'.ljust(15)+'asientoss por Fila:'.ljust(20))        
        print('-'*35)
        for sala in salas:
            print(f'{sala[0]:<5}{sala[1]:<15}{sala[2]:<20}')
        print('-'*35)


    def leer_asientos_sala(self, caracteres_asientos, sala):
        filas = {1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',10:'J',11:'K',12:'L'}  
        print('LOS ASIENTOS OCUPADOS ESTAN MARCADOS CON UNA X')     
        print("Sala:", sala[0])
        print('  '+'---'*sala[2])
        print('  '+'PANTALLA'.center(sala[2]*3))
        print('')
        i = 0
        cont = 0
        while i < sala[1]:
            j = 0
            print(filas[i+1],end='| ')
            while j < sala[2]:
                print(caracteres_asientos[cont],end='  ')
                j+=1
                cont+=1
            print('')
            i+=1
        i = 0
        print('  '+'---'*sala[2])
        print('   ',end='')
        while i < sala[2]:
            if i+1<10:
                print(i+1,end='  ')
            else:
                print(i+1,end=' ')
            i+=1
        print('')


    #--------- CLientes ---------#
    def ver_todos_los_clientes(self):
        clientes = self.db.getData('clientes')
        print('-'*50)
        print('CLIENTES'.center(55))
        print('-'*50)
        print('ID:'.ljust(5)+'Nombre:'.ljust(15)+'Apellido:'.ljust(11)+'Email:'.ljust(18))        
        print('-'*55)
        for cliente in clientes:
            print(f'{cliente[0]:<5}{cliente[1]:<15}{str(cliente[2]):<11}{cliente[3]:<18}')
        print('-'*55)

