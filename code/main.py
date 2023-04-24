import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle
from pygame.locals import *

#The game class that is used to make the flappy bird game
class Game:
	def __init__(self):
		
		# setup for making the basic components to open the file
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		pygame.display.set_caption('Flappy Plane')
		self.clock = pygame.time.Clock()
		self.active = True

		#creates all sprite groups and gives the ones that need it a collision
		self.all_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()

		#scale factor for the background and the ground
		bg_height = pygame.image.load('../CSC235Final/graphics/environment/background.png').get_height()
		self.scale_factor = WINDOW_HEIGHT / bg_height

		# sprite setup 
		BG(self.all_sprites,self.scale_factor)
		Ground([self.all_sprites,self.collision_sprites],self.scale_factor)
		self.plane = Plane(self.all_sprites,self.scale_factor / 1.7)

		# timer for keeping track of the score
		self.obstacle_timer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.obstacle_timer,1400)

		# text for keeping track of the score
		self.font = pygame.font.Font('../CSC235Final/graphics/font/BD_Cartoon_Shout.ttf',30)
		self.score = 0
		self.start_offset = 0

		# menu for introducing the game and showing controls
		self.menu_surf = pygame.image.load('../CSC235Final/graphics/ui/menu.png').convert_alpha()
		self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2))

		# music that loops in the background of the game
		self.music = pygame.mixer.Sound('../CSC235Final/sounds/music.wav')
		self.music.set_volume(VOLUME * 0.05)
		self.music.play(loops = -1)
		
	#Creates collision on all sprites that need it 
	def collisions(self):
		if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False,pygame.sprite.collide_mask)\
		or self.plane.rect.top <= 0:
			for sprite in self.collision_sprites.sprites():
				if sprite.sprite_type == 'obstacle':
					sprite.kill()
			self.active = False
			self.plane.kill()

	#Displays the score in the middle top of the screen
	def display_score(self):
		if self.active:
			self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
			y = WINDOW_HEIGHT / 10
		else:
			y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

		score_surf = self.font.render(str(self.score),True,'black')
		score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2,y))
		self.display_surface.blit(score_surf,score_rect)

	#Runs the game itself and listens for any controls
	def run(self):
		last_time = time.time()
		while True:
			
			# delta time
			dt = time.time() - last_time
			last_time = time.time()

			# event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					pygame.quit()
					sys.exit()
				#Controls (Mouse Click or space or up arrow)
				if event.type == pygame.MOUSEBUTTONDOWN or (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)):
					if self.active:
						self.plane.jump()
					else:
						self.plane = Plane(self.all_sprites,self.scale_factor / 1.7)
						self.active = True
						self.start_offset = pygame.time.get_ticks()

				if event.type == self.obstacle_timer and self.active:
					Obstacle([self.all_sprites,self.collision_sprites],self.scale_factor * 1.1)
			
			# game logic for updating all components to simulate the game playing
			self.display_surface.fill('black')
			self.all_sprites.update(dt)
			self.all_sprites.draw(self.display_surface)
			self.display_score()

			if self.active: 
				self.collisions()
			else:
				self.display_surface.blit(self.menu_surf,self.menu_rect)

			pygame.display.update()
			# self.clock.tick(FRAMERATE)

print("WELCOME TO FLAPPY PLANE")
print("======================")
print("Press space or up arrow or mouse click to start the game")
print("Pressing space or up lifts or mouse click the plane upwards")
print("Press Escape to close the game")
print("----------------------")
print("Avoid the ground and the rocks to avoid losing")
print("the longer you last the more score is added")

if __name__ == '__main__':
	game = Game() #creates the game class
	game.run()	  #runs the game