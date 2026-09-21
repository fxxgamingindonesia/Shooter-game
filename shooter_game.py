from pygame import *
from random import *
import time as tm
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter Game")

font.init()
font2 = font.Font(None, 36)
font3 = font.Font(None, 80)

win = font3.render('YOU WIN!', True, (255, 255, 255))
lose = font3.render('YOU LOSE!', True, (180, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image  =transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
    
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            lost = lost + 1        

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

background = transform.scale(image.load("galaxy.jpg"), ((win_width, win_height)))
ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

bullets  =sprite.Group()
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png' , randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy('asteroid.png' ,randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

lost = 0
score = 0
goal = 7
life = 3
rel_time = False
num_fire = 0
finish = False
game = True
fps = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                
                if num_fire >= 10 and rel_time == False:
                    last_time = tm.time()
                    rel_time = True


    if finish != True:
        window.blit(background, (0, 0))
        text = font2.render("Score: "+ str(score), 1 , (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        ship.reset()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)

        if rel_time == True:
            now_time = tm.time()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                    num_fire = 0
                    rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        sprite.groupcollide(asteroids, bullets, False, True)
        for c in collides:
                score = score + 1
                monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                monsters.add(monster)

        if score == goal:
            finish = True
            window.blit(win, (200, 200))

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1
        if life == 0 or lost >= 10:

            finish = True
            window.blit(lose, (200, 200))
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        text_life = font3.render(str(life), 1 , life_color)
        window.blit(text_life, (650, 10))
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1,7))
            asteroids.add(asteroid)


    display.update()
    fps.tick(60)