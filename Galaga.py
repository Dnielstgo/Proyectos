import pygame, random

# Configuración del juego
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaga")
clock = pygame.time.Clock()

# Grupos globales
all_sprites = None
bullets = None

# Funciones de texto y barras
def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont("serif", size)
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    surface.blit(surf, rect)

def draw_multiline_text(surface, lines, size, x, start_y, line_space=10, color=WHITE):
    font = pygame.font.SysFont("serif", size)
    total_h = len(lines) * size + (len(lines) - 1) * line_space
    y = start_y - total_h // 2
    for line in lines:
        surf = font.render(line, True, color)
        rect = surf.get_rect(center=(x, y))
        surface.blit(surf, rect)
        y += size + line_space

def draw_shield_bar(surface, x, y, pct):
    BAR_L, BAR_H = 100, 10
    fill = (pct / 100) * BAR_L
    pygame.draw.rect(surface, GREEN, (x, y, fill, BAR_H))
    pygame.draw.rect(surface, WHITE, (x, y, BAR_L, BAR_H), 2)

# Niveles y mensajes
LEVELS = {
    'easy':   {'count': 7,  'speed_min': 1,  'speed_max': 5,  'name': 'Tierra inocente'},
    'medium': {'count': 10, 'speed_min': 2,  'speed_max': 9,  'name': 'Tierra en guerra '},
    'hard':   {'count': 18, 'speed_min': 4,  'speed_max': 17, 'name': 'Tierra condenada'},
}

VICTORY_MSG = {
    'easy': [
        "Al investigar la señal, descubre que los alienígenas ",
        "estaban intentando atraer a más de los suyos.",
        "Tenía poco tiempo. Con ayuda de su IA, ",
        "localiza tres transmisores: África, Pacífico, Himalaya.",
        "Con los nodos destruidos, la amenaza desaparece. ",
        "La Tierra, aún inocente, nunca supo del peligro.",
        "El Viajero deja una baliza defensiva y desaparece entre las estrellas."
    ],
    'medium': [
        "La Arklight queda dañada. Deben defender",
        " el núcleo y preparar el asalto final.",
        "Usando tecnología robada, mejora sus ",
        "armas y lanza una misión suicida.",
        "Recorre túneles, combate en naves y",
        " destruye el último núcleo en órbita baja.",
        "La red colapsa. El cielo se limpia. La humanidad ve las estrellas.",
        "El Viajero parte en silencio. La guerra continúa, pero hay esperanza."
    ],
    'hard': [
        "El Viajero sobrevive y llega al Nexo, ",
        "una estructura viva en el corazón del planeta.",
        "No puede salvar la Tierra, pero sí destruir al enemigo.",
        "Activa el colapso gravitacional: él y la nave se funden con el Nexo.",
        "Explosión cuántica aniquila la red enemiga en todo el sistema.",
        "En un satélite lejano, una sonda capta: 'Tierra caída. Invasión neutralizada.'"
    ]
}

# Carga de recursos
fondo           = pygame.image.load("Fondo.jpg").convert()
fondo_tierra_1  = pygame.image.load("tierra_inocente.jpg").convert()
fondo_tierra_2  = pygame.image.load("tierra_guerra.jpg").convert()
fondo_tierra_3  = pygame.image.load("tierra_condenada.jpg").convert()
fondo_perder    = pygame.image.load("fondo_perder.jpg").convert()
laser_sound     = pygame.mixer.Sound("assets_laser.ogg")
explosion_sound = pygame.mixer.Sound("assets_explosion.wav")
pygame.mixer.music.set_volume(2)

enemy_images = []
for f in ["enemy_1.png","enemy_3.png","enemy_5.png",
          "enemy_6.png","enemy_7.png","enemy_11.png",
          "enemy_22.png"]:
    img = pygame.image.load(f).convert()
    img.set_colorkey(BLACK)
    enemy_images.append(img)

explosion_anim = []
for i in range(9):
    im = pygame.image.load(f"0{i}.png").convert()
    im.set_colorkey(BLACK)
    explosion_anim.append(pygame.transform.scale(im, (70, 70)))

# Clases de sprites
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player_1.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(midbottom=(WIDTH//2, HEIGHT-10))
        self.speed_x = 0
        self.shield = 100

    def update(self):
        self.speed_x = 0
        ks = pygame.key.get_pressed()
        if ks[pygame.K_LEFT]: self.speed_x = -5
        if ks[pygame.K_RIGHT]: self.speed_x = 5
        self.rect.x += self.speed_x
        self.rect.clamp_ip(screen.get_rect())

    def shoot(self):
        global all_sprites, bullets
        b = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(b); bullets.add(b)
        laser_sound.play()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(enemy_images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(speed_min, speed_max)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speedx *= -1
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(speed_min, speed_max)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("laser_1.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=(x, y))
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0: self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect(center=center)
        self.frame = 0
        self.last = pygame.time.get_ticks()
        self.rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last > self.rate:
            self.last = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect(center=center)

# Pantallas y utilidades
def wait_for_key(specific=None):
    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            if e.type == pygame.KEYUP and (specific is None or e.key == specific):
                return

def show_title():
    screen.blit(fondo, (0, 0))
    draw_text(screen, "GALAGA", 80, WIDTH//2, HEIGHT//4)
    draw_text(screen, "Presiona cualquier tecla", 30, WIDTH//2, HEIGHT//2)
    pygame.display.flip()
    wait_for_key()

def show_story():
    pygame.mixer.music.load("starman.wav")
    pygame.mixer.music.play()
    parts = [
        [
            "En el año 2189, la Tierra envió una señal de auxilio al cosmos.",
            "Fue un grito de desesperación, no un mensaje de paz.",
            "Desde una estrella lejana, un Starman escuchó.",
            "Sin nombre ni origen conocido, ",
            "descendió en la Arklight para proteger la vida."
        ],
        [
            "Pero algo falló: la Tierra lo marcó como amenaza.",
            "Otra fuerza oscura entró al sistema solar.",
            "El tiempo se fracturó: ",
              "Tierra inocente  ",
              "Tierra en guerra",
                      "Tierra condenada.",
            "El Starman cae… no como salvador, sino último guardián."
        ]
    ]
    for lines in parts:
        screen.fill(BLACK)
        draw_multiline_text(screen, lines, 28, WIDTH//2, HEIGHT//2)
        draw_text(screen, "Presiona una tecla...", 20, WIDTH//2, HEIGHT-50)
        pygame.display.flip()
        wait_for_key()

def show_difficulty():
    global fondo 
    screen.blit(fondo, (0, 0))
    draw_text(screen, "Selecciona dificultad:", 50, WIDTH//2, HEIGHT//4)
    draw_text(screen, "A - Tierra inocente", 35, WIDTH//2, HEIGHT//2-30)
    draw_text(screen, "B - Tierra en guerra", 35, WIDTH//2, HEIGHT//2)
    draw_text(screen, "C - Tierra condenada", 35, WIDTH//2, HEIGHT//2+30)
    pygame.display.flip()
    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_a:
                    fondo = fondo_tierra_1
                    pygame.mixer.music.stop()
                    return 'easy'
                if e.key == pygame.K_b:
                    fondo = fondo_tierra_2
                    pygame.mixer.music.stop()
                    return 'medium'
                if e.key == pygame.K_c:
                    fondo = fondo_tierra_3
                    pygame.mixer.music.stop()
                    return 'hard'
        pygame.display.flip()

def show_victory(level):
    screen.blit(fondo, (0, 0))
    draw_text(screen, "¡VICTORIA!", 50, WIDTH//2, HEIGHT/5)
    draw_multiline_text(screen, VICTORY_MSG[level], 24, WIDTH//2, HEIGHT//2)
    draw_text(screen, "Presiona R para cambiar dificultad", 20, WIDTH//2, HEIGHT-50)
    pygame.display.flip()
    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            if e.type == pygame.KEYUP and e.key == pygame.K_r:
                return

def show_failure(score):
    screen.blit(fondo_perder, (0, 0))
    draw_text(screen, "FALLASTE EN TU MISIÓN", 64, WIDTH//2, HEIGHT//4)
    draw_text(screen, f"Puntos: {score}", 36, WIDTH//2, HEIGHT//2)
    draw_text(screen, "Presiona R para cambiar dificultad", 22, WIDTH//2, HEIGHT-50)
    pygame.display.flip()
    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            if e.type == pygame.KEYUP and e.key == pygame.K_r:
                return

# Bucle principal
def main():
    show_title()
    show_story()
    while True:
        difficulty = show_difficulty()
        params = LEVELS[difficulty]
        global speed_min, speed_max, all_sprites, bullets
        speed_min, speed_max = params['speed_min'], params['speed_max']

        pygame.mixer.music.load("assets_music.ogg")
        pygame.mixer.music.play(-1)

        all_sprites = pygame.sprite.Group()
        bullets     = pygame.sprite.Group()
        enemies     = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)
        for _ in range(params['count']):
            e = Enemy()
            all_sprites.add(e); enemies.add(e)

        score = 0
        game_over = False
        victory   = False

        while not game_over:
            clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); return
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    player.shoot()

            all_sprites.update()

            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for h in hits:
                score += 10
                explosion_sound.play()
                ex = Explosion(h.rect.center)
                all_sprites.add(ex)
                ne = Enemy(); all_sprites.add(ne); enemies.add(ne)

            hits = pygame.sprite.spritecollide(player, enemies, True)
            for h in hits:
                player.shield -= 25
                ne = Enemy(); all_sprites.add(ne); enemies.add(ne)
                if player.shield <= 0:
                    pygame.mixer.music.stop()
                    game_over = True

            if score >= 500:
                pygame.mixer.music.stop()
                victory = True
                game_over = True

            screen.blit(fondo, (0, 0))
            all_sprites.draw(screen)
            draw_text(screen, str(score), 25, WIDTH//2, 10)
            draw_shield_bar(screen, 5, 5, player.shield)
            pygame.display.flip()

        if victory:
            show_victory(difficulty)
        else:
            show_failure(score)

if __name__ == "__main__":
    main()