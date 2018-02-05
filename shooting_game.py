import pygame, sys, os, random

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# set screen
WIDTH = 360
HEIGHT = 480
FPS = 60
# initialisation
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('shoot')
clock = pygame.time.Clock()

pygame.mixer.music.load(r'C:\Users\LUCAS\Google 云端硬盘\无聊捣鼓\my_pygame\plane\Aria.mp3')
pygame.mixer.music.set_volume(0.25)

shoot_sound = pygame.mixer.Sound(r'C:\Users\LUCAS\Google 云端硬盘\无聊捣鼓\my_pygame\plane\Laser_Shoot.wav')
shoot_sound.set_volume(0.05)

restart_font = pygame.font.SysFont(None, 30)
score_font = pygame.font.SysFont(None, 30)

class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'C:\Users\LUCAS\Google 云端硬盘\无聊捣鼓\my_pygame\plane\universe.jpg').convert()
        self.image = pygame.transform.scale(self.image, (360, 3280))# 2593*23624
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -self.rect.height + HEIGHT
        self.speedy = 2
        self.font = pygame.font.Font(None, 50)
        self.font2 = pygame.font.Font(None, 100)
        self.txt = ''
        self.txt2 = ''
    def update(self):
        self.rect.y += self.speedy
        if self.rect.y >= 0:
            self.speedy = 0
            self.image = pygame.Surface((WIDTH, HEIGHT))
            self.rect = self.image.get_rect()
            self.image.fill(BLACK, self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'C:\Users\LUCAS\Google 云端硬盘\无聊捣鼓\my_pygame\plane\bullet.png').convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -8
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'C:\Users\LUCAS\Google 云端硬盘\无聊捣鼓\my_pygame\plane\aircraft.png').convert()
        self.image = pygame.transform.scale(self.image, (70,50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT
        self.speedx = 0
        self.speedy = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top + 10)
        bullet_group.add(bullet)
        all_sprite.add(bullet)
        shoot_sound.play()
    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y > HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height
        if self.rect.y < 0:
            self.rect.y = 0
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # shoot
# TODO: 制作敌人，石头，要求大小不一
mob_images = []
for i in range(3):
    name = r'C:\Users\LUCAS\Google 云端硬盘\无聊捣鼓\my_pygame\plane\spaceMeteors_00{}.png'.format(i+1)
    mob_images.append(pygame.image.load(name).convert())
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(mob_images)
        self.rect = self.image.get_rect()
        self.scale = random.randrange(20, 45)/100
        self.image = pygame.transform.scale(self.image, (int(self.rect.width * self.scale), int(self.rect.height * self.scale)))
        self.image.set_colorkey(BLACK)
        self.image_copy = self.image.copy()
        self.rect.x = random.randrange(0, WIDTH)
        self.rect.y = random.randrange(-900, -100)
        self.speedy = random.randrange(4, 6)
        self.speedx = random.randrange(-2, 2)
        self.rot = 0
        self.rotspeed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
    def reborn(self):
        self.rect.y = random.randrange(-500, -100)
        self.rect.x = random.randrange(0, WIDTH)
        self.speedy = random.randrange(4, 6)
        self.speedx = random.randrange(-2, 2)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rotspeed) % 360
            new_image = pygame.transform.rotate(self.image_copy, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.y > HEIGHT:
            self.reborn()
        if self.rect.x > WIDTH or self.rect.x < -self.rect.width:
            self.reborn()
        self.rotate()


running = True

# Creating groups for all and mobs
all_sprite = pygame.sprite.Group()
bgs = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

bg = Background()
player = Player()

bgs.add(bg)
all_sprite.add(player)
# creating 5 mob
for i in range(8):
    stone = Mob()
    all_sprite.add(stone)
    mobs.add(stone)

pygame.mixer.music.play(loops=-1, start=10.2)

loop = False
last_time = 0

# game loop
while running:
    clock.tick(FPS)
    time = pygame.time.get_ticks()/1000 - last_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    hits = pygame.sprite.groupcollide(mobs, bullet_group, True, True)
    # Spown mobs to 8
    while len(mobs) < 8:
        stone = Mob()
        all_sprite.add(stone)
        mobs.add(stone)

    # detect collide of mob and plane
    for mob in mobs:
        hits = pygame.sprite.collide_mask(player, mob)
        if hits:
            running = False
    # Restarts:
    if running == False:
        pygame.mixer.music.pause()
        loop = True
        black = pygame.Surface((WIDTH, HEIGHT))
        black.fill(BLACK)
        text = 'Resart?[r]  Quit?[q]'
        restart = restart_font.render(text, 1, WHITE)
        screen.blit(restart, (WIDTH/2 - 100, HEIGHT/2 - 100))
        pygame.display.flip()

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        running = True
                        last_time = pygame.time.get_ticks()/1000

                        pygame.mixer.music.rewind()
                        pygame.mixer.music.play(loops = -1, start=10.2)

                        for item in all_sprite:
                            item.kill()
                        bg.kill()
                        bgs.remove()
                        mobs.remove()
                        all_sprite.remove()
                        player = Player()
                        all_sprite.add(player)
                        for i in range(8):
                            stone = Mob()
                            all_sprite.add(stone)
                            mobs.add(stone)
                        bg = Background()
                        bgs.add(bg)
                    elif event.key == pygame.K_q:
                        running = False
                        loop = False
                elif event.type == pygame.QUIT:
                    quit = True
                    loop = False

    #update：所有的update必须长一样。
    all_sprite.update()
    bg.update()
    # draw
    bgs.draw(screen)
    if bg.rect.y >= 0:
        for i in range(4):
            mob = Mob()
            mobs.add(mob)
            all_sprite.add(mob)
        bg.txt = bg.font.render('Why are you still...', 1, WHITE)
        bg.txt2 = bg.font2.render('HERE?', 1, RED)
        screen.blit(bg.txt, (20, 130))
        screen.blit(bg.txt2, (30, 200))
    score_text = 'Time :{}'.format(str(round(time, 2)))
    score = score_font.render(score_text, 1, WHITE)
    all_sprite.draw(screen)
    screen.blit(score, (10,10))
    # flip
    pygame.display.flip()


pygame.quit()
