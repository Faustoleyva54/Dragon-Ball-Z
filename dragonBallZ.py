'''
skeleton from Lukas Peraza
-pictures from google images
-code influenced by pygame documentation 
-dragon ball z font file "Saiyan-Sans.ttf" from http://www.fonts4free.net/dragonball-z-font.html
'''

import pygame, sys 
from villian import Enemy, Attacks, SuperMove, ComEnemy, ComAttacks, ComAttacksBoss
from character import Player, Extent, kick, Boss
import random

#helper function to create text
def drawText(screen, font, cx, cy, writing, textColor, backgroundColor = ""):
    text = font.render(writing, True, textColor, backgroundColor)
    textrect = text.get_rect()
    textrect.centerx = cx
    textrect.centery = cy
    screen.blit(text, textrect)

#helper function to create text
def drawText1(screen, font, cx, cy, writing, textColor, backgroundColor = ""):
    text = font.render(writing, True, textColor, backgroundColor)
    textrect = text.get_rect()
    textrect.centerx = cx
    textrect.centery = cy
    return (text, textrect)

class MainScreen(object):
    #keeps track of stages of game
    startScreen = True
    pickCharacter = False
    helpScreen = False
    gameScreen = False
    gameOver = False
    levelOver = False
    level2 = False
    level3 = False
    tutorial = False
    pause = False
    wish = False
    won = False

    vegetaPic = pygame.image.load("staticFiles/vegeta/vPic.gif")
    vegetaRect = vegetaPic.get_rect()
    width, height = vegetaPic.get_size()
    vegetaRect.move_ip(1000-width,0)
    gokuPic = pygame.image.load("staticFiles/goku/gokuProfilePic.gif")
    gokuPic = pygame.transform.scale(gokuPic, (width, height))
    gokuRect = gokuPic.get_rect()
    character = "goku"


    def init(self):
        #creates pygame sprite group for enemies and ki blasts
        self.Enemies = pygame.sprite.Group()
        self.ComEnemies = pygame.sprite.Group()
        self.Attacks = pygame.sprite.Group()
        self.ComAttacks = pygame.sprite.Group()

        #keeps track of the stages of the game
        #manages the scrolling of the screen
        self.scrollX = 0
        self.scrollMargin = self.width - self.width//5
        self.allowed = 0 #the amount the user can scroll (has to defeat enemies to increase)
        self.newWave = True #when an enemy is defeated
        self.shifting = False #when the advancing to the next stage

        self.player = Player(MainScreen.character)
        self.player.rect.move_ip(self.width//20, self.height*3//5)
        self.character = None
        self.harm = 0
        self.energyGauge = 4.18
        self.energy = self.width//self.energyGauge #%%%%% 239
        self.charge = 0

        #The different variables which define the main character
        self.punch = Extent(self.player)
        self.leftPunch = Extent(self.player)
        self.leftPunch.rect.move_ip(-135, 0) #the width of Goku and the box
        self.kick = kick(self.player)
        self.leftKick = kick(self.player)
        self.leftKick.rect.move_ip(-135, 0) 
        self.punching = False
        self.countPunchJumps = 0
        self.moving = False
        self.leftMoving = False
        self.kicking = False
        self.shooting = False
        self.shootingSuper = False
        self.superBlast = None
        self.flying = False
        self.standing = True
        self.charging = False
        self.dying = False
        self.blocking = True
        self.count = 0 #counts time after death
        self.movingRight = True #used to controll the image of the character
        self.moveX = 0 #dx
        self.moveY = 0 #dy
        self.nextLevelDelay = False

        self.brolly = Boss()
        self.brolly.rect.move_ip(self.width*7//9, (self.height*3)//5)
        self.brollyPunching = False
        self.brollyMoving = False
        self.brollyLeftMoving = False
        self.brollyKicking = False
        self.brollyShooting = False
        self.brollyShootingSuper = False
        self.brollySuperBlast = None
        self.brollyFlying = False
        self.brollyStanding = True
        self.brollyCharging = False
        self.brollyDying = False
        self.brollyBlocking = True
        

        #mulitple images for background
        mainBackG = pygame.image.load("staticFiles/shenron.jpg")
        self.mainBackG = pygame.transform.scale(mainBackG, (self.width, self.height))
        self.logo = pygame.image.load("staticFiles/logo.png")
        scenary = pygame.image.load("staticFiles/longBackground.png")
        self.scenary = pygame.transform.scale(scenary, (self.width*3,self.height))
        self.scenaryLevel2 = pygame.image.load("staticFiles/level2.jpg")
        self.scenaryLevel2 = pygame.transform.smoothscale(self.scenaryLevel2, (self.width*2, self.height))

        self.index = 0
        self.gameOverbroly1 = pygame.image.load("staticFiles/bLaugh1.gif").convert_alpha()
        self.gameOverbroly1 = pygame.transform.smoothscale(self.gameOverbroly1, (self.width, self.height))
        self.gameOverbroly2 = pygame.image.load("staticFiles/bLaugh2.gif").convert_alpha()
        self.gameOverbroly2 = pygame.transform.smoothscale(self.gameOverbroly2, (self.width, self.height))
        self.bothbrolys = [self.gameOverbroly1, self.gameOverbroly2]
        self.gameOverbroly = self.bothbrolys[self.index]

        self.final = pygame.image.load("staticFiles/tutMode.jpg").convert_alpha()
        self.final = pygame.transform.smoothscale(self.final, (self.width, self.height))
        self.kameHouse = pygame.image.load("staticFiles/kameHouse.jpg").convert_alpha()
        self.kameHouse = pygame.transform.smoothscale(self.kameHouse, (self.width, self.height))

        self.endLevel = pygame.image.load("staticFiles/levelOver.jpg").convert_alpha()
        self.endLevel = pygame.transform.smoothscale(self.endLevel, (self.width, self.height))        
        self.transition = pygame.image.load("staticFiles/transition.png").convert_alpha()
        self.transition = pygame.transform.smoothscale(self.transition, (self.width,self.height))
        self.level = 1 #tracks progress of the game
        self.ballSize = self.width//10
        self.dragonBalls = pygame.image.load("staticFiles/completeDBZ.png").convert_alpha()
        self.dragonBalls = pygame.transform.smoothscale(self.dragonBalls, (self.ballSize,self.ballSize))
        self.dragonOneLeft = pygame.image.load("staticFiles/missingOne.png").convert_alpha()
        self.dragonOneLeft = pygame.transform.smoothscale(self.dragonOneLeft, (self.ballSize,self.ballSize))
        self.dragon2Left = pygame.image.load("staticFiles/dragonBalls2.png").convert_alpha()
        self.dragon2Left = pygame.transform.smoothscale(self.dragon2Left, (self.ballSize,self.ballSize))
        self.dragon3Left = pygame.image.load("staticFiles/dragonBalls3.png").convert_alpha()
        self.dragon3Left = pygame.transform.smoothscale(self.dragon3Left, (self.ballSize,self.ballSize))
        self.pickBackground = pygame.image.load("staticFiles/pickBackground.png").convert_alpha()
        self.pickBackground = pygame.transform.scale(self.pickBackground, (self.width, self.height))
        self.wish = pygame.image.load("staticFiles/shenronWish.gif").convert_alpha()
        self.wish = pygame.transform.scale(self.wish, (self.width, self.height))
        self.finished = pygame.image.load("staticFiles/allBalls.png").convert_alpha()
        self.finished = pygame.transform.scale(self.finished, (self.width//3, self.height//3))
        self.grade = pygame.image.load("staticFiles/grade.png").convert_alpha()
        self.grade = pygame.transform.scale(self.grade, (50, 50))
        self.text = pygame.image.load("staticFiles/text.png").convert_alpha()
        self.text = pygame.transform.scale(self.text, (300, 200))
        self.shot = False
        self.enemyCount = 0

    def mousePressed(self, x, y):
        if self.playrect.collidepoint((x,y)) and MainScreen.startScreen: #gets the game going
            MainScreen.startScreen = False
            MainScreen.pickCharacter = True
        if self.tutrect.collidepoint((x,y)) and MainScreen.startScreen: #tutorial
            MainScreen.startScreen = False
            MainScreen.tutorial = True
        if MainScreen.wish and self.wishrect.collidepoint((x,y)): 
            MainScreen.startScreen = True
            MainScreen.finished = False
            MainScreen.won = True
            MainScreen.wish = False
        if MainScreen.pickCharacter:
            if MainScreen.gokuRect.collidepoint((x,y)):
                MainScreen.character = "goku"
                # self.player = Player(self.character)
                # self.player.rect.move_ip(self.width//20, self.height*3//5)
                MainScreen.pickCharacter = False
                MainScreen.gameScreen = True
                self.init()
            if MainScreen.vegetaRect.collidepoint((x,y)):
                MainScreen.character = "vegeta"
                # self.player = Player(self.character)
                # self.player.rect.move_ip(self.width//20, self.height*3//5)
                MainScreen.pickCharacter = False
                MainScreen.gameScreen = True
                self.init()
    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    #controls all player moves
    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_r: #restarts the game
            MainScreen.startScreen = True
            MainScreen.pickCharacter = False
            MainScreen.helpScreen = False
            MainScreen.gameScreen = False
            MainScreen.gameOver = False
            MainScreen.levelOver = False
            MainScreen.level2 = False
            MainScreen.level3 = False
            MainScreen.tutorial = False
            MainScreen.wish = False
            self.init()
        #responsible for the player's movements --- if moving and want to punch stop movement
        if keyCode == pygame.K_DOWN:
            self.moveY = 5
        if keyCode == pygame.K_UP and not (self.charging or self.punching or self.kicking or self.shootingSuper):
            if self.flying:
                self.moveY = -5
            elif self.standing:
                self.moveY = -25
                self.standing = False
        if keyCode == pygame.K_RIGHT and not (self.charging or self.punching or self.kicking or self.shootingSuper):
            self.moveX = 5
            self.moving = True
        if keyCode == pygame.K_LEFT and not (self.charging or self.punching or self.kicking or self.shootingSuper):
            self.moveX = -5
            self.leftMoving = True

        if keyCode == pygame.K_RSHIFT: #enables the player to fly
            if self.flying:
                self.flying = False
            else:
                self.flying = True
        if keyCode == pygame.K_d and (MainScreen.gameScreen or MainScreen.level2 or MainScreen.tutorial or MainScreen.level3) and not (self.moving or self.leftMoving or self.shootingSuper): #punches
            self.punching = True
        if keyCode == pygame.K_a and (MainScreen.gameScreen or MainScreen.level2 or MainScreen.tutorial or MainScreen.level3) and not (self.moving or self.leftMoving or self.shootingSuper): #kicks
            self.kicking = True
        if keyCode == pygame.K_s and (MainScreen.gameScreen or MainScreen.level2 or MainScreen.tutorial or MainScreen.level3) and not (self.moving or self.leftMoving or self.shootingSuper): #charges up energy
            self.charging = True
            self.charge = 1
        if keyCode == pygame.K_f and (MainScreen.gameScreen or MainScreen.level2 or MainScreen.tutorial or MainScreen.level3) and not (self.moving or self.leftMoving or self.shootingSuper): #charges up energy
            self.blocking = True
        if keyCode == pygame.K_p and (MainScreen.gameScreen or MainScreen.level2 or MainScreen.level3) and not MainScreen.tutorial: #charges up energy
            if MainScreen.pause:
                MainScreen.pause = False
            else:
                MainScreen.pause = True

        if keyCode == pygame.K_f and (MainScreen.gameScreen): #charges up energy
            MainScreen.gameScreen = False
            MainScreen.level2 = True
        elif keyCode == pygame.K_f and MainScreen.level2:
            MainScreen.level2 = False
            MainScreen.level3 = True

        if keyCode == pygame.K_SPACE and (MainScreen.gameScreen or MainScreen.level2 or MainScreen.tutorial or MainScreen.level3) and not (self.moving or self.leftMoving): #shoots kiBlast 
            if self.energy > 10 and not self.charging:
                self.createKiBlast(self.movingRight)
                self.energy -= self.width/(8*self.energyGauge)
                self.shooting = True
        if keyCode == pygame.K_w and (MainScreen.gameScreen or MainScreen.level2 or MainScreen.tutorial or MainScreen.level3) and not (self.moving or self.leftMoving): #shoots super attack
            if self.energy >= (self.width//(self.energyGauge))//2 and not self.charging:
                self.createSuper()
                self.energy -= 100
                self.shootingSuper = True
        if keyCode == pygame.K_RIGHT and MainScreen.levelOver:
            MainScreen.level2 = True
            MainScreen.levelOver = False
            if MainScreen.level3:
                MainScreen.level2 = False
            self.init()

    def keyReleased(self, keyCode, modifier):
        #resets the movement when key is released 
        if keyCode == pygame.K_DOWN:
            self.moveY = 0
        if keyCode == pygame.K_UP:
            self.moveY = 0
        if keyCode == pygame.K_RIGHT:
            self.moveX = 0
            self.moving = False
        if keyCode == pygame.K_LEFT:
            self.moveX = 0
            self.leftMoving=False
        #when the key is released the action is stopped 
        if keyCode == pygame.K_d and (MainScreen.gameScreen or MainScreen.level2 or MainScreen.tutorial or MainScreen.level3):
            self.punching = False
        if keyCode == pygame.K_a and (MainScreen.gameScreen or MainScreen.level2 or MainScreen.tutorial or MainScreen.level3):
            self.kicking = False
        if keyCode == pygame.K_s and (MainScreen.gameScreen or MainScreen.level2 or MainScreen.tutorial or MainScreen.level3):
            self.charging = False
            self.charge = 0
        if keyCode == pygame.K_SPACE and (MainScreen.gameScreen or MainScreen.level2 or MainScreen.tutorial or MainScreen.level3):
            self.shooting = False  
        if keyCode == pygame.K_w and (MainScreen.gameScreen or MainScreen.level2 or MainScreen.tutorial or MainScreen.level3):
            self.shootingSuper = False 
            self.superBlast = None       

    def createKiBlast(self, movingRight): #adds new blast to sprite group
        kiblast = Attacks(self.player, movingRight)
        self.Attacks.add(kiblast)

    def createSuper(self): #creates a super attack
        superBlast = SuperMove(self.player, self.movingRight)
        self.superBlast = superBlast
    
    def createEnemy(self): #adds an enemy to the screen
        newEnemy = Enemy()
        newEnemy.rect.move_ip(self.width-self.player.width, self.height*3//5+35)
        self.Enemies.add(newEnemy)

    def createComEnemy(self): #adds an enemy to the screen
        self.enemyCount += 1
        newEnemy2 = None
        if self.enemyCount > 2:
            self.enemyCount = 1
            newEnemy2 = ComEnemy(self.enemyCount)
            self.enemyCount += 1
        newEnemy = ComEnemy(self.enemyCount)
        newEnemy.rect.move_ip(self.width-self.player.width, self.height*3//5+35)
        self.ComEnemies.add(newEnemy)
        if newEnemy2:
            self.ComEnemies.add(newEnemy2)

    def checkScroll(self):
        #makes sure the screen moves only the allotted amount(increases when an enemy is defeated)
        if not MainScreen.level3:
            if self.scrollX < self.allowed:
                self.shifting = True
                if self.player.rect.right >= self.scrollMargin:
                    self.scrollX += 10
            #when the screen finishs moving, the player is moved to the starting position and an enemy approaches from the right
            elif (self.scrollX == self.allowed) and (self.allowed != 0) and (self.player.rect.left + self.width//3.33 > self.width) and len(self.Enemies) == 0 and len(self.ComEnemies) == 0: #boundry at the end
                transport = self.width//1.535
                self.player.rect.move_ip(-1*transport, 0)
                self.punch.rect.move_ip(-1*transport, 0)
                self.leftPunch.rect.move_ip(-1*transport, 0)
                self.kick.rect.move_ip(-1*transport, 0)
                self.leftKick.rect.move_ip(-1*transport, 0)            
                self.newWave = True    
                self.shifting = False#in charge of moving screen

    #takes care of where the player is looking by finding the nearest enemy and looking towards its location
    def orientation(self):
        closest = None
        range = 0
        cx, cy = self.player.rect.center
        if self.gameScreen:
            enemies = self.Enemies
        else:
            enemies = self.ComEnemies
        for enemy in enemies:
            x, y = enemy.rect.center
            newRange = x - cx
            if abs(newRange) > range:
                closest = enemy
                range = newRange
        if MainScreen.level3:
            closest = self.brolly
            x,y = closest.rect.center
            range = x - cx
        if range >= 0:
            self.movingRight = True
        else:
            self.movingRight = False

    def checkBoundries(self): #makes sure the player is within bounds
        if MainScreen.level3 or MainScreen.tutorial:
            if self.player.rect.right >= self.width and self.moveX > 0:
                self.moveX = 0
            elif self.player.rect.left <= 0 and self.leftMoving:
                self.moveY = 0
        elif self.player.rect.right >= self.scrollMargin and self.moveX > 0:
            self.moveX = 0
        elif self.player.rect.left <= 0 and self.leftMoving:
            self.moveX = 0
        if self.player.rect.top <= 0:
            self.moveY = 0

    #moves the player and the invisible boxes which represent his punches and kicks
    def movePLayer(self):
        self.player.rect.move_ip(self.moveX, self.moveY)
        self.punch.rect.move_ip(self.moveX, self.moveY)
        self.leftPunch.rect.move_ip(self.moveX, self.moveY)
        self.kick.rect.move_ip(self.moveX, self.moveY)
        self.leftKick.rect.move_ip(self.moveX, self.moveY)

    def gravityAndLevel(self):
        #gravity aspect - brings the character down from jumping
        gravFact = self.player.width // 15
        if self.player.rect.bottom < self.height*3//5+2*self.player.width and not self.flying:
            self.player.rect.move_ip(0,gravFact)
            self.punch.rect.move_ip(0,gravFact)
            self.leftPunch.rect.move_ip(0,gravFact)
            self.kick.rect.move_ip(0,gravFact) 
            self.leftKick.rect.move_ip(0,gravFact)
        #keeps the player at ground level
        if self.player.rect.bottom > self.height*3//5+2*75:
            self.player.rect.move_ip(0,-1*gravFact)
            self.punch.rect.move_ip(0,-1*gravFact)
            self.leftPunch.rect.move_ip(0,-1*gravFact)
            self.kick.rect.move_ip(0,-1*gravFact) 
            self.leftKick.rect.move_ip(0,-1*gravFact)
        # if the player is on the ground then he is standing
        elif self.player.rect.bottom == self.height*3//5+2*self.player.width: 
            self.standing = True #keeps player at level

    def enemyAI(self, ticks):
        pushbackFact = 5.55 #the factor pushed back
        if MainScreen.level2:
            enemies = self.ComEnemies
        else:
            enemies = self.Enemies
        for enemy in enemies:
            enemy.dodge(self.Attacks, self.movingRight) #dodges most attacks
            enemy.Punch(self.player, self.movingRight) #punches when player is in short range
            if MainScreen.level2:
                if not self.shot: 
                    self.ComEnemyShoot(enemy)
                    self.shot = True 
            for blast in self.ComAttacks:
                if pygame.sprite.collide_rect(blast, self.player): 
                    pushback = -1 * self.width//pushbackFact
                    if not self.movingRight:
                        pushback *= -1
                    if self.player.rect.move(pushback, 0).left < 0:
                        pushback = -1*self.player.rect.left
                    if self.player.rect.move(pushback, 0).right > self.width:
                        pushback = self.width - self.player.rect.right
                    if not blast.damaged:
                        self.player.rect.move_ip(pushback, 0) #if hit, then moved back
                        self.punch.rect.move_ip(pushback, 0)
                        self.leftPunch.rect.move_ip(pushback, 0)
                        self.kick.rect.move_ip(pushback, 0)
                        self.leftKick.rect.move_ip(pushback, 0)
                    ##move the whole player (punches and everything)
                    if not blast.damaged:
                        self.harm += 40   
                        blast.damaged = True
                    if self.harm >= self.width//3.58:
                        self.harm = self.width//3.58
                        self.dying = True
                    # self.ComAttacks.remove(blast) #removes kiblast when hit
                    self.shot = True
                if blast.rect.left > self.width*1.5:
                    self.ComAttacks.remove(blast)
                    self.shot = False
                elif blast.rect.left < -.5*self.width:
                    self.ComAttacks.remove(blast)
                    self.shot = False
            for kiblast in self.Attacks: #handles collisions between attacks
                if pygame.sprite.collide_rect(kiblast, enemy): 
                    pushback = self.width//pushbackFact
                    if not self.movingRight:
                        pushback *= -1
                    enemy.rect.move_ip(pushback, 0) #if hit, then moved back
                    enemy.health -= 1   
                    if enemy.health == 0: #increases allowed when enemy defeated
                    #################################################
                        self.Enemies.remove(enemy)
                        self.allowed += self.width
                        if self.allowed == self.width*3 and MainScreen.gameScreen:
                            self.nextLevelDelay = True
                        elif self.allowed == self.width*4 and MainScreen.level2 and len(self.ComEnemies) == 0:
                            self.nextLevelDelay = True
                        continue
                    self.Attacks.remove(kiblast) #removes kiblast when hit
                if kiblast.rect.left > self.width:
                    self.Attacks.remove(kiblast)
            if self.superBlast:
                for image, rect in self.superBlast.fullKame:
                    if rect.colliderect(enemy):
                        pushback = self.width//pushbackFact
                        if self.movingRight and pushback < 0:
                            pushback *= -1
                        elif not self.movingRight and pushback > 0:
                            pushback *= -1
                        enemy.rect.move_ip(pushback, 0) #if hit, then moved back
                        enemy.health -= 1 
                        if enemy.health == 0:
                        ######################################
                            enemies.remove(enemy)
                            self.allowed += self.width
                        if self.allowed == self.width*3 and MainScreen.gameScreen:
                            self.nextLevelDelay = True
                        elif self.allowed == self.width*4 and MainScreen.level2 and len(self.ComEnemies) == 0:
                            self.nextLevelDelay = True
            if not self.punching and not self.kicking:   
                if pygame.sprite.collide_rect(self.player, enemy):
                    self.harm += 1
            if self.harm >= self.width//3.58: ###gets 279
                self.dying = True
            if enemy.punching:
                self.enemyPunch(enemy)
                if self.movingRight:
                    enemy.rect.move_ip(self.jump+self.jump//2,-1*self.jump)
                else:
                    enemy.rect.move_ip(-1*self.jump-self.jump//2,-1*self.jump)
                enemy.moved = True
                self.jump = 0 
            if self.punching:
                if self.movingRight:
                    punch = self.punch
                else: 
                    punch = self.leftPunch
                if pygame.sprite.collide_rect(punch, enemy):
                    enemy.health -= 1
                    if enemy.health == 0:
                        #####################################################
                        enemies.remove(enemy)
                        self.allowed += self.width
                    if self.allowed == self.width*3 and MainScreen.gameScreen:
                        self.nextLevelDelay = True
                    elif self.allowed == self.width*4 and MainScreen.level2 and len(self.ComEnemies) == 0:
                        self.nextLevelDelay = True
                    pushback = self.width//pushbackFact
                    if not self.movingRight:
                        pushback *= -1
                    enemy.rect.move_ip(pushback, 0)          
            if self.kicking:
                if self.movingRight:
                    kick = self.kick
                else:
                    kick = self.leftKick
                if pygame.sprite.collide_rect(kick, enemy):
                    enemy.health -= 1
                    if enemy.health==0:
                        enemies.remove(enemy)
                        self.allowed += self.width
                        self.checkLevel()
                    pushback = self.width//pushbackFact
                    if not self.movingRight:
                        pushback *= -1
                    enemy.rect.move_ip(pushback, 0)    
            if not enemy.punching:
                enemy.move(self.player)#simpler AI

    def bossAI(self):
        if MainScreen.level3:
            self.brolly.dodge(self.Attacks, self.movingRight) #dodges most attacks
            self.brolly.eitherOr += 1    
            if self.brolly.eitherOr %5 == 0:
                self.brolly.Punch(self.player, self.movingRight) #punches when player is in short range
            else:
                self.brolly.Kick(self.player, self.movingRight)
            if len(self.ComAttacks) == 0: 
                self.ComEnemyShoot(self.brolly)
                self.brolly.shot = True
            else:
                self.brolly.count2 += 1
                if self.brolly.count2 == 15:
                    self.brolly.shot = False
                    self.brolly.count2 = 0
                    self.moved = True
            pushbackFact = 5.55
            for blast in self.ComAttacks:
                if pygame.sprite.collide_rect(blast, self.player): 
                    pushback = -1 * self.width//pushbackFact
                    if not self.movingRight:
                        pushback *= -1
                    if self.player.rect.move(pushback, 0).left < 0:
                        pushback = -1*self.player.rect.left
                    if self.player.rect.move(pushback, 0).right > self.width:
                        pushback = self.width - self.player.rect.right
                    if not blast.damaged:
                        self.player.rect.move_ip(pushback, 0) #if hit, then moved back
                        self.punch.rect.move_ip(pushback, 0)
                        self.leftPunch.rect.move_ip(pushback, 0)
                        self.kick.rect.move_ip(pushback, 0)
                        self.leftKick.rect.move_ip(pushback, 0)
                    ##move the whole player (punches and everything)
                    if not blast.damaged:
                        self.harm += 20   
                        blast.damaged = True
                    if self.harm >= self.width//3.58:
                        self.harm = self.width//3.58
                        self.dying = True
                    self.shot = True
                if blast.rect.left > self.width*1.5:
                    self.ComAttacks.remove(blast)
                elif blast.rect.left < -.5*self.width:
                    self.ComAttacks.remove(blast)
            pushback = self.width//pushbackFact
            for kiblast in self.Attacks: #handles collisions between attacks
                if pygame.sprite.collide_rect(kiblast, self.brolly): 
                    if not self.movingRight:
                        pushback *= -1
                    self.brolly.rect.move_ip(pushback, 0) #if hit, then moved back
                    self.brolly.health -= 1   
                    if self.brolly.health == 0: #increases allowed when enemy defeated #once win, shenron appears
                        self.brolly.dying = True
                        # MainScreen.level3 = False
                        # MainScreen.wish = True
                    self.Attacks.remove(kiblast) #removes kiblast when hit
                    continue
                if kiblast.rect.left > self.width:
                    self.Attacks.remove(kiblast)
            if self.superBlast:
                for image, rect in self.superBlast.fullKame:
                    if rect.colliderect(self.brolly):
                        pushback = self.width//pushbackFact
                        if not self.movingRight:
                            pushback *= -1
                        self.brolly.rect.move_ip(pushback, 0) #if hit, then moved back
                        self.brolly.health -= 1   
                        if self.brolly.health == 0: #increases allowed when enemy defeated #once win, shenron appears
                            self.brolly.dying = True
                            # MainScreen.level3 = False
                            # MainScreen.wish = True
            if not self.punching and not self.kicking:
                if pygame.sprite.collide_rect(self.player, self.brolly):
                    self.harm += 1
            if self.harm >= self.width//3.58: ###gets 279
                self.dying = True
            if self.punching:
                if self.movingRight:
                    punch = self.punch
                else: 
                    punch = self.leftPunch
                if pygame.sprite.collide_rect(punch, self.brolly):
                    pushback = self.width//pushbackFact
                    if not self.movingRight:
                        pushback *= -1
                    self.brolly.rect.move_ip(pushback, 0) 
                    self.brolly.health -= 1   
                    if self.brolly.health == 0: #increases allowed when enemy defeated #once win, shenron appears
                        self.brolly.dying = True
                        # MainScreen.level3 = False
                        # MainScreen.wish = True

            if self.kicking:
                if self.movingRight:
                    kick = self.kick
                else:
                    kick = self.leftKick
                if pygame.sprite.collide_rect(kick, self.brolly):
                    pushback = self.width//pushbackFact
                    if not self.movingRight:
                        pushback *= -1
                    self.brolly.rect.move_ip(pushback, 0) 
                    self.brolly.health -= 1   
                    if self.brolly.health == 0: #increases allowed when enemy defeated #once win, shenron appears
                        self.brolly.dying = True
                        # MainScreen.level3 = False
                        # MainScreen.wish = True 
            if self.brolly != None and not self.brolly.punching and not self.brolly.kicked and not self.brolly.shot:
                self.brolly.move(self.player)  

            if not self.brolly.moved:
                if self.brolly.punching or self.brolly.kicked:                    
                    if self.movingRight:
                        self.player.rect.move_ip(-4, 0)
                        self.punch.rect.move_ip(-4, 0)
                        self.leftPunch.rect.move_ip(-4, 0)
                        self.kick.rect.move_ip(-4, 0)
                        self.leftKick.rect.move_ip(-4, 0)
                    else:
                        self.player.rect.move_ip(4, 0)
                        self.punch.rect.move_ip(4, 0)
                        self.leftPunch.rect.move_ip(4, 0)
                        self.kick.rect.move_ip(4, 0)
                        self.leftKick.rect.move_ip(4, 0)
                    self.brolly.count += 1
                    if self.brolly.count == 12:
                        self.brolly.count = 0
                        self.brolly.punching = False
                        self.brolly.kicked = False
                        self.brolly.moved = True
            if self.brolly.dying:
                self.brolly.count += 1
                if self.brolly.count == 20:
                    MainScreen.level3 = False
                    MainScreen.wish = True                                #smarter AI

    def checkLevel(self):
        if self.allowed == self.width*3 and MainScreen.gameScreen and not MainScreen.level3:
            self.nextLevelDelay = True
        elif self.allowed == self.width*4 and MainScreen.level2 and len(self.ComEnemies) == 0 and not MainScreen.level3:
            self.nextLevelDelay = True        #keeps count of enemies killed

    def enemyPunch(self, enemy):
        self.harm += (self.width//3.58)//6.975 ### 40
        if self.harm >= self.width//3.58:
            self.harm = self.width//3.58
            self.dying = True
        pygame.time.delay(100)
        self.jump = self.width//10
        enemy.punching = False   
        enemy.moved = True #in charge of enemy punches

    def ComEnemyShoot(self, enemy):
        for enemy in self.ComEnemies:
            enemy.Shoot(self.player)
        if MainScreen.level3:
            kiblast = ComAttacksBoss(self.brolly, 25, self.movingRight)
            self.ComAttacks.add(kiblast)    
        else:        
            kiblast = ComAttacks(enemy, 25, enemy.shootLeft)
            self.ComAttacks.add(kiblast)         #2nd level enemy shooting action

    def enemyGravity(self):
        #brings the enemy to ground level if he jumped and harms player
        if MainScreen.level2:
            enemies = self.ComEnemies
        else:
            enemies = self.Enemies
        for enemy in enemies:
            # if enemy.moved:
            #     print(enemy.rect.bottom)
            if enemy.rect.bottom < self.height*3//5+2*75:
                enemy.rect.move_ip(0,5)
            if enemy.rect.bottom > self.height*3//5+2*75:
                enemy.rect.move_ip(0,-5)
        if MainScreen.level3:
            if not self.brolly.fly:
                if self.brolly.rect.bottom < self.height*3//5+2*75:
                    self.brolly.rect.move_ip(0,5)
                if self.brolly.rect.bottom > self.height*3//5+2*75:
                    self.brolly.rect.move_ip(0,-5) #keeps AI level

#mehtod for animating gif taken from https://stackoverflow.com/questions/14044147/animated-sprite-from-few-images
    def updateGameOverScreen(self):
        self.index += 1
        if self.index >= len(self.bothbrolys):
            self.index = 0
        self.gameOverbroly = self.bothbrolys[self.index] #moving gif 

    def gameOverTransition(self):
        if MainScreen.gameScreen:
            MainScreen.gameScreen = False
        elif MainScreen.level2:
            MainScreen.level2 = False
        elif MainScreen.level3:
            MainScreen.level3 = False
        MainScreen.gameOver = True 
    
    def nextLevel(self):
        self.level += 1
        if self.allowed == self.width*3 or (MainScreen.level2 and self.allowed == self.width*4):
            MainScreen.levelOver = True
            MainScreen.gameScreen = False
            if MainScreen.level2:
                MainScreen.level2 = False
                MainScreen.level3 = True
            self.level += 1
            self.nextLevelDelay = False #keeps track of level

    def timerFired(self, dt):
        if MainScreen.gameScreen or MainScreen.level2 or MainScreen.tutorial or MainScreen.level3:
            #creates a clock and monitors the frequency some actions are preformed
            pygame.time.Clock()
            ticks = pygame.time.get_ticks()
            ################
            self.checkScroll() #makes sure the amount scrolling is allowed        
            self.checkBoundries() #boaundries for player
            self.movePLayer()
            if self.nextLevelDelay:
                self.count += 1
                if self.count == 50:
                    self.count = 0
                    self.nextLevel()
            if self.dying:
                self.count += 1
                if self.count == 30:
                    self.gameOverTransition()
            ################

            if not self.shootingSuper:   
                self.orientation()
            ###############
            if self.energy < 239: #prevents an excess amount of energy
                self.energy += self.charge
            self.gravityAndLevel()
            if not MainScreen.tutorial and not MainScreen.level3: #gives a delay 
                if len(self.ComEnemies) == 0 and self.newWave and MainScreen.level2: #creates a new enemy each round
                    self.createComEnemy()
                    self.newWave = False
                elif len(self.Enemies) == 0 and self.newWave: #creates a new enemy each round
                    self.createEnemy()
                    self.newWave = False
            ###############

            for blast in self.Attacks: #creates the direction the blasts go in - depends on orientation
                if blast.movingRight: direction = 1
                else: direction = -1
                blast.move(direction) #moves blast depending on dir
            for comBlast in self.ComAttacks: #creates the direction the blasts go in - depends on orientation
                if comBlast.shootingLeft: ######shoots left all the time
                    direction = -1
                else: direction = 1
                cy = self.player.rect.centery                
                comBlast.move(direction, cy) #moves blast depending on dir
            ###############
            if self.superBlast: #creates an ultimate attack 
                if ticks%1 == 0:
                    self.superBlast.move()
                if len(self.superBlast.fullKame) > self.width//20: #blast ends when the width is too long
                    self.superBlast = None
            self.enemyAI(ticks)
            self.enemyGravity()
            self.bossAI()
        else:
            pygame.time.Clock()
            ticks2 = pygame.time.get_ticks()
            if MainScreen.gameOver:
                if ticks2%10 == 0:
                    self.updateGameOverScreen()

    def findDifference(self, x,y,cx,cy): #used to find difference between user and other object
        return (cx-x,cy-y)

    ###########################################################################
                                ## draw functions ##
    ###########################################################################

    def drawTutorial(self, screen):
        screen.blit(self.kameHouse, (0,0))
        self.drawCharacter(screen)
        self.drawAttacks(screen)
        self.drawSuper(screen)
        drawText(screen, self.font1, self.width//2, self.height//20, "Tutorial", (222,62,2), backgroundColor = "")
        drawText(screen, self.font2, self.width//2, self.height//8, "Use the Up, Down, Left, Right Arrows to move your Character", (20,20,20))
        drawText(screen, self.font2, self.width//2, self.height*2//11, "Use 'A' to kick", (20,20,20))
        drawText(screen, self.font2, self.width//2, self.height*3//13, "Use 'D' to Punch", (20,20,20))
        drawText(screen, self.font2, self.width//2, self.height*5//17, "Use 'Space' to shoot Ki Blast", (20,20,20))
        drawText(screen, self.font2, self.width//2, self.height*3//8, "Use 'W' to shoot super attack", (20,20,20))
        drawText(screen, self.font2, self.width//2, self.height*3//8, "Use 'W' to shoot super attack", (20,20,20))
        drawText(screen, self.font2, self.width//2, self.height*4//9, "Use 'Right Shift' to fly", (20,20,20))
        drawText(screen, self.font2, self.width//2, self.height*5//9, "Press R to go to the home screen", (100,62,2))

    def drawStartScreen(self, screen, font2):
        screen.blit(self.mainBackG, (0,0))
        self.textPlay, self.playrect = drawText1(screen, font2, self.width//3.5, self.height*2//3+self.height//5, "Play", (250,134,21))
        self.textTut, self.tutrect = drawText1(screen, font2, self.width//3.5, self.height*2//3+self.height//3.75, "Tutorial", (250,134,21))
        screen.blit(self.textPlay, self.playrect)
        screen.blit(self.textTut, self.tutrect)
        screen.blit(self.logo, (0,(self.height*2//3)-self.height//6))
        pygame.display.flip()

    def drawPunching(self, screen):
        cx, cy = self.player.rect.center
        x, y = self.player.punchingRect.center
        dx, dy = self.findDifference(x,y,cx,cy)
        self.player.punchingRect.move_ip(dx,dy)
        if self.movingRight:
            screen.blit(self.player.punching, (self.player.punchingRect))
        else:
            screen.blit(pygame.transform.flip(self.player.punching, True, False), (self.player.punchingRect))

    def drawKicking(self, screen):
        cx, cy = self.player.rect.center
        x, y = self.player.kickingRect.center
        dx, dy = self.findDifference(x,y,cx,cy)
        self.player.kickingRect.move_ip(dx,dy)
        # screen.blit(self.player.kicking, (self.player.kickingRect))
        if self.movingRight:
            screen.blit(self.player.kicking, (self.player.kickingRect))
        else:
            screen.blit(pygame.transform.flip(self.player.kicking, True, False), (self.player.kickingRect))

    def drawCharacter(self, screen):
        if self.punching:
            self.drawPunching(screen)
        elif self.dying:
            if self.movingRight:
                screen.blit(self.player.dead, (self.player.rect))
            else:
                screen.blit(pygame.transform.flip(self.player.dead, True, False), (self.player.rect))               
        elif self.kicking:
            self.drawKicking(screen)
        elif self.moving:
            if self.movingRight:
                screen.blit(self.player.walking, (self.player.rect))
            else:
                screen.blit(pygame.transform.flip(self.player.leftWalking, True, False), (self.player.rect))
        elif self.leftMoving:
            if self.movingRight:
                screen.blit(self.player.leftWalking, (self.player.rect))
            else:
                screen.blit(pygame.transform.flip(self.player.walking, True, False), (self.player.rect))
        elif self.charging:
            if self.movingRight:
                screen.blit(self.player.charging, (self.player.rect))
            else:
                screen.blit(pygame.transform.flip(self.player.charging, True, False), (self.player.rect))
        elif self.shooting:
            if self.movingRight:
                screen.blit(self.player.shooting, (self.player.rect))
            else:
                screen.blit(pygame.transform.flip(self.player.shooting, True, False), (self.player.rect))
        elif self.shootingSuper:
            if self.movingRight:
                screen.blit(self.player.superMove, (self.player.rect))
            else:
                screen.blit(pygame.transform.flip(self.player.superMove, True, False), (self.player.rect))
        elif self.flying:
            if self.movingRight:
                screen.blit(self.player.flying, (self.player.rect))
            else:
                screen.blit(pygame.transform.flip(self.player.flying, True, False), (self.player.rect))
        else:
            if self.movingRight:
                screen.blit(self.player.user, (self.player.rect))
            else:
                screen.blit(pygame.transform.flip(self.player.user, True, False), (self.player.rect))

    def drawBackground(self, screen, image):
        screen.blit(image, (0-self.scrollX,0))
        if self.shifting:
            drawText(screen, self.font2, self.width//2, self.height//2, "Move Right To Fight Next Enemy", (150,20,10))
        if MainScreen.gameScreen:
            screen.blit(self.dragon3Left, (self.width-self.width//8, self.height//25))
        elif MainScreen.level2:
            screen.blit(image, (self.width*2-self.scrollX,0))
            screen.blit(image, (self.width*4-self.scrollX,0))
            screen.blit(self.dragon2Left, (self.width-self.width//8, self.height//25))
        elif MainScreen.level3:
            screen.blit(image, (self.width*2-self.scrollX,0))
            screen.blit(image, (self.width*4-self.scrollX,0))
            screen.blit(self.dragonOneLeft, (self.width-self.width//8, self.height//25))
        screen.blit(self.player.bar, (15,15))
        screen.blit(self.player.pic, (35,18))
        pygame.draw.rect(screen, (255,255,255), (164, 42, 276-self.harm, 22)) #max health = 276
        pygame.draw.rect(screen, (255,255,0), (164, 72, self.energy, 9)) #max stamina = 239


    def drawEnemies(self, screen):
        if MainScreen.level2:
            enemies = self.ComEnemies
        else:
            enemies = self.Enemies
        for enemy in enemies:
            if enemy.punching:
                if self.movingRight:
                    screen.blit(enemy.punch, (enemy.rect))
                else:
                    screen.blit(pygame.transform.flip(enemy.punch, True, False), (enemy.rect))
            else:
                if self.movingRight:
                    screen.blit(enemy.object, (enemy.rect))
                else:
                    screen.blit(pygame.transform.flip(enemy.object, True, False), (enemy.rect))

    def drawAttacks(self, screen):
        if MainScreen.level2 or MainScreen.level3:
            for blast in self.ComAttacks:
                if blast.shootingLeft and not blast.damaged:
                    screen.blit(blast.object, (blast.rect))
                elif not blast.damaged:
                    screen.blit(pygame.transform.flip(blast.object, True, False), (blast.rect))
        for blast in self.Attacks:
            if blast.movingRight:
                screen.blit(blast.object, (blast.rect))
            else:
                screen.blit(pygame.transform.flip(blast.object, True, False), (blast.rect))
    
    def drawSuper(self, screen):
        if self.superBlast != None:
            if self.movingRight:
                for image, rect in self.superBlast.fullKame:
                    screen.blit(image, rect)
            else:
                for image, rect in self.superBlast.fullKame[::-1]:
                    screen.blit(pygame.transform.flip(image, True, False), rect)
            #     screen.blit(pygame.transform.flip(self.superBlast.object, True, False), (self.superBlast.rect)) # (self.player.rect.left - self.superBlast.width, self.superBlast.y))

    def drawComEnemies(self, screen): #more complicated AIs
        for enemy in self.ComEnemies:
            if enemy.punching:
                screen.blit(enemy.punch, (enemy.rect))
            else:
                screen.blit(enemy.object, (enemy.rect))
        for blast in self.ComAttacks:
            screen.blit(blast.object, (blast.rect))

    def drawPickScreen(self, screen):
        screen.blit(self.pickBackground, (0,0))
        screen.blit(MainScreen.gokuPic, MainScreen.gokuRect)
        screen.blit(MainScreen.vegetaPic, MainScreen.vegetaRect) #(self.width-MainScreen.width, 0)
        screen.blit(self.text, (self.width//3, self.height*5//7))        
        drawText(screen, self.font2, self.width//2, self.height//8, "Choose A Character", (250,134,21))
        drawText(screen, self.font2, self.width//2, self.height//4, "Dragon Balls grant any wish,", (0,0,0))
        drawText(screen, self.font2, self.width//2, self.height*3//8, "and you have four, but need three", (0,0,0))
        drawText(screen, self.font2, self.width//2, self.height//2, "more. You must defeat the enemies", (0,0,0))
        drawText(screen, self.font2, self.width//2, self.height*5//8, "in order for your wish to be granted", (0,0,0))
        drawText(screen, self.font2, self.width//2, self.height*3//4, "or else the enemies will steal your four balls", (0,0,0))
        drawText(screen, self.font2, self.width//8, self.height*6//13, "Goku", (180,23,10))
        drawText(screen, self.font2, self.width*7//8, self.height*6//13, "Vegeta", (180,23,10))

    def drawBoss(self, screen):
        if self.brolly.punching:
            if self.movingRight:
                screen.blit(self.brolly.punchingPic, self.brolly.rect)
            else:
                screen.blit(pygame.transform.flip(self.brolly.punchingPic, True, False), self.brolly.rect)
        elif self.brolly.kicked:
            if self.movingRight:
                screen.blit(self.brolly.kicking, self.brolly.rect)
            else:
                screen.blit(pygame.transform.flip(self.brolly.kicking, True, False), self.brolly.rect)
        elif self.brolly.shot:
            if self.movingRight:
                screen.blit(self.brolly.shooting, self.brolly.rect)
            else:
                screen.blit(pygame.transform.flip(self.brolly.shooting, True, False), self.brolly.rect)
        elif self.brolly.moved:
            if self.movingRight:
                screen.blit(self.brolly.brolly, self.brolly.rect)
            else:
                screen.blit(pygame.transform.flip(self.brolly.brolly, True, False), (self.brolly.rect))
        elif self.brolly.dying:
            if self.movingRight:
                screen.blit(self.brolly.dead, self.brolly.rect)
            else:
                screen.blit(pygame.transform.flip(self.brolly.dead, True, False), (self.brolly.rect))
    def redrawAll(self, screen):
        self.font1 = pygame.font.Font("Saiyan-Sans.ttf", int(self.width//13.33))
        self.font2 = pygame.font.Font("Saiyan-Sans.ttf", int(self.width//25))
        if MainScreen.pickCharacter:
            self.drawPickScreen(screen)
        if MainScreen.startScreen:
            self.drawStartScreen(screen, self.font2)
        elif MainScreen.gameScreen:
            self.drawBackground(screen, self.scenary)
            self.drawCharacter(screen)
            self.drawEnemies(screen)
            self.drawAttacks(screen)
            self.drawSuper(screen)
            pygame.draw.line(screen, (0,0,0), (0,self.height*3//5+2*75), (self.width, self.height*3//5+2*75))
            pygame.display.flip()
        elif MainScreen.levelOver:
            screen.blit(self.endLevel, (0,0)) 
            screen.blit(self.transition, (0,0))
        elif MainScreen.level2:
            self.drawBackground(screen, self.scenaryLevel2)
            self.drawCharacter(screen)
            self.drawEnemies(screen)
            self.drawAttacks(screen)
            self.drawSuper(screen)
            pygame.draw.line(screen, (0,0,0), (0,self.height*3//5+2*75), (self.width, self.height*3//5+2*75))
            pygame.display.flip()
        elif MainScreen.level3:
            self.drawBackground(screen, self.final)
            self.drawCharacter(screen)
            self.drawAttacks(screen)
            self.drawSuper(screen)
            self.drawBoss(screen)
        elif MainScreen.wish:
            screen.blit(self.wish, (0,0))
            drawText(screen, self.font2, self.width//2, self.height//8, "What is your wish,", (200,200,200))
            self.textWish, self.wishrect = drawText1(screen, self.font2, self.width//2, self.height//2, "Get a Good Grade on the Term Project", (250,134,21))
            screen.blit(self.finished, (self.width*3//10+20,self.height*3//5))
            screen.blit(self.textWish, self.wishrect)
        elif MainScreen.gameOver:
            screen.blit(self.gameOverbroly, (0,0))
            drawText(screen, self.font2, self.width*4//5, self.height//3, "Game Over", (120,80,80))
            drawText(screen, self.font2, self.width*4//5, self.height//2, "Broly has taken", (120,80,80))
            drawText(screen, self.font2, self.width*4//5, self.height*3//5, "the dragon balls", (120,80,80))
        elif MainScreen.tutorial:
            self.drawTutorial(screen)   
        if MainScreen.won:
            screen.blit(self.grade, (self.width*3//4, 30))         

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=1000, height=600, fps=60, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)
        # stores all the keys currently being held down
        self._keys = dict()
        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                    event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            screen.convert()
            self.redrawAll(screen)
            pygame.display.flip()
        pygame.quit()


def main():
    game = MainScreen()
    game.run()

if __name__ == '__main__':
    main()