
from re import A
from pygame import mixer
import pygame, sys
import os 
import random 
import Botones_Inicio
import csv

mixer.init()
pygame.init()



# Pantalla
Width = 1100
Height = 640

Pantalla = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('GameFinal')

#Velocidad de Fotogramas 
clock = pygame.time.Clock()
FPS = 50 #El control de FPS se utiliza para hacer que los frames (imágenes) pasen por la pantalla más rápido o más lento


#Variables de Juego
Gravedad = 0.75
Scroll = 200
Tile_Size = 40 #Tamaño de Mosaicos
filas = 16
columnas = 150
level = 1
max_levels = 3
Tile_Size = Height // filas
Tiles_type = 29
bg_scroll = 0
Pantalla_scroll = 0

Comenzar_Juego = False
Intro = False


#Movimientos de Personaje 
Movimiento_Derecha = False
Movimiento_Izquierda = False
shoot = False
shoot_a = False
shoot_b = False
shoot_c = False
shoot_d = False
grenade = False
grenade_lanzada = False



#Cargo Musica
# Musica_Fondo = pygame.mixer.Sound('audio/Audio_Prueba.mpeg')
# Musica_Fondo.play(-1)
# Musica_Fondo.set_volume(0.05) 
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.05)
shot_fx = pygame.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.05)
grenade_fx = pygame.mixer.Sound('audio/grenade.wav')
grenade_fx.set_volume(0.05)

#Bullets 
bullet_d = pygame.image.load('img/icons/bullet_d.png')
Escopeta_bullet = pygame.image.load('img/icons/bullet_c.png')
Fusil_bullet   = pygame.image.load('img/icons/lobo_a.png')
ametralladora_bullet  = pygame.image.load('img/icons/bala_franco.png')
bullet_img = {
    'Bullet' : bullet_d,
    'Escopeta' : Escopeta_bullet,
    'Fusil' : Fusil_bullet,
    'Ametralladora' : ametralladora_bullet
}

#Cargo imagenes
 
#Armas 
bala_icons = pygame.image.load('img/icons/Cartucho.png')
granada_icons = pygame.image.load('img/icons/grenade_c.png')
grenade_img  = pygame.image.load('img/icons/grenade_c.png')

#Salud
Recuperar_Salud_img = pygame.image.load('img/icons/Medicina.png')
Recuperar_Salud50_img = pygame.image.load('img/icons/salud.png')
Recargar_Municion_img  = pygame.image.load('img/icons/Cartucho.png')
Recargar_Granadas_img  = pygame.image.load('img/icons/granadas.png')

#Background
Fondo_Menu = pygame.image.load('img/Soldado_B.jpg')
sky_img = pygame.image.load('img/Background/Fondo_d.jpg').convert_alpha()
img_list = []
for x in range(Tiles_type):
    img = pygame.image.load(f'img/tile/{x}.png')
    img = pygame.transform.scale(img,(Tile_Size , Tile_Size))
    img_list.append(img)
    
      
    

#Botones 
start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()

#Items
Escopeta = pygame.image.load('img/icons/escopeta.png')
Fusil  = pygame.image.load('img/icons/Fusil_asalto.png')
ametralladora = pygame.image.load('img/icons/ametralladora.png')
corazon_icons = pygame.image.load('img/icons/corazon_a.png')




caja_articulos = { #Diccionario 
    'Salud'   : Recuperar_Salud_img,  #Llamo cada imagen segun la seleccion de Nombre: 'Salud', 'Municion', etc..
    'Municion' : Recargar_Municion_img,
    'Granadas' : Recargar_Granadas_img,
    'Salud50%' : Recuperar_Salud50_img,
    'Ametralladora' : ametralladora,
    'Fusil' : Fusil,
    'Escopeta' : Escopeta,
}

#Fuentes 

font = pygame.font.SysFont( 'Bodoni', 30 ,  ) #Declaro el tipo de font y su tamaño 

# Colores
Verde_claro = ( 144, 201, 120) #Verde Claro
Amarillo = (255,255,0 ) # Amarillo
Rojo = (255, 0, 0) #Rojo
White = (255, 255, 255)
Verde = (0, 255,0 )
Black = (0, 0, 0)
color_a = (14, 98, 81)
color_b =(22, 160, 133)
color_c =(204, 204, 255)
Rosa = (255, 153, 204)
Azul_claro = (102, 204, 255)
Azul_Cielo = (204, 204, 255)
Azul_aqua = (0, 255, 255)
Azul_aquamarine = (127, 255, 212)

# Colores=https://htmlcolorcodes.com/es/tabla-de-colores/tabla-de-colores-web-seguros/


# -----------------///---------------///----------///----

def draw_text(text, font, text_color , x , y): #Metodo para escribir en pantalla 
    img = font.render(text, True, text_color) #Renderizo el texto como imagen 
    Pantalla.blit(img,(x,y)) 

def draw_bg():
    Pantalla.fill(Azul_aquamarine)
    Width = sky_img.get_width()
    for x in range (5): #Repeticiones de imagen/ Fondo mapa
        Pantalla.blit(sky_img, ((x * Width) - bg_scroll * 0.5, 0))

# pygame.draw.line(Pantalla,Black,(0, 500), (Width,500))

#Funcion reiniciar Nivel
def reset_level():
	Enemigo_group.empty()
	bullet_group.empty()
	grenade_group.empty()
	explosion_group.empty()
	caja_articulos_group.empty()
	decoration_group.empty()
	water_group.empty()
	exit_group.empty()

	#Lista de mosaicos
	data = []
	for row in range(filas):
		r = [-1] * columnas
		data.append(r)
	return data

# -----------------///---------------///----------///----

class Player(pygame.sprite.Sprite):
    def __init__(self, Salud ,char_type, x, y, scale, speed, municion, grenade): #Parametros
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type #Declaro el tipo de imagen que quiero insertar 
        self.speed = speed
        self.municion = municion #Esta me reducira la municion cada vez que dispare
        self.municion_a = 0
        self.municion_b = 0
        self.municion_c = 0
        self.Start_municion = municion #Municion Inicial 
        # self.Start_municion_a = 0
        self.grenade = grenade
        self.shoot_enfriamiento = 0 #Enfriamiento o tiempo para disparar (Limitacion de la rapidez con la que puedo disparar )
        self.shoot_a_enfriamiento = 0
        self.shoot_b_enfriamiento = 0
        self.shoot_c_enfriamiento = 0
        self.Salud = Salud
        self.Salud_maxima = self.Salud
        self.direction = 1
        self.velocidad_y = 0
        self.jump = False
        self.en_aire = True
        self.flip = False
        self.lista_animaciones = []
        self.frame_index = 0 # Punto en el que se encuentra la Animacion
        self.action = 0
        self.update_time = pygame.time.get_ticks() # Me permite medir o actualizar las horas de cada animacion
        
        # IA Variables 
        self.move_counter = 0
        self.marcha = False
        self.idling_counter = 0 #Sacar a los enemigos del estado inactivo 
        self.linea_vision = pygame.Rect(0 , 0, 160, 20) #= Posicion en x, Posicion en y, ancho y altura 
        
        
        
        
        #Crago las imagenes para el player 
        animation_types = ['Idle','Movimientos_Derecha', 'Salto' , 'Death']
        for animation in animation_types:
            #Resetear lista temporal de Imagenes
            temp_lista = []
            #Contar numeros de archivos por carpeta 
            Numero_De_Archivos = len(os.listdir(f'img/{self.char_type}/{animation}')) #Me cuenta el numero de archivos por carpetas
            for i in range(Numero_De_Archivos):       #Cantidad de imagenes que quiero tener
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img,(int(img.get_width() * scale), int(img.get_height() * scale))) #Esto me permite ajustar mis imagenes a un tamaño determinado
                temp_lista.append(img)
            self.lista_animaciones.append(temp_lista)     
            # temp_lista = []
            # for i in range(6):       #Cantidad de imagenes que quiero tener
            #     img = pygame.image.load(f'img/{self.char_type}/Movimientos_Derecha/{i}.png')
            #     img = pygame.transform.scale(img,(int(img.get_width() * scale), int(img.get_height() * scale))) #Esto me permite ajustar mis imagenes a un tamaño determinado
            #     temp_lista.append(img)     
            # self.lista_animaciones.append(temp_lista)
        self.image = self.lista_animaciones[self.action][self.frame_index]
        self.rect =  self.image.get_rect() #Esto toma la imagen y nos permite controlar la posicion de todo
        self.rect.center = (x,y)
        self.Width = self.image.get_width()
        self.Height = self.image.get_height()
        
		
    def update(self):
        self.update_animacion()
        self.check_alive()
        #Actualizar enfriamiento 
        if self.shoot_enfriamiento > 0: 
            self.shoot_enfriamiento -= 1
        if self.shoot_a_enfriamiento > 0: 
            self.shoot_a_enfriamiento -= 1   
        if self.shoot_b_enfriamiento > 0: 
            self.shoot_b_enfriamiento -= 1   
        if self.shoot_c_enfriamiento > 0: 
            self.shoot_c_enfriamiento -= 1                
       
       
            
        
    def movimiento(self, Movimiento_Derecha, Movimiento_Izquierda):
        
        
        Pantalla_scroll = 0
        dx = 0  #Posiciones en X , Y
        dy = 0
        
        #Variables de Movimiento para Derecha e Izquierda 
        if Movimiento_Derecha:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if Movimiento_Izquierda:
            dx = -self.speed
            self.flip = True
            self.direction = -1

            
            
        #Saltar 
        if self.jump == True and self.en_aire == False:
            self.velocidad_y = -14 #Altera la distancia de salto
            self.jump = False
            self.en_aire = True
            
        # Declaro la gravedad 
        self.velocidad_y += Gravedad
        if self.velocidad_y > 10:#Limite /  #Velocidad terminal
            self.velocidad_y
        dy += self.velocidad_y   
                
        #Verificacion de colision con el suelo
        # if self.rect.bottom + dy > 300:
        #     dy = 300 - self.rect.bottom 
        #     self.en_aire = False   
            
       
        
        for tile in world.Lista_obstaculos: 
            #Colision en X
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.Width , self.Height):
                dx = 0
                #Colision con pared
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
			#Colisiones en Y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.Width , self.Height):
                #Comprueba si esta debajo del suelo o superficies /  Saltando
                if self.velocidad_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #Comprueba si esta encima del suelo o superficies / cayendo  
                elif self.velocidad_y >= 0:
                    self.velocidad_y = 0
                    self.en_aire = False
                    dy = tile[1].top - self.rect.bottom  
        
        #Colisiones con el Agua
        if pygame.sprite.spritecollide(self, water_group, False):  
            self.Salud = 0 
            
        #Al completar nivel
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True
            
        # Comprobrar si ha caido fuera del mapa    
        if self.rect.bottom > Height:
            self.Salud = 0
            
        #Borde de la pantalla
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > Width:
                dx = 0  
                
        #Actualizar Rectangulo de Posicion
        self.rect.x += dx   
        self.rect.y += dy
        
        #Desplazamiento segun posicion de jugador 
        if self.char_type == 'player':
            if (self.rect.right > Width - Scroll and bg_scroll < (world.level_length * Tile_Size) - Width)\
                or (self.rect.left < Scroll and bg_scroll > abs(dx)):
                self.rect.x -= dx
                Pantalla_scroll = -dx
        
        return Pantalla_scroll, level_complete            
                            
                    
                    
                    
					  
    def shoot(self):      
        if self.shoot_enfriamiento == 0 and self.municion > 0:
            self.shoot_enfriamiento = 20 # Tiempo entre cada Disparo            
                                                  # ⬇️Evita la colision de la bala con el jugador mismo 
            bullet = Bullet(self.rect.centerx + (0.8 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, 'Bullet') #(player.rect.size[0]): me permite hacer el disparo de la bala
            bullet_group.add(bullet)
            self.municion -=1
            shot_fx.play()
            
    
    def shoot_a(self):      
        if self.shoot_a_enfriamiento == 0 and self.municion_a > 0:
            self.shoot_a_enfriamiento = 50 # Tiempo entre cada Disparo            
                                                  # ⬇️Evita la colision de la bala con el jugador mismo 
            bullet = Bullet(self.rect.centerx + (0.8 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, 'Escopeta') #(player.rect.size[0]): me permite hacer el disparo de la bala
            bullet_group.add(bullet)
            self.municion_a -=1    
            shot_fx.play()
    def shoot_b(self):      
        if self.shoot_b_enfriamiento == 0 and self.municion_b > 0:
            self.shoot_b_enfriamiento = 80 # Tiempo entre cada Disparo            
                                                  # ⬇️Evita la colision de la bala con el jugador mismo 
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, 'Fusil') #(player.rect.size[0]): me permite hacer el disparo de la bala
            bullet_group.add(bullet)
            self.municion_b -=1 
            shot_fx.play() 
    def shoot_c(self):      
        if self.shoot_c_enfriamiento == 0 and self.municion_c > 0:
            self.shoot_c_enfriamiento = 6 # Tiempo entre cada Disparo            
                                                  # ⬇️Evita la colision de la bala con el jugador mismo 
            bullet = Bullet(self.rect.centerx + (0.9 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, 'Ametralladora') #(player.rect.size[0]): me permite hacer el disparo de la bala
            bullet_group.add(bullet)
            self.municion_c -=1 
            shot_fx.play()
    
    #IA de Enemigos 
    def ai(self):
        if self.alive and player.alive:
            if self.marcha == False and random.randint (1, 200) == 1: # 1. (1,200) = Numero aleatorio entre 1 y 200  2. 1= Probabilidad 3. Si esta en marcha y se esta ejecuntando random, se cumplira la condicion y la animacion inicial pasa a ser la 0
                self.update_action(0) #Animacion 0 = Idle o Quieto / Primera condicion = inactividad
                self.marcha = True
                self.idling_counter = 50 #Cuenta Regresiva
                #validar si la IA o linea de vision colisiona con el jugador 
            if self.linea_vision.colliderect(player.rect):
                #detener la accion y enfrentar como espartano al jugador 
                self.update_action(0) #Animaccion de inactividad 
                #Atacar sin piedad al jugador
                self.shoot()
            else:    
                if self.marcha == False: #Pone en marcha los enemigos caundo no esten inactivos / Estado no inactivo
                    if not self.direction == 1: #Dirreccion del perosnaje / mirando a la derceha = 1
                        ai_Movimiento_derecha = True
                    else:
                        ai_Movimiento_derecha = False 
                    ai_Movimiento_izquierda = not ai_Movimiento_derecha #Evita que la IA se atasque tratando de moverse en ambas direcciones    
                    self.movimiento(ai_Movimiento_izquierda , ai_Movimiento_derecha) #Introduzco los argumentos
                    self.update_action(1) #Caminar o correr
                    self.move_counter +=1
                    #Actualizo la animacion a medida que el personaje se mueve 
                    self.linea_vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    # pygame.draw.rect(Pantalla, Rosa, self.linea_vision) #Me permite ver el rango de vision 
                    if self.move_counter > Tile_Size:
                        self.direction *= -1
                        self.move_counter *= -1  
                else:  #Si esta inactivo me va a reducir el idling_counter, para que cuando llegue a 0 retome marcha / Cuenta Regresiva
                    self.idling_counter -=1       
                    if self.idling_counter <=0:
                        self.marcha = False
        #scroll
        self.rect.x += Pantalla_scroll      
                    
                        
                          
        
    def  update_animacion(self): 
        #Actualizar tiempo de animacion / Temporizador / Enfriamiento de animacion
        Animation_Cooldown = 100
        #Actualizacion de imagen segun el fotograma
        self.image = self.lista_animaciones[self.action] [self.frame_index]
        #Verificacion de Tiempo
        if pygame.time.get_ticks() - self.update_time > Animation_Cooldown:
           self.update_time = pygame.time.get_ticks()
           self.frame_index += 1
        if self.frame_index >= len(self.lista_animaciones[self.action]):
            if self.action == 3:
                self.frame_index = len(self.lista_animaciones[self.action]) -1 #1.Declaro la funcion de animacion para la muerte y demas 
            else:                                                              #2.Le resto menos uno al conteo para que termine el ciclo en ese punto
                self.frame_index = 0   
            
    
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action  
            #Actualizar animacion  
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks() 
            
    
    def check_alive(self): 
        if self.Salud <=0:
            self.Salud = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
                
        
    def draw(self): #Declaracion de los metodos /  #Me muestra en la ventana ambas declaraciones 
         Pantalla.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) #(pygame.transform.flip(self.image, self.flip, False) me gira la imagen hacia la Izquierda cuando flip sea True y cuando sea Flase se queda igual
         # Pantalla.blit(player2.image, player2.rect) -- Player2 
        #  pygame.draw.rect(Pantalla , Amarillo, self.rect, 1 ) Observa el rectangulo de cada personaje
 
 
# -----------------///---------------///----------///---- 


class World():
    def __init__(self):
        self.Lista_obstaculos = []
     
    def  procesar_datos(self, data):
        self.level_length  = len(data[0])
        #interacciones con los datos de nivel 
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * Tile_Size
                    img_rect.y = y * Tile_Size
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 10: #Segun el numero de cada imagen, selcciono cuales son los obstaculos
                        self.Lista_obstaculos.append(tile_data)
                    elif tile >= 25 and tile <= 26: #Agua
                        water = Water(img, x * Tile_Size, y * Tile_Size)
                        water_group.add(water)
                    elif tile >= 11 and tile <=  16: #Decoracion
                        decoration = Decoration(img, x * Tile_Size, y * Tile_Size)
                        decoration_group.add(decoration)    
                    elif tile == 27: #Crea al player
                        player = Player(100,'player', x * Tile_Size , y * Tile_Size , 2 , 9 , 30 , 5) 
                        barra_salud = Barra_Salud( 940 , 10, player.Salud , player.Salud_maxima)
                    elif tile == 28: #Crea enemigos   
                        Enemigo = Player(100,'enemy', x * Tile_Size , y * Tile_Size, 2 , 2 , 100 , 0) #Uso las mismas propiedades de mi Clase para otros Objetos "Enemigos o Jugadores"    
                        Enemigo_group.add(Enemigo)    
                    elif tile == 17:
                        caja = Caja_de_Articulos ('Ametralladora' , x * Tile_Size , y * Tile_Size )
                        caja_articulos_group.add(caja)
                    elif tile == 18:
                        caja = Caja_de_Articulos ('Municion' , x * Tile_Size , y * Tile_Size  )
                        caja_articulos_group.add(caja)
                    elif tile == 19: 
                        caja = Caja_de_Articulos ('Escopeta' , x * Tile_Size , y * Tile_Size )
                        caja_articulos_group.add(caja)   
                    elif tile == 20: 
                        caja = Caja_de_Articulos ('Fusil' , x * Tile_Size , y * Tile_Size  )
                        caja_articulos_group.add(caja) 
                    elif tile == 21:
                        caja = Caja_de_Articulos ('Granadas' , x * Tile_Size , y * Tile_Size )
                        caja_articulos_group.add(caja)
                    elif tile == 22:
                        caja = Caja_de_Articulos ('Salud50%' , x * Tile_Size , y * Tile_Size  )
                        caja_articulos_group.add(caja)   
                    elif tile == 23:
                        caja = Caja_de_Articulos('Salud', x * Tile_Size , y * Tile_Size ) 
                        caja_articulos_group.add(caja)
                    elif tile == 24: #Exit o Final
                          exit = Exit(img, x * Tile_Size, y * Tile_Size)
                          exit_group.add(exit)                                 
        return player, barra_salud
    
    def draw (self):
        for tile in self.Lista_obstaculos:
            tile[1][0] += Pantalla_scroll
            Pantalla.blit(tile[0], tile[1])    
    
# -----------------///---------------///----------///----   

class Decoration(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + Tile_Size // 2, y + (Tile_Size - self.image.get_height()))

	def update(self):
		self.rect.x += Pantalla_scroll


# -----------------///---------------///----------///----  
 

class Water(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + Tile_Size // 2, y + (Tile_Size - self.image.get_height()))

	def update(self):
		self.rect.x += Pantalla_scroll
 

# -----------------///---------------///----------///----  

class Exit(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + Tile_Size // 2, y + (Tile_Size - self.image.get_height()))

	def update(self):
		self.rect.x += Pantalla_scroll

# -----------------///---------------///----------///----  


class Barra_Salud():
       def __init__(self, x, y, Salud, Salud_maxima ):
        self.x = x
        self.y = y
        self.Salud = Salud
        self.Salud_maxima = Salud_maxima
        
        
       def draw( self, Salud):
           #Actualizar barra de Salud 
           self.Salud = Salud
           #Calculo de relacion con salud 
           ratio = self.Salud / self.Salud_maxima
        
           pygame.draw.rect(Pantalla, Black,(self.x -2, self.y -2 , 120, 15))
           pygame.draw.rect(Pantalla, color_a, (self.x, self.y , 120, 15))
           pygame.draw.rect(Pantalla, color_b, (self.x, self.y , 120 * ratio,  15))
           
 

            
 # -----------------///---------------///----------///---- 
 
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction,Type_bullet):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.Type_bullet = Type_bullet
        self.image = bullet_img[self.Type_bullet]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.flip = False
        
    def update(self): 
       #Movimiento de la Bala / Desplazamiento en X
       self.rect.x += (self.direction * self.speed) + Pantalla_scroll
       #Verificaciones de disparo
       if self.rect.right < 0 or self.rect.left > Width : #Width - 100:
        self.kill()
        #Desaparece la bala luego de ser disparada  
        for tile in world.Lista_obstaculos:
            if tile[1].colliderect(self.rect):
                self.kill()
			
        #Colisiones    
       if pygame.sprite.spritecollide(player, bullet_group, False):
           if player.alive:
              player.Salud -= 10
              self.kill() #Hace desaparcer la bala una vez impacta 
       for Enemigo in Enemigo_group:  #Este ciclo me permite colisionar la bala con el group de enemigos = colisiones con todos los enemigos
            if pygame.sprite.spritecollide(Enemigo, bullet_group, False):
                if Enemigo.alive:
                   Enemigo.Salud -= 25
                   self.kill() #Hace desaparcer la bala una vez impacta 
            
# -----------------///---------------///----------///----
            
class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100 
        self.velocidad_y = -15
        self.speed = 5
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction
        
    def update(self):
        self.velocidad_y += Gravedad
        dx = self.direction * self.speed
        dy = self.velocidad_y
        
        for tile in world.Lista_obstaculos:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                if self.velocidad_y < 0:
                    self.velocidad_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.velocidad_y >= 0:
                    self.velocidad_y = 0
                    dy = tile[1].top - self.rect.bottom    
                
        
        self.rect.x += dx + Pantalla_scroll
        self.rect.y += dy
		    
        #Temporizador de explosion 
        self.timer -= 1
        if self.timer <=0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 1.5 )
            explosion_group.add(explosion)
            #Daño de Explosion / #Ranfo de Explosion
            if abs (self.rect.centerx - player.rect.centerx) < Tile_Size * 2 and \
                abs (self.rect.centery - player.rect.centery) < Tile_Size * 2: #La función Python abs() devuelve el valor absoluto y elimina el signo negativo de un número en Python
                player.Salud -=50
            for Enemigo in Enemigo_group:
                if abs (self.rect.centerx - Enemigo.rect.centerx) < Tile_Size * 2 and \
                    abs (self.rect.centery - Enemigo.rect.centery) < Tile_Size * 2:
                    Enemigo.Salud -=50    
                 

     
 
  # -----------------///---------------///----------///----
 
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        for num in range (1,8):
            img= pygame.image.load(f'img/Explosiones/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width()* scale) , int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0 # Contador
    
    
    def update(self):
        Explosion_speed = 4
        # Actualizar animacion de Explosion
        self.counter += 1
        
        if self.counter >= Explosion_speed: #Si el contador ha excedido este limite de velocidad 
            self.counter = 0  #Reiniciamos el contador 
            self.frame_index += 1 #Aumentamos el indice de fotogramas en uno
            #Si  la animacion esta completa elimine la explosion
            if self.frame_index >= len(self.images): # si es mayor o igual a la longitud de esa lista
                self.kill() #Desagase de esa animacion  
            else: 
                self.image = self.images[self.frame_index]
           

# -----------------///---------------///----------///----  


class Caja_de_Articulos(pygame.sprite.Sprite):
    def __init__(self, type_item, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type_item = type_item  #Tipo de Item
        self.image = caja_articulos[self.type_item]
        self.rect = self.image.get_rect() #rect = rectangulo: El objeto  
        self.rect.midtop = ( x + Tile_Size // 2, y + (Tile_Size - self.image.get_height())) #Posicionamiento de los item en base a los mosaicos (centrado)
    
    
    def update(self):  
        
        self.rect.x += Pantalla_scroll #Evita que los item se muevan 
        #Verificar que el jugador recoja los items (Colision con los items)
        if pygame.sprite.collide_rect(self, player): #Busco una colision entre el rectangulo de elementos y el rectangulo de personaje
            # pass: permite no leer el metodo 
            #Verificamos el tipo de Item 
            if self.type_item == 'Salud':
                player.Salud += 100
                if player.Salud > player.Salud_maxima:
                    player.Salud = player.Salud_maxima
                # print(player.Salud)
            elif self.type_item == 'Salud50%':
                player.Salud += 50
                if player.Salud > player.Salud_maxima:
                    player.Salud = player.Salud_maxima
                # print(player.Salud)
            elif self.type_item == 'Municion':
                player.municion += 25
                # print(player.municion)
            elif self.type_item == 'Escopeta':
                player.municion_a += 10
            elif self.type_item == 'Fusil':
                player.municion_b += 20
            elif self.type_item == 'Ametralladora':
                player.municion_c += 100    
            elif self.type_item == 'Granadas':
                player.grenade += 5
                # print(player.grenade)
            #Elimine el item una vez sea recojido 
            self.kill()  
                       

# -----------------///---------------///----------///----        
        
class IntroFade(): #Posibles mejoras
	def __init__(self, direction, color, speed):
		self.direction = direction
		self.color = color
		self.speed = speed
		self.Contador_desvanecimiento = 0


	def fade(self):
		Desvanecimiento_Completo = False
		self.Contador_desvanecimiento += self.speed
		if self.direction == 1:
			pygame.draw.rect(Pantalla, self.color, (0 - self.Contador_desvanecimiento, 0, Width // 2, Height))
			pygame.draw.rect(Pantalla, self.color, (Width // 2 + self.Contador_desvanecimiento, 0, Width, Height))
			pygame.draw.rect(Pantalla, self.color, (0, 0 - self.Contador_desvanecimiento, Width, Height // 2))
			pygame.draw.rect(Pantalla, self.color, (0, Height // 2 + self.Contador_desvanecimiento, Width, Height))
		if self.direction == 2:
			pygame.draw.rect(Pantalla, self.color, (0, 0, Width, 0 + self.Contador_desvanecimiento))
		if self.Contador_desvanecimiento >= Width:
			Desvanecimiento_Completo = True
		return Desvanecimiento_Completo


intro_fade = IntroFade(1, Black, 4)
death_fade = IntroFade(2, Black, 4)

          
# -----------------///---------------///----------///----     
  
 
#Botones 
start_button = Botones_Inicio.Button(Width // 2 - 350, Height // 2 - 80, start_img, 1)
exit_button = Botones_Inicio.Button(Width  // 2 - 10, Height // 2 - 80 , exit_img, 1)
restart_button = Botones_Inicio.Button(Width  // 2 - 100, Height // 2 - 50, restart_img, 2)

 
 # -----------------///---------------///----------///----    
 
#Grupos de sprites 
Enemigo_group = pygame.sprite.Group()                 
bullet_group = pygame.sprite.Group()  
grenade_group = pygame.sprite.Group()  
explosion_group = pygame.sprite.Group()   
caja_articulos_group = pygame.sprite.Group()   
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
 
# -----------------///---------------///----------///----

#Cantidad de vida, Clase , posiciones en x , y , tamaño de imagen , Velocidad, Municion de balas y granadas     
# player = Player(100,'player',100,300,0.8,5,20,6) #Relaciono con una variable la clase y declaro sus atributos  /aaaaa
# barra_salud = Barra_Salud( 940 , 10, player.Salud , player.Salud_maxima)
# Enemigo = Player(100,'player',400,200,3,3,100,0) #Uso las mismas propiedades de mi Clase para otros Objetos "Enemigos o Jugadores"    
# Enemigo2 = Player(100,'player',500,200,3,3,100,0)
# Enemigo3 = Player(100,'player',600,200,3,3,100,0)

# Enemigo_group.add(Enemigo)     
# Enemigo_group.add(Enemigo2)    
# Enemigo_group.add(Enemigo3) 





# X = 200
# Y = 200
# scale = 0.4



# -----------------///---------------///----------///---

#Lista de Mosaicos 

World_data = []
for row in range (filas):
    r = [-1] * columnas
    World_data.append(r)
    
#Carga de datos / Datos de Nivel 
with open (f'level{level}.csv', newline='' ) as csvfile:
    reader =  csv.reader(csvfile, delimiter=',')  
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            World_data[x][y] = int(tile) 
world = World() 
player, barra_salud = world.procesar_datos(World_data)     
  

# -----------------///---------------///----------///----Seccion donde corre el juego 
# Bucle para mantener la ventana abierta

Run = True
while Run: #Ciclo de Juego
   
    
    clock.tick(FPS)
    
    if Comenzar_Juego == False:
        Pantalla.blit(Fondo_Menu,(0,0))
        if start_button.draw(Pantalla):
            Comenzar_Juego = True
        if exit_button.draw(Pantalla):
            Run = False
		
    else:
        #Dibujo el fondo
        draw_bg()
        #Dibujo el mapa
        world.draw()
        #Barra de Salud
        barra_salud.draw(player.Salud)
        
        #Municion
        draw_text(f'Municion: {player.municion} * ', font, Black, 10, 15 ) #Me dibuja en pantalla la municion que tengo 
        Pantalla.blit(Recargar_Municion_img, (200 , 15)) #1.Posicion en x mas x * 10 2. Posicion en Y  
        #Municion
        draw_text(f'Granadas: {player.grenade} * ' , font, Black, 310, 13 )
        Pantalla.blit(corazon_icons, (933, 2))
        Pantalla.blit(granada_icons, (500 , 15))
        
         
         
        player.draw() 
        player.update()
       
        for Enemigo in Enemigo_group:
            Enemigo.ai()
            Enemigo.update()
            Enemigo.draw()
        
       
        explosion_group.draw(Pantalla)
        caja_articulos_group.draw(Pantalla)
        grenade_group.draw(Pantalla)
        decoration_group.draw(Pantalla)
        water_group.draw(Pantalla)
        exit_group.draw(Pantalla)
        bullet_group.draw(Pantalla)    
      
       
       
       
        bullet_group.update()
        grenade_group.update()
        explosion_group.update()
        caja_articulos_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        
       

        if shoot_a:                                 
            player.shoot_a()
        if shoot_b:                                 
            player.shoot_b()
        if shoot_c:                                 
            player.shoot_c() 
            
        if Intro == True:
            if intro_fade.fade():
                Intro = False
                intro_fade.Contador_desvanecimiento = 0   
        
        if player.alive:
            #Shoot Bullet 
            if shoot:                                 
                player.shoot()
            elif grenade and grenade_lanzada == False and player.grenade > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction*1.8),\
                                player.rect.top, player.direction*1.8)
                grenade_group.add(grenade)
                player.grenade -= 1
                grenade_lanzada = True
                # print(player.grenade)
            if player.en_aire:
                player.update_action(2)#2: Salto
            elif Movimiento_Derecha or Movimiento_Izquierda:
                player.update_action(1) #1 : Movimientos/Caminar
            else:
                player.update_action(0)#0 : Idle
            Pantalla_scroll, level_complete =  player.movimiento(Movimiento_Derecha, Movimiento_Izquierda)   
            bg_scroll -= Pantalla_scroll
            
         
            #Nivel completado
            if level_complete:
                Intro = True
                level += 1
                bg_scroll = 0
                World_data = reset_level()
                if level <= max_levels:
                    #Cargo niveles y crea los mundo
                    with open (f'level{level}.csv', newline='' ) as csvfile:
                        reader =  csv.reader(csvfile, delimiter=',')  
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                World_data[x][y] = int(tile) 
                    world = World() 
                    player, barra_salud = world.procesar_datos(World_data)  	
        else:  
            Pantalla_scroll = 0
            if death_fade.fade():
                if restart_button.draw(Pantalla):
                    death_fade.Contador_desvanecimiento = 0
                    Intro = True
                    bg_scroll = 0
                    world_data = reset_level()
                    #Cargo niveles y crea los mundo
                    with open (f'level{level}.csv', newline='' ) as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')  
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)   
                    world = World() 
                    player, barra_salud = world.procesar_datos(World_data)  	
                         
                    
    for event in pygame.event.get(): #Declaracion de eventos en Pygame
        #Quitar Juego
        if event.type == pygame.QUIT:
            Run = False
            
        #Evento al presionar los botones 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                Movimiento_Derecha = True  
            if event.key == pygame.K_LEFT:
                Movimiento_Izquierda = True
            if event.key == pygame.K_UP and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                Run = False  
            #---- // ---- // ---- // ----- // --- Shoots    
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_a:
                shoot_a = True    
            if event.key == pygame.K_s:
                shoot_b = True   
            if event.key == pygame.K_d:
                shoot_c = True         
            #---- // ---- // ---- // ----- // --- Grenades 
            if event.key == pygame.K_q:
                grenade = True
            
            
    
                
        #Evento al soltar los botones 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                Movimiento_Derecha = False  
            if event.key == pygame.K_LEFT:
                Movimiento_Izquierda = False  
        #---- // ---- // ---- // ----- // --- Shoots        
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_a:
                shoot_a = False   
            if event.key == pygame.K_s:
                shoot_b = False    
            if event.key == pygame.K_d:
                shoot_c = False    
        #---- // ---- // ---- // ----- // --- Grenades 
            if event.key == pygame.K_q:
                grenade = False
                grenade_lanzada = False
    pygame.display.update()       
            

pygame.quit()

#Continuar las Pruebas
#Cambios: 1.Agrege nuevos botones = w
#2. Agregeue la bala como diccionario 
#3. Agregue un nuevo item con condicion = Escopeta 
#4. Shot_a


