from pygame import *
from random import *
import time as t

#создай окно игры
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter Game')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
shot = mixer.Sound('fire.ogg')
mixer.music.play()

enemies = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

ammo = 5
lifes = 3
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width,player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

player = GameSprite('rocket.png', 335, 400, 6, 60, 85)

miss = 0
class bullet(GameSprite):
    def update(self):
        global miss
        global ammo
        self.rect.y -= self.speed
        if self.rect.y < -35:
            self.kill()
            miss += 1

lastReloadTime = 0

lost = 0
score = 0 
class enemy(GameSprite):
    def update(self):
        global score
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -65
            lost += 1
            self.speed = 1
        enemies_list = sprite.groupcollide(enemies, bullets, False, True)
        for i in enemies_list:
            i.rect.x = randint(80, win_width - 80)
            i.rect.y = -65
            score += 1

class asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = randint(-150, -65)
            self.speed = 1
        sprite.groupcollide(asteroids, bullets, False, True)

for i in range(2):
    aster = asteroid('asteroid.png', randint(80, win_width - 80), randint(-650, -300), 1, 35, 35)
    asteroids.add(aster)

for i in range (5):
    ene = enemy('ufo.png', randint(80, win_width - 80), randint(-150, -65), 1, 85, 60)
    enemies.add(ene)

font.init()
write = font.SysFont('arial', 24)
winlose = font.SysFont('arial', 48)


clock = time.Clock()
FPS = 60

finish = False
game = True
reloading = False

while game:
    losed = write.render(f'Пропущено: {lost}', 1, (0,255,124))
    missed = write.render(f'Промазал: {miss}', 1, (0,255,124))
    shoot = write.render(f'Счёт: {score}', 1, (0,255,124))
    lifes_s = write.render(f'Жизни: {lifes}', 1, (0,255,124))
    win = winlose.render('YOU WIN!', 1, (0,255,124))
    lose = winlose.render('YOU LOSE!', 1, (0,255,124))
    fired = winlose.render('YOU ARE FIRED!', 1, (255,0,0))
    fired2 = winlose.render('YOU MISSED SO MUCH!', 1, (255,0,0))
    reloading_wr = write.render('Перезарядка...', 1, (0,255,124))
    ammo_wr = write.render(f'{ammo}/5', 1, (0,255,124))


    key_pressed = key.get_pressed()

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not reloading:
                a = bullet('bullet.png', player.rect.x + 20, player.rect.top, 5, 20, 35)
                bullets.add(a)
                shot.play()
                ammo -= 1
    if key_pressed[K_LEFT] and player.rect.x > 10:
        player.rect.x -= player.speed
    if key_pressed[K_RIGHT] and player.rect.x < 630:
        player.rect.x += player.speed


    if finish != True:
        window.blit(background,(0,0))
        player.reset()

        enemies.draw(window)
        enemies.update()
        
        bullets.draw(window)
        bullets.update()

        asteroids.draw(window)
        asteroids.update()


    if ammo <= 0:
        lastReloadTime = t.time()
        reloading = True
        ammo = 5
    if t.time() - lastReloadTime > 1.5:
        reloading = False
    if reloading:
        window.blit(reloading_wr, (280,30))


    window.blit(losed, (20,15))
    window.blit(shoot, (20,40))
    window.blit(missed, (20,65))
    window.blit(lifes_s, (585,15))
    window.blit(ammo_wr, (585,45))


    if lost >= 3:
        window.blit(lose, (220,210))
        finish = True
    if score >= 40:
        window.blit(win, (220,210))
        finish = True
    if miss >= 8:
        window.blit(fired, (150,180))
        window.blit(fired2, (90,260))
        finish = True
    enemies_list2 = sprite.spritecollide(player, enemies, False, False)
    for i in enemies_list2:
        i.rect.x = randint(80, win_width - 80)
        i.rect.y = -65
        lifes -= 1
    if lifes <= 0:
        window.blit(lose, (220,210))
        finish = True
    enemies_list3 = sprite.spritecollide(player, asteroids, False, False)
    for i in enemies_list3:
        lifes = 0


    display.update()
    clock.tick(FPS)
