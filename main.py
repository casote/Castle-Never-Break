import pygame
import math
from enemy import Enemy

pygame.init()

# ----------Game window setup

screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('The Castle Never Break')

clock = pygame.time.Clock()
fps = 30

#----clouds iterator

c_i = 0

#-----------Colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ----------Assets

#----Castle

#bg_comp = pygame.image.load('assets/grassy mountains parallax background/Grassy_Mountains_preview_fullcolor.png').convert_alpha()
bg_layer1 = pygame.image.load('assets/grassy mountains parallax background/layers/clouds_front.png').convert_alpha()
bg_layer2 = pygame.image.load('assets/grassy mountains parallax background/layers/clouds_mid.png').convert_alpha()
bg_layer3 = pygame.image.load('assets/grassy mountains parallax background/layers/far_mountains.png').convert_alpha()
bg_layer4 = pygame.image.load('assets/grassy mountains parallax background/layers/grassy_mountains.png').convert_alpha()
bg_layer5 = pygame.image.load('assets/grassy mountains parallax background/layers/hill.png').convert_alpha()
bg_layer6 = pygame.image.load('assets/grassy mountains parallax background/layers/sky.png').convert_alpha()

Bg2 = pygame.transform.scale(bg_layer2, (screen_width, screen_height))
Bg3 = pygame.transform.scale(bg_layer3, (screen_width, screen_height))
Bg4 = pygame.transform.scale(bg_layer4, (screen_width, screen_height))
Bg5 = pygame.transform.scale(bg_layer5, (screen_width, screen_height))
Bg6 = pygame.transform.scale(bg_layer6, (screen_width, screen_height))

Bg_front = pygame.transform.scale(bg_layer1, (screen_width, screen_height))
bg_layer2 = pygame.transform.scale(bg_layer2, (screen_width, screen_height))
bg_layer3 = pygame.transform.scale(bg_layer3, (screen_width, screen_height))
bg_layer4 = pygame.transform.scale(bg_layer4, (screen_width, screen_height))
bg_layer5 = pygame.transform.scale(bg_layer5, (screen_width, screen_height))
bg_layer6 = pygame.transform.scale(bg_layer6, (screen_width, screen_height))

Bg_front.set_alpha(128) # "change opacity"

castle_healthy = pygame.image.load('assets/castle/png/Asset 24.png').convert_alpha()
# castle_breaking = pygame.image.load('assets/castle/png/Asset 22.png').convert_alpha()
# castle_fully_destroyed = pygame.image.load('assets/castle/png/Asset 23.png').convert_alpha()

#----Cannon

bullet_asset = pygame.image.load('assets/cannon/shoot2.png').convert_alpha()
b_w = bullet_asset.get_width()
b_h = bullet_asset.get_height()
bullet_asset = pygame.transform.scale(bullet_asset, (int(b_w * 1.5), int(b_h * 1.5)))

#----Enemys

enemy_animations = []
enemy_types = ['skeleton']
enemy_health = [100]

animation_types = ['walk', 'attack', 'death']

for enemy in enemy_types:

    #load animation
    animation_list = []
    for animation in animation_types:

        ##reset sprites list

        temp_list = []

        #define number of frames
        num_of_frames = 6
        for f_i in range(num_of_frames):
            assets = pygame.image.load(f'assets/monsters/{enemy}/{animation}/{f_i}.png').convert_alpha()
            e_w = assets.get_width()
            e_h = assets.get_height()
            assets = pygame.transform.scale(assets, (int(e_w * 2), int(e_h * 2)))
            temp_list.append(assets)
        animation_list.append(temp_list)
    enemy_animations.append(animation_list)

# ----------Class

#----Castle

class Castle():
    def __init__(self, cas_100, x, y, scale):
        self.health = 999
        self.max_health = self.health
        self.fired = False
        width = cas_100.get_width()
        height = cas_100.get_height()

        self.cas_100 = pygame.transform.scale(cas_100, (int(width * scale), int(height * scale)))
        self.rect = self.cas_100.get_rect()
        self.rect.x = x
        self.rect.y = y

    def shoot(self):
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.midleft[0]
        y_dist = -(pos[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

#---Get mouse clicks
        if pygame.mouse.get_pressed()[0] and self.fired == False:
            self.fired = True
            bullet2 = Bullet(bullet_asset, self.rect.midleft[0], self.rect.midleft[1], self.angle)
            bullet_comp.add(bullet2)
            #pygame.draw.line(screen, BLACK, (self.rect.midleft[0], self.rect.midleft[1]), (pos))

        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False


    def draw(self):
        self.image = self.cas_100
        screen.blit(self.image, self.rect)

#----Bullets

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle)
        self.speed = 10
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle) * self.speed)

    def update(self):
        #----Bullets gone out the sceen
        if self.rect.right < 0 or self.rect.left > screen_width or self.rect.bottom < 0 or self.rect.top > screen_height:
            self.kill()

        self.rect.x += self.dx
        self.rect.y += self.dy

cas_comp = Castle(castle_healthy, screen_width - 310, screen_height - 350, 0.3)

bullet_comp = pygame.sprite.Group()
enemy_comp = pygame.sprite.Group()

#create enemies


enemy_1 = Enemy(enemy_health[0], enemy_animations[0], 200, screen_height - 220, 1)
enemy_comp.add(enemy_1)

#----------Game loop

run = True
while run:
    clock.tick(fps)

#----------Raise Assets

    c_i += 0.1
    screen.blit(bg_layer6, (0, 0))
    screen.blit(bg_layer2, (0, 0))
    screen.blit(bg_layer3, (0, 0))
    screen.blit(bg_layer4, (0, 0))
    screen.blit(bg_layer5, (0, 0))

    cas_comp.draw()
    cas_comp.shoot()

    bullet_comp.update()
    bullet_comp.draw(screen)

    # draw enemies
    enemy_comp.update(screen, cas_comp, bullet_comp)

    screen.blit(Bg_front, (-960 + c_i, 0))
    screen.blit(Bg_front, (960 + c_i, 0))
    screen.blit(Bg_front, (2880 + c_i, 0))

#    print(bullet_comp)
#    print(c_i) #clouds interator need to be polished

#----------event handler

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

#----------Update display

    pygame.display.update()

pygame.quit()
