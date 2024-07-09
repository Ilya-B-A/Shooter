import pygame
import pygame_menu
from random import randint
import time

pygame.init()

window = pygame.display.set_mode((700, 600))
pygame.display.set_caption('Space Fight')
bake = pygame.transform.scale(pygame.image.load('bakgraund.jpeg'), (700, 600))

clock = pygame.time.Clock()


class GameSprit(pygame.sprite.Sprite):
    def __init__(self, image, x, y, w, h, speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def resise(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprit):
    def update(self):
        keys_pressed = pygame.key.get_pressed()
        if (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]) and self.rect.x <= 625:
            self.rect.x += self.speed
        if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]) and self.rect.x >= 10:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 30, 3)
        bullets.add(bullet)

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

class Enemy(GameSprit):
    def update(self):
        if self.rect.y <= 600:
            self.rect.y += self.speed
            global lost
            global n
        else:
            self.rect.x = randint(0, 600)
            self.rect.y = 0
            self.speed = randint(1, 2)
            lost += 1
            hearts.sprites()[n].kill()
            n += 1

class Bullet(GameSprit):
    def update(self):
        if self.rect.y < 0:
            self.kill()
        self.rect.y -= self.speed

enemys = pygame.sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(0, 600), 0, 65, 50, randint(1, 2))
    enemys.add(enemy)
bullets = pygame.sprite.Group()
player = Player('rocket.png', 330, 500, 65, 90, 5)
font = pygame.font.SysFont('Arial', 30)
title_lose = font.render('Пропущено: 0', True, (255, 255, 255))
asteroid = Bullet('asteroid.png', randint(0, 600), 0, 90, 90, -1)

font2 = pygame.font.SysFont('Arial', 30)
counter = font2.render('Сбито: 0', True, (255, 255, 255))

font3 = pygame.font.SysFont('Arial', 60)
defit = font3.render('Поражение', True, (255, 255, 255))

font4 = pygame.font.SysFont('Arial', 60)
victory = font4.render('Победа', True, (255, 255, 255))

font5 = pygame.font.SysFont('Arial', 15)
recharge = font5.render('Перезарядка', True, (255, 255, 255))

hearts = pygame.sprite.Group()
x = 570

shot = pygame.mixer.Sound('fire.ogg')
shot.set_volume(0.2)

i = 0
lost = 0
fire_clip = 0
fire_not = True
y = False
n = -3
recharge2 = False

clock = pygame.time.Clock()
def main():
    pygame.mixer.music.load('fight.ogg')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.2)
    global stop
    global counter
    global n
    x = 570
    n = -3
    global y
    global i
    global fire_not
    global fire_clip
    global lost
    global recharge
    global clock
    global enemys
    global bullets
    global hearts
    global title_lose
    global asteroid
    global recharge2
    recharge = False
    asteroid.rect.y = 0
    asteroid.rect.x = randint(0, 600)
    for i in range(3):
        heart = GameSprit('heart.png', x, 10, 35, 35, 0)
        x += 40
        hearts.add(heart)

    enemys.empty()
    bullets.empty()
    player.rect.x = 335
    player.rect.y = 500
    lost = 0
    i = -15
    y = True
    stop = False
    fire_clip = 0
    fire_not = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                hearts.empty()
                pygame.mixer.music.stop()
                return
            if fire_not:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if fire_clip < 30:
                            player.fire()
                            shot.play()
                            fire_clip += 1
                        else:
                            fire_not = False
                            recharge2 = True
                            start_time = time.time()
                            x = 3
            else:
                cur_time = time.time()
                if cur_time - start_time >= 2:
                    x -= 1
                if x <= 0:
                    fire_not = True
                    recharge2 = False
                    fire_clip = 0

        if lost >= 3:
            title_lose = font.render('Пропущено: 10', True, (255, 255, 255))
            pygame.mixer.music.stop()
            pygame.mixer.music.stop()
            hearts.empty()
            show_menu_end(False)
        if i == 10:
            pygame.mixer.music.stop()
            counter = font2.render('Сбито: 10', True, (255, 255, 255))
            pygame.mixer.music.stop()
            hearts.empty()
            show_menu_end(True)

        window.blit(bake, (0,0))
        title_lose = font.render('Пропущено: ' + str(lost), True, (255, 255, 255))
        window.blit(title_lose, (10, 10))
        counter = font2.render('Сбито: ' + str(i), True, (255, 255, 255))
        window.blit(counter, (10, 50))

        player.update()
        player.resise()


        asteroid.resise()
        asteroid.update()
        bullets.draw(window)
        bullets.update()
        enemys.draw(window)
        enemys.update()
        hearts.draw(window)

        collisions = pygame.sprite.groupcollide(bullets, enemys, True, True)
        if player.is_collided_with(asteroid):
            pygame.mixer.music.stop()
            hearts.empty()
            show_menu_end(False)
        if collisions:
            i += 1

        for collid in collisions:
            enemy = Enemy('ufo.png', randint(0, 600) , 0, 65, 50, randint(1, 1))
            enemys.add(enemy)
        if len(enemys) < 5:
            enemy = Enemy('ufo.png', randint(0, 600) , 0, 65, 50, randint(1, 1))
            i += 5 - len(enemys)
            enemys.add(enemy)

        if asteroid.rect.y >= 600:
            asteroid.rect.x = randint(0, 600)
            asteroid.rect.y = 0

        if recharge2:
            recharge = font5.render('Перезарядка', True, (255, 255, 255))
            window.blit(recharge, (player.rect.x, player.rect.y))
        if recharge2 == False:
            recharge = font5.render('', True, (255, 255, 255))
            window.blit(recharge, (player.rect.x, player.rect.y))

        clock.tick(60)
        pygame.display.update()
def show_menu_start():
    menu = pygame_menu.Menu('', 700, 600, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Играть', main)
    menu.add.button('Выйти', pygame_menu.events.EXIT)
    menu.mainloop(window)

def show_menu_end(win):
    global victory
    global defit
    menu2 = pygame_menu.Menu('', 700, 600, theme=pygame_menu.themes.THEME_DARK)
    if win:
        menu2.add.label('Победа')
    else:
        menu2.add.label('Порожение')

    menu2.add.button('Заново', main)
    menu2.add.button('Выйти', pygame_menu.events.EXIT)
    menu2.mainloop(window)

if __name__ == '__main__':
    show_menu_start()