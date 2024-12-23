#Import and intialize pygame
import pygame
pygame.init() 

# A window where all our elements will be
screenWidth = 500
win = pygame.display.set_mode((screenWidth, screenWidth))

# Giving our window a name
pygame.display.set_caption("Attack on Jump City")

# Player sprite images uploaded
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()
starboltSound = pygame.mixer.Sound('starbolt.wav')
starboltSound.set_volume(0.4)
hitSound = pygame.mixer.Sound('hit.wav')
hitSound.set_volume(1.0)
collisionSound = pygame.mixer.Sound('swordslash.wav')

music = pygame.mixer.music.load('music.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
score = 0 

# Player and enemy classes
class player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = True 
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 20, self.y + 5, 30, 55) 
        self.health = 20
        self.visible = True

    def draw(self, win):
        if self.visible:
            if self.walkCount + 1 >= 27: # Each player sprite will be displayed for 3 frames: 3 * 9 imgs = 27. 27 frames per second
                self.walkCount = 0       # set to 0 to prevent index error

            if not (self.standing):
                if self.left:
                    win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                    self.walkCount += 1
                elif self.right:
                    win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                    self.walkCount += 1
            else:
                # Instead of standing facing fowarding - win.blit(char , (self.x,self.y)), face the last direction you were in
                if (self.right):
                    win.blit(walkRight[0] , (self.x , self.y))
                else:
                    win.blit(walkLeft[0] , (self.x , self.y))

            pygame.draw.rect(win, (0, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 30, 10)) 
            pygame.draw.rect(win, (181, 5, 222), (self.hitbox[0], self.hitbox[1] - 20, 30 * (self.health / 20), 10)) 

            self.hitbox = (self.x + 20, self.y + 5, 30, 55)
           # pygame.draw.rect(win, (255,0,0), self.hitbox, 2), uncomment to show hitbox

    def hit(self):
        if self.health > 0:
            self.health -= 5
        else:
            self.visible = False
        self.isJump = False
        self.jumpCount = 10
        self.x = 250 
        self.y = 410
        self.walkCount = 0 
        font1 = pygame.font.SysFont('Pokemon GB.ttf', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (500/2 - (text.get_width() / 2), 200))
        pygame.display.update()
        i= 0
        while i < 300:
            pygame.time.delay(5)
            i += 1
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    i = 301

class projectile:
    def __init__(self, x , y, radius, color, facing): # Facing tells us if the bullets are moving left or right 
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color 
        self.facing = facing
        self.velocity = 8 * facing 

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x , self.y), self.radius)

class enemy:
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [x, end] 
        self.walkCount = 0
        self.velocity = 10 
        self.hitbox = (self.x, self.y, 30, 60)
        self.health = 50 
        self.visible = True 

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33: # 33 frames, 11 enemy imgs * 3
                self.walkCount = 0

            if self.velocity > 0: 
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1 
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1 

            health_percentage = self.health if self.health > 0 else 1 
            pygame.draw.rect(win, (0, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 30, 10)) 
            pygame.draw.rect(win, (255, 116, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (30 / health_percentage * (50 - health_percentage)), 10)) 

            self.hitbox = (self.x, self.y, 30, 60)
            #pygame.draw.rect(win, (255,0,0), self.hitbox, 2), uncomment to show hitbox


    def move(self):
        if self.velocity > 0: # If velocity is positive, enemy is moving right
            if self.x + self.velocity < self.path[1] : 
                self.x += self.velocity
            else:
                self.velocity *= -1 # Change directions 
                self.walkCount = 0
        else:
            if self.x - self.velocity > self.path[0] : 
                self.x += self.velocity
            else:
                self.velocity *= -1 # Change directions 
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('Hit')

    def enemyAndplayerCollision(self):
        self.x = 60 
        self.y = 410
        self.walkCount = 0
        print('Hit')
        
        

def redrawGameWindow():
    win.blit(bg , (0,0))
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (350, 10)) 
    starfire.draw(win) # How our player is added to the screen
    slade.draw(win) # How our enemy is added to the screen
    for starbolt in starbolts:
        starbolt.draw(win)
     
    if not slade.visible:
        win_text = pygame.font.SysFont('Pokemon GB.ttf', 50).render('You Win!', 1, (0, 255, 0))
        win.blit(win_text, (screenWidth // 2 - win_text.get_width() // 2, screenWidth // 2 - win_text.get_height() // 2))

    if not starfire.visible:
        win_text = pygame.font.SysFont('Pokemon GB.ttf', 50).render('You Lose!', 1, (255, 0, 0))
        win.blit(win_text, (screenWidth // 2 - win_text.get_width() // 2, screenWidth // 2 - win_text.get_height() // 2))

    pygame.display.update() 

# Mainloop
font = pygame.font.SysFont('Pokemon GB.ttf', 30) 
starfire = player(300, 410, 64, 64) 
slade = enemy(60, 410, 64, 64, 450)  
shootLoop = 0
starbolts = []
run = True
while run:
    clock.tick(27) 

    # Handles enemy and player collision 
    if slade.visible == True and starfire.visible == True:
        if starfire.hitbox[1] < slade.hitbox[1] + slade.hitbox[3] and starfire.hitbox[1] + starfire.hitbox[3] > slade.hitbox[1]: 
            if starfire.hitbox[0] + starfire.hitbox[2] > slade.hitbox[0] and starfire.hitbox[0] < slade.hitbox[0] + slade.hitbox[2]:
                collisionSound.play() 
                starfire.hit()
                slade.enemyAndplayerCollision() 
                score -= 5

    for starbolt in starbolts:
         # If a starbolt is within the x and y coordinates then its inside slade's hotbox, slade.hitbox[0] is his x coord. 
        if starbolt.y - starbolt.radius < slade.hitbox[1] + slade.hitbox[3] and starbolt.y + starbolt.radius > slade.hitbox[1] : 
            if starbolt.x + starbolt.radius > slade.hitbox[0] and starbolt.x - starbolt.radius < slade.hitbox[0] + slade.hitbox[2]:
                hitSound.play()
                slade.hit()
                score += 1
                starbolts.pop(starbolts.index(starbolt)) # starbolt should disappear after collision 

        if starbolt.x < 500 and starbolt.x > 0:
            starbolt.x += starbolt.velocity 
        else:
            starbolts.pop(starbolts.index(starbolt))

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        starboltSound.play()
        if starfire.left:
            facing = -1
        else:
            facing = 1
        if len(starbolts) < 5: 
            starbolts.append(projectile(round(starfire.x + starfire.width // 2),
                                        round(starfire.y + starfire.height // 2), 6, (99, 255, 0), facing))
        shootLoop = 1


    if keys[pygame.K_LEFT] and starfire.x > starfire.velocity:
        starfire.x-= starfire.velocity
        starfire.left = True
        starfire.right = False
        starfire.standing = False 
    elif keys[pygame.K_RIGHT]and starfire.x < screenWidth - starfire.width - starfire.velocity:
        starfire.x += starfire.velocity
        starfire.right = True
        starfire.left = False
        starfire.standing = False  
    else: 
        # We just standing there 
        starfire.standing = True
        starfire.walkCount = 0


    if not (starfire.isJump):
        if keys[pygame.K_UP]: 
            starfire.isJump = True
            starfire.walkCount = 0
    else:
        if starfire.jumpCount >= -10:
            neg = 1
            if starfire.jumpCount < 0:
                neg = -1 
            starfire.y -= (starfire.jumpCount ** 2) * 0.5 * neg # Start of the jump, upwards motion
            starfire.jumpCount -= 1 # Slowing moving down
        else: 
            # Jump has concluded
            starfire.isJump = False
            starfire.jumpCount = 10

    redrawGameWindow()
pygame.quit()
