## all enemies and attacks

import pygame
import random
class Enemy(pygame.sprite.Sprite): #basic enemies
	def __init__(self):
		super().__init__()
		self.health = 4
		self.object = pygame.image.load("staticFiles/saibamanStanding.png").convert_alpha()
		self.object = pygame.transform.scale(self.object, (60, 100))
		self.punching = False
		self.punch = pygame.image.load("staticFiles/saibamanPunch.png").convert_alpha()
		self.punch = pygame.transform.scale(self.punch, (60,100))
		self.rect = self.object.get_rect()
		self.topLeft = self.rect.topleft
		self.bottomRight = self.rect.bottomright
		self.centerX, self.centerY = self.rect.center 
		self.probability = (2, 5)  #2/5 chance to dodge
		self.moved = False
		self.punched = False
		self.dx = 5
		self.shotDelay = 0

	def move(self, user): #moves character
		cx, cy = user.rect.center
		x, y = self.rect.center
		direction = x - cx
		if abs(direction) < 225:
			self.rect.move_ip(self.dx, 0)
		elif abs(direction) < 800:
			if direction > 0 and self.dx > 0:
				self.dx *= -1
			elif direction <0 and self.dx < 0:
				self.dx *= -1
			self.rect.move_ip(self.dx, 0)

	def dodge(self, kiBlasts, movingRight): #detect blast and dodge
		for blast in kiBlasts:
			if movingRight:
				futureRect = blast.rect.move(10, 0)
				if self.rect.colliderect(futureRect):
					self.rect.move_ip(-40,-150)
					self.moved = True
			else:
				futureRect = blast.rect.move(-10, 0)
				if self.rect.colliderect(futureRect):
					self.rect.move_ip(40,-150)
					self.moved = True

	def Punch(self, user, movingRight): #punch if able to
		if movingRight:
			futureRect = user.rect.move(5,0)
			if self.rect.colliderect(futureRect):
				self.punching = True
		else:
			futureRect = user.rect.move(-5,0)
			if self.rect.colliderect(futureRect):
				self.punching = True

class Attacks(pygame.sprite.Sprite): #ki blasts
	def __init__(self, user, movingRight):
		super().__init__()
		self.user = user
		self.movingRight = movingRight
		self.cx, self.cy = self.user.rect.center
		self.width, self.height = self.user.user.get_size()		
		self.object = pygame.image.load("staticFiles/kiBlast.gif")
		self.object = pygame.transform.scale(self.object, (45,30))
		self.rect = self.object.get_rect()
		self.rect.move_ip(self.cx+self.width//2, self.cy-self.height//4)

	def move(self, d):
		self.rect.move_ip(5*d, 0) #directional value

class ComEnemy(Enemy): #more advanced AI
	def __init__(self, enemyNum):
		super().__init__()
		self.health = 7
		if enemyNum == 1:
			self.object = pygame.image.load("staticFiles/raditzStanding.png").convert_alpha()
			self.object = pygame.transform.scale(self.object, (60, 160))
			self.punch = pygame.image.load("staticFiles/raditzPunch.png").convert_alpha()
			self.punch = pygame.transform.scale(self.punch, (60,160))
		elif enemyNum == 2:
			self.object = pygame.image.load("staticFiles/nappaStance.png").convert_alpha()
			self.object = pygame.transform.scale(self.object, (80, 160))
			self.punch = pygame.image.load("staticFiles/nappaPunch.png").convert_alpha()
			self.punch = pygame.transform.scale(self.punch, (80,160))	
		self.shootLeft = True
		self.rect = self.object.get_rect()

	def Shoot(self, user):
		cx, cy = user.rect.center
		x, y = self.rect.center
		direction = x - cx		
		if direction > 0: #shoot to the left
			self.shootLeft = True
		else:  #shoot to the right
			self.shootLeft = False

class ComAttacks(pygame.sprite.Sprite): #enemy ki blast
	def __init__(self, user, speed, left):
		super().__init__()
		self.user = user
		self.speed = speed
		self.shootingLeft = left
		self.damaged = False
		self.cx, self.cy = self.user.rect.center
		self.width, self.height = self.user.object.get_size()		
		self.object = pygame.image.load("staticFiles/raditzBlast.gif")
		self.object = pygame.transform.scale(self.object, (45,30))
		self.rect = self.object.get_rect()
		self.rect.move_ip(self.cx+self.width//2, self.cy-self.height//4)

	def move(self, d, cy):
		centerY = self.user.rect.centery
		difference = cy - centerY
		if difference < -40:
			d2 = -1
		elif difference > 40:
			d2 = 1
		else:
			d2 = 0
		self.rect.move_ip(6*d, d2) #directional value

class ComAttacksBoss(pygame.sprite.Sprite): #enemy attack
	def __init__(self, user, speed, left):
		super().__init__()
		self.user = user
		self.speed = speed
		self.shootingLeft = left
		self.damaged = False
		self.cx, self.cy = self.user.rect.center
		self.width, self.height = self.user.brolly.get_size()		
		self.object = pygame.image.load("staticFiles/brolly/bKi.png")
		self.object = pygame.transform.scale(self.object, (45,30))
		self.rect = self.object.get_rect()
		self.rect.move_ip(self.cx+self.width//2, self.cy-self.height//4)

	def move(self, d, cy):
		centerY = self.user.rect.centery
		difference = cy - centerY
		if difference < -40:
			d2 = -1
		elif difference > 40:
			d2 = 1
		else:
			d2 = 0
		self.rect.move_ip(6*d, d2) #directional value

class SuperMove(Attacks): #super moves generated 
	def __init__(self, user, movingRight):
		super().__init__(user, movingRight)
		cx, cy = self.user.rect.center
		self.userwidth, self.userheight = self.user.user.get_size()	
		self.movingRight = movingRight	
		if user.character == "vegeta":
			self.start = pygame.image.load("staticFiles/vSuperp1.png")
			self.mid = pygame.image.load("staticFiles/vSupermid.png")
			self.last = pygame.image.load("staticFiles/vSuperp3.png")
		else:
			self.start = pygame.image.load("staticFiles/firstKame.gif")
			self.mid = pygame.image.load("staticFiles/midKame.gif")
			self.last = pygame.image.load("staticFiles/lastKame.gif")
		self.start = pygame.transform.scale(self.start, (45, 30))
		self.mid = pygame.transform.scale(self.mid, (10, 30))
		self.last = pygame.transform.scale(self.last, (45, 30))
		self.rect1 = self.start.get_rect()
		self.rect2 = self.mid.get_rect()
		self.rect3 = self.last.get_rect()
		self.fullKame = [(self.start, self.rect1), (self.mid, self.rect2), (self.last, self.rect3)]
		self.y = cy-self.userheight//4
		if self.movingRight:
			self.rect1.move_ip(cx+self.userwidth//2+30, cy-self.userheight//4)
			self.rect2.move_ip(cx+self.userwidth//2+30+40, cy-self.userheight//4)
			self.rect3.move_ip(cx+self.userwidth//2+30+50, cy-self.userheight//4)
		else:
			self.rect1.move_ip(cx-self.userwidth//2-30, cy-self.userheight//4)
			self.rect2.move_ip(cx+self.userwidth//2-30-40, cy-self.userheight//4)
			self.rect3.move_ip(cx+self.userwidth//2-30-50, cy-self.userheight//4)

	def createMid(self, x):
		cx, cy = self.user.rect.center
		if self.user.character == "goku":
			newMid = pygame.image.load("staticFiles/midKame.gif")
		else:
			newMid = pygame.image.load("staticFiles/vSupermid.png")
		newMid = pygame.transform.scale(newMid, (10, 30))
		newMidRect = newMid.get_rect()
		newMidRect.move_ip(x, cy-self.userheight//4)
		self.fullKame.append((newMid, newMidRect))
		# self.fullKame.insert(-1, (newMid, newMidRect))

	def move(self):
		last, rect0, = self.fullKame.pop()
		lastMid, rect = self.fullKame[-1]
		cx, cy = self.user.rect.center

		if self.movingRight:
			dx = 10
			x0 = rect0.left
			x = rect.right
			self.createMid(x)
		else:
			dx = -10
			x0 = rect0.right
			x = rect.left - 10
			self.createMid(x)			

		newMid, newRect = self.fullKame[-1]
		newRect3 = rect0.move(dx, 0)
		self.fullKame.append((last, newRect3))	

