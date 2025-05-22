from vehiculo import Vehiculo

class Auto(Vehiculo):
    def __init__(self, velocidad):
        super().__init__(velocidad)
    
    def __str__(self):
        return f"Vehículo Terrestre (Velocidad: {self.velocidad} km/h)"

    def calcular_tiempo_viaje(self, distancia, trafico):
        if distancia <= 0 or self.velocidad <= 0:
            return float('inf')
        return distancia / self.velocidad + trafico
