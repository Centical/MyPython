import pygame
pygame.init()

win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("pyDventure")

bg = pygame.image.load('pics/bcgrd.png')


walkRight = [pygame.image.load('pics/R1.png'), pygame.image.load('pics/R2.png'),
             pygame.image.load('pics/R3.png'), pygame.image.load('pics/R4.png'),
             pygame.image.load('pics/R5.png'), pygame.image.load('pics/R6.png')]
walkLeft = [pygame.image.load('pics/L1.png'), pygame.image.load('pics/L2.png'),
            pygame.image.load('pics/L3.png'), pygame.image.load('pics/L4.png'),
            pygame.image.load('pics/L5.png'), pygame.image.load('pics/L6.png')]

clock = pygame.time.Clock()

score = 0

shotSound = pygame.mixer.Sound('sound/pupp.wav')
hitSound = pygame.mixer.Sound('sound/click.wav')
shotSound.set_volume(0.1)
hitSound.set_volume(0.4)

music = pygame.mixer.music.load('sound/normalland.mp3')
pygame.mixer.music.play(-1)
pygame.mixer_music.set_volume(0.7)

screenx = 1280
screeny = 720


class Monster(object):
    walkRight = [pygame.image.load('pics/mr1.png'), pygame.image.load('pics/mr2.png'),
                 pygame.image.load('pics/mr3.png'), pygame.image.load('pics/mr4.png'),
                 pygame.image.load('pics/mr5.png'), pygame.image.load('pics/mr6.png'),
                 pygame.image.load('pics/mr7.png'), pygame.image.load('pics/mr8.png'), ]
    walkLeft = [pygame.image.load('pics/ml1.png'), pygame.image.load('pics/ml2.png'),
                pygame.image.load('pics/ml3.png'), pygame.image.load('pics/ml4.png'),
                pygame.image.load('pics/ml5.png'), pygame.image.load('pics/ml6.png'),
                pygame.image.load('pics/ml7.png'), pygame.image.load('pics/ml8.png'), ]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkcount = 0
        self.vel = 6
        self.hitbox = (self.x + 10, self.y + 30, 36, 30)
        self.facing = -1
        self.health = 10
        self.visible = True

    def draw(self, win):


        self.hitbox = ((self.x + self.facing), self.y + 30, 36, 30)
    #   pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        self.move()
        if self.visible:
            if self.walkcount + 1 >= 16:
                self.walkcount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkcount // 2], (self.x, self.y))
                self.walkcount += 1
                self.facing = 20
            else:
                win.blit(self.walkLeft[self.walkcount // 2], (self.x, self.y))
                self.walkcount += 1
                self.facing = 8
            pygame.draw.rect(win, (0, 0, 0), (self.hitbox[0] + 2 , self.hitbox[1] - 10.5, 32, 10))
            pygame.draw.rect(win, (130, 0, 155), (self.hitbox[0] + 2, self.hitbox[1] - 10, 30 - ((30/10) * (10 - self.health) ), 8))

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0

    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 7
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 60, 28, 60)

    def draw(self, win):
        self.hitbox = (self.x + 17, self.y + 60, 28, 60)
        if self.walkCount + 1 >= 24:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 4], (self.x, self.y))
                self.walkCount += 1
                return win
            elif self.right:
                win.blit(walkRight[self.walkCount // 4], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.velocity = 7
        self.x = 640
        self.y = 546 - 128
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsansms', 100)
        text11 = font1.render('Game Over', 1, (255, 0, 0))
        win.blit(text11, ((1280 / 2) - (text11.get_width() / 2), (720 / 2) - (text11.get_height() / 2)))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velocity = 15 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


moveen = 0


def redrawgamewindow():
    win.blit(bg, (moveen + bg.get_width(), 0))
    win.blit(bg, (moveen, 0))
    win.blit(bg, (moveen - bg.get_width(), 0))
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, ((1255 - text.get_width()), 10))
    man.draw(win)
    monstro.draw(win)
    for bullet in bullets:
        bullet.draw(win)


# mainloop
font = pygame.font.SysFont('comicsansms', 30, True, False)
man = Player(640, (546 - 128), 64, 128)
monstro = Monster(110 + 64, (546 - 64), 64, 64, (1280 - 64))
shootloop = 0
bullets = []
run = True
while run:

    clock.tick(24)

    if man.hitbox[1] < monstro.hitbox[1] + monstro.hitbox[3] and man.hitbox[1] + man.hitbox[3] > monstro.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > monstro.hitbox[0] and man.hitbox[0] < monstro.hitbox[0] + monstro.hitbox[2]:
            if monstro.visible:
                man.hit()
                score = 0

    if shootloop > 0:
        shootloop += 1
    if shootloop > 3:
        shootloop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < monstro.hitbox[1] + monstro.hitbox[3]\
                and bullet.y + bullet.radius > monstro.hitbox[1]:
            if bullet.x + bullet.radius > monstro.hitbox[0]\
                    and bullet.x - bullet.radius < monstro.hitbox[0] + monstro.hitbox[2]:
                if monstro.visible:
                    hitSound.play()
                    monstro.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))

        if 0 < bullet.x < 1280:
            bullet.x += bullet.velocity
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootloop == 0:
        shotSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 100:
            bullets.append(Projectile(round(man.x + man.width // 2),
                                      round(man.y + man.height // 1.3), 3, (153, 153, 0), facing))

        shootloop = 1

    if keys[pygame.K_a] and man.x > 1:
        monstro.x += man.velocity
        moveen += man.velocity
        man.x -= man.velocity * 0.7
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_d] and man.x < screenx - man.width:
        monstro.x -= man.velocity
        moveen -= man.velocity
        man.x += man.velocity * 0.7
        man.right = True
        man.left = False
        man.standing = False

    else:
        man.standing = True
        man.walkCount = 0

    if not(man.isJump):
        if keys[pygame.K_w]:
            man.isJump = True
            man.velocity = 16
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount <= 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) / 2 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.velocity = 7
            man.jumpCount = 10

    pygame.display.update()
    redrawgamewindow()

pygame.quit()
