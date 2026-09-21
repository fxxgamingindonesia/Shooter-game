from pygame import *
window  =display.set_mode((700,500))
display.set_caption("Maze")
win_width = 700
win_height = 500

class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
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
        if keys[K_d] and self.rect.x < win_width - 65:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 65:
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = 'left'
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >= win_width - 65:
            self.direction = 'left'

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color, x, y, width, height):
        super().__init__ ()
        self.color = color 
        self.width = width
        self.height = height
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


background = transform.scale(image.load("background.jpg"), ((win_width,win_height)))
packman = Player('hero.png', 5, win_height - 80, 4)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)


w1 = Wall((75, 255, 118), 100, 20, 10, 380)
w2 = Wall((75, 255, 118), 100, 20, 450, 10)
w3 = Wall((75, 255, 118), 100, 480, 450, 10)
w4 = Wall((75, 255, 118), 220, 160, 10, 320)
w5 = Wall((75, 255, 118), 350, 20, 10, 320)
w6 = Wall((75, 255, 118), 470, 160, 10, 320)

finish = False
game = True
fps = time.Clock()

font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (0, 0, 255))
lose = font.render('YOU LOSE!', True, (255, 0, 0))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
sound_win = mixer.Sound('money.ogg')
sound_lose = mixer.Sound('kick.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:

        window.blit(background, (0, 0))
        w1.draw()
        w2.draw()
        w3.draw()
        w4.draw()
        w5.draw()
        w6.draw()
        packman.update()
        monster.update()

        packman.reset()
        monster.reset()
        final.reset()

        if sprite.collide_rect(packman, final):
            finish = True
            window.blit(win, (200, 200))
            sound_win.play()

        if sprite.collide_rect(packman, monster) or  sprite.collide_rect(packman, w1) or  sprite.collide_rect(packman, w2) or  sprite.collide_rect(packman, w3) or sprite.collide_rect(packman, w4) or  sprite.collide_rect(packman, w5) or  sprite.collide_rect(packman, w6):
            finish = True
            window.blit(lose, (200, 200))
            sound_lose.play()
    display.update()
    fps.tick(60)