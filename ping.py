import pygame
import random

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
back = (200, 255, 255)
win_width = 600
win_height = 500
pygame.display.set_caption("Ping-Pong")
window = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fuente para el puntaje
font = pygame.font.Font(None, 36)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        pygame.sprite.Sprite.__init__(self)
        try:
            # Intentar cargar la imagen
            self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
        except:
            # Si no se puede cargar la imagen, crear un rectángulo de color
            self.image = pygame.Surface((size_x, size_y))
            if "ball" in player_image.lower():
                self.image.fill(RED)
            else:
                self.image.fill(WHITE)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_l(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed
    
    def update_r(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, ball_image, ball_x, ball_y, size_x, size_y, speed_x, speed_y):
        super().__init__(ball_image, ball_x, ball_y, size_x, size_y, 0)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.base_speed = 4  # Velocidad base
        self.max_speed = 12  # Velocidad máxima
    
    def update(self):
        # Mover la pelota
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Rebote en bordes superior e inferior
        if self.rect.y <= 0 or self.rect.y >= win_height - self.rect.height:
            self.speed_y = -self.speed_y
    
    def increase_speed(self):
        # Incrementar velocidad gradualmente con cada golpe
        if abs(self.speed_x) < self.max_speed:
            if self.speed_x > 0:
                self.speed_x += 0.5
            else:
                self.speed_x -= 0.5
    
    def reset_ball(self):
        self.rect.x = win_width // 2
        self.rect.y = win_height // 2
        self.speed_x = random.choice([-self.base_speed, self.base_speed])
        self.speed_y = random.choice([-self.base_speed, self.base_speed])

# Crear los objetos del juego
player1 = Player("paddle1.png", 30, win_height // 2 - 50, 20, 100, 5)
player2 = Player("paddle2.png", win_width - 50, win_height // 2 - 50, 20, 100, 5)
ball = Ball("ball.png", win_width // 2, win_height // 2, 20, 20, 4, 4)

# Puntajes
score1 = 0
score2 = 0

game = True
while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
    
    # Actualizar jugadores
    player1.update_l()
    player2.update_r()
    
    # Actualizar pelota
    ball.update()
    
    # Detectar colisiones con las paletas
    if ball.rect.colliderect(player1.rect):
        ball.speed_x = abs(ball.speed_x)  # Asegurar que vaya hacia la derecha
        # Añadir efecto según donde golpee la paleta
        hit_pos = (ball.rect.centery - player1.rect.centery) / (player1.rect.height / 2)
        ball.speed_y = hit_pos * 4
        ball.increase_speed()  # Incrementar velocidad con cada golpe
    
    if ball.rect.colliderect(player2.rect):
        ball.speed_x = -abs(ball.speed_x)  # Asegurar que vaya hacia la izquierda
        # Añadir efecto según donde golpee la paleta
        hit_pos = (ball.rect.centery - player2.rect.centery) / (player2.rect.height / 2)
        ball.speed_y = hit_pos * 4
        ball.increase_speed()  # Incrementar velocidad con cada golpe
    
    # Detectar puntos
    if ball.rect.x < 0:
        score2 += 1
        ball.reset_ball()
    elif ball.rect.x > win_width:
        score1 += 1
        ball.reset_ball()
    
    # Dibujar todo
    window.fill(back)
    
    # Dibujar línea central
    pygame.draw.line(window, WHITE, (win_width // 2, 0), (win_width // 2, win_height), 5)
    
    # Dibujar sprites
    player1.reset()
    player2.reset()
    ball.reset()
    
    # Dibujar puntajes
    score_text1 = font.render(str(score1), True, WHITE)
    score_text2 = font.render(str(score2), True, WHITE)
    window.blit(score_text1, (win_width // 4, 50))
    window.blit(score_text2, (3 * win_width // 4, 50))
    
    # Mostrar controles y velocidad
    controls_text = pygame.font.Font(None, 24).render("Jugador 1: W/S  |  Jugador 2: ↑/↓", True, WHITE)
    speed_text = pygame.font.Font(None, 24).render(f"Velocidad: {abs(ball.speed_x):.1f}", True, WHITE)
    window.blit(controls_text, (win_width // 2 - 150, win_height - 50))
    window.blit(speed_text, (win_width // 2 - 60, win_height - 25))
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
