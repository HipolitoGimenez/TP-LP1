from datetime import datetime
from typing import List
from src.Vehiculos.auto import Auto
from src.Vehiculos.avion import Avion
from src.Vehiculos.helicoptero import Helicoptero
from src.Vehiculos.vehiculo import Vehiculo
from src.Personas.cirujano import Cirujano
from src.Personas.paciente import Paciente
from src.Personas.donantes import Donante
from src.Personas.receptor import Receptor

class CentroDeSalud:
    def __init__(self, nombre: str, direccion: str, partido: str, provincia: str, telefono: str):
        """
        Inicializa un centro de salud con sus datos principales.
        Crea listas vacías para cirujanos y vehículos, e inicializa el contador de trasplantes realizados.
        """
        self.nombre = nombre
        self.direccion = direccion
        self.partido = partido
        self.provincia = provincia
        self.telefono = telefono
        self.cirujanos = []  
        self.vehiculos = []  
        self.pacientes=[]
        self.receptor=[]
        self.donante=[]
        self.transplante_realizado = 0 

    
    def agregar_vehiculos(self, vehiculo):
        """
        Recibe: un objeto Vehiculo.
        Hace: lo agrega a la lista de vehículos del centro.
        Devuelve: nada.
        """
        self.vehiculos.append(vehiculo)


    def agregar_cirujano(self, nuevo_cirujano: Cirujano):  
        """
        Recibe: un objeto Cirujano.
        Hace: lo agrega a la lista de cirujanos del centro.
        Devuelve: nada.
        """     
        self.cirujanos.append(nuevo_cirujano)
    
    def agregar_pacientes(self,nuevo_paciente:Paciente):
       """
    Agrega un paciente (donante o receptor) a la lista general de pacientes.

    Args:
        nuevo_paciente (Paciente): Instancia de la clase Paciente o sus subclases.
    """
       self.pacientes.append(nuevo_paciente)
    

    def agregar_receptor(self,nuevo_receptor:Receptor):
       """
    Agrega un receptor a la lista de receptores y también a la lista general de pacientes.

    Args:
        nuevo_receptor (Receptor): Instancia de Receptor.
    """
       self.receptor.append(nuevo_receptor)
       self.pacientes.append(nuevo_receptor)


    def agregar_donantes(self,nuevo_donante:Donante):
       """
    Agrega un donante a la lista de donantes y también a la lista general de pacientes.

    Args:
        nuevo_donante (Donante): Instancia de Donante.
    """
       self.donante.append(nuevo_donante)
       self.pacientes.append(nuevo_donante)
  

    def asignar_cirujano(self, organo_necesario):
      print("Asignando_cirujano")
      """
        Recibe: un objeto Organo.
        Hace: busca un cirujano disponible y especializado en el tipo de órgano necesario.
              Si lo encuentra, lo marca como ocupado y lo devuelve.
        Devuelve: el cirujano asignado o False si no hay uno disponible.
        """
      if not self.cirujanos:
        print("No hay cirujanos registrados.")
        return False

      for i in range(len(self.cirujanos)):
        ciru = self.cirujanos[i]  
        if ciru.disponibilidad and ciru.es_especialista(organo_necesario):
            ciru.ocupado()
            print(f"Cirujano asignado: {ciru.nombre} para el órgano {organo_necesario}")
            return ciru.calcular_exito(organo_necesario)

        print(f"No se encontró cirujano disponible para el {organo_necesario}")
        return False


    def asignarVehiculo(self, otroCentroSalud, distancia:int, nivelTrafico:int):
        print("Comienzo asignacion Vehiculo")
        """
        Recibe: otro CentroDeSalud, una distancia (float/int), y un nivel de tráfico (str/int).
        Hace: elige un tipo de vehículo apropiado (Auto, Helicóptero, Avión) según la ubicación del otro centro,
              y lo usa para transportar el órgano.
        Devuelve: nada.
        """
        if(self._estanEnLaMismaProvinciaYPartido(otroCentroSalud)):
           print("Vehiculo designado  auto")
           self.transportarOrgano( self._obtenerVehiculo('Auto'), distancia, nivelTrafico)
        elif (self._estanEnMismaProvincia(otroCentroSalud)):
           print("Vehiculo designado  Helicoptero")
           self.transportarOrgano( self._obtenerVehiculo('Helicoptero'), distancia, nivelTrafico)
        else:
           print("Vehiculo designado Avion")
           self.transportarOrgano( self._obtenerVehiculo('Avion'), distancia, nivelTrafico)
    

    def _estanEnLaMismaProvinciaYPartido(self, otroCentroSalud):
       
       """
        Recibe: otro CentroDeSalud.
        Hace: compara provincia y partido entre ambos centros.
        Devuelve: True si están en el mismo partido y provincia, False si no.
        """
       return self.provincia == otroCentroSalud.provincia and self.partido == otroCentroSalud.partido
    

    def _estanEnMismaProvincia(self, otroCentroSalud):
       """
        Recibe: otro CentroDeSalud.
        Hace: compara solo la provincia entre ambos centros.
        Devuelve: True si están en la misma provincia, False si no.
        """
       return self.provincia == otroCentroSalud.provincia
    

    def transportarOrgano(self, vehiculo:Vehiculo, distancia, nivelTrafico):
       """
        Recibe: un objeto Vehiculo, una distancia y un nivel de tráfico.
        Hace: asigna esos valores al vehículo y registra el viaje con destino al centro de salud actual.
        Devuelve: nada.
        """
       vehiculo.setDistancia(distancia)
       vehiculo.registrar_viaje(self.direccion,distancia,nivelTrafico)

    
    def _obtenerVehiculo(self, tipo):
       """
        Recibe: un string que indica el tipo de vehículo ('Auto', 'Avion', 'Helicoptero').
        Hace: busca el primer vehículo disponible del tipo especificado, lo marca como ocupado.
        Devuelve: el vehículo encontrado o None si no hay disponible.
        """
       vehiculoAsignado = None
       for vehiculo in self.vehiculos:
          vehiculoobjeto=Vehiculo(vehiculo)
          if not vehiculoobjeto.enUso:
            vehiculoobjeto.ocupado()
            vehiculoAsignado = vehiculoobjeto
            break
       return vehiculoAsignado


    def realizarAblacion(self, donante, organo):
        print("Se realiza Ablacion")
        """
        Recibe: un objeto Donante y un objeto Organo.
        Hace: registra la fecha y hora de ablación del órgano y lo quita de la lista del donante.
        Devuelve: nada.
        """
        organo.fecha_hora_de_ablacion = datetime.now()
        donante.lista_organos.remove(organo)
    

    def __eq__(self, otroCentroSalud): 
        """
        Recibe: otro objeto CentroDeSalud.
        Hace: compara nombre y dirección entre ambos objetos.
        Devuelve: True si ambos centros son considerados iguales, False si no.
        """
        return self.nombre == otroCentroSalud.nombre and self.direccion == otroCentroSalud.direccion 


   
 


        
        




    