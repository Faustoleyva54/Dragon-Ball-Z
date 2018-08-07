#Main character and boss

import pygame

class Player(pygame.sprite.Sprite): #two users 
	def __init__(self, character):
		super().__init__()
		self.character = character
		if self.character == "goku":
			self.user = pygame.image.load("staticFiles/goku/gStand.png").convert_alpha()
			self.punching = pygame.image.load("staticFiles/goku/gPunch.png").convert_alpha()
			self.walking = pygame.image.load("staticFiles/goku/gMoving.png").convert_alpha()
			self.leftWalking = pygame.image.load("staticFiles/goku/gMovingLeft.png").convert_alpha()
			self.dead = pygame.image.load("staticFiles/goku/gDead.png").convert_alpha()
			self.charging = pygame.image.load("staticFiles/goku/gCharge.png").convert_alpha()
			self.shooting = pygame.image.load("staticFiles/goku/gKi.png").convert_alpha()
			self.superMove = pygame.image.load("staticFiles/goku/gSuper.png").convert_alpha()
			self.flying = pygame.image.load("staticFiles/goku/gJump.png").convert_alpha()
			self.kicking = pygame.image.load("staticFiles/goku/gKick.png").convert_alpha()
			self.blocking = pygame.image.load("staticFiles/goku/gokuBlocking.png").convert_alpha()
			self.pic = pygame.image.load("staticFiles/goku/gokuProfilePic.gif").convert_alpha()
		# if character == "vegeta":
		else:
			self.user = pygame.image.load("staticFiles/vegeta/vegetaStanding.png").convert_alpha()
			self.punching = pygame.image.load("staticFiles/vegeta/vPunch.png").convert_alpha()
			self.walking = pygame.image.load("staticFiles/vegeta/vMovingRight.png").convert_alpha()
			self.leftWalking = pygame.image.load("staticFiles/vegeta/vMovingBack.png").convert_alpha()
			self.dead = pygame.image.load("staticFiles/vegeta/vDead.png").convert_alpha()
			self.charging = pygame.image.load("staticFiles/vegeta/vCharge.png").convert_alpha()
			self.shooting = pygame.image.load("staticFiles/vegeta/vShoot.png").convert_alpha()
			self.superMove = pygame.image.load("staticFiles/vegeta/vShootingSuper.png").convert_alpha()
			self.flying = pygame.image.load("staticFiles/vegeta/vFly.png").convert_alpha()
			self.kicking = pygame.image.load("staticFiles/vegeta/vKick.png").convert_alpha()
			self.blocking = pygame.image.load("staticFiles/vegeta/vBlock.png").convert_alpha()
			self.pic = pygame.image.load("staticFiles/vegeta/vPic.gif").convert_alpha()
			
		self.user = pygame.transform.scale(self.user, (75, 150))
		self.width, self.height = self.user.get_size()
		self.punching = pygame.transform.scale(self.punching, (self.width+30, self.height))
		self.punchingRect = self.punching.get_rect()		
		
		self.walking = pygame.transform.scale(self.walking, (self.width+20, self.height))
		self.leftWalking = pygame.transform.scale(self.leftWalking, (self.width+30, self.height))
		self.dead = pygame.transform. scale(self.dead, (self.height, self.width+30))

		self.charging = pygame.transform.scale(self.charging, (self.width+30, self.height))
		self.shooting = pygame.transform.scale(self.shooting, (self.width+30, self.height))
		self.superMove = pygame.transform.scale(self.superMove, (self.width+30, self.height))

		self.flying = pygame.transform.scale(self.flying, (self.width+30, self.height))		
		self.kicking = pygame.transform.scale(self.kicking, (self.width+30, self.height))
		self.blocking = pygame.transform.scale(self.blocking, (self.width+30, self.height))

		self.bar = pygame.image.load("staticFiles/bar.png")
		self.bar = pygame.transform.scale(self.bar, (450, 90))
		self.pic = pygame.transform.scale(self.pic, (100,80))

		self.kickingRect = self.kicking.get_rect()
		self.rect = self.user.get_rect()
		self.bottomRight = self.rect.bottomright
		self.centerX, self.centerY = self.rect.center


class Extent(pygame.sprite.Sprite):
	def __init__(self, user):
		super().__init__()
		self.extent = pygame.image.load("staticFiles/emptyness.png").convert_alpha()
		self.extent = pygame.transform.scale(self.extent, (40,40))
		self.rect = self.extent.get_rect()
		right, top = user.rect.topright
		self.rect.move_ip(right, top+40)

class kick(pygame.sprite.Sprite):
	def __init__(self, user):
		super().__init__()
		self.kick = pygame.image.load("staticFiles/emptyness.png").convert_alpha()
		self.kick = pygame.transform.scale(self.kick, (40,40))
		self.rect = self.kick.get_rect()
		print(self.rect)
		right, bottom = user.rect.bottomright
		self.rect.move_ip(right, bottom-40)


class Boss(pygame.sprite.Sprite): #ultimate boss
	def __init__(self):
		super().__init__()
		self.brolly = pygame.image.load("staticFiles/brolly/bStand.png").convert_alpha()
		self.punchingPic = pygame.image.load("staticFiles/brolly/bPunch.png").convert_alpha()
		self.walking = pygame.image.load("staticFiles/brolly/brollyMoving.png").convert_alpha()
		self.leftWalking = pygame.image.load("staticFiles/brolly/bMovingBack.png").convert_alpha()
		self.dead = pygame.image.load("staticFiles/brolly/bDead.png").convert_alpha()
		self.charging = pygame.image.load("staticFiles/brolly/bCharge.png").convert_alpha()
		self.shooting = pygame.image.load("staticFiles/brolly/bShoot.png").convert_alpha()
		self.superMove = pygame.image.load("staticFiles/brolly/bSuperp1.png").convert_alpha()
		self.flying = pygame.image.load("staticFiles/brolly/bfly.png").convert_alpha()
		self.kicking = pygame.image.load("staticFiles/brolly/bKick.png").convert_alpha()
		self.blocking = pygame.image.load("staticFiles/brolly/bBlock.png").convert_alpha()
		self.pic = pygame.image.load("staticFiles/brolly/bPic.gif").convert_alpha()

		self.brolly = pygame.transform.scale(self.brolly, (75, 150))
		self.width, self.height = self.brolly.get_size()
		self.punchingPic = pygame.transform.scale(self.punchingPic, (self.width+30, self.height))
		self.punchingRect = self.punchingPic.get_rect()		
		
		self.walking = pygame.transform.scale(self.walking, (self.width+20, self.height))
		self.leftWalking = pygame.transform.scale(self.leftWalking, (self.width+30, self.height))
		self.dead = pygame.transform. scale(self.dead, (self.height, self.width+30))

		self.charging = pygame.transform.scale(self.charging, (self.width+30, self.height))
		self.shooting = pygame.transform.scale(self.shooting, (self.width+30, self.height))
		self.superMove = pygame.transform.scale(self.superMove, (self.width+30, self.height))

		self.flying = pygame.transform.scale(self.flying, (self.width+30, self.height))		
		self.kicking = pygame.transform.scale(self.kicking, (self.width+30, self.height))
		self.blocking = pygame.transform.scale(self.blocking, (self.width+30, self.height))

		self.bar = pygame.image.load("staticFiles/bar.png")
		self.bar = pygame.transform.scale(self.bar, (450, 90))
		self.pic = pygame.transform.scale(self.pic, (100,80))

		self.kickingRect = self.kicking.get_rect()
		self.rect = self.brolly.get_rect()
		self.bottomRight = self.rect.bottomright
		self.centerX, self.centerY = self.rect.center
		self.dx = 5
		self.dy = -2
		self.moved = True
		self.punching = False
		self.kicked = False
		self.shot = False
		self.count = 0
		self.count2 = 0
		self.eitherOr = 0
		self.fly = False
		self.dying = False
		self.health = 13


	def move(self, user):
		cx, cy = user.rect.center
		x, y = self.rect.center
		direction = x - cx
		if abs(direction) < 225 and not self.fly:
			self.rect.move_ip(self.dx, 0)
			self.moved = True
		elif abs(direction) < 800 and not self.fly:
			if direction > 0 and self.dx > 0 and not self.fly:
				self.dx *= -1
			elif direction <0 and self.dx < 0 and not self.fly:
				self.dx *= -1
			self.rect.move_ip(self.dx, 0)
		yDirection = y - cy
		if abs(yDirection) > 50:
			if yDirection > 0:
				self.rect.move_ip(0, self.dy)
				self.moved =True
				self.fly = True
			elif yDirection < 50:
				self.fly = False
		if not user.flying:
			self.fly = False
			self.moved =True


	def Shoot(self, user): 
		cx, cy = user.rect.center
		x, y = self.rect.center
		direction = x - cx		
		if direction > 0: #shoot to the left
			self.shootLeft = True
		else:  #shoot to the right
			self.shootLeft = False

	def dodge(self, kiBlasts, movingRight):
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

	def Punch(self, user, movingRight):
		if movingRight:
			futureRect = user.rect.move(10,0)
			if self.rect.colliderect(futureRect):
				self.punching = True
				self.moved = False
		else:
			futureRect = user.rect.move(-10,0)
			if self.rect.colliderect(futureRect):
				self.punching = True
				self.moved = False
	def Kick(self, user, movingRight):
		if movingRight:
			futureRect = user.rect.move(10,0)
			if self.rect.colliderect(futureRect):
				self.kicked = True
				self.moved = False
		else:
			futureRect = user.rect.move(-10,0)
			if self.rect.colliderect(futureRect):
				self.kicked = True
				self.moved = False
