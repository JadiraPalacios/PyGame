import sys  #para usar el exit()
import pygame 
import time #para usar sleep()

ANCHO= 640 #ancho de la pantalla
ALTO =480  #alto de la pantalla
color_negro=(0,0,0)#color negro de fondo
color_blanco=(255,255,255)

pygame.init()

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
        #evitar que salga por debajo
        if self.rect.top <= 0:
           self.speed[1]= -self.speed[1]
        #evitar que salga por la derecha
        elif self.rect.right >= ANCHO or self.rect.left <= 0:
            self.speed[0]= -self.speed[0]
        #mover en base a posicion actual y velocidad
        self.rect.move_ip(self.speed)    

class Paleta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #cargar imagen
        self.image = pygame.image.load("./paleta.png")
        #obtener rectangulo de la imagen
        self.rect=self.image.get_rect()
        #posicion inicial centrada en pantalla X
        self.rect.midbottom=(ANCHO/2,ALTO-20)
        #establecer velocidad inicial
        self.speed=[0,0]



    def update(self,evento):
        #buscar si se presiono flecha izquierda
        if evento.key==pygame.K_LEFT and self.rect.left>0:
            self.speed=[-5,0]
        elif evento.key==pygame.K_RIGHT and self.rect.right<ANCHO:
            self.speed=[5,0]
        else:
            self.speed=[0,0]
        #mover en base a posicion actual y velocidad
        self.rect.move_ip(self.speed)


class Ladrillo(pygame.sprite.Sprite):
    def __init__(self,posicion):
        pygame.sprite.Sprite.__init__(self)
        #cargar imagen
        self.image = pygame.image.load("./ladrillo.png")
        #obtener rectangulo de la imagen
        self.rect=self.image.get_rect()
        #posicion inicial cprovista externamentr
        self.rect.topleft=posicion


class Muro(pygame.sprite.Group):
    def __init__(self,cantidadLadrillos):
        pygame.sprite.Group.__init__(self)

        pos_x=0
        pos_y=20
        for i in range(cantidadLadrillos):
            ladrillo=Ladrillo((pos_x,pos_y))
            self.add(ladrillo)

            pos_x+=ladrillo.rect.width
            if pos_x>=ANCHO:
                pos_x=0
                pos_y +=ladrillo.rect.height

#funcion llamada tras dejar ir la bolita
def juego_terminado():
    fuente=pygame.font.SysFont("Consolas",30)
    texto=fuente.render("Juego terminado :c",True,(255,0,0))
    texto_rect=texto.get_rect()
    texto_rect.center=[ANCHO/2,ALTO/2]
    pantalla.blit(texto,texto_rect)
    pygame.display.flip()
    #pausar por 3 segundos
    time.sleep(3)
    #salir
    sys.exit()

def mostrar_puntuacion():
    fuente=pygame.font.SysFont("Consolas",20)
    texto=fuente.render(str(puntuacion).zfill(5),True,color_blanco)
    texto_rect=texto.get_rect()
    texto_rect.topleft=[0,0]
    pantalla.blit(texto,texto_rect)
   
def mostrar_vidas():
    fuente=pygame.font.SysFont("Consolas",20)
    cadena="Vidas: "+str(vidas).zfill(2)
    texto=fuente.render(cadena,True,color_blanco)
    texto_rect=texto.get_rect()
    texto_rect.topright=[ANCHO,0]
    pantalla.blit(texto,texto_rect)

#inicializando pantalla
pantalla=pygame.display.set_mode((ANCHO,ALTO))
#configurar titulo de pantalla
pygame.display.set_caption("Juego de ladrillos")
#crear el reloj
reloj=pygame.time.Clock()
pygame.key.set_repeat(30)

bolita=Bolita()
jugador=Paleta()
muro=Muro(50)
puntuacion=0
vidas=3
esperando_saque=True

while True:
    #establecer FPS
    reloj.tick(60)

    #revisar todos los eventos
    for evento in pygame.event.get():
        #si se preciona la tachita de la barra de titulo
        if evento.type == pygame.QUIT:
            #cerrar videojuego
            sys.exit()

        elif evento.type==pygame.KEYDOWN:
            jugador.update(evento)
            if esperando_saque==True and evento.key ==pygame.K_SPACE:
                esperando_saque=False
                if bolita.rect.centerx<ANCHO/2:
                    bolita.speed=[3,-3]
                else:    
                    bolita.speed=[-3,-3]
    #actualizar posicion de la bolita
    if esperando_saque==False:
         bolita.update()
    else:
        bolita.rect.midbottom=jugador.rect.midtop

    #colision entre jugador y bolita
    if pygame.sprite.collide_rect(bolita,jugador):
        bolita.speed[1]=-bolita.speed[1]

    #colision de la biblia con el muro
    lista = pygame.sprite.spritecollide(bolita,muro,False)
    if lista:
        ladrillo=lista[0]
        cx=bolita.rect.centerx
        if cx<ladrillo.rect.left or cx>ladrillo.rect.right:
            bolita.speed[0]=-bolita.speed[0]
        else:
            bolita.speed[1]=-bolita.speed[1]
        muro.remove(ladrillo)
        puntuacion+=10

    #REvisar si bolita sale de la pantalla
    if bolita.rect.top >ALTO:
        vidas-=1
        esperando_saque=True


    #rellenar pantalla
    pantalla.fill(color_negro)
    #mostrar puntuacion
    mostrar_puntuacion()
    #mostrar vidas
    mostrar_vidas()
    #dibujar bolita en la pantalla
    pantalla.blit(bolita.image,bolita.rect)
    #dibujar jugador en la pantalla
    pantalla.blit(jugador.image,jugador.rect)
    #dibujar los ladrillos
    muro.draw(pantalla)
    #actualizar elementos de la pantalla
    pygame.display.flip()

    if vidas<=0:
        juego_terminado()
