import sys  #para usar el exit()
import pygame 

ANCHO= 640 #ancho de la pantalla
ALTO =480  #alto de la pantalla

class Bolita(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #cargar imagen
        self.image = pygame.image.load("./bolita.png")
        #obtener rectangulo de la imagen
        self.rect=self.image.get_rect()
        #posicion inicial centrada en pantalla
        self.rect.centerx=ANCHO/2
        self.rect.centery=ALTO/2
        #establecer velocidad inicial
        self.speed=[3,3]
    def update(self):
        #mover en base a posicion actual y velocidad
        self.rect.move_ip(self.speed)    


#inicializando pantalla
pantalla=pygame.display.set_mode((ANCHO,ALTO))
#configurar titulo de pantalla
pygame.display.set_caption("Juego de ladrillos")
#crear el reloj
reloj=pygame.time.Clock()

bolita=Bolita()

while True:
    #establecer FPS
    reloj.tick(60)

    #revisar todos los eventos
    for event in pygame.event.get():
        #si se preciona la tachita de la barra de titulo
        if event.type == pygame.QUIT:
            #cerrar videojuego
            sys.exit()

    #actualizar posicion de la bolita
    bolita.update()

    #dibujar bolita en la pantalla
    pantalla.blit(bolita.image,bolita.rect)
    #actualizar elementos de la pantalla
    pygame.display.flip()