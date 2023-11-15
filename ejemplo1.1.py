import pygame
import random
import sys

# Configuración inicial de Pygame
pygame.init()
ANCHO = 1200
ALTO = 750
ventana = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

class Organismo:
    def __init__(self, x, y, vida, energia, velocidad):
        self.x = x
        self.y = y
        self.vida = vida
        self.energia = energia
        self.velocidad = velocidad

    def perder_energia(self):
        # Los organismos pierden energía en cada ciclo
        self.energia -= 1
        if self.energia <= 0:
            self.vida = 0  # El organismo muere si se queda sin energía

    def mover(self):
        # Movimiento aleatorio sin salir de la pantalla
        desplazamiento_x = random.randint(-1, 1)
        desplazamiento_y = random.randint(-1, 1)

        nueva_posicion = (
            (self.x + desplazamiento_x * self.velocidad) % ANCHO,
            (self.y + desplazamiento_y * self.velocidad) % ALTO
        )

        self.x, self.y = nueva_posicion
        self.perder_energia()

class Animal(Organismo):
    def __init__(self, x, y, vida, energia, velocidad, especie, dieta, genero):
        super().__init__(x, y, vida, energia, velocidad)
        self.especie = especie
        self.dieta = dieta
        self.genero = genero

    def alimentarse(self, organismo, lista_organismos):
        # Lógica de alimentación
        if isinstance(organismo, Planta) and organismo.vida > 0 and abs(self.x - organismo.x) <= 20 and abs(self.y - organismo.y) <= 20:
            organismo.vida = 0
            self.energia += 10  # Ganar energía al alimentarse de plantas
            lista_organismos.remove(organismo)   # Eliminar la planta consumida

    def cazar(self, presa):
        # Lógica de caza
        distancia_x = abs(self.x - presa.x)
        distancia_y = abs(self.y - presa.y)

        if distancia_x <= 10 and distancia_y <= 10:
            # El animal puede cazar si la presa está a una casilla de distancia
            presa.vida = 0
            self.energia += 20

    def reproducirse(self, otro_animal):
        # Lógica de reproducción
        if self.energia > 70 and random.random() < 0.01 and self.genero != otro_animal.genero:
            return Animal(random.randint(0, ANCHO), random.randint(0, ALTO), 100, 50, 10, self.especie, self.dieta, random.choice(["macho", "hembra"]))
        return None

class Planta(Organismo):
    def __init__(self, x, y, vida, energia):
        super().__init__(x, y, vida, energia, 0)  # Las plantas no se mueven

    def fotosintesis(self):
        # Lógica de fotosíntesis
        self.energia += 3

    def reproducir(self):
        # Lógica de reproducción por semillas
        if random.random() < 0.01:
            nueva_posicion = (
                (self.x + random.randint(-20, 20)) % ANCHO,
                (self.y + random.randint(-20, 20)) % ALTO
            )
            nueva_planta = Planta(nueva_posicion[0], nueva_posicion[1], 50, 30)
            return nueva_planta
        return None

class Ambiente:
    def __init__(self, ecosistema):
        self.ecosistema = ecosistema
        self.factores_abioticos = {
            "temperatura": 25,
            "humedad": 50,
            "viento": 10
        }

        self.ciclos_meteorito = 30
        self.ciclos_tornado = 14
        self.ciclos_transcurridos_tornado = 0
        self.ciclos_transcurridos_meteorito = 0
        self.tornado_activado = False
        self.posicion_tornado = (random.randint(0, ANCHO), random.randint(0, ALTO))
        self.zona_impacto_tornado = set()
        self.duracion_impacto_tornado = 5  # Duración del impacto del tornado en segundos
        self.duracion_color_rojo = 5  # Duración del color rojo en segundos

    def aplicar_clima(self):
        self.factores_abioticos["temperatura"] += random.randint(-2, 2)
        self.factores_abioticos["humedad"] += random.randint(-5, 5)
        self.factores_abioticos["viento"] += random.randint(-3, 3)

        if self.ciclos_transcurridos_meteorito % self.ciclos_meteorito == 0 and random.random() < 0.6:
            self.impacto_meteorito()

        if self.ciclos_transcurridos_tornado % self.ciclos_tornado == 0 and random.random() < 0.6:
            self.activar_tornado()

        if self.tornado_activado:
            self.impacto_tornado()

        # Reducir la duración del color rojo
        if self.duracion_color_rojo > 0:
            self.duracion_color_rojo -= 1

    def impacto_meteorito(self):
        print("¡Impacto de meteorito!")
        self.ecosistema.organismos = []
        self.ciclos_transcurridos_meteorito = 0

    def activar_tornado(self):
        print("¡Tornado activado!")
        self.tornado_activado = True
        self.duracion_impacto_tornado = 5  # Duración del impacto del tornado en segundos

    def impacto_tornado(self):
        for organismo in self.ecosistema.organismos:
            if isinstance(organismo, Animal) or isinstance(organismo, Planta):
                distancia_x = abs(self.posicion_tornado[0] - organismo.x)
                distancia_y = abs(self.posicion_tornado[1] - organismo.y)
                if distancia_x <= 50 and distancia_y <= 50:
                    organismo.vida = 0
                    self.zona_impacto_tornado.add((organismo.x, organismo.y))
        # Desactivar el tornado después de un impacto
        self.ciclos_transcurridos_tornado = 0

    def avanzar_ciclo(self):
        self.ciclos_transcurridos_tornado += 1
        self.ciclos_transcurridos_meteorito += 1
        if self.duracion_impacto_tornado > 0:
            self.duracion_impacto_tornado -= 1
        self.aplicar_clima()
class Ecosistema:
    def __init__(self):
        self.organismos = []

        for _ in range(50):
            self.organismos.append(Animal(random.randint(0, ANCHO), random.randint(0, ALTO), 100, 50, 10, "León", "Carnívora", random.choice(["macho", "hembra"])))

        for _ in range(50):
            self.organismos.append(Animal(random.randint(0, ANCHO), random.randint(0, ALTO), 80, 40, 8, "Cebra", "Herbívora", random.choice(["macho", "hembra"])))

        for _ in range(50):
            self.organismos.append(Planta(random.randint(0, ANCHO), random.randint(0, ALTO), 50, 30))

    def update(self):
        nuevos_organismos = []

        for organismo in self.organismos:
            organismo.mover()

            for otro_organismo in self.organismos:
                if organismo != otro_organismo:
                    if isinstance(otro_organismo, Planta) and isinstance(organismo, Animal) and organismo.dieta == "Herbívora":
                        organismo.alimentarse(otro_organismo, self.organismos)
                    elif isinstance(otro_organismo, Animal) and isinstance(organismo, Animal) and organismo.dieta == "Carnívora":
                        organismo.cazar(otro_organismo)
                        if otro_organismo.vida <= 0:
                            self.organismos.remove(otro_organismo)
                    elif isinstance(otro_organismo, Animal) and isinstance(organismo, Animal) and organismo.dieta == "Herbívora":
                        nuevo_animal = organismo.reproducirse(otro_organismo)
                        if nuevo_animal:
                            nuevos_organismos.append(nuevo_animal)

            if organismo.vida <= 0:
                self.organismos.remove(organismo)

        for organismo in self.organismos:
            if isinstance(organismo, Planta):
                organismo.fotosintesis()
                nueva_planta = organismo.reproducir()
                if nueva_planta:
                    nuevos_organismos.append(nueva_planta)

        self.organismos.extend(nuevos_organismos)

# Ciclo principal del simulador
reloj = pygame.time.Clock()

ecosistema = Ecosistema()
ambiente = Ambiente(ecosistema)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ambiente.avanzar_ciclo()
    ecosistema.update()

    ventana.fill((255, 255, 255))  # Llenar la ventana con fondo blanco

    # Dibujar impacto del tornado
    for x, y in ambiente.zona_impacto_tornado:
        pygame.draw.circle(ventana, (255, 0, 0), (int(x), int(y)), 20)

    # Dibujar organismos en la ventana
    for organismo in ecosistema.organismos:
        if isinstance(organismo, Animal):
            if organismo.especie == "Cebra":
                color = (255, 0, 0)  # Rojo para cebras
            else:
                color = (0, 0, 255)  # Azul para otros animales
        elif isinstance(organismo, Planta):
            color = (0, 255, 0)  # Verde para plantas
        else:
            color = (0, 0, 255)  # Azul para otros organismos

        # Cambiar el color en la zona de impacto del tornado
        if (organismo.x, organismo.y) in ambiente.zona_impacto_tornado:
            color = (255, 0, 0)  # Rojo brillante

        pygame.draw.rect(ventana, color, pygame.Rect(organismo.x - 5, organismo.y - 5, 10, 10))

    # Dibujar área de impacto del tornado
    for punto_impacto in ambiente.zona_impacto_tornado:
        pygame.draw.circle(ventana, (255, 0, 0), punto_impacto, 100)

        

    pygame.display.flip()
    reloj.tick(5)  # Ajusta la velocidad de actualización de la ventana
