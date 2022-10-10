from pygame import *
import pygame
import random
from os import path
from time import *
#-------------------------------------------------------------------

img_dir = path.join(path.dirname(__file__), 'img')
#-------------------------------------------------------------
WIDTH = 700
HEIGHT = 500
FPS = 60
#---------------------------------------------------------------------------
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
#----------------------------------------------------
# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shuter")
clock = pygame.time.Clock()
#---------------------------------------------------------------------------
font_name = pygame.font.match_font('arial')
#-------------------------------------------------------
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
#---------------------------------------------------------------------------
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
#--------------------------------------------------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        

    def update(self):
        
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1500:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx =  8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        sound.set_volume(0.5)
        sound.play()
        
    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
#--------------------------------------------------------        
#Создаем класс для метеорита
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)               

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)

#Создаем клас врага--------------------------------------------------------
class Ufo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ufo_img, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)
 
#---------------------------------------------
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()
            #sound.stop()
#-------------------------------------------------------------
# Загрузка спрайтов
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect() 
player_img = pygame.image.load(path.join(img_dir, "Player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
meteor_img = pygame.image.load(path.join(img_dir, "Meteor.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laser.png")).convert()
ufo_img = pygame.image.load(path.join(img_dir, "Enemy.png")).convert()
#  bonus = pygame.image.load(path.join(img_dir, "powerupYellow_bolt.png")).convert()

#---------------------------------------
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
Lifes = 3
all_sprites.add(player)
#-----------------------------------------------------------------
for i in range(2):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    
for i in range(2):
    m = Ufo()
    all_sprites.add(m)
    mobs.add(m)

#----------------------------------------
mixer.init()
mixer.music.load("space.ogg")
sound = mixer.Sound("sfx_laser2.ogg")
sound_1 = mixer.Sound("sfx_laser2.ogg")
mixer.music.play()
# Цикл игры

score = 0
#---------------------------------------------------
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Обновление
    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 1
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 1
        m = Ufo()
        all_sprites.add(m)
        mobs.add(m)
        
     #Проверка, не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, mobs, False) 
    if hits:
        sound_1.set_volume(1.5)
        sound_1.play()
        player.hide()
        player.lives -= 1      
        
    if score != 50:
        runnig = True
    else:
        runnig = False
    
    if player.lives == 0:
        running = False
        
    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    
    #draw_text(screen, str(Win_Text), 50, WIDTH / 2, 50)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_lives(screen, WIDTH - 100, 5, player.lives,
               player_mini_img)
    
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
